# Caveman

Ultra-terse communication mode. Cuts token usage ~75% while keeping full technical accuracy.

## Domain

**Density** — controls token count, verbosity, compression level of live responses.

## When to Use

- User says "caveman mode", "talk like caveman", "use caveman"
- User wants "less tokens", "be brief", token efficiency
- Explicit invocation: `/caveman [level]`

## Intensity Levels

| Level | Reduction | Style | Use When |
|-------|-----------|-------|----------|
| **lite** | ~30% | No filler/hedging. Keep articles + full sentences. Professional but tight. | Light cleanup, keep readability |
| **full** | ~50% | Drop articles, fragments OK, short synonyms. Classic caveman. | General compression, good balance |
| **ultra** | ~75% | Abbreviate (DB/auth/config), arrows for causality (X → Y), one word when enough. | Maximum compression, telegraphic |

## Examples

### Question: "Why does my React component re-render?"

**lite:**
> Your component re-renders because you create a new object reference each render. Wrap it in `useMemo`.

**full:**
> New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`.

**ultra:**
> Inline obj prop → new ref → re-render. `useMemo`.

### Question: "Explain database connection pooling."

**lite:**
> Connection pooling reuses open connections instead of creating new ones per request. Avoids repeated handshake overhead.

**full:**
> Pool reuse open DB connections. No new connection per request. Skip handshake overhead.

**ultra:**
> Pool = reuse DB conn. Skip handshake → fast under load.

## What Gets Dropped

### Always Removed
- Articles: a, an, the (when meaning survives)
- Filler: just, really, basically, actually, simply
- Pleasantries: sure, certainly, of course, happy to
- Hedging: might, perhaps, maybe, possibly
- Throat-clearing: before we begin, first of all, let's dive in

### Pattern

```
[thing] [action] [reason]. [next step].
```

**Not:** "Sure! I'd be happy to help you with that. The issue you're experiencing is likely caused by..."

**Yes:** "Bug in auth middleware. Token expiry check use `<` not `<=`. Fix:"

## Auto-Clarity

Caveman mode drops for:
- Security warnings
- Irreversible action confirmations
- Multi-step sequences where fragment order risks misread
- User confused

Resume caveman after clear part done.

**Example — destructive op:**
> **Warning:** This will permanently delete all rows in the `users` table and cannot be undone.
> ```sql
> DROP TABLE users;
> ```
> Caveman resume. Verify backup exist first.

## Boundaries

- Code/commits/PRs: write normal
- "stop caveman" or "normal mode": revert
- Level persist until changed or session end

## Composability

### Domain Declaration

```yaml
domain: density
composable: true
yields_to: [process]
```

Caveman owns **density** — token count, verbosity, compression level of live responses. NOT file compression (that's compress skill's job).

### When Caveman Leads

- Any request for terse/compressed responses
- When token efficiency is the priority
- When user explicitly invokes caveman mode

### When Caveman Defers

| Other Skill's Domain | What Caveman Does |
|---------------------|-------------------|
| **Voice** | Compress, but preserve voice markers. If a voice skill says use "sed" for disappointment — keep "sed." Don't replace it with a shorter word. Compress the FILLER, not the PERSONALITY. |
| **Process** | Compress content inside the structure. Never drop required sections, template fields, or structural elements. A 5-step workflow stays 5 steps — each step just gets tighter. |
| **Craft** | Don't compress craft-critical details. If a craft skill specifies `cubic-bezier(0.16, 1, 0.3, 1)`, keep it exact. Compress the explanation around it. |
| **Safety/Clarity** | Auto-clarity rules ALWAYS override density. Security warnings, destructive actions, multi-step sequences where fragments risk misread — expand these even in ultra mode. |

### Layered Composition Rules

1. **Density + Voice**: Compress filler, keep personality tokens. Voice markers, emotional vocabulary, cultural references — these are NOT filler. They're payload.

2. **Density + Process**: Compress within cells, not the table. Compress within steps, not the step count. The skeleton of a process skill's output is sacred — the meat can be lean.

3. **Density + Craft**: Technical precision is not compressible. `ease-out` ≠ `easing`. `4.5:1 contrast ratio` ≠ `good contrast`. Keep exact values, compress surrounding prose.

## Commands

```bash
/caveman lite   # Light cleanup
/caveman full   # Classic caveman (default)
/caveman ultra  # Maximum compression

stop caveman    # Revert to normal mode
normal mode     # Same as above
```

## Tips

1. **Start with lite** — get comfortable before going full/ultra
2. **Use for iteration** — caveman mode great for rapid back-and-forth
3. **Not for final docs** — use for working sessions, expand for deliverables
4. **Compose with voice** — caveman + blogger = terse posts in authentic voice
5. **Check comprehension** — if user confused, auto-clarity kicks in

## Related Skills

- [Compress](./compress) — file compression (caveman for files)
- [Blogger](./blogger) — voice skill that composes well with caveman
- [Documenter](./documenter) — content skill that yields to caveman

## Resources

- [SIP Framework](/guide/sip-framework) — how caveman composes
- [Best Practices](/reference/best-practices) — advanced patterns
