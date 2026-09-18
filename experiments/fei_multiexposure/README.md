# FEI multi-exposure key-pool study

**Documentation checked: 2026-09-18. Study completed: 2026-09-12.** This retained third-dataset study now sits alongside [SCface](../scface_multiexposure/README.md) in the [73-condition comparison](../cross_dataset_key_pool_summary.csv). Additional FEI scheme findings are [one-seed pilots](../scheme_extension_pilot/README.md), not reruns of this BioHash study.

Status: **COMPLETED THIRD-DATASET REPLICATION; NOT A PAPER REPRODUCTION**.

FEI face database (Centro Universitario da FEI, Brazil; research use only, no redistribution). Four official `originalimages_part1-4.zip` archives (344 MB) downloaded on 2026-09-12 from the official page and hashed locally; hashes are kept outside Git in the external data folder. 2,800 images, 200 identities, 14 images each (11 profile-rotation steps, two frontal expressions, one low-illumination image), 640x480, white background, institutional volunteers aged 19-40, 100 male / 100 female.

Protocol: all 200 identities, 12 of 14 images chosen per identity by seed `20260912`, identity-disjoint 120/40/40 split (1,440/480/480 images). Embeddings extracted with the same hash-pinned YuNet (`8f2383e4...`) and ArcFace `w600k_r50` (`4c06341c...`) models as MOBIO and LFW: 2,378/2,400 succeeded. All 22 failures are the low-illumination pose 14; every identity keeps at least 11 embeddings, so the held-out gallery plus ten exposures is intact. 960/320/320 attack sets per level. Chance top-1 `1/40 = 2.50%`. BioHash 128-bit, randomized pool assignment, key seed 90697, set seed 90703, model seeds 367/377/387, exposures 1 and 10, mean-pool MLP. Preregistered in `docs/protocols/multi_exposure.md` before inspection.

## Results (10-record mean-pool top-1; 1-record single-MLP in parentheses)

| pool | top-1 (%) | AUROC | min clustered lower (%) | pass |
|---|---|---|---|---|
| 1 | 76.88 (74.58) | 0.970 | 58.8 | yes |
| 2 | 63.44 (36.35) | 0.961 | 45.0 | yes |
| 3 | 54.79 (3.75) | 0.931 | 37.8 | yes |
| 4 | 47.50 (3.44) | 0.932 | 31.6 | yes |
| 5 | 37.50 (2.81) | 0.926 | 18.1 | yes |
| 7 | 23.65 (2.40) | 0.872 | 10.9 | yes |
| 10 | 3.96 (3.02) | 0.575 | 0.0 | no |
| fresh (2,378 keys) | 1.77 (2.29) | 0.502 | 0.0 | - |

Unprotected oracle `100%`. Runtime 8.65 minutes.

## Interpretation

- Fresh keys: 10-record top-1 `1.77%`, below `2.50%` chance, AUROC `0.502`; no multiplicity amplification (`2.29% -> 1.77%`). Third dataset consistent with Theorem 1.
- Recurring pools: tested pools 1/2/3/4/5/7 pass both preregistered criteria; pool 10 fails (top-1 `3.96%`, one interval lower bound at zero). Pools 6/8/9 were not tested. Tested pools 3/4/5/7 have small single-record means (`2.4-3.8%`) while ten-record means reach `24-55%` of a 40-identity gallery; this is not an equivalence test of the single-record endpoint.
- Compared with MOBIO and LFW: FEI has the steepest single-record collapse (pool 3 already at chance) and the cleanest 10-record decay; the boundary is between pools 7 and 10, close to MOBIO partitions A/2 and later than MOBIO partition 3. FEI varies pose within one session, so this is a pose-robustness result, not a session-robustness result.

Full metrics remain local under `results/fei_key_pool_boundary/`. Reproduce with:

```powershell
.\.venv\Scripts\python.exe scripts\data\prepare_fei_protocol.py --image-root "$env:USERPROFILE\ResearchData\FEI\originalimages" `
  --identities 200 --samples-per-identity 12 --seed 20260912
.\.venv\Scripts\python.exe scripts\train_or_extract\extract_arcface.py --input-csv data\interim\fei_multiexposure_protocol.csv `
  --backend opencv-yunet --model-name buffalo_l --recognition-model models\insightface\buffalo_l\w600k_r50.onnx `
  --detection-model models\opencv_zoo\face_detection_yunet_2023mar.onnx --skip-errors `
  --output data\processed\embeddings\fei_multiexposure\buffalo_l_yunet
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\fei_key_pool_boundary.yaml
```
