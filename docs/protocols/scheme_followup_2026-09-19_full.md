# Extended multi-seed scheme follow-up: exposures, pool-8, SCface

Protocol written on 2026-09-19 before inspecting any result. User-authorized bounded local compute, budget at most 3,600 seconds on local CPU, matching the ceiling already used for `scheme_followup_2026-09-18`. This extends that study; it does not retroactively change its frozen 216 endpoints, which remain the primary evidence at pool-4/exposures-1-and-10.

## Motivation

Three items were open after `scheme_followup_2026-09-18` and `pool_replication_2026-09-19`: the 2- and 5-record exposure levels were untested in the rigorous multi-seed/multi-partition setting (only 1 and 10 were); pool-8 was untested at that rigor (only pool-1/pool-4 were, pool-8 only existed in the earlier one-seed pilots); and SCface had no multi-seed/multi-partition coverage at all (one-seed pilots only). This protocol covers all three in one run since they share the same runner and cost structure.

## Fixed design

- Datasets: MOBIO and SCface, each at two identity-reassignment seeds (91831, 91843), matching `scheme_followup_2026-09-18`'s partition convention. FEI is not present on this host and remains out of scope, not a null result.
- Schemes: IoM-GRP and PolyProtect, same paper-specified configuration as every prior pilot/follow-up (IoM-GRP: 300 groups, q=16; PolyProtect: window 5, overlap 2, coefficient bound 50).
- Conditions: `independent_unseen_keys`, `random_key_pool_1`, `random_key_pool_4`, `random_key_pool_8` (the fourth is new; the first three match the existing follow-up).
- Exposures: 1, 2, 5, 10 (2 and 5 are new; 1 and 10 match the existing follow-up).
- Models: `mean_mlp` and `deepsets` for exposures > 1; `single_mlp` for exposure 1 (unchanged from the existing runner's convention).
- Training: three model seeds (601, 607, 613), 120-epoch cap, patience 30, hidden width 256, matching every prior pilot/follow-up exactly so results are comparable.
- Key/set seeds: 92101 (key) and 92107 (set), new values not reused from any earlier study, since this is a materially larger condition/exposure grid than the one those seeds were frozen for.

## Analysis, fixed before inspection

Reuses `analyse_runs` from `scripts/train/run_scheme_followup.py` unchanged. Its primary-family logic (`condition == "random_key_pool_4" and model == "mean_mlp"` at exposure 10) is untouched, so the original eight-hypothesis primary family from `scheme_followup_2026-09-18` is not altered or re-tested here; this run reports its own descriptive endpoints for every condition/exposure/model cell, and computes ten-minus-one contrasts at exposure 10 for every condition (not only pool-4), labelling only the pre-existing pool-4/mean_mlp cells as primary. Pool-1, pool-8, and every 2- and 5-exposure endpoint are exploratory, not a new corrected family, and are reported as such alongside pass/fail and negative results.

Native PolyProtect controls (`run_controls`) repeat on the newly-added SCface partitions using the same three native key seeds (91873/91879/91883) and permutation/bootstrap machinery already used for MOBIO/FEI, extending `native_null_controls.csv` and `norm_sensitivity.csv` coverage rather than replacing the existing MOBIO/FEI rows.

## Scope and limits, stated in advance

FEI is excluded (no local embeddings on this host). This does not add a fifth protection scheme, does not retrain a raw-input attacker, and does not establish a full Stage-B confirmatory matrix by itself (identity assignments still overlap across the two partitions per dataset, and training key/set seeds are still fixed across model seeds). A negative or chance-compatible result at any new condition/exposure is reported as designed. Private per-identity scores, embeddings, and images stay local and ignored; only compact aggregates are tracked.
