# Source inference, proposed mathematics and security/utility evaluation

**Completed execution: 2026-09-25, 18 new trained endpoints, 75.64 seconds.**
The source interpreter and proposed formulas are implemented. The benchmark has
not received independent labels, and **neither dataset passed the predeclared
utility-noninferiority gate**. This is not a completed proof of deployment security
or journal novelty.

Open the [four-page PDF](../../reports/Source_Security_Utility_2026-09-25.pdf),
[prospective protocol](../../docs/protocols/source_security_utility_2026-09-25.md),
and [formal model, derivations and assumptions](../../docs/theory/source_scope_and_utility.md).
The earlier [96-endpoint configuration study](../static_policy_2026-09-25/README.md)
is separate evidence and was not overwritten.

## Requirement coverage

| Requested contribution | Implemented / measured | What remains unestablished |
|---|---|---|
| Infer reuse/correlation from implementations | AST propagation through integer expressions, aliases, helpers, finite pools, shared prefixes and explicit concatenated projection blocks | Arbitrary Python/dataflow and numerical correlation; independently unseen constructions |
| Formal analysis and new mathematics | Conditional structural-induction argument; proposed exposure reuse mass and utility-constrained gate; qualified ideal collision envelope | Independent proof review and priority; general privacy bounds for actual finite implementations |
| Comparison with rules and existing tools | 24 cases, YAML baseline, Bandit 1.8.6, separate finite-domain runtime oracle, raw predictions and abstentions | Independently authored/labeled cases and a specialist-analysis baseline |
| Lower leakage with retained legitimate matching | New paired learned attacks and validation-thresholded, held-out trusted-key verification | Utility noninferiority: both primary gates fail at the fixed three-point margin |

## Source analyzer

[SourceAnalysis](../../src/biometrics_ai/protection/source_analysis.py) parses Python
without executing it. Its abstract values are fixed, record-injective,
bounded(K), and unknown. Adding a constant or nonzero integer multiplication can
preserve injectivity; modulo/masking impose a finite image. Hashing a pool slot
does not restore per-record separation. Positional local helpers and aliases are
inlined to a depth cap. Trusted BioHash/KDF contracts identify protection sinks.

The matrix extension propagates block widths and key provenance through explicit
`_orthonormal_projection` calls, NumPy `concatenate(..., axis=1)`, matrix products,
and zero thresholding. It detects a shared 16-column block next to a fresh
48-column block without a named correlated-policy condition. This is structural
sharing inference, not general inference of covariance between arbitrary matrices.

Assumptions: unique integer record IDs; other entry inputs fixed in the audited
context; trusted unmodified callees; no reflection, monkeypatching or external
mutation; an ideal collision-free KDF. Actual keys are 64-bit truncated hashes,
so the ideal injectivity result requires a collision qualification. Key uniqueness
alone does not establish entropy, secrecy or independent random transforms.

Unsupported control flow/calls produce unknown, not secure. The repository's
branch-heavy `protect_embeddings` is outside this subset and returns unknown.
The actual [three study recipes](../../scripts/diagnostics/source_policy_recipes.py)
are analyzed and their numerical outputs are checked against the batched evaluator.
A bounded(K) finding signals finite capacity; it need not imply an observed
collision in a deployment of at most K records. No production approval is emitted.

## Proposed mathematical contribution

Let E contain target-training and target-target pairs, with n target records and
m training records. Component j has output weight w_j and transform label Z_rj.
Define **exposure reuse mass**:

$$\mathcal{R}_E=\sum_{(r,s)\in E}\sum_j w_j\Pr[Z_{rj}=Z_{sj}].$$

For IID uniform slots from pools K_j:

$$\mathcal{R}_E=\left(nm+\binom n2\right)\sum_j\frac{w_j}{K_j}.$$

This equals an expected weighted repeated-component count by linearity of
expectation. It can exceed one and is **not identity leakage or a privacy bound**.
For IID biased slots, use sum_k p_jk^2. A capacity upper bound provides only a
collision lower bound under IID allocation, not an upper security guarantee.

A separate coupling/union-bound derivation uses UNWEIGHTED component collisions
and requires independent hidden isotropic component transforms. It is usually
vacuous for small pools and does not apply to the actual dependent correlated
orthogonal construction or PolyProtect. See the full assumptions and proof sketch
in the theory note. Weighting that privacy bound by w_j would not be justified.

Define an operational acceptance gate with leakage L, legitimate TAR U and FMR F:

