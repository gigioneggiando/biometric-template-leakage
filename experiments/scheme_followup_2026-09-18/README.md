# Multi-seed, multi-partition scheme follow-up

**Completed: 2026-09-18.** All 24 planned cells and 216 model endpoints completed in **859.63 seconds total** on CPU (8 Torch threads), including controls and analysis, within the authorized one-hour budget. This is a bounded independent validation study, separate from the earlier one-seed pilots. It is not the full cross-dataset roadmap.

## Design and provenance

MOBIO and FEI; IoM-GRP and PolyProtect; identity reassignments 91831/91843; model seeds 601/607/613. Fresh, shared (pool 1), and pool-4 conditions use key seed 91861 and set seed 91867. One-record single MLP, ten-record mean MLP and DeepSets share 120-epoch caps, patience 30 and the original optimizer/loss. Eight nested sets per identity preserve pairing; source targets are normalized means of the exposed embeddings, not gallery embeddings.

The [protocol](../../docs/protocols/scheme_followup_2026-09-18.md) and [configuration](../../configs/attacks/scheme_followup_2026-09-18.yaml) were written before execution. The [execution manifest](execution_manifest.json) records base commit `4352eeb`, dirty-worktree status, UTC timestamps and SHA-256 hashes of 32 source/configuration/protocol files. No new Git commit was created. All 32 hashes were verified unchanged after execution. The exact source snapshots must be retained with this result package for reproduction.

## Primary result

Pool-4 mean-MLP ten-minus-one-record top-1 gains, in percentage points:

| Dataset | Scheme | Identity split | Gain | Crossed-bootstrap 95% interval | Holm p |
|---|---|---:|---:|---|---:|
| FEI | IoM-GRP | 91831 | 28.23 | [20.31, 36.26] | 0.004 |
| FEI | IoM-GRP | 91843 | 25.83 | [18.75, 33.65] | 0.004 |
| FEI | PolyProtect | 91831 | 23.96 | [14.27, 33.44] | 0.004 |
| FEI | PolyProtect | 91843 | 21.35 | [10.21, 31.46] | 0.004 |
| MOBIO | IoM-GRP | 91831 | 37.36 | [26.67, 48.19] | 0.004 |
| MOBIO | IoM-GRP | 91843 | 40.83 | [31.39, 49.72] | 0.004 |
| MOBIO | PolyProtect | 91831 | 21.25 | [8.05, 33.34] | 0.004 |
| MOBIO | PolyProtect | 91843 | 29.31 | [8.61, 47.50] | 0.004 |

All eight planned primary contrasts support positive amplification. Intervals independently resample model seeds and identity clusters within each partition (2,000 draws). One-sided identity sign-flip tests use seed-averaged paired differences, 1,999 permutations and Holm correction over eight hypotheses. These tests condition on the trained seed ensemble and assume null sign exchangeability; the intervals and tests are not interchangeable. Model-seed SD is exported separately. The two identity assignments overlap and are sensitivity checks, not independent populations.

Fresh-key learned endpoints remain chance-compatible: every crossed 95% interval includes the dataset chance rate. That does not establish equivalence. No scientific equivalence margin was approved or selected from the new results. The existing +/-1/2/5-point sensitivity output is descriptive, not an equivalence conclusion.

## Native matching and radial stress

Fresh PolyProtect protected-gallery matching was repeated with three independent key seeds per dataset/identity partition (12 tests). Identity-balanced top-1 is **10.91-14.55% on MOBIO** versus 3.33% chance and **10.11-11.64% on FEI** versus 2.50% chance. Every gallery-label permutation test has Holm-adjusted **p = 0.006** across the planned family of 12; each unadjusted p reaches the Monte Carlo resolution of 0.0005. Gallery-label permutations preserve probe clusters; identity-bootstrap intervals and probe-weighted top-1 are reported alongside the primary identity-balanced endpoint. This verifies the earlier native discrepancy under the tested protocol, not a learned reconstruction result or a causal explanation.

Positive scales 0.5 and 2 were applied to 32 held-out unit embeddings per dataset/partition with fixed keys. IoM-GRP outputs are exactly unchanged. PolyProtect relative template L2 change is 0.510-0.524 at scale 0.5 and 1.110-1.235 at scale 2; mean template cosine remains 0.993-0.996 and 0.988-0.989, respectively. This is synthetic radial sensitivity, not proof of natural norm leakage, a norm-based identity attack, or an explanation of native linkage.

## Files and reproduction

- [results_summary.csv](results_summary.csv): 216 trained endpoints, code/configuration references, model seeds and partition labels.
- [seed_identity_endpoints.csv](seed_identity_endpoints.csv): 72 endpoint summaries with model-seed SD and crossed uncertainty.
- [seed_identity_contrasts.csv](seed_identity_contrasts.csv): paired gains, crossed intervals and corrected primary tests.
- [paired_uncertainty.csv](paired_uncertainty.csv): per-model paired identity intervals; `seed` is the trained-model seed and `bootstrap_seed` is separate.
- [native_null_controls.csv](native_null_controls.csv) and [norm_sensitivity.csv](norm_sensitivity.csv): targeted controls.
- [native_utility.csv](native_utility.csv) and [equivalence_sensitivity.csv](equivalence_sensitivity.csv): standard runner diagnostics.
- [matrix_status.json](matrix_status.json) and [execution_manifest.json](execution_manifest.json): completion, timing and frozen-source hashes.
- [coverage_audit.csv](coverage_audit.csv): 15 key-pool/scheme source groups; not every historical control or single-template study.

```powershell
python scripts/train/run_scheme_followup.py
python scripts/train/run_scheme_followup.py --analyse-only
python scripts/figures/build_run_matrix.py --audit-out experiments/scheme_followup_2026-09-18/coverage_audit.csv
```

Execution refuses to overwrite an existing freeze; analysis can be regenerated from private saved metrics. Biometric records, keys and identity-level scores remain ignored. The local inventory now has **849 rows from 49 artifacts**; all previous 633 rows were preserved exactly. Two earliest MOBIO key-pool sources have legacy detailed schemas not represented in that inventory; SCface key-pool and scheme detailed artifacts are unavailable locally. Their tracked aggregate results remain in the figures.

## Remaining scope

No new SCface/LFW training, 2/5-record exposure sweep, pool-8 follow-up, further protection families, natural non-normalized extraction or independent human review was performed. Training key/set seeds remain fixed; the three fresh-key seeds apply to native controls only. The full roadmap, approved equivalence analysis, independent theorem/novelty review and venue requirements therefore remain outside the completed experiment. These administrative decisions are kept out of the findings presentation, not marked as completed.