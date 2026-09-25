# Source-analysis v2 confirmation protocol

Date: 2026-09-25. Status at freeze: prepared, not executed.

This internally authored confirmation contains 20 new valid Python programs, with
ten semantic reuse labels and ten semantic fresh labels. The cases use real API
signatures and differ from the first holdout through new combinations of keyword
binding, local helpers, containers, loops, floor division and projection sinks.

The corpus, labels, evaluator, v2 analyzer and thresholds must be committed before
the first execution. The evaluator refuses to overwrite outputs and records source
hashes. No rule or label may change after results are observed.

Frozen gates:

- zero reuse-labelled cases predicted fresh;
- at least 95% correct among non-abstained cases;
- decisions on at least 75% of all cases;
- all three requirements must pass.

This is a post-implementation holdout, not an externally authored or blinded test:
the same assistant implemented v2, constructed the corpus and executes the test at
the user's request. Passing would provide an additional internal regression check,
not independent proof of general Python soundness, biometric security or novelty.
