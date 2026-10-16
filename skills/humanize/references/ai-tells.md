# AI tells, full detection catalog

<!-- humanize-check: catalog -->

Detection reference. Source: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

One tell is weak evidence. Clusters are strong. Scan for all of these, then read the
composite signal section at the end before concluding anything.

---

## 1. Language and word choice

**High-frequency vocabulary.** These words cluster. Finding one means looking for more
nearby, usually in the same paragraph.

By era, which is useful for dating a draft:

| Period | Words |
|---|---|
| 2023 to mid-2024 | additionally, delve, intricate, intricacies, garner, pivotal, testament, underscore, tapestry, vibrant, meticulous |
| mid-2024 to mid-2025 | align with, enhance, emphasizing, fostering, highlighting, showcasing |
| Grok-leaning | causal, empirical, correlate, underscore, "X rather than Y" |

The full banned list lives in SKILL.md rule 1, with replacements.

**Copula avoidance.** Replacing is and are with serves as, marks, features, represents,
functions as, stands as, offers, refers to. Conspicuous because a person reaches for "is".

**Elegant variation.** Cycling synonyms to avoid repeating a word: "the author, the writer,
the wordsmith". Reads forced. In technical writing it is worse than forced, because the
reader starts wondering whether two different things are under discussion.

**Promotional buzzwords.** vibrant, rich, nestled, boasts, showcasing, cutting-edge,
world-class, state-of-the-art, seamless, robust, holistic.

---

## 2. Sentence structure

**Negative parallelism.** "Not only X but also Y", "it's not X, it's Y", "X rather than Y",
"more than just". A top tell, and the one that survives most rewrite passes because each
instance looks reasonable in isolation. Count them across the whole document.

**Rule of three.** Auto-grouping into three adjectives or phrases to fake depth: "fast,
reliable, and scalable". Real writing uses the count the meaning needs, and varies it.

**Present-participle padding.** Trailing "-ing" clauses claiming significance with no
evidence: "..., enhancing its role as a dynamic hub", "..., contributing to the socio-economic
development of the region".

**Uniform sentence length.** Not in the original catalog, and worth adding. Generated prose
converges on medium-length sentences and stays there. A section where every sentence runs
sixteen to twenty-two words reads machine-made even when every word is right. Check the
shortest sentence in a long section: if it is over twelve words, the rhythm is flat.

---

## 3. Fake significance and analysis

**Undue emphasis on legacy.** "stands as", "marks a pivotal moment", "symbolizing its
ongoing", "leaves an indelible mark", "enduring testament".

**Superficial depth.** Vague statements about "broader implications", "philosophical
questions", "what it means to..." with nothing behind them.

**The challenges formula.** "Despite its [positives], [subject] faces challenges typical
of... but continues to thrive", followed by future speculation.

**Future and potential speculation.** "future investments could", "potential expansions
might", "has shaped emerging policy discussions". Unfounded and unfalsifiable.

---

## 4. Tone and voice

**Promotional and press-release.** "commitment to", "dedication to", "ensuring",
"passionate about", "we're excited to", "revolutionary".

**Cultural-heritage over-emphasis.** Repeatedly reminding the reader of "rich history",
"spiritual significance", "cultural heritage", including where it is irrelevant.

**Active social media presence.** A post-2024 idiosyncrasy: "maintains a strong digital
presence, particularly on Instagram".

---

## 5. Hedging and attribution

**Weasel attribution.** "experts say", "studies show", "observers have noted", "researchers
treat X as", "it is widely believed", "many argue". No named source anywhere.

**Exaggerated source quantity.** Presenting one or two sources as "widely held", or "such
as X and Y" implying a longer list that does not exist.

---

## 6. Formatting and structure

This category catches as many drafts as vocabulary does, and a word-list scanner sees none
of it.

- Title Case In Headings, where sentence case belongs.
- Excessive boldface for mechanical emphasis.
- Inline-header vertical lists: `**Standard Saws**: used for...`. The single most common
  formatting tell in generated documents, and the easiest to miss because the prose around
  it can be good.
- Em dashes. Overuse is flagged. Rewrite with a comma, period, colon, or parentheses.
- Curly and smart quotes where straight quotes belong. Usually a paste artifact.
- Emoji as bullets or section markers.
- Markdown leaking where it does not belong: stray asterisks, hashtags in plain text.
- Skipped heading levels, or a horizontal rule before every single heading.

### 6b. Formula sections

- "Despite its [positives], it faces challenges..." as a section opening.
- Headings named "Future Outlook", "Challenges and Legacy", "Challenges and Future
  Directions", "Final Thoughts", which end a piece on vague positive speculation.

---

## 7. Copy-paste artifacts

`contentReference`, `oaicite`, `oai_citation`, `:::writing`, `turn0search0`, a bare `+1`,
`attached_file`, `grok_card`, links pointing at search queries, `utm_source=` inside
citation URLs, invalid DOI or ISBN, citations with no page numbers, named refs never used.

---

## 8. Hollow conclusions

"In conclusion", "Overall", "Ultimately", "In summary", "To sum up", "In short", "Going
forward". Closing paragraphs that restate the piece. Section summaries that recap what the
reader just read two paragraphs ago.

---

## 9. Historical and fading tells

"As an AI, I...", "I cannot...", didactic disclaimers, abrupt mid-sentence cut-offs,
end-of-section recaps. Rare in current models, still worth a look.

---

## Weak on their own

Per Wikipedia, these are weak evidence in isolation. Do not treat any of them as proof, and
when rewriting, do not mangle meaning to purge a single instance.

- One "AI vocabulary" word. A single "vibrant" is not a verdict.
- Promotional tone by itself. People write marketing copy too.
- **AI-detector tool output.** High error rates in both directions. They flag human text
  constantly, and clear machine text regularly. Never cite a detector score as evidence,
  and never promise a user that a document will pass one.

---

## Composite signal

Confidence rises sharply when several cluster: AI vocabulary, plus superficial analysis,
plus promotional tone, plus excessive bold, plus Title Case, plus inline-header lists.

Human judgment on a single sentence is close to chance. Pattern-matching the clustered list
is what works.

When generating rather than auditing, the rule is simpler: do not produce these patterns at
all.
