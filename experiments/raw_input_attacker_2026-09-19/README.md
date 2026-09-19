# Learned raw-input attacker

Status: **COMPLETED; DESCRIPTIVE NEAR-CHANCE POLYPROTECT AND STRONG IOM POOL-4 LINKAGE**.

**Interpretation correction, report refresh:** this run has no matched unit-input arm. It changes key/set seeds and identity assignments relative to the extended unit study. The unchanged runner also averages raw source vectors for training targets, weighting larger norms more strongly before target normalization. Thus cross-study differences cannot be attributed solely to input normalization; IoM code-level invariance does not guarantee identical learned results. Fresh-key means are near chance descriptively, not a corrected null or equivalence conclusion. The frozen tables and execution records are unchanged.

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

**IoM-GRP retains strong pool-4 linkage in this raw-input run:** 91.11%/67.63%. This is consistent with its scale-invariant codes, but the comparison with unit-input studies is not paired, and raw target weighting changes. Neither unchanged learned performance nor correct operation of every pipeline component follows from high accuracy alone.

**PolyProtect has no positive mean-pooling gain in this raw-input run:** ten-record mean top-1 is 3.61%/3.85%, versus one-record 4.72%/5.77% on MOBIO/SCface. All raw pool-4 endpoints lie between 3.61% and 5.77%. This is a descriptive failure setting. The extended unit study has MOBIO mean top-1 58.06-62.50% but SCface 10.10-10.26%, not a universal 53-62% range. Different pools, assignments, targets and input scales prevent isolating which change explains the difference.

## Interpretation

This does not establish that raw input is safer in general. One plausible mechanism, not tested directly here: PolyProtect's output is a degree-1-to-5 polynomial in the input coordinates, so per-record norm variation (roughly 15-33 here) propagates into a large, identity-irrelevant scale variation across protected templates (a ratio of the norm extremes raised to the fifth power is several orders of magnitude). That variation may dominate the numerical range the attacker has to learn from, making the shared coefficients underlying pool-4 reuse harder to detect, even though they are unchanged. This is a candidate explanation, not a demonstrated one; distinguishing it from other explanations (e.g. optimization difficulty from the wider output range) is future work.

Both scientifically important results here are `null`/`no-effect` findings, not detections. Neither is a bootstrap-corrected test; both are three-seed descriptive means read against the same chance baseline and gallery protocol used everywhere else in this project. A single identity partition per dataset, only two conditions and two exposure levels, and no FEI coverage all limit generality.

## Files

- [raw_input_results.csv](raw_input_results.csv): 24 endpoint rows (2 datasets x 2 schemes x 2 conditions x 3 exposure/model combinations).
- [execution_manifest.json](execution_manifest.json): base commit, dirty-worktree flag, source hashes, timing, raw-extraction audit.

Reproduce with `python scripts/diagnostics/run_raw_input_attacker.py` (refuses to overwrite an existing freeze). Requires local MOBIO/SCface source images and hash-verified models; raw embeddings and per-record data stay in ignored `results/` and `data/processed/`, never Git-tracked.
