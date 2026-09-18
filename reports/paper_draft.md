# Hidden Transform Reuse Amplifies Linkage from Protected Face Records

Working draft, revised 2026-09-19. Fixed-pool follow-up, subsequent independent-pool study, earlier exploration and raw-norm audit remain separately labeled. Later evidence does not retroactively change the original primary family. No independent human review or source-exact reproduction is claimed.

## Abstract

We study how hidden transform reuse conditions the benefit of combining protected face records. An attacker trains on paired examples from the same hidden pool but disjoint identities, then links one or ten same-person records to a small closed gallery. A fixed-pool MOBIO/FEI study of IoM-GRP and PolyProtect spans three model seeds and two identity assignments: 216 trained endpoints and eight positive planned pool-4 contrasts (21.25-40.83 percentage points; Holm p = 0.004). A prospective follow-up adds three independently drawn pools, 144 fits and 72 prediction-mean evaluations. IoM gains persist across tested pools, but PolyProtect gains range from -3.23 to +72.40 points. All direct input-mean versus prediction-mean intervals include zero; superiority is not established. Separate audits expose shared-key DeepSets regressions and do not establish identity-specific natural norm leakage. Prior work already studies multiplicity, joint-score maximal linkability, adaptive identity extraction and residual naive-parameter PolyProtect linkage. Our contribution is the controlled hidden-reuse comparison and its boundaries, not those general observations. Chance-compatible attacks do not establish privacy.

## 1. Introduction

Retained templates can expose several records grouped by an account pseudonym even when real identity and protection keys remain unknown. We study a strong access scenario: paired training examples and targets share the same realized hidden transform pool. We do not claim that this policy is prevalent in products. The question is whether same-person aggregation helps under reuse, and where that statement fails.

Contributions:

1. **Reuse-conditioned amplification:** eight corrected fixed-pool contrasts, followed by three new pools where IoM gains persist but PolyProtect is pool-sensitive. Earlier four-dataset sweeps are not pooled into these inference claims.
2. **Limits on aggregation:** mechanism controls, shared-key regressions and a competitive prediction-mean baseline constrain interpretation. Neither more records nor a set-trained model is universally better.
3. **Separate native and learned attack surfaces:** reference implementation/matcher checks and genuine raw/shuffled/fixed-radius controls validate the local native computation without attributing it to natural norm leakage or stronger parameter policies.

### Closest research

Li and Hu (2014, DOI 10.1002/cpe.3042) already attack multiple fingerprint templates with disclosed parameters. PolyProtect (2022), IV-C3, evaluates inversion of 1-10 versions of the same embedding with disclosed coefficients/exponents; IV-D finds residual different-image linkage under naive parameters and reduces it through stricter selection. Our different-image hidden-pool learned task differs, but multiplicity and native residual linkage are not novel.

The cancelable-biometrics benchmark already compares recognition, unlinkability and information estimates, including sample-specific keys. FaceLinkGen v3 (3 September 2026) already trains adaptive ArcFace-aligned extractors from paired data under unknown per-query randomness. IoM magnitude independence is prior art. Otroshi Shahreza, Shkel and Marcel (IEEE Access 2024, DOI 10.1109/ACCESS.2024.3433536) study joint-score maximal linkability across modalities, encoders, schemes, keys and scoring functions. The full corresponding author-thesis section 5.4 was inspected; the publisher PDF was blocked and version identity is not certified. Its binary mated/non-mated information measure is not our closed-set top-1. Our recurring-pool sweep and trained different-image aggregation differ from its experiments; multiplicity and multi-key leakage are not new. See the [full-text evidence](../docs/literature/closest_work_2026-09-18.md). This bounded review does not establish global priority.

## 2. Threat model

