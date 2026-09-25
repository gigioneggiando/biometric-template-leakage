# Frozen source-analysis holdout: results

Completed 2026-09-25 against commit `f4785d6`, after the cases, labels, thresholds
and corrected runner had been committed. The [protocol](protocol.md) defines the
scope and gates; [attempts.md](attempts.md) records the pre-evaluation import failure.

## Result

| Measure | Result | Gate |
|---|---:|---:|
| Labelled cases | 24: 12 reuse, 12 fresh | Fixed |
| Decisions | 16 | - |
| Abstentions | 8 | - |
| Coverage | 66.67% | **Fail**: required at least 75% |
| Correct decided cases | 16/16 | **Pass**: 100% >= 95% |
| Reuse cases predicted fresh | 0 | **Pass** |
| Overall gate | Failed | All three gates required |

All eight cases built only from the documented supported fresh constructs were
classified fresh. All eight supported reuse cases were detected. The analyzer
abstained on all eight deliberately realistic unsupported cases: four fresh and
four reuse. It produced no false-fresh or false-reuse decision.

## Interpretation

The v1 analyzer is conservative and accurate on this bounded holdout when it emits
a decision. It is not yet sufficiently complete for the frozen practical-coverage
target. The next version should improve branch handling first, then keyword argument
binding, simple container selection, bounded loops and integer-division reasoning.
The v1 result and failed coverage gate must remain unchanged when v2 is developed.

This is an internal holdout prepared by an evaluator other than Manish, but after
inspection of the implementation. It is stronger than rerunning the original
same-author examples, but is not blinded external validation or evidence of general
Python soundness, biometric security, novelty or deployment readiness.

Machine-readable outputs are [results.csv](results.csv), [summary.json](summary.json),
[details.json](details.json) and [execution_manifest.json](execution_manifest.json).
