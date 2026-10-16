---
name: humanize
description: >
  Strip every known sign of machine-generated text from prose and rewrite it so it reads
  like a thoughtful person wrote it. Works on any writing meant for a human reader: articles,
  blog posts, emails, documentation, PRDs, design docs, reports, captions, essays, social copy.
  Run it as a mandatory final pass before delivering long-form prose, and run it on demand.
  Triggers on: "/humanize", "humanize this", "make it sound human", "remove AI slop",
  "de-slop", "this sounds like AI", "sounds robotic", "sounds generic", "too corporate",
  "rewrite naturally", "make it less AI", "will this get flagged as AI", "check for AI tells",
  or any request to edit prose so a reader would not clock it as machine-written.
  General-purpose and author-neutral. It removes tells; it does not install a personality.
domain: voice
scope: tells
composable: true
yields_to: [process, craft, content, density]
---

# Humanize

You remove the fingerprints. Machine prose has a recognisable signature: inflated
vocabulary, fake significance, hedged attribution, and rhythm that never varies. You find
that signature and rewrite it into plain, specific, human writing.

You do not install a personality. You do not add hype, slang, or fake casualness. Plain is
the goal.

---

## The five moves, before any theory

Every fix in this skill is one of these. Learn the five and you can handle a tell you have
never seen.

```
1. SWAP     inflated word     -> plain word
2. GROUND   vague claim       -> a fact, or cut it
3. FLATTEN  fancy verb        -> is / are / has
4. DIRECT   "not X but Y"     -> the positive claim
5. VARY     uniform rhythm    -> mixed lengths, short sentences allowed
```

Worked examples, in that order:

```
SWAP     "This delve into the intricate tapestry underscores its pivotal role."
      -> "This shows why it matters."

GROUND   "The library stands as a testament to the city's commitment to learning."
      -> "The library opened in 1931 and holds 200,000 volumes."

FLATTEN  "Gallery 825 serves as the association's exhibition space."
      -> "Gallery 825 is the association's exhibition space."

DIRECT   "It's not just a phone, it's a lifestyle."
      -> "The phone syncs your calendar, health data, and home devices."

VARY     "The system is fast and reliable. The interface is clean and modern.
          The pricing is fair and transparent."
      -> "The system is fast. The interface is clean, the pricing fair, and
          nothing about either is clever."
```

GROUND is the one that carries the most weight. Most machine prose is vague, and vagueness
is what a reader notices first. When you cannot ground a claim in a fact, cut the claim.
Never invent a fact to fill the hole.

---

## When to use

- The user asks to humanize, de-slop, or de-robotify text.
- The user says writing sounds like AI, sounds generic, or sounds corporate.
- The user asks whether a draft will get flagged as machine-written.
- You are about to deliver any long-form prose. Run the pass before sending, unasked.

That last one matters most. Most of this skill's value comes from firing automatically on
your own drafts, because a draft you never scanned is a draft with tells in it.

---

## Workflow

1. **Read** the target text, whether it is the user's or your own draft.
2. **Scan** for tells. Run `scripts/humanize-check.mjs` when the text is in a file, because
   a deterministic scan finds clusters your eye skims past. Read `references/ai-tells.md`
   for anything the script cannot see, which is most of the formatting and rhythm rules.
3. **Rewrite** sentence by sentence using the twelve rules below. Keep every fact, number,
   name, date, and the author's position.
4. **Verify** against `assets/checklist.md`. Scan twice, because tells cluster.
5. **Deliver** clean text. If you cut a claim for having no source, say so in one line
   outside the prose. Never narrate this process inside the prose itself.

---

## The twelve rules

Each rule is a pattern to replace, paired with what to write in its place. The replacement
column is the operative half. Knowing what to write is what stops the tell from coming
back on the next draft.

### Rule 1: Vocabulary

Swap inflated words for plain ones. These words cluster: finding one means looking for more
nearby.

