# Source-Level Key-Scope Analysis and Utility-Constrained Biometric Protection

Working draft, revised 2026-09-26. The source analyzer, matched remediation study and utility confirmations are separate from the fixed-pool follow-up, independent-pool study, earlier exploration and raw-norm audit. Later evidence does not retroactively change an earlier primary family. No independent human review, global priority or source-exact reproduction is claimed.

## Abstract

We extend configuration auditing with a bounded Python source interpreter that propagates record-dependent key provenance through arithmetic, aliases, conservative branches, finite literal loops, containers, helper calls and reviewed BioHash, IoM-GRP and PolyProtect sinks. On a frozen 20-program internal confirmation, version 2 emits 19/19 correct decisions, abstains once (95% coverage) and makes no false-fresh decision. Version 3 retains these outcomes and correctly classifies six executable recurring/fresh protection recipes; over the combined 26 cases it emits 25/25 correct decisions at 96.15% coverage, while a transparent intraprocedural baseline emits six decisions and gets five correct. These programs and labels were authored within the project, so independent validation remains pending. We also propose component-weighted exposure reuse mass and an uncertainty-aware security/utility gate under explicit assumptions. A separate 18-endpoint BioHash pilot reduces mean learned linkage from 27.08% to 3.47% on MOBIO and 27.92% to 2.50% on FEI, but both predeclared utility gates fail. Two utility-only replications subsequently pass 2/4 MOBIO/FEI cells and 0/4 new MOBIO/SCface cells. The source analysis and mathematical construction are proposed contributions, not established priority, a general privacy proof, or demonstrated deployment readiness.

Earlier configuration-only contribution and its separate experiment:

We introduce Key-Scope Static Analysis (KSSA v1), a configuration-level checker that classifies declared key scope, flags reuse/correlation and slot disclosure, rejects unsupported declarations, and retains explicit scheme/runtime review obligations. It proposes a separate fresh-key policy without altering the source experiment. In a new matched MOBIO/FEI evaluation with two schemes, two identity assignments and three model seeds, all 96 trained endpoints complete. Eight planned ten-record pool-4-minus-fresh comparisons show reductions of 72.08-94.48 percentage points, each with a positive paired crossed-bootstrap interval and Holm p = 0.004. Fresh learned intervals include chance, but native PolyProtect linkage remains descriptively above chance. This supports the audited policy-change workflow under the tested threat model, not general analyzer accuracy, authentication utility, a novel fresh-key defense or universal unlinkability. Sani suggested exploring an algorithmic contribution; Manish proposed this static-analysis direction. Sani has not yet reviewed this implementation or its conclusions, and neither attribution establishes priority.

Historical motivation and boundaries follow, with their evidence families kept separate:

We study how hidden transform reuse conditions the benefit of combining protected face records. An attacker trains on paired examples from the same hidden pool but disjoint identities, then links same-person records to a small closed gallery. The original MOBIO/FEI study has 216 trained endpoints and eight positive planned pool-4 contrasts (21.25-40.83 percentage points; Holm p = 0.004). A three-pool follow-up finds persistent IoM gains but PolyProtect gains from -3.23 to +72.40 points; all direct input-mean versus prediction-mean intervals include zero. An extended MOBIO/SCface study adds 672 endpoints at 1/2/5/10 records and fresh/pool-1/4/8 conditions. Its eight primary gains pass Holm correction (p = 0.004-0.034), including smaller SCface PolyProtect gains of 5.93/5.77 points. Separate raw-input retraining finds near-chance PolyProtect performance and strong IoM pool-4 linkage, but changed seeds, partitions and targets prevent a causal normalization comparison. A local stricter PolyProtect selection rule does not demonstrate reduced native linkage. Prior work already studies multiplicity, joint-score maximal linkability, adaptive identity extraction and residual naive-parameter linkage. Our contribution is the controlled hidden-reuse comparison and its boundaries, not those general observations. Chance-compatible attacks do not establish privacy.

## 1. Introduction

Retained templates can expose several records grouped by an account pseudonym even when real identity and protection keys remain unknown. We study a strong access scenario: paired training examples and targets share the same realized hidden transform pool. We do not claim that this policy is prevalent in products. The question is whether same-person aggregation helps under reuse, and where that statement fails.

Contributions:

The proposed primary contribution is bounded source-derived key/component provenance and a formalized utility-constrained remediation workflow (Section 4.2), extending the earlier configuration checker (Section 4.1). Internal confirmation and executable integration are complete, but independently authored source cases, external labels, priority review and demonstrated utility noninferiority remain open. The following empirical contributions motivate the rules and retain their original limits:

1. **Reuse-conditioned amplification:** eight corrected fixed-pool contrasts, followed by three new pools where IoM gains persist but PolyProtect is pool-sensitive. Earlier four-dataset sweeps are not pooled into these inference claims.
2. **Limits on aggregation:** mechanism controls, shared-key regressions and a competitive prediction-mean baseline constrain interpretation. Neither more records nor a set-trained model is universally better.
3. **Separate native and learned attack surfaces:** reference implementation/matcher checks and genuine raw/shuffled/fixed-radius controls validate the local native computation without attributing it to natural norm leakage or stronger parameter policies.

### Closest research

Li and Hu (2014, DOI 10.1002/cpe.3042) already attack multiple fingerprint templates with disclosed parameters. PolyProtect (2022), IV-C3, evaluates inversion of 1-10 versions of the same embedding with disclosed coefficients/exponents; IV-D finds residual different-image linkage under naive parameters and reduces it through stricter selection. Our different-image hidden-pool learned task differs, but multiplicity and native residual linkage are not novel.

