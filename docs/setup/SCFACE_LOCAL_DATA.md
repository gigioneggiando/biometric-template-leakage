# SCface local data setup

SCface is restricted research data. Do not redistribute its images, agreement, credentials, embeddings, or identity-level artifacts. Only aggregate results may enter Git.

## Authorized archive

Sani supplied the project archive on 2026-09-18.

| Archive | Bytes | SHA-256 |
|---|---:|---|
| `SCface_database.zip` | 1,546,981,520 | `F9F819C5B9634F457F1FE683E88F7BDF054174DDDC60F2947DBEA2BDFAFB1D7F` |

The archive has 7,176 entries, including duplicated convenience subsets. The experiment extracts only `mugshot_frontal_cropped_all/` and `surveillance_cameras_all/`. The latter contains 21 visible surveillance images plus one infrared image per identity; the protocol excludes infrared.

## Local layout

```text
E:\Research\Biometrics\SCFace\
  SCface_database.zip
  extracted\mugshot_frontal_cropped_all\
  extracted\surveillance_cameras_all\
```

`SCFace/`, `data/`, and `results/` are ignored. The deterministic protocol CSV and embedding files remain local.

## Commands

```powershell
.\.venv\Scripts\python.exe scripts\data\prepare_scface_protocol.py `
  --image-root E:\Research\Biometrics\SCFace\extracted --identities 130 --seed 20260918

.\.venv\Scripts\python.exe scripts\train_or_extract\extract_arcface.py `
  --input-csv data\interim\scface_multiexposure_protocol.csv --backend opencv-yunet `
  --model-name buffalo_l --recognition-model models\insightface\buffalo_l\w600k_r50.onnx `
  --detection-model models\opencv_zoo\face_detection_yunet_2023mar.onnx --skip-errors `
  --output data\processed\embeddings\scface_multiexposure\buffalo_l_yunet

.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py `
  --config configs\attacks\scface_key_pool_boundary.yaml
.\.venv\Scripts\python.exe scripts\train\run_scheme_extension_pilot.py `
  --config configs\attacks\scface_scheme_extension_pilot.yaml
```

Expected extraction: 2,851 successes and 9 detection failures from 2,860 selected visible images. All 130 mugshot gallery images succeed and every identity retains at least 19 surveillance exposures.