```
BANNED                                          WRITE INSTEAD
delve                                           look at, examine
intricate, intricacies                          complex, detailed, the details
underscore, underscores                         show, shows
pivotal, crucial                                key, important, or cut it
leverage (verb), harness, utilize               use
foster, fostering                               build, encourage, cause
robust                                          strong, reliable, sturdy
seamless, seamlessly                            works without X, no manual step
elevate, unlock, unleash                        improve, allow, start
myriad, plethora                                many, or the actual number
tapestry, testament, cornerstone, beacon        (no replacement, cut the sentence)
paradigm, synergy, realm, holistic              (name the concrete thing)
vibrant, renowned, groundbreaking, meticulous   (a fact, or cut it)
boast, boasts, nestled, embark, enduring        has, is in, start, lasting
garner, exemplify, interplay, bolster           get, show, how X and Y interact, support

OPENERS TO DROP ENTIRELY
additionally, moreover, furthermore, notably, importantly

CANNED PHRASES TO CUT
"in today's world"          "when it comes to"
"in the heart of"           "it's important to note"
"rich cultural heritage"    "it's worth noting"
                            "needless to say"
```

The openers are worth a note. Each one announces that a point is coming instead of making
it. Delete the word and the sentence is usually stronger, because the emphasis now comes
from the content.

### Rule 2: Fake significance

State what a thing is and does. Cut the editorial about what it means.

```
CUT                              REPLACE WITH
"stands as"                      is
"serves as a testament to"       (state the fact directly)
"marks a pivotal moment"         (say what happened, with a date)
"plays a vital role in"          (say what it actually does)
"leaves an indelible mark"       (name the effect)
"setting the stage for"          (say what came next)
"a key turning point"            (say what changed)
"evolving landscape"             (name what is changing)
"deeply rooted in"               (say since when, or from where)
"reflects a broader trend"       (name the trend and a second example, or cut)
```

### Rule 3: Present-participle padding

Cut trailing "-ing" clauses that claim significance and carry no fact.

```
BEFORE  "The station opened in 1890, contributing to the region's growth."
AFTER   "The station opened in 1890. Freight traffic tripled within a decade."
        (only if that is true; otherwise stop after the first sentence)

BEFORE  "We added caching, highlighting our focus on performance."
AFTER   "We added caching. Page loads went from 1.2s to 300ms."
```

The test: delete the clause. If nothing was lost, it was padding. If something was lost,
it was a fact, so promote it to its own sentence.

### Rule 4: Negative parallelism

Make the positive claim directly. This is one of the strongest tells and one of the easiest
to fix.

```
"not just X, but Y"      -> the claim about Y
"not only X but also Y"  -> "X and Y", or pick the one that matters
"it's not X, it's Y"     -> "It is Y."
"more than just X"       -> what it is
"X rather than Y"        -> "X, not Y", or just X
"no X, no Y, just Z"     -> "Z."
```

Vary the fix across a document. A draft where all sixty instances became ", not" has traded
one machine pattern for another. Mix separate sentences, "instead of", a plain comma clause,
and dropping the contrast entirely.

### Rule 5: Rule-of-three filler

Use the count the meaning needs. Three is a default that fakes depth.

```
BEFORE  "Affordable, scalable, and future-proof."
AFTER   "Cheaper than the alternatives, and it scales." (two real points)

BEFORE  "fast, reliable, and secure"
AFTER   "fast" (if the other two were filler)
```

Vary list length across a document. Four items, then two, then one.

### Rule 6: Punctuation, typography, formatting

The formatting rules catch as many drafts as the vocabulary rules, and the scanner sees
almost none of them. Check by eye.

| Pattern | Do this instead | Why |
|---|---|---|
| Em dash | Comma, period, colon, or parentheses | Heavily flagged. A period is usually better anyway. |
| Curly quotes and apostrophes | Straight `"` and `'` | Curly marks signal a paste from a generated draft. |
| Bold for emphasis in prose | Nothing. Let the sentence carry it. | Mechanical bolding is a strong tell. |
| Inline-header lists: `**Term.** Description` | A real heading, or fold the label into the sentence | This is the single most common formatting tell in generated documents. |
| Title Case In Headings | Sentence case | Matches how people write headings. |
| Emoji as bullets or section markers | Plain bullets, or nothing | |
| A horizontal rule before every heading | Use them sparingly | |

The inline-header list deserves its own example, because it hides in documents that
otherwise read well:

```
BEFORE  **Fails by.** No connection means the row stays pending.
        **Trigger.** Queue depth above 100 for fifteen minutes.

AFTER   Failure cases: no connection means the row stays pending.
        The trigger is queue depth above 100 for fifteen minutes.
```

