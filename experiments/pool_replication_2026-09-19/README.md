# Independent pools and prediction-mean baseline

Completed 2026-09-19 in **254.188 seconds** on CPU (eight Torch threads), within 3,600 seconds: **24 cells, 144 trained endpoints and 72 prediction-mean evaluations**. The [prospective protocol](../../docs/protocols/pool_replication_2026-09-19.md) and [configuration](../../configs/attacks/pool_replication_2026-09-19.yaml) were frozen before training. Earlier executed sources and results are unchanged.

## Design

MOBIO/FEI; IoM-GRP/PolyProtect; pool size four; partitions 91831/91843; independently seeded pools 91901/91907/91909; model seeds 601/607/613. Set seed 91867 and eight nested sets stay fixed. The key seed changes **both transforms and sample-to-slot assignments**, not transforms alone. Seeds recur across datasets/partitions; the summaries are not independent population replications.

Single-record and input-mean MLPs retain hidden width 256, normalized targets, the earlier optimizer, 120 epochs and patience 30. Prediction mean applies the **same fitted single-record checkpoint** to each of ten records, averages normalized outputs and normalizes again; it requires no additional training. All ten-record endpoints share records and galleries. Gallery images are excluded from targets.

Access, inference records, encoder, gallery, model seeds, architecture widths and epoch caps are matched. Training objectives and effective record presentations are not: single-record training uses nested one-record queries, while the set model trains on ten-record means. This is a simple inference-matched baseline, not an exhaustive optimized comparison.

## Results

Input-mean ten-record minus single-record top-1, percentage points. Intervals use 4,000 crossed pool/model-seed/identity bootstrap draws; they are pointwise, not simultaneous or multiplicity-adjusted. Three pools cannot support strong distribution-wide guarantees; no new corrected significance claim is made. A/B = 91831/91843.

| Dataset | Scheme | Split | Gain [95% interval], pp | Pool minimum / maximum, pp | Positive pools |
|---|---|---|---|---|---|
| FEI | IoM-GRP | A | 26.22 [19.96,32.50] | 24.79 / 28.65 | 3/3 |
| FEI | IoM-GRP | B | 25.38 [18.54,32.95] | 21.56 / 27.71 | 3/3 |
| MOBIO | IoM-GRP | A | 38.47 [29.58,47.96] | 34.86 / 42.36 | 3/3 |
| MOBIO | IoM-GRP | B | 33.84 [23.75,43.75] | 29.31 / 40.97 | 3/3 |
| FEI | PolyProtect | A | 30.35 [0.31,70.11] | -0.31 / 72.40 | 2/3 |
| FEI | PolyProtect | B | 29.97 [-2.50,65.00] | -3.23 / 67.40 | 2/3 |
| MOBIO | PolyProtect | A | 26.25 [0.46,56.94] | -0.28 / 58.89 | 2/3 |
| MOBIO | PolyProtect | B | 23.94 [0.97,49.31] | 0.83 / 47.78 | 3/3 |

IoM gains persist in 12/12 tested dataset/split/pool combinations. PolyProtect has 9/12 positive gains and three reversals: **strong pool sensitivity**, not uniform robustness. Earlier corrected fixed-pool findings remain conditional on their original pool.

Direct input-mean minus prediction-mean ten-record top-1:

| Dataset | Scheme | Split | Difference [95% interval], pp |
|---|---|---|---|
| FEI | IoM-GRP | A | 1.01 [-1.77,4.93] |
| FEI | IoM-GRP | B | -0.10 [-6.11,7.08] |
| MOBIO | IoM-GRP | A | 1.16 [-2.92,6.02] |
| MOBIO | IoM-GRP | B | -1.06 [-8.06,6.62] |
| FEI | PolyProtect | A | 21.53 [-10.21,70.94] |
| FEI | PolyProtect | B | 22.71 [-5.00,66.46] |
| MOBIO | PolyProtect | A | 15.28 [-14.17,55.42] |
| MOBIO | PolyProtect | B | 12.22 [-11.11,44.86] |

All eight intervals include zero. Neither input-pooling superiority nor equivalence is established. Prediction averaging recovers most IoM benefit; PolyProtect's mean differences are dominated by pool variation. The contribution is reuse-conditioned measurement, not a superior aggregation architecture.

## Scope and reproduction

SCface remains historical BioHash and one-seed scheme **supporting pilot evidence**: private inputs were unavailable on this host, so no new cross-camera replication occurred. LFW remains historical BioHash evidence. See [coverage](../../reports/figures/fig_dataset_coverage.pdf) and [pool/baseline results](../../reports/figures/fig_pool_replication.pdf).

The attacker requires same-person grouping, paired training from the **same realized hidden system-wide pool**, and a small unprotected gallery guaranteed to contain the target. Neither keys nor slots are disclosed. A query interface must expose protected outputs or an equivalent observation; accept/reject responses alone do not supply the assumed pairs. Distinct per-person/provider pools, unrelated-key proxy training, unknown grouping and open-set search are not evaluated. Deployment prevalence is not asserted.

- [results_summary.csv](results_summary.csv): 216 aggregate endpoints (144 fits, 72 reused-checkpoint evaluations).
- [pool_contrasts.csv](pool_contrasts.csv): 48 pool-specific contrasts.
- [crossed_contrasts.csv](crossed_contrasts.csv): 16 summaries, eight primary and eight baseline contrasts.
- [execution_manifest.json](execution_manifest.json): 34 source/config/protocol hashes, input hashes, versions, timing and counts.
- [executed_sources.zip](executed_sources.zip): exact hashed sources; no data, identity scores or weights.

Reproduction requires authorized matching inputs and dependencies. Extract the source snapshot into a separate clean directory, not over the working repository, then run `python scripts/train/run_pool_replication.py --config configs/attacks/pool_replication_2026-09-19.yaml`. Existing frozen output paths are refused. Private identity scores stay ignored; recomputing bootstrap intervals requires those scores or a fresh authorized run. The historical 849-row inventory is unchanged; this different-schema study is indexed separately. Tests check trainer parity, baseline semantics, aggregate consistency and archive integrity. Independent human review, stricter PolyProtect selection and broader confirmation remain open.