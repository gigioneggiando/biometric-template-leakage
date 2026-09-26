# Exploratory utility precision sensitivity

Completed 2026-09-26 using published historical aggregates only. This is not
independent validation, a new matching experiment, a bootstrap coverage study,
or established joint power. No new participants or biometric evaluations were used.

## Method and limitations

The [runner](../../scripts/diagnostics/plan_utility_precision.py) reads the four
published identity-axis and key-axis standard deviations from the earlier
[post-hoc diagnostics](../utility_failure_diagnostics_2026-09-26/README.md).
Private per-person records of that later study were not present in the local
results directory. Instead of claiming a fitted crossed model, this calculation
uses the marginal SDs as planning proxies:

$$SE_{proxy}^2 = v (s_{person}^2/N + s_{key}^2/K).$$

Here $N$ is the future test-person count, $K$ the key-draw count, and $v$ a variance
multiplier. With an assumed normal mean, fixed known proxy variance, three-point
margin and the proposed single-cohort tail allocation $\alpha=0.05/3$, the
illustrative TAR-only gate probability is

$$\Phi((\Delta + 0.03)/SE_{proxy} - z_{1-\alpha}).$$

This is not the historical confirmation's $0.05/8$ allocation, and no historical
decision is recomputed. The marginal SDs already contain residual variation; they
are not separately estimated independent variance components. The plug-in normal
calculation ignores variance-estimation uncertainty, threshold estimation, gallery
uncertainty, population shift and attack/FMR endpoint dependence. It neither
simulates nor validates the proposed crossed-bootstrap procedure. Its apparently
high values can be optimistic; duplicated residual variation can also inflate the
variance proxy. It is not a calibrated upper or lower bound on actual power.

The fixed sensitivity grid has 384 rows: four historical cells, test-person counts
40/100/200/400, key counts 12/24/48/96, assumed mean changes 0/-1/-2 points, and
variance multipliers 1/2. Cells overlap and remain separate; do not pool them as
independent replications. All scenarios are retained, with no success-based selection.

## Illustrative results

For 200 future test people, assumed mean TAR change -1 point and variance multiplier
1, the normal approximation gives these TAR-only gate probabilities:

| Historical variability source | Split | 12 keys | 48 keys | 96 keys |
|---|---:|---:|---:|---:|
| MOBIO | 93083 | 47.7% | 89.2% | 96.6% |
| MOBIO | 93089 | 93.3% | >99.9% | >99.9% |
| SCface | 93083 | 23.4% | 62.4% | 81.1% |
| SCface | 93089 | 16.2% | 50.5% | 75.3% |

Even assuming zero mean loss, the two SCface-based 200-person/12-key scenarios
give only 49.0% and 33.9%. Doubling variance reduces the -1-point, 96-key SCface
scenarios to 50.0% and 44.4%. These are assumption-dependent calculations, not
predicted or measured outcomes for an unavailable new cohort.

The proposed 200 test people and 12 draws therefore must not be described as
demonstrably powered. Adding people alone leaves a key-variation term. More keys
can reduce that term but cannot establish population generalization or fix low
absolute recognition accuracy. No key count in this grid is selected as the new
protocol. Even adequate marginal TAR power would not prove adequate joint power.

## Required next step

An independent statistician and application owner should approve the estimand,
three-point margin and trusted-verifier architecture. Recover the paired historical
arrays to model key, person and residual effects; specify a range of plausible
new-cohort changes; simulate the actual joint attack/TAR/FMR decision rule and
check coverage and joint power. Revise the proposed design prospectively if needed,
including computational budget. Obtain authorized new data before execution.

The [existing new-cohort protocol](../../docs/protocols/new_participant_joint_2026-09-25.md)
is unchanged. The earlier 0/2 joint, 2/4 utility and later 0/4 utility results remain
unchanged. This planning exercise does not satisfy its required power approval.

[scenarios.csv](scenarios.csv) contains all aggregate scenarios;
[summary.json](summary.json) records assumptions, source/input hashes and the CSV
hash. The generator refuses overwrite. Tests check the normal null boundary,
variance scaling, invalid inputs, aggregate-only exports and frozen artifact hashes.