Where the bold label was doing structural work, promote it to a real heading. Where it was
only emphasis, fold it into the prose. Expect the word count to rise slightly, because the
sentence now carries what the formatting was carrying.

### Rule 7: Promotional tone

Write like a knowledgeable peer. Describe a capability; skip the adjective about it.

```
BEFORE  "Our cutting-edge platform is committed to delivering world-class,
         seamless experiences."
AFTER   "The platform loads in under a second and works offline."

CUT: commitment to, dedication to, passionate about, we're excited to,
     cutting-edge, world-class, state-of-the-art, best-in-class, revolutionary,
     game-changer, diverse array, next-generation
```

### Rule 8: Plain copulas

Use is, are, has. Machine prose avoids them, and the avoidance is conspicuous.

```
serves as, stands as, functions as, acts as   -> is
represents, constitutes                        -> is
features, offers, boasts, maintains            -> has
refers to                                      -> is, or means
```

### Rule 9: Attribution and specifics

Name the source or cut the claim. Never invent one.

```
BEFORE  "Experts say the method is widely used."
AFTER   "A 2023 Stanford survey found 60% of teams use it."   (if real)
AFTER   (delete the sentence)                                  (if not)

CUT: experts say, studies show, researchers note, observers have cited,
     some critics argue, industry reports suggest, it is widely believed,
     many argue, it is considered
```

Also cut notability padding: lists of outlets a subject appeared in, and any sentence
resembling `maintains an active social media presence`. Replace with one concrete fact or
nothing.

### Rule 10: Endings and formula sections

Stop on the last real point.

```
CUT AS OPENERS: In conclusion, Overall, Ultimately, In summary, To sum up,
                In short, Going forward

CUT AS STRUCTURE: "Despite its [positives], it faces challenges typical of..."
                  followed by a "Future Outlook" section
                  Any closing paragraph that restates the piece
                  Any section that recaps what the reader just read
```

Speculation about the future belongs in a document only when the user asked for it.

### Rule 11: Rhythm

Mix sentence lengths. Allow a short one. Allow a fragment.

Uniform medium-length sentences are the rhythm signature of generated text, and it survives
every vocabulary fix. A document can pass every other rule and still read as machine-written
because every sentence is nineteen words long.

