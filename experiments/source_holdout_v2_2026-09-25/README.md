# Source-analysis v2: development evaluation

Completed 2026-09-25 against commit `16c9c47`. This evaluates v2 on the already
observed and audited v1 holdout, so it is a development result, not an unseen
confirmation.

## Result

| Measure | V1 audited | V2 | V2 gate |
|---|---:|---:|---:|
| Semantically valid cases | 23 | 23 | Fixed |
| Decisions | 16 | 22 | - |
| Abstentions | 7 | 1 | - |
| Coverage | 69.57% | 95.65% | **Pass**: >=75% |
| Selective accuracy | 100% | 100% | **Pass**: >=95% |
| False-fresh decisions | 0 | 0 | **Pass** |
| Overall gate | Fail | Pass | All gates required |

V2 adds conservative support for real keyword binding, self-subtraction, integer
floor-division reuse, literal sequence/dictionary selection, finite literal loops
and branch joins. The remaining valid abstention has two path-local injective key
derivations. V2 does not assume their combined output is injective without a proof
that the path ranges or KDF domains are disjoint.

The invalid v1 keyword case remains excluded according to the frozen-study
[erratum](../source_holdout_2026-09-25/errata.md). Machine-readable results are in
[results.csv](results.csv), [summary.json](summary.json), [details.json](details.json)
and [execution_manifest.json](execution_manifest.json).

These results show improved bounded-language coverage without an observed loss of
soundness on this development corpus. They do not establish general Python
soundness, unseen generalization, biometric utility, novelty or deployment security.
