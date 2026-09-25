# New-participant joint study: preparation only

**Status: blocked pending authorized new data and review. No new participants
have been added, and no new-cohort attack or matching results exist.** The user
confirmed no new cohort is available and requested protocol/PDF preparation.

The [cohort audit](cohort_audit.json) hashes the earlier execution record and verifies
that the current FEI/MOBIO metadata are byte-identical to its inputs:

| Available embeddings | Records | Participants | Previously used | Eligible new IDs |
|---|---|---|---|---|
| FEI | 2,378 | 200 | 200 | 0 |
| MOBIO | 1,799 | 150 | 150 | 0 |

A separate local directory count found 2,800 FEI JPG files representing 200 numeric
participant IDs. Extra raw images do not add people. This directory count is a
local inventory observation, not a checksum audit of every photograph. LFW is
available but not certified independent, and must not be relabeled as FEI.

## Connection to the algorithm

The same audit runs the source interpreter on the actual recipe code: recurring
and partial return reuse, separated returns conditional_fresh. JSON traces and
recipe/analyzer hashes are retained. The candidate comparison is selected from
this finding before new outcomes: four-key pool versus record-specific derivation.
Source freshness is conditional, not privacy. The change in key policy, not the
act of scanning the code, is the experimental intervention.

The [proposed fixed joint protocol](../../docs/protocols/new_participant_joint_2026-09-25.md)
specifies one new cohort, a planning target of 500 eligible new people (200 train,
100 validation, 200 test), 12 paired key/model draws, 24 attack fits and 24 matching
evaluations. All three bounds must pass on the same test people: reduced attack,
TAR loss at most three points, FMR at most 2%. The target needs feasibility,
power and ethics/access approval; it is not a completed power calculation.

## What the data owner needs to provide

Supply an authorized cohort's location and provenance to the responsible research
team, with stable pseudonymous IDs, at least 11 distinct usable photos per person,
capture/session information, permission scope and an overlap review against all
earlier participants. Do not send faces, keys or confidential documents through
public Git or chat. Newly named IDs alone cannot establish independence.

Before data arrives, neither an empirical improvement nor a successful new joint
gate can be reported. The earlier 0/2 joint and 2/4 utility gates remain unchanged.

- [Updated pizza PDF](../../reports/Pizza_Algorithm_Explained_2026-09-25.pdf)
- [Local overlap checker](../../scripts/diagnostics/audit_new_participants.py)
- [Independent case-review handoff](../source_review_2026-09-25/README.md)
- [Internal proof and novelty review](../../docs/review/source_proof_novelty_2026-09-25.md)