# MOBIO/SCface utility confirmation

Completed 2026-09-25: 96 evaluations in 13.38 seconds, with no attacker
training. The protocol and sources were frozen in commit `6762290`.

See the [prospective protocol](../../docs/protocols/scface_utility_confirmation_2026-09-25.md).
The runner used private MOBIO and SCface embeddings and wrote identity-level arrays
only under the ignored `results/` directory.

| Dataset | Split | Baseline TAR | Fresh TAR | TAR change | Lower bound | Fresh FMR upper | Pass |
|---|---:|---:|---:|---:|---:|---:|---:|
| MOBIO | 93083 | 93.51% | 92.70% | -0.81 pt | -4.87 pt | 0.93% | No |
| MOBIO | 93089 | 94.97% | 94.24% | -0.73 pt | -3.16 pt | 0.70% | No |
| SCface | 93083 | 29.23% | 29.45% | +0.22 pt | -5.36 pt | 0.78% | No |
| SCface | 93089 | 30.19% | 31.82% | +1.63 pt | -3.57 pt | 1.00% | No |

All FMR bounds pass the fixed 2% ceiling. All four cells fail only the TAR
noninferiority criterion, so the primary SCface and cross-dataset gates fail.
The SCface mean changes are nonnegative, but the bounds are too wide to exclude a
loss greater than three points. The new MOBIO partitions also fail, unlike the two
earlier MOBIO replication cells, showing that the utility conclusion is
partition-sensitive under the fixed method.

This does not prove that fresh derivation degrades SCface. It shows that the current
sample, verifier and three-point margin do not establish stable noninferiority. The
very low absolute SCface TAR also limits deployment relevance. No leakage attacker
was rerun, and these utility-only outcomes cannot be combined with a different
security study to claim a joint pass.

- [Aggregate effects](effects.csv)
- [All 96 aggregate endpoints](endpoints.csv)
- [Execution and input hashes](execution_manifest.json)
