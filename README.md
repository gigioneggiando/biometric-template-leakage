# Key-agnostic multi-exposure biometric template leakage

**Last status update:** 2026-09-25. New-participant audit and algorithm-linked joint protocol prepared; no new-cohort experiment run. Historical results remain separate.

**Navigation:** [Research package index](reports/README.md), [current evidence and gates](reports/final_research_status.md), [figure captions](reports/figures/README.md), and [review slides](reports/slides/research_review.pdf).

## Simple explanation and next research gates

Open the [eight-page pizza explanation PDF](reports/Pizza_Algorithm_Explained_2026-09-25.pdf).
It explains the algorithm, shared components, trusted matching and results with
simple wording, original pizza drawings and no typographic dashes.

Pages 7 and 8 add the [participant audit and next-study handoff](experiments/new_participant_joint_2026-09-25/README.md).
All 200 local FEI and 150 MOBIO participants were previously used. No genuinely
new participants have been added. The [proposed joint protocol](docs/protocols/new_participant_joint_2026-09-25.md)
links analyzer findings to attacks and matching on the same new test cohort.
Its 500-person planning target requires authorized data, feasibility/power review
and approval before execution; it is not a new result or established sample size.

The [fixed utility replication](experiments/utility_replication_2026-09-25/README.md)
completed 96 evaluations: both MOBIO splits pass, both FEI splits remain
inconclusive under the unchanged three-point tolerance. This is utility-only,
not a new joint security pass. The earlier failed joint gates remain unchanged.
The [answer-free reviewer packet](experiments/source_review_2026-09-25/README.md)
and [internal proof/prior-work review](docs/review/source_proof_novelty_2026-09-25.md)
are ready; independent labels, external signoff and novelty review are still pending.

## Source-level extension and matching utility

The [source interpreter](src/biometrics_ai/protection/source_analysis.py) now infers
key reuse and explicitly shared projection components from a bounded Python subset.
The [new study](experiments/source_security_utility_2026-09-25/README.md) adds proposed
mathematical criteria, 24 source cases with YAML/Bandit baselines, and 18 new
MOBIO/FEI attacker and trusted-key verification endpoints. Open the
[four-page PDF](reports/Source_Security_Utility_2026-09-25.pdf) and
[formal model](docs/theory/source_scope_and_utility.md).

**Result:** learned linkage decreases and average matching TAR remains near
95-97%, but **both fixed utility-noninferiority gates fail**. Independent benchmark
labels and research novelty remain unverified. This is a bounded research
prototype, not a general source analyzer or a deployment security certificate.

The [frozen 24-case holdout](experiments/source_holdout_2026-09-25/README.md)
produced 16/16 correct decisions with no false-fresh result, but abstained on eight
realistic unsupported cases. Its 66.67% coverage misses the fixed 75% gate, defining
the concrete language-coverage work for a separate v2.

[Source-analysis v2](experiments/source_holdout_v2_2026-09-25/README.md) resolves
22/23 valid development cases with 100% selective accuracy, 95.65% coverage and no
false-fresh decisions. This passes the development gates; unseen confirmation and
the separate biometric security/utility gate remain open.

The [frozen v2 confirmation](experiments/source_holdout_v2_confirmation_2026-09-25/README.md)
adds 20 new valid programs: 19/19 emitted decisions are correct, coverage is 95%,
no reuse case is predicted fresh and all fixed gates pass. It is an internally
authored post-implementation holdout, not external validation.

[V3 integration](experiments/source_real_integration_2026-09-25/README.md) adds
explicit BioHash, IoM-GRP and PolyProtect sink contracts. Across six executable
scheme recipes and the 20-case frozen regression corpus, v3 emits 25/25 correct
decisions with 96.15% coverage and zero false-fresh results. A transparent local
AST baseline reaches 23.08% coverage and 5/6 correct decisions; it is not a
state-of-the-art comparator.

## Static analysis and security evaluation

[KSSA v1](src/biometrics_ai/protection/policy.py) statically audits the YAML key policy
for reuse, correlated projections and slot disclosure, rejects unsupported
declarations, and preserves scheme/runtime review warnings. It proposes fresh
keys without overwriting the source policy. It is configuration-level analysis,
not a general source-code analyzer or proof of security.