The cancelable-biometrics benchmark already compares recognition, unlinkability and information estimates, including sample-specific keys. FaceLinkGen v3 (3 September 2026) already trains adaptive ArcFace-aligned extractors from paired data under unknown per-query randomness. IoM magnitude independence is prior art. Otroshi Shahreza, Shkel and Marcel (IEEE Access 2024, DOI 10.1109/ACCESS.2024.3433536) study joint-score maximal linkability across modalities, encoders, schemes, keys and scoring functions. The full corresponding author-thesis section 5.4 was inspected; the publisher PDF was blocked and version identity is not certified. Its binary mated/non-mated information measure is not our closed-set top-1. Our recurring-pool sweep and trained different-image aggregation differ from its experiments; multiplicity and multi-key leakage are not new. See the [full-text evidence](../docs/literature/closest_work_2026-09-18.md). This bounded review does not establish global priority.

## 2. Threat model

Attacker capabilities: knows the scheme family and hyperparameters; observes $n \in \{1, 2, 5, 10\}$ protected records of a target from different images, except in the same-image control; never observes key values; may train on paired protected records and unprotected embeddings of disjoint identities. Goal: link the target to a held-out unprotected gallery, with one image per identity. Gallery sizes are 30 on MOBIO, 25 on LFW, and 40 on FEI, giving chance rates of 3.33%, 4.00%, and 2.50%. LFW and FEI boundary studies use endpoints 1 and 10, not the full exposure sweep.

Conditions:

- **Fresh keys (K0).** Every source record has its own key; train/validation/test key pools are disjoint. The theorem describes an idealized rotationally invariant version of this condition, not every finite seeded implementation.
- **Recurring pool of size $k$ (R-$k$).** A hidden pool of $k$ transforms is drawn once and each record is assigned one by a hash of its sample ID. Keys recur across identity splits; slot labels are hidden. $k = 1$ is the unknown-shared-token setting. Increasing pool size to the number of records does not create K0 because hash assignment can still collide; K0 explicitly generates a distinct key per source record.
- **Controls.** Unprotected oracle and shared-key calibration. Earlier MOBIO/LFW/FEI setups reach 100%; SCface's camera-shift oracle is 84.375%, not 100%.

**Access justification.** Persistent account/session identifiers can group records without revealing gallery identity. An authorized enrollment/query interface using consented faces, or a provider observing originals and protected outputs, could supply paired training data. Recurring-pool training must use the same realized hidden pool as the targets; an unrelated-key proxy is insufficient. Lawful public or consented images could supply a reference gallery. Here target membership is guaranteed among only 25-40 identities (SCface: 26); gallery images are excluded from exposures. Open-set search, internet-scale distractors, unknown grouping and cross-provider transfer are untested. Fresh independent keys can impair legitimate matching and are not a validated drop-in defense.

Prior stolen-token attacks (Nagar et al. 2010; Lacharme et al. 2013; Feng et al. 2014; Dong et al. 2019, 2022; Wang et al. 2020; Ghammam et al. 2020; Durbet et al. 2021) assume the transform is known. Record multiplicity has been analyzed for fuzzy vaults (Scheirer and Boult 2007; Merkle and Tams 2013), where no secret rotation is involved. PolyProtect (Krivokuca Hahn and Marcel 2022, Section 4.3) already studies one to ten records with disclosed parameters. Our hidden-parameter learned linkage task differs, but multiplicity alone is not novel. Priority claims await an independent current literature review; see the [local review memo](../docs/review/scheme_pilot_review_2026-09-12.md).

## 3. Theory

Statement and proof: [multiplicity_invariance.md](../docs/theory/multiplicity_invariance.md). Summary: if $P_K R \overset{d}{=} P_K$ for all $R \in O(d)$, then for unit $x, y$, $P_K x \overset{d}{=} P_K y$; with independent keys the joint law is a product of source-independent factors. Under a uniform identity prior, expected Bayes top-1 is chance for every record count. With admissible side information Z, joint independence of key randomness from identity, sources and Z is required; templates give no gain beyond the Bayes decision from Z alone. Without normalization, norms bound possible information, but need not leak: positive scaling leaves zero-threshold BioHash and IoM-GRP unchanged. This is not a finite-implementation or PolyProtect privacy theorem.

Scope: the theorem assumes ideal Gaussian or Haar/Stiefel sampling, independent hidden keys, fixed-norm sources, and source-independent postprocessing. It does not cover key reuse, correlated keys, non-invariant transforms, or key-correlated side information. Raw `numpy.linalg.qr` does not implement the Haar sign convention (Mezzadri 2007). The sign-corrected variant gave fresh-key 10-record top-1 2.64%, pool 1 74.58%, and pool 5 48.06% (`haar_corrected_key_pool_summary.csv`). These results are qualitatively similar to the default construction; no equivalence test was performed. Sign correction aligns the ideal sampling construction, but finite PRNG keys and numerical precision remain implementation assumptions requiring review.

## 4. Experimental setup

