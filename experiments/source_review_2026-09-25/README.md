# External review handoff

Status: prepared, not independently reviewed. Zero independent labels or new
externally authored holdout cases have been received.

Update 2026-09-26: the user can arrange reviewers. Use the
[corrected-analyzer handoff](../independent_validation_2026-09-26/README.md) for
the invitation and disclosure sequence. It preserves this masked packet unchanged
and freezes the corrected code separately. External submissions remain pending.

Send only [independent_cases.zip](independent_cases.zip) to each case reviewer.
Its instructions, 24 neutral filenames and blank CSV omit our predictions and
runtime labels. The original-to-neutral mapping stays in the ignored results
directory. Source code is visible, so this is answer masking, not double blinding.
The cases remain same-author development cases even after external relabeling.

Ask two reviewers to work separately and avoid the repository's result pages
until their labels are frozen. Retain both originals, hashes, disagreements and
adjudication reasons. Request independent new cases before showing tool outputs.
Reviewer names and dates alone do not verify independence: obtain conflict and
prior-exposure declarations. No packet has been sent automatically.

[packet_manifest.json](packet_manifest.json) tracks every archive member's hash.
The [generator](../../scripts/diagnostics/prepare_independent_review.py) also
provides a form validator that rejects blank or incomplete submissions.

After case labels are locked, share the
[internal proof and prior-work review](../../docs/review/source_proof_novelty_2026-09-25.md)
and frozen theory with an appropriate mathematical reviewer. This memo is not
external signoff or a comprehensive novelty search.