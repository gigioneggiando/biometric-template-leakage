# Final research status

## External review ready; utility precision planning completed

Later on 2026-09-26 the user confirmed they can arrange reviewers but still have
no new authorized cohort. The [handoff](../experiments/independent_validation_2026-09-26/README.md)
freezes the corrected analyzer separately from an unchanged answer-masked 24-case
packet. The invitation requests independent declarations, labels and new cases
before source/results disclosure. No invitations were sent automatically; no
reviewer agreements, labels, new cases or signoffs have been received.

A [384-scenario planning analysis](../experiments/utility_precision_planning_2026-09-26/README.md)
uses published identity/key variability as proxies. Under its known-variance normal
approximation, 200 people/12 keys give only 33.9-49.0% TAR-gate probability using
SCface variability even assuming zero mean loss. More people alone leave key
uncertainty. This is not fitted hierarchical variance, calibrated bootstrap power
or joint power; local private per-person records of that later study were absent.
No scenario selects a replacement design or authorizes a run.

The required next steps are real reviewer submissions, approved joint power and
coverage planning, authorized new people and matched attack/verification testing.
All historical gates remain unchanged. The paper and nine-page pizza PDF now
distinguish these preparations from completed independent validation or utility
retention evidence.

## Branch correctness and provenance repair: 2026-09-26

A review reproduced a v2/v3 false-fresh result for protection calls inside distinct
branches: eight records shared four actual derived keys, but each path's sink was
marked fresh. The [repair](../experiments/source_branch_fix_2026-09-26/README.md)
adds a cross-path warning for branch-local sinks and rejects unsupported predicates
as complete evidence. The counterexample now returns unknown/incomplete. Existing
reuse findings may remain reuse/incomplete. This is a bounded conservative repair,
not independent proof of general Python soundness.

Separate post-fix regression records all 69 historical evaluations (overlapping
corpora) with unchanged predictions. Original manifests and result tables remain
unchanged; the exact executed v2 bytes are archived and hash-verified. Six Windows
provenance failures were LF/CRLF checkout differences. The shared verifier permits
only explicit newline conversions that reproduce recorded hashes, and explicit
exact-byte snapshots for modified historical sources. Content changes still fail.

The [pizza PDF](Pizza_Algorithm_Explained_2026-09-25.pdf) now has nine pages. At the
user's initial request, independent labels, external proof/novelty review and signoff
were deferred. The handoff above is now ready; submissions remain pending. No new biometric evaluation was run for
the fix. The 0/2 original joint, 2/4 first utility and 0/4 later utility results
remain separate and unchanged. New authorized people and approved power/margin
planning remain necessary for the proposed joint confirmation.

## Utility failure diagnosis: 2026-09-26

The [frozen MOBIO/SCface confirmation](../experiments/scface_utility_confirmation_2026-09-25/README.md)
completed 96 evaluations and passes every 2% FMR ceiling, but **0/4 cells pass**
the unchanged three-point TAR noninferiority criterion. The four lower bounds are
-3.16 to -5.36 points. SCface mean changes are nonnegative, so this is primarily
an uncertainty failure rather than consistent observed degradation; the two new
MOBIO failures also show partition sensitivity relative to the earlier passes.

The [post-hoc diagnostic](../experiments/utility_failure_diagnostics_2026-09-26/README.md)
exports only aggregate, non-identifying results. Identity-axis and key-axis
variation are material relative to the margin, while mean threshold shifts are
at most 0.26 points. SCface TAR is strongly distance-structured, from roughly
8-10% at distance 1 to 50-56% at distance 3. No frozen gate was changed. The
next defensible evaluation needs an application-approved utility margin, a new
authorized identity cohort, a prospective crossed identity/key power analysis
and predefined capture strata. More key seeds alone do not resolve population
uncertainty.

## New-participant joint protocol: preparation only

The [local cohort audit](../experiments/new_participant_joint_2026-09-25/README.md)
finds zero eligible unused IDs in the current FEI/MOBIO inputs: all 200 FEI and
150 MOBIO people were already present in the hash-frozen pilot metadata. The
raw FEI inventory also has only 200 participant IDs. Extra images or new split
seeds do not add independent people. The user confirmed no authorized new cohort
is currently available and requested protocol/PDF preparation only.

