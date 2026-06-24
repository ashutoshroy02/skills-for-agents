# GEMM / Matmul Technique Depth

When the triage says "optimize" (see SKILL.md), these are the levers, in the order a profiler usually demands them. Sources: Simon Boehm's CUDA-MMM worklog, official Triton matmul/persistent/group-GEMM tutorials, NVIDIA CUTLASS/CuTe, Stream-K (2301.03598), Marlin, GemLite, DeepGEMM.

> Always establish the **roofline** first: a GEMM of (M,N,K) does `2·M·N·K` FLOPs and moves `(M·K + K·N + M·N)·dtype_bytes` (minimum). Arithmetic intensity `= FLOPs/bytes` tells you which wall you're hitting. Large square → compute-bound (tensor cores or bust). Skinny/GEMV → memory-bound.

## Memory-side levers (fix first if memory-bound)

- **Global-memory coalescing** — consecutive threads must read consecutive addresses. Lay out the inner loop so a warp's 32 loads hit one (or few) 128B cache lines. Boehm's single biggest early jump. In Triton this is mostly automatic via block layout, but check the access pattern of any manual pointer arithmetic.
- **Shared-memory (SMEM) tiling** — stage a `BLOCK_M×BLOCK_K` tile of A and `BLOCK_K×BLOCK_N` of B into SMEM, reuse across the block. Reduces HBM reads by ~BLOCK factor. The classic tiled-GEMM.
- **Register tiling / thread-tiling** — each thread computes a micro-tile (e.g. 8×8) of C accumulated in registers; reuse SMEM values across the micro-tile. This is what lifts a tiled kernel from ~30% to ~80%+ of cuBLAS (Boehm).
- **Vectorized loads** — `float4` / 128-bit loads (`tl` handles via block loads; in CUDA use `cp.async` or `ld.global.v4`). Fewer, wider transactions.
- **Bank-conflict-free SMEM swizzling** — permute SMEM layout so threads in a warp hit distinct banks (CUTLASS swizzle functors). Removes serialization on SMEM reads feeding the MMA.

## Compute-side levers (fix if compute-bound)

- **Tensor-core MMA** — the #1 miss is `tensor-core util ≈ 0` on a matmul. Use `tl.dot` (Triton) / `wmma` / `wgmma` (Hopper) / `tcgen05` (Blackwell). Requires **aligned dims** and the right register/SMEM layout; check dtype is tensor-core-eligible (FP16/BF16/TF32/FP8).
- **Software pipelining / double-buffering** (`num_stages` in Triton; `cp.async` + barriers in CUDA) — prefetch the next K-tile while computing the current one, overlapping memory and MMA. `num_stages=2–4` typical.
- **Warp specialization (Hopper+)** — producer warps issue TMA loads, consumer warps run wgmma. Needs CUDA/CUTLASS (Triton can't express it directly). FA-3 pattern.

## Shape-specific levers

- **Split-K** — when K is large but M·N is small (few output tiles → few CTAs → idle SMs), split the K dimension across CTAs and atomically/`reduce`-add partials. Fills the machine.
- **Stream-K** — generalizes split-K with **even work decomposition** across a fixed CTA grid, fixing the quantization/tail effect on odd grids. Up to 6.74× vs cuBLAS and 14.7× vs CUTLASS data-parallel on adversarial shapes. Use for skinny/irregular GEMMs.
- **GEMV + batch-size dispatcher (decode, M≈1)** — at M=1 the op is pure memory-bound; a tensor-core GEMM wastes the MMA. Use a **CUDA-core GEMV** (FastGEMV/FlashDecoding++: +22% vs cuBLAS at M=1) — but it collapses past M≈4, so **dispatch on batch size**: GEMV kernel for M≤~4, tiled tensor-core GEMM above. A naive Triton matmul at M=1 is ~1.94× SLOWER than cuBLAS — do not ship it for decode.
- **Persistent kernel** — launch grid = number of SMs, loop over output tiles inside the kernel. Amortizes launch overhead and improves L2 reuse for many-tile GEMMs (Triton persistent-matmul tutorial).

## Quantized GEMM (sub-FP16) — with measured data

- **INT4×FP16 (Marlin, GemLite, Machete)** — dequantize weights in-kernel into the MMA path; the win is bandwidth (4-bit weights = 4× less weight traffic), largest at **batch-1 decode** (GemLite int4 H100: BS=1 **1.95×**, BS=32 1.16×). **Machete** (Hopper-native CUTLASS w4a16, vLLM) vs AWQ-without-Marlin: **741 vs 68 tok/s on H200**. Watch dequant overhead vs bandwidth saved.
- **FP8 / block-scaled (DeepGEMM, CUTLASS)** — fine-grained per-block scaling cuBLAS doesn't do natively. **CUTLASS FP8 Ping-Pong vs cuBLAS FP8 (H100): ~2.4× at small M (decode M=1–8), shrinking to ~1.55× at M=128** (pytorch.org TMA blog). **DeepGEMM** ≈78% of H800 FP8 peak, ~1.2× over prior CUTLASS grouped GEMMs (DeepSeek V3/R1). **PyTorch TK-GEMM Triton + SplitK = 1.87× faster than cuBLAS FP8** on Llama-3-70B shapes — the strongest documented Triton beat. Mostly a **format win**, not same-problem compute — label it.
- **NVFP4/MXFP4 (Blackwell, tcgen05)** — `tcgen05.mma` (OMMA FP4 / QMMA FP6-FP8), TMEM holds operands; B200 peak 9000 TFLOPS FP4. cuBLAS (CUDA 12.9 `cublasLtMatmul`, `CUDA_R_4F_E2M1` + UE4M3 scales, 16-elem blocks) claims 4.6× over FP8 synthetic / 1.7–2.2× on LLM workloads. **But achieved is only 36–58% of theoretical** (DGX Spark 36–37%, B200 ceiling 58%) — *"the frontier is kernel engineering: tile shapes, TMA alignment, memory scheduling, not library availability"* (CUTLASS reaches up to 98% of peak with hand-tuned tiles). This is the skill's thesis in one line.

## Two honesty caveats (from the benchmark survey)

- **FP32 worklogs understate cuBLAS.** Most academic matmul worklogs (incl. Boehm's, reaching 93.7%) compare against cuBLAS in **FP32** mode. Production cuBLAS uses **TF32/BF16 tensor cores** — a different, faster baseline. When you claim "% of cuBLAS," state the dtype/mode, or you're beating a strawman.
- **Consumer GPUs have real cuBLAS dispatch gaps** *(directly relevant to consumer cards like the RTX 3050/5090)*: cuBLAS 13.3.0 on RTX 5090 (sm_120) misdispatches `simt_sgemm` for batched workloads → only 41% FMA util (vs 73–82% on datacenter GPUs), and a custom kernel hits **120–170% of cuBLAS**. On consumer hardware, "cuBLAS is optimal" is *especially* false — check the dispatched kernel with `ncu`.
- **CUDA-L2 (RL-discovered):** +11.4% over cuBLASLt-AutoTuning across 1000 shapes, largest gains on small-to-medium matrices where heuristics misfire.

## Always-do

- **Autotune** `BLOCK_M/N/K`, `num_warps`, `num_stages` over a config grid keyed on the shape. Static heuristics mis-pick on non-canonical shapes (tritonBLAS: −13.9% on Llama3 shapes vs autotuned). Cache the best config per shape.
- **Verify** correctness against `torch.matmul` (tight tolerance, fp32 accumulate) before trusting any speedup.
