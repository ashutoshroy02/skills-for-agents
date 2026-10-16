#!/usr/bin/env node
// humanize-check - scan text for AI-writing tells.
// Zero dependencies. Node 18+.
//
//   node scripts/humanize-check.mjs <file>...      # check files
//   cat draft.md | node scripts/humanize-check.mjs # check stdin
//   node scripts/humanize-check.mjs --quiet <file> # summary only
//   node scripts/humanize-check.mjs --all <file>   # include fenced code blocks
//
// Exit code is non-zero when tells are found, so this drops into a pre-commit
// hook or a CI step unchanged.
//
// Derived from humanize-ai-writing (MIT), extended with the formatting and
// rhythm checks the original could not see.

import { readFileSync } from "node:fs";

const BANNED_WORDS = [
  "delve", "delves", "delving", "tapestry", "testament", "underscore",
  "underscores", "underscoring", "pivotal", "intricate", "intricacies",
  "meticulous", "meticulously", "garner", "garners", "garnered", "vibrant",
  "bolster", "bolsters", "bolstered", "enduring", "interplay", "crucial",
  "valuable", "exemplify", "exemplifies", "renowned", "groundbreaking", "boast",
  "boasts", "nestled", "realm", "realms", "embark", "embarks", "leverage",
  "leverages", "leveraging", "elevate", "elevates", "unlock", "unlocks",
  "unleash", "unleashes", "harness", "harnesses", "robust", "seamless",
  "seamlessly", "holistic", "myriad", "plethora", "cornerstone", "beacon",
  "paradigm", "synergy", "synergies", "showcasing", "showcases", "fostering",
  "fosters", "utilize", "utilizes", "utilizing", "additionally", "moreover",
  "furthermore", "notably", "importantly",
];

