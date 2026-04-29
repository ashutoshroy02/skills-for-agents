# Creating Skills

Build your own composable skills that work seamlessly with the ecosystem.

## What Makes a Good Skill?

A skill is a **dense compression of expertise into instructions an AI can follow**. The best skills are:

1. **Opinionated** — they make decisions so the AI doesn't have to reinvent them every time
2. **Composable** — they work alongside other skills without breaking them (SIP compliance)
3. **Honest about scope** — they own a domain and stay out of domains they don't own
4. **Explanatory** — they explain *why*, not just *what* (LLMs respond to reasoning)
5. **Lean** — every line earns its place

## Quick Start

Use the **skill-creator** skill:

```
/create-skill "skill for X"
```

It will interview you, generate the skill structure, and ensure SIP compliance.

## Manual Creation

### Step 1: Choose a Domain

Every skill owns exactly one domain:

| Domain | Controls | Examples |
|--------|----------|----------|
| **Voice** | Tone, personality, vocabulary | Blogger |
| **Density** | Token count, verbosity | Caveman, Compress |
| **Craft** | Visual design, code quality | Painter, Harden |
| **Process** | Workflow steps, templates | Memory, Postmortem |
| **Content** | Substance being produced | Documenter, Researcher |

**Rule:** Don't try to own multiple domains. Pick one.

### Step 2: File Structure

```
skill-name/
├── SKILL.md              ← Required. Main instruction set.
├── references/           ← Optional. Deep-dive docs.
│   └── detailed-guide.md
├── scripts/              ← Optional. Helper scripts.
│   └── helper.py
├── templates/            ← Optional. Reusable templates.
│   └── template.md
└── examples/             ← Optional. Usage examples.
    └── example-output.md
```

Only `SKILL.md` is required.

### Step 3: SKILL.md Structure

Every SKILL.md has two parts:

#### Part 1: Frontmatter (YAML)

```yaml
---
name: skill-name                    # lowercase-with-hyphens
description: >                      # THE triggering mechanism. Be pushy.
  What this skill does. When to use it. Include specific trigger phrases.
  Must be < 1000 characters total.
domain: voice | density | craft | process | content
composable: true                    # almost always true
yields_to: [process, craft]         # domains this skill defers to
---
```

**Critical:** The `description` field determines whether the skill activates. Make it pushy. Instead of "Helps with X" write "Use this whenever the user mentions X, wants Y, or is working with Z."

#### Part 2: Content (Markdown)

```markdown
# Skill Title

[1-2 sentence identity statement]

---

## When to Use

[Bullet list of activation scenarios. Be generous.]

---

## Core Instructions

[The heart of the skill. Clear, actionable, opinionated.
 Use imperative voice. Explain WHY, not just WHAT.]

---

## [Domain-Specific Sections]

[Whatever the skill needs — patterns, rules, references]

---

## Boundaries

[What this skill does NOT do]

---

## Composability — Working With Other Skills

[Required. Full SIP compliance section.]
```

### Step 4: SIP Compliance

Every skill must end with a composability section. Use this template:

