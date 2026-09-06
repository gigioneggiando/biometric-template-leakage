# MOBIO fresh-key and correlated-key controls

Status: **COMPLETED EXPLORATORY CONTROLS; NOT A PAPER REPRODUCTION**.

These controls were preregistered in `docs/protocols/multi_exposure.md` before their results were inspected. They use MOBIO selected still images, identity-disjoint 90/30/30 splits, one held-out gallery image per identity, eight attack sets per identity, 128-bit sign-corrected Haar BioHash, and three deterministic model seeds. Top-1 chance is `3.33%` over 30 test identities. Full metrics remain local under `results/`.

## Same image under different fresh keys

The paired baseline uses different images of the same identity. The control repeats the exact same normalized ArcFace embedding under ten distinct fresh, split-disjoint keys.

| exposure construction | 1-record top-1 | 10-record top-1 | amplification | 10-record AUROC |
|---|---:|---:|---:|---:|
| different images, fresh keys | 3.33% | 3.33% | 0.00 pp | 0.4964 |
| same image, different fresh keys | 3.19% | 3.33% | +0.14 pp | 0.4997 |

Every 10-record seed was exactly at chance in both conditions. The fresh-key null is therefore not caused by session or image variation obscuring a signal: even ten protected versions of the identical source embedding contain no detected linkage information under independent hidden Haar keys.

## Coarse correlated-key sweep

Each record keeps a private key, but its BioHash projection shares an exact system-wide prefix of projection columns. Private columns are projected into the orthogonal complement and re-orthonormalized. This is a controlled model of partial projection reuse, not a claim about a standard key-derivation implementation.

| shared dimensions | shared fraction | 1-record top-1 | 10-record top-1 | amplification | 10-record AUROC |
|---:|---:|---:|---:|---:|---:|
| 0/128 | 0% | 3.33% | 3.33% | 0.00 pp | 0.5008 |
| 32/128 | 25% | 3.33% | 9.44% | +6.11 pp | 0.6927 |
| 64/128 | 50% | 39.17% | 46.39% | +7.22 pp | 0.9312 |
| 96/128 | 75% | 50.83% | 61.11% | +10.28 pp | 0.9560 |
| 128/128 | 100% | 69.17% | 71.67% | +2.50 pp | 0.9678 |

The 25% point was suggestive but unstable: seed top-1 values were `6.67/15.00/6.67%`, and two of three clustered intervals included zero. This observation motivated the separately preregistered fine sweep on a new identity partition.

## Fine correlated-key sweep

| shared dimensions | shared fraction | 1-record top-1 | 10-record top-1 | seed top-1 | 10-record AUROC |
|---:|---:|---:|---:|---|---:|
| 0/128 | 0% | 3.06% | 3.33% | 3.33 / 3.33 / 3.33% | 0.5026 |
| 16/128 | 12.5% | 3.19% | 3.75% | 4.58 / 3.33 / 3.33% | 0.5317 |
| 24/128 | 18.75% | 3.47% | 6.94% | 3.33 / 6.67 / 10.83% | 0.5742 |
| 32/128 | 25% | 4.17% | 7.64% | 3.33 / 3.33 / 16.25% | 0.6006 |
| 40/128 | 31.25% | 5.14% | 14.17% | 6.67 / 29.17 / 6.67% | 0.6560 |
| 48/128 | 37.5% | 28.19% | 35.83% | 33.75 / 35.42 / 38.33% | 0.8459 |
| 56/128 | 43.75% | 35.42% | 49.31% | 42.08 / 53.75 / 52.08% | 0.8765 |
| 64/128 | 50% | 35.00% | 42.64% | 40.00 / 44.17 / 43.75% | 0.8848 |

The independent split confirms a graded relationship between projection correlation and leakage. Results are near chance through 12.5%, weak and seed-sensitive from 18.75% to 31.25%, and consistently large from 37.5% onward. The exact transition is not established: there are only 30 test identities, points near the transition have high seed variance, and the 43.75%/50% ordering is non-monotonic. The defensible result is a correlation-dependent leakage regime, not a universal percentage threshold.

Reproduce with:

```powershell
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\mobio_same_image_fresh_baseline.yaml
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\mobio_same_image_fresh_control.yaml
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\mobio_correlated_key_sweep.yaml
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\mobio_correlated_key_fine_sweep.yaml
```
