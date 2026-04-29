# Researcher

Deep web research skill. Diverse sources, cross-referencing, synthesis.

## Domain

**Content** — substance of gathered information, sources, synthesis, findings.

## When to Use

- "research X", "find info about Y", "what's the latest on Z"
- "look up", "investigate", "gather context on"
- "how does X work", "compare X vs Y"
- "deep dive", "explore topic"

## Search Strategy

### Phase 1: Official Sources
- Official docs
- GitHub repos
- Release notes / changelogs

### Phase 2: Community Knowledge
- English tech blogs
- **Chinese tech blogs** (ablations, hardware insights)
- Academic sources (arxiv)
- Community discussions (Reddit, HN, Stack Overflow)

### Phase 3: Specialized
- Benchmarks and comparisons
- GitHub issues and PRs
- Conference talks and videos

## Output Formats

- **Context Feed** — quick (5-7 sources)
- **Overview** — medium (10-15 sources)
- **Deep Dive** — comprehensive (20-30 sources)
- **Comparison** — decision-focused
- **Hypothesis Test** — adversarial (stress-test ideas)
- **Debug/Optimize** — diagnostic

## Why Chinese Blogs?

Chinese ML community publishes extensive ablation studies, benchmark comparisons, and optimization techniques often not found in English sources. Critical for TPU, GPU, distributed training research.

## Composability

```yaml
domain: content
composable: true
yields_to: [process, voice]
```

## Related Skills

- [Documenter](./documenter) — structures research into docs
- [ML Engine](./ml-engine) — implements research findings
- [Blogger](./blogger) — turns research into blog posts

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/researcher/SKILL.md)
