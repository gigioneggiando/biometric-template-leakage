# Record Multiplicity Does Not Break Fresh-Key Template Protection, But Transform Reuse Does

Working draft, 2026-09-04. Every number below is traceable to a tracked summary in `experiments/mobio_multiexposure/` and a preregistration entry in `docs/protocols/multi_exposure.md`. Items marked TODO are not yet supported by evidence and must not be filled in from memory.

## Abstract

Cancelable biometric schemes such as BioHashing and MLP-Hash protect a face embedding by a secret, key-seeded random projection. A natural fear is that an attacker who collects many protected records of the same person, from different services with different keys, can pool them to recover identity even without any key. We show that this fear is unfounded under one precise condition and fully justified under another. First, we prove that for unit-norm embeddings and independently drawn rotationally invariant projections, the joint law of any number of protected records is independent of the source: $I(Y; T_1, \dots, T_n) = 0$ for every $n$, so no attacker, with any training data or compute, exceeds chance. Second, we show empirically on MOBIO (150 identities, 12 sessions) and public LFW (125 identities, 12 images) with ArcFace embeddings that this guarantee collapses as soon as hidden transforms recur. With a pool of 4 to 7 recurring hidden BioHash transforms, a single protected record is at chance (3.5-4.3% top-1 over 30 identities) yet ten records pooled by a permutation-invariant attacker recover 34-54% of identities. The effect vanishes near 8-10 transforms and is absent under fresh keys in every run. The pattern replicates across identity partitions and for paper-specified MLP-Hash. A shuffled-record control collapses the recurring-pool result to chance, while true slot labels improve a paired DeepSets attacker by at most 4.44 points. Record multiplicity is therefore not a privacy risk per se; it is an amplifier whose gain is set by the diversity of the deployed transforms.

## 1. Introduction

TODO: motivation, deployment reality (application-specific keys, shared salts), gap in the literature.

Contributions:

1. A fresh-key multiplicity invariance theorem with explicit assumptions (Section 3) and a norm-leakage corollary.
2. A key-blind attacker for sets of protected records (single-template MLP, mean/max pooling, DeepSets) and an identity-disjoint, key-disjoint evaluation protocol on MOBIO with preregistered endpoints.
3. The first measurement, to our knowledge, of leakage as a function of the number of hidden recurring transforms, showing a sharp regime change and multiplicity amplification that exists only under reuse.
4. Cross-scheme (BioHash, MLP-Hash), cross-partition (three MOBIO partitions), and cross-dataset (MOBIO, LFW) replication, with all preregistered failures reported.
5. Mechanism controls showing that the gain requires multiple records from the same identity and is not primarily limited by hidden transform-slot identification.

## 2. Threat model

Attacker capabilities: knows the scheme family and hyperparameters; observes $n \in \{1, 2, 5, 10\}$ protected records of a target from different images; never observes any key; may train on protected records and unprotected embeddings of disjoint identities. Goal: link the target to a gallery of unprotected embeddings (30 identities, one image each; chance 3.33%).

Conditions:

- **Fresh keys (K0).** Every record has its own key; train/validation/test key pools are disjoint. Covered by Theorem 1.
- **Recurring pool of size $k$ (R-$k$).** A hidden pool of $k$ transforms is drawn once and each record is assigned one by a hash of its sample ID. Keys recur across identity splits; slot labels are hidden. $k = 1$ is the unknown-shared-token setting; $k = 1799$ (one per record) equals K0.
- **Controls.** Unprotected oracle (100% in every run); shared-key calibration.

Prior stolen-token attacks (Nagar et al. 2010; Lacharme et al. 2013; Feng et al. 2014; Dong et al. 2019, 2022; Wang et al. 2020; Ghammam et al. 2020; Durbet et al. 2021) assume the transform is known. Record multiplicity has been analyzed for fuzzy vaults (Scheirer and Boult 2007; Merkle and Tams 2013), where no secret rotation is involved. We found no prior treatment of R-$k$ with $k > 1$ or of the fresh-key invariance for deep embeddings; see `docs/theory/multiplicity_invariance.md` for search coverage and the required IEEE Xplore / Google Scholar recheck.

## 3. Theory

Statement and proof: `docs/theory/multiplicity_invariance.md`. Summary: if $P_K R \overset{d}{=} P_K$ for all $R \in O(d)$, then for unit $x, y$, $P_K x \overset{d}{=} P_K y$; with independent keys the joint law of $(P_{K_i} x_i)_i$ is a product of source-independent factors, hence $(T_1, \dots, T_n) \perp (Y, x_{1:n})$. Corollaries: chance-level linkage for any attacker and any $n$; only embedding norms can leak when inputs are not normalized.

