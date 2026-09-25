# Fixed utility replication

Completed 2026-09-25: 96 evaluations in 12.36 seconds, no new attacker training.
This exploratory follow-up ran while independent case/proof review was pending.

The [protocol](../../docs/protocols/utility_replication_2026-09-25.md) and source
hashes were recorded before execution. Twelve new key seeds, two new identity
partitions per dataset, validation-only threshold selection, a three percentage
point true-acceptance tolerance and a 2% false-match upper limit were fixed.
Eight one-sided bootstrap bounds use alpha 0.05/8 with 20,000 resamples.

| Dataset | Partition | Baseline TAR | Candidate TAR | TAR change lower bound, points | FMR upper bound | Utility criteria |
|---|---|---|---|---|---|---|
| MOBIO | 92821 | 94.02% | 95.15% | -2.32 | 0.93% | Pass |
| MOBIO | 92831 | 93.48% | 94.48% | -2.02 | 1.16% | Pass |
| FEI | 92821 | 93.74% | 94.12% | -3.71 | 0.93% | Not passed |
| FEI | 92831 | 92.46% | 92.69% | -3.61 | 1.09% | Not passed |

TAR is genuine acceptance; FMR is false-match rate. Baseline is a four-key pool,
candidate is record-specific derivation. Both FEI cells fail only the TAR
noninferiority criterion. This does not prove actual degradation; it means the
data and interval method do not establish the chosen tolerance. All four FMR
upper bounds are below the ceiling. Two of four utility gates pass.

These results do not revise the original pilot's two failed joint gates. No new
joint leakage-and-utility pass is claimed by combining experiments. Bootstrap
coverage is approximate; intervals condition on the gallery and observed validation
thresholds. Identity partitions overlap and are not new independent populations.
The twelve-seed rationale is heuristic, not a formal power calculation. Key custody
and the trusted raw-probe verifier remain assumptions.

- [Aggregate effects](effects.csv)
- [All 96 endpoint measurements](endpoints.csv)
- [Frozen execution record](execution_manifest.json)
- [Runner](../../scripts/train/run_utility_replication.py)
- [Internal proof and prior-work review](../../docs/review/source_proof_novelty_2026-09-25.md)
- [Simple pizza PDF](../../reports/Pizza_Algorithm_Explained_2026-09-25.pdf)

Private identity-level arrays remain in the ignored results directory. Independent
labels, external proof signoff, practical margin approval and novelty review are
still pending.