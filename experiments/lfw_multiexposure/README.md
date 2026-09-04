# LFW multi-exposure key-pool study

Status: **COMPLETED SECOND-DATASET REPLICATION; NOT A PAPER REPRODUCTION**.

Funneled LFW (public, UMass source via scikit-learn), 125 of the 127 identities with at least 12 images, 12 images each, seed `20260904`, identity-disjoint 75/25/25 split (900/300/300 images), 1,500/1,500 embeddings extracted with the same hash-pinned YuNet (`8f2383e4...`) and ArcFace `w600k_r50` (`4c06341c...`) models as MOBIO. One held-out gallery image per identity; 600/200/200 attack sets per level; chance top-1 `1/25 = 4.00%`. BioHash 128-bit, randomized pool assignment, key seed 90679, set seed 90683, model seeds 337/347/357, exposures 1 and 10, mean-pool MLP. Preregistered in `docs/protocols/multi_exposure.md` before inspection.

## Results (10-record mean-pool top-1; 1-record single-MLP in parentheses)

| pool | top-1 | AUROC | min clustered lower | pass |
|---|---|---|---|---|
| 1 | 73.17 (70.67) | 0.979 | 52.0 | yes |
| 2 | 63.17 (37.33) | 0.950 | 41.0 | yes |
| 3 | 62.50 (23.83) | 0.960 | 35.5 | yes |
| 4 | 42.50 (16.83) | 0.862 | 19.5 | yes |
| 5 | 41.00 (11.50) | 0.864 | 22.5 | yes |
| 7 | 32.00 (11.67) | 0.776 | 13.0 | yes |
| 10 | 25.33 (4.33) | 0.792 | 4.0 | interval touches chance |
| fresh (1,500 keys) | 4.00 (4.67) | 0.505 | 0.0 | - |

Unprotected oracle `100%`. Runtime 5.66 minutes.

## Interpretation

- Fresh keys: 10-record top-1 exactly at chance with zero seed variance, AUROC `0.505`; no multiplicity amplification (`4.67% -> 4.00%`). Consistent with Theorem 1 on a second dataset.
- Recurring pools: every pool leaks. Pools 1-7 pass both preregistered criteria; pool 10 exceeds fresh by `21.3` points but one clustered lower bound equals chance, so it fails the interval criterion as designed.
- Difference from MOBIO: leakage decays more slowly on LFW (pool 10 at `25.3%` versus `5.6%` on MOBIO), and 1-record rates stay above chance up to pool 7 (`11.7%`), whereas on MOBIO they reach chance by pool 4. The boundary is therefore dataset-dependent and must be reported per protocol; the qualitative structure (chance under fresh keys, strong amplification under reuse) is the transferable finding.

Full metrics remain local under `results/lfw_key_pool_boundary/`. Reproduce with:

```powershell
.\.venv\Scripts\python.exe scripts\data\prepare_lfw.py --image-root data\raw\lfw\lfw_home\lfw_funneled `
  --output data\interim\lfw_multiexposure_protocol.csv --identities 125 --samples-per-identity 12 --seed 20260904
.\.venv\Scripts\python.exe scripts\train_or_extract\extract_arcface.py --input-csv data\interim\lfw_multiexposure_protocol.csv `
  --backend opencv-yunet --model-name buffalo_l --recognition-model models\insightface\buffalo_l\w600k_r50.onnx `
  --detection-model models\opencv_zoo\face_detection_yunet_2023mar.onnx --skip-errors `
  --output data\processed\embeddings\lfw_multiexposure\buffalo_l_yunet
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\lfw_key_pool_boundary.yaml
```
