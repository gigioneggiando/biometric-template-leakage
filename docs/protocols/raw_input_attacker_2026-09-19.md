# Learned raw-input attacker

Protocol written on 2026-09-19 before inspecting any result. User-authorized bounded local compute, budget at most 1,800 seconds on local CPU. This is the last item from the 2026-09-19 open list (2/5 exposures, pool-8, SCface rigor, and this were requested together; the first three are complete in `scheme_followup_2026-09-19_full`).

## Question

`norm_native_audit_2026-09-18` found that native (untrained) cosine matching of raw, non-unit-normalized PolyProtect templates leaks descriptively more than matching unit-normalized templates, though only the FEI raw-unit gain survived correction. That is a single-record, untrained diagnostic. Does a *learned* multi-record attacker trained on protected templates built from raw (non-unit-normalized) ArcFace embeddings recover more identity-discriminative information than the standard unit-normalized pipeline, for a norm-sensitive scheme (PolyProtect), and does it stay chance-compatible under fresh keys the way the unit pipeline does? IoM-GRP is included as a control: it is already proven scale-invariant (`scale_invariance.csv`, zero of 38,400 sampled codes changed between raw and unit input), so a learned attacker should not do better than chance under fresh keys there either.

## Fixed design

- Datasets: MOBIO and SCface. FEI is not present on this host.
- Raw extraction: re-extract every image's raw (pre-normalization) 512-D ArcFace vector directly from its source image using the existing hash-pinned YuNet/ArcFace pipeline, reusing `extract_raw` from `scripts/diagnostics/run_norm_native_audit.py` unchanged, including its check that `raw / ||raw|| == saved unit embedding` (max abs error <= 1e-4) before anything downstream runs. Raw vectors are cached under ignored `results/`, never Git-tracked.
- The raw vectors are then written to a new on-disk embedding directory (`data/processed/embeddings/{dataset}_raw/buffalo_l_yunet/`, gitignored like every other embeddings directory) with identical metadata/manifest to the existing unit directory, so the existing `run_real_multiexposure.run()` pipeline can load it unmodified via `embedding_dir`. This is the only way to feed non-unit-normalized input through that pipeline: `run_pilots` (used by the pilot/follow-up runners) explicitly asserts unit-normalized input and must not be weakened, so this study calls `runner.run()` directly instead, bypassing `run_pilots`, not the assertion itself.
- No new identity split: the existing train/val/test assignment already on disk is reused (no reassignment), one partition per dataset, to bound scope given the added extraction cost.
- Schemes: PolyProtect (scale-sensitive, the primary interest) and IoM-GRP (scale-invariant, the control). Same paper-specified configuration as every prior study.
- Conditions: `independent_unseen_keys` (fresh) and `random_key_pool_4`. Key seed 92201, set seed 92207 (new, not reused).
- Exposures 1 and 10; single MLP at 1, mean-pool MLP and DeepSets at 10; three model seeds (601, 607, 613), 120-epoch cap, patience 30, matching every prior study exactly.

## Analysis, fixed before inspection

For each dataset/scheme/condition/exposure/model cell, report top-1 against chance with the existing `identity_clustered_top1_interval`/`aggregate_runs` machinery already used by `runner.run()`, unchanged. The primary comparisons, fixed in advance:

1. Is fresh-key top-1 (exposure 10, mean-pool) chance-compatible for raw-input PolyProtect, the same way it already is for unit-input PolyProtect? A clustered interval excluding chance would be a genuine new finding, not a replication.
2. Is fresh-key top-1 chance-compatible for raw-input IoM-GRP (the scale-invariance control)? It is expected to be, and a violation would indicate a pipeline problem, not a scientific finding, and must be investigated before anything else is reported.
3. Does the pool-4 ten-minus-one gain for raw-input PolyProtect differ materially from the already-reported unit-input gain at the same pool size (not a formal paired test against a different study's seeds; a descriptive comparison only, since key/set seeds and identity assignment differ from the earlier runs).

No formal multiple-comparison family is preregistered here beyond the two chance-compatibility checks in (1) and (2); this is an exploratory pilot on one partition, not a confirmatory study, and is reported as such regardless of outcome.

## Scope and limits, stated in advance

One identity partition per dataset, not the two-partition sensitivity check used elsewhere. Two schemes, two conditions, two exposure levels only (no pool-1, pool-8, or 2/5-exposure raw-input coverage). FEI is excluded. This does not retrain BioHash or MLP-Hash on raw input, does not establish a causal mechanism for any leakage found, and does not constitute independent human review. A null (chance-compatible) result for PolyProtect is reported as designed, not treated as a failure.