The [proposed fixed design](../docs/protocols/new_participant_joint_2026-09-25.md)
connects the actual source-analysis traces to a preselected four-key-pool versus
record-specific intervention, then tests both attack and matching on the same
new test participants. It proposes 500 eligible new people (200 train, 100 validation,
200 test), 12 paired key/model draws and one three-criterion joint gate. This is
a planning target, not a completed power calculation or independently approved
protocol. Access, overlap review, feasibility, power and margin approval remain
execution gates. **No new participants, new-cohort endpoints or joint pass exist.**
The [pizza report](Pizza_Algorithm_Explained_2026-09-25.pdf) now has nine pages,
including the data blocker and algorithm-to-experiment connection.

## Review preparation and utility replication: 2026-09-25

The [simple pizza PDF](Pizza_Algorithm_Explained_2026-09-25.pdf) explains the
algorithm and limitations, now extended to nine pages. A [24-case reviewer archive](../experiments/source_review_2026-09-25/README.md)
withholds our predictions and oracle labels, but no independent forms or new
externally authored cases have been received. The [internal review](../docs/review/source_proof_novelty_2026-09-25.md)
documents proof obligations and overlap with abstract interpretation, CogniCrypt,
CryptoGuard and Bandit. It is a targeted project-page review, not external proof
certification or an exhaustive novelty search.

The prospectively fixed [utility-only replication](../experiments/utility_replication_2026-09-25/README.md)
completed 96 evaluations in 12.36 seconds: twelve new key seeds and two new splits
on each of MOBIO and FEI. With unchanged margins and eight corrected one-sided
bootstrap bounds, MOBIO passes both utility gates (TAR lower changes -2.32/-2.02
points); FEI does not (-3.71/-3.61). All four FMR upper bounds remain below 2%.
Thus **2/4 utility gates pass**, without a new attacker evaluation or joint gate.
The original **0/2 joint gates** below remain unchanged. These are overlapping
partitions, conditional bootstrap intervals and a heuristic seed-count rationale,
not independent populations or a formal power calculation. External review was
still pending at execution; this is not post-review confirmation.

## Source-analysis and utility extension: 2026-09-25

Implemented bounded Python source inference for key provenance and explicitly assembled shared projection blocks, extending the earlier YAML checker. Added a conditional soundness argument, proposed component-weighted exposure reuse mass, an idealized unweighted collision envelope, and a utility-constrained acceptance criterion. These combine established methods; independent novelty/proof review is not completed.

The [new study](../experiments/source_security_utility_2026-09-25/README.md) has 24 same-author source cases and 18 new BioHash attacker/verification endpoints, completed in 75.64 seconds. Source analysis detects 13/17 observed-reuse cases and abstains on four, with seven finite-domain non-reuse cases; the runtime oracle is separate but human-independent labels remain pending. Bandit 1.8.6 supplies a generic-security baseline, not a specialist biometric analyzer.

Pool-4 to fresh learned linkage falls **27.08% to 3.47% on MOBIO** and **27.92% to 2.50% on FEI**. Trusted-key verification TAR averages 95.45% to 96.87% and 95.71% to 95.67%, respectively. However, simultaneous-bootstrap TAR difference lower bounds are **-3.94/-5.68 points**, below the prospectively fixed -3-point margin: **0/2 primary joint gates pass**. Leakage-reduction and FMR criteria pass; utility noninferiority does not. Do not claim demonstrated retention from point estimates alone. The architecture requires raw-probe access and keys outside the attacker database; it is not a drop-in defense or protection against key-service compromise.

[Four-page PDF](Source_Security_Utility_2026-09-25.pdf), [formal assumptions/derivations](../docs/theory/source_scope_and_utility.md), and the revised manuscript document the proposal and failures. A post-execution name-binding defect was fixed; exact executed analyzer bytes are archived and hash-verified, and all benchmark predictions rechecked unchanged. Historical studies remain intact.

