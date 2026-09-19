# Stricter PolyProtect selection: native-matching comparison

Status: **COMPLETED NEGATIVE FINDING; NOT A CONFIRMATION OF ANY IMPROVEMENT**.

[Protocol](../../docs/protocols/polyprotect_stricter_audit_2026-09-19.md) frozen before execution. Runtime 729.04 seconds on CPU, base commit `6ccad8d` (dirty worktree: the new `max_development_pairs` argument and this script were added after that commit and are recorded in the execution manifest's source hashes). MOBIO and SCface only; FEI embeddings are not present on this host.

## What was tested

`polyprotect_parameters_stricter` (added 2026-09-19; see `docs/research_log.md`) is our own operationalization of the PolyProtect paper's Section IV-D qualitative selection criterion: among 20 candidate `(C, E)` parameter draws per record, keep the one minimizing the mean amount by which mated (genuine-pair) cosine scores on a 200-pair development-set subsample fall outside `[-0.5, 0.5]`. The development set is the training-split identities only, disjoint from the test-split gallery/probes used for evaluation.

For each dataset, three independent fresh key seeds (92003/92011/92017) protected the test-split embeddings under both the existing naive selection (`polyprotect_parameters`) and this stricter selection, then compared native fresh-key protected-gallery matching top-1 using the same held-out gallery/probe protocol, permutation null, and identity-bootstrap machinery already used in `experiments/norm_native_audit_2026-09-18` (reused unchanged).

## Result

| Dataset | Chance | Naive top-1 | Stricter top-1 | Stricter minus naive [95% interval], pp | Holm p (paired, family 2) |
|---|---:|---:|---:|---|---:|
| MOBIO | 3.33% | 13.13% | 16.26% | +3.13 [0.10, 6.16] | 0.1344 |
| SCface | 3.85% | 10.44% | 10.12% | -0.32 [-2.19, 1.47] | 0.7556 |

Both naive and stricter arms exceed their gallery-label permutation null on both datasets (Holm p = 0.0008, family of 4): the naive residual leakage already reported in `norm_native_audit_2026-09-18` and `scface_scheme_extension_pilot` is reproduced here under new key seeds. The stricter-minus-naive paired contrast does **not** show a reduction: it is directionally worse on MOBIO (not significant after Holm correction) and negligible on SCface (clearly not significant). No implementation error was found: matcher cross-checks against an independent scalar reference match to float precision (~1e-16), with zero prediction disagreements, ties, or gallery/probe overlap (`implementation_audit.csv`).

## Interpretation

This operationalization of the paper's stricter selection does not reduce native leakage in this construction, on these two datasets, with 20 candidates and a 200-pair development subsample. Plausible, untested explanations: the paper's own criterion may not be well approximated by minimizing mean out-of-band mated-score mass (a different statistic, e.g. minimizing the maximum mated |score|, might behave differently); 20 candidates or 200 development pairs may be too few to find a materially better parameter set; 512-D ArcFace embeddings may not exhibit the same score-clustering pathology as the paper's 128-D Facenet/Idiap embeddings; or native residual leakage on this dataset may not be governed primarily by the score-extremeness mechanism the paper targets. This audit does not distinguish between these explanations and does not establish that no stricter selection procedure could help.

This is a single run at fixed hyperparameters, not a sweep over `candidates`, `max_development_pairs`, or `unlinkable_band`; a genuine refutation of the approach would need that sweep plus FEI coverage. The finding is reported as designed, not omitted or reframed as a partial success.

## Files

- [native_comparison.csv](native_comparison.csv): per-dataset/arm top-1, intervals, permutation-null tests.
- [paired_contrasts.csv](paired_contrasts.csv): stricter-minus-naive paired contrasts.
- [implementation_audit.csv](implementation_audit.csv): per-key-seed matcher cross-checks.
- [execution_manifest.json](execution_manifest.json): base commit, dirty-worktree flag, source hashes, timing.

Reproduce with `python scripts/diagnostics/run_polyprotect_stricter_audit.py` (refuses to overwrite an existing freeze). Requires local MOBIO/SCface embeddings; private per-record data stays ignored.
