# Rewrite rules, the fix for each tell

<!-- humanize-check: catalog -->

Every tell in `ai-tells.md` with its fix and a before and after. Preserve meaning and facts.
When a claim has no source, cut it. Never fabricate a replacement.

---

## Banned vocabulary, to plain words

**Before:** "This delve into the intricate tapestry underscores its pivotal role."
**After:** "This shows why it matters."

Swaps: delve to look at, intricate to complex or detailed, underscore to show, pivotal to
key, leverage to use, foster to build or encourage, robust to strong or reliable, utilize to
use, myriad to many or the actual number.

---

## Fake significance, to what it is

**Before:** "The library stands as a testament to the city's enduring commitment to
learning."
**After:** "The library opened in 1931 and holds 200,000 volumes."

Cut "stands as", "serves as a testament", "pivotal moment", "indelible mark". State the
fact. If there is no fact available, the sentence was carrying nothing.

---

## Present-participle padding, cut or convert

**Before:** "The station opened in 1890, contributing to the region's growth."
**After:** "The station opened in 1890. Freight traffic tripled within a decade."

Only if the second sentence is true. Otherwise stop after the first.

The test: delete the clause. Nothing lost means it was padding. Something lost means it was
a fact, so give it its own sentence.

---

## Negative parallelism, to a direct claim

**Before:** "It's not just a phone, it's a lifestyle."
**After:** "The phone syncs your calendar, health data, and home devices."

**Before:** "Not only fast but also reliable."
**After:** "Fast and reliable." Or pick the one that matters.

**Before:** "We chose Postgres rather than MongoDB."
**After:** "We chose Postgres." Or "We chose Postgres, not MongoDB," if the contrast carries
information.

Vary the fix across a document. Sixty instances of "rather than" all converted to ", not"
have traded one machine pattern for another, and the second one is more obvious because it
is rarer in real writing.

---

## Rule of three, to the real count

**Before:** "Affordable, scalable, and future-proof."
**After:** "Cheaper than the alternatives, and it scales." Two real points.

---

## Punctuation and typography

**Em dashes.** Avoid them. Rewrite with a comma, period, colon, or parentheses.

**Before:** "The tools you use — Slack, GitHub, Linear — sync automatically."
**After:** "The tools you use, like Slack, GitHub, and Linear, sync automatically."

Replace curly quotes and apostrophes with straight ones. Remove bold used for emphasis.
Headings to sentence case. No emoji as bullets.

**Inline-header bold lists** get their own treatment, because they are the most common
formatting tell and the fix depends on what the label was doing.

Label doing structural work, promote it:

```
BEFORE  **URL normalisation.** Duplicate detection depends on...
AFTER   #### URL normalisation

        Duplicate detection depends on...
```

Label doing only emphasis, fold it in:

```
BEFORE  **Fails by.** No connection means the row stays pending.
AFTER   Failure cases: no connection means the row stays pending.
```

Expect a slight word-count rise. The sentence now carries what the formatting carried.

---

## Copula avoidance, back to is and are

**Before:** "Gallery 825 serves as the association's exhibition space."
**After:** "Gallery 825 is the association's exhibition space."

Swap back: serves as, stands as, represents, features, maintains, boasts, functions as, all
to is, are, or has.

---

## Notability padding, cut it

**Before:** "She has been profiled in major outlets and maintains an active social media
presence."
**After:** Delete it. Or state one concrete sourced fact: "Her 2024 talk has 2M views."

---

## Promotional tone, to peer voice

**Before:** "Our cutting-edge platform is committed to delivering world-class, seamless
experiences."
**After:** "The platform loads in under a second and works offline."

---

## Weasel attribution, name it or cut it

**Before:** "Experts say the method is widely used."
**After:** "A 2023 Stanford survey found 60% of teams use it." Only if that source is real.

No source exists, delete the sentence. Never invent one to satisfy this rule. Inventing a
citation to fix a style problem is a much worse defect than the style problem.

---

## Hollow conclusion, end on the last real point

**Before:** "In conclusion, this tool offers many benefits and has a bright future ahead."
**After:** Delete it. Stop at the final concrete sentence.

---

## Rhythm, vary it

Break up uniform medium-length sentences. Add a short one. Allow a fragment.

**Before:** "The system is fast and reliable. The interface is clean and modern. The pricing
is fair and transparent."
**After:** "The system is fast. The interface is clean, the pricing fair, and nothing about
either is clever."

Let a key term repeat instead of cycling synonyms.

---

## Technical documents, three extra rules

Not in the source material, and necessary once this runs on specifications.

**Leave normative text alone.** Requirement statements, acceptance criteria, API schemas,
error codes, and code blocks are specifications. An ambiguity introduced there is a defect,
not a style improvement. Rewrite the prose around them.

**Quoted bad writing is data.** A banned word inside an example of what not to write must
stay. Never "fix" a fixture, an example, or a quotation.

**Identifiers are not prose.** `url_hash`, `POST /v1/items`, `snake_case_names`. Leave them
exactly as they are, even when a word inside them is on the banned list.

---

## What not to do while humanizing

- Do not add slang or fake casualness to sound human. That is its own tell.
- Do not change facts, numbers, names, dates, or the author's position.
- Do not pad to hit a length. Shorter is usually more human.
- Do not replace one banned word with another banned word.
- Do not delete real information to purge a flagged word. Rewrite cleanly, or leave it.
