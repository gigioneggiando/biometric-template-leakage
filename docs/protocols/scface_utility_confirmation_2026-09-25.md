# MOBIO/SCface trusted-verifier utility confirmation

Protocol frozen 2026-09-25 before execution. This is a utility-only prospective
generalization study; it does not retrain the leakage attacker and cannot create a
new joint security/utility pass by combining results from separate experiments.

## Inputs and design

- MOBIO: 150 identities, preserved 90/30/30 identity split counts, at least 11
  records per identity.
- SCface: 130 identities, preserved 78/26/26 counts, one frontal mugshot enrollment
  followed by visible surveillance probes, at least 20 successful records per identity.
- Two new identity reassignments: 93083 and 93089.
- Twelve new paired master-key seeds per split.
- Baseline: recurring pool of four BioHash keys.
- Candidate: record-specific BioHash derivation.
- Legitimate verifier: each gallery key is held by the trusted verifier, which
  re-encodes raw probes under that gallery key before Hamming comparison.
- Threshold: selected only from validation impostor scores at target FMR 1%.
- Test outcomes: identity-clustered TAR difference and candidate FMR.

## Frozen gates

There are four dataset/split cells and two one-sided criteria per cell. Each bound
uses crossed key-seed/identity bootstrap with 20,000 resamples and tail alpha
`0.05 / 8 = 0.00625`.

- TAR noninferiority: lower bound of candidate minus baseline is at least -3 points.
- FMR: candidate upper bound is at most 2%.
- A cell passes only if both criteria pass.
- Primary new-dataset utility support requires both SCface cells to pass.
- Cross-dataset support requires all four cells to pass.

The three-point margin and two-percent FMR ceiling are retained from the prior
study; their operational acceptability still requires Sani/application-owner review.

## Planning limitation

At 80% normal-approximation power, zero true TAR change and one-sided alpha 0.00625,
the design can clear a three-point margin only if the effective paired identity-level
standard deviation is approximately at most 4.92 points for 30 MOBIO test identities
and 4.58 points for 26 SCface identities. These are feasibility thresholds, not
estimates from unseen outcomes. Failure may therefore mean insufficient precision,
not demonstrated degradation.

No threshold, seed, split, margin or analysis rule may change after execution.
Identity partitions overlap across reassignments and do not represent independent
populations. Passing would not validate key custody, leakage resistance or deployment.
