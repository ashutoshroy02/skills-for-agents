# Fusion, MLP, and Activation Optimization

Sources: Liger-Kernel, CODA epilogue abstraction (2605.19269), FlashAttention, official Triton tutorials.

## Fusion taxonomy — what "fuse" means and when it pays

- **Vertical fusion (producer → consumer epilogue):** the output of op A feeds op B; instead of writing A's result to HBM and reading it back in B, compute B in A's epilogue while the data is still in registers/SMEM. The dominant LLM win (FlashAttention, fused-CE). **Pays when the intermediate is memory-bound** (large tensor round-tripping HBM).
- **Horizontal fusion (siblings sharing an input):** two+ ops read the same input — fuse into one kernel / one GEMM. Examples: QKV projection (one GEMM with stacked weights instead of three), **gate+up projection in an MLP** (one GEMM producing `[gate | up]`). Saves redundant input reads + launches.
- **Elementwise-into-GEMM epilogue:** apply bias/activation/scale/residual *inside* the GEMM kernel after the `tl.dot` accumulation, before writing C. CODA's 5 composable epilogue primitives.
- **Reduction fusion:** fold a reduction (sum/max/norm) into the producing kernel (norm+residual, the loss kernels).

**When fusion BACKFIRES (don't fuse blindly):** when it forces **recompute** of something compute-bound (you trade cheap HBM for expensive FLOPs); when it **kills occupancy** (the fused kernel needs too many registers/SMEM, fewer CTAs resident, slower overall); when the intermediate is tiny (no HBM saving to capture). Always confirm with the profiler, not the assumption.

## The HBM-traffic accounting method

For a candidate fusion, compute bytes saved:
```
intermediate_bytes = numel(intermediate) × dtype_bytes
saved = 2 × intermediate_bytes   # one write + one read avoided
```
If `saved` is a large fraction of the op's total HBM traffic and the op is memory-bound → fuse. Example (BiBo dense MLP, the original miss): `gate_up` is `[M, 2I]`; writing + reading it is `4·M·I·dtype_bytes` of avoidable traffic. Fusing the activation into the GEMM epilogue removes all of it.

## MLP optimization (the SwiGLU/GLU FFN)

A dense MLP is `down( act(gate(x)) * up(x) )`. Three GEMMs + an activation. Optimizations, highest leverage first:

1. **Horizontally fuse gate + up into ONE GEMM.** Concatenate the gate and up weight matrices → a single `x @ W_gate_up` producing `[M, 2I]`. One launch, one read of `x`, better tensor-core utilization than two skinny GEMMs. *(The BiBo deployed patch still did two separate GEMMs despite a benchmarked fused version existing — fix that.)*
2. **Fuse the activation into the GEMM epilogue.** Don't write `gate_up` to HBM and read it back for the activation. Compute `silu(gate)*up` in the GEMM epilogue (or, if using a library GEMM, in a kernel that the GEMM's output tile flows into without an HBM hop). This kills the `[M, 2I]` round-trip — the single biggest MLP win after #1.
3. **Fuse down_proj's epilogue** — add the residual (and any post-scale) inside the down-projection kernel's epilogue instead of a separate add kernel.
4. **Backward:** a fused backward recomputes `silu/up` from the saved input in-kernel and produces `grad_gate_up` in one pass (avoids materializing separate grad intermediates). Forward-only fusion is still valuable (saves the forward intermediate; PyTorch autograd handles the rest correctly) — fuse the backward when it's >~40% of step time or re-materializes large intermediates.

**Chunk over the token dim (M)** when M is huge and intermediates don't fit — process blocks of rows, bounding peak memory.

## Activation optimization (per activation)

Compute the activation in **fp32 registers** then cast back to the storage dtype — `because` doing the nonlinearity in bf16/fp16 loses precision and the cast is nearly free. Fuse the activation into the producer's epilogue (above). Each activation's fused forward + the backward derivative you need:

| Activation | Forward | Backward (d/dx) |
|---|---|---|
| **SiLU/Swish** `x·σ(x)` | `g*sig` where `sig=1/(1+e^{-g})` | `sig·(1 + g·(1−sig))` |
| **GELU (tanh approx)** | `0.5x(1+tanh(√(2/π)(x+0.044715x³)))` | derivative of the tanh form (Liger has it); use tanh approx for speed unless exact required |
| **GELU (exact)** | `x·Φ(x)` | `Φ(x) + x·φ(x)` |
| **ReLU²** `relu(x)²` | `where(x>0, x², 0)` | `where(x>0, 2x, 0)` |
| **SwiGLU** `silu(gate)·up` | split `[gate|up]`, `silu(gate)*up` | `grad_up = grad·silu(gate)`; `grad_gate = grad·up·dsilu(gate)` |
| **GeGLU** `gelu(gate)·up` | split, `gelu(gate)*up` | `grad_up = grad·gelu(gate)`; `grad_gate = grad·up·dgelu(gate)` |

For GLU-family, the input is the concatenated `[gate | up]` of width `2I`; index `gate = cols[:I]`, `up = cols[I:]` with a single load using an offset — one kernel reads both halves, no extra pass. Backward writes `grad_gate_up` of width `2I` in the same kernel.