// [label, regex, suggestion]
const PHRASES = [
  ["em dash", /\u2014/g, "use a comma, period, colon, or parentheses"],
  ["curly quote", /[\u2018\u2019\u201c\u201d]/g, "use straight quotes ' \""],

  ["fake significance", /\b(stands?|serves?) as (a |an )?(testament|reminder|symbol|cornerstone)\b/gi, "say what it is and does"],
  ["fake significance", /\bmarks? a (pivotal|defining|significant|key) (moment|point|shift)\b/gi, "drop the significance editorializing"],
  ["fake significance", /\b(plays?|played) an? (vital|crucial|pivotal|key|important|central) role\b/gi, "state the concrete contribution"],
  ["fake significance", /\b(indelible mark|setting the stage|turning point|evolving landscape|deeply rooted|focal point)\b/gi, "cut the legacy framing"],
  ["fake significance", /\breflects a broader\b|\brepresents a shift\b/gi, "name the trend and a second example, or cut"],

  ["negative parallelism", /\bnot just\b[^.?!]*\bbut\b/gi, "make the positive claim directly"],
  ["negative parallelism", /\bnot only\b[^.?!]*\bbut\b/gi, "make the positive claim directly"],
  ["negative parallelism", /\bit'?s not\b[^.?!]*,\s*it'?s\b/gi, "make the positive claim directly"],
  ["negative parallelism", /\bmore than just\b/gi, "make the positive claim directly"],
  ["negative parallelism", /\brather than\b/gi, "say what it is: 'X, not Y', or drop the contrast"],

  ["promo tone", /\b(cutting-edge|world-class|state-of-the-art|best-in-class|next-generation|game-changer|revolutionary|diverse array)\b/gi, "describe a concrete capability"],
  ["promo tone", /\bcommitment to\b|\bdedication to\b|\bpassionate about\b|\bwe'?re excited to\b/gi, "write like a peer, not marketing"],

  ["copula avoidance", /\b(serves|stands|functions|acts) as\b/gi, "use is/are/has"],

  ["weasel attribution", /\b(experts?|studies|research|researchers?|observers?|critics?|sources?|reports?) (say|says|show|shows|argue|argues|note|notes|suggest|suggests|indicate|indicates|have cited|have noted)\b/gi, "name a source or cut it"],
  ["weasel attribution", /\bit is (widely |generally |commonly )?(believed|considered|known|thought|accepted)\b/gi, "name a source or cut it"],
  ["weasel attribution", /\b(many|some) (argue|believe|claim|say)\b/gi, "name a source or cut it"],

  ["notability padding", /\b(maintains?|has) an active (social media |digital |online )?presence\b/gi, "cut it or give one sourced fact"],

  ["hollow conclusion", /^(\s*#{0,6}\s*)?(in conclusion|overall|ultimately|in summary|to sum up|in short|going forward)\b/gim, "stop on the last real point"],

  ["formula section", /\bdespite (its|these|the|their)\b[^.?!]*\bchallenges?\b/gi, "drop the Despite/challenges template"],
  ["formula section", /^\s*#{1,6}\s*(future outlook|challenges and legacy|challenges and future directions|final thoughts)\b/gim, "drop the template heading"],

  ["filler phrase", /\b(in today'?s (world|fast-paced world|digital age)|when it comes to|it'?s (important|worth) (to note|noting)|needless to say|in the heart of|rich cultural heritage)\b/gi, "cut the filler"],

  ["participle padding", /,\s+(highlighting|reflecting|contributing to|showcasing|emphasizing|underscoring|demonstrating|signaling|solidifying|cementing)\b/gi, "cut it, or promote the fact to its own sentence"],

  ["copy-paste artifact", /\b(oaicite|contentReference|oai_citation|turn0search\d|grok_card|attached_file)\b/gi, "remove leftover markup"],
  ["copy-paste artifact", /:::/g, "remove leftover markup"],
  ["tracking param", /utm_source=/gi, "strip tracking params from links"],
];

const wordRegex = new RegExp(`\\b(${BANNED_WORDS.join("|")})\\b`, "gi");

// Lines inside fenced code blocks are data, not prose. A document that
// documents tells will quote them. Skipped unless --all is passed.
function fenceMask(lines) {
  const mask = new Array(lines.length).fill(false);
  let inFence = false;
  lines.forEach((line, i) => {
    if (/^\s*(```|~~~)/.test(line)) {
      mask[i] = true;
      inFence = !inFence;
      return;
    }
    mask[i] = inFence;
  });
  return mask;
}

function isTableRow(line) {
  return /^\s*\|/.test(line);
}

function checkText(text, name, opts) {
  const findings = [];
  const lines = text.split(/\r?\n/);
  const inFence = opts.all ? new Array(lines.length).fill(false) : fenceMask(lines);

  lines.forEach((line, i) => {
    if (inFence[i]) return;

    // Escape hatch for lines that legitimately quote a tell: fixtures,
    // examples, catalogs of what not to write. A quoted tell is data.
    if (/humanize-check:\s*ignore/.test(line)) return;

    const push = (type, match, col, suggestion) =>
      findings.push({ name, line: i + 1, col: col + 1, type, match, suggestion });

    // Inline code spans are identifiers, not prose. `url_hash` and
    // `oai_citation` are things being named, not words being used.
    const prose = line.replace(/`[^`]*`/g, (m) => " ".repeat(m.length));

    for (const m of prose.matchAll(wordRegex))
      push("banned word", m[0], m.index, "swap for a plain word");

    for (const [label, rx, suggestion] of PHRASES) {
      const flags = rx.flags.includes("g") ? rx.flags : rx.flags + "g";
      for (const m of prose.matchAll(new RegExp(rx.source, flags.replace("m", ""))))
        push(label, m[0], m.index, suggestion);
    }

    // Inline-header bold list: "**Term.** description" at line start.
    // The most common formatting tell in generated documents.
    const runIn = line.match(/^\s*\*\*[^*]{2,80}\*\*/);
    if (runIn && !isTableRow(line))
      push("inline-header bold", runIn[0].trim(), runIn.index || 0,
        "promote to a real heading, or fold the label into the sentence");

    // Title Case In Headings. Skip single-letter labels ("Appendix B:"),
    // acronyms, and backticked identifiers so proper nouns don't false-positive.
    const head = line.match(/^\s*#{1,6}\s+(.*)$/);
    if (head) {
      const body = head[1].replace(/^[\d.]+\s*/, "").replace(/`[^`]*`/g, "");
      const words = body
        .split(/\s+/)
        .map((w) => w.replace(/[^A-Za-z]/g, ""))
        .filter((w) => w.length > 1 && !/^[A-Z]+$/.test(w));
      const capsAfterFirst = words.slice(1).filter((w) => /^[A-Z]/.test(w));
      if (words.length >= 4 && capsAfterFirst.length >= words.length - 1)
        push("title case heading", body.slice(0, 60), 0, "use sentence case");
    }

    // Emoji or decorative glyph used as a bullet or section marker.
    // Ranges stay separate: a combined class silently widens into ASCII.
    if (/^\s*(?:[\u2022\u25aa\u25b8\u25cf\u2705\u274c\u2714\u2716\u27a4]|\p{Extended_Pictographic})/u.test(line))
      push("emoji formatting", line.trim().slice(0, 20), 0, "use a plain bullet");
  });

  return findings;
}

// Document-level checks: bold density and flat rhythm. Both are invisible
// line by line and both matter.
function checkDocument(text, name, opts) {
  const findings = [];
  const lines = text.split(/\r?\n/);
  const inFence = opts.all ? new Array(lines.length).fill(false) : fenceMask(lines);

  const prose = [];
  lines.forEach((line, i) => {
    if (inFence[i]) return;
    const s = line.trim();
    if (!s || isTableRow(s) || /^#{1,6}\s/.test(s) || s === "---" || /^\s*[-*+]\s/.test(s))
      return;
    prose.push(s);
  });

  const body = prose.join(" ");
  const words = body.split(/\s+/).filter(Boolean).length;

  // Count bold in prose only. Table cells and code blocks legitimately use it,
  // and counting them made this fire on every document with a wide table.
  const boldCount = (body.match(/\*\*/g) || []).length / 2;
  if (words > 400 && boldCount > words / 200)
    findings.push({
      name, line: 0, col: 1, type: "bold density",
      match: `${Math.round(boldCount)} bold spans in ~${words} words of prose`,
      suggestion: "prose needs almost no bold; let the sentences carry emphasis",
    });

  const sents = body.split(/(?<=[.?!])\s+/).map((s) => s.split(/\s+/).length)
    .filter((n) => n > 1);
  if (sents.length >= 25) {
    const sorted = [...sents].sort((a, b) => a - b);
    const shortShare = sorted.filter((n) => n < 8).length / sorted.length;
    if (shortShare < 0.05)
      findings.push({
        name, line: 0, col: 1, type: "flat rhythm",
        match: `shortest of ${sorted.length} sentences is ${sorted[0]} words; ${Math.round(shortShare * 100)}% under 8 words`,
        suggestion: "split a long sentence; let one idea stand alone",
      });
  }

  return findings;
}

function readInput(args) {
  const files = args.filter((a) => !a.startsWith("--"));
  if (files.length === 0) return [["<stdin>", readFileSync(0, "utf8")]];
  return files.map((f) => [f, readFileSync(f, "utf8")]);
}

// A catalog file lists tells on purpose. Scanning one and reporting hundreds of
// hits is noise, so a file may opt out with a marker on any of its first 20 lines.
function isCatalog(text) {
  return /humanize-check:\s*catalog/.test(text.split(/\r?\n/).slice(0, 20).join("\n"));
}

const args = process.argv.slice(2);
const opts = { quiet: args.includes("--quiet"), all: args.includes("--all") };
const inputs = readInput(args);

let total = 0;
let skipped = 0;
const byType = {};
for (const [name, text] of inputs) {
  if (isCatalog(text) && !opts.all) {
    skipped++;
    if (!opts.quiet) console.log(`${name}  skipped (declares itself a tell catalog)`);
    continue;
  }
  const findings = [
    ...checkText(text, name, opts),
    ...checkDocument(text, name, opts),
  ];
  total += findings.length;
  for (const f of findings) {
    byType[f.type] = (byType[f.type] || 0) + 1;
    if (!opts.quiet) {
      const loc = f.line === 0 ? `${f.name}` : `${f.name}:${f.line}:${f.col}`;
      console.log(`${loc}  ${f.type}: "${f.match}" - ${f.suggestion}`);
    }
  }
}

console.log("");
if (total === 0) {
  const note = skipped ? ` (${skipped} catalog file${skipped === 1 ? "" : "s"} skipped)` : "";
  console.log(`clean - no AI tells found.${note}`);
  process.exit(0);
}
console.log(`${total} tell${total === 1 ? "" : "s"} found:`);
for (const [type, n] of Object.entries(byType).sort((a, b) => b[1] - a[1]))
  console.log(`  ${n.toString().padStart(3)}  ${type}`);
console.log("\nNot machine-checkable, verify by eye: whether a rewrite lost meaning,");
console.log("whether a fact you added is real, and whether facts survived unchanged.");
process.exit(1);
