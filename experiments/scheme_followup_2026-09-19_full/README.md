# Extended multi-seed scheme follow-up: exposures, pool-8, SCface

**Completed: 2026-09-19.** All 32 planned cells and 672 model endpoints completed on CPU (8 Torch threads). The matrix records **1,008.66 seconds**; the outer execution manifest records **1,024.74 seconds** including subsequent work, within the authorized one-hour budget. This extends [scheme_followup_2026-09-18](../scheme_followup_2026-09-18/README.md); it does not change that study's frozen 216 endpoints or its original eight-hypothesis primary family, which remain unchanged.

## Design and provenance

MOBIO and SCface (FEI not present on this host); IoM-GRP and PolyProtect; identity reassignments 91831/91843; model seeds 601/607/613. Fresh, shared (pool 1), pool-4, and pool-8 conditions use key seed 92101 and set seed 92107 (new seeds, not reused from the earlier follow-up). Exposures 1, 2, 5, and 10; single MLP at exposure 1, mean-pool MLP and DeepSets at exposures 2/5/10; matched 120-epoch caps, patience 30.

[Protocol](../../docs/protocols/scheme_followup_2026-09-19_full.md) and [configuration](../../configs/attacks/scheme_followup_2026-09-19_full.yaml) were written before execution. The [execution manifest](execution_manifest.json) records the base commit, dirty-worktree status, and source/configuration/protocol hashes, matching the existing follow-up's provenance pattern.

## Primary result: pool-4 replicates on SCface

Pool-4 mean-MLP ten-minus-one-record top-1 gains, under new key/set seeds:

| Dataset | Scheme | Split | Gain (pp) | Holm p (family 8) |
|---|---|---:|---:|---:|
| MOBIO | IoM-GRP | 91831 | 32.50 | 0.004 |
| MOBIO | IoM-GRP | 91843 | 27.22 | 0.004 |
| MOBIO | PolyProtect | 91831 | 58.19 | 0.004 |
| MOBIO | PolyProtect | 91843 | 53.47 | 0.004 |
| SCface | IoM-GRP | 91831 | 16.19 | 0.006 |
| SCface | IoM-GRP | 91843 | 34.29 | 0.004 |
| SCface | PolyProtect | 91831 | 5.93 | 0.034 |
| SCface | PolyProtect | 91843 | 5.77 | 0.011 |

All eight contrasts are positive and Holm-significant. This is a second, independent confirmation of the MOBIO pool-4 finding under different key/set seeds (compare 21.25-40.83pp in `scheme_followup_2026-09-18`), and the first multi-seed, statistically corrected confirmation of the same pattern on SCface, which previously only had one-seed pilot evidence.

## Fresh keys remain chance-compatible at every tested exposure count

All **56** `independent_unseen_keys` seed-aggregated endpoints have crossed 95% intervals containing chance: 2 datasets x 2 schemes x 2 splits x 7 model/exposure combinations. The single-at-1/mean-at-2/5/10 subset contains **32** endpoints. This extends coverage to the tested counts 2 and 5; it does not test every integer between 1 and 10, establish equivalence, or prove privacy.

## Pool-8 does not behave like a simple extension of pool-4, and PolyProtect is not monotonic in pool size

Ten-record mean-MLP top-1 by condition (chance-adjusted context: MOBIO 3.33%, SCface 3.85%):

| Dataset | Scheme | Split | Pool 4 | Pool 8 |
|---|---|---:|---:|---:|
| MOBIO | IoM-GRP | 91831 | 91.25% | 68.47% |
| MOBIO | IoM-GRP | 91843 | 90.97% | 72.36% |
| MOBIO | PolyProtect | 91831 | 62.50% | 80.28% |
| MOBIO | PolyProtect | 91843 | 58.06% | 75.42% |
| SCface | IoM-GRP | 91831 | 39.90% | 24.20% |
| SCface | IoM-GRP | 91843 | 63.78% | 35.26% |
| SCface | PolyProtect | 91831 | 10.26% | 49.36% |
| SCface | PolyProtect | 91843 | 10.10% | 57.21% |

IoM-GRP decreases from pool 4 to pool 8 in all four dataset/split cells, consistent with the intuition that a larger recurring pool dilutes per-transform reuse structure. **PolyProtect does the opposite in all four cells: pool-8 leaks more than pool-4**, in one SCface case by a factor of roughly five. This matches the pool-sensitivity already reported in [`pool_replication_2026-09-19`](../pool_replication_2026-09-19/README.md) (three reversals out of twelve pool draws at fixed pool size 4) and the pool-6-vs-7 non-monotonicity already reported for BioHash in `mobio_multiexposure`: pool size alone does not determine leakage for every scheme, and PolyProtect specifically should not be assumed to degrade smoothly or safely as the nominal pool size grows. This run used one pool draw per condition per partition, not multiple independent draws at pool 8, so it cannot separate "pool size 8 is inherently worse for PolyProtect" from "this particular draw of 8 transforms happened to be worse"; both are live explanations.

## Native PolyProtect controls now cover SCface

Three native key seeds (91873/91879/91883) per partition, extending [`norm_native_audit_2026-09-18`](../norm_native_audit_2026-09-18/README.md)'s MOBIO/FEI coverage:

| Dataset | Chance | Native top-1 range | Holm p (family 12) |
|---|---:|---:|---:|
| MOBIO | 3.33% | 10.9-14.5% | 0.006 |
| SCface | 3.85% | 7.2-14.3% | 0.006 |

All six SCface tests exceed their gallery-label permutation null, replicating the earlier single-key-seed SCface pilot finding (10.66%) with three independent keys and a corrected family.

## Files and reproduction

**Source recovery required:** the report-refresh audit found three recorded source hashes unresolved in the current checkout, committed history and earlier source archive. See the [exact paths, hashes and audit method](../../reports/final_research_status.md#provenance-check). Recover the executed versions from the experiment machine before asserting exact reproduction. Aggregates and manifests remain unchanged; passing current tests is not evidence that these missing source versions are identical.

- [results_summary.csv](results_summary.csv): 672 trained endpoints.
- [seed_identity_endpoints.csv](seed_identity_endpoints.csv): 224 endpoint summaries (32 cells x 7 exposure/model combinations) with crossed uncertainty.
- [seed_identity_contrasts.csv](seed_identity_contrasts.csv): 64 ten-minus-one contrasts (32 cells x 2 models); 8 are the corrected primary family, the rest are descriptive.
- [native_null_controls.csv](native_null_controls.csv) and [norm_sensitivity.csv](norm_sensitivity.csv): native PolyProtect controls, now including SCface.
- [execution_manifest.json](execution_manifest.json) and [matrix_status.json](matrix_status.json): completion, timing, frozen-source hashes.

```powershell
python scripts/train/run_scheme_followup.py --config configs/attacks/scheme_followup_2026-09-19_full.yaml
python scripts/train/run_scheme_followup.py --config configs/attacks/scheme_followup_2026-09-19_full.yaml --analyse-only
```

Execution refuses to overwrite an existing freeze. Biometric records, keys, and identity-level scores remain ignored.

## Remaining scope

FEI is not covered at this expanded matrix. No additional protection family beyond IoM-GRP/PolyProtect/BioHash/MLP-Hash was added; the candidate-selection review records the decision not to implement SWG-MinHash. A [separate learned raw-input study](../raw_input_attacker_2026-09-19/README.md) is now complete, without a matched unit arm. Multiple independent pool-8 draws, approved equivalence margins and independent human review remain open. Identity assignments overlap and reuse the same pipeline; this is a sensitivity replication, not an independent population or outside replication.
