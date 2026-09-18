# Final research status

## Findings update: 2026-09-18

**Recurring hidden transforms permit substantial multi-record linkage in the tested protocols; fresh-key learned endpoints remain chance-compatible.** The completed bounded follow-up adds model-seed and identity-partition sensitivity, not a universal privacy result or a complete cross-dataset confirmation matrix.

Completed: FEI adds a third multi-exposure dataset to MOBIO/LFW, with 200 identities, 2,378 usable embeddings, and three model seeds. Its ten-record fresh-key top-1 is 1.77% versus 2.50% chance; tested recurring pools 1/2/3/4/5/7 pass, while pool 10 fails. No additional training was needed for this presentation audit because the completed run and compact summary already exist.

On 2026-09-18 Sani supplied the authorized SCface archive directly (see [local data setup](../docs/setup/SCFACE_LOCAL_DATA.md)). SCface adds a fourth multi-exposure dataset: a mugshot gallery matched against visible surveillance probes from seven cameras at three distances, 130 identities, 2,851 usable embeddings, and three model seeds. Unprotected mugshot-to-surveillance matching reaches 84.375% top-1 against a 544-probe test set. Its ten-record fresh-key top-1 is 3.85% versus 3.846% chance; tested recurring pools 1/2/3 pass the all-seed clustered-interval criterion, while pools 4/5/7/10 do not. [Results and caveats](../experiments/scface_multiexposure/README.md).

The user subsequently reported Sani's approval of paper-specified IoM-GRP and PolyProtect and authorized pilots for up to one hour. Both were implemented and frozen at `d5f4e89` for MOBIO/FEI (16 cells, 48 model runs, 277.89 seconds on CPU) and at `69a93e4` for SCface (8 cells, 24 model runs, 128.22 seconds on CPU). At pool 4, mean-pool ten-minus-one gains are 37.92/33.75/34.62 points for IoM-GRP on MOBIO/FEI/SCface and 30.00/58.13/41.83 for PolyProtect, with positive paired 95% intervals conditional on one seed. These are pilots, not confirmation. [MOBIO/FEI results and caveats](../experiments/scheme_extension_pilot/README.md); [SCface results and caveats](../experiments/scface_scheme_extension_pilot/README.md).

Fresh-key uncertainty remains broad: no endpoint meets the illustrative +/-1-point equivalence band. Native fresh-key PolyProtect protected-gallery top-1 reaches 12.73%/13.73%/10.66% against 3.33%/2.50%/3.846% chance on MOBIO/FEI/SCface. This is distinct from learned unprotected-gallery linkage and prevents a general privacy claim. PolyProtect is outside the rotational-invariance theorem.

The subsequent authorized [MOBIO/FEI follow-up](../experiments/scheme_followup_2026-09-18/README.md) completed 24 cells / 216 endpoints in 859.63 seconds. IoM-GRP and PolyProtect were tested on two new identity partitions with three model seeds, fresh/shared/pool-4 conditions and matched 120-epoch caps. All eight primary pool-4 mean-pool amplification contrasts have positive crossed-bootstrap 95% intervals and Holm p = 0.004. All 12 fresh PolyProtect native matching tests exceed their gallery-label permutation null (Holm p = 0.006). IoM-GRP is unchanged by positive radial scaling; PolyProtect changes, but this synthetic sensitivity is not natural norm leakage or a causal explanation of native linkage. Fresh learned intervals include chance; no equivalence claim follows.

The presentation contains three diagrams, twelve result plots, an eight-slide editable deck/PDF, a 15-figure appendix and a [nine-page September update](Sept_Dataset_Update.pdf). Architecture overview and attacker details are separate. Base integration is `4352eeb`; the new run records separate source/configuration hashes. Earlier 73-condition/12-study results, 72 pilot endpoints and 216 follow-up endpoints remain distinct. The inventory contains 849 rows from 49 artifacts, preserving all previous 633 rows. The [coverage audit](../experiments/scheme_followup_2026-09-18/coverage_audit.csv) identifies two legacy-schema sources and unavailable SCface details; tracked SCface aggregates still feed figures directly. Export checks cover text overlap, bounds, box padding and unsupported dashes. Native PowerPoint rendering still needs a check on the presenting machine.

| Remaining gate | Current status / next action |
|---|---|
| Second additional dataset beyond MOBIO/LFW | FEI and SCface are both complete as added-dataset BioHash key-pool studies (pilot-grade, one identity assignment each). AgeDB remains an optional third addition; access is not yet available. |
| Two additional protection families | Paper-specified implementations, MOBIO/FEI/SCface pilots and three-seed/two-partition MOBIO/FEI follow-up complete; full cross-dataset confirmation remains open. |
| Confirmatory matrix | Current LFW/FEI/SCface studies cover BioHash endpoints 1 and 10, not all schemes, attackers, exposures, and partitions requested in the roadmap. |
| Statistical inference | Follow-up crossed seed/identity intervals and prespecified Holm families complete. Approved equivalence margins, older-study inference and full historical coverage remain open. |
| Theory and implementation | Native permutation and synthetic radial controls complete; natural norm leakage, causal explanation and independent human review remain open. |
| Novelty and venue fit | Independent related-work review, realistic key-reuse motivation, and comparison to the selected venue's closest work. An unavailable benchmark blocks an exact reproduction claim, not every possible high-tier independent paper. |
| Professor review | Review the manuscript and eight-slide package; record decisions before expanding experiments. |

