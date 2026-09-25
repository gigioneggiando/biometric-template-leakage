# Prospective utility replication

Written before this replication is executed. This is an exploratory follow-up
informed by the failed pilot, not external preregistration or independent review.
The pilot and its failed gates must remain unchanged.

## Fixed design

- MOBIO and FEI existing authorized unit embeddings.
- Sign-corrected 64-bit BioHash, recurring pool 4 versus fresh keys.
- Trusted verifier and validation-only threshold selection unchanged from the pilot.
- Twelve new key seeds: 92701, 92707, 92717, 92723, 92737, 92753, 92761,
  92767, 92779, 92789, 92801, 92809.
- Two new identity assignments: 92821 and 92831. These overlap within each dataset
  and are sensitivity analyses, not independent populations.
- 96 policy/key/dataset/partition evaluations, no new attacker training.
- Same utility margin: candidate minus baseline TAR >= -0.03.
- Same validation target FMR <= 0.01 and held-out FMR upper limit <= 0.02.
- Eight one-sided primary bounds: TAR difference lower bound and candidate FMR
  upper bound for each of four dataset/partition cells. Bonferroni tail .05/8;
  20,000 crossed key-seed/probe-identity bootstrap draws, analysis seed 92843.
- One fixed run, 3,600-second cap, no optional stopping, margin changes, favorable
  seed selection or after-the-fact expansion. Partial runs cannot support completion.

## Sample-size rationale and limitations

Twelve rather than three key seeds improves estimation of key-draw variation.
Under independent seeds with comparable variance, the seed-only standard-error
component scales by sqrt(3/12) = 0.5. This is a planning heuristic, not a powered
design: identity variation, rare errors, gallery dependence and threshold selection
can dominate. No claim of 80% or 90% power is made. Two partitions check sensitivity
without pooling overlapping identities as independent observations.

Thresholds are selected separately for each policy and seed on validation identities
and remain fixed on test identities. Rates are identity-balanced. Bootstrap
inference is conditional on each realized enrollment gallery and observed validation
thresholds; enrollment-gallery population uncertainty is not captured. Nominal
Bonferroni allocation does not make bootstrap coverage exact.

The result is a utility-only replication. Historical leakage results must not be
combined with new utility intervals into a new joint security-and-utility pass.
It neither certifies secrecy nor adds population-independent evidence. Both pass
and fail are published. External reviewers must approve practical margins before
deployment conclusions. Independent labeling and proof/novelty review remain pending;
this run does not imply either gate has been cleared.

## Preservation

Before execution, record exact source/configuration/protocol/input hashes and
software versions. Detailed identity rates stay in ignored local results. Export
aggregate endpoints and all four effects. Use a new dated directory; refuse to
overwrite it. No raw biometric data, identities or keys are included in the review PDF.