# LFW Month 1 single-template protocol

## Classification

This is **engineering validation, not a `benchmark_cb` or MOBIO reproduction**. It addresses the proposal's Month 1 milestone: establish ArcFace plus one protection scheme, identity-disjoint splits, a single-template MLP, evaluation metrics, and a first leakage result while MOBIO access is pending.

## Data and model

- Dataset: funneled LFW acquired through `sklearn.datasets.fetch_lfw_people` from the UMass source.
- Deterministic subset seed: `20260826`.
- Planned subset: 60 identities with 6 images each; 36 train, 12 validation, and 12 test identities.
- Extracted subset: 359/360 images. SCRFD did not detect a face in one test image, leaving 216 train, 72 validation, and 71 test embeddings.
- Test protocol: one gallery image per test identity and 59 remaining probe images across 12 identities. Random top-1 chance is `1/12 = 8.33%`.
- Feature model: official InsightFace `buffalo_l`, ResNet50@WebFace600K, 512 dimensions, non-commercial research use only.
- Detection/alignment: `det_10g.onnx` SCRFD at 640x640, five-point ArcFace alignment, then `w600k_r50.onnx` through OpenCV DNN.
- Archive SHA-256: `80ffe37d8a5940d59a7384c201a2a38d4741f2f3c51eef46ebb28218a7b0ca2f`.
- Recognition model SHA-256: `4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43`.
- Detection model SHA-256: `5838f7fe053675b1c7a08b633df49e7af5495cee0493c7dcf6697200b85b5b91`.

The OpenCV backend was used because ONNX Runtime could not initialize its native DLL on this Windows host. Repeat extraction of a checked image was exact, all embedding norms were within `1.2e-7` of 1, and mean same-identity cosine was `0.628` versus `0.0056` for 2,000 sampled different-identity pairs.

## Protection and attacker

The local reference BioHash maps a 512-D ArcFace vector to 128 bits using a keyed orthonormal random projection and zero threshold. It has not been cross-checked against the unavailable official `benchmark_cb` source.

Two conditions are intentionally separate:

1. `shared_key_calibration`: one fixed transformation is used everywhere. This is a learnability upper bound, not the proposed low-knowledge threat model and not automatically equivalent to the paper's stolen-token scenario.
2. `independent_unseen_keys`: every image receives an independent key and train/validation/test key pools are disjoint. The attacker never receives a key. This is the primary Month 1 condition.

The attacker is a `128 -> 256 -> 512` MLP with ReLU and L2-normalized output. It is trained on public training identities to align with same-image ArcFace embeddings using cosine loss plus `0.1` MSE. Early stopping uses identity-disjoint validation identities. Seeds are `7`, `17`, and `27`.

## Results

| Condition | Evaluator | Target cosine | Top-1 | AUROC | EER |
| --- | --- | ---: | ---: | ---: | ---: |
| Chance reference | N/A | N/A | 8.33% | 0.500 | 50.00% |
| Unprotected ArcFace | direct gallery/probe | N/A | 98.31% | 0.9987 | 0.85% |
| Shared-key BioHash | direct Hamming similarity | N/A | 98.31% | 0.9936 | 1.85% |
| Shared-key calibration | MLP, mean +/- SD | 0.1545 +/- 0.0030 | 53.11% +/- 2.59% | 0.8925 +/- 0.0107 | 20.67% +/- 1.89% |
| Independent-key BioHash | direct Hamming similarity | N/A | 5.08% | 0.5237 | 52.16% |
| Independent unseen keys | MLP, mean +/- SD | 0.0342 +/- 0.0052 | 9.60% +/- 0.98% | 0.5139 +/- 0.0188 | 49.13% +/- 3.40% |

For independent unseen keys, top-1 counts were 5/59, 6/59, and 6/59. Exact one-sided binomial tests against chance gave `p = 0.552`, `0.369`, and `0.369`. These probe-level tests are descriptive because multiple probes share identities. This study therefore found **no evidence of useful single-template identity recovery under independent unseen keys**. The fixed-transform calibration was well above chance, confirming that the extraction and learning path can recover identity signal when the transform is reusable.

This negative primary result does not test or reject the proposed novelty. The hypothesis is specifically that multiple independently protected observations may be collectively exploitable even when a single observation is weak. Month 2 must compare 1/2/5/10 exposures under the same unseen-identity and unseen-key controls.

## Reproduction commands

```powershell
python scripts\data\download_lfw.py --data-home data\raw\lfw --min-faces-per-person 5
python scripts\setup\download_buffalo_l.py --accept-research-only-license
python scripts\data\prepare_lfw.py
python scripts\train_or_extract\extract_arcface.py `
  --input-csv data\interim\lfw_month1_protocol.csv `
  --backend opencv --model-name buffalo_l `
  --recognition-model models\insightface\buffalo_l\w600k_r50.onnx `
  --detection-model models\insightface\buffalo_l\det_10g.onnx `
  --skip-errors --output data\processed\embeddings\lfw\buffalo_l
python scripts\diagnostics\check_leakage.py --manifest data\interim\lfw_month1_protocol.csv
python scripts\train\run_lfw_month1.py --config configs\attacks\month1_lfw.yaml
```

Raw images, embeddings, model weights, and detailed run artifacts remain gitignored.

The tracked aggregate is in `experiments/month1_lfw/results_summary.csv`.