$$\mathcal{G}_{\delta,\tau}=
\mathbf1\{\operatorname{LCB}(L_b-L_c)>0\}
\mathbf1\{\operatorname{LCB}(U_c-U_b)\geq-\delta\}
\mathbf1\{\operatorname{UCB}(F_c)\leq\tau\}.$$

Here delta = 0.03 and tau = 0.02 were fixed before execution. Validation thresholds
target 1% FMR; the 2% ceiling is a separate test-set acceptance tolerance. These
are exploratory operational choices, not professor-approved deployment margins.
The proposed contribution is their domain-specific combination and source-derived
reuse accounting, **not discovery of expectation, coupling or noninferiority**.
Independent literature review is necessary before calling either expression novel.

## Benchmark: report abstentions honestly

All 24 cases were authored in this session. A separate executable oracle enumerates
actual component key labels over 64 record IDs and never reads static predictions.
It labels observed repetition, not full biometric leakage. Distinct labels in
this finite domain do not prove freshness on all integers. There are 17 observed-
reuse and seven no-reuse-observed cases; no cases are unlabeled by the runtime oracle.

| Method | TP | FP | TN | FN on decided cases | Abstain |
|---|---:|---:|---:|---:|---:|
| Source interpreter | 13 | 0 | 7 | 0 | 4 |
| YAML checker, declared fresh policy | 0 | 0 | 7 | 17 | 0 |
| Bandit 1.8.6, any warning | 1 | 0 | 7 | 16 | 0 |

Source coverage is **20/24 (83.3%)**. Detection across all observed-reuse cases is
**13/17 (76.5%)**, counting unknown cases as undetected. The four abstentions are
integer division, record-minus-itself cancellation, a branch and an external RNG
call. These are not counted as safe or omitted from the denominator.

Bandit emits B311 on the RNG example; it did not infer biometric transform reuse.
It is a general security scanner, not a competing specialized key-scope analysis.
The YAML checker cannot inspect a source implementation that contradicts its
declared fresh condition. These are useful baselines, not grounds for universal
analyzer superiority or a real-world accuracy estimate.

- [Per-case predictions, labels and blank reviewer-label column](benchmark/benchmark.csv)
- [Corpus with source text and hashes](benchmark/corpus.json)
- [Full source traces and runtime-label counts](benchmark/details.json)
- [Counts and tool version](benchmark/summary.json)
- Raw per-case Bandit JSON and executable source fixtures are in the benchmark directory.

**Independent review is pending.** An external reviewer should first label the
source fixtures without consulting predictions, add independently designed cases,
and lock labels before evaluation. Alpha-renaming our own examples is not an
independent holdout. No specialist literature search or human adjudication has
been silently substituted with an automated same-author benchmark.

## Matching architecture and experiment

The trusted verifier has a raw probe embedding and can retrieve the claimed
enrollment's secret key from an external key service. It re-encodes the probe under
that key and compares Hamming agreement with the enrolled BioHash. Both baseline
and candidate receive the same authorized capability. The template-only attacker
does not receive the keys or compatible-output oracle. This is not direct cross-key
matching and is not a drop-in defense with unchanged infrastructure.

MOBIO/FEI; sign-corrected 64-bit BioHash; pool 4, shared 16/64 projection and fresh
keys; three joint transform/model seeds; one new identity partition; ten records
per set and mean-pool MLP; 120-epoch cap/patience 30. The three seed draws measure
joint sensitivity, not independent key-by-model factors. Attacker training remains
paired with the realized baseline pool, on disjoint identities.

Validation identities select each threshold using impostor scores only; thresholds
are applied unchanged to test identities. Means below average identity-level
rates across the three seeds. Detailed identity scores stay in ignored local
results, not shareable exports.

| Dataset | Attack pool 4 | Attack fresh | TAR pool 4 | TAR fresh | FMR pool 4 | FMR fresh |
|---|---:|---:|---:|---:|---:|---:|
| MOBIO | 27.08% | 3.47% | 95.45% | 96.87% | 0.59% | 0.77% |
| FEI | 27.92% | 2.50% | 95.71% | 95.67% | 0.91% | 0.80% |

The uncertainty-aware primary gate uses 10,000 crossed joint-seed/probe-identity
bootstrap draws and a Bonferroni tail probability of 0.05/6 for six one-sided bounds.
It is conditional on the realized enrollment gallery and has no finite-sample
coverage guarantee.

