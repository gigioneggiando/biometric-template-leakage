# Learned raw-input attacker

Status: **COMPLETED; FRESH-KEY NULL HOLDS, POOL-4 AMPLIFICATION DOES NOT TRANSFER TO RAW INPUT**.

[Protocol](../../docs/protocols/raw_input_attacker_2026-09-19.md) frozen before execution. Runtime 775.48 seconds on CPU. MOBIO and SCface only (FEI not present on this host); one identity partition per dataset (the existing saved split, no reassignment); PolyProtect (scale-sensitive) and IoM-GRP (scale-invariant control).

## What was tested

Raw (pre-normalization) 512-D ArcFace vectors were re-extracted directly from source images for every MOBIO and SCface record, reusing `extract_raw` from `norm_native_audit_2026-09-18` unchanged, including its check that `raw / ||raw||` matches the saved unit embedding (max abs error <= 1e-4). Norm ranges reproduce that earlier audit exactly: MOBIO 15.00-28.53, SCface 11.22-32.94. These raw vectors, not the unit-normalized ones, were then fed through the existing key-blind attacker pipeline (`run_real_multiexposure.run()`, called directly rather than through `run_pilots`, which asserts unit-normalized input and was not weakened) under fresh keys and pool-4 reuse, at exposures 1 and 10, three model seeds.

## Result

| Dataset | Scheme | Condition | Exposures | Model | Chance | Raw-input top-1 |
|---|---|---|---:|---|---:|---:|
| MOBIO | PolyProtect | fresh | 10 | mean_mlp | 3.33% | 3.61% |
| MOBIO | PolyProtect | pool-4 | 10 | mean_mlp | 3.33% | 3.61% |
| MOBIO | IoM-GRP | fresh | 10 | mean_mlp | 3.33% | 3.33% |
| MOBIO | IoM-GRP | pool-4 | 10 | mean_mlp | 3.33% | 91.11% |
| SCface | PolyProtect | fresh | 10 | mean_mlp | 3.85% | 3.69% |
| SCface | PolyProtect | pool-4 | 10 | mean_mlp | 3.85% | 3.85% |
| SCface | IoM-GRP | fresh | 10 | mean_mlp | 3.85% | 3.85% |
| SCface | IoM-GRP | pool-4 | 10 | mean_mlp | 3.85% | 67.63% |

Full per-exposure/model results are in [raw_input_results.csv](raw_input_results.csv).

**Fresh keys remain chance-compatible for raw input, for both schemes, on both datasets.** This is descriptive (three-seed mean/std, not a bootstrap interval or corrected test, per the protocol's stated scope), but every fresh-key mean sits within about one point of chance with no consistent direction. Raw, non-unit-normalized input does not break the fresh-key null in this pilot.

**IoM-GRP pool-4 amplification is essentially unchanged by raw input** (compare 91.11%/67.63% here to 90.97-91.25%/39.90-63.78% for unit input in `scheme_followup_2026-09-19_full`, same order of magnitude), exactly as expected for a scheme already proven scale-invariant at the code level (`scale_invariance.csv`). This is a useful positive control: the pipeline substitution (raw embeddings fed through the unmodified attacker/training code) behaves correctly.

**PolyProtect pool-4 amplification, which is large under unit-normalized input (53-62% ten-record top-1 in `scheme_followup_2026-09-19_full`), is essentially absent under raw input**: every raw-input PolyProtect pool-4 endpoint here is within a couple of points of chance (3.6-4.7%), with seed standard deviations comparable to the means, i.e. no consistent signal across seeds. Raw, per-record magnitude variation did not help this learned attacker exploit the recurring-transform structure; if anything it appears to swamp it.

## Interpretation

This does not establish that raw input is safer in general. One plausible mechanism, not tested directly here: PolyProtect's output is a degree-1-to-5 polynomial in the input coordinates, so per-record norm variation (roughly 15-33 here) propagates into a large, identity-irrelevant scale variation across protected templates (a ratio of the norm extremes raised to the fifth power is several orders of magnitude). That variation may dominate the numerical range the attacker has to learn from, making the shared coefficients underlying pool-4 reuse harder to detect, even though they are unchanged. This is a candidate explanation, not a demonstrated one; distinguishing it from other explanations (e.g. optimization difficulty from the wider output range) is future work.

Both scientifically important results here are `null`/`no-effect` findings, not detections. Neither is a bootstrap-corrected test; both are three-seed descriptive means read against the same chance baseline and gallery protocol used everywhere else in this project. A single identity partition per dataset, only two conditions and two exposure levels, and no FEI coverage all limit generality.

## Files

- [raw_input_results.csv](raw_input_results.csv): 24 endpoint rows (2 datasets x 2 schemes x 2 conditions x 3 exposure/model combinations).
- [execution_manifest.json](execution_manifest.json): base commit, dirty-worktree flag, source hashes, timing, raw-extraction audit.

Reproduce with `python scripts/diagnostics/run_raw_input_attacker.py` (refuses to overwrite an existing freeze). Requires local MOBIO/SCface source images and hash-verified models; raw embeddings and per-record data stay in ignored `results/` and `data/processed/`, never Git-tracked.
