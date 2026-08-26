# Month 1 real-dataset single-template protocol

## Scope

This is **engineering validation, not a `benchmark_cb`, MOBIO, or FaceLinkGen reproduction**. It completes the proposal's Month 1 single-template baseline on real biometric data while authorized MOBIO access and the official `benchmark_cb` source remain unavailable. Synthetic runs are pipeline tests only and are excluded from the evidence below.

## Data and provenance

All protocols use deterministic identity-disjoint 60/20/20 train/validation/test splits with seed `20260826`.

| Dataset/protocol | Planned data | Extracted | Test gallery/probes | Preprocessing |
| --- | ---: | ---: | ---: | --- |
| LFW small | 60 identities x 6 | 359/360 | 12 / 59 | SCRFD + ArcFace |
| LFW small robustness | 60 identities x 6 | 360/360 | 12 / 60 | YuNet + ArcFace |
| LFW large | 150 identities x 10 | 1,500/1,500 | 30 / 270 | YuNet + ArcFace |
| Olivetti faces | 40 identities x 10 | 400/400 | 8 / 72 | YuNet + ArcFace |
| CFP frontal | 500 identities x 10 | 4,999/5,000 | 100 / 900 | YuNet + ArcFace |
| CFP profile | 500 identities x 4 | 1,983/2,000 | 100 / 295 | YuNet + ArcFace |

- LFW funneled was acquired from the UMass source through `sklearn.datasets.fetch_lfw_people`.
- Olivetti faces was acquired through `sklearn.datasets.fetch_olivetti_faces`; cache SHA-256: `47398b319d88c78459514b30b87c562313aad345b5c6a387b678d7f8177be4ba`.
- CFP was acquired from its official HTTP research download; archive SHA-256: `666b87635e6af028177ac72a85f03099fac263baf09c21f333fa445f930f65b1`. The official host has no trusted HTTPS endpoint on this machine, so the pinned hash is mandatory before extraction. The archive contains no explicit license file, so redistribution is not assumed.
- The feature model is official InsightFace `buffalo_l`, ResNet50@WebFace600K, 512 dimensions, under the provider's non-commercial research terms. Recognition-model SHA-256: `4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43`.
- The primary detector is OpenCV Zoo YuNet, which supplies five landmarks for ArcFace alignment. Model SHA-256: `8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4`.

YuNet was selected after the existing SCRFD model failed dataset-suitability probes on Olivetti and CFP. The original LFW SCRFD run is retained, and the matched LFW YuNet run checks that the primary conclusion is not detector-specific.

## Protection, attacker, and evaluation

The local BioHash reference projects each 512-D embedding through a keyed orthonormal random matrix and thresholds at zero. The main experiments use 128 bits. A secondary LFW/Olivetti sweep uses 64, 128, and 256 bits.

Two conditions are kept separate:

1. `shared_key_calibration` reuses one transformation. It is a positive learnability control, not the primary threat model.
2. `independent_unseen_keys` assigns every image a separate key, with disjoint train/validation/test key scopes. It is the primary Month 1 condition.

The attacker is a `template_bits -> 256 -> 512` MLP with ReLU and L2-normalized output, trained with cosine loss plus `0.1` MSE. Early stopping uses validation identities. Model seeds are `7`, `17`, and `27`. Evaluation uses one gallery embedding per test identity, remaining images as probes, top-k linkage, AUROC, EER, and TAR at fixed FAR.

### Seed-robustness design

The larger LFW and CFP frontal protocols also use a crossed `3 identity assignments x 3 key seeds x 3 model seeds` design. Identity-assignment and key seeds are `20260826`, `20260827`, and `20260828`; model seeds remain `7`, `17`, and `27`. Robustness keys are derived from each stable `sample_id` rather than row order or assigned split, keeping identity-assignment and key factors separate while retaining unique, split-disjoint keys within every run. Protected templates are therefore computed once per key seed and reused across identity assignments without changing their values. Each split/key cell is summarized across its three model runs before study-level ranges are computed, so model runs are not treated as independent protocol replications. Cells share fixed datasets and pipeline components; this is a sensitivity analysis, not 27 independent replications per condition.