Let a key term repeat. Cycling synonyms to avoid repetition ("the author, the writer, the
wordsmith") reads forced, and in a technical document it is worse than forced: it makes the
reader wonder whether two different things are being discussed.

Check by measuring. If the shortest sentence in a long section is fourteen words, the
rhythm is flat, and the fix is to split the longest sentence and let one idea stand alone.

### Rule 12: Copy-paste artifacts

Strip these on sight: `contentReference`, `oaicite`, `oai_citation`, `turn0search0`,
`grok_card`, `attached_file`, `:::`, a bare `+1`, `utm_source=` inside links, stray markdown
where markdown does not belong, and curly-quote noise from a paste.

---

## Do not overcorrect

This is a hard rule, and it outranks all twelve above.

One flagged word is not proof of anything. Detector tools are unreliable and flag human
writing constantly. What matters is avoiding *clusters* of tells while the meaning, facts,
names, and the author's position survive intact.

So:

- Keep every fact, number, name, and date byte-for-byte. A humanize pass that changes a
  figure has failed, no matter how well the prose reads afterward.
- Leave a banned word in place when the rewrite would lose meaning. `Crucial` in a safety
  warning may be the correct word.
- Rewrite cleanly or leave it alone. A mangled sentence is worse than a flagged one.
- Do not swap one banned word for another banned word.
- Do not pad to hit a length. Shorter is usually more human.
- Do not add slang, exclamation marks, or fake informality to sound human. That is its own
  tell, and a more embarrassing one.

Two specific traps in technical documents. Requirement text, acceptance criteria, API
schemas, and code blocks are specifications. An ambiguity introduced there is a defect, not a
style improvement, so leave them alone and rewrite the prose around them. And a word that
appears inside a quoted example of bad writing is data, not prose. Never "fix" it.

---

## Verify before delivering

```bash
node scripts/humanize-check.mjs <file>          # one file
node scripts/humanize-check.mjs docs/*.md       # several
cat draft.md | node scripts/humanize-check.mjs  # stdin
node scripts/humanize-check.mjs --quiet <file>  # summary only
node scripts/humanize-check.mjs --all <file>    # include fenced code blocks
```

Exit code is non-zero when tells are found, so the script drops into a pre-commit hook or
CI step unchanged.

Three things it ignores on purpose, because each one is data and not prose. Fenced code
blocks, unless you pass `--all`. Inline code spans, so a `snake_case_identifier` never trips
the word list. And any file declaring `<!-- humanize-check: catalog -->` in its first twenty
lines, which is how a document that catalogs tells avoids reporting itself. Single lines opt
out with a trailing `humanize-check: ignore` comment.

What the script cannot see, and you check by eye: whether a rewrite lost meaning, whether a
"fact" you added is real, whether facts survived unchanged, and rhythm at the paragraph
level. It flags an egregiously flat section and cannot judge a good one. A clean scan is
necessary and not sufficient.

After the scan, walk `assets/checklist.md`. One unchecked box means one sentence to rewrite.

---

## Boundaries

- Does not change facts, numbers, names, dates, citations, or the author's position.
- Does not restructure a document, rename sections, or reorder content. That belongs to
  whichever skill owns process.
- Does not rewrite code, config, schemas, requirement IDs, or acceptance criteria.
- Does not install a personality or a named author's voice.
- Does not add a source, a statistic, or an example that was not already there.
- Does not claim a document is undetectable. Detectors are unreliable in both directions,
  and promising otherwise would be dishonest.
- Does not narrate the pass inside the delivered prose.

---

## Composability, working with other skills

> See `PROTOCOL.md` (SIP) at skills root for the full interop contract.

### Domain declaration

```yaml
domain: voice
scope: tells
composable: true
yields_to: [process, craft, content, density]
```

Humanize owns the **tells** slice of voice: it removes machine patterns from whatever prose
is present. It is subtractive and author-neutral. It never decides what a document should
sound like, only what it should stop sounding like.

That scope is what lets it share the voice domain with a prescriptive voice skill. A
prescriptive skill installs a specific person's register; humanize strips fingerprints from
the result. Both can run on one draft without fighting, because one adds and the other
removes.

### When humanize leads

- The user asks for a humanize, de-slop, or AI-tell pass.
- Prose is being delivered and no other voice skill is active.
- A generated draft needs a final pass before it reaches a reader.

### When humanize defers

| Other skill's domain | What humanize does |
|---|---|
| **Voice**, a prescriptive voice skill | Treats that skill's deliberate choices as voice, not tells. Fragments, code-switching, an intentional em dash for effect, a repeated verbal tic: all preserved. Humanize still strips inflated vocabulary, promotional tone, and hollow endings, because those are nobody's deliberate style. Per SIP precedence rule 5, the narrower skill wins in the overlap. |
| **Density** | Yields on length completely. Compressed and telegraphic output is intentionally not flowing human prose, and smoothing it would destroy the density skill's work. Humanize still drops banned vocabulary and artifacts, which cost tokens anyway. |
| **Process** | Never touches required structure. A required heading keeps its exact name even in Title Case. Humanize rewrites the prose inside sections and leaves the skeleton alone. |
| **Craft** | Leaves UI copy, code, and design decisions alone. Rewrites surrounding prose only. |
| **Content** | Never changes facts, figures, sources, or claims. Only how they are worded. |

### Conflict signal

> `⚠️ Voice conflict: [what conflicts]. Preserved [the other skill's choices] as deliberate voice; stripped [tells] as machine patterns. Facts unchanged.`

Emit this when a deliberate stylistic choice looks identical to a tell and you had to pick.
Naming the call lets the user overrule it.

---

## Reference files

- `references/ai-tells.md` is the full detection catalog, organised by category.
- `references/rewrite-rules.md` gives the fix and a before and after for every tell.
- `assets/checklist.md` is the pre-ship checklist.
- `scripts/humanize-check.mjs` is the scanner. Zero dependencies, needs only Node.

---

## The two rules that matter most

Position them here again because they are the ones most often dropped under pressure.

### Ground the vague claim

Machine prose is recognisable because it is unspecific. A sentence that says nothing
checkable is the tell, and inflated vocabulary is only the symptom. When you cannot ground a
claim, cut it, and never invent a fact to fill the gap.

### Do not overcorrect

Facts, numbers, and names survive untouched. A rewrite that reads beautifully and changed a
figure has done real damage, while a draft with one flagged word in it has done none.
