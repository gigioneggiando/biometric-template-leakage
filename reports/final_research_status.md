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

The preregistered exploratory MOBIO multi-exposure run tested 1/2/5/10 records with mean pooling, max pooling, and DeepSets. Independent unseen-key top-1 stayed between `2.64%` and `4.17%` against `3.33%` chance; all three 10-exposure models were exactly at chance, AUROC remained near `0.5`, and every run-level identity-clustered interval included chance. DeepSets changed by `-0.83` percentage points from 1 to 10 exposures, so the preregistered amplification criterion failed. The unprotected 10-exposure oracle reached `100%`, while shared-key mean pooling reached `87.36%` at five exposures, supporting pipeline sensitivity.

A preregistered cross-scheme run repeated the experiment with paper-specified MLP-Hash and new key/set/model seeds. Independent-key top-1 remained at chance for every exposure level and architecture: one-record top-1 was `2.50% +/- 1.10%`, while 10-record DeepSets was `3.33%`, AUROC `0.4998`, and EER `49.81%`. The unprotected oracle remained `100%`; shared-key mean pooling reached `80.83%` at five records. The second amplification criterion also failed.

## Multiplicity-invariance proposition

Let every source embedding have fixed norm and let each protected record begin with an independently sampled hidden Haar-distributed orthogonal or semi-orthogonal projection. For any two source vectors of equal norm, rotational invariance makes the projected-vector distributions identical. Any subsequent measurable transformation, including sign thresholding or independently randomized nonlinear layers, preserves that equality in distribution. With independent fresh keys, the joint distribution of any finite number of protected records is therefore independent of the source identity: $I(Y; T_1,\ldots,T_n)=0$. Under a uniform closed-set prior, Bayes-optimal top-1 identification is exactly chance for every $n$.

This proposition explains both cross-scheme null results and upgrades the contribution from an unsuccessful attack to a scoped impossibility result. It is not a universal irreversibility theorem. It does not cover non-normalized embeddings, biased or correlated projections, finite-key defects, key leakage, key reuse, implementation side channels, or transformations lacking rotational invariance. Those violations define the positive experimental boundary for the paper.

The first boundary experiment found a large key-reuse effect, but used session-aligned pool assignment. At 10 records, mean-pool top-1 decreased from `66.39%` with one recurring transform to `61.11%`, `47.64%`, and `33.89%` with pools of 2/5/10, then collapsed to `2.92%` with fresh keys. A preregistered sample-randomized confirmation retained `77.50%`, `69.44%`, and `46.94%` for pools 1/2/5 but pool 10 fell to `5.56%`, equal to its fresh endpoint. Thus the all-pools confirmation criterion failed. The surviving positive result is a severe small-pool reuse regime and a protocol-specific threshold between 5 and 10 transforms.

Three further preregistered runs generalized this. On a new identity partition, pools 1/2/5 gave `81.67%/73.89%/51.11%` and pool 10 `5.56%`. A dense BioHash sweep gave `65.00%/54.03%/17.36%/34.44%/10.42%/3.89%` for pools 3/4/6/7/8/9, placing the boundary near 7-9 with visible seed noise. Paper-specified MLP-Hash gave `71.39%/68.89%/22.92%/1.94%` for pools 1/2/5/10. The central finding is that multiplicity amplification exists only under transform reuse: for pools 4-7 a single record is at chance (`3.5-4.3%`) while ten records recover `34-54%`, whereas fresh-key 1-record and 10-record rates coincide in every run. This is the empirical counterpart of the fresh-key invariance theorem in `docs/theory/multiplicity_invariance.md`.

## Limitations and next work

These studies use one ArcFace checkpoint and a local BioHash reference not cross-checked against unavailable official code. The primary cross-dataset table uses one identity assignment, while larger LFW and CFP add three identity assignments, three key seeds, and three model seeds. Those cells share fixed datasets and pipeline components, so they are dependent sensitivity checks rather than independent replications. Identity-clustered percentile intervals are descriptive, can under-cover, and were inspected without familywise error correction. Chance inclusion does not prove equivalence or irreversibility. None of the protocols is comparable to the paper's MOBIO protocol or official implementation.

Continue requesting a corrected `benchmark_cb` source; keep the reproduction blocked until then. Repeat the 3-9 sweep on two more partitions, add MLP-Hash pools 3/4, add a Haar sign-corrected projection variant, and run non-normalized, same-image/different-key, and shuffled-record controls. A high-tier claim still requires independent proof review, at least one source-exact published transform, a second dataset, a literature recheck on IEEE Xplore and Google Scholar, and statistical equivalence rather than failure-to-reject significance tests.

## Commands

Month 1 targets are listed in the `Makefile`; equivalent Python commands are documented in `docs/protocols/real_datasets_month1.md`. They require local authorized datasets and hash-verified model assets. Exact benchmark commands remain withheld until the official upstream protocol is recovered.
