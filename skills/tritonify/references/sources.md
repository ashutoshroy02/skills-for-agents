# Tritonify — Accepted Source Backbone

The curated sources for the rehauled skill. **Kernel-craft only** — every entry teaches *what makes a kernel fast* (technique, not agent plumbing). The old 36-paper survey's RL-training / multi-agent / evolutionary / benchmark papers were **purged** (they're about orchestrating an LLM to emit kernels, not about kernel optimization itself — see "Purged" at the bottom for the record).

> Status: craft + workflow sources migrated from the old `paper-survey.md`. Canonical hands-on references (Triton tutorials, CUTLASS docs, Simon Boehm worklog, GPU MODE) added — these were **missing** from the old skill and are the primary "how to actually optimize" sources. Verification research will confirm exact numbers and may add more.

---

## 1. Technique papers (the substance)

| Source | Link | What to mine from it |
|---|---|---|
| **FlashAttention** | [2205.14135](https://arxiv.org/abs/2205.14135) | IO-awareness; tile so the working set stays in SRAM, never materialize the big intermediate to HBM |
| **FlashAttention-3** | [2407.08608](https://arxiv.org/abs/2407.08608) | Hopper warp-specialization (producer/consumer), TMA, FP8; overlap memory & tensor-core compute |
| **CUTLASS FlashAttention-2** | [2312.11918](https://arxiv.org/abs/2312.11918) | TMA + WGMMA pipelining; epilogue fusion |
| **CODA** | [2605.19269](https://arxiv.org/abs/2605.19269) · [coda-kernels](https://github.com/HanGuo97/coda-kernels) | **GEMM + epilogue fusion** — 5 composable epilogue primitives. *This is exactly the matmul+activation fusion the BiBo MLP skipped.* |
| **CUDA-L2** | [2512.02551](https://arxiv.org/abs/2512.02551) · [CUDA-L2](https://github.com/deepreinforce-ai/CUDA-L2) | **Beats cuBLAS by 19.2% / cuBLASLt by 11.4%** on HGEMM — the proof matmul is optimizable; mine the techniques it found |
| **ThunderKittens** | [2410.20399](https://arxiv.org/abs/2410.20399) · [ThunderKittens](https://github.com/HazyResearch/ThunderKittens) | warp/block/grid tile abstractions; matches cuBLAS & FA-3; register-layout discipline for tensor cores |
| **muCUTLASS** | [2603.29010](https://arxiv.org/abs/2603.29010) | compact DSL + **Speed-of-Light guidance** (roofline-anchored target before coding) |
| **CuTeGen** | [2604.01489](https://arxiv.org/abs/2604.01489) | CuTe layout-algebra representation; progressive refinement |
| **Liger Kernel** | [2410.10989](https://arxiv.org/abs/2410.10989) · [Liger-Kernel](https://github.com/linkedin/Liger-Kernel) | production fused Triton kernels (norm/activation/loss). **Use as a baseline to beat, NOT as the stopping point** — its "fuse only the activation, leave GEMMs to cuBLAS" pattern is what capped the BiBo kernels |

## 2. Canonical hands-on references (primary "how to optimize" — were MISSING)

| Source | Link | What to mine from it |
|---|---|---|
| **Triton official tutorials** | [triton-lang.org/tutorials](https://triton-lang.org/main/getting-started/tutorials/index.html) | matmul, **group-GEMM**, **persistent matmul**, fused-attention, fused-softmax, layernorm — with their measured cuBLAS-relative numbers |
| **NVIDIA CUTLASS + CuTe** | [github.com/NVIDIA/cutlass](https://github.com/NVIDIA/cutlass) | the reference for efficient GEMM: tiling hierarchy, swizzling, pipelining, epilogue visitor trees, split-K / stream-K |
| **Simon Boehm — "How to optimize a CUDA matmul kernel"** | [siboehm.com/articles/22/CUDA-MMM](https://siboehm.com/articles/22/CUDA-MMM) | the canonical step-by-step matmul worklog from naive → ~cuBLAS: coalescing, shared-mem tiling, register tiling, vectorized loads, warp-tiling |
| **DeepGEMM** | [github.com/deepseek-ai/DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) | FP8 / block-scaled GEMM, grouped GEMM for MoE |
| **Marlin** | [github.com/IST-DASLab/marlin](https://github.com/IST-DASLab/marlin) | mixed-precision (INT4×FP16) GEMM that beats cuBLAS in its regime — quantized-matmul technique |
| **GPU MODE lectures** | [github.com/gpu-mode/lectures](https://github.com/gpu-mode/lectures) | community lectures on profiling, tensor cores, quantization, Triton/CUDA — primary teaching material |
| **Production kernel repos** | vLLM, SGLang, FlashInfer | real fused/quantized kernels as worked examples (the MIT-KDA candidate ledgers point here) |

## 2b. Verified evidence — when custom BEATS cuBLAS (the decision rule the new skill must encode)

Confirmed by multi-source research (RTX 3090 / A100 / H100 / MI300X, cited). **The "cuBLAS is already optimal, don't bother" blanket is wrong — but the wins are regime-specific, and ~half the loud "Nx" posts are bandwidth/format wins, not fair compute-for-compute beats.** Encode this as the matmul triage:

| Regime | Verdict | Evidence |
|---|---|---|
| **Fused epilogue** (matmul + activation/bias/residual) | **Custom wins** — kills the HBM round-trip of the intermediate | the BiBo MLP miss; CODA epilogue abstraction |
| **Small-M / decode / GEMV** (M=1) | **Specialized GEMV wins** — but a *naive* Triton matmul **LOSES 1.94×** at M=1, reaching parity only ~M=5 ([triton#3104](https://github.com/triton-lang/triton/issues/3104)). Needs a real GEMV kernel + **batch-size dispatcher** | FastGEMV/FlashDecoding++ (MLSys'24): cuBLAS only 82% of custom GEMV at M=1 (+22%), collapses to ~50% at M=4 |
| **Skinny / irregular / odd-grid** | **Stream-K wins** via load balancing | Stream-K: **6.74× vs cuBLAS**, 14.7× vs CUTLASS data-parallel on specific shapes |
| **Sub-FP16 precision** (FP8/FP4/INT4) | **Custom wins — but mostly a FORMAT gap cuBLAS doesn't handle natively**, not a same-problem beat. Largest at batch 1, decays with batch | GemLite int4 H100: BS=1 **1.95×**, BS=32 1.16×; DeepGEMM FP8, Marlin INT4 |
| **New-arch features** (Hopper wgmma/TMA, Blackwell tcgen05/MXFP) | **Custom/CUTLASS leads** where cuBLAS lags the newest ISA | FA-3, CUTLASS |
| **Large aligned square FP16/BF16/TF32** | **cuBLAS still wins** — custom tops out at ~85–96%. Don't waste effort here | multiple |
| **Tile selection** | static heuristics mis-pick on non-canonical shapes (−13.9% on Llama3 shapes) → **autotune** | tritonBLAS (MI300X) |

**Decision rule:** optimize matmul when there's an epilogue to fuse, a small/skinny/irregular shape, a sub-FP16 format, or a new-arch feature cuBLAS underuses — and **autotune the tile**. Just call cuBLAS for large aligned square GEMM in a precision it supports.

Added confirmed sources: FastGEMV/FlashDecoding++ (MLSys 2024) · [GemLite](https://github.com/mobiusml/gemlite) (PyTorch int4 GEMV) · Stream-K ([arXiv 2301.03598](https://arxiv.org/abs/2301.03598)) · tritonBLAS · [triton#3104](https://github.com/triton-lang/triton/issues/3104) (the naive-Triton-loses-at-small-M caveat).

## 3. Workflow skeleton (keep the loop, drop the plumbing)

| Source | Link | What to keep |
|---|---|---|
| **MIT Kernel Design Agents** | [mit-han-lab/kernel-design-agents](https://github.com/mit-han-lab/kernel-design-agents) | the **Profile → Diagnose → Plan → Implement → Validate** loop and "keep workflow separate from task workspace"; the candidate kernel ledgers (flash-attn-4, deepgemm, nvfp4-gemm/gemv, fp8-block-scale-gemm, grouped-gemm, fused-moe) as real targets |

---

## Purged (recorded for traceability — do NOT re-add)

Agent-plumbing papers removed (about making an *LLM* emit kernels / benchmarking it, not about kernel craft):
- **RL-training:** Dr.Kernel, DRTriton, TritonRL, AutoTriton, CUDA-Agent, Kevin, Makora/GPT-5-RL, DICE
- **Multi-agent:** KernelSkill, CudaForge, Astra, cuPilot, CUDAnalyst
- **Evolutionary/search:** EvoEngineer, OptiML, KernelFoundry, GPU-Kernel-Scientist, R3, Kernel-Smith
- **Benchmarks:** KernelBench, AgentKernelArena, FastKernels, TritonBench, robust-kbench — *(if we later add a measurement/eval loop, KernelBench or TritonBench can return as an eval harness only, not as technique sources)*