## Static-analysis update: 2026-09-25

Implemented **KSSA v1**, a static checker for the repository's YAML protection policies: key reuse, shared projections, slot disclosure, unsupported declarations and unresolved scheme/runtime assumptions. It proposes a separate fresh-key configuration; it does not certify security or analyze arbitrary Python source. Sani suggested exploring an algorithmic contribution, and Manish proposed this static-analysis direction. Sani has not yet reviewed this specific implementation or its conclusions; independent novelty review remains open.

The [new matched rerun](../experiments/static_policy_2026-09-25/README.md) completed **16 cells / 96 trained endpoints in 352.766 seconds**, on MOBIO/FEI, IoM-GRP/PolyProtect, two identity assignments and three model seeds. All eight primary ten-record pool-4-minus-fresh reductions are positive (72.08-94.48 points), with positive paired intervals and Holm p = 0.004. Fresh learned intervals include chance, not equivalence. Fresh PolyProtect native top-1 remains descriptively 7.80-13.33%; its warning remains. Authentication utility, broader analyzer accuracy, independent-pool robustness and production secrecy are unverified. SCface was not rerun because embeddings are absent locally.

The later [source-analysis v3 integration](../experiments/source_real_integration_2026-09-25/README.md)
adds explicit BioHash, IoM-GRP and PolyProtect call contracts. It produces 25/25
correct emitted decisions, one abstention, 96.15% coverage and zero false-fresh
results across six executable local recipes plus the frozen 20-case regression
corpus. This is internally authored bounded evidence, not external validation or
a general Python soundness result. The separate security/utility gate is unchanged.

The later [MOBIO/SCface utility confirmation](../experiments/scface_utility_confirmation_2026-09-25/README.md)
ran 96 prospective evaluations on two new split assignments and twelve new paired
keys. All candidate FMR upper bounds remain below 2%, but all four TAR lower bounds
cross the fixed -3-point margin (-3.16 to -5.36 points). The SCface mean TAR changes
are nonnegative, yet too imprecise; both new MOBIO cells also fail. Stable utility
noninferiority and any joint security/utility claim therefore remain unestablished.

The [three-page static-analysis PDF](Static_Policy_Analysis_2026-09-25.pdf), [revised manuscript](paper_draft.md), [prospective protocol](../docs/protocols/static_policy_2026-09-25.md), and hash-frozen aggregate results are the new package. The previous 19-page September report, 15-slide deck, 22 figures and historical experiment families are preserved rather than silently re-labeled.

## Findings update: 2026-09-19

**Presentation assessment after finalized experiments:** evidence is stronger for a bounded empirical manuscript, not uniformly larger attack scores or a completed submission. The current package is **19 report pages, 15 slides and 22 figures**, with a [simple explanation of every page](Sept_Dataset_Update_README.md). SCface now has the extended multi-seed study. Raw learned and local stricter-policy studies are complete, but neither establishes a universal protection conclusion. No new training was run for this report refresh; private SCface records were not independently re-audited on this host. Coauthor review, final references/venue preparation and the stated scientific limits remain.

**Learned raw-input attacker completed:** [MOBIO/SCface, PolyProtect/IoM-GRP, fresh/pool-4](../experiments/raw_input_attacker_2026-09-19/README.md), 775.48 seconds. Raw PolyProtect pool-4 mean accuracy is 3.61%/3.85%, versus IoM 91.11%/67.63%. Fresh means are near chance. These descriptive three-seed results have no corrected null/equivalence test. Unit/raw studies change key/set seeds, identity assignments and the weighting of target vectors, so neither an unchanged learned IoM effect nor a causal normalization explanation is established. Raw input is not demonstrated to be safer.

