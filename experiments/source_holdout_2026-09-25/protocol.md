# Frozen source-analysis holdout protocol

Date: 2026-09-25. Status at freeze: prepared, not executed.

## Purpose and independence

This holdout evaluates the unchanged source analyzer on 24 newly written and
manually labelled programs: 12 with semantic key reuse and 12 with semantically
fresh per-record keys. The labels follow integer and Python semantics rather than
the analyzer output.

The evaluator is separate from Manish, who proposed the algorithm, but inspected
the implementation before constructing these cases. This is therefore an internal,
adversarial, frozen holdout, not a blinded external validation or peer review.

## Freeze and execution

The protocol, labelled cases and evaluation script must be committed before the
first execution. The analyzer, cases, labels and thresholds must not change between
freeze and execution. The evaluator writes a new result directory once and refuses
to overwrite existing output. Source hashes are recorded in the execution manifest.

The corpus has three equal evaluation regions:

- eight fresh cases using constructs intended to be supported;
- eight reuse cases using constructs intended to be supported;
- four fresh and four reuse cases using realistic constructs outside the documented
  subset, including branches, keyword calls, containers, loops and floor division.

No biometric data, model training or source execution is required. The task is
static classification of key provenance at protection sinks.

## Frozen outcomes and gates

`reuse` is a positive finding, `conditional_fresh` is a fresh prediction and
`unknown` is an abstention. An abstention is neither correct nor incorrect.

- Safety gate: zero reuse-labelled cases predicted fresh.
- Selective-accuracy gate: at least 95% correct among non-abstained cases.
- Coverage gate: a decision on at least 75% of all cases.
- Overall gate: all three gates pass.

Report the full result table, abstentions by true label, false-fresh decisions and
false-reuse decisions. Passing these gates would validate only this bounded corpus;
it would not establish general Python soundness, security, novelty or deployment
readiness.
