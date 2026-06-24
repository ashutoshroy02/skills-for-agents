<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: nothing (drives the interview)</span>
</div>

# No Doubts

Relentlessly interview the user about a plan, design, or topic until you reach shared understanding — checkpointing every answer to a brainstorm file so nothing is lost as context fills up.

## When to Use

- User wants to stress-test a plan or get grilled on a design
- Running a brainstorm or discovery session
- Extracting what's in the user's head into a durable doc

## Triggers

```
"grill me", "no doubts", "any doubts", "stress test this", "what am I missing"
"poke holes", "challenge this", "steel man this", "red team this plan"
```

## How It Works

- **The capture file is the point.** A brainstorm file at `brainstorms/{date}-{topic}.md` is the source of truth — not the agent's context.
- **Checkpoint after every answer.** Before asking the next question, the agent appends the key facts, decisions, and open flags. Never batches.
- **One question at a time**, each with a recommended answer so the user can confirm, correct, or redirect.
- Walks down each branch of the decision tree, resolving dependencies one by one.

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Stress-test a design</div>
<div class="example-desc">Grill an architecture before committing to it.</div>

```
"Grill me on this caching design before I build it."

The agent creates brainstorms/2026-06-24-caching-design.md, then asks
one question at a time — eviction policy, invalidation, cold-start,
consistency — checkpointing each answer and flagging the unknowns.
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Extract a plan from your head</div>
<div class="example-desc">Turn vague intent into an organized doc.</div>

```
"I have a rough product idea — interview me and write it down."

The agent walks the decision tree, captures every answer to disk,
and ends with a structured brainstorm file plus a list of open flags
and who should resolve them.
```
</div>
