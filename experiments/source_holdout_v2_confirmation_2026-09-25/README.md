# Source-analysis v2: frozen confirmation results

Completed 2026-09-25 against commit `eb5aa74`, after the 20 new programs, labels,
thresholds, evaluator and analyzer had been committed.

| Measure | Result | Gate |
|---|---:|---:|
| Cases | 20: 10 reuse, 10 fresh | Fixed |
| Decisions | 19 | - |
| Abstentions | 1 | - |
| Coverage | 95% | **Pass**: >=75% |
| Selective accuracy | 19/19, 100% | **Pass**: >=95% |
| False-fresh decisions | 0 | **Pass** |
| Overall gate | **Pass** | All three gates required |

All ten reuse cases were detected. Nine fresh cases were classified fresh. V2
abstained on `fresh_floor_identity`: floor division by one is semantically the
identity, but v2 does not currently encode that special case. The analyzer was not
changed after observing this result.

This strengthens the internal evidence that v2 improves language coverage while
remaining fail-closed on the tested programs. The same assistant implemented v2,
wrote the post-implementation corpus and executed it, so this is not an externally
authored, blinded or peer-reviewed validation. It does not prove general Python
soundness, biometric security, authentication utility, novelty or deployment
readiness.

See the frozen [protocol](protocol.md), [results.csv](results.csv),
[summary.json](summary.json), [details.json](details.json) and
[execution_manifest.json](execution_manifest.json).
