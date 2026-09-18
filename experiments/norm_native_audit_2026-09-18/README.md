# Raw-norm and native-matching audit

Completed 18 September 2026 in **254.157 seconds**, within a frozen 3,600-second CPU cap. Base commit `15e4384`; dirty state and executed source/config/protocol hashes are in [execution_manifest.json](execution_manifest.json). Separate computational audit, not independent human review or source-exact reproduction.

## Design and checks

[Prospective protocol](../../docs/protocols/norm_native_audit_2026-09-18.md): same ArcFace/YuNet pipeline, MOBIO/FEI, two assignments, three fresh-key seeds, four matched PolyProtect arms: unit, genuine raw output, within-split shuffled norms, common training-median radius. Keys are identical across arms. No learned raw-input attacker was retrained.

All **4,177** images were re-extracted without exclusions. Re-normalized outputs reproduce saved embeddings within **2.98e-8** maximum absolute error. Raw norm ranges: MOBIO 15.00-28.53 (median 23.09); FEI 17.44-25.97 (median 21.48). Raw arrays, identities and paths remain private.

All 48 implementation cells match a separate scalar polynomial calculation exactly after float32 casting. Matrix/SciPy cosine scores differ by at most 1.33e-15: zero prediction disagreements, reversed-gallery changes, ties or gallery/probe overlap. Every held-out record has a unique fresh key. Unit results reproduce earlier three-key averages. Explicit grouped-dot tests check IoM-GRP; sampled natural unit/raw comparisons change zero of 38,400 codes.

## Native results

Identity-balanced top-1 (%); A/B are overlapping splits 91831/91843, not independent cohorts.

| Dataset / split | Unit | Raw | Shuffled norms | Fixed radius | Chance |
|---|---:|---:|---:|---:|---:|
| MOBIO A | 12.42 | 16.46 | 17.07 | 17.17 | 3.33 |
| MOBIO B | 12.20 | 16.66 | 16.05 | 16.45 | 3.33 |
| FEI A | 11.12 | 15.58 | 15.49 | 16.03 | 2.50 |
| FEI B | 11.09 | 16.01 | 16.16 | 16.23 | 2.50 |

All 16 endpoints exceed gallery-label nulls (Holm p = 0.0032, family 16). Tests average three fixed key-seed confusion matrices before testing; 95% identity-bootstrap intervals condition on that ensemble, not a key population. Earlier 12 separate-key tests (Holm p = 0.006) remain unchanged.

Raw-unit gains: MOBIO 4.04/4.45 points, FEI 4.46/4.92. Two-sided paired sign-flips, Holm family 8: p = 0.1380/0.1032 and 0.0160/0.0168. **Only FEI survives correction.** Raw-shuffled differences span -0.61 to +0.61 points; every interval includes zero, adjusted p >= 0.7584. This shows scale sensitivity, **not demonstrated identity-specific norm leakage**, nor equivalence. Shuffling disrupts quality associations as well as identity associations.

Raw norm-only nearest-gallery matching is an **oracle**, not extraction from protected templates; none of four tests survives correction. Fixed radius retains approximately raw-arm performance. Unit-input median nonlinear residual is 0.072-0.085 of full template norm; linear-only native top-1 is 10.70-12.53%. This is a mechanism clue, not proof of a complete explanation. PolyProtect already reports residual naive-parameter linkage; its stricter parameter policy is not tested here.

## Complete follow-up failure analysis

All **48** one-to-ten contrasts from 216 trained endpoints have crossed model-seed/identity 95% intervals, seed ranges, leave-one-seed-out gains and two-sided sign-flips. This **post-hoc family 48** does not replace original primary family 8.

- Eight pool-4 mean gains remain significant (Holm p = 0.0192), positive for every seed and leave-one-seed-out mean (minimum 17.71 points).
- No pool-4 DeepSets gain survives this family (minimum p = 0.0576); this does not establish inability to help.
- Four shared-key PolyProtect DeepSets contrasts are negative, -15.42 to -24.86 points (Holm p = 0.0192). More records are not universally better. Optimization/aggregation explanations are untested.
- Fresh contrasts are nonsignificant, not evidence of privacy. Pointwise bootstrap intervals are not simultaneous and need not agree with corrected tests.

## Artifacts

| File | Rows | Purpose |
|---|---:|---|
| [extraction_audit.csv](extraction_audit.csv) | 2 | Extraction agreement/ranges/hashes |
| [implementation_audit.csv](implementation_audit.csv) | 48 | Formula, matcher, keys, gallery |
| [native_norm_controls.csv](native_norm_controls.csv) | 16 | Arms, intervals, corrected nulls |
| [paired_norm_contrasts.csv](paired_norm_contrasts.csv) | 8 | Paired raw-unit/raw-shuffled |
| [norm_only_linkage.csv](norm_only_linkage.csv) | 4 | Source-norm oracle |
| [scale_invariance.csv](scale_invariance.csv) | 4 | Sampled IoM check |
| [failure_analysis.csv](failure_analysis.csv) | 48 | All follow-up contrasts |

Command: `.venv\Scripts\python.exe scripts/diagnostics/run_norm_native_audit.py`. Refuses to overwrite a completed manifest. Requires authorized local images/models and private follow-up metrics. These **130 audit rows are not new trained endpoints**, and remain separate from the 849-row inventory. Historical inference without paired scores, raw-input learned retraining, stricter PolyProtect policy, other encoders/datasets and human review remain outside this audit.