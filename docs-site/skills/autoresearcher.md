<div class="domain-header">
  <span class="skill-badge process">Process</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: nothing (orchestrates the loop)</span>
</div>

# Autoresearcher

Autonomous research loop that improves any measurable artifact — a prompt, a scoring config, weights, an algorithm, a heuristic, a code block — against a frozen evaluation.

## When to Use

- User wants to optimize, improve, or "push the score" on something with a measurable objective
- The work should run autonomously and keep iterating on its own
- There's a frozen eval (or one can be defined) to score candidates against

## Triggers

```
"optimize X", "improve X", "push the score on X", "run autoresearch on X"
Anything with a measurable objective: code, models, prompts, pipelines, parameters
```

## How It Works

The loop is diagnosis-driven. Each round:

1. **Look** at where the current best artifact fails on the frozen eval.
2. **Diagnose** the root cause of those failures.
3. **Dispatch** the right idea engine at that cause — one of four:
   - **Novel** — original ideas aimed at the failure
   - **Tangential** — cross-domain transfers from unrelated fields
   - **Baseline-improvement** — incremental refinement of what works
   - **Diagnosis** — instrument and probe to understand the failure better
4. **Test** the candidate against the frozen eval.
5. **Keep** it only if it provably beats the current best.
6. **Repeat** until a stopping condition holds.

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Push a prompt's accuracy</div>
<div class="example-desc">Improve a classification prompt against a held-out set.</div>

```
"Run autoresearch on this prompt — eval is the 200-row labeled set,
keep going until it plateaus."

The agent diagnoses misclassifications, dispatches idea engines at
the failure clusters, scores each candidate on the frozen 200 rows,
and only commits prompts that beat the best so far.
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Optimize a scoring heuristic</div>
<div class="example-desc">Tune a ranking config against an offline metric.</div>

```
"Improve this ranking config. Objective is NDCG@10 on the frozen
query set. Run it autonomously."

The loop probes which queries regress, transfers a cross-domain
re-ranking idea, tests it, keeps it only if NDCG@10 improves.
```
</div>