Scope: the theorem covers i.i.d. Gaussian and Haar/Stiefel projections. It does not cover key reuse, correlated keys, non-invariant transforms, or side channels. Implementation caveat: `numpy.linalg.qr` without sign correction is not exactly Haar (Mezzadri 2007). A preregistered sign-corrected variant (`haar_sign_corrected: true`) gave fresh-key 10-record top-1 2.64%, pool 1 74.58%, pool 5 48.06% (`haar_corrected_key_pool_summary.csv`), indistinguishable from the default construction; the theorem therefore covers an executed configuration.

## 4. Experimental setup

- Data: MOBIO selected still images, 150 identities, 12 sessions, 1,799 embeddings (one detection failure), 90/30/30 identity-disjoint splits; one gallery image per identity held out; eight nested exposure permutations per identity; 720/240/240 attack sets per level.
- Embeddings: InsightFace `buffalo_l` ArcFace (SHA-256 recorded), YuNet detection, L2-normalized.
- Protection: 128-bit BioHash (key-seeded orthonormal Gaussian projection, sign threshold); paper-specified MLP-Hash (512-1024-1024-1024-512, ReLU, semi-orthogonal key-seeded layers, output-mean binarization; not source-exact, authors' repository unavailable).
- Attackers: single-template MLP (n=1); mean-pool MLP, max-pool MLP, DeepSets (n>1); hidden 256; cosine + 0.1 MSE loss; 400 epochs, patience 60; three model seeds.
- Metrics: top-1/top-5 linkage against the unprotected gallery, AUROC, EER, TAR@FAR, 2,000-resample identity-clustered 95% intervals. Preregistered per-pool criterion: all clustered intervals above chance and at least five points over the fresh endpoint.

## 5. Results

### 5.1 Fresh keys: no leakage, no amplification

10-record DeepSets top-1 under K0: BioHash 3.33% (AUROC 0.4988), MLP-Hash 3.33% (AUROC 0.4998); one-record 2.50-3.33%. Unprotected oracle 100%; shared-key mean pooling up to 80.83% at five records. Across the nine later runs the fresh-key 10-record mean-pool top-1 ranged 1.53-5.56% (chance 3.33%) and never differed from the 1-record rate by more than 2.4 points: (1-record, 10-record) = (3.2, 5.6), (2.9, 3.1), (4.0, 3.6), (2.4, 1.5), (3.8, 4.4), (3.1, 2.6), (3.1, 3.5). Source: `results_summary.csv`, `mlphash_results_summary.csv`, and the `*_summary.csv` files.

### 5.2 Recurring transforms: leakage rises sharply with reuse

10-record mean-pool top-1 (1-record single-MLP in parentheses), randomized assignment. BioHash partitions A, 2, 3 are three identity-disjoint 90/30/30 partitions of MOBIO:

| pool size | BioHash A (dense) | BioHash 2 | BioHash 3 | BioHash B (1/2/5/10) | MLP-Hash |
|---|---|---|---|---|---|
| 1 | - | - | - | 81.67 (75.97) | 71.39 (52.08) |
| 2 | - | - | - | 73.89 (35.00) | 68.89 (33.61) |
| 3 | 65.00 (27.50) | 48.61 (22.36) | 56.39 (5.83) | - | 54.31 (3.06) |
| 4 | 54.03 (3.47) | 48.61 (7.64) | 51.94 (5.42) | - | 37.78 (4.58) |
| 5 | - | 40.28 (6.39) | 8.06 (4.86) | 51.11 (4.31) | 22.92 (4.44) |
| 6 | 17.36 (3.47) | 36.39 (6.39) | 8.61 (4.58) | - | - |
| 7 | 34.44 (4.17) | 30.42 (5.00) | 8.89 (5.69) | - | - |
| 8 | 10.42 (4.03) | 14.17 (3.19) | 3.89 (3.06) | - | - |
| 9 | 3.89 (3.19) | 6.39 (2.50) | 6.67 (4.72) | - | - |
| 10 | - | - | - | 5.56 (4.31) | 1.94 (4.58) |
| fresh | 5.56 (3.19) | 1.53 (2.36) | 4.44 (3.75) | 3.61 (4.03) | 3.06 (2.92) |

Preregistered pooled rule over partitions A/2/3 (`dense_key_pool_pooled_analysis.csv`): pools 3 and 4 pass in 3/3 partitions (pooled 56.67%, 51.53%); pool 7 in 2/3 (24.58%); pools 5 and 6 in 1/2 and 1/3 (24.17%, 20.79%); pools 8 and 9 in 0/3 (9.49%, 5.65%); fresh pooled 3.84%. MLP-Hash: pools 1-4 pass, pool 5 fails on the interval criterion only (one lower bound 0.0; seed std 19.9 points), pool 10 fails. Regimes for this protocol: robust leakage at $k \le 4$; partition-dependent transition at $k = 5$-$7$; null at $k \ge 8$ (BioHash) and $k \ge 5$ (MLP-Hash, interval criterion).

### 5.3 Multiplicity amplification is gated by transform diversity

Amplification = 10-record minus 1-record top-1. Pool 3: +37.5, +26.3, +50.6 (BioHash A/2/3), +51.3 (MLP-Hash); pool 4: +50.6, +41.0, +46.5, +33.2; pool 5 (partition B): +46.8; Haar-corrected pool 5: +44.6; pool 9: +0.7, +3.9, +1.9; fresh: -0.4 to +2.4 in every run. A single record under R-3 to R-7 is indistinguishable from a fresh-key record, yet ten such records identify a third to a half of the gallery. Record multiplicity is the amplifier; transform diversity sets the gain.

### 5.4 Session-aligned assignment inflates the curve

The first boundary run assigned keys by session index and gave 33.89% at pool 10; randomized assignment gave 5.56%. Session-aligned reuse is a plausible deployment pattern (one key per capture device or session) and is reported separately, not pooled.

### 5.5 Second dataset: LFW

Public funneled LFW, 125 identities x 12 images, 75/25/25 identity-disjoint split, chance 4.00% (`experiments/lfw_multiexposure/key_pool_boundary_summary.csv`). Fresh keys: 10-record top-1 exactly 4.00% with zero seed variance (1-record 4.67%), AUROC 0.505. Recurring pools 1/2/3/4/5/7/10: 73.17 / 63.17 / 62.50 / 42.50 / 41.00 / 32.00 / 25.33% (1-record 70.67 / 37.33 / 23.83 / 16.83 / 11.50 / 11.67 / 4.33%). Pools 1-7 pass; pool 10 fails only the interval criterion. The qualitative structure transfers; the boundary is later than on MOBIO (pool 10 still 25.3%), so its location is dataset-specific.

### 5.6 Mechanism controls

On a new paired MOBIO partition, hidden-slot DeepSets gave 10-record top-1 `55.28 / 46.25 / 32.92 / 23.75%` for pools 3/4/5/7 and `3.33%` for fresh keys. Supplying the true recurring-transform slot to the per-record encoder gave `57.08 / 50.69 / 33.61 / 22.92%`, differences of only `+1.81 / +4.44 / +0.69 / -0.83` points. Hidden-slot mixture identification is therefore not the main limitation in this range.

In a separate shuffled-non-anchor control, each 10-record set retained one target-identity record and received nine records from other identities while preserving record count and position-wise marginals. Pools 3/4 and fresh keys all produced exactly `3.33%` top-1 for every seed with AUROC `0.499/0.503/0.500`. Thus the recurring-pool gain requires multiple same-identity records and is not a set-size or global transform-frequency artefact. The negative pool-3 change from its `18.19%` one-record baseline reflects dilution of the sole informative record under mean pooling.

## 6. Discussion

- Deployment implication: per-record fresh salts make record multiplicity harmless in the idealized model; application-wide or device-wide keys make multiplicity a strong amplifier even when the key is never exposed.
- Boundary location is protocol- and partition-specific and must be reported as a range: partition 3 collapsed at $k = 5$ while partitions A and 2 held to $k = 7$; pool 6 vs 7 non-monotonicity within partition A (seed std 18 points) shows that single-seed points near the boundary are unreliable.
- Why the collapse: as $k$ grows, the number of training records per transform falls as $1080/k$ and fewer same-transform relations recur within a set. The paired key-slot control changes top-1 by at most 4.44 points, so explicit mixture labels do not remove the boundary; loss of repeated cross-record structure is the stronger explanation under this attacker.

## 7. Limitations

Two datasets (MOBIO restricted, LFW public), each with a single embedding model; 30 or 25 test identities per partition; three model seeds; MLP-Hash is paper-specified, not source-exact; `benchmark_cb` unavailable (404); the key-slot control exposes transform identifiers but not transform values; equivalence rather than significance testing for the fresh-key null is still to be added; novelty recheck on IEEE Xplore / Google Scholar pending.

## 8. Reproducibility

All configurations, preregistrations, compact summaries, and hashes are in the repository. Restricted MOBIO data, embeddings, keys, and full metrics remain local. Commands: `experiments/mobio_multiexposure/README.md`.