| Dataset | Leakage reduction LCB | TAR difference LCB | Fresh FMR UCB | Gate |
|---|---:|---:|---:|---|
| MOBIO | +0.42 points | -3.94 points | 1.43% | FAIL: TAR noninferiority |
| FEI | +5.00 points | -5.68 points | 1.14% | FAIL: TAR noninferiority |

Both leakage reductions have positive lower bounds, and both fresh FMR upper
bounds are below 2%. **Neither TAR lower bound clears -3 points.** Similar average
TAR is therefore not sufficient to claim demonstrated retention under the stated
criterion. Margins and seeds were not changed after seeing this result.

The partial-sharing control gives mean attack top-1 7.36%/4.48% on MOBIO/FEI versus
3.33%/2.50% chance. Those are secondary descriptive values, not a corrected claim
that shared components necessarily enable the trained attack. Its TAR means are
95.45%/93.85%. All seed-level endpoints and secondary contrasts remain exported.

## Limitations and next evidence

- Independent labels, independently unseen constructions and specialist analyzer comparisons remain open.
- The source language is restricted; branches/loops and general covariance inference are unsupported.
- Three joint seeds, one partition and small galleries limit statistical precision.
- Utility inference is conditional on the gallery and validation-chosen thresholds; shared enrollment dependence is not a population-level uncertainty model.
- The trusted-key architecture changes custody and compute requirements. No latency/availability benchmark or key-service compromise defense is claimed.
- Public research seeds are not deployment secrets; unrestricted compatible-output queries invalidate the attacker restriction.
- No new SCface run, PolyProtect utility study, new cryptographic transform, certified novelty or journal-tier upgrade follows.

A further study should use a prospectively powered, independently specified
replication and approved utility margins, not repeat seeds until the existing gate
passes. The present gate failure must remain part of the record.

## Provenance and post-execution correction

[The execution manifest](execution_manifest.json) records all source/protocol/input
hashes, package versions, seeds, thread counts, budget and completion. The base
commit does not contain uncommitted additions. [Executable-recipe audits](source_audits.json),
[18 endpoint summaries](endpoints.csv), and [primary/secondary effects](security_utility_effects.csv)
are unchanged.

A post-execution soundness check found stale local-function summaries after a
later import rebound the same module name. Helper and entry-point resolution were
corrected. The exact originally executed analyzer is preserved in
[executed_source_analysis.zip](executed_source_analysis.zip) and verified against
its original manifest hash. Other executed sources still match the checkout.
Tests recompute all 24 static decisions and runtime labels after the fix: all
remain unchanged. No benchmark table, learned endpoint, threshold, interval or
manifest was rewritten to conceal this correction.

## Reproduction and use

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[analysis,presentation,dev]"
.\.venv\Scripts\python.exe -m biometrics_ai.protection.source_analysis scripts/diagnostics/source_policy_recipes.py --entry recurring
.\.venv\Scripts\python.exe -m biometrics_ai.protection.source_analysis scripts/diagnostics/source_policy_recipes.py --entry partial
.\.venv\Scripts\python.exe -m biometrics_ai.protection.source_analysis scripts/diagnostics/source_policy_recipes.py --entry separated
.\.venv\Scripts\python.exe -m pytest tests/unit/test_source_analysis.py -q
.\.venv\Scripts\python.exe scripts/figures/make_source_security_report.py
```

Execution used `python scripts/train/run_source_security_utility.py`. The runner
refuses to overwrite existing outputs. A new study requires explicitly versioned
output paths and a new prospective protocol. Do not delete the completed study
to obtain another favorable draw. The source CLI emits a conditional analysis
report only; it is not a production enforcement/approval command.

## Attribution and novelty boundary

- Cousot and Cousot (1977), [Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml), supplies the established general analysis framework. This restricted straight-line interpreter does not implement a general fixpoint engine.
- [Bandit 1.8.6 documentation](https://bandit.readthedocs.io/en/1.8.6/) describes its AST/plugin-based common-security checks; that is the scope of the external baseline.
- Linearity of expectation, collision probabilities, coupling/union bounds and noninferiority testing are established mathematics. Their proposed biometric-policy integration needs specialist prior-art review, not merely new terminology.
- [Earlier biometric closest-work review](../../docs/literature/closest_work_2026-09-18.md) remains relevant but is not a review of all source-level analysis literature.

The two directly linked foundational/tool pages were checked on 2026-09-25.
No exhaustive novelty search or independent mathematical review is claimed.