Top-1 uncertainty is additionally estimated by resampling test identities with replacement and retaining all probes belonging to each sampled identity. The deterministic percentile interval uses 2,000 resamples at 95% confidence. This respects within-identity probe clustering, but percentile intervals can under-cover with few identity clusters. Run-level intervals are inspected without familywise error correction; chance inclusion means compatibility with chance under that protocol, not equivalence, irreversibility, or a universal privacy guarantee.

## Cross-dataset results

| Protocol | Chance | Unprotected top-1 | Fixed-transform MLP | Independent-key MLP | AUROC | EER |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| LFW small, SCRFD | 8.33% | 98.31% | 53.11% +/- 2.59% | 9.60% +/- 0.98% | 0.5139 | 49.13% |
| LFW small, YuNet | 8.33% | 100.00% | 51.11% +/- 8.22% | 6.67% +/- 2.89% | 0.4962 | 51.24% |
| LFW large, YuNet | 3.33% | 100.00% | 76.05% +/- 2.63% | 3.83% +/- 0.93% | 0.5035 | 50.07% |
| Olivetti, YuNet | 12.50% | 100.00% | 61.57% +/- 7.65% | 11.57% +/- 1.60% | 0.4969 | 49.90% |
| CFP frontal, YuNet | 1.00% | 99.89% | 91.00% +/- 0.48% | 1.15% +/- 0.17% | 0.5007 | 50.04% |
| CFP profile, YuNet | 1.00% | 94.92% | 63.16% +/- 1.28% | 1.02% +/- 0.00% | 0.4996 | 49.56% |

Independent-key per-seed top-1 counts were `5/59, 6/59, 6/59`; `5/60, 5/60, 2/60`; `10/270, 13/270, 8/270`; `9/72, 7/72, 9/72`; `12/900, 10/900, 9/900`; and `3/295` for all three CFP profile seeds. One-sided exact binomial tests against the applicable random top-1 rate gave `p >= 0.1205`. These tests are descriptive because probes sharing an identity are not independent.

The dimension sweep was also null. LFW independent-key top-1 was `6.67%`, `6.67%`, and `7.22%` at 64/128/256 bits versus `8.33%` chance. Olivetti was `12.04%`, `11.57%`, and `10.65%` versus `12.50%` chance.

### Crossed-seed sensitivity results

| Dataset/condition | Chance | Mean across 9 split/key cells | Cell-mean range | Run intervals including chance |
| --- | ---: | ---: | ---: | ---: |
| CFP frontal, independent keys | 1.00% | 0.97% +/- 0.10% | 0.81-1.11% | 27/27 |
| CFP frontal, fixed transform | 1.00% | 93.57% +/- 1.21% | 91.70-94.74% | 0/27 |
| LFW large, independent keys | 3.33% | 3.14% +/- 0.31% | 2.59-3.58% | 27/27 |
| LFW large, fixed transform | 3.33% | 73.58% +/- 3.82% | 66.54-77.41% | 0/27 |

Mean and standard deviation above summarize nine dependent split/key cell means; they are not standard errors over independent datasets. All 54 independent-key run-level identity-clustered intervals included chance, while every fixed-transform interval excluded it. This supports robustness to the tested identity assignment, key randomness, and optimizer randomness. It does not prove equivalence to chance, and the many interval checks have no familywise error correction.

## Interpretation

The fixed-transform control is strongly learnable while the independent-key condition is consistently compatible with chance across three datasets, frontal/profile views, two detectors, a 4.2x LFW sample expansion, three template dimensions, and crossed identity/key/model seeds on larger LFW and CFP. This is convergent evidence that the current key-agnostic MLP does not recover useful identity information from one independently keyed template under these protocols.

This result does not establish universal irreversibility and does not test the proposed novelty. The unresolved research question is whether combining 2/5/10 independent observations changes leakage. That belongs to Month 2 and was intentionally not run here.

## Reproduction

Dataset acquisition and protocol commands are exposed through `scripts/data/`. Extraction uses `scripts/train_or_extract/extract_arcface.py --backend opencv-yunet`. Tracked experiment configs are under `configs/attacks/month1_*.yaml`; training uses `scripts/train/run_lfw_month1.py`. The dimension sweep uses `scripts/train/run_month1_dimension_sweep.py`; crossed seed robustness uses `scripts/train/run_month1_seed_robustness.py`.

Exact aggregate values are tracked in `experiments/month1_real_datasets/`. Raw data, protocol manifests containing local source paths, embeddings, model weights, keys, and detailed result artifacts stay gitignored.
