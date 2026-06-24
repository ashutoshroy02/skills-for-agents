# The Trial-Loop — Detail

Adapted from the HuggingFace `kernels` agent skills (the Xe-Forge loop in `xpu-kernels`, the H100/A100/T4 loop in `cuda-kernels`). The loop is a **tree of trials** on a frozen correctness+performance benchmark, run until a decisive win or you've exhausted the trial budget. The principle that makes it work: **never stop at a plateau** — LLM sampling can discover a better idea at any trial.

## If the HF scripts are installed, use them — don't hand-roll a harness

If `cuda-kernels` / `xpu-kernels` are available (`~/.claude/skills/`), they ship standalone CLI tools. Use them instead of writing your own benchmark/test scripts (writing your own is the #1 way to get a wrong number):

| Tool | Purpose |
|---|---|
| `analyze_kernel.py <file>` | static analysis: ops, shapes, fusion opportunities (PyTorch reference) |
| `validate_triton.py <file>` / `validate_cpu_kernel.py` | syntax + constraint checks, **no GPU needed** — run before spending GPU time |
| `benchmark.py <baseline> <candidate>` | correctness + performance; cache the baseline time and pass `--baseline-us` on later trials to skip re-measuring it |
| `*_profiler.py <file>` | hardware counters (Nsight/VTune) + recommendations |
| `trial_manager.py init/save/result/status/best/finalize` | tree-structured trial tracking |

**Rules carried from the HF skills:** only create kernel files (not ad-hoc benchmark/test scripts); if a tool fails, **stop and report** — don't work around it with a custom script; generated kernels are self-contained (helpers inline). On a single-GPU box, **serialize GPU jobs** (benchmark/profile one at a time) — concurrent GPU workloads produce wrong numbers. CPU-only tools (analyze/validate/trial-manager) parallelize freely.

If the scripts are not installed, run the equivalent steps manually with `triton.testing.do_bench` + `ncu`, and keep a small trial log (a JSONL or a markdown table) playing the role of `trial_manager`.

## The decide-next-action tree (Step 7)

After each benchmarked + profiled trial:

- **Decisive win at SoL** (e.g. ≥ target speedup, achieved % near roofline) → finalize, stop.
- **Improved** → continue on this branch; apply the next optimization level (see each catalog's progression).
- **Regressed** → branch back to the **best** trial so far; try a *different* strategy (not a tweak of the loser).
- **Correctness failed** → fix on the same branch; never record a perf number for an incorrect kernel.
- **Profiler says low occupancy** → larger tiles / fewer registers / check SMEM pressure.
- **Profiler says memory-bound, low BW %** → coalescing, vectorized loads, fusion to kill round-trips.
- **Profiler says tensor-core util ≈ 0 on matmul-ish** → wire up `tl.dot`/wmma/wgmma with aligned dims (biggest single miss).
- **Plateau (2+ trials no gain)** → do NOT stop. Switch to a **fundamentally different** approach: different algorithm, different tiling, different fusion boundary — or **climb the access ladder** (`access-envelope.md`) to unlock a technique the current access level forbade.

## Trial budget & stopping

- Set a trial budget up front (the HF skills cap via `config.yaml: max_trials` and **run all of them**). Don't stop early on a plateau; do stop on a decisive win or user request.
- Keep the **best trial** always recoverable (the tree's job) so a regression never loses ground.
- Final number: re-benchmark the finalized kernel cleanly (no cached baseline) and label it (GPU, dtype, shape, baseline kind, compute-beat vs bandwidth/format win).

## How this maps to the Five Non-Negotiables

ANALYZE = roofline + HBM-traffic (#1, #2). PLAN/DECIDE = beat-the-baseline + matmul triage (#3, #4). The plateau branch = the access-envelope climb (#5). BENCHMARK = correctness-first + no-unmeasured-claims (the playbook's two overriding rules).
