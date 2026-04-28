# Composability

Deep dive into how skills compose using the SIP Framework.

## Core Concepts

### Domains

Every skill owns exactly one domain:

- **Voice** — tone, personality, vocabulary
- **Density** — token count, verbosity
- **Craft** — visual design, code quality
- **Process** — workflow steps, templates
- **Content** — substance being produced

### Composition Modes

**Layered** — simultaneous application:
```
/blog + /caveman
```

**Pipeline** — sequential processing:
```
/postmortem → /compress
```

**Handoff** — skill delegates to another:
```
Postmortem detects UI issue → invokes painter
```

**Advisory** — skill references another's principles:
```
Blogger writing about UI → references painter's heuristics
```

## Precedence Rules

When skills conflict, resolution follows this order:

::: warning Priority Order
1. **Safety/Accuracy** — always wins (implicit)
2. **User's explicit instruction** — second priority
3. **Domain owner** — authoritative in its domain
4. **Most recently invoked** — last one wins
5. **Specificity** — narrow scope beats broad scope
:::

## The Composition Contract

Every SIP-compliant skill must follow these rules:

::: details Composition Contract
1. **Input Agnosticism** — operate on any input
2. **Domain Respect** — don't modify other domains
3. **Marker Preservation** — keep structure intact
4. **Signal Emission** — state what you're handling
5. **Graceful Degradation** — defer when conflicting
:::

## Examples

### Example 1: Voice + Density

**User:** "Write a blog, make it terse"

**Skills:** Blogger (voice) + Caveman (density)

**Resolution:** Caveman density wins. Blogger's voice preserved in fewer words.

### Example 2: Process + Density

**User:** "Run postmortem, then compress it"

**Skills:** Postmortem (process) → Compress (density)

**Resolution:** Pipeline. Postmortem structure preserved, content compressed.

### Example 3: Craft + Voice

**User:** "Blog about UI decisions"

**Skills:** Blogger (voice) + Painter (craft, advisory)

**Resolution:** Blogger owns voice. Painter validates technical claims.

## Conflict Resolution Matrix

| Skill A | Skill B | Resolution |
|---------|---------|------------|
| Blogger (voice) | Caveman (density) | Caveman wins, blogger voice preserved |
| Postmortem (process) | Compress (density) | Pipeline: structure preserved, content compressed |
| Painter (craft) | Blogger (voice) | Painter advisory, blogger owns voice |

## Best Practices

1. **Declare domain clearly** — don't try to own multiple
2. **Yield to process** — structure is sacred
3. **Preserve upstream work** — keep structure intact
4. **Signal boundaries** — state what you handle
5. **Test composition** — ensure works with other skills

## Resources

- [SIP Framework](/guide/sip-framework) — full specification
- [Creating Skills](/guide/creating-skills) — build SIP-compliant skills
- [PROTOCOL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/PROTOCOL.md) — source