Attacker capabilities: knows the scheme family and hyperparameters; observes $n \in \{1, 2, 5, 10\}$ protected records of a target from different images, except in the same-image control; never observes key values; may train on paired protected records and unprotected embeddings of disjoint identities. Goal: link the target to a held-out unprotected gallery, with one image per identity. Gallery sizes are 30 on MOBIO, 25 on LFW, and 40 on FEI, giving chance rates of 3.33%, 4.00%, and 2.50%. LFW and FEI boundary studies use endpoints 1 and 10, not the full exposure sweep.

Conditions:

- **Fresh keys (K0).** Every source record has its own key; train/validation/test key pools are disjoint. The theorem describes an idealized rotationally invariant version of this condition, not every finite seeded implementation.
- **Recurring pool of size $k$ (R-$k$).** A hidden pool of $k$ transforms is drawn once and each record is assigned one by a hash of its sample ID. Keys recur across identity splits; slot labels are hidden. $k = 1$ is the unknown-shared-token setting. Increasing pool size to the number of records does not create K0 because hash assignment can still collide; K0 explicitly generates a distinct key per source record.
- **Controls.** Unprotected oracle and shared-key calibration. Earlier MOBIO/LFW/FEI setups reach 100%; SCface's camera-shift oracle is 84.375%, not 100%.

**Access justification.** Persistent account/session identifiers can group records without revealing gallery identity. An authorized enrollment/query interface using consented faces, or a provider observing originals and protected outputs, could supply paired training data. Recurring-pool training must use the same realized hidden pool as the targets; an unrelated-key proxy is insufficient. Lawful public or consented images could supply a reference gallery. Here target membership is guaranteed among only 25-40 identities (SCface: 26); gallery images are excluded from exposures. Open-set search, internet-scale distractors, unknown grouping and cross-provider transfer are untested. Fresh independent keys can impair legitimate matching and are not a validated drop-in defense.

Prior stolen-token attacks (Nagar et al. 2010; Lacharme et al. 2013; Feng et al. 2014; Dong et al. 2019, 2022; Wang et al. 2020; Ghammam et al. 2020; Durbet et al. 2021) assume the transform is known. Record multiplicity has been analyzed for fuzzy vaults (Scheirer and Boult 2007; Merkle and Tams 2013), where no secret rotation is involved. PolyProtect (Krivokuca Hahn and Marcel 2022, Section 4.3) already studies one to ten records with disclosed parameters. Our hidden-parameter learned linkage task differs, but multiplicity alone is not novel. Priority claims await an independent current literature review; see the [local review memo](../docs/review/scheme_pilot_review_2026-09-12.md).

## 3. Theory

Statement and proof: [multiplicity_invariance.md](../docs/theory/multiplicity_invariance.md). Summary: if $P_K R \overset{d}{=} P_K$ for all $R \in O(d)$, then for unit $x, y$, $P_K x \overset{d}{=} P_K y$; with independent keys the joint law is a product of source-independent factors. Under a uniform identity prior, expected Bayes top-1 is chance for every record count. With admissible side information Z, joint independence of key randomness from identity, sources and Z is required; templates give no gain beyond the Bayes decision from Z alone. Without normalization, norms bound possible information, but need not leak: positive scaling leaves zero-threshold BioHash and IoM-GRP unchanged. This is not a finite-implementation or PolyProtect privacy theorem.

Scope: the theorem assumes ideal Gaussian or Haar/Stiefel sampling, independent hidden keys, fixed-norm sources, and source-independent postprocessing. It does not cover key reuse, correlated keys, non-invariant transforms, or key-correlated side information. Raw `numpy.linalg.qr` does not implement the Haar sign convention (Mezzadri 2007). The sign-corrected variant gave fresh-key 10-record top-1 2.64%, pool 1 74.58%, and pool 5 48.06% (`haar_corrected_key_pool_summary.csv`). These results are qualitatively similar to the default construction; no equivalence test was performed. Sign correction aligns the ideal sampling construction, but finite PRNG keys and numerical precision remain implementation assumptions requiring review.

## 4. Experimental setup

