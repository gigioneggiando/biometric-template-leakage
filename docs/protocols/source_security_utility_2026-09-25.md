# Source analysis and security/utility pilot

Written before execution. Exploratory research, not externally registered or
independently reviewed. Previous studies and manifests remain immutable.

## Source benchmark

Freeze source interpreter and generated case corpus before scoring. Cases include
constants, hidden modulo/masks, affine renaming/helper variants, shared prefixes,
unknown external calls and unsupported control flow. Runtime oracle independently
enumerates returned component key labels for 64 integer record IDs by replacing
protection sinks in trusted synthetic fixtures with label-returning stubs. It does
not call the static analyzer or read its predictions. A duplicate label gives a
finite-domain reuse label; all-distinct means no reuse observed on that domain,
NOT proof of unbounded freshness. Runtime errors are unlabeled, never negative.

These are SAME-AUTHOR synthetic development/stress cases, not independently authored
or blinded held-out constructions. Human labels remain pending. Export sources,
oracle labels, disagreements and a blank reviewer-label column for external review.
No result will be described as independent validation or global detection accuracy.
Alpha-renamed and composed cases exercise implementation inference without YAML
condition names, but do not demonstrate generalization to independently unseen code.

Baselines: current KSSA v1 given the same declared fresh-key YAML in every case;
Bandit 1.8.6 default Python security rules, with any warning counted as an alert.
Bandit is a general-purpose scanner, not a biometric reuse detector. Export all rule
IDs and raw JSON, report TP/FP/TN/FN and abstentions/coverage separately. Generic
alerts are not evidence of discovering key reuse. No unsupported case is silently
scored as safely fresh. Record observed per-case time separately from subprocess
startup and do not compare incomparable timing measurements.

## Matched real-data study

- Local authorized MOBIO and FEI unit embeddings; one new identity partition 92583.
- Sign-corrected 64-bit BioHash; baseline pool 4, a 16/64 shared-projection control,
  and fresh per-record candidate. Executable recipes define actual key behavior.
- Three transform/master seeds 92603/92609/92617; one ten-record mean-pool attacker
  per transform seed with model seeds 811/821/823 respectively (joint seed sensitivity,
  not independently crossed key/model factors). Set seed 92627; eight sets/identity;
  training cap 120 epochs, patience 30, existing 256-hidden MLP/loss.
- 18 newly trained endpoints; one-hour wall cap. Frozen input, source and protocol
  hashes; retain detailed identity scores only in ignored local results.
- Primary remediation: pool 4 -> fresh, one contrast per dataset. Partial-sharing
  attack is secondary and is NOT required to succeed. No attacker-architecture or
  seed search after observing test results.

## Legitimate verification

For validation/test splits separately, first image per identity is enrollment;
remaining images are probes. For every claimed enrollment, re-encode the raw probe
under THAT enrollment's key in the trusted verifier and score Hamming agreement.
Both arms get identical trusted-verifier capabilities. Keys remain outside the
attacker's template database. Reuse/fresh keys use the same derivation recipes as
the attacker experiment. Direct cross-key matching is not the legitimate endpoint.

Choose a threshold per policy/transform seed using validation impostor scores only:
smallest next-representable score above the order statistic allowing <=1% validation
FMR. Apply unchanged to held-out test identities. Export TAR/FMR, threshold and pair
counts. Use identity-balanced genuine rates, and impostor rates per probe identity.
Bootstrap key-seed and probe-identity axes, conditional on the realized enrollment
gallery. This does not capture enrollment-gallery population uncertainty; both
genuine and impostor scores are dependent. No binomial independence claim.

Primary gate: positive leakage-reduction lower bound, TAR-difference lower bound
>= -0.03 (three percentage points), and candidate test FMR upper bound <=0.02.
Margins are exploratory operational choices, not professor-approved deployment
requirements. Six one-sided bounds (three criteria x two datasets) use a Bonferroni
tail probability .05/6 and 10,000 crossed seed/identity resamples. This is a nominal
simultaneous-bootstrap gate, not a finite-sample coverage theorem. Report both pass
and fail, plus pointwise descriptive intervals for the shared-projection control.
Chance compatibility does not prove privacy. Security of the key service, query
restrictions, latency at scale and broader biometric threats remain untested.

The mathematical accounting functional, conditional source soundness argument and
idealized coupling bound are in [the theory note](../theory/source_scope_and_utility.md).
None establishes priority. The correlated projection is outside the independent-
component privacy bound. The proposed score must not be marketed as a universal
privacy predictor. Independent labeling and a specialist literature review are
external completion gates, not tasks an automated self-authored benchmark can meet.