# Cross-Domain Map — The Tangential Engine's Lookup Table

The tangential engine's job is **one move, the ladder of abstraction**:

> Take your specific problem → climb **UP** to its abstract relational/functional structure → jump **ACROSS** to a foreign field whose tools fit that structure → map the foreign machinery **BACK DOWN** onto your problem → **verify** the mapping is structural, not surface.

Worked instance (the example that motivated this skill): a knowledge graph whose edges are *entity relationships* abstracts to "strategic interaction among agents" → import **game theory**; a graph whose edges are *weighted* abstracts to "a distribution of information over states" → import **entropy / information theory** (PMI, the scorer already uses, is exactly this import made without naming it).

---

## The table — read your problem's abstract structure (left), import the machinery (right)

| If your problem's abstract structure is… | Import from… | The ready-made machinery |
|---|---|---|
| **Relational** — entities + typed relationships, who-connects-to-whom | Graph theory; social-network analysis; **game theory** if relations are strategic | Centrality, community detection, equilibria/ESS, Nash/minimax, mechanism design |
| **Weighted / probabilistic** — a distribution of mass/information over states | **Information theory**; Bayesian inference; **optimal transport** | Entropy `−Σp log p`, KL/PMI, mutual information; posterior updating; **Wasserstein** distance (when supports are disjoint and KL blows up) |
| **Many weakly-coupled units + a global cost, rugged landscape** | **Statistical mechanics** | Energy functions `E=−½Σwᵢⱼsᵢsⱼ` (Hopfield/Boltzmann), **simulated annealing**, mean-field approximation |
| **Sharp qualitative change as a parameter crosses a threshold** | **Phase transitions / percolation** | Critical point `p_c`, critical exponents, universality, finite-size scaling, giant component |
| **Multiple self-interested agents; adversarial or equilibrium objective** | **Game theory** | Nash/minimax, saddle points (GANs *are* this), evolutionarily stable strategies |
| **Search a huge combinatorial space, no gradient, only a quality score** | **Evolutionary biology** | Genetic algorithms (selection/crossover/mutation), evolution strategies, quality-diversity |
| **Something spreads through a population via contact** | **Epidemiology** | SIR/compartmental models, R₀, Bass diffusion, threshold/cascade models |
| **Sequential / temporal — hidden state evolving under noisy observation** | **Bayesian filtering / control** | Kalman/particle filters (predict-update recursion), HMMs |
| **Object lives on a curved space; natural distance is non-Euclidean** | **Differential geometry** | Riemannian manifolds; **information geometry** (Fisher-Rao metric, **natural gradient** `G⁻¹∇f` — invariant steepest descent) |
| **Compare two distributions where naive divergences fail** | **Optimal transport** | Wasserstein / earth-mover's distance, Kantorovich dual (Wasserstein GAN, diffusion models) |
| **Compose effectful/sequential operations; structure-preserving maps** | **Category theory** | Monads (sequencing), functors (databases as functors `C→Set`), adjunctions |
| **Extract robust, deformation-invariant shape from noisy data** | **Algebraic topology** | Persistent homology, barcodes, filtrations (TDA) |
| **A discrete iterative process to analyze as a continuous trajectory + stability** | **Control theory / dynamical systems** | ODEs (Neural ODEs), Lyapunov stability, adjoint method, gradient flow |
| **Rank nodes by long-run importance in a graph of flows** | **Linear algebra / Markov chains** | Dominant eigenvector (PageRank), stationary distribution; electrical-circuit analogy (effective resistance = commute time) |
| **Multiscale hierarchy — coarse-graining away irrelevant detail** | **Renormalization group** (physics) | Block-spin coarse-graining, RG flow (maps onto deep nets) |
| **Beliefs/choices that interfere, depend on order, violate classical probability** | **Quantum probability** | Hilbert-space states, non-commuting projectors, Born rule (quantum cognition — math without the physics) |

**Proof the table works** (transfers that became famous): Shannon ← Boltzmann's entropy. Hopfield nets ← the Ising energy. Simulated annealing ← metallurgical annealing (Kirkpatrick). Evolutionarily stable strategies ← game theory (Maynard Smith). Genetic algorithms ← natural selection (Holland). Bass diffusion ← SIR (epidemiology). Natural gradient ← differential geometry (Amari). Wasserstein GAN ← optimal transport (Arjovsky). PageRank ← Markov-chain eigenvectors (Brin & Page). Quantum cognition ← quantum probability (Busemeyer).

---

## How to operationalize a tangential proposal (the 5-step pipeline)

1. **Abstract the problem** — strip domain content, emit a domain-independent representation. Best schemas: **(purpose, mechanism)** facets for idea-level work; a **relational/predicate graph** for rigorous structural work; a **TRIZ contradiction** over generic parameters for engineering-shaped problems. Climb the ladder with WordNet hypernyms or anti-unification (the "generic space" of a blend).

2. **Retrieve a distant source** — the move that defines tangentiality: **hold purpose/structure fixed, vary the domain.** Implement as *high purpose-similarity + LOW mechanism-similarity* nearest-neighbor; or graph traversal **with forced random hops** (plain RAG stays too near the seed — push outward explicitly); or **Swanson ABC** bridge search across two disjoint literatures; or a **TRIZ matrix** lookup. Seed it with the table above.

3. **Generate the mapping** — align source↔target under structural consistency (map relations, not surface), or **facet-swap** (your problem's purpose + the analog's mechanism). The candidate inference = the unmapped source structure projected onto your target. *That projection is the new idea.*

4. **SANITY-CHECK — kill superficial and hallucinated mappings (the critical step):**
   - **Systematicity test** — does a *system of connected relations* align, or just isolated surface attributes? Reject surface matches.
   - **Hesse triage** — explicitly list **positive** analogy (what's shared), **negative** (where it breaks), **neutral** (untested). If the negative dominates the load-bearing relations → discard. The **neutral residue** is where the import generates novel predictions rather than relabeling.
   - **Consistency check** — does the mapping contradict what you already know about the problem (your data, your ontology)? If it implies something false, kill it.
   - **Novelty dedup** — embed against prior attempts; reject near-duplicates.
   - **Never let the LLM be the sole judge.** The demand effect means it will manufacture an analogy on request whether or not real structure exists. Require a structural verifier, then test the mapping like any other idea — *against the frozen eval.*

5. **Retain** — store accepted mappings as cases so retrieval improves with use.

**Punchline:** generation is cheap; **verification is the whole game.** A tangential idea earns its place only when, after the sanity-check survives, it produces a candidate that the frozen eval scores higher than the incumbent — exactly like any other idea. The cross-domain framing buys you *reach*, not a free pass on evidence.

---

## Meta-science — when the bet actually pays off

- **Atypical combinations win** (Uzzi et al., *Science* 2013): hit ideas = a **conventional core + ONE atypical import** (~2× citations). Not maximal exoticness — graft *one* well-chosen foreign ingredient onto a solid base. So the tangential engine should usually fire **one** cross-domain swap at a time, on top of a working baseline.
- **Form is the currency** (Wigner): search by the problem's **form/structure, not its subject area**.
- **Absorptive capacity** (Akcigit et al.): you can only absorb a foreign field that's reasonably **near your knowledge network** — prefer adjacent imports over maximally exotic ones.
- **Tools-to-Theories** (Gigerenzer): transfer runs instrument→model, and the borrowed tool silently shapes the resulting theory — note what assumptions you're importing along with the math.
