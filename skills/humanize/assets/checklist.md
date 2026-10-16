# Pre-ship checklist

<!-- humanize-check: catalog -->

Run before delivering any prose. One unchecked box means one sentence to rewrite.

Run the scanner first, then walk this list. The scanner catches rules 1 to 5, most of 7 to
10, and rule 12. Rules 6 and 11 and the final-pass section are eye-only.

```bash
node scripts/humanize-check.mjs <file>
```

---

## The twelve

- [ ] **1. Vocabulary.** None of: delve, tapestry, testament, underscore, pivotal, intricate,
  meticulous, garner, vibrant, bolstered, enduring, interplay, crucial, valuable, exemplify,
  renowned, groundbreaking, boasts, nestled, realm, embark, leverage, elevate, unlock,
  harness, robust, seamless, holistic, myriad, cornerstone, paradigm, synergy. No openers:
  additionally, moreover, furthermore, notably, importantly. No "in today's world", "in the
  heart of", "rich cultural heritage", "it's important to note", "it's worth noting".

- [ ] **2. No fake significance.** No "stands as", "serves as a testament", "pivotal
  moment", "indelible mark", "setting the stage", "turning point", "evolving landscape",
  "deeply rooted".

- [ ] **3. No -ing padding.** No trailing "..., highlighting / reflecting / contributing to..."
  clauses that add no fact.

- [ ] **4. No negative parallelism.** No "not just X but Y", "not only... but also", "it's not
  X, it's Y", "no X, no Y, just Z", "X rather than Y". Counted across the whole document,
  not per paragraph.

- [ ] **5. No forced triples.** List length matches the real number of points, and varies
  across the document.

- [ ] **6. Punctuation and formatting.** No em dashes. Straight quotes only. Almost no bold,
  and zero inline-header bold lists. Sentence-case headings. No emoji as formatting.
  *(Eye-only. The scanner sees the bold and the heading case, nothing else here.)*

- [ ] **7. No promo tone.** No "commitment to", "cutting-edge", "world-class", "passionate
  about", "we're excited to", "diverse array".

- [ ] **8. Plain copulas.** Used is, are, has. Not serves as, stands as, represents,
  features, maintains, offers, boasts.

- [ ] **9. No weasel or notability padding.** Every "experts say / studies show / observers
  have cited / some critics argue" is either named or cut. No media-coverage lists. No
  "active social media presence". No source invented to satisfy this box.

- [ ] **10. No hollow conclusion or formula.** No "In conclusion / Overall / Ultimately / In
  summary". No "Despite its... faces challenges... Future Outlook". No future speculation unless
  it was asked for.

- [ ] **11. Rhythm.** Sentence lengths vary. At least one short sentence per long section.
  Repetition allowed over synonym-cycling. *(Eye-only, though the scanner flags an
  egregiously flat section.)*

- [ ] **12. No artifacts.** No oaicite, contentReference, turn0search0, `:::`, utm_source=,
  curly quotes, stray markdown.

---

## Final pass

- [ ] Facts, numbers, names, dates, and citations are unchanged from the source. Verify by
  diffing if the document is long.
- [ ] Did not overcorrect. No real information deleted to purge a word.
- [ ] Requirement text, acceptance criteria, code blocks, schemas, and identifiers are
  untouched.
- [ ] Quoted examples of bad writing were left as-is. A fixture is data, not prose.
- [ ] No fabricated source, statistic, or example was added.
- [ ] Reads like a knowledgeable person wrote it, not a brand and not a machine.
- [ ] Did not claim the result is undetectable. Detectors are unreliable in both directions.
