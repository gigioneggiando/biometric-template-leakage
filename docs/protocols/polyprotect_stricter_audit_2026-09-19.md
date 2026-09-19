# Stricter PolyProtect selection: native-matching comparison

Protocol written on 2026-09-19 before inspecting any result. This is an unauthorized-budget-free diagnostic run using only already-saved local embeddings (no new dataset acquisition, image re-extraction, or learned-attacker training). Maximum execution budget: 1,800 seconds on local CPU; stop and report incomplete cells rather than silently expanding it.

A timing probe (on a throwaway key not used for the actual audit, before the candidate/pair counts below were fixed) showed that scoring all mated development pairs per candidate is too slow for this host: MOBIO alone would need roughly 1,700 candidate/key-seed record evaluations. `polyprotect_parameters_stricter` was therefore extended with an optional `max_development_pairs` argument that deterministically subsamples mated pairs for scoring; this is a feasibility change made before running the audit, not a result-conditioned one.

## Question

Does `polyprotect_parameters_stricter` (our own operationalization of the PolyProtect paper's Section IV-D score-conditioned selection, implemented and unit-tested on synthetic data on 2026-09-19; see `docs/research_log.md`) reduce native fresh-key protected-gallery matching top-1 relative to the naive random selection (`polyprotect_parameters`) already reported in `experiments/norm_native_audit_2026-09-18` (MOBIO/FEI) and `experiments/scface_scheme_extension_pilot` (SCface)?

## Fixed design

- Datasets: MOBIO and SCface only. FEI embeddings are not present on this host; FEI is explicitly out of scope for this run, not a null result.
- Single frozen identity split per dataset, taken directly from the saved embedding metadata (MOBIO 90/30/30; SCface 78/26/26). No new identity reassignment.
- Development set: training-split embeddings and identity labels only, used exclusively for `polyprotect_parameters_stricter` candidate search (`candidates=20`, `unlinkable_band=0.5` function default, `max_development_pairs=200`). The development set never contributes to the evaluation gallery or probes, and vice versa.
- Evaluation: held-out gallery/probe protocol from `scripts/diagnostics/run_norm_native_audit.py` (`gallery_protocol`, `native_confusion`, `identity_interval`, `signflip`), reused unchanged to avoid a second, independently-bugged scoring path.
- Config: `PolyProtectConfig()` defaults (input_dim 512, window_size 5, overlap 2, coefficient_bound 50), matching all prior PolyProtect studies.
- Keys: three independent fresh key seeds per dataset, 92003/92011/92017, not reused from any earlier study. For each key seed and each arm (`naive`, `stricter`), generate one parameter set and protect the test-split embeddings; average the three key-seed confusion matrices before testing, matching the existing native-audit convention.

## Analysis, fixed before inspection

Reuses `gallery_protocol`, `native_confusion`, `identity_interval`, and `signflip` from `scripts/diagnostics/run_norm_native_audit.py` unchanged, including their built-in analysis seed 91903, 4,999 gallery-label permutations, and 4,000 identity-bootstrap resamples. This is the same analysis machinery as the existing native audit, applied to a new comparison, not a re-derivation.

- Primary family (4 tests): naive and stricter identity-balanced top-1 against a gallery-label permutation null, for MOBIO and SCface. Holm-adjust within this family of 4.
- Paired family (2 tests): stricter-minus-naive top-1 difference per dataset, with a 95% identity-bootstrap interval and a two-sided identity sign-flip test. Holm-adjust within this family of 2.
- A negative (stricter is not lower, or the paired interval includes zero) is reported as designed, not treated as a bug or omitted.

## Scope and limits, stated in advance

This does not evaluate FEI, does not use multiple identity partitions, does not retrain a learned attacker on raw or protected inputs, and does not establish why any observed difference occurs. It measures one operationalization of one qualitative paper description against the existing naive baseline, on two datasets, one split each. It is not a reproduction of the PolyProtect paper's own reported unlinkability improvement, which used different embeddings (Facenet/Idiap, 128-D) and its own exact scoring/selection procedure. Private per-identity scores and embeddings stay local and ignored; only compact aggregates are tracked.
