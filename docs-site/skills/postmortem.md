# Postmortem

Blameless incident documentation. Structured reports with 5 Whys and action items.

## Domain

**Process** — workflow, template, required sections, review checklist, file structure.

## When to Use

- `/postmortem`
- "incident review", "post-incident", "blameless review"
- "what broke and why", "SEV1/SEV2 report"
- Any production incident documentation

## What It Creates

File: `postmortem/YYYY-MM-DD-<slug>.md` (gitignored)

Sections:
- TL;DR (impact snapshot)
- Timeline (precise, UTC/IST)
- Root Cause (5 Whys with evidence)
- Detection (what worked, what didn't)
- Response (time to resolve, responders)
- Lessons (went well, went wrong, got lucky)
- Action Items (P0/P1/P2 with owners)

## Blameless Culture

**Never blame people. Always blame systems.**

| Don't Say | Say Instead |
|-----------|-------------|
| "Alice pushed broken code" | "Deploy lacked canary stage" |
| "Bob missed it in review" | "Review checklist didn't cover infra changes" |
| "On-call was slow" | "Alert threshold too high to fire early" |

## Workflow

1. **Gather context** — incident details, timeline, metrics
2. **Generate report** — fill template with 5 Whys
3. **Review pass** — check blamelessness, completeness
4. **Save** — gitignored file, action items created

## Composability

```yaml
domain: process
composable: true
yields_to: []
```

Process owns structure — nobody overrides it.

## Related Skills

- [Blogger](./blogger) — turn postmortem into blog post
- [Compress](./compress) — shrink report for storage
- [Painter](./painter) — if incident was UI-related (advisory)

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/postmortem/SKILL.md)
