# Bounded scheme follow-up: 2026-09-18

## Authorization and freeze

The user authorized at most one hour of local computation on MOBIO/FEI on 2026-09-18. SCface embeddings are unavailable on this host; its existing compact results remain separate. This protocol and configuration are written before the new results are inspected. No Git commit is created without user permission: the execution manifest records the base commit, dirty-worktree status, SHA-256 hashes of all source files and configuration, and UTC start/end timestamps instead. This is a prospective bounded follow-up, not completion of the full roadmap or independent review.

## Learned linkage matrix

- MOBIO and FEI, identity reassignments 91831 and 91843, preserving original split sizes and excluding the gallery from exposure sets.
- Paper-specified IoM-GRP and PolyProtect with the original pilot dimensions and parameters.
- Fresh keys, one shared hidden transform, and random pool 4; common key seed 91861 and set seed 91867.
- Three model seeds (601/607/613), single MLP at one record, mean MLP and DeepSets at ten records, eight nested sets per identity. All use 120 epochs maximum, patience 30, hidden width 256, Adam learning rate 0.001 and weight decay 0.0001; best validation-loss checkpoint.
- Twenty-four condition cells and 216 model endpoints are planned. Each completed cell is persisted before the next begins. Partial cells are not reported as completed. The budget is shared with the diagnostics below; no missing cell is imputed.
- No 2/5-record sweep, LFW/SCface extension, extra protection families, or natural non-normalized embedding extraction is included in this bounded run.

## Analysis defined before execution

Report each dataset/scheme/identity-partition separately. Model-seed means and sample SD describe the three trained seeds. For each endpoint and ten-minus-one contrast, a crossed seed/identity bootstrap resamples model seeds and identities independently (2,000 draws), preserving pairing between endpoints. These descriptive intervals do not include key/set-seed uncertainty and do not turn overlapping identity partitions into independent replications.

The primary family comprises eight pool-4 mean-MLP ten-minus-one contrasts (two datasets x two schemes x two identity assignments). Use a one-sided paired sign-flip randomization test of the identity-level differences averaged across model seeds, with 1,999 permutations and Holm correction across the eight planned hypotheses. The sign-flip test assumes null sign exchangeability and conditions on the trained seed ensemble; report that distinction from crossed-bootstrap uncertainty. If cells are missing, retain family size eight, treating missing tests as p=1 for correction. Secondary endpoints are descriptive. No equivalence margin is chosen by looking at these results; +/-1/2/5-point sensitivity is not confirmatory equivalence.

## Native PolyProtect and norm diagnostics

For each dataset/identity partition, generate fresh PolyProtect templates with three independent key seeds (91873/91879/91883). Match a protected gallery to all remaining held-out probes using the existing cosine metric. Test identity-balanced top-1 against gallery-label permutations (1,999), preserving every identity's probe cluster. Report identity-bootstrap intervals and Holm-adjusted p-values across all 12 planned native tests, not a selection of positive runs. This is a different task from learned unprotected-gallery linkage.

Using the first 32 held-out records in metadata order, apply positive scales 0.5 and 2 to the original unit-norm embeddings while holding fresh keys fixed. Measure template relative L2 change and cosine change for IoM-GRP and PolyProtect. This synthetic radial stress test checks whether the implementation is norm-sensitive; it does not demonstrate natural norm leakage, linkability from norms alone or a trained norm-based attack.

## Coverage and reporting

Keep new compact outputs under `experiments/scheme_followup_2026-09-18/` and private embeddings, identity scores and detailed metrics under ignored `results/`. Export no identities, templates or keys. Compare stages in separate figure panels. Audit which historical compact summaries have local detailed sources; do not overwrite the historical inventory with a partial scan. Human novelty/theorem review, venue selection and licensing/ethics approval cannot be completed by a numerical run.