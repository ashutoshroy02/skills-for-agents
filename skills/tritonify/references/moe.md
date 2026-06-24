# MoE (Mixture-of-Experts) Kernel Optimization

A MoE FFN routes each token to its top-k experts, runs each expert's SwiGLU FFN on its assigned tokens, and scatter-adds the weighted results back. The naive PyTorch path (loop over experts, index, `F.linear`, `index_add_`) is launch-bound and memory-bound. Sources: DeepGEMM (FP8 grouped GEMM), Megablocks, vLLM/SGLang fused MoE, Triton group-GEMM tutorial, MIT-KDA candidates (fused-moe, grouped-gemm).

> Roofline note: at inference/decode, MoE is **memory-bound** (few tokens per expert, weight-load dominated). At training/prefill with many tokens, the expert GEMMs become **compute-bound**. The right kernel differs — dispatch on the regime.

## 1. Grouped / batched expert GEMM (the core)

The problem: experts have **variable token counts** (ragged), so you can't use a single batched GEMM with uniform batch size. Options:
- **Grouped GEMM** — one kernel launch handles all experts; each CTA is assigned a `(expert, tile)` pair via a precomputed schedule, reads that expert's weights, and does `tl.dot` over its token tile. No per-expert launch. This is the win over the Python expert loop. (Triton group-GEMM tutorial; DeepGEMM for FP8.)
- **Block-scheduled / sorted** — sort tokens by expert id so each expert's tokens are contiguous, then a single GEMM with per-expert row offsets (Megablocks "dropless" / block-sparse formulation). Avoids padding to capacity.
- **Padded batched** — pad each expert to a fixed capacity and use a true batched GEMM; simplest but wastes compute on padding (bad when load is skewed).

Fuse the **gate+up** projection as one grouped GEMM producing `[tokens, 2I]` (horizontal fusion, same as dense MLP), then the activation, then the down grouped GEMM.

## 2. Token dispatch / routing fusion

The dispatch (gather tokens per expert) and combine (scatter weighted outputs back) are pure memory movement — fuse them:
- **Fuse the permutation into the GEMM's load** — instead of materializing a gathered `[tokens_for_expert, H]` buffer in HBM, have the grouped-GEMM kernel **gather rows via an index map directly in its load** (read `x[token_id]` for the tokens this CTA owns). Kills the dispatch buffer's HBM round-trip.
- **Fuse the combine/scatter into the down-GEMM epilogue** — multiply by the routing weight and `atomic_add` (or sorted-segment-reduce) into the output in the epilogue, instead of a separate weighted `index_add_`.
- **Sort once, reuse** — compute the sort/permutation (argsort of expert assignments) once; reuse the index map for dispatch, both GEMMs, and combine.

## 3. Quantized / FP8 grouped GEMM

**DeepGEMM** does FP8 block-scaled *grouped* GEMM for MoE — the production path for DeepSeek-V3/R1 (~78% of H800 FP8 peak, ~1.2× over prior CUTLASS grouped kernels). Use when weights are FP8/INT4 and the expert GEMMs are the bottleneck; the dequant fuses into the grouped-GEMM mainloop.

## 4. Load balancing & its kernel implications

- Token-per-expert counts are **skewed**; a capacity factor caps tokens/expert (drops overflow) for fixed-shape kernels, but dropping hurts quality. Dropless (Megablocks) handles ragged counts without padding — preferred if the kernel supports variable offsets.
- The schedule (which CTA does which `(expert, tile)`) should balance work across SMs — a Stream-K-style even decomposition over the *total* token-tiles beats per-expert grids when load is uneven.

## When the naive path is actually fine (be honest)

- **Tiny #tokens** (short decode, batch 1, top-1): the sort + grouped-GEMM scheduling overhead can exceed the savings; the per-expert loop may win. Profile before fusing.
- **Few experts, balanced load**: a padded batched GEMM is simpler and close enough.
- The biggest real MoE win is usually **#1 (grouped GEMM, no per-expert launch) + #2 (fused dispatch/combine)** — do those before chasing quantization.
