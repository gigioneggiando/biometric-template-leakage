# MOBIO local data setup for Luigi

MOBIO is restricted, so its images, annotations, metadata, derived embeddings, and local manifests must never be committed or shared through GitHub. Each researcher must request access from the official [Zenodo record](https://zenodo.org/records/4269551) and accept its terms independently.

## Files acquired

The current workstation has these extracted components:

| Download | Extracted directory | Files | Purpose |
|---|---|---:|---|
| `IMAGES_PNG.tar.gz` | `IMAGES_PNG/` | 30,326 | Official PNG still frames |
| `IMAGE_ANNOTATIONS.tar.gz` | `IMAGE_ANNOTATIONS/` | 30,326 | Coordinates for PNG frames |
| `selected-still-images.tar.gz` | `selected-still-images/` | 28,800 | Selected face images used by the local study |
| `selected-still-image-annotations.tar.gz` | `selected-still-image-annotations/` | 28,800 | Coordinates for selected stills |
| `PROTOCOLS.tar.gz` | `PROTOCOLS/` | 81 | Official face/speaker verification lists |
| `MOBIO_PROTOCOLS-current-26-11-2010.tar.gz` | `MOBIO_PROTOCOLS-current-26-11-2010/` | 13 | Original phase protocols |
| `mobio-metadata-sql.tar.gz` | `mobio-metadata-sql/` | 13 | Participant/site metadata and examples |
| `PATCHES_V2.tar.gz` | `PATCHES_V2/` | 1 | Upstream correction script/reference |
| `MD5SUM.TXT` | `MD5SUM.TXT` | 1 | Upstream archive checksums |
| Zenodo API metadata | `4269551.json` | 1 | Acquisition provenance |

Total after extraction: 118,362 files and 8.204 GB. Audio, ICB2013, and site-specific raw video archives were not downloaded because the current experiment is face-only.

## Local layout

On Windows, keep the complete extracted tree here:

```text
%USERPROFILE%\ResearchData\MOBIO\
```

Do not place it inside the repository. Extract each archive into its own directory and preserve the internal folder names. The selected-image root used by the experiment is:

```text
%USERPROFILE%\ResearchData\MOBIO\selected-still-images\selected-images
```

## Reproduce the local preparation

From the repository root:

```powershell
$env:MOBIO_ROOT = "$env:USERPROFILE\ResearchData\MOBIO"
python scripts\data\prepare_mobio.py --root $env:MOBIO_ROOT
python scripts\data\prepare_mobio_protocol.py `
  --image-root "$env:MOBIO_ROOT\selected-still-images\selected-images"
python scripts\diagnostics\check_leakage.py `
  --manifest data\interim\mobio_multiexposure_protocol.csv
```

The generated manifest and protocol contain local paths and are Git-ignored. Expected protocol totals are 150 identities, 1,800 images, 12 distinct sessions per identity, and identity-disjoint splits of 90 train / 30 validation / 30 test identities.

The repository also ignores a root-level `MOBIO_datasets/` directory as a final safeguard, but that is not the recommended storage location.
