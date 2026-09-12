# Approved scheme pilots: 2026-09-12

Engineering diagnostics, not confirmatory evidence or a published reproduction. The user reported Sani's approval of paper-specified IoM-GRP and PolyProtect and authorized up to one hour of pilots. The protocol and implementation were committed as `d5f4e89` before execution.

## Scope and outcome

All 16 cells completed in 277.89 seconds on CPU (8 Torch threads), producing 48 trained-model results. No failed or unrun cells remain. Existing authorized MOBIO and FEI embeddings were reused; no new dataset was acquired. Each dataset/scheme was tested at pools 1/4/8 and fresh independent keys, with single-record MLP and ten-record mean-pool/DeepSets. Model seed 419, key seed 91217 and set seed 91219 are fixed. Training has a 120-epoch cap and patience 30.

IoM-GRP uses 300 groups of 16 Gaussian projections, with 4,800-dimensional one-hot attacker input. PolyProtect uses five-element windows, overlap two, unique nonzero integer coefficients in [-50,50], and a permutation of exponents 1..5; its 170 real outputs are not normalized. Both implementations are independently paper-specified, not source-exact. See the [frozen protocol](../../docs/protocols/scheme_extension_pilot_2026-09-12.md).

| Pool-4 endpoint | MOBIO IoM-GRP | FEI IoM-GRP | MOBIO PolyProtect | FEI PolyProtect |
|---|---:|---:|---:|---:|
| Single-record top-1 (%) | 52.50 | 61.25 | 4.17 | 3.13 |
| Ten-record mean top-1 (%) | 90.42 | 95.00 | 34.17 | 61.25 |
| Paired gain (percentage points) | 37.92 | 33.75 | 30.00 | 58.13 |
| Paired 95% interval (points) | [28.33,48.33] | [24.69,42.81] | [16.67,44.17] | [44.69,71.56] |

These four paired intervals exclude zero, conditional on this single trained seed and partition. They are descriptive, unadjusted for multiple comparisons, and do not establish confirmation. At pool 8, IoM-GRP retains large mean-pool gains; PolyProtect gains are small with intervals containing zero. At pool 1, FEI PolyProtect mean pooling performs worse than the single-record baseline. Do not infer universal improvement from more records or rank schemes against earlier three-seed, 400-epoch runs.

## Fresh keys and native matching

MOBIO has 30 gallery identities (3.33% chance); FEI has 40 (2.50%). Learned fresh-key top-1 ranges from 1.88% to 6.67% across the tested models. Paired ten-minus-one mean-pool intervals all include zero. No endpoint's 90% interval is strictly contained in +/-1 percentage point of chance; only one of 12 endpoints meets the illustrative +/-2-point band. Margins were not scientifically approved in advance. This is exploratory interval sensitivity, not confirmatory equivalence or a privacy result.

**Native protected-gallery matching is a separate diagnostic.** Pool-1 native top-1 and AUROC equal 1.0 for both schemes/datasets. With fresh PolyProtect parameters, protected-gallery top-1 is 12.73% on MOBIO and 13.73% on FEI, while AUROC is 0.4971/0.5237. This above-chance identification diagnostic needs confirmation and threat-model-specific analysis even though the learned embedding-linkage attackers are near chance. It uses all remaining test records as probes, not the eight nested attack sets. PolyProtect is not rotationally invariant and is outside the fresh-key theorem. There are no zero template rows in these diagnostics.

## Files and reproduction

- [results_summary.csv](results_summary.csv): 48 model runs, configuration fingerprint, code commit, and clustered intervals.
- [native_utility.csv](native_utility.csv): 16 protected-gallery diagnostics and template checks.
- [paired_uncertainty.csv](paired_uncertainty.csv): paired identity-bootstrap contrasts, using 2,000 resamples.
- [equivalence_sensitivity.csv](equivalence_sensitivity.csv): exploratory 90% intervals and strict containment at +/-1/2/5 points.
- [matrix_status.json](matrix_status.json): timing, completion and budget.

```powershell
.\.venv\Scripts\python.exe scripts/train/run_scheme_extension_pilot.py --config configs/attacks/scheme_extension_pilot.yaml
```

Completed outputs are protected from accidental overwrite; `--resume` requires matching configuration fingerprints. Identity-level scores, biometric artifacts and detailed metrics remain ignored. Aggregate exports whitelist fields and do not include identities or secret keys.

The [per-seed matrix](../multiexposure_run_matrix.csv) contains 633 rows from 25 locally available multi-exposure artifacts, including these 48 pilots. Five non-multi-exposure artifacts are excluded. It is a local coverage inventory, not proof that every historical study has been recovered. `config_sha256` in that matrix hashes the saved YAML bytes; the pilot table hashes canonical configuration serialization, so the two hashes are not interchangeable. Historical plots still use their tracked source-separated summaries; migration to one fully reconciled matrix remains pending. Missing stage annotations default to exploratory, not confirmation.

Next steps are listed in the [review and confirmation gates](../../docs/review/scheme_pilot_review_2026-09-12.md). No additional training beyond the authorized pilots was launched.