# Loss Fusion — and How to Build Your Own Fused Loss

Sources: Liger-Kernel fused CE + fused-linear-CE (2410.10989), online softmax (Milakov & Gimelshein), FlashAttention's online-softmax, Apple "Cut Cross-Entropy" (CCE), Triton fused-softmax tutorial. Follows the per-kernel playbook (`playbook.md`).

## Why fused cross-entropy is the canonical win

The LM head produces **logits `[B·T, V]`** with V = vocab (often 128k–256k). Materializing that tensor — and its softmax and gradient — dominates memory. Gemma-2B loss over a batch can be **~24 GB**; fused, **~1 MB**. Three layers, each independently valuable:

1. **Online / streaming softmax** — never store the full logit row. One pass with running max `m` and running sum `s`:
   ```
   for each chunk of logits in the row:
       m_new = max(m, max(chunk))
       s     = s * exp(m - m_new) + sum(exp(chunk - m_new))   # rescale running sum
       m     = m_new
   lse  = m + log(s);   loss = lse - logit[target]
   ```
   The load-bearing primitive (same recurrence FlashAttention uses). fp32 for `m,s`; subtract the max for stability.

2. **Chunk over the token dimension** — process the `B·T` rows in blocks; compute scalar loss + per-row grad per block; only one block's logits live at once. Bounds peak memory to `O(chunk × V)`.

3. **Fuse the final linear projection INTO the loss (fused-linear-CE)** — the biggest win. Don't compute `logits = hidden @ W_vocabᵀ` as a separate GEMM that writes `[B·T, V]` to HBM. For each token chunk, compute its logits on-the-fly in the loss kernel (`tl.dot` of the hidden chunk with vocab weights), online-softmax, get the loss, and compute the gradient w.r.t. hidden (and accumulate w.r.t. W) **in the same pass** — so `[B·T, V]` never exists in HBM. (Liger fused-linear-cross-entropy; Apple CCE.)

## THE GENERAL RECIPE — fuse ANY custom loss

Generalize the five steps that make CE fast, to fuse a *new* loss:

1. **Find the big intermediate that shouldn't be materialized** — a `[N, big]` tensor: logits `[tokens, vocab]`, a pairwise matrix `[N, N]` (contrastive), per-class scores `[N, C]`. That tensor is the enemy.
2. **Tile over the big axis** — loop the kernel over chunks of `big` (or of `N`), one chunk live in SRAM/registers.
3. **Replace any softmax/normalization with its online/streaming form** so the normalizer is computed across chunks without storing them.
4. **Fuse the upstream projection into the loss kernel** — if the big intermediate is `hidden @ Wᵀ`, compute it on-the-fly per chunk (`tl.dot`) instead of materializing it.
5. **Compute and accumulate the gradient in the same pass (fused backward)** — while each chunk's intermediate is live, add its contribution to `grad_hidden`/`grad_W`. fp32 accumulation.

### Worked templates
- **Label-smoothed / z-loss CE** — CE plus `α·lse²` (z-loss) or the uniform-target mix, applied per chunk. No new materialization.
- **Focal loss** — CE weighted by `(1−p_t)^γ`; `p_t = exp(logit_t − lse)` is available once you have the online `lse`; apply the focal weight to the per-token loss and gradient in the same pass.
- **Contrastive / InfoNCE** — the big intermediate is the `[N, N]` similarity matrix. Tile over the key axis, online-softmax the denominator over keys, fuse the `q·kᵀ` similarity. Same shape as FlashAttention.

## Numerical-stability gotchas (verify these)
- Always subtract the running max before `exp` (overflow otherwise).
- fp32 for accumulators (`m`, `s`, grad accumulation), even with bf16/fp16 storage.
- **Correctness gate (playbook rule):** full-model loss matches the unfused reference within tight tolerance; gradients match (max_diff small, cosine ≈ 1), no NaN/Inf — *before* trusting any speed number.

## When NOT to fuse the loss
- The loss isn't the bottleneck (small vocab; the GEMMs dominate) → little gained.
- Chunking forces expensive **recompute** in backward that outweighs the HBM saved (rare for CE — logits are cheap to recompute — but check for losses with expensive per-element ops).
