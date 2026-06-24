# Statistical Honesty — Telling a Real Gain From Noise

The loop's whole value depends on not fooling yourself. Most "improvements" in iterative optimization are eval noise or selection bias. This file is the keep/discard arithmetic. Read it before promoting any candidate to champion.

> **The one rule:** a candidate becomes the new champion only when it beats the current best **on a held-out split the loop is not optimized against**, by **more than the noise floor**, confirmed by a **paired test**. Everything below is how to compute those three things.

---

## 1. The noise floor — compute it first, before any experiment

For a binary metric (accuracy, recall@k — each case passes or fails) with pass-rate `p` over `n` cases:

```
σ = √( p·(1−p) / n )          # standard error of the metric
95% CI ≈ ±1.96·σ
```

Worked, for a 1000-case eval at recall@1, p≈0.55:  **σ ≈ 1.57%**, 95% CI ≈ ±3.1%.
At recall@5, p≈0.92:  **σ ≈ 0.86%** — near the boundary, use a **Wilson / Agresti–Coull** interval, not Wald.

**Consequence:** on 1000 cases, a **+2% @1 bump is inside the noise** — indistinguishable from luck *unless* you use a paired test (below). Anything below ~1σ is a tie; do not promote it.

Also measure your **evaluator's own run-to-run std** if it is stochastic (e.g. an LLM judge): re-run the same candidate a few times and take the spread. That variance adds to the floor.

---

## 2. Paired tests — the right tool for one fixed eval set

Because every candidate is scored on the **same** eval cases, use **paired** tests. They cancel shared per-case difficulty and validate gains ~2× smaller than unpaired CIs can. You have per-case predictions cached → b and c are free to compute.

### McNemar's test — for @1 (one right/wrong label per case)

Build the 2×2 of old-vs-new on each case. Only the **discordant** cells matter:
- `b` = cases only the **new** candidate got right
- `c` = cases only the **old** champion got right

```
χ² = (|b − c| − 1)² / (b + c)        # significant at p<0.05 when χ² > 3.84
# use the exact binomial test instead when b + c < 25
```

Worked — "is a +12/1000 net @1 gain real?" It depends entirely on the discordant pile:
- b=12, c=0  → p≈0.0005 ✅ real
- b=21, c=9  → p≈0.045  ✅ real
- b=22, c=10 → p≈0.052  ❌ not significant
- b=56, c=44 → p≈0.27   ❌ noise

So **a +12 net clears p<0.05 only while the loser cell c ≲ 9–10.** A net gain with a big churning discordant pile is noise. `from statsmodels.stats.contingency_tables import mcnemar`.

### Paired bootstrap — for @k, ICD, or judge scores (no clean 2×2)

```
for B = 10_000 iterations:
    resample case indices WITH replacement  (the SAME indices for both candidates)
    record δ = new_score − old_score on that resample
promote only if the 95% CI of δ excludes 0
```

The shared-indices pairing is what makes it powerful — it removes the variance from which cases got sampled.

---

## 3. The Ladder — a promotion rule that survives many attempts (Blum & Hardt 2015)

Running many candidates against the same eval inflates the apparent best. The Ladder rule: **refuse to acknowledge an improvement smaller than the noise floor.**

```
promote new → champion  ONLY IF  new_score > best_score + margin
    margin = 1σ   (minimum)
    margin = 2σ   (recommended — ≈3% @1 on a 1000-case eval)
```

So **82.3 vs 81.9 is a tie — do not promote.** Treat the running progression log as a Ladder; report scores to **±1%, not three decimals**; consult the frozen test set **rarely and per method-family, not per micro-tweak**.

---

## 4. Selection bias — the garden of forking paths (Gelman & Loken)

Trying `m` candidates and keeping the best inflates the reported number **even if you report only one**:

```
best-of-m noisy candidates beats the true mean by  ≈ σ·√(2 ln m)
```

Worked: σ=1.57%, m=20 candidates → **+3.8% of pure selection bias** — the same magnitude as the gains usually chased. So after a search, **confirm the winner on data that was not used to select it** (the held-out split), and never tune on the frozen test. A "ceiling" found by trying 45 methods is itself inflated by ~2–3σ; the true ceiling is plausibly lower.

---

## 5. Ablation discipline — attributing the delta cleanly

- **One change per iteration.** Change two things and you cannot attribute the delta — and credit assignment is *delayed* (an upstream change can surface as a downstream score move), so single-change keeps the chain clean.
- **Ablate from the same full baseline each time**, not cumulatively (cumulative biases later removals).
- **Equal tuning effort per arm — especially the baseline** (Henderson, "Deep RL that Matters"): the most common fake win is tuning the new arm harder than its baseline ("continental breakfast" comparison).
- **Audit the new code path for bugs before believing its delta** — a silent bug is indistinguishable from a real win, and a result you can't reproduce by re-running is not a result.
- **Interacting knobs** (e.g. two toggles that may only help together): a sequential one-at-a-time sweep finds a ridge, not the optimum → run a small **2×2 factorial** for those two.

---

## 6. The Goodhart trip-wire — guarding the frozen eval

A frozen metric + per-iteration optimization is Goodhart by construction (optimize a proxy hard enough and it stops tracking what you care about). Three defenses, all cheap:

1. **Held-out split the loop is never scored on** — only consulted at promotion (GEPA's measured overfitting: test peaked at steps 4–7, then degraded; 20–100 examples beat 500).
2. **Multi-metric agreement** — if you have several metrics (e.g. exact-match AND a semantic/ICD match AND a judge), gaming one usually breaks another; require the promotion to not regress the others.
3. **Standing-slice regression trip-wire** — keep a few fixed sub-population slices; if any regresses while the aggregate rises, **halt and inspect**. That divergence is the overfitting signature.
