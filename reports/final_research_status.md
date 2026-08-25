# Final research status

## Research question

Can a key-agnostic learned set model recover identity-discriminative information from multiple independently protected face templates?

## Literature and threat model

See `docs/literature/` and `docs/literature/threat_models.md`. The main future evaluation is unseen identities plus unseen keys; K0 knows only the scheme family and K1 additionally knows hyperparameters.

## Completed infrastructure

- Deterministic BioHash reference, key scope splitting, identity-disjoint synthetic data, single MLP/DeepSets models, metrics, leakage checks, tests, configs, and per-run artifacts.
- Official GaFaR/InsightFace/Arc2Face commits recorded. benchmark_cb source remains unresolved.

## Results

No real-data, published-baseline, FaceLinkGen, cross-scheme, ablation, or statistical result has been run. Every such result is **TODO / not run**. A single CPU synthetic engineering smoke test completed at 1/2/5/10 exposures; it showed no stable leakage trend and has no scientific interpretation. Its untracked artifacts are under `results/reproduced/smoke_test.json`.

## Limitations and next work

Obtain MOBIO authorization and a corrected benchmark_cb source; verify FaceLinkGen details/code; then validate ArcFace/MOBIO before evaluating BioHash. Run multiple seeds only after the real-data protocol and leakage checks are complete.

## Commands

`make test`, `make system-info`, and `make smoke-test` are currently reproducible without datasets. Exact benchmark commands are intentionally withheld until their verified upstream protocol is available.