See [figures/README.md](figures/README.md), [slides/research_review.pdf](slides/research_review.pdf), and [../docs/ROADMAP.md](../docs/ROADMAP.md). No biometric images, templates, keys, or model weights are included in the presentation package.

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

The cross-scheme null results are consistent with this idealized proposition, but do not validate all its assumptions in the finite implementation. It is not a universal irreversibility theorem. It does not cover non-normalized embeddings, biased or correlated projections, finite-key defects, key-correlated side information, key leakage, key reuse, implementation side channels, or transformations lacking rotational invariance. Those cases define boundaries for further testing.

The first boundary experiment found a large key-reuse effect, but used session-aligned pool assignment. At 10 records, mean-pool top-1 decreased from `66.39%` with one recurring transform to `61.11%`, `47.64%`, and `33.89%` with pools of 2/5/10, then collapsed to `2.92%` with fresh keys. A preregistered sample-randomized confirmation retained `77.50%`, `69.44%`, and `46.94%` for pools 1/2/5 but pool 10 fell to `5.56%`, equal to its fresh endpoint. Thus the all-pools confirmation criterion failed. The surviving positive result is a severe small-pool reuse regime and a protocol-specific threshold between 5 and 10 transforms.

Three further preregistered runs extended the evidence. On a new identity partition, pools 1/2/5 gave `81.67%/73.89%/51.11%` and pool 10 `5.56%`. A dense BioHash sweep gave `65.00%/54.03%/17.36%/34.44%/10.42%/3.89%` for pools 3/4/6/7/8/9, with visible seed sensitivity and non-monotonicity. Paper-specified MLP-Hash gave `71.39%/68.89%/22.92%/1.94%` for pools 1/2/5/10. Large multi-record gains occur in the tested reuse regimes, sometimes from near-chance single-record means, but not universally: BioHash dense A pool 3 already has `27.50%` single-record linkage. Fresh-key means vary slightly across exposures; they do not coincide exactly in every run.

Across three MOBIO dense studies, pools 3/4 pass the interval criterion in all three partitions (pooled `56.7% / 51.5%`), pools 5-7 are partition-dependent, and tested pools 8/9 fail that criterion in all three. Failure is not equivalence to chance. Haar sign-corrected BioHash gave `74.6 / 48.1 / 2.6%` for pools 1/5/fresh; the ideal sampling argument still needs separate treatment of finite keys and numerical precision. MLP-Hash pools 3/4 gave `54.3 / 37.8%`. LFW fresh keys gave `4.0%` against `4.0%` chance; pool 10 gave `25.3%` but failed the strict interval rule. FEI fresh keys gave `1.8%` against `2.5%` chance; tested pools 1/2/3/4/5/7/10 gave `76.9 / 63.4 / 54.8 / 47.5 / 37.5 / 23.6 / 4.0%`. Pool 10 fails; untested pools 6/8/9 cannot locate a precise threshold. The source-separated study table is `experiments/cross_dataset_key_pool_summary.csv`.

Two preregistered mechanism controls strengthen the interpretation. On a new paired MOBIO partition, hidden-slot DeepSets gave `55.3/46.3/32.9/23.8%` for pools 3/4/5/7 and `3.33%` fresh; providing the correct transform-slot label changed these by only `+1.8/+4.4/+0.7/-0.8` points. In the shuffled-non-anchor control, retaining one correct record but replacing the other nine with other identities collapsed pools 3/4 and fresh keys to exactly `3.33%` for every seed. The gain therefore requires multiple same-identity records and is not primarily a set-size, transform-frequency, or hidden-slot-identification artefact.

The same-image control removed the remaining image/session-variation explanation: protecting one identical normalized embedding under ten distinct fresh keys still gave exactly `3.33%` top-1 for every seed (AUROC `0.4997`). Controlled correlated-key sweeps then shared an exact prefix of each 128-dimensional BioHash projection. On an independent fine-sweep partition, ten-record top-1 was `3.33/3.75/6.94/7.64/14.17/35.83/49.31/42.64%` as the shared fraction increased through `0/12.5/18.75/25/31.25/37.5/43.75/50%`. Leakage was consistently large from 37.5% onward, while the lower transition region was seed-sensitive. This establishes a graded correlation-dependent regime for the tested construction, not a universal threshold.

## Limitations and next work

These studies use one ArcFace checkpoint and a local BioHash reference not cross-checked against unavailable official code. The primary cross-dataset table uses one identity assignment, while larger LFW and CFP add three identity assignments, three key seeds, and three model seeds. The new MOBIO/FEI follow-up uses two overlapping assignments and three model seeds with fixed training key/set seeds. These cells share datasets and pipeline components, so they are sensitivity checks rather than independent populations. Older identity-clustered intervals were inspected without familywise correction; the follow-up corrects only its prespecified primary and native families. Bootstrap intervals can under-cover, and chance inclusion does not prove equivalence or irreversibility. None of the protocols is an exact reproduction of the paper's MOBIO protocol or official implementation.

Continue requesting a corrected `benchmark_cb` source; keep its exact reproduction blocked until then. Strengthen transform-source validation, independent proof and literature review, statistical equivalence analysis, and uncertainty around the correlation transition. These are concrete evidence improvements, not a guarantee of any venue rank or acceptance. The dated readiness audit above separates approval/access gates from executable follow-up work.

## Commands

Month 1 targets are listed in the `Makefile`; equivalent Python commands are documented in `docs/protocols/real_datasets_month1.md`. They require local authorized datasets and hash-verified model assets. Exact benchmark commands remain withheld until the official upstream protocol is recovered.
