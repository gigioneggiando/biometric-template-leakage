# Key-agnostic multi-exposure biometric template leakage

**Last status update:** 2026-09-04

**Research question:** Can a key-agnostic attacker recover identity information from multiple independently protected face templates without their secret keys?

**Overall status:**

- [x] Month 1 engineering milestone completed on 2026-08-26.
- [x] Month 2 exploratory main experiment completed on 2026-09-04; confirmation pending.
- [ ] Month 3 validation, paper, and submission completed.
- [ ] Published `benchmark_cb` or FaceLinkGen result reproduced.

LFW, Olivetti, CFP, and MOBIO results are **independent engineering studies, not paper reproduction**. Synthetic runs validate plumbing only and are excluded from the scientific evidence. No published result has been reproduced yet.

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

**Completed:** 2026-09-04 for the first preregistered MOBIO protocol; confirmation remains open.

- [x] Masked permutation-invariant DeepSets model implemented and tested on synthetic data.
- [x] Synthetic 1/2/5/10 exposure smoke runs available for pipeline validation only.
- [x] Build real MOBIO sets for 1/2/5/10 independently keyed exposures.
- [ ] Separate same-image/new-key from different-image/new-key experiments.
- [x] Run held-out identities with unseen test keys over three model seeds.
- [x] Compare MLP, mean pooling, max pooling, and DeepSets baselines.
- [x] Compare one exposure with 2/5/10 exposures using identity-clustered intervals and a preregistered threshold.

**Results:** Independent-key top-1 stayed at chance across 1/2/5/10 exposures and all aggregation models. Ten-exposure DeepSets achieved `3.33%` top-1 versus `3.33%` chance, AUROC `0.4988`, and EER `49.81%`. Shared-key and unprotected controls were strongly positive.

**Milestone question:** Does multi-exposure create significantly greater identity leakage?

**[x] Exploratorily answered on 2026-09-04:** No greater identity leakage was detected up to 10 independently keyed exposures. This is a scoped negative result requiring confirmation, not proof of irreversibility.

Evidence: [preregistered protocol](docs/protocols/multi_exposure.md) and [MOBIO multi-exposure results](experiments/mobio_multiexposure/README.md).

## [ ] Month 3 - Validation and paper

**Proposal period:** Weeks 9-12

**Status checked:** 2026-08-26

- [ ] Run cross-scheme tests and required ablations.
- [ ] Complete confidence intervals, significance tests, and failure analysis.
- [ ] Run revisions and final experiments.
- [ ] Produce final figures, reproducible commands, and paper draft.
- [ ] Submit the paper.

**Results:** Not started. No cross-scheme or final multi-exposure evidence exists.

**Proposal deliverable:** Reproducible attack framework, results, and paper.

**[ ] Not met as of 2026-08-26.** The framework is partially implemented, but the main Month 2 evidence and paper are pending.

## Dataset status

| Dataset              | Status       | Work completed                                                        | Next action                                         |
| -------------------- | ------------ | --------------------------------------------------------------------- | --------------------------------------------------- |
| Synthetic identities | [x] Plumbing | CPU smoke pipeline only; excluded from scientific evidence            | Keep as test data only                              |
| LFW funneled         | [x] Used     | Detector, sample-size, dimension, and crossed-seed sensitivity checks | Preserve as Month 1 evidence                        |
| Olivetti faces       | [x] Used     | Full 40-identity protocol and dimension sweep                         | Preserve as cross-dataset evidence                  |
| CFP                  | [x] Used     | Full frontal/profile protocols and crossed-seed sensitivity checks    | Preserve as large-scale/view evidence               |
| MOBIO                | [x] Used     | 150-identity single/multi-exposure study; data remains local          | Confirm across protocol/key seeds and another scheme |
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

1. Confirm the exploratory MOBIO null result across new protocol and key seeds.
2. Add at least one substantially different cancelable transform before making a cross-scheme claim.
3. Run the same-image/different-key control separately from the completed different-image/different-key condition.
4. Request the corrected official `benchmark_cb` source; do not substitute unofficial code.

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

MOBIO must be obtained through the [official access procedure](docs/setup/MOBIO.md). The repository does not bypass dataset or model access controls.

See [reports/final_research_status.md](reports/final_research_status.md) for the current scientific interpretation and limitations.
