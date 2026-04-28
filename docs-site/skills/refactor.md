# Refactor

Restructure messy codebases into clean, modular architecture.

## Domain

**Process** — structural organization, architectural skeleton.

## When to Use

- "refactor my project", "clean up my code"
- "split this file", "restructure my files"
- Codebase is monolithic or messy

## What It Does

- Splits oversized files (>300 lines)
- Establishes modular folder structure
- Extracts duplicated logic
- Enforces single responsibility
- Preserves all functionality (no breaking changes)

## Workflow

1. **Analyze** — map project, identify files >300 lines
2. **Plan** — new folder structure, file-by-file mapping
3. **Execute** — refactor files, update imports
4. **Verify** — all routes/UI preserved, no file >300 lines

## Hard Limits

- No file >300 lines
- Every function <80 lines
- Single responsibility per file

## Composability

```yaml
domain: process
composable: true
yields_to: []
```

## Related Skills

- [Harden](./harden) — use after refactor for production patterns
- Refactor = WHERE code lives, Harden = WHAT goes inside

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/refactor/SKILL.md)
