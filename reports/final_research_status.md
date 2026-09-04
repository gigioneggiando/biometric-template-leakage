# Final research status

## Research question

Can a key-agnostic learned set model recover identity-discriminative information from multiple independently protected face templates?

## Literature and threat model

See `docs/literature/` and `docs/literature/threat_models.md`. The main future evaluation is unseen identities plus unseen keys; K0 knows only the scheme family and K1 additionally knows hyperparameters.

## Completed infrastructure

- Deterministic BioHash reference, key scope splitting, identity-disjoint real-data protocols, single MLP/DeepSets models, gallery/probe metrics, leakage checks, tests, configs, and per-run artifacts.
- Reusable OpenCV SCRFD/ArcFace and YuNet/ArcFace extraction backends; official `buffalo_l` and YuNet hash verification; deterministic LFW, Olivetti, and CFP protocol construction; and a three-seed Month 1 runner.
- Official GaFaR/InsightFace/Arc2Face commits recorded. The `benchmark_cb` source remains unresolved after a 2026-08-26 recheck.

## Results

No published experiment has been reproduced. The paper's face targets were verified directly from arXiv source, and authorized MOBIO face data is now prepared locally, but the official `benchmark_cb` implementation remains unavailable.

Real-image **engineering validation** was completed on LFW, Olivetti faces, and CFP. Six protocol variants cover SCRFD/YuNet preprocessing, 60/150-identity LFW subsets, and CFP frontal/profile views. Unprotected ArcFace top-1 ranged from `94.92%` to `100.00%`, showing that the source embeddings preserve identity.

Under independent unseen keys, the three-seed MLP remained at the applicable random top-1 rate on every protocol. Headline results were `3.83% +/- 0.93%` versus `3.33%` chance on the 1,500-image larger LFW protocol and `1.15% +/- 0.17%` versus `1.00%` chance on 4,999 CFP frontal embeddings. AUROC remained near `0.5`, EER near `50%`, and no per-seed descriptive exact binomial test rejected chance (`p >= 0.1205`). CFP profile and matched LFW YuNet runs showed that pose and detector choice did not change the conclusion.

The fixed-transform positive control reached `51.11%` to `91.00%` top-1. A 64/128/256-bit sweep on LFW and Olivetti also remained compatible with chance under independent keys.

The first MOBIO engineering run adds all 150 identities with one selected image from each of 12 sessions. YuNet plus ArcFace extracted 1,799/1,800 embeddings. On the 30-identity test split, unprotected ArcFace reached `100%` top-1. The shared-key learned attack reached `81.21% +/- 3.19%` top-1, while independent unseen keys reached `3.33% +/- 0.30%` against `3.33%` chance, with AUROC `0.4992` and EER `50.28%`. This is strong confirmation of the single-template null pattern on MOBIO, not an exact reproduction or proof of irreversibility.

A crossed `3 identity assignments x 3 key seeds x 3 model seeds` sensitivity study strengthened the larger LFW and CFP frontal results. Independent-key split/key cell means ranged `2.59-3.58%` versus `3.33%` chance on LFW and `0.81-1.11%` versus `1.00%` chance on CFP. All 54 run-level identity-clustered 95% intervals included chance. Fixed-transform cell means remained `66.54-77.41%` on LFW and `91.70-94.74%` on CFP. The convergent control/null pattern is the main Month 1 finding: no useful identity recovery from one independently keyed template was detected across the tested real-data protocols.

This is a stronger negative baseline, not a universal irreversibility result and not the proposed breakthrough. It does not test whether 2/5/10 observations amplify leakage. Synthetic runs are excluded from this scientific conclusion.

## Limitations and next work

These studies use one ArcFace checkpoint and a local BioHash reference not cross-checked against unavailable official code. The primary cross-dataset table uses one identity assignment, while larger LFW and CFP add three identity assignments, three key seeds, and three model seeds. Those cells share fixed datasets and pipeline components, so they are dependent sensitivity checks rather than independent replications. Identity-clustered percentile intervals are descriptive, can under-cover, and were inspected without familywise error correction. Chance inclusion does not prove equivalence or irreversibility. None of the protocols is comparable to the paper's MOBIO protocol or official implementation.

Continue requesting a corrected `benchmark_cb` source; keep the reproduction blocked until then. Authorization to begin the MOBIO experiment was given on 2026-09-04. Before interpreting any 1/2/5/10 result as the proposed contribution, preregister exposure construction, protocol seeds, and identity-clustered uncertainty analysis.

## Commands

Month 1 targets are listed in the `Makefile`; equivalent Python commands are documented in `docs/protocols/real_datasets_month1.md`. They require local authorized datasets and hash-verified model assets. Exact benchmark commands remain withheld until the official upstream protocol is recovered.