The [new MOBIO/FEI experiment](experiments/static_policy_2026-09-25/README.md)
completed 96 trained endpoints in 352.766 seconds. All eight planned ten-record
pool-4-minus-fresh reductions are positive: 72.08-94.48 percentage points,
Holm p = 0.004 each. Native PolyProtect linkage remains; authentication utility
and broad analyzer detection accuracy are unverified. Open the
[three-page PDF](reports/Static_Policy_Analysis_2026-09-25.pdf) or
[updated manuscript](reports/paper_draft.md).

```powershell
.\.venv\Scripts\python.exe -m biometrics_ai.protection.policy --config configs/attacks/static_policy_2026-09-25.yaml
```

Add `--enforce` to fail the gate: exit 2 for blocking findings, 3 for unresolved
review. Even fresh policies require review. Sani suggested exploring an algorithmic
contribution; Manish proposed this static-analysis direction. Sani has not yet
reviewed this specific implementation or its conclusions.
See the [internal algorithm review](docs/review/algorithm_review_2026-09-25.md)
for the evidence limits and prioritized v2 validation plan.

## What we have now

| Completed work | Available evidence |
|---|---|
| Four multi-exposure datasets: MOBIO, LFW, FEI, SCface | [73 key-pool conditions from 12 source-separated studies](experiments/cross_dataset_key_pool_summary.csv) |
| IoM-GRP and PolyProtect historical pilots | 24 cells / 72 endpoints across MOBIO/FEI/SCface; one model seed per endpoint |
| New MOBIO/FEI scheme follow-up | [24 cells / 216 endpoints](experiments/scheme_followup_2026-09-18/README.md), two identity assignments and three model seeds; 859.63 seconds total |
| Follow-up statistical controls | Eight positive pool-4 amplification contrasts (Holm p = 0.004); twelve native permutation tests (Holm p = 0.006); separate synthetic radial sensitivity |
| Local run inventory | [849 rows from 49 artifacts](experiments/multiexposure_run_matrix.csv), with [legacy/missing-detail coverage audit](experiments/scheme_followup_2026-09-18/coverage_audit.csv) |
| Raw-norm and native audit | [4,177 verified raw extractions, 48 implementation cells, 130 aggregate rows](experiments/norm_native_audit_2026-09-18/README.md); completed in 254.157 seconds |
| Independent recurring pools and simple baseline | [24 cells / 144 fits / 72 prediction-mean evaluations](experiments/pool_replication_2026-09-19/README.md); three new pools, three model seeds, two partitions; 254.188 seconds |
| Extended MOBIO/SCface study | [32 cells / 672 endpoints](experiments/scheme_followup_2026-09-19_full/README.md); 1/2/5/10 records; fresh/pool-1/4/8; all eight primary gains pass correction |
| Learned raw input and stricter selection | [Raw-input study](experiments/raw_input_attacker_2026-09-19/README.md) and [local stricter-selection audit](experiments/polyprotect_stricter_audit_2026-09-19/README.md); negative findings, not universal scheme conclusions |
| Scientific presentation | 19-page report, 15-slide PDF/editable deck, 22 figures and a [simple page-by-page README](reports/Sept_Dataset_Update_README.md) |

**New result:** SCface now has multi-seed/two-partition new-scheme evidence: pool-4 gains of 16.19/34.29 points for IoM and 5.93/5.77 for PolyProtect. Pool-8 PolyProtect scores are higher in this draw, not evidence of a universal pool-size effect. Raw learned PolyProtect stays near chance in a separate descriptive study; changed seeds, partitions and targets prevent a causal unit/raw comparison. The local stricter policy shows no corrected reduction in native linkage. Earlier independent-pool evidence remains: IoM gains persist, PolyProtect varies strongly, and no input-pooling superiority is established. Publisher-version verification and independent human review remain open.

The original trained follow-up is hash-frozen against `4352eeb`; the native raw audit against `15e4384`, with executed source hashes recording additions. Historical studies are not pooled. Raw-vs-shuffled controls do not establish identity-specific norm leakage. All 48 original follow-up contrasts retain their corrected analysis. SCface extension and learned raw retraining are now complete; full cross-dataset coverage, matched raw/unit causal analysis, equivalence and independent review remain open. Chance compatibility is not privacy.

