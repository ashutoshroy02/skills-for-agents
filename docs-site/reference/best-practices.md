# Best Practices

Advanced patterns for using and creating skills.

## Composition Patterns

### Layered Composition

Use when multiple skills should apply simultaneously:

```
/blog technical + /caveman lite
```

Result: Technical blog post in compressed format.

### Pipeline Composition

Use when one skill's output feeds into the next:

```
/postmortem → /compress
```

Result: Postmortem report, then compressed version.

### Natural Language

Let the AI detect skills automatically:

```
"Write a blog about the UI incident, make it terse"
```

Detected: blogger (voice) + caveman (density) + postmortem (content)

## Skill Selection

### Start Simple

Use one skill at a time until you understand it.

### Compose Gradually

Add skills one by one, test each addition.

### Check Domains

Ensure skills don't conflict (different domains = safe).

## Common Workflows

### Documentation

```
/researcher + /documenter
```

Researcher gathers context, documenter structures it.

### Production Code

```
/refactor → /harden
```

Refactor establishes structure, harden adds production patterns.

### Incident Response

```
/postmortem → /compress → /blog
```

Document incident, compress report, write blog post.

### ML Research

```
/ml-engine + /researcher
```

Researcher finds prior work, ml-engine implements experiments.

## Troubleshooting

### Skill Not Triggering

Check the skill's `description` field. It lists trigger phrases.

### Skills Conflicting

Check their domains. If both are same domain, specify which wins.

### Output Too Verbose

Add density skill: `/caveman lite`

### Output Too Terse

Remove density skills: `stop caveman`

## Advanced Techniques

### Explicit Precedence

```
/skill1 (primary) + /skill2
```

### Conditional Activation

Some skills auto-activate based on context (e.g., memory on startup).

### Skill Chaining

```
/skill1 → /skill2 → /skill3
```

Each skill processes the previous output.

## Resources

- [SIP Framework](/guide/sip-framework) — composability rules
- [Creating Skills](/guide/creating-skills) — build your own
- [Skills](/skills/) — available skills