**Extended follow-up completed:** [32 cells, 672 endpoints](../experiments/scheme_followup_2026-09-19_full/README.md), MOBIO and SCface, exposures 1/2/5/10, conditions fresh/pool-1/pool-4/pool-8, 1,008.66 seconds. The fresh-key null now holds at every tested exposure count, not only 1 and 10. Pool-4 amplification replicates on SCface with full statistical rigor (8/8 primary contrasts positive, Holm-significant). Pool-8 does not behave like a simple extension of pool-4: IoM-GRP decreases as expected, but PolyProtect leaks *more* at pool-8 than pool-4 in all four tested cells, up to roughly 5x on SCface, consistent with the pool-sensitivity already seen in the independent-pool study below. SWG-MinHash was reviewed and not implemented as a third scheme (no citable paper for the method itself); AgeDB was reviewed and not pursued (the two-additional-dataset requirement is already met by FEI/SCface). Both decisions are recorded in `docs/TODO.md`, not silently dropped.

**Independent-pool revision completed:** [24 cells, 144 fits and 72 prediction-mean evaluations](../experiments/pool_replication_2026-09-19/README.md), three pools x three model seeds x two partitions, 254.188 seconds. IoM gains persist in all 12 dataset/split/pool combinations; PolyProtect has three reversals and gains from -3.23 to +72.40 points. All eight direct input-mean versus prediction-mean intervals include zero: neither superiority nor equivalence. Pool seeds change transforms and slot assignment jointly; only three draws and pointwise intervals limit inference. The historical fixed-pool corrected family remains unchanged.

The [full author-thesis maximal-linkability chapter comparison](../docs/literature/closest_work_2026-09-18.md) is complete; publisher-PDF version verification remains blocked. SCface's former pilot-only status is superseded by the extended study, but it still lacks the independent-pool baseline matrix. Same-pool paired access, output-visible queries, known grouping and a small closed gallery remain strong explicit assumptions. No exhaustive novelty, deployment prevalence or independent human review is claimed.

**Subsequent revision completed:** [raw-norm/native audit](../experiments/norm_native_audit_2026-09-18/README.md), 254.157 seconds, 4,177 genuine raw extractions, 48 separate formula/matcher checks, 130 aggregate rows. No matching disagreements were found. Native raw matching rises descriptively, but only FEI raw-unit paired gains survive correction; raw-shuffled comparisons do not establish identity-specific norm leakage. All 48 follow-up contrasts now include corrected inference and seed sensitivity: eight pool-4 mean gains and four shared-key DeepSets losses survive the post-hoc family. The [closest-work review](../docs/literature/closest_work_2026-09-18.md) narrows novelty and explicitly requires training access to the same realized hidden pool. The manuscript has three supported claims, not a universal privacy conclusion.

**Recurring hidden transforms permit substantial multi-record linkage in the tested protocols; fresh-key learned endpoints remain chance-compatible.** The completed bounded follow-up adds model-seed and identity-partition sensitivity, not a universal privacy result or a complete cross-dataset confirmation matrix.

Completed: FEI adds a third multi-exposure dataset to MOBIO/LFW, with 200 identities, 2,378 usable embeddings, and three model seeds. Its ten-record fresh-key top-1 is 1.77% versus 2.50% chance; tested recurring pools 1/2/3/4/5/7 pass, while pool 10 fails. No additional training was needed for this presentation audit because the completed run and compact summary already exist.

On 2026-09-18 Sani supplied the authorized SCface archive directly (see [local data setup](../docs/setup/SCFACE_LOCAL_DATA.md)). SCface adds a fourth multi-exposure dataset: a mugshot gallery matched against visible surveillance probes from seven cameras at three distances, 130 identities, 2,851 usable embeddings, and three model seeds. Unprotected mugshot-to-surveillance matching reaches 84.375% top-1 against a 544-probe test set. Its ten-record fresh-key top-1 is 3.85% versus 3.846% chance; tested recurring pools 1/2/3 pass the all-seed clustered-interval criterion, while pools 4/5/7/10 do not. [Results and caveats](../experiments/scface_multiexposure/README.md).

