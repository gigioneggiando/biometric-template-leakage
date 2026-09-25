# Real protection integration and baseline protocol

Date: 2026-09-25. Status at freeze: prepared, not executed.

## Scope

V3 adds explicit protection-sink contracts for the repository's BioHash, IoM-GRP
and PolyProtect implementations. Six integration recipes execute those actual
implementations under recurring-pool and record-fresh key allocation. The evaluation
also reuses the 20 already frozen v2 confirmation programs as a regression corpus.

The recipes are controlled repository integration code, not externally sourced
applications. IoM-GRP and PolyProtect are paper-specified local implementations,
not recovered author code. The v2 inference rules and prior results remain unchanged.

## Baseline

The comparison baseline is a deliberately simple intraprocedural AST analysis. It
tracks constants, the record argument, local assignments, selected arithmetic and
direct `generate_key` calls within the entry function. It has no helper summaries,
branches, loops, containers or component contracts. It is a transparent engineering
baseline, not a state-of-the-art static-analysis competitor.

## Frozen execution

Commit the v3 analyzer, recipes, baseline, tests, evaluator and this protocol before
execution. The runner refuses to overwrite outputs and records hashes. For v3, the
existing safety, selective-accuracy and coverage gates remain: zero false-fresh,
at least 95% accuracy among decisions and at least 75% coverage. Baseline results
are descriptive and use no pass gate.

Passing does not prove soundness for general Python, security of a protection
scheme, authentication utility, novelty or superiority over specialized tools.
