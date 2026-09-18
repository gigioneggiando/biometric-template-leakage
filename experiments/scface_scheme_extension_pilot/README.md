# SCface IoM-GRP and PolyProtect pilots

**Study and documentation date: 2026-09-18.** Integrated in `4352eeb`, with protocol freeze `69a93e4`. Together with the [2026-09-12 MOBIO/FEI pilots](../scheme_extension_pilot/README.md), the current package has 24 cells / 72 model endpoints, shown in the [September update](../../reports/Sept_Dataset_Update.pdf).

Status: **COMPLETED ONE-SEED ENGINEERING PILOTS; NOT CONFIRMATION**.

The frozen `69a93e4` configuration evaluates paper-specified IoM-GRP and PolyProtect on the authorized SCface embeddings. All eight scheme/key-regime cells completed in 128.22 seconds, producing 24 trained-model endpoints. The test gallery has 26 identities and `3.846%` chance. Model seed `509`, key seed `91817`, set seed `91819`, a 120-epoch cap, and eight nested repeats are fixed.

| Scheme / condition | One record (%) | Ten-record mean (%) | Ten-record DeepSets (%) | Mean ten-minus-one gain (points) |
|---|---:|---:|---:|---:|
| IoM-GRP / pool 1 | 61.06 | 90.38 | 78.37 | 29.33 |
| IoM-GRP / pool 4 | 28.37 | 62.98 | 51.44 | 34.62 |
| IoM-GRP / pool 8 | 13.94 | 34.13 | 31.73 | 20.19 |
| IoM-GRP / fresh | 5.29 | 3.85 | 3.85 | -1.44 |
| PolyProtect / pool 1 | 67.79 | 82.21 | 78.85 | 14.42 |
| PolyProtect / pool 4 | 27.88 | 69.71 | 61.06 | 41.83 |
| PolyProtect / pool 8 | 5.29 | 9.62 | 30.29 | 4.33 |
| PolyProtect / fresh | 3.85 | 3.37 | 4.33 | -0.48 |

Fresh-key learned linkage remains chance-compatible for both schemes in this pilot. Recurring transforms create large linkage and paired multi-record gains, especially at pool 4. IoM-GRP retains a strong pool-8 effect; PolyProtect pool 8 depends heavily on the attacker architecture. These are conditional one-seed findings and cannot rank schemes or establish confirmation.

Native protected-gallery matching is a separate diagnostic. Under fresh parameters it gives `4.60%` top-1 for IoM-GRP and `10.66%` for PolyProtect, with AUROC `0.5110/0.5075`. The PolyProtect value is above chance and requires its own multi-seed uncertainty and null-calibration study; learned unprotected-gallery results near chance do not imply unlinkability.

Tracked files contain aggregate results only. See `results_summary.csv`, `paired_uncertainty.csv`, `equivalence_sensitivity.csv`, `native_utility.csv`, and `matrix_status.json`.

The [849-row local inventory](../multiexposure_run_matrix.csv) covers 49 artifacts but excludes SCface because its detailed artifacts are unavailable on this host. Its compact tables remain the source for current figures. The subsequent [MOBIO/FEI follow-up](../scheme_followup_2026-09-18/README.md) adds 216 endpoints across three model seeds and two identity assignments, plus native permutation and radial controls. It does not extend these SCface pilots: local SCface embeddings were unavailable, and the MOBIO/FEI null calibration cannot be attributed to SCface. Keep the [authorized archive provenance](../../docs/setup/SCFACE_LOCAL_DATA.md), original code freeze and run date.
