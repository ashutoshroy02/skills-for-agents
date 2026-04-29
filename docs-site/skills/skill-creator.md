# Skill Creator

Meta-skill for creating, auditing, and improving other skills.

## Domain

**Process** — workflow for creating, improving, and auditing skills.

## When to Use

- `/create-skill`, "make a skill", "turn this into a skill"
- "new skill", "skill for X"
- "improve this skill", "audit this skill"
- User describes repeatable workflow: "I wish this was automatic"

## What It Does

### Creation Pipeline

1. **Capture Intent** — interview user, extract requirements
2. **Write Skill** — generate SKILL.md with proper structure
3. **SIP Compliance** — ensure composability section complete
4. **Review & Iterate** — test, check anti-patterns, refine

### Improvement

- Audit existing skills for SIP compliance
- Check for anti-patterns
- Identify gaps and edge cases
- Retrofit composability sections

## File Structure Created

```
skill-name/
├── SKILL.md              ← Main instruction set
├── references/           ← Optional deep-dive docs
├── scripts/              ← Optional helper scripts
├── templates/            ← Optional templates
└── examples/             ← Optional usage examples
```

## Skill Anti-Patterns Detected

- ❌ The Vague Skill (no specifics)
- ❌ The Dictator Skill (ALWAYS/NEVER without reasoning)
- ❌ The Novel Skill (2000+ lines, no references)
- ❌ The Island Skill (no composability section)
- ❌ The Copycat Skill (duplicates existing domain)

## Composability

```yaml
domain: process
composable: true
yields_to: []
```

Skill-creator owns the meta-process of building skills.

## Related Skills

- Creates all other skills
- Audits all other skills for SIP compliance

## Resources

- [Full SKILL.md](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skill-creator/SKILL.md)
- [Anatomy](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skill-creator/anatomy.md)
- [Evaluation](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skill-creator/evaluation.md)
- [Improvement Guide](https://github.com/IsNoobgrammer/skills-for-agents/blob/main/skill-creator/improvement-guide.md)
