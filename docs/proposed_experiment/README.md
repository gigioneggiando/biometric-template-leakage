# Proposed experiment readiness

**Status checked: 2026-09-18**, against `4352eeb`. BioHash key-pool evidence now covers MOBIO/LFW/FEI/SCface: 73 conditions in 12 source-separated studies. FEI (2026-09-12) and SCface (2026-09-18) complete two added datasets; approved IoM-GRP/PolyProtect pilots cover 24 cells and 72 model endpoints. See the [September update](../../reports/Sept_Dataset_Update.pdf) and [current gates](../../reports/final_research_status.md).

Implemented now: deterministic key generation, a BioHash reference interface, identity/key-disjoint synthetic test data and real LFW/Olivetti/CFP/MOBIO protocols, single-template MLP and masked permutation-invariant DeepSets extraction, ArcFace extraction, gallery/probe linkage and verification metrics, leakage checks, and run artifacts.

The Month 1 single-template baseline is complete over three real datasets, six protocol variants, and three model seeds. It found no useful recovery under independent unseen keys and strong positive fixed-transform calibrations. The 64/128/256-bit sweep was also null. Synthetic data is excluded from this conclusion.

The authorized MOBIO face data is prepared locally. Preregistered 1/2/5/10 runs with BioHash and paper-specified MLP-Hash both detected no amplification under independent unseen keys. BioHash changed from `4.17%` at one record to `3.33%` for 10-record DeepSets; MLP-Hash changed from `2.50%` to `3.33%`, against `3.33%` chance. AUROC remained near `0.5`, while shared-key and unprotected controls were strong.

The resulting paper direction combines a scoped multiplicity-invariance theorem with a positive deployment boundary. The [theorem](../theory/multiplicity_invariance.md) requires fixed norms, independent hidden rotationally invariant projections and the stated side-information assumptions; it does not cover PolyProtect. In recurring pools, a MOBIO split's pool 5 rose from `4.3%` (one record) to `51.1%` (ten records), and dense pool 4 from `3.5%` to `54.0%`. The boundary varies with partition and dataset. LFW pool 10 reaches `25.3%` but fails the strict interval criterion; SCface pools 1/2/3 pass while pool 4 is seed-sensitive. Failed criteria and chance-compatible learned attacks are not equivalence or privacy proofs.

## Completed follow-up and available outputs

The [2026-09-18 MOBIO/FEI follow-up](../../experiments/scheme_followup_2026-09-18/README.md) completed 24 cells / 216 endpoints in 859.63 seconds: IoM-GRP and PolyProtect, two new identity assignments, three model seeds, fresh/shared/pool-4 conditions and matched 120-epoch caps. All eight primary pool-4 amplification contrasts have positive crossed-bootstrap intervals and Holm p = 0.004. Fresh learned endpoints remain chance-compatible, not equivalent to chance.

The historical native PolyProtect values were `12.73/13.73/10.66%` on MOBIO/FEI/SCface. New MOBIO/FEI native controls reject their gallery-label permutation null in all 12 cases (Holm p = 0.006). Synthetic radial stress leaves IoM-GRP unchanged and changes PolyProtect; it is not a natural norm-leakage experiment or a causal explanation of native matching. SCface has no new follow-up because local embeddings were unavailable.

Available deliverables: [nine-page findings report](../../reports/Sept_Dataset_Update.pdf), [eight-slide deck](../../reports/slides/research_review.pdf), [editable PowerPoint](../../reports/slides/research_review.pptx), [15-figure appendix](../../reports/slides/figure_appendix.pdf), and [849-row local inventory](../../experiments/multiexposure_run_matrix.csv) from 49 artifacts. Overview and detailed attacker diagrams are separate. The [coverage audit](../../experiments/scheme_followup_2026-09-18/coverage_audit.csv) identifies missing SCface details and legacy schemas.

Broader confirmation, approved equivalence margins, natural norm-leakage experiments and independent review remain open. Exact `benchmark_cb` claims remain blocked by its unavailable source. The original Month 1/2 results above remain historical; the new follow-up is a separate hash-frozen study against base commit `4352eeb`.