The user subsequently reported Sani's approval of paper-specified IoM-GRP and PolyProtect and authorized pilots for up to one hour. Both were implemented and frozen at `d5f4e89` for MOBIO/FEI (16 cells, 48 model runs, 277.89 seconds on CPU) and at `69a93e4` for SCface (8 cells, 24 model runs, 128.22 seconds on CPU). At pool 4, mean-pool ten-minus-one gains are 37.92/33.75/34.62 points for IoM-GRP on MOBIO/FEI/SCface and 30.00/58.13/41.83 for PolyProtect, with positive paired 95% intervals conditional on one seed. These are pilots, not confirmation. [MOBIO/FEI results and caveats](../experiments/scheme_extension_pilot/README.md); [SCface results and caveats](../experiments/scface_scheme_extension_pilot/README.md).

Fresh-key uncertainty remains broad: no endpoint meets the illustrative +/-1-point equivalence band. Native fresh-key PolyProtect protected-gallery top-1 reaches 12.73%/13.73%/10.66% against 3.33%/2.50%/3.846% chance on MOBIO/FEI/SCface. This is distinct from learned unprotected-gallery linkage and prevents a general privacy claim. PolyProtect is outside the rotational-invariance theorem.

The subsequent authorized [MOBIO/FEI follow-up](../experiments/scheme_followup_2026-09-18/README.md) completed 24 cells / 216 endpoints in 859.63 seconds. IoM-GRP and PolyProtect were tested on two new identity partitions with three model seeds, fresh/shared/pool-4 conditions and matched 120-epoch caps. All eight primary pool-4 mean-pool amplification contrasts have positive crossed-bootstrap 95% intervals and Holm p = 0.004. All 12 fresh PolyProtect native matching tests exceed their gallery-label permutation null (Holm p = 0.006). IoM-GRP is unchanged by positive radial scaling; PolyProtect changes, but this synthetic sensitivity is not natural norm leakage or a causal explanation of native linkage. Fresh learned intervals include chance; no equivalence claim follows.

The package contains 22 figures, a 15-slide editable deck/PDF and a [19-page September report](Sept_Dataset_Update.pdf), with a [simple README](Sept_Dataset_Update_README.md) and [detailed guide](Sept_Dataset_Update_guide.md). Latest results are recorded through `4831d99`; exact executed hashes are retained. Earlier studies, the 672 extended endpoints, 24 raw summaries and stricter native audit remain separate. The historical inventory retains 849 rows / 49 artifacts and is not a complete inventory of the new studies. Native PowerPoint rendering remains a presenting-machine check.

| Remaining gate | Current status / next action |
|---|---|
| Second additional dataset beyond MOBIO/LFW | FEI and SCface are both complete as added-dataset BioHash key-pool studies. SCface now also has full multi-seed/multi-partition IoM-GRP/PolyProtect coverage, matching MOBIO. AgeDB was reviewed and deliberately not pursued (2026-09-19); the requirement is met without it. |
| Two additional protection families | Paper-specified implementations complete; three-seed/two-partition MOBIO/SCface follow-up now covers exposures 1/2/5/10 and pools 1/4/8. FEI coverage at this rigor and a third scheme (SWG-MinHash, reviewed and declined for lacking a citable source paper) remain open. |
| Confirmatory matrix | MOBIO/SCface now cover fresh/pool-1/pool-4/pool-8 at exposures 1/2/5/10 with 3 seeds/2 partitions. FEI is not covered at this rigor (no local embeddings on this host); only one pool-8 draw was tested per cell, not multiple independent draws; attacker architectures beyond mean-pool/DeepSets/single-MLP remain untested. |
| Statistical inference | Follow-up crossed seed/identity intervals and prespecified Holm families complete. Approved equivalence margins, older-study inference and full historical coverage remain open. |
| Theory and implementation | Separate formulas/matcher and genuine raw-norm controls complete. A stricter PolyProtect parameter-selection function was implemented, unit-tested, and evaluated against real MOBIO/SCface native matching: it did not reduce leakage (directionally worse on MOBIO, no effect on SCface; neither significant after correction). A learned raw-input attacker was also completed: fresh-key null holds under raw input; PolyProtect pool-4 amplification, large under unit input, is essentially absent under raw input (IoM-GRP is unaffected, as expected). A hyperparameter sweep on the stricter selection, FEI coverage, a mechanistic explanation for the raw-input PolyProtect finding, and independent human review remain open. |
| Novelty and venue fit | Versioned closest-work comparison and deployment assumptions documented; exhaustive priority and independent human review are not claimed. |
| Professor review | Review the revised manuscript and 12-slide package; record decisions before expanding experiments. |

