# SCface IoM-GRP and PolyProtect pilots

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