```markdown
## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

\`\`\`yaml
domain: [the domain]
composable: true
yields_to: [domains this skill defers to]
\`\`\`

[Skill name] owns **[domain]** — [one sentence on what exactly it controls].

### When [Skill Name] Leads

- [Primary scenario 1]
- [Primary scenario 2]

### When [Skill Name] Defers

| Other Skill's Domain | What [Skill Name] Does |
|---------------------|------------------------|
| **[Domain]** | [Concrete: what it preserves, what it hands off] |

### Layered Composition Rules

1. **[This domain] + [Other domain]**: [Who handles what, where the boundary is]

### Pipeline Behavior

- **Upstream**: [How it handles pre-processed input]
- **Downstream**: [What downstream skills should expect]

### Conflict Signal

If [specific tension]:

> `⚠️ [Domain] conflict: [what's conflicting]. [resolution].`
```

## Writing Rules

### 1. Explain the Why

LLMs respond better to reasoning than commands.

**Bad:** "ALWAYS use expo-out easing"

**Good:** "Use expo-out easing because linear and ease feel mechanical — the human eye expects objects to decelerate as they settle, matching physical reality."

### 2. Use the Imperative

"Check authentication" not "You should check authentication"

### 3. Be Specific Over Generic

`cubic-bezier(0.16, 1, 0.3, 1)` beats `use a smooth easing curve`

### 4. Show, Don't Describe

```markdown
❌ Bad: "Write clear error messages"

✅ Good:
  Before: "Error occurred"
  After:  "Payment failed: card ending 4242 was declined. Try a different card."
```

### 5. Keep It Lean

Every sentence should earn its place. Dense > verbose.

### 6. No Throat-Clearing

Don't start with "In this skill, we will..." Just start with the instructions.

## Size Guidelines

| Skill Type | SKILL.md Lines | Sections |
|-----------|---------------|----------|
| **Focused** (single pattern) | 50–150 | Core + Composability |
| **Standard** (workflow/domain) | 150–350 | Full structure |
| **Comprehensive** (knowledge base) | 350–500 | Full + reference files |

If you're past 500 lines, you need reference files.

## The `yields_to` Decision

This is the hardest part. Think through it carefully:

- A voice skill yields to `[process, craft]` because structure and design outrank tone
- A density skill yields to `[process]` because you can't compress away required structure
- A process skill yields to `[]` because the skeleton is sacred
- A craft skill yields to `[voice, process]` because it doesn't control tone or workflow order
- Safety/Accuracy always wins — it's implicit, never listed

## Testing Your Skill

### Mental Test

Pick 2-3 realistic user prompts. Walk through how the skill would handle them. Identify gaps.

### Composition Test

Test with at least 2 other skills:
- Does it preserve their output?
- Does it defer correctly?
- Do conflicts resolve as expected?

### Anti-Pattern Check

- [ ] No ALWAYS/NEVER/MUST without reasoning
- [ ] No vague instructions ("make it good")
- [ ] No novel-length SKILL.md without reference files
- [ ] No island behavior (missing composability)
- [ ] No domain duplication with existing skills

## Skill Anti-Patterns

### ❌ The Vague Skill

```markdown
## Instructions
Make the code better.
```

**Fix:** Be specific. What does "better" mean? Faster? More readable? Pick one and give concrete steps.

### ❌ The Dictator Skill

```markdown
ALWAYS do X. NEVER do Y. MUST follow Z.
```

**Fix:** Explain the reasoning. `Use X because Y` is more powerful than `ALWAYS use X`.

### ❌ The Novel Skill

A 2000-line SKILL.md that tries to teach everything in one file.

**Fix:** Extract to reference files. SKILL.md is the router, not the encyclopedia.

### ❌ The Island Skill

A skill with no composability section.

**Fix:** Every skill composes. Add the section.

### ❌ The Copycat Skill

A skill that duplicates another skill's domain.

**Fix:** Either merge them or make one yield to the other.

## Audit Checklist

### Frontmatter
- [ ] `name` matches folder name
- [ ] `description` is pushy enough to trigger reliably
- [ ] `description` is < 1000 characters
- [ ] `domain` is declared and correct
- [ ] `composable: true`
- [ ] `yields_to` is thoughtfully chosen

### Content Quality
- [ ] Instructions use imperative voice
- [ ] WHYs are explained alongside WHATs
- [ ] Examples are realistic and helpful
- [ ] No throat-clearing or filler sections
- [ ] Under 500 lines (or uses reference files)

### SIP Compliance
- [ ] Composability section exists and is complete
- [ ] Domain declaration matches frontmatter
- [ ] "When Leads" scenarios are specific
- [ ] "When Defers" table has concrete contracts
- [ ] Conflict signal template defined

## Examples

### Minimal Skill (Focused)

```yaml
---
name: json-formatter
description: >
  Formats JSON output with proper indentation and syntax highlighting.
  Use whenever user requests JSON output or mentions "format json".
domain: craft
composable: true
yields_to: [process]
---

# JSON Formatter

Format JSON with 2-space indentation and syntax highlighting.

## When to Use

- User requests JSON output
- User says "format json", "pretty print json"
- JSON appears in output

## Core Instructions

Always format JSON with:
- 2-space indentation (not tabs)
- Syntax highlighting in code blocks
- Trailing commas removed
- Keys sorted alphabetically (unless order matters)

\`\`\`json
{
  "key": "value",
  "nested": {
    "array": [1, 2, 3]
  }
}
\`\`\`

## Boundaries

- Does NOT validate JSON schema
- Does NOT transform data structure
- Only formats existing JSON

## Composability — Working With Other Skills

[Full SIP section here]
```

### Standard Skill (Workflow)

See existing skills like [Postmortem](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/postmortem/SKILL.md) or [Refactor](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/refactor/SKILL.md).

## Next Steps

1. **Use skill-creator** — `/create-skill` for guided creation
2. **Study existing skills** — see how they structure content
3. **Test composition** — ensure your skill works with others
4. **Submit PR** — contribute to the ecosystem

## Resources

- [Skill Creator](../skills/skill-creator) — meta-skill for creating skills
- [SIP Framework](./sip-framework) — composability rules
- [Best Practices](../reference/best-practices) — advanced patterns
- [Anatomy](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skill-creator/anatomy.md) — structural patterns
- [Evaluation](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skill-creator/evaluation.md) — quality frameworks