See [figures/README.md](figures/README.md), [slides/research_review.pdf](slides/research_review.pdf), and [../docs/ROADMAP.md](../docs/ROADMAP.md). No biometric images, templates, keys, or model weights are included in the presentation package.

## Provenance check

**Resolved 2026-09-20.** The report refresh checked 44 source-hash entries across the three newly finalized manifests: 30 matched checkout bytes, 10 matched after CRLF-to-LF normalization, and one stricter-audit dependency matched the CRLF form of its historical `9506849c` snapshot. Three extended-study hashes ([multiexposure.py](../src/biometrics_ai/data/multiexposure.py), [protection/\_\_init\_\_.py](../src/biometrics_ai/protection/__init__.py), [biohash.py](../src/biometrics_ai/protection/biohash.py)) did not match the checkout, its history, or either uniform line-ending transform at first. Running the [recovery utility](../scripts/diagnostics/recover_executed_sources.py) directly against the experiment machine (`E:\Research\Biometrics`) found all **33/33** manifest entries present unchanged, including these three: they were never lost, edited, or overwritten. The earlier automated search missed them only because it tried uniform or single-boundary mixed line endings, while the executed files have a non-uniform newline mix from edits across multiple tools; normalizing either version to plain LF shows the underlying content was identical to the current checkout all along. The recovered archive was independently re-hashed against the manifest (33/33 match) separately from the utility's own check. See the [experiment README](../experiments/scheme_followup_2026-09-19_full/README.md#source-recovery-resolved-2026-09-20) for the full account. No source, protocol, result CSV, or manifest was changed to resolve this; the finalized aggregates and passing tests were never in question, only this provenance trace.

## Research question

Can a key-agnostic learned set model recover identity-discriminative information from multiple independently protected face templates?

## Literature and threat model

See `docs/literature/` and `docs/literature/threat_models.md`. The main future evaluation is unseen identities plus unseen keys; K0 knows only the scheme family and K1 additionally knows hyperparameters.

## Completed infrastructure

- Deterministic BioHash reference, key scope splitting, identity-disjoint real-data protocols, single MLP/DeepSets models, gallery/probe metrics, leakage checks, tests, configs, and per-run artifacts.
- Reusable OpenCV SCRFD/ArcFace and YuNet/ArcFace extraction backends; official `buffalo_l` and YuNet hash verification; deterministic LFW, Olivetti, and CFP protocol construction; and a three-seed Month 1 runner.
- Official GaFaR/InsightFace/Arc2Face commits recorded. The `benchmark_cb` source remains unresolved after a 2026-08-26 recheck.

## Results

No published experiment has been reproduced. The paper's face targets were verified directly from arXiv source, and authorized MOBIO face data is now prepared locally, but the official `benchmark_cb` implementation remains unavailable.

Real-image **engineering validation** was completed on LFW, Olivetti faces, and CFP. Six protocol variants cover SCRFD/YuNet preprocessing, 60/150-identity LFW subsets, and CFP frontal/profile views. Unprotected ArcFace top-1 ranged from `94.92%` to `100.00%`, showing that the source embeddings preserve identity.

Under independent unseen keys, the three-seed MLP remained at the applicable random top-1 rate on every protocol. Headline results were `3.83% +/- 0.93%` versus `3.33%` chance on the 1,500-image larger LFW protocol and `1.15% +/- 0.17%` versus `1.00%` chance on 4,999 CFP frontal embeddings. AUROC remained near `0.5`, EER near `50%`, and no per-seed descriptive exact binomial test rejected chance (`p >= 0.1205`). CFP profile and matched LFW YuNet runs showed that pose and detector choice did not change the conclusion.

The fixed-transform positive control reached `51.11%` to `91.00%` top-1. A 64/128/256-bit sweep on LFW and Olivetti also remained compatible with chance under independent keys.

