# SIP Framework

**Skills Interoperability Protocol** — the shared contract that teaches all skills how to compose, layer, pipeline, and defer to each other.

## Core Principle

> A skill owns its **domain**. It does not own the **conversation**.

When multiple skills are active, each one handles its domain and stays out of the others'. No skill overrides another. No skill assumes it's the only one running.

## Domains

Every skill has a **domain** — the specific aspect of output it controls.

| Domain | Controls | Example Skills |
|--------|----------|----------------|
| **Voice** | Tone, vocabulary, personality | Blogger |
| **Density** | Token count, verbosity | Caveman, Compress |
| **Craft** | Visual design, code quality | Painter, Harden |
| **Process** | Workflow steps, templates | Memory, Postmortem, Refactor |
| **Content** | Substance being written | Documenter, Researcher |

**Rule:** If two skills share a domain, the most recent invocation wins. If ambiguous, ask.

## Composition Modes

### Mode A: Pipeline (Sequential)

One skill's output feeds into the next. Order matters.

```
/postmortem → /compress
```

Flow: postmortem generates report → compress shrinks it

**Signal words:** "then", "after that", "once done", "now compress it"

### Mode B: Layered (Simultaneous)

Multiple skills apply to the same output at once, each handling its domain.

```
/blog + /caveman
```

Flow: blogger handles voice + content, caveman handles density

**Signal words:** "in X mode", "using X", "with X", simultaneous invocation

### Mode C: Handoff (Delegated)

One skill recognizes it needs another skill's capability and explicitly calls for it.

```
Postmortem: "This incident involved a UI regression. 
             Invoking painter for the visual audit section."
```

**Signal:** Skill detects content outside its domain that another skill could handle better.

### Mode D: Advisory (Consult)

A skill references another skill's principles without fully activating it.

```
Blogger: Writing a technical blog about UI decisions.
         References painter's heuristics for accuracy,
         but voice stays in blogger's domain.
```

**Signal:** Domain overlap in content (not output style).

## Precedence Rules

When skills conflict, resolve with this hierarchy:

1. **Safety/Accuracy** — always wins. Implicit and absolute. No skill can override this.
2. **User's explicit instruction** — second priority. "Write this in caveman mode" means caveman density overrides blogger's default verbosity.
3. **Domain owner** — each skill is authoritative in its domain. Voice conflicts → voice skill wins.
4. **Most recently invoked** — if two skills share a domain and no explicit priority, the last one invoked takes precedence.
5. **Specificity** — a skill with narrow scope beats a skill with broad scope in the overlap area.

## The Composition Contract

Every skill MUST follow these rules to be composable:

### 1. Input Agnosticism

A skill must operate on output from ANY other skill. Don't assume your input is raw user text — it might be pre-processed.

### 2. Domain Respect

Never modify aspects outside your domain:
- **Voice skills**: don't restructure layout or process steps
- **Density skills**: don't change tone, personality, or factual content
- **Craft skills**: don't rewrite prose that isn't UI copy
- **Process skills**: don't impose voice or density preferences

### 3. Marker Preservation

If a skill produces structured output (tables, code blocks, frontmatter, templates), downstream skills must preserve that structure.

Compress the content INSIDE structures, not the structures themselves.

### 4. Signal Emission

When a skill recognizes it's in a multi-skill context, it should:
- State which domain it's handling
- Note if it's deferring on any aspect
- Flag conflicts it can't resolve alone

### 5. Graceful Degradation

If a skill can't fully operate alongside another, it should:
1. Identify the conflict
2. Apply the precedence rules
3. Note what was deferred: `[density deferred to caveman]`

## Conflict Resolution Matrix

| Skill A | Skill B | Conflict | Resolution |
|---------|---------|----------|------------|
| Blogger (voice) | Caveman (density) | Blogger wants 600-1200 words; caveman wants minimal | Caveman density wins, blogger voice/personality preserved in fewer words |
| Blogger (voice) | Postmortem (process) | Blogger hates headers like "Introduction"; postmortem needs structured sections | Postmortem structure wins (process domain), blogger voice applies within sections |
| Painter (craft) | Blogger (voice) | Blog post about UI decisions | Painter is advisory — provides technical accuracy for UI claims. Blogger owns the voice |
| Caveman (density) | Compress (density) | Both want to reduce tokens | Most recently invoked wins. If simultaneous: caveman for live responses, compress for files |
| Postmortem (process) | Compress (density) | Postmortem generates report, compress shrinks it | Pipeline: postmortem first, compress second. Structure preserved, content compressed |

