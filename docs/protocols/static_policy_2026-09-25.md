# Static policy analysis: matched security evaluation

Protocol written before execution on 2026-09-25. Exploratory independent study,
not benchmark_cb reproduction or an externally registered confirmatory trial.
The user reports that the professor identified a static-analysis algorithm as
the contribution to pursue. This is project direction, not verified priority.

## Algorithm and scope

Key-Scope Static Analysis (KSSA v1) interprets the repository's YAML experiment
configuration language without loading biometric records, executing protection,
or fitting an attacker. It is configuration-level static analysis, not a general
Python source-code analyzer, a new protection transform, or a security proof.

For each scheme/condition pair, map key scope to fresh-declared, shared across
splits, shared projection, or unknown. Positive recurring pools and global keys
trigger KEY_REUSE; a nonzero shared projection triggers KEY_CORRELATION; exposed
pool-slot labels trigger SLOT_DISCLOSURE. Unknown schemes/conditions and malformed
required fields fail closed. PolyProtect always retains NATIVE_LINKAGE_REVIEW;
uncorrected BioHash retains HAAR_ASSUMPTION. Runtime assumptions always require
review. No output means "secure". Cost is O(S*C) condition classifications for S
schemes and C conditions, excluding input string length and finding serialization.

The candidate changes only the condition to independent_unseen_keys and removes
explicit key-slot disclosure. It preserves scheme parameters, identities, sample
selection, seeds, training settings and exposure counts. It is a separate proposal,
never an in-place rewrite of an experiment or deployment. Manual review is required.
The CLI --enforce exits 2 for blocking findings and 3 for unresolved review;
without --enforce it prints findings with exit 0 for research auditing.

## Hypothesis and fixed matrix

Changing random_key_pool_4 to independent_unseen_keys reduces learned ten-record
linkage in the tested setting. A nonpositive paired interval or corrected p >= .05
does not support the reduction for that comparison. We do not require or predict
native PolyProtect unlinkability. Findings must be reported even if unfavorable.

- MOBIO and FEI local authorized, unit-normalized 512-D embeddings.
- IoM-GRP (300 groups, 16 entries) and PolyProtect (window 5, overlap 2, bound 50).
- Two identity partitions (92531, 92543), three model seeds (701, 709, 719).
- One and ten exposures; single MLP and mean-pool MLP respectively.
- Pool 4 baseline and analyzer-generated fresh-key candidate, same key/set seeds.
- 16 cells, 96 trained endpoints; 120 epochs maximum, patience 30, one-hour cap.
- Primary family: eight ten-record baseline-minus-candidate contrasts.
- Crossed seed/identity bootstrap (2,000 draws), identity sign-flip of seed-mean
  paired differences (1,999 resamples), Holm correction over eight contrasts.
- One-record comparisons, native cosine linkage, and after-policy chance-relative
  intervals are secondary/descriptive. No equivalence test or approved margin.

The existing runner enforces identity-disjoint splits, finite unit inputs,
gallery holdout, and unique/disjoint fresh keys. Static findings and runtime checks
are different evidence. Runtime-key-audit agreement on synthetic fixtures tests the
scope abstraction, not real-world vulnerability detection accuracy. Existing
attacks motivated the rules; this is not a blinded detector benchmark.

## Interpretation and preservation

The attacker retains paired training access to the same realized hidden pool in
the baseline, knows grouping, and searches a small closed gallery. Candidate keys
remove that recurring-transform access. Same seeds do not mean identical draws
between distinct key mechanisms. Only one pool draw is studied per scheme; the
two identity assignments overlap and are not independent populations. Sign-flip
inference assumes symmetric independent identity-cluster differences conditional
on the realized training; the small number of seeds limits uncertainty estimates.

No authentication-utility guarantee follows: fresh per-record keys may require
key management and compatible re-encoding for legitimate matching. The native
endpoint is cross-record cosine linkage, not deployed genuine/impostor verification
under authorized key access. Public deterministic research seeds are not production
secrets; entropy, secrecy, side channels, metadata identity, source fidelity and
input norms cannot be certified from YAML. Larger pools are never declared safe
from a numerical threshold. SCface is not rerun because its embeddings are absent
from this workspace. No raw biometric data or per-identity scores are exported.

Sources, protocol, configuration, software versions and local input hashes are
frozen before execution. New outputs use dated directories; historical results
are untouched. Partial/failed runs are recorded and cannot produce a complete
primary-family claim. Aggregate tables and a separate PDF addendum document the
actual completed results and residual risks.