The [closest-work comparison](docs/literature/closest_work_2026-09-18.md) identifies the contribution as controlled **hidden-pool reuse and set aggregation**, not multiplicity or identity distillation themselves. Training requires paired access to the same realized pool used by targets; this is a strong explicit assumption.

## Open results, images and diagrams

No environment setup or experiment rerun is needed to view the existing outputs. Open PNG images directly, PDFs in a PDF viewer/browser, and the editable deck in PowerPoint. In VS Code, open this README's Markdown preview for clickable navigation.

| What to view | Location |
|---|---|
| September dataset update: findings, architecture overview and detailed attacker | [reports/Sept_Dataset_Update.pdf](reports/Sept_Dataset_Update.pdf) |
| All 22 figures together, including architecture and results | [reports/slides/figure_appendix.pdf](reports/slides/figure_appendix.pdf) |
| 15-slide research overview | [reports/slides/research_review.pdf](reports/slides/research_review.pdf) |
| Four-dataset evidence coverage | [reports/figures/fig_dataset_coverage.pdf](reports/figures/fig_dataset_coverage.pdf) |
| Independent pools and matched prediction baseline | [reports/figures/fig_pool_replication.pdf](reports/figures/fig_pool_replication.pdf) |
| Each report page explained simply | [reports/Sept_Dataset_Update_README.md](reports/Sept_Dataset_Update_README.md) |
| Editable presentation | [reports/slides/research_review.pptx](reports/slides/research_review.pptx) |
| Architecture diagram image | [reports/figures/fig_architecture.png](reports/figures/fig_architecture.png) |
| Architecture diagram vector PDF | [reports/figures/fig_architecture.pdf](reports/figures/fig_architecture.pdf) |
| Detailed attacker: tensors, layers, objective and linkage | [reports/figures/fig_attack_detail.pdf](reports/figures/fig_attack_detail.pdf) |
| Three-seed, two-partition scheme follow-up | [experiments/scheme_followup_2026-09-18/README.md](experiments/scheme_followup_2026-09-18/README.md) |
| Threat model and key regimes | [reports/figures/fig_threat_model.png](reports/figures/fig_threat_model.png) |
| Earlier three-seed results overview | [reports/figures/fig_results_overview.png](reports/figures/fig_results_overview.png) |
| New IoM-GRP and PolyProtect pilot results | [reports/figures/fig_scheme_pilots.png](reports/figures/fig_scheme_pilots.png) |
| All plot descriptions and regeneration commands | [reports/figures/README.md](reports/figures/README.md) |
| Pilot numerical results and interpretation | [experiments/scheme_extension_pilot/README.md](experiments/scheme_extension_pilot/README.md) |

Individual plots, including paired uncertainty, equivalence sensitivity and native matching, are in `reports/figures/`, each as a `.png` and `.pdf` pair. Combined PDFs and the PowerPoint are in `reports/slides/`. These are generated research graphics, not raw face photographs; private biometric data and detailed run artifacts are deliberately excluded.

## Dataset access and archives

**MOBIO, LFW, FEI and SCface have been used.** Sani supplied the authorized SCface archive on 2026-09-18; its BioHash study and one-seed scheme pilots are complete, but its private inputs were unavailable on the host executing the later follow-ups. FEI and SCface satisfy added-dataset coverage beyond MOBIO/LFW, not the broader confirmatory matrix. AgeDB remains an optional addition without authorized access.

