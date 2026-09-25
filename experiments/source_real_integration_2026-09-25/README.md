# V3 real-protection integration and baseline results

Completed 2026-09-25 against commit `4a3d71b`, after the analyzer, executable
recipes, baseline, evaluator and protocol were committed.

## Results

| Analyzer | Decisions | Correct | Abstentions | Coverage | Selective accuracy | False fresh |
|---|---:|---:|---:|---:|---:|---:|
| Source analysis v3 | 25/26 | 25 | 1 | 96.15% | 100% | 0 |
| Intraprocedural baseline | 6/26 | 5 | 20 | 23.08% | 83.33% | 0 |

V3 passes all frozen gates. It correctly classifies recurring and fresh executable
integration recipes for each repository scheme:

| Scheme | Recurring pool | Record-fresh |
|---|---|---|
| BioHash | Reuse detected | Conditional fresh |
| IoM-GRP | Reuse detected | Conditional fresh |
| PolyProtect | Reuse detected | Conditional fresh |

The recipes import and execute the actual local protection functions; unit tests
also verify their output shapes. V3 follows the key through the shared helper and
records the protection sink and call trace. The local baseline cannot cross that
helper, so it abstains on all six recipes. On the frozen regression cases it also
misclassifies floor division by one as reuse. This is a useful sanity baseline,
not a state-of-the-art competitor.

The single v3 abstention is the already recorded floor-division-by-one case. V3 was
not changed after observing it. The six recipes are controlled project integration
code, not independent third-party applications, and local IoM-GRP/PolyProtect are
paper-specified implementations rather than recovered author code.

See the frozen [protocol](protocol.md), [results.csv](results.csv),
[summary.json](summary.json), [details.json](details.json) and
[execution_manifest.json](execution_manifest.json).
