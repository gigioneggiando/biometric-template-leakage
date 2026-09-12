# FEI local data setup

FEI is research-use only and must not be redistributed. Nothing under this path enters Git: no images, embeddings, protocol CSVs, or manifests with personal paths.

## Acquisition (done 2026-09-12)

Official page: <https://fei.edu.br/~cet/facedatabase.html> (Centro Universitario da FEI, Dr. Carlos Eduardo Thomaz). Download only the four original-image archives; the aligned frontal subsets have two images per identity and cannot support the ten-record protocol.

| Archive | Bytes | SHA-256 |
|---|---|---|
| `originalimages_part1.zip` | 86,857,988 | `1D0B0EBE94278A5677EDC450251F91450DADB821D9774EDC111AD1BE0E7475ED` |
| `originalimages_part2.zip` | 89,176,109 | `993C2A48AC38C64824C619CBCDB0700598786AA2FA20A76F4B199457C8662E69` |
| `originalimages_part3.zip` | 88,206,682 | `65D282B338001E4ECE78944B751D5D78D94EDDFACF2C734CF8530BCD6435E252` |
| `originalimages_part4.zip` | 89,251,729 | `DD82ED2B475781DD4E829FB964923EB3A69E6F413F0E05AE694E65FCE9FBE44F` |

The page publishes no hashes; these were computed locally after download. A transfer interruption truncated part 4 on the first attempt (59,467,264 bytes); verify sizes before hashing.

## Layout

```
%USERPROFILE%\ResearchData\FEI\
  archives\originalimages_part{1..4}.zip
  SHA256SUMS.txt
  originalimages\<subject>-<pose>.jpg      2,800 files, subjects 1..200, poses 01..14
```

Poses 01-11 are a profile rotation sweep, 12-13 are frontal neutral/smiling, 14 is a low-illumination frontal. YuNet fails on 22 of the 200 pose-14 images in the 12-image protocol; every identity still keeps at least 11 valid embeddings.

## Commands

```powershell
$root = "$env:USERPROFILE\ResearchData\FEI"
New-Item -ItemType Directory -Force "$root\archives" | Out-Null
foreach ($i in 1..4) {
  Invoke-WebRequest -Uri "https://fei.edu.br/~cet/originalimages_part$i.zip" -OutFile "$root\archives\originalimages_part$i.zip" -UseBasicParsing
}
Get-FileHash "$root\archives\*.zip" -Algorithm SHA256 | ForEach-Object { "$($_.Hash)  $(Split-Path $_.Path -Leaf)" } | Set-Content "$root\SHA256SUMS.txt"
foreach ($i in 1..4) { Expand-Archive "$root\archives\originalimages_part$i.zip" -DestinationPath "$root\originalimages" -Force }

.\.venv\Scripts\python.exe scripts\data\prepare_fei_protocol.py --image-root "$root\originalimages" --identities 200 --samples-per-identity 12 --seed 20260912
.\.venv\Scripts\python.exe scripts\train_or_extract\extract_arcface.py --input-csv data\interim\fei_multiexposure_protocol.csv `
  --backend opencv-yunet --model-name buffalo_l --recognition-model models\insightface\buffalo_l\w600k_r50.onnx `
  --detection-model models\opencv_zoo\face_detection_yunet_2023mar.onnx --skip-errors `
  --output data\processed\embeddings\fei_multiexposure\buffalo_l_yunet
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\fei_key_pool_boundary.yaml
```

Expected extraction manifest: `count 2378, failure_count 22`, input manifest SHA-256 `dbffb260d983958d3074ce3c1e7f475018c54de90fd8f56116722f72d6da7b99`.

## Publication note

The FEI page grants research use but forbids distribution or reproduction of the database. Do not place FEI images in slides or the paper without checking with the maintainer; report aggregate results only. Cite Thomaz and Giraldi, Image and Vision Computing 28(6), 2010.
