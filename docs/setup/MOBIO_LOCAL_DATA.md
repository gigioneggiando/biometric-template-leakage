# MOBIO local data setup for Luigi

MOBIO is restricted, so its images, annotations, metadata, derived embeddings, and local manifests must never be committed or shared through GitHub. Each researcher must request access from the official [Zenodo record](https://zenodo.org/records/4269551) and accept its terms independently.

## Local acquisition record

The authorized archives were downloaded on 2026-09-03 and extracted and validated on 2026-09-04. The compressed archives were removed after extraction; `4269551.json` and `MD5SUM.TXT` were retained as provenance. The MD5 values below agree with both files from the official record.

Exactly these eight archives were downloaded:

| Download | Bytes | Official MD5 | Extracted directory | Files | Used in this study |
|---|---:|---|---|---:|---|
| `IMAGES_PNG.tar.gz` | 7,955,650,560 | `d443738314f7ded24397e326a888ab88` | `IMAGES_PNG/` | 30,326 | No; retained as the official PNG frame set |
| `IMAGE_ANNOTATIONS.tar.gz` | 1,085,440 | `20f9c51f93e9fde6a137bf759a6d3bc9` | `IMAGE_ANNOTATIONS/` | 30,326 | No |
| `selected-still-images.tar.gz` | 715,332,747 | `7dd3438b6bf5abbb7de45e4ad1637b18` | `selected-still-images/` | 28,800 | **Yes; image source for all MOBIO runs** |
| `selected-still-image-annotations.tar.gz` | 571,119 | `9f1974450f1e54599ec701521c1f4a08` | `selected-still-image-annotations/` | 28,800 | No; YuNet detected landmarks independently |
| `PROTOCOLS.tar.gz` | 7,229,440 | `2b96f0c768bb8ab5c89933c8f4d68eec` | `PROTOCOLS/` | 81 | No; retained for future exact reproduction |
| `MOBIO_PROTOCOLS-current-26-11-2010.tar.gz` | 111,036 | `e4fbb29e3bed30fff00fbe40e0285758` | `MOBIO_PROTOCOLS-current-26-11-2010/` | 13 | No; retained for provenance |
| `mobio-metadata-sql.tar.gz` | 1,630,013 | `f1eb45f83328d4c32093c5b528bda234` | `mobio-metadata-sql/` | 13 | No |
| `PATCHES_V2.tar.gz` | 10,240 | `99e06b887eaf03fbb41239948f207def` | `PATCHES_V2/` | 1 | No |

The extracted directories plus the two retained provenance files contain 118,362 files and 8,809,097,683 bytes (8.204 GiB). Audio, ICB2013, file-mapping, score, correction, and site-specific raw video archives in the 36-file Zenodo record were not downloaded because the current experiment is face-only.

## Local layout

On Windows, keep the complete extracted tree here:

```text
%USERPROFILE%\ResearchData\MOBIO\
```

Do not place it inside the repository. Extract each archive into its own directory and preserve the internal folder names. The selected-image root used by the experiment is:

```text
%USERPROFILE%\ResearchData\MOBIO\selected-still-images\selected-images
```

Only that `selected-images` directory is read by `prepare_mobio_protocol.py`. The local protocol does not claim to reproduce the unavailable `benchmark_cb` configuration: it parses identity and session from the selected-still filenames, chooses one image from each of 12 sessions for each of 150 identities, and makes an identity-disjoint 90/30/30 split.

## Luigi setup and verification

Luigi should obtain the same eight files through his own authorized Zenodo session. The content endpoint for each file is `https://zenodo.org/api/records/4269551/files/<archive-name>/content`; restricted downloads require Luigi's authenticated access and must not use a shared token. Verify each archive against the MD5 table before extraction, then extract it directly below `%USERPROFILE%\ResearchData\MOBIO` so the directory names match the table.

From the repository root:

```powershell
$env:MOBIO_ROOT = "$env:USERPROFILE\ResearchData\MOBIO"
.\.venv\Scripts\python.exe scripts\data\prepare_mobio.py --root $env:MOBIO_ROOT
.\.venv\Scripts\python.exe scripts\data\prepare_mobio_protocol.py `
  --image-root "$env:MOBIO_ROOT\selected-still-images\selected-images"
.\.venv\Scripts\python.exe scripts\diagnostics\check_leakage.py `
  --manifest data\interim\mobio_multiexposure_protocol.csv
```

Expected output is a 118,362-file inventory followed by a protocol containing 150 identities, 1,800 images, 12 distinct sessions per identity, and identity-disjoint splits of 90 train / 30 validation / 30 test identities. The generated manifest and protocol contain private local paths and are Git-ignored.

The extraction stage later produced 1,799 usable ArcFace embeddings from those 1,800 protocol rows. YuNet detected no face for `m120_07_p03_i0_0`; this single failure is recorded rather than silently replaced.

The repository also ignores a root-level `MOBIO_datasets/` directory as a final safeguard, but that is not the recommended storage location.