| Dataset and role | Official contact | Who should request access and what to send |
|---|---|---|
| **SCface: acquired and evaluated**, camera/distance variation | [Official page](https://www.scface.org/) | Authorized archive received 2026-09-18. Preserve license restrictions; local archive hash, layout and commands are in [SCface setup](docs/setup/SCFACE_LOCAL_DATA.md). No new access request is needed for the completed study. |
| **AgeDB: backup or optional third addition**, age variation | **Stylianos Moschoglou**, contact listed by Imperial College iBUG: [s.moschoglou@imperial.ac.uk](mailto:s.moschoglou@imperial.ac.uk). [Official page](https://ibug.doc.ic.ac.uk/resources/agedb/) | An authorized project member should email from an **academic address**, state affiliation and non-commercial research purpose, and request the archive password. Clarify collaborator/site and derived-result publication permissions. Keep the password private, outside chat and Git. |

Contacts and procedures were checked against the official pages on **2026-09-12**; SCface acquisition was recorded on **2026-09-18**. FEI's four official archives were acquired on 2026-09-12; MOBIO acquisition is documented in the [local handoff](docs/setup/MOBIO_LOCAL_DATA.md). Archives, faces, embeddings and keys remain private and are not cleanup targets. Each included identity must retain a gallery image plus ten usable exposures. See the [full access checklist](docs/datasets/access_request_checklist.md). Access does not itself authorize new training.

**Research question:** Can a key-agnostic attacker recover identity information from multiple independently protected face templates without their secret keys?

**Overall status:**

- [x] Month 1 engineering milestone completed on 2026-08-26.
- [x] Month 2 exploratory main experiment completed on 2026-09-04; MLP-Hash cross-scheme confirmation completed the same day.
- [ ] Month 3 validation, paper, and submission completed. Key-reuse boundary ablations started 2026-09-04.
- [ ] Published `benchmark_cb` or FaceLinkGen result reproduced.
- [ ] Post-meeting generalization completed on 2-3 additional face datasets and 2 additional protection schemes.

LFW, Olivetti, CFP, and MOBIO results are **independent engineering studies, not paper reproduction**. Synthetic runs validate plumbing only and are excluded from the scientific evidence. No published result has been reproduced yet.

**Latest extension:** The authorized one-hour MOBIO/FEI follow-up completed 24 cells / 216 endpoints in 859.63 seconds: IoM-GRP and PolyProtect, two new identity partitions, three model seeds, and fresh/shared/pool-4 keys. All eight primary pool-4 amplification contrasts have positive crossed-bootstrap intervals and Holm p = 0.004. Fresh PolyProtect native matching exceeds its permutation null in all 12 controls (Holm p = 0.006); synthetic radial sensitivity is not natural norm leakage. See the [follow-up results and scope](experiments/scheme_followup_2026-09-18/README.md). This bounded study does not complete the full roadmap.

SCface adds 130 identities and 2,851/2,860 valid embeddings, with 84.375% unprotected top-1 over 544 probes. BioHash pools 1/2/3 pass the all-seed rule; pool 4 fails. The earlier table remains 73 conditions / 12 studies, and pilots remain 24 cells / 72 endpoints. See [SCface results](experiments/scface_multiexposure/README.md), [SCface pilots](experiments/scface_scheme_extension_pilot/README.md), and the [17-figure appendix](reports/slides/figure_appendix.pdf). The [849-row inventory](experiments/multiexposure_run_matrix.csv) preserves all previous 633 rows, excluding unavailable SCface details; its [coverage audit](experiments/scheme_followup_2026-09-18/coverage_audit.csv) identifies legacy-schema gaps.

## [x] Month 1 - Foundation and baselines

**Proposal period:** Weeks 1-4

**Completed:** 2026-08-26, for the cross-dataset real-image engineering protocol

- [x] Literature review and threat-model comparison.
- [x] ArcFace-compatible extraction with official InsightFace `buffalo_l`.
- [x] Local 128-bit BioHash reference and independent-key generation.
- [x] Deterministic LFW, Olivetti, and CFP protocols with identity-disjoint train/validation/test splits.
- [x] Single-template MLP, three seeds, leakage checks, and evaluation metrics.
- [x] Six real-image protocol variants covering detector, sample-size, and pose robustness.
- [x] BioHash dimension robustness at 64/128/256 bits on two real datasets.
- [x] Crossed identity-assignment/key/model sensitivity study on larger LFW and CFP frontal.
- [x] Identity-clustered bootstrap intervals for correlated probes.
- [x] Cross-dataset leakage result documented and reproducible.
- [ ] Exact ArcFace + BioHash + MOBIO `benchmark_cb` reproduction. Blocked by the missing official source and exact protocol.

**Data:** Funneled LFW (small SCRFD/YuNet and 150-identity YuNet protocols), all 40 Olivetti identities, and all 500 CFP identities in separate frontal/profile protocols. The largest run used 4,999 CFP frontal embeddings, 100 gallery identities, and 900 probes.

**Results:**

- Unprotected ArcFace top-1: `94.92%` to `100.00%` across six protocol variants.
- Fixed-transform calibration top-1: `51.11%` to `91.00%`, confirming learnability when the transform is reusable.
- Independent unseen-key top-1 remained compatible with the applicable chance rate on every protocol; AUROC stayed near `0.5` and EER near `50%`.
- CFP frontal: `1.15% +/- 0.17%` top-1 versus `1.00%` chance over 900 probes.
- Larger LFW: `3.83% +/- 0.93%` top-1 versus `3.33%` chance over 270 probes.
- No per-seed descriptive exact binomial test rejected chance (`p >= 0.1205`); 64/128/256-bit sweeps were also null.
- In the crossed `3 identity assignments x 3 key seeds x 3 model seeds` sensitivity study, independent-key cell means were `0.81-1.11%` on CFP versus `1.00%` chance and `2.59-3.58%` on larger LFW versus `3.33%` chance.
- All 54 independent-key run-level identity-clustered 95% intervals included chance; fixed-transform cell means remained `91.70-94.74%` on CFP and `66.54-77.41%` on LFW.

**Milestone question:** Can a key-free attacker recover identity from one template?

**[x] Answered on 2026-08-26 for the tested real-data protocols:** No useful recovery was detected under independent unseen keys. This is a robust but scoped negative result, not a universal privacy or irreversibility claim.

Evidence: [cross-dataset protocol](docs/protocols/real_datasets_month1.md), [aggregate results](experiments/month1_real_datasets/results_summary.csv), [dimension sweep](experiments/month1_real_datasets/dimension_sweep.csv), [seed-robustness summary](experiments/month1_real_datasets/seed_robustness_summary.csv), [cell aggregates](experiments/month1_real_datasets/seed_robustness_cells.csv), and [research log](docs/research_log.md).

## [x] Month 2 - Exploratory main experiment

**Proposal period:** Weeks 5-8

**Completed:** 2026-09-04 for preregistered BioHash and MLP-Hash MOBIO protocols; broader validation remains open.

- [x] Masked permutation-invariant DeepSets model implemented and tested on synthetic data.
- [x] Synthetic 1/2/5/10 exposure smoke runs available for pipeline validation only.
- [x] Build real MOBIO sets for 1/2/5/10 independently keyed exposures.
- [x] Separate same-image/new-key from different-image/new-key experiments.
- [x] Run held-out identities with unseen test keys over three model seeds.
- [x] Compare MLP, mean pooling, max pooling, and DeepSets baselines.
- [x] Compare one exposure with 2/5/10 exposures using identity-clustered intervals and a preregistered threshold.

**Results:** Independent-key top-1 stayed at chance across 1/2/5/10 exposures and all aggregation models. Ten-exposure DeepSets achieved `3.33%` top-1 versus `3.33%` chance, AUROC `0.4988`, and EER `49.81%`. Shared-key and unprotected controls were strongly positive.

**Milestone question:** Does multi-exposure create significantly greater identity leakage?

**[x] Exploratorily answered on 2026-09-04:** No greater identity leakage was detected up to 10 independently keyed exposures. This is a scoped negative result requiring confirmation, not proof of irreversibility.

**Cross-scheme confirmation:** Paper-specified MLP-Hash also remained at chance: `2.50% +/- 1.10%` top-1 at one record and `3.33%` for 10-record DeepSets, with AUROC `0.4998`. The shared-key and unprotected controls remained strongly positive.

Evidence: [preregistered protocol](docs/protocols/multi_exposure.md) and [MOBIO multi-exposure results](experiments/mobio_multiexposure/README.md).

## [ ] Month 3 - Validation and paper

**Proposal period:** Weeks 9-12

**Status checked:** 2026-09-18

- [x] Run a preregistered paper-specified MLP-Hash cross-scheme test with new key/set/model seeds.
- [x] Run session-aligned and sample-randomized key-reuse boundary ablations (pools 1/2/5/10 versus fresh keys).
- [x] Replicate the key-pool boundary on a new identity partition, a dense 3-9 pool sweep, and paper-specified MLP-Hash.
- [x] Resolve the boundary over three partitions, add a Haar sign-corrected variant, and replicate on public LFW.
- [x] Write the fresh-key multiplicity-invariance theorem with explicit assumptions and implementation caveats.
- [x] Start the paper draft with every number traced to a tracked summary ([reports/paper_draft.md](reports/paper_draft.md)).
- [x] Run corrected key-slot-known and shuffled-non-anchor mechanism controls.
- [x] Run key-correlation and same-image/different-key ablations.
- [x] Run genuine raw/shuffled/fixed-radius native controls on MOBIO/FEI; identity-specific norm leakage not established.
- [x] Complete intervals, corrected tests and failure analysis for all 48 bounded-follow-up contrasts; historical missing-score inference remains open.
- [x] Run the bounded revision audit and revise supported claims; broader confirmatory experiments remain outside this scope.
- [x] Produce revised figures, reproducible commands and paper draft; independent review/final submission remain open.
- [ ] Submit the paper.

**Results:** BioHash and MLP-Hash both show chance-level identity recovery under fresh independent hidden keys. A scoped rotational-invariance proposition explains why arbitrary record multiplicity cannot help under fixed-norm ideal assumptions; the key-reuse boundary below tests one important violation.

**Positive boundary result:** With 10 records and session-aligned recurring BioHash transforms, mean-pool top-1 was `66.39%/61.11%/47.64%/33.89%` for pools of 1/2/5/10, versus `2.92%` with fresh keys. A preregistered sample-randomized confirmation retained severe leakage for pools 1/2/5 (`77.50%/69.44%/46.94%`) but not pool 10 (`5.56%`, equal to the fresh endpoint). The all-pools criterion therefore failed, refining the result to a small-pool reuse threshold rather than a universal monotonic curve.

**Generalization (three further preregistered runs):**

- New identity partition (split seed 90551): pools 1/2/5 gave `81.67%/73.89%/51.11%`, pool 10 gave `5.56%`, fresh `3.61%`. Pools 1/2/5 passed, pool 10 failed, matching the first randomized run.
- Dense sweep: pools 3/4/6/7/8/9 gave `65.00%/54.03%/17.36%/34.44%/10.42%/3.89%`, fresh `5.56%`. Pools 3/4/7 passed; 6/8/9 failed. The threshold lies near 7-9 transforms under this protocol and is noisy near the boundary (pool 6 below pool 7).
- Paper-specified MLP-Hash: pools 1/2/5/10 gave `71.39%/68.89%/22.92%/1.94%`, fresh `3.06%`. Pools 1/2 passed; pool 5 exceeded the five-point margin but one clustered interval touched chance; pool 10 failed.

**Multiplicity amplification depends on transform diversity.** Selected BioHash pools show small single-record means (`3.5%-4.3%`) while ten-record means reach `34%-54%`. This is not universal. Fresh-key one- and ten-record means vary (`3.2%` vs `5.6%`; `4.0%` vs `3.6%`); the idealized [invariance theorem](docs/theory/multiplicity_invariance.md) does not require exact finite empirical equality or prove equivalence.

**Boundary resolution and second dataset.** Across three MOBIO identity partitions, pools 3-4 pass in every partition (pooled `56.7% / 51.5%`), pools 5-7 are partition-dependent, and tested pools 8/9 fail the interval criterion (pooled fresh `3.8%`). Failure is not equivalence. Haar sign-corrected BioHash gives `74.6 / 48.1 / 2.6%` for pools 1/5/fresh, a qualitatively similar pattern, not verified equivalence. MLP-Hash pools 3/4 give `54.3% / 37.8%`. On LFW (125 identities x 12 images, chance `4.0%`), fresh keys give `4.0%` while pools 1/2/3/4/5/7/10 give `73.2 / 63.2 / 62.5 / 42.5 / 41.0 / 32.0 / 25.3%`; pool 10 fails the strict interval rule. See [experiments/lfw_multiexposure/README.md](experiments/lfw_multiexposure/README.md).

**Third dataset (FEI, 2026-09-12).** Controlled high-resolution pose sweep, 200 identities x 12 images, chance `2.5%`. Fresh keys gave `1.8%` (AUROC `0.502`); pools 1/2/3/4/5/7/10 gave `76.9 / 63.4 / 54.8 / 47.5 / 37.5 / 23.6 / 4.0%`. Tested pools 3/4/5/7 have small single-record means (`2.4-3.8%`) and ten-record means `24-55%`. Tested pools 1/2/3/4/5/7 pass; pool 10 fails; pools 6/8/9 were not tested. See [experiments/fei_multiexposure/README.md](experiments/fei_multiexposure/README.md), the study-level [experiments/cross_dataset_key_pool_summary.csv](experiments/cross_dataset_key_pool_summary.csv), and [reports/figures/README.md](reports/figures/README.md).

**Mechanism controls.** On a new MOBIO partition, the hidden-slot DeepSets baseline gave `55.3 / 46.3 / 32.9 / 23.8%` for pools 3/4/5/7 and `3.33%` for fresh keys. Giving DeepSets the true recurring-transform slot changed these by only `+1.8 / +4.4 / +0.7 / -0.8` points, so implicit slot identification is not the main boundary mechanism. Replacing nine of ten records with records from other identities collapsed pools 3/4 and fresh keys to exactly `3.33%` for every seed. The reuse gain therefore requires multiple records from the same identity rather than set size or transform frequencies alone; see [experiments/mobio_mechanism_controls/README.md](experiments/mobio_mechanism_controls/README.md).

**Fresh-key and correlation controls.** Repeating the identical normalized image embedding under ten distinct fresh keys remained exactly at chance (`3.33%`, AUROC `0.4997`), matching the different-image fresh-key baseline. In a controlled partial-projection-reuse model, a new-partition fine sweep remained near chance through `12.5%` shared dimensions, was weak and seed-sensitive at `18.75-31.25%`, and gave `35.8 / 49.3 / 42.6%` ten-record top-1 at `37.5 / 43.75 / 50%` shared dimensions. This supports a graded correlation-to-leakage relationship, not a universal transition threshold; see [experiments/mobio_correlation_controls/README.md](experiments/mobio_correlation_controls/README.md).

**Proposal deliverable:** Reproducible attack framework, results, and paper.

**[ ] Full submission milestone not met as of 2026-09-18.** The framework, four-dataset evidence, 72 pilot/216 follow-up endpoints, genuine raw-input native audit, complete follow-up failure analysis, revised figures and manuscript exist. The full matrix, raw-input learned retraining, stricter PolyProtect policy, equivalence margins, independent review and submission remain open. Source-exact reproduction is still blocked.

**Fourth dataset (SCface, 2026-09-18).** On a 78/26/26 identity split, ten-record BioHash top-1 is `81.57/61.06/33.17/20.51/5.93/1.92/3.04%` for pools 1/2/3/4/5/7/10; fresh keys give `3.85%` against `3.846%` chance. Pools 1-3 pass the all-seed interval criterion. SCface pool-4 pilot paired gains are `+34.62` points for IoM-GRP and `+41.83` for PolyProtect, conditional on one seed. These are independent studies, not benchmark reproductions or confirmation of the complete roadmap.

## Dataset status

| Dataset              | Status       | Work completed                                                        | Next action                                         |
| -------------------- | ------------ | --------------------------------------------------------------------- | --------------------------------------------------- |
| Synthetic identities | [x] Plumbing | CPU smoke pipeline only; excluded from scientific evidence            | Keep as test data only                              |
| LFW funneled         | [x] Used     | Month 1 checks; 125 x 12 key-pool replication of the MOBIO protocol   | Preserve as second-dataset evidence                 |
| FEI                  | [x] Used     | BioHash key-pool study; IoM-GRP/PolyProtect pilots and 108 follow-up endpoints | Extend only beyond the documented bounded scope |
| SCface               | [x] Used     | 130 identities; mugshot/surveillance BioHash study; IoM-GRP/PolyProtect pilots | Confirm across seeds and partitions |
| AgeDB                | [ ] Optional | No authorized archive or experiments | Acquire only if the optional third addition is approved |
| Olivetti faces       | [x] Used     | Full 40-identity protocol and dimension sweep                         | Preserve as cross-dataset evidence                  |
| CFP                  | [x] Used     | Full frontal/profile protocols and crossed-seed sensitivity checks    | Preserve as large-scale/view evidence               |
| MOBIO                | [x] Used     | Boundary/controls; pilots and 108 follow-up endpoints; genuine raw-norm/native audit | Independent review and scoped remaining confirmation |
| CASIA-WebFace        | [ ] Not used | Reviewed as a possible FaceLinkGen training source                    | Use only after license and protocol verification    |
| TPDNE                | [ ] Not used | Reviewed as optional FaceLinkGen evaluation data                      | Defer until core identity linkage works             |

Data, embeddings, keys, model weights, and detailed run artifacts are gitignored.

## Models and reproductions

- [x] InsightFace `buffalo_l` archive and model hashes verified on 2026-08-26.
- [x] OpenCV SCRFD/ArcFace and hash-pinned OpenCV Zoo YuNet/ArcFace backends validated because ONNX Runtime cannot initialize on this host.
- [x] Local BioHash and single-template attack path validated.
- [ ] `benchmark_cb`: paper targets and MOBIO data are available, but the official repository and exact configuration are unavailable.
- [ ] FaceLinkGen: no verified official implementation or local reproduction.

## Next work

Sani requested the next generalization phase during the 2026-09-10 meeting. The full staged plan, selection gates, experiment matrix, and presentation deliverables are in [docs/ROADMAP.md](docs/ROADMAP.md).

1. Review completed FEI/SCface added-dataset studies; decide whether optional AgeDB coverage is justified before requesting access.
2. Review the 216-endpoint follow-up alongside the 72 historical pilot endpoints; investigate the mechanism behind native PolyProtect linkage after the completed permutation controls.
3. Approve and freeze the remaining cross-dataset/exposure matrix before further training; SCface follow-up needs local embeddings.
4. Review completed raw/shuffled/fixed-radius controls and all 48 follow-up contrasts; approve equivalence margins before any equivalence claim.
5. Obtain independent human theory/novelty review using the [review checklist](docs/review/scheme_pilot_review_2026-09-12.md).
6. Review the regenerated deck and figures with Sani; reconcile historical artifacts with the local per-seed matrix.
7. Recover the official `benchmark_cb` source before claiming source-exact reproduction.

Full task details and human-only blockers are in [docs/TODO.md](docs/TODO.md).

## AI handoff rules

Any AI assistant working in this repository must update this README when project status changes.

1. Read this README, [docs/TODO.md](docs/TODO.md), [docs/research_log.md](docs/research_log.md), and the relevant protocol/results before changing a checkbox.
2. Mark a task `[x]` only after it has executable evidence. Mark a month `[x]` only when its milestone question or deliverable is answered; partial code is not enough.
3. Update `Last status update` and add the completion or status-check date in `YYYY-MM-DD` format.
4. Under the relevant month, record what ran, the dataset/protocol, exact headline results, and whether the milestone question was answered.
5. Update the dataset table and `Next work`; carry unresolved blockers forward.
6. Append commands, results, failures, and decisions to [docs/research_log.md](docs/research_log.md).
7. Never convert LFW or synthetic validation into a paper-reproduction claim, and never fabricate a missing result.
8. Never commit biometric data, embeddings, keys, credentials, private paths, model weights, or detailed sensitive artifacts.

## Install and run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,face]"
make test
make smoke-test
```

Run the completed studies through the Month 1 targets in the `Makefile` after following the [real-dataset protocol](docs/protocols/real_datasets_month1.md). Results are written under gitignored `results/`. On Windows systems without GNU Make, run the listed Python commands directly.

MOBIO must be obtained through the [official access procedure](docs/setup/MOBIO.md). Luigi's exact eight-file acquisition list, checksums, external layout, experiment input directory, and preparation commands are in the [local MOBIO handoff](docs/setup/MOBIO_LOCAL_DATA.md). The repository does not bypass dataset or model access controls.

See [reports/final_research_status.md](reports/final_research_status.md) for the current scientific interpretation and limitations.
