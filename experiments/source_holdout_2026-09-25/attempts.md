# Execution attempts

## Attempt 1: failed before evaluation

Command: `python scripts/diagnostics/evaluate_source_holdout.py`

The first post-freeze invocation failed while importing
`scripts.diagnostics.source_holdout_cases`: the runner had added `src/`, but not
the repository root, to `sys.path`. No call to `analyse_source` occurred and no
result file was written. The only correction adds the repository root to the import
path. The analyzer, corpus, labels, thresholds and metric logic remain unchanged.

The corrected runner must be committed before attempt 2.
