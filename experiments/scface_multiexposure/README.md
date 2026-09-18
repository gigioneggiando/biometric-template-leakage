# SCface multi-exposure key-pool study

**Study and documentation date: 2026-09-18.** Protocol freeze: `69a93e4`; results integrated in `4352eeb`. This fourth dataset adds eight conditions to the [73-condition / 12-study table](../cross_dataset_key_pool_summary.csv). The [September report](../../reports/Sept_Dataset_Update.pdf) and all current figures include these results.

Status: **COMPLETED ADDED-DATASET STUDY; NOT A PAPER REPRODUCTION**.

Sani supplied the authorized SCface archive on 2026-09-18. The archive contains 130 identities with a visible frontal mugshot, 21 visible surveillance images from seven cameras at three distances, nine pose mugshots, and one infrared image per identity. This protocol uses the frontal mugshot as the held-out gallery record and the 21 visible surveillance images as exposure candidates; pose mugshots and infrared images are excluded.

Protocol: all 130 identities, identity-disjoint 78/26/26 split, seed `20260918`, 2,860 selected images. YuNet plus ArcFace extracted 2,851 embeddings; all 130 gallery mugshots succeeded, seven identities retain 20 exposure candidates, one retains 19, and the others retain 21. The held-out gallery plus ten-exposure construction therefore remains valid for every identity. The test gallery has 26 identities, so chance top-1 is `3.846%`.

Unprotected mugshot-to-surveillance matching reaches `84.375%` top-1, `91.176%` top-5, AUROC `0.9474`, and EER `10.827%` over 544 test probes. The positive control passes despite the difficult cross-camera and cross-distance domain shift.

## BioHash results

BioHash 128-bit, randomized pool assignment, key seed `91897`, set seed `91903`, model seeds `457/467/477`, exposures 1 and 10, mean-pool MLP. Configuration and code were committed at `69a93e4` before result inspection. Runtime was 392.14 seconds on CUDA.

| Pool | One-record top-1 (%) | Ten-record top-1 (%) | AUROC | Seed SD (points) | All clustered intervals exclude chance |
|---|---:|---:|---:|---:|---|
| 1 | 40.71 | 81.57 | 0.953 | 1.38 | yes |
| 2 | 22.44 | 61.06 | 0.915 | 2.96 | yes |
| 3 | 5.29 | 33.17 | 0.836 | 5.10 | yes |
| 4 | 4.01 | 20.51 | 0.734 | 12.02 | no |
| 5 | 5.13 | 5.93 | 0.565 | 0.99 | no |
| 7 | 4.17 | 1.92 | 0.535 | 1.36 | no |
| 10 | 3.21 | 3.04 | 0.522 | 0.45 | no |
| Fresh | 4.33 | 3.85 | 0.502 | 0.00 | no |

Fresh-key ten-record top-1 equals chance and AUROC is near 0.5. Pools 1-3 show clear reuse leakage and multi-record amplification. Pool 4 has a large mean gain but high seed variability and fails the all-interval criterion; pools 5, 7, and 10 do not show useful mean-pool linkage. This locates the transition near pools 3-5 for this protocol, without establishing equivalence in the failed conditions.

The tracked [summary](key_pool_boundary_summary.csv) contains only aggregate statistics. Images, embeddings, protocol manifests with local paths, keys, and detailed results remain ignored under `data/`, `results/`, and `SCFace/`.

Archive checksum and acquisition steps are retained in the [SCface setup record](../../docs/setup/SCFACE_LOCAL_DATA.md). The 633-row local per-seed inventory does not yet include SCface; do not infer its run-level coverage from the aggregate figures. Separate [IoM-GRP/PolyProtect pilots](../scface_scheme_extension_pilot/README.md) use one model seed and cannot establish full confirmation. No additional training was run for the report refresh.
