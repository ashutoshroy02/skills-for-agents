# The Per-Kernel Playbook

Every kernel you write or optimize follows this structure (adapted from tensormux `kernel-skills`). It forces constraint-gathering before code, kills cargo-cult optimization, and bans unmeasured claims. The technique catalogs (`gemm.md`, `fusion-mlp-activation.md`, `moe.md`, `loss-fusion.md`) are instances of it; apply the same skeleton to any new kernel.

> Why: AI agents produce worse kernels from vague prompts — they skip constraints, pick wrong tiles, ignore boundaries, and make up speedups. This skeleton removes those failure modes.

## The skeleton

1. **Use this when** — the concrete situations where a custom kernel is the right call (an epilogue to fuse, a format the library lacks, a shape it underperforms, a research kernel needing full control).

2. **Do NOT use this when** *(the most important section — most-skipped)* — when to just call the library and say so: standard large aligned fp16/bf16 GEMM with no epilogue (`torch.mm`/cuBLAS wins); very small shapes cuBLAS handles via grouped routines; a fusion `torch.compile` already does; latency-bound small-batch where profiling, not assumption, must decide.

3. **Gather inputs first** — confirm before a line of code:
   - exact shapes / ranges (static vs dynamic)
   - input dtype + **accumulation dtype** (accumulate in fp32 unless proven safe)
   - layout / strides (row/col-major; transposed?) — *pass strides as kernel args, never hardcode from shape*
   - epilogue (bias / activation / scale / residual / in-place accumulate)
   - batch (2D / batched / broadcast)
   - **hardware target** (arch sets tensor-core path + pipeline depth + SMEM size)
   - autotuning allowed? (production-fixed config needs justification)

4. **Reasoning process** — the ordered decisions: tensor-core eligibility, tile assignment, pointer/stride math, fp32 accumulation, boundary masking, epilogue placement, autotune config, correctness reference.

5. **Correctness requirements** — the invariants that silently corrupt results if wrong: K-boundary mask every load; mask the output store on all dims; strides as args; fp32 accumulate; tile assignment is a bijection (no gaps/overlaps); `.contiguous()` or documented stride handling.

6. **Performance requirements** — reason through tile-shape-vs-occupancy, BLOCK_K & pipeline depth, num_warps, swizzling benefit, arithmetic intensity vs the arch threshold — *before* finalizing. **And: do not claim a speedup over the library without a benchmark call.**

7. **Common failure modes** — the specific bugs for this kernel class (wrong pid mapping, fp16 accumulation, missing K-boundary mask, BLOCK_K<16 disabling tensor cores, hardcoded strides, grid off-by-one, alpha/beta semantics).

8. **Review checklist** — a binary checklist to run before declaring done. The last item is always: **no performance claim is made without a benchmark to back it.**

## The two rules that override everything

- **Correctness before performance.** A fast wrong kernel is worthless. Validate against a reference (`torch.allclose`, tight tol; fp64/cpu reference for the hard cases; gradients match with no NaN/Inf) *before* trusting any number.
- **No unmeasured claims.** Every "Nx faster" must trace to a `benchmark.py`/`do_bench` run, with the GPU, dtype, shape, and baseline (cuBLAS vs cuBLASLt vs torch.compile, FP32 vs TF32 mode) stated. Label compute-beat vs bandwidth/format win.
