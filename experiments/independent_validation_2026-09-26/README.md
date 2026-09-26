# Corrected-analyzer independent review handoff

Prepared 2026-09-26 after the user confirmed they can arrange reviewers. Status:
awaiting reviewer agreements and submissions. No reviewer was contacted
automatically; zero independent labels, external cases or signoffs are recorded.
The user confirmed that no new authorized participant cohort is available.

## Send now

Send [reviewer_request.md](reviewer_request.md) and
[independent_cases.zip](independent_cases.zip) separately to two qualified reviewers.
Each reviewer should work without the other's answers. Do not send the repository,
paper, results, coordinator notes or source snapshot before their labels and new
cases have been locked. The packet is byte-identical to the original answer-masked
24-case packet, not a new or independently authored corpus.

The ZIP contains source cases, contracts and blank labels. The invitation asks for
declarations and new cases. Reviewers should not upload confidential or identifying
information; contact and conflict records can be held privately by the coordinator.

## Frozen target, disclosed later

[target_manifest.json](target_manifest.json) fixes the exact corrected v3 analyzer
and its v1/v2 dependencies through hashes. The
[source snapshot](source_after_label_lock.zip) includes package source and dependency
specifications, not private biometric data, old predictions or coordinator mappings.
This snapshot is for phase 2, after label lock. The
[freezer](../../scripts/diagnostics/prepare_independent_review.py) refuses overwrite.
Future analyzer changes require a new target and separate results, not replacement
of this target. An archive fixes bytes; it is not an externally timestamped registration.

## Coordinator sequence

1. Record reviewer qualifications, conflicts, prior exposure and acceptance. Aim
   for two reviewers who did not author the implementation or its tests. Prior
   exposure must be disclosed rather than silently called blinded review.
2. Receive each original CSV, declaration, notes and new-case package separately.
   Store them read-only with SHA-256 hashes and receipt times before sharing
   answers or analyzer output. Use the existing `validate_labels` function against
   the packet's case hashes for mechanical checks; it does not certify independence.
3. Retain unsure labels. Report finite-domain and unbounded-contract judgments
   separately. Request at least ten new cases from each reviewer as an initial
   diagnostic budget, not a powered accuracy sample. Freeze every submitted case,
   label and assumption, including duplicates or invalid cases, before evaluation.
4. Have an adjudicator record agreements, disagreements and reasons after both
   original reviews are locked. Document exclusions without hiding them. A finite
   no-collision observation must not become an unbounded injectivity proof.
5. Run the exact frozen analyzer on all admitted cases without tuning it. Treat
   submitted code as untrusted: parse it for analysis, do not execute it on the
   workstation. Any needed runtime check requires separately approved isolation.
6. Report the old 24 relabeled development cases separately from new external
   cases. Include all attempted cases, abstention/coverage, completeness, uncertain
   labels and a confusion table. Highlight every fresh claim contradicted by a
   reviewer-supported reuse counterexample. Do not select a favorable subset or
   silently score unknown labels as correct. An abstention is not a correct decision.
7. Only then release the source snapshot, paper and internal proof/prior-art note
   for specialist review. Ask separately about the soundness scope, existing
   crypto-misuse analysis, actual contribution and trusted-verifier assumptions.
   Labeling accuracy alone does not establish proof validity or novelty.

Request reviewer approval for attribution or anonymous aggregate reporting. Human
judgments can disagree and are not automatically ground truth; retain the evidence
and caveats. No independent-validation success criterion or accuracy result is
claimed before those submissions exist.

## Matching study remains separate

The [aggregate precision sensitivity](../utility_precision_planning_2026-09-26/README.md)
is a planning aid, not new utility evidence or an approved power calculation.
The proposed new-participant protocol remains unchanged. New authorized people,
approved margins, prospective joint power/coverage analysis and a matched
attack-and-verification run remain required. The historical 0/4 utility result
cannot be replaced by this handoff or by more tests of the source analyzer.