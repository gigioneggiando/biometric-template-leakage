# Exploratory utility-failure diagnostics

Completed 2026-09-26 after the frozen MOBIO/SCface utility decisions were known.
This is descriptive post-hoc diagnosis, not a new confirmatory test. It does not
change the 0/4 utility result, its three-point margin or any multiplicity rule.

## Variability axes

| Dataset | Split | Mean TAR change | SD across identity means | SD across key means | Identities with negative mean | Keys with negative mean |
|---|---:|---:|---:|---:|---:|---:|
| MOBIO | 93083 | -0.81 pt | 5.65 pt | 3.05 pt | 43.3% | 66.7% |
| MOBIO | 93089 | -0.73 pt | 3.17 pt | 1.75 pt | 36.7% | 58.3% |
| SCface | 93083 | +0.22 pt | 6.55 pt | 4.67 pt | 50.0% | 50.0% |
| SCface | 93089 | +1.63 pt | 5.29 pt | 5.93 pt | 46.2% | 41.7% |

Both identity and key axes vary materially relative to the fixed three-point
margin. Baseline/fresh identity-level TAR correlations are only 0.10-0.35. The
mean threshold shift is between -0.26 and +0.26 percentage points, so a large
systematic threshold displacement is not visible in these cells.

The two test partitions overlap by 7/30 MOBIO identities and 2/26 SCface
identities. Their disagreement is therefore not merely duplicate evaluation of the
same people, but neither split is an independent population sample.

## SCface capture difficulty

Distance-aggregated TAR, averaged across the twelve keys:

| Split | Distance | Recurring TAR | Fresh TAR | Change |
|---|---:|---:|---:|---:|
| 93083 | 1 | 7.64% | 8.10% | +0.46 pt |
| 93083 | 2 | 28.71% | 29.67% | +0.96 pt |
| 93083 | 3 | 51.29% | 50.46% | -0.83 pt |
| 93089 | 1 | 8.70% | 10.21% | +1.51 pt |
| 93089 | 2 | 28.98% | 29.30% | +0.32 pt |
| 93089 | 3 | 52.88% | 55.95% | +3.07 pt |

Distance 1 is consistently hardest and distance 3 easiest under the SCface naming
used by the dataset. The fresh-minus-recurring direction is not consistently
negative. These patterns are consistent with capture difficulty and crossed
identity/key heterogeneity driving wide bounds; they do not prove a causal source
of the failed gate.

## Next protocol recommendation

1. Keep the failed utility result unchanged.
2. Ask Sani/application owners to approve the three-point margin and trusted-verifier
   architecture before another run.
3. Power the next study using observed crossed identity/key variability, not only
   the number of key seeds.
4. Prefer a new authorized identity cohort. Additional keys alone do not address
   between-identity and population uncertainty.
5. Predefine distance-stratified SCface endpoints or use a dataset with operationally
   acceptable unprotected cross-condition recognition. Do not introduce strata or
   margins after observing the next outcomes.

Compact non-identifying outputs are [variability.csv](variability.csv),
[scface_capture.csv](scface_capture.csv), [summary.json](summary.json) and the
[execution manifest](execution_manifest.json). No identity labels or identity-level
measurements are exported.