The first MOBIO engineering run adds all 150 identities with one selected image from each of 12 sessions. YuNet plus ArcFace extracted 1,799/1,800 embeddings. On the 30-identity test split, unprotected ArcFace reached `100%` top-1. The shared-key learned attack reached `81.21% +/- 3.19%` top-1, while independent unseen keys reached `3.33% +/- 0.30%` against `3.33%` chance, with AUROC `0.4992` and EER `50.28%`. This is strong confirmation of the single-template null pattern on MOBIO, not an exact reproduction or proof of irreversibility.

A crossed `3 identity assignments x 3 key seeds x 3 model seeds` sensitivity study strengthened the larger LFW and CFP frontal results. Independent-key split/key cell means ranged `2.59-3.58%` versus `3.33%` chance on LFW and `0.81-1.11%` versus `1.00%` chance on CFP. All 54 run-level identity-clustered 95% intervals included chance. Fixed-transform cell means remained `66.54-77.41%` on LFW and `91.70-94.74%` on CFP. The convergent control/null pattern is the main Month 1 finding: no useful identity recovery from one independently keyed template was detected across the tested real-data protocols.

The preregistered exploratory MOBIO multi-exposure run tested 1/2/5/10 records with mean pooling, max pooling, and DeepSets. Independent unseen-key top-1 stayed between `2.64%` and `4.17%` against `3.33%` chance; all three 10-exposure models were exactly at chance, AUROC remained near `0.5`, and every run-level identity-clustered interval included chance. DeepSets changed by `-0.83` percentage points from 1 to 10 exposures, so the preregistered amplification criterion failed. The unprotected 10-exposure oracle reached `100%`, while shared-key mean pooling reached `87.36%` at five exposures, supporting pipeline sensitivity.

A preregistered cross-scheme run repeated the experiment with paper-specified MLP-Hash and new key/set/model seeds. Independent-key top-1 remained at chance for every exposure level and architecture: one-record top-1 was `2.50% +/- 1.10%`, while 10-record DeepSets was `3.33%`, AUROC `0.4998`, and EER `49.81%`. The unprotected oracle remained `100%`; shared-key mean pooling reached `80.83%` at five records. The second amplification criterion also failed.

## Multiplicity-invariance proposition

Let every source embedding have fixed norm and let each protected record begin with an independently sampled hidden Haar-distributed orthogonal or semi-orthogonal projection. For any two source vectors of equal norm, rotational invariance makes the projected-vector distributions identical. Any subsequent measurable transformation, including sign thresholding or independently randomized nonlinear layers, preserves that equality in distribution. With independent fresh keys, the joint distribution of any finite number of protected records is therefore independent of the source identity: $I(Y; T_1,\ldots,T_n)=0$. Under a uniform closed-set prior, Bayes-optimal top-1 identification is exactly chance for every $n$.

The cross-scheme null results are consistent with this idealized proposition, but do not validate all its assumptions in the finite implementation. It is not a universal irreversibility theorem. It does not cover non-normalized embeddings, biased or correlated projections, finite-key defects, key-correlated side information, key leakage, key reuse, implementation side channels, or transformations lacking rotational invariance. Those cases define boundaries for further testing.

The first boundary experiment found a large key-reuse effect, but used session-aligned pool assignment. At 10 records, mean-pool top-1 decreased from `66.39%` with one recurring transform to `61.11%`, `47.64%`, and `33.89%` with pools of 2/5/10, then collapsed to `2.92%` with fresh keys. A preregistered sample-randomized confirmation retained `77.50%`, `69.44%`, and `46.94%` for pools 1/2/5 but pool 10 fell to `5.56%`, equal to its fresh endpoint. Thus the all-pools confirmation criterion failed. The surviving positive result is a severe small-pool reuse regime and a protocol-specific threshold between 5 and 10 transforms.

