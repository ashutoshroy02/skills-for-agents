# The Capability Envelope — Access-Aware Optimization

The boundary on a kernel is **not** a fixed wall — it is a function of *what access you have*. Before concluding "this is as fast as it gets," climb this ladder and ask what each rung unlocks. The old skill found its own wall ("cuBLAS is optimal, not possible") and quit; the real wall moves with access.

> Rule: **never declare an optimization impossible without naming which rung you stopped at and what the next rung would allow.** State the access you have; if a technique needs a higher rung, say "possible with X access" instead of "impossible."

## Rung 1 — Framework only (PyTorch / Triton, no special privileges)

Almost always non-empty even when it "feels" maxed:
- **Autotune** tile/block/warps/stages (static heuristics mis-pick — tritonBLAS lost 13.9% on Llama3 shapes).
- **Fusion** — vertical (epilogue) + horizontal (gate+up, QKV) to kill HBM round-trips.
- **Custom Triton** with `tl.dot`, swizzling, `num_stages` pipelining, block-pointer/tensor-descriptor loads.
- **Recompute vs store** tradeoffs; chunking to fit SRAM.

## Rung 2 — Inline PTX / SASS (still framework-level, just lower)

Emit instructions the compiler won't:
- **Triton `tl.inline_asm_elementwise`** / CUDA `asm volatile` — `prmt` (byte permute), `lop3` (fused 3-input logic, key for fast int4 dequant), `vabsdiff`, fast approximate transcendentals (`ex2.approx`, `rcp.approx`).
- Hand-scheduled `cp.async` variants the compiler is conservative about.
- This is how Marlin/GemLite squeeze int4 dequant — `lop3`-based unpacking in the MMA path.
- **Cost:** portability and maintainability. Use only where the profiler shows the compiler-emitted path is the bottleneck.

> **Hardware reality for the current targets (T4 sm_75 / RTX 3050 sm_86):** Rung 3's headline features — TMA, wgmma, thread-block clusters/DSMEM, tcgen05 — are **Hopper/Blackwell only and do not exist on sm_75 or sm_86**. `cp.async` exists on sm_86 but **not on sm_75 (T4)**. So on your hardware the ladder effectively stops at **Rung 2 (inline PTX)**, and Triton already covers most of Rungs 1–2. The big CUDA-only ceiling advantage is unavailable here → Triton-default is the right call; reserve CUDA for a profiled compute-bound dense GEMM only. Also: T4 has **no bf16 tensor cores** — use fp16 for the TC path on the training GPU.

## Rung 3 — Driver / architecture features (CUDA, recent-arch GPUs — Hopper/Blackwell)

Features Triton can't express; need CUDA/CUTLASS:
- **TMA (Tensor Memory Accelerator, Hopper+)** — bulk async global↔shared copies with hardware descriptors; frees warps from address math. Big for GEMM/attention prologues.
- **`cp.async` pipelines** — multi-stage software prefetch (the manual form of `num_stages`).
- **Thread-block clusters + Distributed Shared Memory (DSMEM, Hopper)** — CTAs in a cluster read each other's SMEM; enables larger effective tiles and cross-CTA reduction without HBM.
- **Warp specialization / producer-consumer** — dedicated load warps (TMA) + compute warps (wgmma); the FA-3 pattern.
- **Persistent kernels** — grid = #SMs, loop over output tiles internally; amortizes launch overhead, improves L2 reuse, enables Stream-K load balancing.
- **Blackwell `tcgen05.mma` + TMEM** — 5th-gen tensor cores (OMMA FP4 / QMMA FP6-FP8), operands in Tensor Memory; CUTLASS reaches up to 98% of FP4 peak where cuBLAS lags.

## Rung 4 — Direct HBM / low-level memory control

- **Avoid redundant HBM round-trips** by owning the whole fused pipeline (the recurring theme — FlashAttention, fused-CE).
- **L2 residency / cache hints** — `cudaStreamSetAttribute` carve-out, `evict_first/evict_last` eviction policies, `__ldg`/streaming loads to control what stays resident.
- **GPUDirect / peer access** for multi-GPU when the bottleneck is the transfer, not the kernel.
- Bypassing framework overhead (graph capture, fused launch) when launch/dispatch dominates at small batch.

## How to use the ladder in the loop

When the trial-loop hits a **plateau** (`trial-loop.md` Step 7), don't stop — ask: *"which rung am I on, and what does the next rung unlock for this bottleneck?"* If the profiler says "memory-bound, address-generation overhead," Rung 3's TMA is the unlock. If "int4 dequant is the bottleneck," Rung 2's `lop3` is. If "launch-bound at small batch," Rung 3's persistent kernel is.

**Honesty (the other half):** higher rungs cost portability and maintenance, and don't always pay. If Rung 1 already sits at the roofline, say so and stop — climbing further is wasted effort. The ladder is for when there's a *named, profiled* bound that a higher rung removes — not for reflexive low-level effort.