## Multi-Skill Invocation Syntax

```bash
# Explicit chaining
/blog technical | /caveman lite
→ Blogger writes technical post, caveman lite compresses output

# Layered invocation
/postmortem + /caveman
→ Postmortem runs full workflow, output compressed by caveman

# Natural language
"Write a blog post about the UI fix, in caveman mode, 
 and make sure the code examples follow painter standards"
→ blogger (voice) + caveman (density) + painter (craft, advisory only)

# Sequential
"Run a postmortem on the outage, then blog about it"
→ postmortem (process) → blogger (voice + content)
```

**Operators:**
- `|` = pipeline (sequential)
- `+` = layered (simultaneous)
- Natural language = parsed by context

## Future Skill Integration

New skills automatically integrate by:

1. **Declaring their domain** in SKILL.md frontmatter
2. **Following the composition contract** (above)
3. **Referencing this protocol** so they know how to yield and compose

No existing skill needs to be updated when a new skill is added. The protocol handles it.

## Domain Declaration (Frontmatter)

```yaml
---
name: my-skill
description: >
  What this skill does. When to use it. Specific triggers.
domain: voice | density | craft | process | content
composable: true
yields_to: [list of domain types this skill defers to]
---
```

## Anti-Patterns

**Don't:**
- ❌ Hardcode references to specific other skills
- ❌ Override another skill's domain silently
- ❌ Assume you're the only skill running
- ❌ Drop structured output from upstream skills
- ❌ Refuse to operate because another skill's output "looks weird"
- ❌ Double-process (if input is already compressed, don't compress again)

**Do:**
- ✅ Check if your domain is already handled — defer if so
- ✅ Preserve structure you didn't create
- ✅ State what you're handling and what you're not
- ✅ Accept pre-processed input gracefully
- ✅ Flag conflicts explicitly rather than silently resolving

## The Litmus Test

> Can two skills that have never seen each other's code work together on a single user request without breaking each other's output?

If yes, the protocol works. If no, one of them is violating the composition contract.

## Examples

### Example 1: Layered Composition

**User:** "Write a blog about TPU training, make it terse"

**Skills activated:**
- Blogger (voice) — handles personality, tone, structure
- Caveman (density) — compresses output
- ML Engine (content, advisory) — provides technical accuracy

**Result:** A blog post in Shaurya's voice, compressed to ~50% normal length, with accurate TPU details.

**How it works:**
1. Blogger generates full post (600-1200 words)
2. Caveman compresses it (300-600 words)
3. ML Engine validates technical claims (advisory only)

### Example 2: Pipeline Composition

**User:** "Run a postmortem on the DB outage, then compress it"

**Skills activated:**
- Postmortem (process) — generates structured report
- Compress (density) — shrinks the file

**Result:** A postmortem report in `postmortem/YYYY-MM-DD-slug.md`, then a compressed version.

**How it works:**
1. Postmortem generates full report (structure + content)
2. Compress reads the file, compresses prose, preserves structure
3. Output: compressed report with all sections intact

### Example 3: Conflict Resolution

**User:** "Write a casual blog post with proper structure"

**Skills activated:**
- Blogger (voice) — casual tone
- Postmortem (process, implied) — structured sections

**Conflict:** Blogger hates formal headers. Postmortem needs them.

**Resolution:** Postmortem structure wins (process domain). Blogger applies casual voice within sections.

**Result:** Structured report with casual prose.

## Best Practices

1. **Declare your domain clearly** — don't try to own multiple domains
2. **Yield to process** — structure is sacred, don't restructure it
3. **Preserve upstream work** — if input has tables/code/structure, keep it
4. **Signal your boundaries** — state what you handle and what you don't
5. **Test composition** — ensure your skill works with at least 2 other skills

## Resources

- [Creating Skills](/guide/creating-skills) — build SIP-compliant skills
- [Best Practices](/reference/best-practices) — advanced composition patterns
- [PROTOCOL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/PROTOCOL.md) — full spec