- Data: MOBIO selected still images, 150 identities, 12 sessions, 1,799 embeddings (one detection failure), 90/30/30 identity-disjoint splits; one gallery image per identity held out; eight nested exposure permutations per identity; 720/240/240 attack sets per level.
- Embeddings: InsightFace `buffalo_l` ArcFace (SHA-256 recorded), YuNet detection, L2-normalized.
- Protection: 128-bit BioHash (key-seeded orthonormal Gaussian projection, sign threshold); paper-specified MLP-Hash (512-1024-1024-1024-512, ReLU, semi-orthogonal key-seeded layers, output-mean binarization; not source-exact, authors' repository unavailable).
- Attackers: single-template MLP (n=1); mean/max-pool MLP and DeepSets (n>1); hidden 256; cosine + 0.1 MSE. Earlier studies use 400 epochs/patience 60; matched follow-up uses 120/patience 30, three seeds and mean/DeepSets at n=10. Target: normalized mean of exposed source embeddings, not the gallery.
- Metrics: top-1/top-5 linkage against the unprotected gallery, AUROC, EER, TAR@FAR, 2,000-resample identity-clustered 95% intervals. Preregistered per-pool criterion: all clustered intervals above chance and at least five points over the fresh endpoint.

### 4.1 Static analysis algorithm and matched remediation

KSSA v1 operates on the existing YAML configuration language, not arbitrary Python programs. For each scheme/condition pair it computes an abstract scope in {fresh-declared, shared-across-splits, shared-projection, unknown}. Positive finite recurring pools and shared calibration keys emit KEY_REUSE. A positive shared BioHash projection dimension emits KEY_CORRELATION. Exposed key-slot labels emit SLOT_DISCLOSURE. Unsupported schemes/conditions and malformed required declarations block analysis. This is not exhaustive parameter-schema validation. PolyProtect retains NATIVE_LINKAGE_REVIEW; uncorrected BioHash retains HAAR_ASSUMPTION; every configuration retains RUNTIME_ASSUMPTIONS. Classification requires O(S*C) steps for S schemes and C conditions, excluding string parsing/output. The decision is block or review, never certified secure.

The recommendation replaces the key condition with independent_unseen_keys, removes slot disclosure, and preserves the remaining configuration in a separate object. This is an operationalization of a known key-freshness principle, not a new cryptographic transform. Static findings cannot certify production entropy/secrecy, input normalization, record-ID uniqueness, side channels, implementation fidelity, or legitimate matching utility. The opt-in enforcement command exits nonzero for both blocking and unresolved-review outcomes; research runners still allow deliberately insecure controls.

The [new protocol](../docs/protocols/static_policy_2026-09-25.md) was written before execution. Two MOBIO/FEI identity assignments (92531/92543), IoM-GRP/PolyProtect, seeds 701/709/719, and one/ten exposures produce 16 cells and 96 trained endpoints in 352.766 seconds. Baseline pool-4 and recommended fresh keys share inputs, splits, set/key seeds, model seeds and training caps (120 epochs, patience 30). Key mechanisms differ, so identical seed numbers do not imply identical draws. Primary inference uses eight paired ten-record baseline-minus-candidate contrasts, crossed seed/identity bootstrap intervals (2,000 draws), identity sign-flips of seed-mean differences (1,999 resamples), and Holm correction over eight tests.

All eight primary reductions have positive intervals and Holm p = 0.004: 92.08/94.44 points for MOBIO IoM, 94.48/94.27 for FEI IoM, 72.08/72.08 for MOBIO PolyProtect, and 83.75/85.52 for FEI PolyProtect. Fresh learned intervals include chance but do not establish equivalence. Fresh PolyProtect native cosine top-1 remains descriptively 10.30-13.33% on MOBIO and 7.80-8.97% on FEI versus 3.33%/2.50% chance. These new native values have no corrected null test; the review warning is retained.

The [full table and reproduction record](../experiments/static_policy_2026-09-25/README.md) and [PDF addendum](Static_Policy_Analysis_2026-09-25.pdf) separate these results from earlier studies. Runtime-agreement fixtures validate declared scope against actual key audits, not detector precision/recall. One pool draw, overlapping identity assignments, three model seeds, one architecture and same-pool paired training access bound inference. No authentication-utility or SCface rerun was part of this initial study; Sections 4.2-4.3 report later, separately frozen evaluations. Rule selection was informed by earlier results, so this is not a blinded discovery benchmark. Independent literature review of configuration-level biometric static analysis remains necessary before asserting novelty.

### 4.2 Source-derived component scope and utility-constrained remediation

**Analysis.** The interpreter reads Python ASTs without executing them. A distinguished unique integer record argument maps to record-injective provenance; fixed inputs, bounded images and unknown expressions form the remaining abstract values. Integer affine maps preserve injectivity; modulo, masking and floor division bound image cardinality; deterministic hashing cannot restore diversity lost by pooling. Acyclic helper calls, positional or keyword binding, aliases, literal container selection, conservative branch joins and finite literal loops propagate summaries to reviewed protection sinks. Explicit projection blocks, concatenation, matrix multiplication and thresholding propagate component widths and key provenance. Version 3 adds explicit sink contracts for the repository's BioHash, IoM-GRP and PolyProtect implementations. This detects structurally shared key material without a named YAML condition, but not arbitrary numerical covariance. Recursion, unbounded loops, dynamic calls and incompatible branch values yield unknown. The full research runner remains outside the supported language; small executable recipes call the actual local protection functions.

**Qualified soundness.** Structural induction establishes the fixed/capacity/injectivity transfer rules for the supported subset with unique integer record IDs, fixed context inputs, trusted unmodified callees, no reflection/external mutation, and an ideal collision-free KDF contract. Real keys truncate SHA-256 to 64 bits, so ideal injectivity is not a universal finite-implementation guarantee. An upper capacity bound K signals possible reuse; it forces a collision only beyond K records. Neither injectivity nor static completion proves secrecy or unlinkability. A post-execution module-binding defect was repaired; the executed source is hash-preserved and all 24 recorded predictions were rechecked unchanged.

**Proposed functional.** For target-training and target-target pairs E, component weights summing to one, and component transform labels Z, define

$$\mathcal{R}_E = \sum_{(r,s)\in E}\sum_j w_j\Pr[Z_{rj}=Z_{sj}].$$

Linearity of expectation identifies this as expected weighted repeated-component mass. For n target records, m training records and IID uniform pools K_j it becomes

$$\mathcal{R}_E = \left(nm+\binom n2\right)\sum_j w_j/K_j.$$

This is structural accounting, not leaked identity information. Nonuniform IID pools require their actual collision sum; a cardinality bound alone cannot upper-bound privacy risk. A separate unweighted collision/coupling bound requires mutually independent hidden isotropic components and can be vacuous. It does not cover the actual dependent correlated-orthogonal construction or PolyProtect. The [full theory note](../docs/theory/source_scope_and_utility.md) states the proof sketch and assumptions. Standard expectation/coupling facts are not claimed as new theorems.

**Benchmark.** A separate runtime label oracle enumerates 64 integer record IDs per trusted synthetic source fixture. Audit found that one of the original 24 expected labels was invalid because it assumed keyword binding that version 1 did not implement. On the remaining 23 valid development cases, version 1 emits 16 correct decisions (69.57% coverage); version 2 emits 22/22 correct decisions (95.65% coverage) and abstains once. A subsequently frozen set of 20 new, valid internally authored programs gives version 2 19/19 correct emitted decisions, one abstention, 95% coverage and no false-fresh result.

Version 3 then adds scheme-specific sink contracts without changing the frozen confirmation outcomes. Six executable recipes cover recurring-pool and record-fresh policies for BioHash, IoM-GRP and PolyProtect and call the actual local protection implementations. Across these six recipes plus the 20 confirmation programs, version 3 emits 25/25 correct decisions at 96.15% coverage, with the existing floor-division-by-one case as its only abstention. A transparent intraprocedural baseline emits only six decisions, gets five correct and misclassifies floor division by one as reuse. The baseline is a sanity check, not a state-of-the-art comparator. All cases and expected labels were authored inside this project; independent human labels and independently authored applications remain absent. See the [frozen confirmation](../experiments/source_holdout_v2_confirmation_2026-09-25/README.md) and [real-integration evaluation](../experiments/source_real_integration_2026-09-25/README.md).

**Utility-constrained evidence.** Let L be attack top-1, U legitimate TAR, and F legitimate FMR. The proposed gate is

$$\mathcal{G}_{\delta,\tau} =
\mathbf1\{\operatorname{LCB}(L_b-L_c)>0\}
\mathbf1\{\operatorname{LCB}(U_c-U_b)\geq-\delta\}
\mathbf1\{\operatorname{UCB}(F_c)\leq\tau\}.$$

The prospective pilot fixes delta = 0.03 and tau = 0.02. Validation identities select thresholds targeting 1% FMR; held-out test identities evaluate TAR/FMR. Both arms use a trusted raw-probe verifier that retrieves the claimed enrollment key from outside the template database and re-encodes the probe under it. This excludes key-service compromise and unrestricted compatible-output queries and introduces real custody/compute requirements. It is not public cross-key matching or unchanged-infrastructure security.

The [18-endpoint study](../experiments/source_security_utility_2026-09-25/README.md) completed in 75.64 seconds: MOBIO/FEI, sign-corrected 64-bit BioHash, pool 4/shared 16-of-64/fresh conditions, three joint key/model seeds, one identity assignment and ten-record mean pooling. Mean pool-4 to fresh learned linkage falls 27.08% to 3.47% on MOBIO and 27.92% to 2.50% on FEI. Legitimate TAR changes 95.45% to 96.87% and 95.71% to 95.67%; fresh FMR is 0.77%/0.80%. Six one-sided bounds use 10,000 crossed joint-seed/probe-identity bootstrap draws and Bonferroni tail allocation 0.05/6, conditional on the enrollment gallery. Leakage-reduction lower bounds are +0.42/+5.00 points and fresh FMR upper bounds 1.43%/1.14%, but TAR-difference lower bounds are -3.94/-5.68 points. **Both primary gates fail on utility noninferiority.** Similar average accuracy does not establish utility retention under the chosen margin. The failed gates, margins and results are retained without post-hoc relaxation.

**Contribution boundary.** The proposal integrates key/component provenance, reuse accounting and utility-constrained evidence. Abstract interpretation, fresh-key principles, collision formulas and noninferiority are established ideas. The [study attribution and review requirements](../experiments/source_security_utility_2026-09-25/README.md#attribution-and-novelty-boundary) identify independent labeling, specialist prior-art review, proof review, application-owner margin approval and a prospectively powered joint replication as remaining gates. A new expression alone is not evidence of journal-level novelty. The [four-page PDF](Source_Security_Utility_2026-09-25.pdf) presents these limitations alongside the measured results.

**Post-execution correctness amendment, 2026-09-26.** A counterexample to v2/v3's
cross-path freshness inference was reproduced: protecting directly in each branch
with index `record_id` for odd records and `record_id + 1` for even records yields
four distinct keys for eight records, yet the original implementation emitted a
complete fresh decision. The branch join did not invalidate prior sink summaries.
The [repair and regression record](../experiments/source_branch_fix_2026-09-26/README.md)
now conservatively marks branch-local sinks and unsupported predicates incomplete,
preventing that freshness claim. This does not prove soundness for all Python.
All 69 evaluations on the overlapping historical internal corpora retain their
predictions; the new counterexample abstains. These are not independent validation
results. Exact executed v2 source bytes are archived, original tables/manifests
remain unchanged, and line-ending conversions in checkout verification are explicit
and accepted only when they reproduce an existing recorded hash. Independent
review is deferred at the user's request and remains an open requirement.

### 4.3 Review preparation and fixed utility-only replication

An [answer-free packet](../experiments/source_review_2026-09-25/README.md) provides
24 neutral-named source cases and blank labeling forms. This masks predictions
and runtime answers, not code behavior; no independent labels or new external
cases have been received. An [internal review memo](../docs/review/source_proof_novelty_2026-09-25.md)
records proof obligations and targeted project-page comparisons with established
abstract interpretation and crypto misuse tools. External mathematical review,
full-paper novelty comparison and application-owner margin approval remain open.

A [prospectively fixed utility replication](../experiments/utility_replication_2026-09-25/README.md)
ran while those reviews were pending, with twelve new key seeds, two new identity
partitions per dataset and no new attacker training. All 96 evaluations completed
in 12.36 seconds. The original delta = 0.03 and tau = 0.02 were retained. Eight
one-sided bounds use 20,000 crossed key/probe-identity bootstrap draws and alpha
0.05/8. MOBIO TAR lower differences are -2.32/-2.02 points, passing both utility
gates; FEI gives -3.71/-3.61 points and passes neither. All four FMR upper bounds
are below 2%. Thus 2/4 utility gates pass, not a new joint security gate. The
earlier 0/2 joint result is unchanged. Partitions overlap, uncertainty is conditional
on enrollment galleries and observed validation thresholds, and the sample-size
rationale is heuristic rather than a formal power calculation. A post-review,
prospectively powered joint confirmation remains a future gate.

A second [prospectively frozen utility confirmation](../experiments/scface_utility_confirmation_2026-09-25/README.md)
used MOBIO and SCface, two new identity partitions (93083/93089), twelve new
key seeds and the same three-point TAR margin and 2% FMR ceiling. All 96
evaluations completed. Every FMR upper bound is below 2%, but all four TAR
lower bounds fail noninferiority: -4.87/-3.16 points on MOBIO and -5.36/-3.57
points on SCface. Hence 0/4 cells pass. MOBIO mean TAR changes are only
-0.81/-0.73 points, while SCface changes are +0.22/+1.63 points; the failure is
therefore an uncertainty result, not evidence of a consistent mean degradation.
It also shows that the prior 2/2 MOBIO utility passes are partition-sensitive.
SCface absolute TAR is only 29-32%, limiting its operational relevance under
this verifier.

A post-hoc, non-confirmatory [failure diagnostic](../experiments/utility_failure_diagnostics_2026-09-26/README.md)
keeps every frozen decision and margin unchanged. Across the four cells, the
standard deviation of identity-mean TAR changes is 3.17-6.55 points and the
standard deviation of key-mean changes is 1.75-5.93 points. Mean threshold
shifts are at most 0.26 points in magnitude. On SCface, fresh TAR ranges from
8.10-10.21% at distance 1 to 50.46-55.95% at distance 3, and the fresh-minus-
recurring direction is not consistently negative. These descriptive patterns
motivate a new authorized identity cohort, a prospectively justified sample
size using crossed identity/key variability, and predefined capture strata;
they do not rescue the failed gate or establish a cause.

### 4.4 New-participant joint evaluation: proposed, not executed

A [local input audit](../experiments/new_participant_joint_2026-09-25/README.md)
shows all 200 FEI and 150 MOBIO embedding identities were already included in the
original hash-frozen pilot inputs. Additional FEI views and identity repartitioning
do not supply independent people. No new authorized cohort is currently available;
no new-cohort outcomes or new joint pass are reported.

The [proposed fixed protocol](../docs/protocols/new_participant_joint_2026-09-25.md)
uses the actual analyzer trace to motivate a preselected pool-4 to record-specific
key change. It proposes 500 new eligible people (200 train, 100 validation, 200 test),
12 paired key/model draws and matched attack/verification outcomes on the same test
people. Three Bonferroni-allocated one-sided bounds at alpha 0.05/3 govern the single
joint gate, retaining the three-point TAR tolerance and 2% FMR ceiling. The person
count is a planning target pending feasibility and power review, not a demonstrated
power result. Authorization, cross-cohort identity review and independent approval
must precede execution. A new dataset is an external-cohort test, not an FEI extension
by relabeling. The key-policy intervention is evaluated; scanning alone does not
cause the protection improvement or establish source-detector generalization.

## 5. Earlier Exploratory Results (Separate Evidence)

### 5.1 Fresh keys: no useful linkage detected by the tested attacks

10-record DeepSets top-1 under K0: BioHash 3.33% (AUROC 0.4988), MLP-Hash 3.33% (AUROC 0.4998); one-record 2.50-3.33%. Unprotected oracle 100%; shared-key mean pooling up to 80.83% at five records. Across the nine later runs the fresh-key 10-record mean-pool top-1 ranged 1.53-5.56% (chance 3.33%) and never differed from the 1-record rate by more than 2.4 points: (1-record, 10-record) = (3.2, 5.6), (2.9, 3.1), (4.0, 3.6), (2.4, 1.5), (3.8, 4.4), (3.1, 2.6), (3.1, 3.5). Source: `results_summary.csv`, `mlphash_results_summary.csv`, and the `*_summary.csv` files.

### 5.2 Recurring transforms: leakage rises sharply with reuse

10-record mean-pool top-1 (1-record single-MLP in parentheses), randomized assignment. BioHash partitions A, 2, 3 are three identity-disjoint 90/30/30 partitions of MOBIO:

| pool size | BioHash A (dense) | BioHash 2 | BioHash 3 | BioHash B (1/2/5/10) | MLP-Hash |
|---|---|---|---|---|---|
| 1 | - | - | - | 81.67 (75.97) | 71.39 (52.08) |
| 2 | - | - | - | 73.89 (35.00) | 68.89 (33.61) |
| 3 | 65.00 (27.50) | 48.61 (22.36) | 56.39 (5.83) | - | 54.31 (3.06) |
| 4 | 54.03 (3.47) | 48.61 (7.64) | 51.94 (5.42) | - | 37.78 (4.58) |
| 5 | - | 40.28 (6.39) | 8.06 (4.86) | 51.11 (4.31) | 22.92 (4.44) |
| 6 | 17.36 (3.47) | 36.39 (6.39) | 8.61 (4.58) | - | - |
| 7 | 34.44 (4.17) | 30.42 (5.00) | 8.89 (5.69) | - | - |
| 8 | 10.42 (4.03) | 14.17 (3.19) | 3.89 (3.06) | - | - |
| 9 | 3.89 (3.19) | 6.39 (2.50) | 6.67 (4.72) | - | - |
| 10 | - | - | - | 5.56 (4.31) | 1.94 (4.58) |
| fresh | 5.56 (3.19) | 1.53 (2.36) | 4.44 (3.75) | 3.61 (4.03) | 3.06 (2.92) |

Preregistered pooled rule over partitions A/2/3 (`dense_key_pool_pooled_analysis.csv`): pools 3 and 4 pass in 3/3 partitions (pooled 56.67%, 51.53%); pool 7 in 2/3 (24.58%); pools 5 and 6 in 1/2 and 1/3 (24.17%, 20.79%); pools 8 and 9 in 0/3 (9.49%, 5.65%); fresh pooled 3.84%. MLP-Hash: tested pools 1-4 pass, pool 5 fails on the interval criterion only (one lower bound 0.0; seed std 19.9 points), pool 10 fails. These failures neither establish equivalence to chance nor support conclusions about untested pool sizes.

### 5.3 Multiplicity amplification is gated by transform diversity

Amplification is 10-record minus 1-record top-1. Pool 3 gains are +37.5, +26.3, and +50.6 points for BioHash A/2/3, and +51.3 for MLP-Hash; pool 4 gains are +50.6, +41.0, +46.5, and +33.2. Large gains can occur when the single-record mean is near chance, but this is not universal: BioHash A pool 3 already gives 27.50% single-record top-1, and LFW pool 4 gives 16.83%. Descriptive gains do not establish paired statistical significance. Fresh-key means vary slightly in both directions; use the source-separated comparison table rather than claiming exact equality across exposures.

### 5.4 Session-aligned assignment inflates the curve

The first boundary run assigned keys by session index and gave 33.89% at pool 10; randomized assignment gave 5.56%. Session-aligned reuse is a plausible deployment pattern (one key per capture device or session) and is reported separately, not pooled.

### 5.5 Second dataset: LFW

Public funneled LFW, 125 identities x 12 images, 75/25/25 identity-disjoint split, chance 4.00% (`experiments/lfw_multiexposure/key_pool_boundary_summary.csv`). Fresh keys: 10-record top-1 exactly 4.00% with zero seed variance (1-record 4.67%), AUROC 0.505. Recurring pools 1/2/3/4/5/7/10: 73.17 / 63.17 / 62.50 / 42.50 / 41.00 / 32.00 / 25.33% (1-record 70.67 / 37.33 / 23.83 / 16.83 / 11.50 / 11.67 / 4.33%). Pools 1-7 pass; pool 10 fails only the interval criterion. The qualitative structure transfers; the boundary is later than on MOBIO (pool 10 still 25.3%), so its location is dataset-specific.

### 5.5b Third dataset: FEI

FEI face database, 200 identities x 12 of 14 images, uses a 120/40/40 identity-disjoint split and 2.50% chance (`experiments/fei_multiexposure/key_pool_boundary_summary.csv`). Extraction succeeded on 2,378/2,400 images; all failures were low-illumination pose 14, and every identity retains at least 11 records. Fresh-key ten-record top-1 is 1.77% (one-record 2.29%), AUROC 0.502. Recurring pools 1/2/3/4/5/7/10 give 76.88 / 63.44 / 54.79 / 47.50 / 37.50 / 23.65 / 3.96% (one-record 74.58 / 36.35 / 3.75 / 3.44 / 2.81 / 2.40 / 3.02%). The tested pools 1, 2, 3, 4, 5, and 7 pass both criteria; pool 10 fails. Pools 3, 4, 5, and 7 show small single-record means and much larger ten-record means. Pools 6, 8, and 9 were not tested, so no exact threshold can be inferred. FEI measures controlled pose/expression variation, not longitudinal session robustness. Full key-pool overview: `reports/figures/fig_results_overview.pdf`; source-separated table: `experiments/cross_dataset_key_pool_summary.csv`.

### 5.6 Mechanism controls

On a new paired MOBIO partition, hidden-slot DeepSets gave 10-record top-1 `55.28 / 46.25 / 32.92 / 23.75%` for pools 3/4/5/7 and `3.33%` for fresh keys. Supplying the true recurring-transform slot to the per-record encoder gave `57.08 / 50.69 / 33.61 / 22.92%`, differences of only `+1.81 / +4.44 / +0.69 / -0.83` points. Hidden-slot mixture identification is therefore not the main limitation in this range.

In a separate shuffled-non-anchor control, each 10-record set retained one target-identity record and received nine records from other identities while preserving record count and position-wise marginals. Pools 3/4 and fresh keys all produced exactly `3.33%` top-1 for every seed with AUROC `0.499/0.503/0.500`. Thus the recurring-pool gain requires multiple same-identity records and is not a set-size or global transform-frequency artefact. The negative pool-3 change from its `18.19%` one-record baseline reflects dilution of the sole informative record under mean pooling.

### 5.7 Same-image and correlated-key controls

Repeating the exact same normalized ArcFace embedding under ten distinct fresh, split-disjoint keys gave `3.33%` top-1 for all three seeds and AUROC `0.4997`, matching the different-image fresh-key baseline. The fresh-key null is therefore not an artefact of within-person session or image variation.

For a controlled correlation test, each BioHash projection shared an exact prefix of system-wide projection columns and used orthonormal private columns for the remainder. A coarse `0/25/50/75/100%` sweep gave 10-record top-1 `3.33/9.44/46.39/61.11/71.67%`. Because the 25% result was unstable, an independently preregistered fine sweep on a new partition tested `0/12.5/18.75/25/31.25/37.5/43.75/50%` and gave `3.33/3.75/6.94/7.64/14.17/35.83/49.31/42.64%`. All three seeds were strongly above chance from 37.5% onward; lower transition points were seed-sensitive. This supports correlation-dependent leakage but neither a sharp universal threshold nor strict empirical monotonicity.

## 6. Corrected Follow-up and Diagnostics

### Pilot extension, reported separately

After user-reported approval, paper-specified IoM-GRP (300 groups, q=16, one-hot input) and PolyProtect (window 5, overlap 2, raw 170-dimensional output) were implemented. The pre-run commit `d5f4e89` freezes the [pilot configuration](../configs/attacks/scheme_extension_pilot.yaml). Sixteen MOBIO/FEI cells produced 48 single/mean/DeepSets runs in 277.89 seconds on CPU. One seed, a 120-epoch cap and endpoints 1/10 distinguish these engineering diagnostics from the earlier studies; they are not a controlled scheme ranking.

At pool 4, paired mean-pool ten-minus-one gains are 37.92 and 33.75 percentage points for IoM-GRP on MOBIO/FEI, and 30.00 and 58.13 for PolyProtect. All four identity-bootstrap 95% intervals exclude zero, conditional on one seed and partition without multiplicity adjustment. Full values, negative gains and pool-8 outcomes remain in the [pilot report](../experiments/scheme_extension_pilot/README.md).

Fresh-key sensitivity does not establish equivalence: no endpoint's 90% interval lies strictly within +/-1 point of chance, and only one of 12 meets the illustrative +/-2-point band. These margins are not prospectively approved scientific bounds. Native fresh-key PolyProtect protected-gallery top-1 is 12.73%/13.73% on MOBIO/FEI, above 3.33%/2.50% chance; AUROC is 0.4971/0.5237. This separate matching task and probe definition must not be conflated with learned unprotected-gallery linkage. The follow-up below supplies null calibration without establishing a causal mechanism or a general privacy claim.

### Multi-seed and identity-partition follow-up

A separately hash-frozen [bounded protocol](../docs/protocols/scheme_followup_2026-09-18.md) tested MOBIO/FEI, IoM-GRP/PolyProtect, two new identity assignments and three model seeds under matched 120-epoch caps. Fresh/shared/pool-4 conditions produced 24 cells and 216 single/mean/DeepSets endpoints. All eight primary pool-4 mean-pool ten-minus-one gains were positive: 25.83-40.83 percentage points for IoM-GRP and 21.25-29.31 for PolyProtect. Crossed model-seed/identity bootstrap 95% intervals excluded zero; one-sided identity sign-flip tests on seed-averaged gains yielded Holm p = 0.004 across the eight-hypothesis family. Full endpoints, seed SD and intervals are in the [follow-up report](../experiments/scheme_followup_2026-09-18/README.md). Identity assignments overlap, and training key/set seeds are fixed; these are sensitivity checks, not independent population replications.

Three fresh-key seeds per dataset/partition produced twelve native PolyProtect controls. Identity-balanced top-1 was 10.91-14.55% on MOBIO and 10.11-11.64% on FEI, with Holm p = 0.006 against identity-preserving gallery-label permutation nulls. Positive radial scales 0.5/2 left IoM-GRP unchanged but changed PolyProtect templates. This synthetic scale sensitivity is not natural norm leakage or an explanation of native linkage. Fresh learned endpoints remained chance-compatible; no equivalence conclusion follows.

SCface separately extends earlier BioHash coverage to a fourth dataset: 130 identities, 2,851 usable embeddings and 26 test identities. Pools 1/2/3 pass the all-seed interval rule; pool 4 does not. Its IoM-GRP/PolyProtect results remain one-seed pilots, not part of the new bounded follow-up. See [SCface results](../experiments/scface_multiexposure/README.md) and [pilots](../experiments/scface_scheme_extension_pilot/README.md).

### Raw inputs, implementation checks and failures

The [raw-norm audit](../experiments/norm_native_audit_2026-09-18/README.md) re-extracted all 4,177 inputs in 254.157 seconds. Re-normalization matches saved vectors within 2.98e-8 maximum absolute error. Separate scalar PolyProtect and matrix/SciPy cosine calculations agree on predictions in all 48 cells, with no gallery overlap, ties or order dependence. Formula/windows/padding/parameter ranges match the paper, but its stricter score-conditioned selection is not implemented. This is computational checking, not official-code equivalence or independent human validation.

Three-key-averaged native unit top-1 is 12.20-12.42% on MOBIO and 11.09-11.12% on FEI; raw top-1 is 16.46-16.66% and 15.58-16.01%. All 16 endpoints pass gallery-label null tests (Holm p = 0.0032). Identity-bootstrap intervals condition on these three fixed keys. Raw-unit gains survive paired Holm family 8 only on FEI (p = 0.0160/0.0168; MOBIO 0.1380/0.1032). Raw-shuffled differences span -0.61 to +0.61 points; all intervals include zero, adjusted p >= 0.7584. Fixed training-median radius performs similarly to raw. This demonstrates scale sensitivity, not identity-specific norm leakage or equivalence; shuffling also disrupts quality associations. No source-norm oracle test survives its family of four, and it is not a protected-template attack. IoM changes zero of 38,400 sampled unit/raw codes, consistent with known scale invariance.

Unit-input linear-only native top-1 is 10.70-12.53%, and median nonlinear residual is 0.072-0.085 of template norm. Low-degree terms may contribute to residual matching; this diagnostic does not prove a complete mechanism. Original PolyProtect already reports naive-parameter residual linkage. Its stricter-policy evaluation is not overturned.

All 48 one-to-ten contrasts now have crossed seed/identity intervals, seed ranges, leave-one-seed-out sensitivity and two-sided Holm correction. The post-hoc family retains eight pool-4 mean gains (p = 0.0192; minimum leave-one-seed-out gain 17.71 points). No pool-4 DeepSets gain survives (minimum p = 0.0576). Four shared-key PolyProtect DeepSets gains are significantly negative, -15.42 to -24.86 points (p = 0.0192). Optimization/aggregation explanations remain untested. Original one-sided primary results (family eight, p = 0.004) are unchanged. Pointwise bootstrap intervals are not simultaneous and need not agree with corrected tests.

### Interpretation of earlier studies

- Deployment implication: independently sampled hidden per-record transforms remove source information under the idealized assumptions. Public salts are not secret keys and are not covered by that claim. Recurring application-wide or device-wide transforms can support multi-record linkage even when their values are hidden.
- Boundary location is protocol- and partition-specific and must be reported as a range: partition 3 collapsed at $k = 5$ while partitions A and 2 held to $k = 7$; pool 6 vs 7 non-monotonicity within partition A (seed std 18 points) shows that single-seed points near the boundary are unreliable.
- Why the collapse: as $k$ grows, the number of training records per transform falls as $1080/k$ and fewer same-transform relations recur within a set. The paired key-slot control changes top-1 by at most 4.44 points, so explicit mixture labels do not remove the boundary; loss of repeated cross-record structure is the stronger explanation under this attacker.
- Correlated transforms weaken the fresh-key symmetry continuously. They create single-record leakage at high shared fractions and additional multiplicity amplification, connecting the theorem's independent-key endpoint to the recurring-pool endpoint.

### Finalized September 19 extensions

The [extended study](../experiments/scheme_followup_2026-09-19_full/README.md) completed 32 cells, 672 trained endpoints and 224 seed-aggregated endpoints. Two datasets (MOBIO/SCface), two schemes, two overlapping identity assignments and four key conditions share 120-epoch caps and three training seeds. The seven model/exposure combinations are single at 1 and mean/DeepSets at 2/5/10. All 56 fresh-key model/exposure intervals contain chance; this is not equivalence. All eight planned pool-4 mean gains pass Holm correction. SCface gains are 16.19/34.29 points for IoM and 5.93/5.77 for PolyProtect. The SCface preparation code gives mugshots sample index 0; identity reassignment changes split labels, not this gallery ordering. Private metadata is unavailable on the report-building host for independent re-audit.

At ten records, PolyProtect pool-8 means exceed pool-4 means in all four dataset/assignment cells (SCface: 49.36/57.21% versus 10.26/10.10%). IoM decreases in all four. This is descriptive non-monotonicity across realized pools, not evidence that pool size itself causes the difference: only one pool realization per condition was tested. The new native control family includes SCface; all 12 MOBIO/SCface tests reject their gallery-label null with Holm p = 0.006. These controls remain distinct from learned linkage.

The [learned raw-input study](../experiments/raw_input_attacker_2026-09-19/README.md) adds 72 fits summarized in 24 rows, with one saved identity assignment, three training seeds, fresh/pool-4 conditions and exposures 1/10. Pool-4 mean top-1 is 3.61%/3.85% for PolyProtect and 91.11%/67.63% for IoM on MOBIO/SCface. These are descriptive seed means and SDs, not corrected null or equivalence tests. No matched unit-input arm uses these key/set seeds and assignments. Furthermore, the unchanged runner builds normalized means of raw source vectors as targets, so source norms reweight the targets as well as affect protection. IoM code-level scale invariance therefore does not imply identical learned performance. The raw study identifies a tested failure setting, not a causal explanation or a safer policy.

The [stricter-selection audit](../experiments/polyprotect_stricter_audit_2026-09-19/README.md) evaluates a local operationalization, not original-author code: 20 candidates, a 200-pair training-only development subsample, and the score band [-0.5, 0.5]. Native stricter-minus-naive changes are +3.13 points on MOBIO (95% interval [0.10, 6.16], Holm p = 0.1344) and -0.32 on SCface ([-2.19, 1.47], p = 0.7556). Neither establishes improvement; all four arms exceed their label-permutation null (family-4 Holm p = 0.0008). This neither validates nor refutes every stricter policy. There is no hyperparameter sweep or exact policy-reproduction claim.

## 7. Limitations

One encoder, four datasets with unequal coverage, and 25-40 gallery identities; only three model seeds, overlapping assignments and few pool draws. SCface now has three-seed/two-assignment new-scheme evidence, but not independent-pool replication. FEI lacks the extended exposure/pool-8 matrix. Training and targets share a hidden pool; unrelated-key transfer is untested. Implementations are paper-specified or explicitly local operationalizations, not source-exact. Raw learned results are descriptive and lack a matched unit arm. The source analyzer covers a bounded Python subset, uses project-authored fixtures and integration recipes, and has neither independently authored applications nor external labels. Its baseline is deliberately simple and does not establish superiority to specialist tools. Utility noninferiority is unstable across partitions: the latest confirmation passes 0/4 cells, while post-hoc diagnostics cannot repair those failures. Exact stricter-policy reproduction, other encoders, open-set galleries, approved utility margins, a powered new-identity cohort, unavailable historical paired scores and independent human review remain open. Bootstrap intervals may under-cover; chance inclusion and nonsignificance do not prove privacy. This revision supports finishing a bounded empirical manuscript for review, not claiming a complete universal matrix or guaranteed acceptance.

## 8. Reproducibility

The report-refresh [provenance audit](final_research_status.md#provenance-check) initially left three extended-study executed-source hashes unresolved; running the recovery utility directly against the experiment machine subsequently matched all 33/33 manifest entries, including these three, as unchanged, and the recovered archive was independently re-verified against the manifest. The files were never lost; the earlier automated search simply did not cover their exact (non-uniform) line-ending pattern. The aggregate tables and recorded manifest are retained unmodified.

All configurations, preregistrations, compact summaries, and hashes are in the repository. The V2 confirmation and V3 integration include source hashes, frozen protocols, per-case aggregate details and executable recipes. The utility confirmations export aggregate endpoints and decision bounds; identity-level arrays remain under ignored `results/` paths. The post-hoc diagnostic exports only non-identifying aggregates and records its source/input hashes. Restricted MOBIO data, embeddings, keys, and full metrics remain local. Commands are documented in each experiment README, including `experiments/source_real_integration_2026-09-25/README.md`, `experiments/scface_utility_confirmation_2026-09-25/README.md`, `experiments/utility_failure_diagnostics_2026-09-26/README.md`, `experiments/mobio_multiexposure/README.md`, `experiments/mobio_mechanism_controls/README.md`, and `experiments/mobio_correlation_controls/README.md`.

## 9. Result coverage

FEI and SCface extend historical BioHash coverage beyond MOBIO/LFW. The earlier table preserves 73 conditions from 12 studies; 72 pilot and 216 follow-up endpoints remain separate. The inventory retains 849 rows from 49 artifacts, including all previous 633. Its [coverage audit](../experiments/scheme_followup_2026-09-18/coverage_audit.csv) identifies legacy schemas and missing local SCface details. The 130 new audit rows are not trained endpoints and remain separate. The revised report distinguishes prior work, access assumptions, historical results, corrected tests, raw-norm controls and failures.
