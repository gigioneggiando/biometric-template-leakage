# Cross-branch freshness repair and provenance verification

Completed 2026-09-26. This is an internal engineering correction and regression
check, not independent validation or a new biometric experiment.

## Defect and correction

The v2 branch handler visited protection calls separately in each branch. Its
conservative join of returned values did not invalidate already recorded fresh
sink summaries. V3 inherits this handler. For a key index that is `record_id`
on the odd branch and `record_id + 1` on the even branch, eight records share
four actual derived keys. Both analyzers previously returned `conditional_fresh`,
`complete=True`, with no warnings. Distinctness inside each path is insufficient
to establish distinctness across paths.

The current handler marks branch-local protection calls as unsupported for
cross-path key reasoning. It also warns on branch predicates containing calls
or other unsupported execution, rather than silently ignoring them. These warnings
prevent a conditional-fresh verdict. Existing reuse findings remain `reuse` with
`complete=False`; all callers must inspect completeness and findings as well as
the decision. The repair is conservative: safe branch-local protection can also
abstain. It is not a general Python soundness proof or path-sensitive solver.

Tests cover direct returns, assignments, helper-dispatched protection calls,
nested branches, unsupported predicates and reuse findings. They exercise both
v2 and v3 and check the concrete repeated key labels using the real derivation
function with a label-returning protection stub.

## Separate post-fix evidence

[regression.json](regression.json) records 69 historical case evaluations:
23 valid v2 development cases, 20 v2 confirmation cases and 26 v3 integration
cases. These sets overlap and are not 69 unique independent programs. All
predictions match the frozen results, with zero false-fresh predictions on those
cases. The formerly invalid development case remains excluded. Completeness
flags can become more conservative; the report retains current full traces.

The executable eight-record counterexample now returns `unknown` and incomplete
in both analyzers. It is a new regression example, not an independent holdout.
The original tables correctly describe their finite corpora, but zero observed
false-fresh outcomes must not be generalized to arbitrary input programs.

The [regression runner](../../scripts/diagnostics/evaluate_source_branch_fix.py)
records source and input hashes and refuses to overwrite its output. It does not
change the frozen evaluators, original source corpora, results or manifests.

## Historical source bytes and Windows checkouts

Before editing v2, its LF-form bytes were verified against the original execution
hash and preserved in [executed_source_analysis_v2.zip](executed_source_analysis_v2.zip).
Member `source_analysis_v2.py` has SHA-256:

`4378a73e791a76829390645851e8d8cf61900257581d16fa406f51a3c4b017e9`

The three affected v2/v3 historical study tests explicitly verify that snapshot,
not the repaired current source. The current source is checked separately against
the post-fix regression record. The unchanged v1 and other dependencies continue
to be verified against their existing manifests.

Six Windows provenance failures were traced to LF/CRLF checkout conversion. The
[shared verifier](../../scripts/diagnostics/source_provenance.py) reports exact
checkout, checkout-to-LF, checkout-to-CRLF or exact snapshot matching. It accepts a
conversion only if the resulting bytes reproduce an existing expected hash, and
does not trim spaces or normalize other content. Snapshot matching permits no
conversion and requires an explicit archive/member. Tests reject actual content
changes and incorrect snapshots. No expected manifest hashes were rewritten.

## Research status unchanged

The later MOBIO/SCface utility confirmation still passes 0/4 utility gates. The
earlier pilot passes 0/2 joint gates, and the earlier utility replication passes
2/4 utility gates. This repair cannot establish retained matching or a new joint
security result. No private-data experiment, participant acquisition or power
calculation was performed as part of this fix.

At the user's request, independent case labeling, external proof/novelty review
and signoff are deferred to the user and reviewers. They are pending, not waived.
The new-participant study also still needs authorized data, overlap review,
feasibility and power justification, application-approved margins and a matched
attack/verification run. No failed gate or threshold has been relaxed.

The [updated pizza PDF](../../reports/Pizza_Algorithm_Explained_2026-09-25.pdf)
has nine pages, with the repair and later utility result on page 9. Older report
and slide artifacts remain historical presentations of their dated experiments.

## Verification

- `python -m pytest tests -q`: 244 passed in 54.05 seconds on the local Windows environment.
- PDF checks cover nine pages, ASCII text, no em/en dashes, text bounds, nonoverlap, required wording and nonblank rendering. The published PDF was regenerated and all nine pages rendered for inspection.
- Editor diagnostics reported no errors in the changed analyzer, new diagnostic scripts, report generator and new regression tests.
- `git diff --check` passed. The documentation link scan found only three pre-existing references to the absent older September guide; those unrelated links were left unchanged.