Three further preregistered runs extended the evidence. On a new identity partition, pools 1/2/5 gave `81.67%/73.89%/51.11%` and pool 10 `5.56%`. A dense BioHash sweep gave `65.00%/54.03%/17.36%/34.44%/10.42%/3.89%` for pools 3/4/6/7/8/9, with visible seed sensitivity and non-monotonicity. Paper-specified MLP-Hash gave `71.39%/68.89%/22.92%/1.94%` for pools 1/2/5/10. Large multi-record gains occur in the tested reuse regimes, sometimes from near-chance single-record means, but not universally: BioHash dense A pool 3 already has `27.50%` single-record linkage. Fresh-key means vary slightly across exposures; they do not coincide exactly in every run.

Across three MOBIO dense studies, pools 3/4 pass the interval criterion in all three partitions (pooled `56.7% / 51.5%`), pools 5-7 are partition-dependent, and tested pools 8/9 fail that criterion in all three. Failure is not equivalence to chance. Haar sign-corrected BioHash gave `74.6 / 48.1 / 2.6%` for pools 1/5/fresh; the ideal sampling argument still needs separate treatment of finite keys and numerical precision. MLP-Hash pools 3/4 gave `54.3 / 37.8%`. LFW fresh keys gave `4.0%` against `4.0%` chance; pool 10 gave `25.3%` but failed the strict interval rule. FEI fresh keys gave `1.8%` against `2.5%` chance; tested pools 1/2/3/4/5/7/10 gave `76.9 / 63.4 / 54.8 / 47.5 / 37.5 / 23.6 / 4.0%`. Pool 10 fails; untested pools 6/8/9 cannot locate a precise threshold. The source-separated study table is `experiments/cross_dataset_key_pool_summary.csv`.

Two preregistered mechanism controls strengthen the interpretation. On a new paired MOBIO partition, hidden-slot DeepSets gave `55.3/46.3/32.9/23.8%` for pools 3/4/5/7 and `3.33%` fresh; providing the correct transform-slot label changed these by only `+1.8/+4.4/+0.7/-0.8` points. In the shuffled-non-anchor control, retaining one correct record but replacing the other nine with other identities collapsed pools 3/4 and fresh keys to exactly `3.33%` for every seed. The gain therefore requires multiple same-identity records and is not primarily a set-size, transform-frequency, or hidden-slot-identification artefact.

The same-image control removed the remaining image/session-variation explanation: protecting one identical normalized embedding under ten distinct fresh keys still gave exactly `3.33%` top-1 for every seed (AUROC `0.4997`). Controlled correlated-key sweeps then shared an exact prefix of each 128-dimensional BioHash projection. On an independent fine-sweep partition, ten-record top-1 was `3.33/3.75/6.94/7.64/14.17/35.83/49.31/42.64%` as the shared fraction increased through `0/12.5/18.75/25/31.25/37.5/43.75/50%`. Leakage was consistently large from 37.5% onward, while the lower transition region was seed-sensitive. This establishes a graded correlation-dependent regime for the tested construction, not a universal threshold.

## Limitations and next work

These studies use one ArcFace checkpoint and a local BioHash reference not cross-checked against unavailable official code. The primary cross-dataset table uses one identity assignment, while larger LFW and CFP add three identity assignments, three key seeds, and three model seeds. The new MOBIO/FEI follow-up uses two overlapping assignments and three model seeds with fixed training key/set seeds. These cells share datasets and pipeline components, so they are sensitivity checks rather than independent populations. Older identity-clustered intervals were inspected without familywise correction; the follow-up corrects only its prespecified primary and native families. Bootstrap intervals can under-cover, and chance inclusion does not prove equivalence or irreversibility. None of the protocols is an exact reproduction of the paper's MOBIO protocol or official implementation.

Continue requesting a corrected `benchmark_cb` source; keep its exact reproduction blocked until then. Strengthen transform-source validation, independent proof and literature review, statistical equivalence analysis, and uncertainty around the correlation transition. These are concrete evidence improvements, not a guarantee of any venue rank or acceptance. The dated readiness audit above separates approval/access gates from executable follow-up work.

## Commands

Month 1 targets are listed in the `Makefile`; equivalent Python commands are documented in `docs/protocols/real_datasets_month1.md`. They require local authorized datasets and hash-verified model assets. Exact benchmark commands remain withheld until the official upstream protocol is recovered.
