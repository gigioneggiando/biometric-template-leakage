# Key-agnostic multi-exposure biometric template leakage

**Last status update:** 2026-09-04

**Research question:** Can a key-agnostic attacker recover identity information from multiple independently protected face templates without their secret keys?

**Overall status:**

- [x] Month 1 engineering milestone completed on 2026-08-26.
- [x] Month 2 exploratory main experiment completed on 2026-09-04; MLP-Hash cross-scheme confirmation completed the same day.
- [ ] Month 3 validation, paper, and submission completed. Key-reuse boundary ablations started 2026-09-04.
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

**Completed:** 2026-09-04 for preregistered BioHash and MLP-Hash MOBIO protocols; broader validation remains open.

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

**Cross-scheme confirmation:** Paper-specified MLP-Hash also remained at chance: `2.50% +/- 1.10%` top-1 at one record and `3.33%` for 10-record DeepSets, with AUROC `0.4998`. The shared-key and unprotected controls remained strongly positive.

Evidence: [preregistered protocol](docs/protocols/multi_exposure.md) and [MOBIO multi-exposure results](experiments/mobio_multiexposure/README.md).

## [ ] Month 3 - Validation and paper

**Proposal period:** Weeks 9-12

**Status checked:** 2026-09-04

- [x] Run a preregistered paper-specified MLP-Hash cross-scheme test with new key/set/model seeds.
- [x] Run session-aligned and sample-randomized key-reuse boundary ablations (pools 1/2/5/10 versus fresh keys).
- [x] Replicate the key-pool boundary on a new identity partition, a dense 3-9 pool sweep, and paper-specified MLP-Hash.
- [x] Resolve the boundary over three partitions, add a Haar sign-corrected variant, and replicate on public LFW.
- [x] Write the fresh-key multiplicity-invariance theorem with explicit assumptions and implementation caveats.
- [x] Start the paper draft with every number traced to a tracked summary ([reports/paper_draft.md](reports/paper_draft.md)).
- [ ] Run key-correlation, norm-leakage, same-image, and shuffled-record boundary ablations.
- [ ] Complete confidence intervals, significance tests, and failure analysis.
- [ ] Run revisions and final experiments.
- [ ] Produce final figures, reproducible commands, and paper draft.
- [ ] Submit the paper.

**Results:** BioHash and MLP-Hash both show chance-level identity recovery under fresh independent hidden keys. A scoped rotational-invariance proposition explains why arbitrary record multiplicity cannot help under fixed-norm ideal assumptions; the key-reuse boundary below tests one important violation.

**Positive boundary result:** With 10 records and session-aligned recurring BioHash transforms, mean-pool top-1 was `66.39%/61.11%/47.64%/33.89%` for pools of 1/2/5/10, versus `2.92%` with fresh keys. A preregistered sample-randomized confirmation retained severe leakage for pools 1/2/5 (`77.50%/69.44%/46.94%`) but not pool 10 (`5.56%`, equal to the fresh endpoint). The all-pools criterion therefore failed, refining the result to a small-pool reuse threshold rather than a universal monotonic curve.

**Generalization (three further preregistered runs):**

- New identity partition (split seed 90551): pools 1/2/5 gave `81.67%/73.89%/51.11%`, pool 10 gave `5.56%`, fresh `3.61%`. Pools 1/2/5 passed, pool 10 failed, matching the first randomized run.
- Dense sweep: pools 3/4/6/7/8/9 gave `65.00%/54.03%/17.36%/34.44%/10.42%/3.89%`, fresh `5.56%`. Pools 3/4/7 passed; 6/8/9 failed. The threshold lies near 7-9 transforms under this protocol and is noisy near the boundary (pool 6 below pool 7).
- Paper-specified MLP-Hash: pools 1/2/5/10 gave `71.39%/68.89%/22.92%/1.94%`, fresh `3.06%`. Pools 1/2 passed; pool 5 exceeded the five-point margin but one clustered interval touched chance; pool 10 failed.

**Multiplicity amplification is gated by transform diversity.** For pools 4-7 (BioHash) and pool 5 (new partition), a single record is at chance (`3.5%-4.3%`) while 10 records recover `34%-54%` of identities. Under fresh keys the 1-record and 10-record rates coincide (`3.2%` vs `5.6%`; `4.0%` vs `3.6%`), as the invariance theorem in [docs/theory/multiplicity_invariance.md](docs/theory/multiplicity_invariance.md) requires.

**Boundary resolution and second dataset.** Across three MOBIO identity partitions, pools 3-4 leak in every partition (pooled `56.7% / 51.5%`), pools 5-7 are partition-dependent, and pools >= 8 are null (pooled fresh `3.8%`). A Haar sign-corrected BioHash behaves identically (`74.6 / 48.1 / 2.6%` for pools 1/5/fresh). MLP-Hash pools 3/4 leak `54.3% / 37.8%`. On public LFW (125 identities x 12 images, chance `4.0%`), fresh keys give exactly `4.0%` with zero seed variance while pools 1/2/3/4/5/7/10 give `73.2 / 63.2 / 62.5 / 42.5 / 41.0 / 32.0 / 25.3%`; see [experiments/lfw_multiexposure/README.md](experiments/lfw_multiexposure/README.md).

**Proposal deliverable:** Reproducible attack framework, results, and paper.

**[ ] Not met as of 2026-09-04.** The framework, MOBIO evidence, cross-scheme confirmation, and first boundary result exist; the paper draft, remaining ablations, and additional seeds/datasets are pending.

## Dataset status

| Dataset              | Status       | Work completed                                                        | Next action                                         |
| -------------------- | ------------ | --------------------------------------------------------------------- | --------------------------------------------------- |
| Synthetic identities | [x] Plumbing | CPU smoke pipeline only; excluded from scientific evidence            | Keep as test data only                              |
| LFW funneled         | [x] Used     | Month 1 checks; 125 x 12 key-pool replication of the MOBIO protocol   | Preserve as second-dataset evidence                 |
| Olivetti faces       | [x] Used     | Full 40-identity protocol and dimension sweep                         | Preserve as cross-dataset evidence                  |
| CFP                  | [x] Used     | Full frontal/profile protocols and crossed-seed sensitivity checks    | Preserve as large-scale/view evidence               |
| MOBIO                | [x] Used     | BioHash/MLP-Hash multi-exposure, key-pool boundary, dense sweep, new partition | Two more partitions on the 3-9 sweep; controls |
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

1. Independent human review of the theorem in [docs/theory/multiplicity_invariance.md](docs/theory/multiplicity_invariance.md).
2. Key-aware (slot-label-known) attacker and same-image/different-key, shuffled-record, and norm-leakage controls.
3. Equivalence testing for the fresh-key null; novelty recheck on IEEE Xplore and Google Scholar.
4. Recover a source-exact published transform (`benchmark_cb` still unavailable) before making a source-exact claim.

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
