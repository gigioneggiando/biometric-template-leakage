# Source-derived scope and utility-constrained remediation

Proposed research construction, 2026-09-25. This document derives an accounting
functional and an acceptance criterion from established probability and
noninferiority concepts. Neither a new notation nor this derivation establishes
research priority. Independent mathematical and literature review remain open.

## Abstract domain and supported language

The analyzer interprets Python ASTs, without executing them, using the domain
D = {fixed, record-injective, bounded(K), unknown}. The distinguished record
argument ranges over unique mathematical integers. Other entry inputs are held
fixed in the audited context. This models per-record key allocation, not secrecy.

- Literals and fixed context parameters are fixed.
- The record argument is record-injective.
- Adding/subtracting an integer constant or multiplying by a nonzero integer
  preserves injectivity; multiplying by zero is fixed.
- Modulo a positive K gives capacity at most K. Masking by a nonnegative integer
  gives capacity at most 2^popcount(mask). Hashing cannot restore lost diversity.
- A trusted deterministic KDF of fixed inputs is fixed. One injective integer
  argument and otherwise fixed inputs yields conditional injectivity under an
  ideal collision-free KDF contract. Bounded inputs give at most the product of
  their capacities. Finite real KDFs require an explicit collision qualification.
- Straight-line assignments, aliases and positional local helper calls propagate
  summaries; recursion, branches, loops, dynamic calls and other unsupported
  expressions/statements yield unknown. Unknown calls never manufacture freshness.
- BioHash whole-transform and correlated-BioHash prefix/suffix contracts identify
  where key provenance controls protected records. Other transforms need reviewed
  contracts. Explicit orthonormal-projection blocks, NumPy axis-1 concatenation,
  embedding-matrix multiplication and zero thresholding additionally propagate
  component widths/provenance, detecting shared components in assembled transforms.
  This prototype does not infer arbitrary numerical matrix correlation.

`reuse` means a sink has fixed/finite provenance, not necessarily that two records
in a specific finite deployment collide. A bound K only forces a collision with
more than K distinct records (pigeonhole principle). `conditional_fresh` means all
reached modeled sinks have injective provenance and no unsupported construct was
encountered. It is not an unlinkability certificate. `unknown` is an abstention.
The `complete` field prevents a partial known finding from hiding unsupported code.

### Conditional soundness statement

For straight-line programs in the supported subset, unique integer record IDs,
fixed non-record inputs, trusted unmodified imported functions, no decorators,
reflection, monkeypatching or external mutation, and the ideal injective KDF
contract, the inferred fixed/capacity/injectivity properties hold at modeled sinks.
Proof is by structural induction on expressions and substitution through acyclic
helper calls: constant and affine cases are immediate; remainder/mask images have
the stated cardinalities; deterministic maps cannot enlarge finite images; KDF
injectivity preserves distinct tuples under its contract. Composition closes the
induction. Unsupported constructs invalidate completeness, rather than extending
the theorem. Helper expansion is depth-limited to 16; no linear-time claim is made
because repeated inlining can grow with the call tree. Parsing trusted source is
not a sandbox for arbitrary adversarially large inputs.

Real `generate_key` truncates SHA-256 to 64 bits and serializes arguments with
delimiters. The injectivity contract is an idealization, not true for all inputs.
For fixed domain/master and an integer record argument the serialization is
unambiguous, but a random-function model still gives collision probability at most
q(q-1)/2^65 for q distinct derivations. Freshness does not establish pseudorandom
independence, high-entropy master secrets, correct matrix sampling or key custody.

## Proposed component-weighted reuse functional

Let training records number m and target exposures number n. Let E contain
target-training pairs and unordered target-target pairs, so

$$|E| = nm + \binom{n}{2}.$$

For transform component j, let w_j > 0 be its fraction of the protected output,
with sum_j w_j = 1, and let Z_rj name the realized component transform for record r.
Define the proposed **exposure reuse mass**:

$$\mathcal{R}_E = \sum_{(r,s)\in E}\sum_j w_j
  \Pr[Z_{rj}=Z_{sj}].$$

By linearity of expectation, this equals the expected total weighted repeated
component count on E. It needs no independence across pairs. It is not mutual
information, attack accuracy, or a privacy bound. It can exceed one.

For IID uniform component slots of size K_j, the collision probability is 1/K_j:

$$\mathcal{R}_E = \left(nm+\binom n2\right)\sum_j \frac{w_j}{K_j}.$$

Ideal fresh components contribute zero; a fixed shared fraction rho and otherwise
fresh components give R_E = |E| rho. For IID nonuniform slots p_jk, replace 1/K_j
with sum_k p_jk^2. A static capacity upper bound K implies only the LOWER collision
bound 1/K for IID allocations, not an upper privacy guarantee. Deterministic or
dependent allocations require their actual pairwise collision law. Correlated
but unequal matrices are not counted; general correlation inference remains open.

### Separate idealized collision envelope

Suppose additionally that distinct component labels select mutually independent,
hidden, source-independent isotropic component transforms, with fixed-norm inputs
and source-independent postprocessing, and that all target components are
independent of training side information whenever there is no equality on E.
Compare the real view with an ideal simulator that uses fresh independent transforms
for each target component. Couple the views until the first reused component.
The coupling inequality and union bound give

$$\operatorname{TV}(P_{\rm view},P_{\rm ideal})
 \leq \Pr[\mathrm{any\ reuse\ on}\ E]
 \leq \min\left(1,\sum_{(r,s)\in E}\sum_j
       \Pr[Z_{rj}=Z_{sj}]\right).$$

The final sum is UNWEIGHTED. Substituting weighted R_E here is generally invalid:
even one shared component can carry distinguishing information. The envelope is
usually vacuous for small pools and large training sets. It is not a proved bound
for finite NumPy keys or PolyProtect. The repository's correlated orthogonal
construction conditions private directions on a shared basis and does not satisfy
the independent-component assumptions; only structural reuse accounting applies.
This is an application of standard coupling/union-bound reasoning, not claimed as
a newly discovered probability theorem.

## Utility-constrained evidence gate

Let L be attacker top-1, U the legitimate true-accept rate (TAR), and F the
legitimate false-match rate (FMR). Thresholds are chosen using validation identities
only. For baseline b and candidate c, define the proposed operational criterion

$$\mathcal{G}_{\delta,\tau} =
 \mathbf{1}\{\operatorname{LCB}(L_b-L_c)>0\}
 \mathbf{1}\{\operatorname{LCB}(U_c-U_b)\geq-\delta\}
 \mathbf{1}\{\operatorname{UCB}(F_c)\leq\tau\}.$$

The confidence bounds, multiplicity allocation, margin delta and FMR ceiling tau
must be chosen before inspecting test outcomes. A failure is reported as failure,
not repaired by increasing delta or selecting a new key seed. This combines
established paired improvement and noninferiority tests; it is a proposed workflow
criterion, not evidence of priority or universal security.

### Authorized matching architecture

Enrollment stores a keyed template and a handle to an external secret key service.
A trusted verifier obtains the raw probe embedding, re-encodes it under the claimed
enrollment's key, then compares protected codes. Fresh enrollment keys therefore
need not prevent legitimate same-key verification, while a template-database-only
attacker does not get compatible encodings or keys. A database-plus-key-service
compromise or unrestricted output-visible chosen-probe oracle is outside this
defense. This is not public cross-key matching or a drop-in improvement at fixed
infrastructure. Keys, compute and availability costs must be stated. Deterministic
public research seeds simulate experiments only; they are not deployable secrets.