- Data: MOBIO selected still images, 150 identities, 12 sessions, 1,799 embeddings (one detection failure), 90/30/30 identity-disjoint splits; one gallery image per identity held out; eight nested exposure permutations per identity; 720/240/240 attack sets per level.
- Embeddings: InsightFace `buffalo_l` ArcFace (SHA-256 recorded), YuNet detection, L2-normalized.
- Protection: 128-bit BioHash (key-seeded orthonormal Gaussian projection, sign threshold); paper-specified MLP-Hash (512-1024-1024-1024-512, ReLU, semi-orthogonal key-seeded layers, output-mean binarization; not source-exact, authors' repository unavailable).
- Attackers: single-template MLP (n=1); mean/max-pool MLP and DeepSets (n>1); hidden 256; cosine + 0.1 MSE. Earlier studies use 400 epochs/patience 60; matched follow-up uses 120/patience 30, three seeds and mean/DeepSets at n=10. Target: normalized mean of exposed source embeddings, not the gallery.
- Metrics: top-1/top-5 linkage against the unprotected gallery, AUROC, EER, TAR@FAR, 2,000-resample identity-clustered 95% intervals. Preregistered per-pool criterion: all clustered intervals above chance and at least five points over the fresh endpoint.

## 5. Earlier Exploratory Results (Separate Evidence)

### 5.1 Fresh keys: no useful linkage detected by the tested attacks

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

Preregistered pooled rule over partitions A/2/3 (`dense_key_pool_pooled_analysis.csv`): pools 3 and 4 pass in 3/3 partitions (pooled 56.67%, 51.53%); pool 7 in 2/3 (24.58%); pools 5 and 6 in 1/2 and 1/3 (24.17%, 20.79%); pools 8 and 9 in 0/3 (9.49%, 5.65%); fresh pooled 3.84%. MLP-Hash: tested pools 1-4 pass, pool 5 fails on the interval criterion only (one lower bound 0.0; seed std 19.9 points), pool 10 fails. These failures neither establish equivalence to chance nor support conclusions about untested pool sizes.

### 5.3 Multiplicity amplification is gated by transform diversity

Amplification is 10-record minus 1-record top-1. Pool 3 gains are +37.5, +26.3, and +50.6 points for BioHash A/2/3, and +51.3 for MLP-Hash; pool 4 gains are +50.6, +41.0, +46.5, and +33.2. Large gains can occur when the single-record mean is near chance, but this is not universal: BioHash A pool 3 already gives 27.50% single-record top-1, and LFW pool 4 gives 16.83%. Descriptive gains do not establish paired statistical significance. Fresh-key means vary slightly in both directions; use the source-separated comparison table rather than claiming exact equality across exposures.

### 5.4 Session-aligned assignment inflates the curve

The first boundary run assigned keys by session index and gave 33.89% at pool 10; randomized assignment gave 5.56%. Session-aligned reuse is a plausible deployment pattern (one key per capture device or session) and is reported separately, not pooled.

### 5.5 Second dataset: LFW

Public funneled LFW, 125 identities x 12 images, 75/25/25 identity-disjoint split, chance 4.00% (`experiments/lfw_multiexposure/key_pool_boundary_summary.csv`). Fresh keys: 10-record top-1 exactly 4.00% with zero seed variance (1-record 4.67%), AUROC 0.505. Recurring pools 1/2/3/4/5/7/10: 73.17 / 63.17 / 62.50 / 42.50 / 41.00 / 32.00 / 25.33% (1-record 70.67 / 37.33 / 23.83 / 16.83 / 11.50 / 11.67 / 4.33%). Pools 1-7 pass; pool 10 fails only the interval criterion. The qualitative structure transfers; the boundary is later than on MOBIO (pool 10 still 25.3%), so its location is dataset-specific.

### 5.5b Third dataset: FEI

FEI face database, 200 identities x 12 of 14 images, uses a 120/40/40 identity-disjoint split and 2.50% chance (`experiments/fei_multiexposure/key_pool_boundary_summary.csv`). Extraction succeeded on 2,378/2,400 images; all failures were low-illumination pose 14, and every identity retains at least 11 records. Fresh-key ten-record top-1 is 1.77% (one-record 2.29%), AUROC 0.502. Recurring pools 1/2/3/4/5/7/10 give 76.88 / 63.44 / 54.79 / 47.50 / 37.50 / 23.65 / 3.96% (one-record 74.58 / 36.35 / 3.75 / 3.44 / 2.81 / 2.40 / 3.02%). The tested pools 1, 2, 3, 4, 5, and 7 pass both criteria; pool 10 fails. Pools 3, 4, 5, and 7 show small single-record means and much larger ten-record means. Pools 6, 8, and 9 were not tested, so no exact threshold can be inferred. FEI measures controlled pose/expression variation, not longitudinal session robustness. Full key-pool overview: `reports/figures/fig_results_overview.pdf`; source-separated table: `experiments/cross_dataset_key_pool_summary.csv`.

### 5.6 Mechanism controls

On a new paired MOBIO partition, hidden-slot DeepSets gave 10-record top-1 `55.28 / 46.25 / 32.92 / 23.75%` for pools 3/4/5/7 and `3.33%` for fresh keys. Supplying the true recurring-transform slot to the per-record encoder gave `57.08 / 50.69 / 33.61 / 22.92%`, differences of only `+1.81 / +4.44 / +0.69 / -0.83` points. Hidden-slot mixture identification is therefore not the main limitation in this range.

In a separate shuffled-non-anchor control, each 10-record set retained one target-identity record and received nine records from other identities while preserving record count and position-wise marginals. Pools 3/4 and fresh keys all produced exactly `3.33%` top-1 for every seed with AUROC `0.499/0.503/0.500`. Thus the recurring-pool gain requires multiple same-identity records and is not a set-size or global transform-frequency artefact. The negative pool-3 change from its `18.19%` one-record baseline reflects dilution of the sole informative record under mean pooling.

### 5.7 Same-image and correlated-key controls

Repeating the exact same normalized ArcFace embedding under ten distinct fresh, split-disjoint keys gave `3.33%` top-1 for all three seeds and AUROC `0.4997`, matching the different-image fresh-key baseline. The fresh-key null is therefore not an artefact of within-person session or image variation.

For a controlled correlation test, each BioHash projection shared an exact prefix of system-wide projection columns and used orthonormal private columns for the remainder. A coarse `0/25/50/75/100%` sweep gave 10-record top-1 `3.33/9.44/46.39/61.11/71.67%`. Because the 25% result was unstable, an independently preregistered fine sweep on a new partition tested `0/12.5/18.75/25/31.25/37.5/43.75/50%` and gave `3.33/3.75/6.94/7.64/14.17/35.83/49.31/42.64%`. All three seeds were strongly above chance from 37.5% onward; lower transition points were seed-sensitive. This supports correlation-dependent leakage but neither a sharp universal threshold nor strict empirical monotonicity.

## 6. Corrected Follow-up and Diagnostics

### Pilot extension, reported separately

After user-reported approval, paper-specified IoM-GRP (300 groups, q=16, one-hot input) and PolyProtect (window 5, overlap 2, raw 170-dimensional output) were implemented. The pre-run commit `d5f4e89` freezes the [pilot configuration](../configs/attacks/scheme_extension_pilot.yaml). Sixteen MOBIO/FEI cells produced 48 single/mean/DeepSets runs in 277.89 seconds on CPU. One seed, a 120-epoch cap and endpoints 1/10 distinguish these engineering diagnostics from the earlier studies; they are not a controlled scheme ranking.

At pool 4, paired mean-pool ten-minus-one gains are 37.92 and 33.75 percentage points for IoM-GRP on MOBIO/FEI, and 30.00 and 58.13 for PolyProtect. All four identity-bootstrap 95% intervals exclude zero, conditional on one seed and partition without multiplicity adjustment. Full values, negative gains and pool-8 outcomes remain in the [pilot report](../experiments/scheme_extension_pilot/README.md).

Fresh-key sensitivity does not establish equivalence: no endpoint's 90% interval lies strictly within +/-1 point of chance, and only one of 12 meets the illustrative +/-2-point band. These margins are not prospectively approved scientific bounds. Native fresh-key PolyProtect protected-gallery top-1 is 12.73%/13.73% on MOBIO/FEI, above 3.33%/2.50% chance; AUROC is 0.4971/0.5237. This separate matching task and probe definition must not be conflated with learned unprotected-gallery linkage. The follow-up below supplies null calibration without establishing a causal mechanism or a general privacy claim.

### Multi-seed and identity-partition follow-up

A separately hash-frozen [bounded protocol](../docs/protocols/scheme_followup_2026-09-18.md) tested MOBIO/FEI, IoM-GRP/PolyProtect, two new identity assignments and three model seeds under matched 120-epoch caps. Fresh/shared/pool-4 conditions produced 24 cells and 216 single/mean/DeepSets endpoints. All eight primary pool-4 mean-pool ten-minus-one gains were positive: 25.83-40.83 percentage points for IoM-GRP and 21.25-29.31 for PolyProtect. Crossed model-seed/identity bootstrap 95% intervals excluded zero; one-sided identity sign-flip tests on seed-averaged gains yielded Holm p = 0.004 across the eight-hypothesis family. Full endpoints, seed SD and intervals are in the [follow-up report](../experiments/scheme_followup_2026-09-18/README.md). Identity assignments overlap, and training key/set seeds are fixed; these are sensitivity checks, not independent population replications.

Three fresh-key seeds per dataset/partition produced twelve native PolyProtect controls. Identity-balanced top-1 was 10.91-14.55% on MOBIO and 10.11-11.64% on FEI, with Holm p = 0.006 against identity-preserving gallery-label permutation nulls. Positive radial scales 0.5/2 left IoM-GRP unchanged but changed PolyProtect templates. This synthetic scale sensitivity is not natural norm leakage or an explanation of native linkage. Fresh learned endpoints remained chance-compatible; no equivalence conclusion follows.

SCface separately extends earlier BioHash coverage to a fourth dataset: 130 identities, 2,851 usable embeddings and 26 test identities. Pools 1/2/3 pass the all-seed interval rule; pool 4 does not. Its IoM-GRP/PolyProtect results remain one-seed pilots, not part of the new bounded follow-up. See [SCface results](../experiments/scface_multiexposure/README.md) and [pilots](../experiments/scface_scheme_extension_pilot/README.md).

### Raw inputs, implementation checks and failures

The [raw-norm audit](../experiments/norm_native_audit_2026-09-18/README.md) re-extracted all 4,177 inputs in 254.157 seconds. Re-normalization matches saved vectors within 2.98e-8 maximum absolute error. Separate scalar PolyProtect and matrix/SciPy cosine calculations agree on predictions in all 48 cells, with no gallery overlap, ties or order dependence. Formula/windows/padding/parameter ranges match the paper, but its stricter score-conditioned selection is not implemented. This is computational checking, not official-code equivalence or independent human validation.

Three-key-averaged native unit top-1 is 12.20-12.42% on MOBIO and 11.09-11.12% on FEI; raw top-1 is 16.46-16.66% and 15.58-16.01%. All 16 endpoints pass gallery-label null tests (Holm p = 0.0032). Identity-bootstrap intervals condition on these three fixed keys. Raw-unit gains survive paired Holm family 8 only on FEI (p = 0.0160/0.0168; MOBIO 0.1380/0.1032). Raw-shuffled differences span -0.61 to +0.61 points; all intervals include zero, adjusted p >= 0.7584. Fixed training-median radius performs similarly to raw. This demonstrates scale sensitivity, not identity-specific norm leakage or equivalence; shuffling also disrupts quality associations. No source-norm oracle test survives its family of four, and it is not a protected-template attack. IoM changes zero of 38,400 sampled unit/raw codes, consistent with known scale invariance.

Unit-input linear-only native top-1 is 10.70-12.53%, and median nonlinear residual is 0.072-0.085 of template norm. Low-degree terms may contribute to residual matching; this diagnostic does not prove a complete mechanism. Original PolyProtect already reports naive-parameter residual linkage. Its stricter-policy evaluation is not overturned.

All 48 one-to-ten contrasts now have crossed seed/identity intervals, seed ranges, leave-one-seed-out sensitivity and two-sided Holm correction. The post-hoc family retains eight pool-4 mean gains (p = 0.0192; minimum leave-one-seed-out gain 17.71 points). No pool-4 DeepSets gain survives (minimum p = 0.0576). Four shared-key PolyProtect DeepSets gains are significantly negative, -15.42 to -24.86 points (p = 0.0192). Optimization/aggregation explanations remain untested. Original one-sided primary results (family eight, p = 0.004) are unchanged. Pointwise bootstrap intervals are not simultaneous and need not agree with corrected tests.

### Interpretation of earlier studies

- Deployment implication: independently sampled hidden per-record transforms remove source information under the idealized assumptions. Public salts are not secret keys and are not covered by that claim. Recurring application-wide or device-wide transforms can support multi-record linkage even when their values are hidden.
- Boundary location is protocol- and partition-specific and must be reported as a range: partition 3 collapsed at $k = 5$ while partitions A and 2 held to $k = 7$; pool 6 vs 7 non-monotonicity within partition A (seed std 18 points) shows that single-seed points near the boundary are unreliable.
- Why the collapse: as $k$ grows, the number of training records per transform falls as $1080/k$ and fewer same-transform relations recur within a set. The paired key-slot control changes top-1 by at most 4.44 points, so explicit mixture labels do not remove the boundary; loss of repeated cross-record structure is the stronger explanation under this attacker.
- Correlated transforms weaken the fresh-key symmetry continuously. They create single-record leakage at high shared fractions and additional multiplicity amplification, connecting the theorem's independent-key endpoint to the recurring-pool endpoint.

## 7. Limitations

One encoder, four datasets and 25-40 gallery identities; only three model seeds, overlapping assignments and fixed training key/set seeds. SCface new-scheme results remain one-seed pilots. Training and targets share a hidden pool; unrelated-key transfer is untested. Implementations are paper-specified, not source-exact; benchmark source retrieval previously failed, and current availability is not asserted. The norm audit covers native matching, not retrained learned raw-input attacks. Stricter PolyProtect selection, other encoders, open-set galleries, approved equivalence margins, unavailable historical paired scores and independent human review remain open. Bootstrap intervals may under-cover; chance inclusion and nonsignificance do not prove privacy. This bounded revision does not complete every dataset, exposure and key seed.

## 8. Reproducibility

All configurations, preregistrations, compact summaries, and hashes are in the repository. Restricted MOBIO data, embeddings, keys, and full metrics remain local. Commands: `experiments/mobio_multiexposure/README.md`, `experiments/mobio_mechanism_controls/README.md`, and `experiments/mobio_correlation_controls/README.md`.

## 9. Result coverage

FEI and SCface extend historical BioHash coverage beyond MOBIO/LFW. The earlier table preserves 73 conditions from 12 studies; 72 pilot and 216 follow-up endpoints remain separate. The inventory retains 849 rows from 49 artifacts, including all previous 633. Its [coverage audit](../experiments/scheme_followup_2026-09-18/coverage_audit.csv) identifies legacy schemas and missing local SCface details. The 130 new audit rows are not trained endpoints and remain separate. The revised report distinguishes prior work, access assumptions, historical results, corrected tests, raw-norm controls and failures.
