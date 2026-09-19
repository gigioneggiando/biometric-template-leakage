# September report: detailed reading guide

Companion to the [19-page report](Sept_Dataset_Update.pdf), revised 19 September 2026. For the simpler explanation of every page, start with the [plain-language README](Sept_Dataset_Update_README.md). This guide retains detailed older numerical tables. A **template** is a list of numbers describing a face; protection changes that list using a secret key. **Top-1** means choosing the correct person on the first try. **Chance** means random guessing among the gallery's people. Percentage points measure a difference: 10% to 30% is a 20-point increase.

Latest scope: SCface now has a multi-seed extended study, and learned raw-input/stricter-selection studies are complete. Pages 17-19 explain these additions. Older references to no raw retraining or to pilot-only SCface apply only to those earlier studies. Three executed-source snapshots for the extended study remain unresolved locally; see the [provenance note](final_research_status.md#provenance-check).

The original page-by-page explanation is retained, with a new coverage diagram (page 15), independent-pool/baseline results (page 16), and revised prior-work/conclusions. Older results were not overwritten. Values below usually retain two decimal places; the PDF heatmap rounds to one. Small rounding differences are not different experiments.

## Reading numbers and uncertainty

- **Identity** means a person; **record** means a protected representation from a picture. Ten records are not ten people.
- **Gallery** is the list of candidate people. **Probe** is a query compared with that list. Learned probes can be sets of pictures; native probes are protected records. Their percentages therefore answer different questions.
- **Top-1 40%** means the correct person ranks first on 40% of evaluated queries under the stated averaging rule. It does not mean 40% of the original face was reconstructed.
- **Identity-balanced** means average each person's success rate first, then give every person equal weight. Probe-weighted accuracy instead weights people with more probes more heavily.
- **Chance** is $100/N$ percent for a uniform guess among $N$ gallery identities: MOBIO 3.333%, LFW 4%, FEI 2.5%, SCface 3.846%. Higher raw accuracy across different datasets is not automatically a better attack: gallery size, capture difficulty and protocol differ.
- **Gain in percentage points (pp)** is ten-record accuracy minus one-record accuracy. A rise from 5% to 35% is +30 pp, not +30% relative improvement.
- **95% bootstrap interval** describes uncertainty from the resampling procedure. It is not a range containing 95% of individual predictions, a guarantee for new datasets, or automatically a 95% probability that the true value lies inside this particular interval. Repeated sets reuse records, so identities, not individual correlated queries, are resampled together.
- **Crossed intervals** on page 6 resample model seeds and identities; page 16 additionally resamples pool draws. Pilot/native intervals do not include the same sources of uncertainty. Native three-key averages condition on that fixed ensemble.
- **Seed** is an integer selecting a reproducible random draw, not a performance score. Training seeds change initial training randomness; split seeds change person assignments; key seeds change transformations. These sources are not interchangeable.
- **p-value** measures extremeness under the specified null and test assumptions, not the probability that the paper is wrong or that a system is private. **Holm correction** adjusts a family of tests to control false rejection risk. We discuss a 0.05 decision threshold, not a universal scientific boundary.
- **Pointwise intervals and corrected p-values differ:** an ordinary 95% interval can exclude zero while a family-adjusted test is nonsignificant. Overlap of two separate intervals is not a paired-difference test either.
- **Nonsignificant** means insufficient evidence under this test, not equality. **Equivalence** would need a scientifically justified margin and appropriate analysis. Neither establishes security against all attackers.
- Axis ticks such as 0, 20, 40, 60 are scale labels, not additional experimental results. Lines connecting points do not supply measurements between those points.
- Footer values `4352eeb` and `15e4384` are Git commit identifiers; source hashes record the exact executed additions. `6/16` means page 6 of 16, not six successful tests.

## Page 1: What data did we test?

We use four face datasets with different challenges: sessions, everyday pictures, poses, and surveillance cameras. People used to teach the attacker are different from people used to test it. The newer careful training study contains 216 measured model results on MOBIO and FEI. That does not mean 216 different datasets or independent experiments.

| Dataset | People | Training / validation / testing people | Valid / selected pictures | Failed extractions | Chance |
|---|---:|---|---|---:|---:|
| MOBIO | 150 | 90 / 30 / 30 | 1,799 / 1,800 | 1 | 3.333% |
| LFW | 125 | 75 / 25 / 25 | 1,500 / 1,500 | 0 | 4.000% |
| FEI | 200 | 120 / 40 / 40 | 2,378 / 2,400 | 22 | 2.500% |
| SCface | 130 | 78 / 26 / 26 | 2,851 / 2,860 | 9 | 3.846% |

Training teaches the attacker; validation selects its checkpoint; testing measures it on unseen people. The same people can move between roles in different partition experiments, but the roles within a partition do not overlap.

SCface's **84.375% over 544 probes** is the unprotected mugshot-to-surveillance reference, equivalent to 459 correct probes. It is not a learned ten-record result and must not be used as that result's matched ceiling. Different probes, set averaging and training can give different rates. All 130 people remain eligible despite nine extraction failures.

**73 conditions / 12 studies** describes historical key-pool summary rows/source studies, not 73 independent populations. **24 pilot cells / 72 endpoints** means 3 datasets x 2 schemes x 4 key conditions, with 3 attacker/exposure endpoints each. **216 follow-up endpoints** means 2 datasets x 2 schemes x 2 identity partitions x 3 key conditions x 3 model seeds x 3 endpoints. The endpoints are one-record single MLP, ten-record mean MLP and ten-record DeepSets. The two uses of "24 cells" describe different designs.

The new **144 fits + 72 prediction-mean evaluations** are a separate pool study: 2 datasets x 2 schemes x 2 partitions x 3 pool draws = 24 cells. Each cell has 3 model seeds x 2 fitted models = 6 fits, plus 3 evaluations that reuse single-record checkpoints. Thus 216 evaluated endpoints does not mean 216 new trained models. See page 16.

## Page 2: The whole system

A face becomes a number list. A secret key changes that list. The attacker sees changed lists and tries to work out which gallery person they belong to. The diagram shows the route through the system; the attacker is not handed the secret keys.

Boxes **1-7** are pipeline steps, not measured results. **Five landmarks** align faces; **512-D** means ArcFace outputs 512 coordinates. The encoder is frozen: these experiments train the attacker, not ArcFace. Unit norm makes each original vector have length one.

| Protection label | Meaning of its numbers |
|---|---|
| BioHash, 128 bits | A record is 128 binary values. This is template length, not a claim of 128-bit cryptographic security. |
| MLP-Hash, 512 bits | A record is 512 binary values. It does not retain the original 512 real coordinates unchanged. |
| IoM-GRP, 300 codes, q=16 | Each of 300 groups stores the winning index among 16 projections. One-hot encoding uses 300 x 16 = 4,800 model-input entries. |
| PolyProtect, 170 reals, m=5, overlap=2 | Each output combines five source coordinates polynomially; neighboring windows share two, so the stride is three. The 512-coordinate vector requires 170 windows, with final zero padding. |

**Eight nested sets per identity** are repeated set constructions, not eight new independent people. Exposure count **n=1 or 10** is how many records each set contains; older experiments also used 2 and 5. **d -> 256 -> 512** describes layer widths: protected input, hidden features, recovered face-vector coordinates. **120 epochs** is the matched maximum number of training passes, with early stopping possible.

Fresh keys are unique by source record and disjoint across splits. Pool keys deliberately recur across training and testing people. Reusing a source record in another nested set also reuses its protected record; "fresh" does not mean drawing a new key every time that stored record is read.

Top-5 counts whether the correct identity appears among five candidates. AUROC summarizes genuine/impostor score separation (0.5 is the noninformative reference); EER is the point where false accept and false reject rates coincide; TAR at FAR measures true acceptance at a specified false-accept rate. They are listed as available metrics, not extra top-1 curves on this page.

## Page 3: How the attacker combines clues

We compare one protected record with ten records from the same person. One method averages the records before learning; DeepSets learns about each record before combining them. The training target comes from the exposed pictures, never the separate gallery picture.

**B x n x d** means batch size x records per set x protected-record width. B is not a dataset size; n is not pool size k. Mean or max pooling removes the n axis, giving B x d. The MLP maps d -> 256 -> 512 with a ReLU nonlinearity. DeepSets instead maps each record d -> 256 -> 256, averages those features, then decodes 256 -> 256 -> 512. Sharing the record encoder and averaging makes the output independent of record order.

The mask in `sum(m * phi(T)) / sum(m)` excludes padding records; every selected record is valid in these runs. Here m is a mask, not PolyProtect's window size on page 2. Output normalization gives a unit vector z.

The target u is the normalized average of the exposed **unprotected training** embeddings. Test-time source embeddings are not supplied to the attacker. The loss is $\operatorname{mean}(1-\cos(z,u)) + 0.1\operatorname{MSE}(z,u)$. The **0.1** weights coordinate error relative to directional error; it is not 10% attack success. Adam learning rate **0.001** controls update size; weight decay **0.0001** penalizes large weights. These are chosen training settings, not discovered privacy thresholds.

The gallery matrix G has **N x 512** entries, one unit reference per test person. Multiplying $zG^T$ gives a cosine score for each candidate; the largest score determines top-1. **3 seeds x 2 partitions** is sensitivity analysis, not six independent datasets. The gallery never supplies training targets.

## Page 4: What happens when keys are reused?

Imagine a system repeatedly choosing from a small box of secret keys. The attacker can learn patterns even without seeing the keys. The colored table shows older results: how much reuse matters changes across datasets. Grey means not tested; a failed statistical rule does not mean safe.

Left panel: one-record accuracy. Right panel: ten-record accuracy. Each row is a **source study**, not a different protection family. Columns **1-10** are the number k of transforms available to the entire recurring pool; **Fresh** is a separate unique-key construction, not k=11. Not every pool was tested in every study.

Each printed cell is absolute top-1 percent averaged over three model seeds. Color instead uses $(\text{top1}-\text{chance})/(1-\text{chance})$: 0 means chance, 1 means perfect, and a small negative value means below chance. The color bar is not a p-value or a fraction of leaked information. An asterisk marks a ten-record condition where **not all seed-level clustered intervals exclude chance**. It does not encode the entire historical rule (which additionally uses a fresh-baseline margin), and is not a modern Holm-adjusted test.

### Every heatmap value

Each entry below is **one-record / ten-record percent**; `NA` is an unavailable one-record endpoint. `*` has exactly the heatmap meaning above. Unlisted pools are grey/unavailable, not zero.

| Study row | Values by pool k |
|---|---|
| MOBIO / BioHash / session-aligned | 1: NA/66.39; 2: NA/61.11; 5: NA/47.64; 10: NA/33.89; Fresh: NA/2.92* |
| MOBIO / BioHash / random confirmation | 1: NA/77.50; 2: NA/69.44; 5: NA/46.94; 10: NA/5.56*; Fresh: NA/5.56* |
| MOBIO / BioHash / split B | 1: 75.97/81.67; 2: 35.00/73.89; 5: 4.31/51.11; 10: 4.31/5.56*; Fresh: 4.03/3.61* |
| MOBIO / BioHash / dense A | 3: 27.50/65.00; 4: 3.47/54.03; 6: 3.47/17.36*; 7: 4.17/34.44; 8: 4.03/10.42*; 9: 3.19/3.89*; Fresh: 3.19/5.56* |
| MOBIO / BioHash / dense 2 | 3: 22.36/48.61; 4: 7.64/48.61; 5: 6.39/40.28; 6: 6.39/36.39; 7: 5.00/30.42; 8: 3.19/14.17*; 9: 2.50/6.39*; Fresh: 2.36/1.53* |
| MOBIO / BioHash / dense 3 | 3: 5.83/56.39; 4: 5.42/51.94; 5: 4.86/8.06*; 6: 4.58/8.61*; 7: 5.69/8.89*; 8: 3.06/3.89*; 9: 4.72/6.67*; Fresh: 3.75/4.44* |
| MOBIO / Haar BioHash | 1: 75.00/74.58; 5: 3.47/48.06; Fresh: 3.06/2.64* |
| MOBIO / MLP-Hash / initial | 1: 52.08/71.39; 2: 33.61/68.89; 5: 4.44/22.92*; 10: 4.58/1.94*; Fresh: 2.92/3.06* |
| MOBIO / MLP-Hash / dense | 3: 3.06/54.31; 4: 4.58/37.78; Fresh: 3.06/3.47* |
| LFW / BioHash | 1: 70.67/73.17; 2: 37.33/63.17; 3: 23.83/62.50; 4: 16.83/42.50; 5: 11.50/41.00; 7: 11.67/32.00; 10: 4.33/25.33*; Fresh: 4.67/4.00* |
| FEI / BioHash | 1: 74.58/76.88; 2: 36.35/63.44; 3: 3.75/54.79; 4: 3.44/47.50; 5: 2.81/37.50; 7: 2.40/23.65; 10: 3.02/3.96*; Fresh: 2.29/1.77* |
| SCface / BioHash | 1: 40.71/81.57; 2: 22.44/61.06; 3: 5.29/33.17; 4: 4.01/20.51*; 5: 5.13/5.93*; 7: 4.17/1.92*; 10: 3.21/3.04*; Fresh: 4.33/3.85* |

Example: SCface pool 3 goes from **5.29% to 33.17%**, a **27.88 pp** descriptive increase, against 3.846% chance. It is not a 33.17 pp gain. Pool 4 reaches **20.51%** but still gets an asterisk because its uncertainty/seed behavior fails the all-seed rule. LFW pool 10 similarly reaches **25.33%** yet fails that rule. Failure is not proof that those settings contain no leakage.

The initial session-aligned study used capture-session structure for key assignment; later randomized studies remove that particular alignment. Dense A/2/3 are separate identity-partition studies. Haar is a projection-sampling correction, not a new dataset. Their different seeds and protocols must not be silently pooled or used as a matched causal comparison. [Source table](../experiments/cross_dataset_key_pool_summary.csv).

## Page 5: Are extra records really helping?

We deliberately change parts of the experiment. Replacing most records with other people's records removes the gain. Giving the attacker key-slot names adds little in these controls. These tests help narrow the explanation, but they do not prove every part of it.

**Panel (a):** x is pool size k; y is ten-record top-1 (%). Blue is DeepSets with slots hidden; orange/red gives the slot label, not the key value. Grey is a separate mean-pooling control keeping one target record and replacing nine with other people's records. These are not three identical models with only one switch changed.

| k | Hidden slots | Known slot labels | Known minus hidden, pp | Shuffled non-anchor |
|---:|---:|---:|---:|---:|
| 3 | 55.28 | 57.08 | +1.81 | 3.33 |
| 4 | 46.25 | 50.69 | +4.44 | 3.33 |
| 5 | 32.92 | 33.61 | +0.69 | Not tested |
| 7 | 23.75 | 22.92 | -0.83 | Not tested |

Differences use underlying unrounded values. No uncertainty bars appear here; these are descriptive three-seed means, not proof that every small difference is significant. The horizontal reference is 3.33% chance.

**Panel (b):** x is the percentage of 128 projection columns shared system-wide, not the percentage of shared identities. For example, 25% means 32 common columns. Remaining columns use the study's private construction. Solid circles show the coarse ten-record sweep; triangles show a fine sweep on another split; dotted circles show coarse one-record matching.

| Shared columns (%) | Coarse one-record (%) | Coarse ten-record (%) | Fine ten-record (%) |
|---:|---:|---:|---:|
| 0 | 3.33 | 3.33 | 3.33 |
| 12.50 | Not tested | Not tested | 3.75 |
| 18.75 | Not tested | Not tested | 6.94 |
| 25 | 3.33 | 9.44 | 7.64 |
| 31.25 | Not tested | Not tested | 14.17 |
| 37.50 | Not tested | Not tested | 35.83 |
| 43.75 | Not tested | Not tested | 49.31 |
| 50 | 39.17 | 46.39 | 42.64 |
| 75 | 50.83 | 61.11 | Not tested |
| 100 | 69.17 | 71.67 | Not tested |

At 50%, coarse and fine are different experiments, not conflicting measurements of one run. The decrease from 49.31% to 42.64% in the fine sweep rules out claiming an exactly monotone observed curve. These are artificial mechanism probes, not a standard deployed key-derivation scheme.

**Panel (c):** both bars are **3.33%** ten-record top-1. The first protects different pictures; the second protects the exact same source embedding ten times under distinct fresh keys. Thus within-person picture variation is not needed to obtain this tested near-chance behavior. Equal aggregate accuracy does not establish identical predictions or a privacy guarantee. Sources: [mechanism controls](../experiments/mobio_mechanism_controls/results_summary.csv), [correlation controls](../experiments/mobio_correlation_controls/results_summary.csv).

## Page 6: The main result repeated carefully

We repeat training with three random starts and two ways to divide people. In all eight planned pool-4 mean-pooling comparisons, ten records help more than one. Gains are about 21-41 percentage points and survive a correction for testing several questions. The partitions overlap, so they are not two completely independent groups of people.

Horizontal position is **gain**, not absolute accuracy. Zero means no improvement; positive means ten-record mean MLP beats the one-record MLP. Each line is a crossed seed/identity 95% interval. Blue is IoM; orange/red is PolyProtect. Split identifiers 91831 and 91843 select assignments, not counts of people.

| Dataset | Scheme | Split | Gain, pp | 95% interval, pp | Holm p |
|---|---|---:|---:|---|---:|
| FEI | IoM-GRP | 91831 | 28.23 | [20.31, 36.26] | 0.004 |
| FEI | IoM-GRP | 91843 | 25.83 | [18.75, 33.65] | 0.004 |
| FEI | PolyProtect | 91831 | 23.96 | [14.27, 33.44] | 0.004 |
| FEI | PolyProtect | 91843 | 21.35 | [10.21, 31.46] | 0.004 |
| MOBIO | IoM-GRP | 91831 | 37.36 | [26.67, 48.19] | 0.004 |
| MOBIO | IoM-GRP | 91843 | 40.83 | [31.39, 49.72] | 0.004 |
| MOBIO | PolyProtect | 91831 | 21.25 | [8.05, 33.34] | 0.004 |
| MOBIO | PolyProtect | 91843 | 29.31 | [8.61, 47.50] | 0.004 |

Example: **+37.36 pp** means about 37 more first-choice successes per 100 evaluated sets than the matched one-record rate, averaged over this experiment, not 37.36% total success. Its interval describes uncertainty in the gain.

The primary family has **8** hypotheses: 2 datasets x 2 schemes x 2 splits. Three model seeds are **601, 607, 613**. **1,999** sign-flip permutations give minimum plus-one Monte Carlo p **1/2,000 = 0.0005**; all eight hit that resolution, yielding Holm p **0.004**. Equal p-values do not mean equally sized or equally precisely estimated effects. Tests average model-seed gains before flipping identity-level differences and require null sign exchangeability. The **2,000** bootstrap draws independently resample seed and identity axes, so the interval and test do not have identical uncertainty interpretations. Training keys/sets are fixed, and only three model seeds are available. [Source](../experiments/scheme_followup_2026-09-18/seed_identity_contrasts.csv).

## Page 7: A different way to match records

Instead of teaching a model, we directly compare protected records with a protected gallery. Fresh-key PolyProtect still matches better than random guessing in these tests. Artificially shrinking or growing input lists changes PolyProtect but not IoM. This older artificial-size test alone cannot show that natural face-list sizes reveal identity.

**Left panel:** blue circles are MOBIO; green squares are FEI. A/B denote splits 91831/91843. Key-seed indices 1/2/3 denote 91873/91879/91883. Each plotted point is identity-balanced native top-1 with an identity-bootstrap 95% interval. Dashed horizontal lines are 3.333%/2.5% chance, not learned-attack baselines.

| Partition / key | MOBIO estimate [95% interval], % | FEI estimate [95% interval], % |
|---|---|---|
| A/1 | 14.55 [10.61, 18.79] | 11.20 [8.20, 14.43] |
| A/2 | 10.91 [8.18, 13.94] | 11.52 [9.27, 14.07] |
| A/3 | 11.82 [8.48, 15.15] | 10.64 [7.89, 13.34] |
| B/1 | 12.79 [8.48, 16.97] | 11.52 [8.32, 14.73] |
| B/2 | 12.18 [8.85, 15.52] | 10.11 [7.05, 13.86] |
| B/3 | 11.64 [8.48, 15.09] | 11.64 [8.25, 15.50] |

There are **12 tests = 2 datasets x 2 splits x 3 key seeds**. Gallery-label permutations break the true identity alignment while retaining correlated probes together. Each raw p reaches 0.0005; Holm family 12 gives **0.006**. This rejects that specific null, not every possible implementation artefact and not the stronger-policy security claim.

**Right panel:** x chooses artificial input scale 0.5 or 2. The y-axis is mean $\|T(sx)-T(x)\|_2/\|T(x)\|_2$, a relative change in the protected template, **not attack accuracy**. A value 1.2 means the difference vector has 1.2 times the original template's length; it does not mean 120% correct identification. Each point averages 32 held-out source records in a dataset/split.

| Dataset / split | PolyProtect at 0.5x | PolyProtect at 2x | IoM at either scale |
|---|---:|---:|---:|
| MOBIO A | 0.521550 | 1.212244 | 0 |
| MOBIO B | 0.509851 | 1.109855 | 0 |
| FEI A | 0.515097 | 1.157472 | 0 |
| FEI B | 0.523615 | 1.234870 | 0 |

Several zero-valued IoM points overlap visually. Its winning ranks do not change under positive rescaling; PolyProtect's different powers respond differently. This alone says nothing about whether natural norms are identity-discriminative. Sources: [native controls](../experiments/scheme_followup_2026-09-18/native_null_controls.csv), [radial controls](../experiments/scheme_followup_2026-09-18/norm_sensitivity.csv).

## Page 8: Earlier trial runs

These are smaller trial experiments, including SCface. They helped decide what to investigate next. All the plotted pilot endpoints use one random training start, so we keep them apart from the stronger three-start study instead of pretending they have equal reliability.

Six panels: top row IoM, bottom row PolyProtect; columns MOBIO, FEI, SCface. **N=30/40/26** is gallery size. The x positions **1, 4, 8** are recurring-pool sizes, not exposure counts. **Fresh** is plotted separately, not joined as k=11. Grey squares: one-record single MLP; blue circles: ten-record mean MLP; green triangles: ten-record DeepSets. Y is absolute top-1 percent. The dashed baseline is chance.

### Every pilot point and error bar

Entries are **estimate [lower95, upper95]**, all in percent. The bars resample identities, conditional on **one** model seed/partition, with a **120-epoch cap**. A 100 [100,100] bootstrap result only says every resampled observed identity succeeded for that endpoint; it does not imply certainty about all future identities.

| Dataset / scheme | Pool | One record | Ten, mean | Ten, DeepSets |
|---|---|---|---|---|
| MOBIO / IoM | 1 | 100.00 [100,100] | 100.00 [100,100] | 90.42 [78.74,100] |
| MOBIO / IoM | 4 | 52.50 [42.49,62.92] | 90.42 [80.82,97.92] | 80.42 [65.82,92.50] |
| MOBIO / IoM | 8 | 27.08 [17.49,37.50] | 57.08 [40.41,74.17] | 43.75 [26.67,62.08] |
| MOBIO / IoM | Fresh | 2.92 [0.42,5.83] | 6.67 [0,16.67] | 3.33 [0,10] |
| FEI / IoM | 1 | 99.69 [99.06,100] | 100.00 [100,100] | 95.00 [87.50,100] |
| FEI / IoM | 4 | 61.25 [52.19,70.31] | 95.00 [87.50,100] | 82.50 [71.56,92.81] |
| FEI / IoM | 8 | 29.06 [21.56,37.81] | 83.44 [71.88,94.38] | 58.75 [44.69,73.44] |
| FEI / IoM | Fresh | 1.88 [0,4.38] | 2.19 [0,6.56] | 2.50 [0,7.50] |
| SCface / IoM | 1 | 61.06 [50.00,71.63] | 90.38 [79.31,99.04] | 78.37 [63.94,91.35] |
| SCface / IoM | 4 | 28.37 [19.23,38.94] | 62.98 [46.15,80.29] | 51.44 [34.13,69.23] |
| SCface / IoM | 8 | 13.94 [7.21,21.17] | 34.13 [20.19,48.56] | 31.73 [17.79,47.12] |
| SCface / IoM | Fresh | 5.29 [0.48,13.46] | 3.85 [0,11.54] | 3.85 [0,11.54] |
| MOBIO / PolyProtect | 1 | 95.00 [90.00,98.75] | 88.75 [76.67,98.75] | 81.25 [67.07,93.35] |
| MOBIO / PolyProtect | 4 | 4.17 [0.42,9.17] | 34.17 [19.58,49.17] | 42.50 [25.00,58.75] |
| MOBIO / PolyProtect | 8 | 4.17 [0,10.00] | 5.83 [0,15.00] | 4.17 [0,11.67] |
| MOBIO / PolyProtect | Fresh | 3.75 [0.83,7.50] | 3.33 [0,10.00] | 3.33 [0,10.00] |
| FEI / PolyProtect | 1 | 96.56 [90.94,100] | 82.81 [70.31,92.81] | 84.06 [72.19,93.75] |
| FEI / PolyProtect | 4 | 3.12 [0,8.75] | 61.25 [47.49,75.00] | 62.19 [48.44,76.25] |
| FEI / PolyProtect | 8 | 4.38 [0.31,9.69] | 5.31 [0.31,12.81] | 3.75 [0,10.00] |
| FEI / PolyProtect | Fresh | 1.88 [0,5.62] | 2.19 [0,5.31] | 2.50 [0,7.50] |
| SCface / PolyProtect | 1 | 67.79 [54.33,78.86] | 82.21 [68.27,94.23] | 78.85 [64.42,91.83] |
| SCface / PolyProtect | 4 | 27.88 [20.18,36.54] | 69.71 [56.25,83.65] | 61.06 [44.23,76.92] |
| SCface / PolyProtect | 8 | 5.29 [0,12.02] | 9.62 [3.37,17.79] | 30.29 [18.74,44.71] |
| SCface / PolyProtect | Fresh | 3.85 [0,9.13] | 3.37 [0,8.65] | 4.33 [0,11.54] |

The heading's **72 endpoints** is these 24 rows x 3 methods. The separately quoted **12.73/13.73/10.66%** are native fresh PolyProtect diagnostics for MOBIO/FEI/SCface, not the green/blue learned Fresh points. They use a protected gallery and different probes. The later corrected follow-up does not include SCface, so its native pilot has not received the same follow-up null calibration. Sources: [MOBIO/FEI pilots](../experiments/scheme_extension_pilot/results_summary.csv), [SCface pilots](../experiments/scface_scheme_extension_pilot/results_summary.csv).

## Page 9: What is actually different from earlier research?

Other researchers already showed that several records can help, that learned attacks can extract identity, and that naive PolyProtect settings can retain links. Our contribution is the controlled question: **how does hidden key reuse change the benefit of combining different pictures of one person?** We are not claiming to have invented those earlier ideas or beaten their results in a fair head-to-head contest.

**1-10** in the prior PolyProtect study counts protected versions of the same original embedding under disclosed parameters for inversion. Ours uses different pictures and hidden parameters for learned linkage; these are differences in task, not proof that ours is harder in every respect. **2022** is the paper year. **v3** is FaceLinkGen's inspected version, not its accuracy or number of datasets. The DOI/arXiv numbers at the bottom are source identifiers.

"Multiplicity is not new" means the idea that several records can help is already known. "Identity distillation is not new" means teaching an attacker to imitate an identity encoder is already known. "IoM scale invariance is not new" means positive rescaling preserving ranks follows its established construction. Using known tools to establish a new empirical result is legitimate; claiming those tools as inventions would not be.

"No head-to-head win" means no superiority over external methods is established; the new local prediction-mean comparison also does not establish a win. "No exhaustive priority claim" means we have not proved nobody studied this combination. The complete author-thesis maximal-linkability chapter (section 5.4, printed 157-171) has now been compared: it already covers different keys, multiple templates and joint-score linkage. Its binary information metric is not gallery top-1; additive composition requires independence conditions. The publisher PDF was blocked, so final-journal version identity remains unverified. "No break of stricter PolyProtect policies" means our naive parameter selection does not test the stronger policy. [Full-text comparison](../docs/literature/closest_work_2026-09-18.md).

## Page 10: What must the attacker have?

It needs to know which records belong together, perhaps from an account label; paired training examples from the **same hidden key pool**; and a gallery containing the target. These are strong assumptions. A training system with unrelated keys does not qualify. We test small lists of 25-40 possible people, not finding anybody anywhere on the internet.

The attacker knows **these ten records belong to one account**, not necessarily **this account belongs to Alice**. The latter is what gallery linkage attempts to discover. Paired training could come from a legitimate query/enrollment interface or a provider observing consented inputs and protected outputs. But the outputs must reflect the same secret pool as targets; merely knowing the mathematical protection algorithm is insufficient to reproduce unknown recurring transforms.

**25-40 candidates** refers to the four gallery sizes, not hundreds of thousands of possible people. Guaranteed membership makes this closed-set identification. There is no tested "none of these people" decision. No claim about prevalence of such access in real products is established. Independent source-record keys can also prevent legitimate matching; a privacy-utility analysis is required before calling them a practical defense.

## Page 11: Did we check our measuring tools?

We calculate the protection formula another way and compare two ways of matching. Their predictions agree, with no reused gallery pictures, score ties or gallery-order problems in these checks. We also re-extract 4,177 raw face lists and verify they match the old lists after normalization. This checks computation; it is not an outside scientist's review or proof that every possible bug is absent.

**48 cells = 2 datasets x 2 splits x 4 input arms x 3 key seeds.** These are native implementation checks, not 48 new trained models. Zero float32 output difference means the separate scalar polynomial and production code returned the same stored numbers in these tested cells, not every imaginable input. The maximum cosine-score discrepancy **1.33e-15** is about 0.00000000000000133, consistent with very small floating-point differences; the winning identities still agree.

Zero gallery/probe overlap means no source record acts as both gallery and probe in that protocol. Zero reversed-gallery changes checks order dependence. Zero ties means no tested highest scores tied within the audit tolerance. Unique keys concern record assignments, not cryptographic certification of randomness. These checks do not audit all possible image-level duplicates, every preprocessing choice, or the entire original-author implementation.

**4,177 = 1,799 MOBIO + 2,378 FEI** raw re-extractions. Normalizing them reproduces saved vectors within **2.98e-8 = 0.0000000298** maximum coordinate error. This supports comparing the same underlying representations with and without normalization.

**38,400 IoM codes = 2 datasets x 2 splits x 32 sampled records x 300 groups.** Zero changed codes is a sampled natural-scale check, not 38,400 people or a full learned raw-input attack. These are computationally separate checks performed within this project, not independent human replication. [Audit details](../experiments/norm_native_audit_2026-09-18/README.md).

## Page 12: Does the natural size of a face list reveal identity?

The old lists were all resized to length one. We recover their genuine original sizes and compare four versions: unit length, original size, shuffled sizes, and one common size. Raw matching is about 16%, compared with about 11-12% for unit lists. But shuffled sizes work similarly, and only FEI's raw-versus-unit improvement survives correction. We found a scale effect, not proof that each person's natural size reveals who they are. We did not retrain learned attackers on raw inputs.

The two panels are MOBIO and FEI; blue circles are partition A, green squares are partition B. Y is native protected-gallery accuracy. Unit means vector length one; Raw means actual pre-normalization output; Shuffled keeps each direction but assigns norms from other records within its split; Fixed radius uses one common radius equal to the training median. Keys are matched across arms. Shuffling removes both identity and quality associations, so it is not a pure intervention on identity alone.

| Dataset / split | Unit [95% CI], % | Raw [95% CI], % | Shuffled [95% CI], % | Fixed [95% CI], % |
|---|---|---|---|---|
| MOBIO A | 12.42 [10.81,14.04] | 16.46 [13.74,19.49] | 17.07 [14.34,20.20] | 17.17 [14.44,20.30] |
| MOBIO B | 12.20 [10.00,14.38] | 16.66 [14.03,19.38] | 16.05 [13.74,18.47] | 16.45 [13.93,19.17] |
| FEI A | 11.12 [9.66,12.61] | 15.58 [13.67,17.67] | 15.49 [13.61,17.58] | 16.03 [13.99,18.22] |
| FEI B | 11.09 [9.18,13.20] | 16.01 [14.18,17.92] | 16.16 [14.27,18.14] | 16.23 [14.41,18.08] |

Every point averages three fixed key-seed confusion matrices. Error bars use **4,000 identity-bootstrap draws**, not new key draws. Dashed lines remain 3.333%/2.5%. **16 tests = 2 datasets x 2 splits x 4 arms**, against gallery-label permutation nulls. **4,999 permutations** give a raw floor **1/5,000 = 0.0002**; Holm family 16 gives **0.0032**. This tests above-null native matching, **not differences between arms**.

The paired arm differences form their own family of **8**, using two-sided sign-flips:

| Dataset / split | Raw minus unit, pp [95% CI] | Adjusted p | Raw minus shuffled, pp [95% CI] | Adjusted p |
|---|---|---:|---|---:|
| MOBIO A | +4.04 [1.01,7.37] | 0.1380 | -0.61 [-1.31,0.10] | 0.7584 |
| MOBIO B | +4.45 [1.32,7.70] | 0.1032 | +0.61 [-0.20,1.41] | 0.7584 |
| FEI A | +4.46 [1.95,7.04] | 0.0160 | +0.09 [-0.52,0.70] | 1.0000 |
| FEI B | +4.92 [2.11,7.68] | 0.0168 | -0.15 [-0.76,0.45] | 1.0000 |

MOBIO's pointwise raw-unit intervals exclude zero, yet its **corrected** tests do not pass 0.05. That is not a contradiction. None of the raw-shuffled tests passes; this does not prove exact equality. The source-norm-only diagnostic also fails its separate four-test correction, and assumes oracle access to raw norms, not extraction from protected data. Sources: [arm endpoints](../experiments/norm_native_audit_2026-09-18/native_norm_controls.csv), [paired tests](../experiments/norm_native_audit_2026-09-18/paired_norm_contrasts.csv).

## Page 13: When does the approach fail?

We report all 48 one-versus-ten comparisons, including bad outcomes. Eight pool-4 average-first gains remain convincing. The more complicated DeepSets method has less certain pool-4 gains, and it becomes about 15-25 points worse in four shared-key PolyProtect cases. More clues and a more complicated model do not automatically give a better answer. We have not yet isolated why those losses occur.

**48 contrasts = 2 datasets x 2 schemes x 2 splits x 3 key conditions x 2 ten-record models**, each compared with its matched single-record baseline and averaged over three training seeds. The graph displays 12 selected contrasts for interpretation; the table publishes all 48. Horizontal axis is gain in pp; zero is no change; left is worse. A/B retain their split meanings. Error bars are pointwise crossed seed/identity intervals from 4,000 draws.

| Left panel: pool-4 DeepSets | Gain, pp | 95% interval, pp | Family-48 Holm p |
|---|---:|---|---:|
| FEI / IoM A | +8.65 | [-3.65,19.17] | 0.8288 |
| FEI / IoM B | +3.54 | [-6.77,13.44] | 1.0000 |
| FEI / PolyProtect A | +14.69 | [0.52,27.09] | 0.2992 |
| FEI / PolyProtect B | +8.44 | [-6.77,24.38] | 1.0000 |
| MOBIO / IoM A | +12.92 | [-4.03,29.44] | 0.6000 |
| MOBIO / IoM B | +10.83 | [-3.75,24.17] | 0.8748 |
| MOBIO / PolyProtect A | +18.33 | [2.08,35.56] | 0.3036 |
| MOBIO / PolyProtect B | +28.47 | [12.22,44.17] | 0.0576 |

Even the last interval entirely above zero does not mean its family-adjusted p passes 0.05. The correct statement is "not significant in this corrected family," not "no effect exists" and not "mean pooling is statistically superior to DeepSets." That last claim would require a direct paired comparison between aggregators.

| Right panel: shared-key PolyProtect DeepSets | Gain, pp | 95% interval, pp | Family-48 Holm p |
|---|---:|---|---:|
| FEI A | -15.42 | [-25.00,-7.50] | 0.0192 |
| FEI B | -20.42 | [-34.17,-8.65] | 0.0192 |
| MOBIO A | -24.17 | [-39.31,-11.67] | 0.0192 |
| MOBIO B | -24.86 | [-41.94,-9.44] | 0.0192 |

For example, -24.86 pp means about 25 fewer correct first choices per 100 queries than the matched single-record baseline, not a negative accuracy. Training/optimization and aggregation explanations are hypotheses, not diagnosed causes.

All eight pool-4 mean gains also survive this larger family at **0.0192**, with all seed-level gains positive. The minimum mean gain after omitting any one seed is **17.71 pp**. This is a robustness summary, not a confidence bound. The repeated 0.0192 arises from the two-sided Monte Carlo floor **0.0004** and Holm family **48**; it is not interchangeable with page 6's one-sided, eight-test p **0.004**. The primary analysis stays unchanged; this wider analysis is explicitly post-hoc. [All contrasts](../experiments/norm_native_audit_2026-09-18/failure_analysis.csv).

## Page 14: What can we honestly conclude?

Hidden reuse can make several same-person records much more useful to an attacker in this setup. That benefit is not universal. Native matching and learned matching are different tests, and natural norm leakage was not demonstrated. Most importantly: **our attacker failing to do better than guessing does not prove nobody could succeed.** Wider tests, stronger parameter policies and independent human review remain unfinished.

This page contains no new experiment: **5.29 -> 33.17%** repeats historical SCface pool 3; **3.846%** is its 1/26 chance; **15.42-24.86 pp losses** summarizes page 13; **216 endpoints / 8 primary contrasts** summarizes page 6. "Four datasets" applies to historical BioHash coverage, not every scheme/control. The page intentionally does not turn chance-compatible results into a privacy guarantee or present all studies as equally replicated.

The revised page also summarizes page 16: IoM gains persist across tested new pools, PolyProtect is pool-sensitive, and all direct baseline intervals include zero. The earlier corrected result is not erased; its scope is clarified as conditional on its particular pool.

## Page 15: Which datasets support which claims?

Columns are MOBIO, LFW, FEI and SCface, not four equally complete experiment suites. Rows distinguish historical BioHash, MOBIO MLP-Hash, one-seed new-scheme pilots, the three-model-seed/two-partition follow-up, native/raw controls and the new three-pool study. Green/blue cells indicate completed coverage, not higher accuracy. Grey **Not run** means no experiment in that layer, not zero linkage or safety.

The numbers within cells describe replication: **3 model seeds** vary optimization; **2 splits** change identity roles but overlap; **3 pools** change transforms and slot assignments. Native controls' three keys are not three independently trained attackers. LFW contributes historical BioHash evidence in this matrix. SCface now also contributes the extended three-seed/two-split study, raw learned study and local stricter audit. It still lacks the independent-pool baseline experiment. Coverage is not uniform across all four datasets.

## Page 16: Do the results survive new pools and a simple baseline?

The left plot asks whether ten records beat one across independently seeded hidden pools. Each colored dot is a mean over **three model seeds** for one pool, not an individual person. Seeds **91901/91907/91909** select the three realizations. Black diamonds average pools and seeds; bars are **4,000-draw crossed pool/seed/identity 95% intervals**. A/B are split seeds **91831/91843**. All gains are percentage points, not relative percent changes.

| Dataset / scheme / split | Gain for pools 91901 / 91907 / 91909, pp | Mean [95% interval], pp |
|---|---|---|
| FEI / IoM A | 25.21 / 28.65 / 24.79 | 26.22 [19.96,32.50] |
| FEI / IoM B | 21.56 / 26.88 / 27.71 | 25.38 [18.54,32.95] |
| MOBIO / IoM A | 38.19 / 34.86 / 42.36 | 38.47 [29.58,47.96] |
| MOBIO / IoM B | 29.31 / 40.97 / 31.25 | 33.84 [23.75,43.75] |
| FEI / PolyProtect A | -0.31 / 18.96 / 72.40 | 30.35 [0.31,70.11] |
| FEI / PolyProtect B | -3.23 / 25.73 / 67.40 | 29.97 [-2.50,65.00] |
| MOBIO / PolyProtect A | -0.28 / 20.14 / 58.89 | 26.25 [0.46,56.94] |
| MOBIO / PolyProtect B | 0.83 / 23.19 / 47.78 | 23.94 [0.97,49.31] |

IoM is positive in **12/12** dataset/split/pool combinations, ranging **21.56-42.36 pp**. PolyProtect is positive in **9/12**, with three small reversals and range **-3.23 to +72.40 pp**. Its large mean gains hide very different outcomes between pools. These 12 cells per scheme are dependent, not a binomial sample of independent populations. Three pool draws are too few for universal robustness, even when a pointwise interval excludes zero. No new Holm-adjusted tests are claimed.

The right plot asks whether averaging protected inputs **before** the learned MLP beats averaging recovered embeddings **after** the single-record MLP. Prediction mean uses ten identical records and the same gallery, with no extra training. Each recovered embedding is normalized, the ten are averaged, and the average is normalized. It reuses the single-record checkpoint, so its training objective and effective record presentations differ from those of the set-trained model. Matched inference is not identical training.

| Dataset / scheme / split | Single 1 / input mean 10 / prediction mean 10, % | Input minus prediction mean [95% interval], pp |
|---|---|---|
| FEI / IoM A | 72.64 / 98.85 / 97.85 | 1.01 [-1.77,4.93] |
| FEI / IoM B | 66.81 / 92.19 / 92.29 | -0.10 [-6.11,7.08] |
| MOBIO / IoM A | 57.96 / 96.44 / 95.28 | 1.16 [-2.92,6.02] |
| MOBIO / IoM B | 57.82 / 91.67 / 92.73 | -1.06 [-8.06,6.62] |
| FEI / PolyProtect A | 27.22 / 57.57 / 36.04 | 21.53 [-10.21,70.94] |
| FEI / PolyProtect B | 24.90 / 54.86 / 32.15 | 22.71 [-5.00,66.46] |
| MOBIO / PolyProtect A | 21.81 / 48.06 / 32.78 | 15.28 [-14.17,55.42] |
| MOBIO / PolyProtect B | 22.45 / 46.39 / 34.17 | 12.22 [-11.11,44.86] |

Every direct-baseline interval includes zero. This is **not evidence of superiority and not proof of equality**. Prediction mean is competitive on IoM; PolyProtect's positive average differences have very large pool uncertainty. The study completed in **254.188 seconds**: **24 cells, 144 fits and 72 reused-checkpoint evaluations**. Pool seeds change both transforms and sample-to-slot assignments; exposure sets stay fixed. [Full design, source freeze and tables](../experiments/pool_replication_2026-09-19/README.md).

## Page 17: Expanded exposures and SCface replication

The eight panels show dataset x scheme x partition. X is record count 1/2/5/10; y is top-1 percentage. Colors are fresh/pool-1/pool-4/pool-8. The graph shows single MLP at 1 and mean MLP thereafter; DeepSets remains in the exported tables. Bars are crossed seed/identity 95% intervals, not across-pool intervals. A/B assignments overlap. The primary comparison is ten-record mean minus one-record single at pool 4, not every difference between curves.

| Dataset / scheme / split | Gain, pp | 95% interval, pp | Holm p |
|---|---:|---|---:|
| MOBIO / IoM A | 32.50 | [25.00,39.72] | 0.004 |
| MOBIO / IoM B | 27.22 | [17.08,36.81] | 0.004 |
| MOBIO / PolyProtect A | 58.19 | [44.17,71.25] | 0.004 |
| MOBIO / PolyProtect B | 53.47 | [38.33,67.22] | 0.004 |
| SCface / IoM A | 16.19 | [5.29,26.77] | 0.006 |
| SCface / IoM B | 34.29 | [21.47,47.12] | 0.004 |
| SCface / PolyProtect A | 5.93 | [0.48,14.11] | 0.034 |
| SCface / PolyProtect B | 5.77 | [1.28,12.02] | 0.011 |

32 cells x 7 model/exposure combinations x 3 seeds = **672 trained endpoints**, or 224 seed-aggregated summaries. Of these, **56** are fresh-key summaries and all include chance; the single/mean-only fresh subset has 32. This does not test unobserved counts 3/4/6/7/8/9. Pool-8 PolyProtect exceeds pool-4 in each of four cells, but pools differ, so a causal pool-size effect is not isolated. Native SCface controls also now have three key draws per partition and corrected null tests. [All plotted values and intervals](../experiments/scheme_followup_2026-09-19_full/seed_identity_endpoints.csv), [primary tests](../experiments/scheme_followup_2026-09-19_full/seed_identity_contrasts.csv).

## Page 18: Separate raw learned study

Y is learned top-1 (%); x separates scheme and fresh/pool-4 condition. Grey/blue/green are single-1/mean-10/DeepSets-10. Bars are **model-seed SD**, not confidence intervals. There is no matched unit arm, corrected null family, or equivalence test. Twenty-four summaries represent 72 fits at one saved partition per dataset.

| Dataset / scheme / condition | Single 1, % | Mean 10, % | DeepSets 10, % |
|---|---:|---:|---:|
| MOBIO / IoM / Fresh | 3.75 | 3.33 | 4.17 |
| MOBIO / IoM / Pool 4 | 55.00 | 91.11 | 63.33 |
| MOBIO / PolyProtect / Fresh | 2.64 | 3.61 | 4.58 |
| MOBIO / PolyProtect / Pool 4 | 4.72 | 3.61 | 4.58 |
| SCface / IoM / Fresh | 3.69 | 3.85 | 3.85 |
| SCface / IoM / Pool 4 | 26.44 | 67.63 | 43.59 |
| SCface / PolyProtect / Fresh | 3.53 | 3.69 | 3.85 |
| SCface / PolyProtect / Pool 4 | 5.77 | 3.85 | 3.69 |

Key/set seeds and assignments differ from page 17. Targets are normalized means of raw vectors, so norms also affect target weighting. The result is a tested PolyProtect failure setting, not a demonstration that normalization alone causes the cross-study difference or that raw input is safer. [All means and plotted SDs](../experiments/raw_input_attacker_2026-09-19/raw_input_results.csv).

## Page 19: Local stricter parameter selection

X is stricter-minus-naive native accuracy in percentage points. Left of zero would favor less linkage; right means more linkage. MOBIO is **+3.13 [0.10,6.16], p=0.1344**; SCface is **-0.32 [-2.19,1.47], p=0.7556**. Intervals condition on three fixed key seeds; p-values adjust the two paired tests. Neither shows a corrected change. The separate four-arm above-null family has p=0.0008; that is a different question.

The rule tries 20 candidates against 200 training-only development pairs and band [-0.5,0.5]. It is a local operationalization, not source-exact replication, a broad hyperparameter sweep or a refutation of every stricter policy. [Paired numbers](../experiments/polyprotect_stricter_audit_2026-09-19/paired_contrasts.csv).

## Why SCface appears only sometimes

| Evidence layer | MOBIO | LFW | FEI | SCface |
|---|---|---|---|---|
| Historical BioHash pool comparison, page 4 | Yes, multiple studies/partitions | Yes | Yes | Yes |
| MLP-Hash pool comparison | Yes | Not in this package | Not in this package | Not in this package |
| New-scheme one-seed pilots, page 8 | Yes | No | Yes | Yes |
| Matched three-seed/two-partition IoM/PolyProtect follow-up, page 6 | Yes | No | Yes | No |
| Corrected native/radial follow-up, page 7 | Yes | No | Yes | No |
| Genuine raw-norm/native audit, pages 11-12 | Yes | No | Yes | No |
| All 48 paired follow-up contrasts, page 13 | Yes | No | Yes | No |
| Three-pool replication and prediction baseline, page 16 | Yes | No | Yes | No |
| Extended exposures and pool-8, page 17 | Yes | No | No | Yes |
| Raw learned retraining, page 18 | Yes | No | No | Yes |
| Local stricter native selection, page 19 | Yes | No | No | Yes |

The original bounded run and three-pool study used MOBIO/FEI. The finalized extension instead used MOBIO/SCface. Private inputs are not all available on the current report-building host; tracked compact results support the updated plots. LFW remains outside those new studies. Missing coverage is not zero linkage or a privacy result.

Cross-dataset figures include page 4's heatmap, page 8's scheme panels, page 15's new coverage diagram, and [BioHash pool curves](figures/fig_pool_curves.pdf) in the [19-figure appendix](slides/figure_appendix.pdf). Missing cells cannot be filled from another scheme, seed budget or different task. Raw percentages and chance-normalized ratios do not remove capture/domain differences.

Page 6 is preserved as the original MOBIO/FEI study; page 17 contains the new MOBIO/SCface study with different key/set seeds. SCface preparation gives mugshots index 0, and split reassignment preserves that ordering. Private metadata was not independently re-audited here. Copying pilot points into the corrected study remains inappropriate.

## Can this become a paper now?

**Recommendation: develop and obtain coauthor review of a narrowly scoped empirical paper now; do not call the current package a finished, validated submission.** There is a coherent result and enough evidence to write it. Acceptance or suitability for a specific venue cannot be inferred from result counts or p-values. A preprint is a way to share a reviewed manuscript, not certification by peer review.

The central claim can be: **Under explicit paired same-pool access, reuse of hidden transformations enables substantial one-to-ten-record linkage gains in the tested settings, with scheme/partition-dependent failures.** The matched MOBIO/FEI results support this claim; broader historical evidence motivates it. We are not proposing a new protection algorithm, a universally best attacker, or an internet-scale deanonymization result.

### Status of the requested strengthening

1. **Full-text comparison completed using the author thesis.** Section 5.4, equations, scenarios and numerical tables are explicitly compared. The blocked publisher PDF's exact version and independent human review remain unverified.
2. **Independent recurring pools completed.** Three new realizations expose persistent IoM gains but substantial PolyProtect sensitivity. This is useful negative evidence, not a universal robustness certificate.
3. **SCface extended study complete.** It now contributes corrected three-seed/two-partition evidence. It still lacks independent-pool replication; no four-dataset cross-scheme matrix is claimed.
4. **Simple baseline and access justification completed.** Prediction averaging is tested on identical ten-record sets/galleries. Training differences, same-pool paired supervision, output-visible queries and closed-set assumptions are explicit. Superiority is not supported.
5. **Reproduction package updated.** Frozen sources, aggregate tables, tests, missing coverage and failure cases are retained. Authorized private inputs remain necessary; coauthor signoff and independent review are not replaced by computational checks.

### Scope that need not expand automatically

- **Stricter PolyProtect policy:** necessary to support a claim that recommended PolyProtect settings are broken; optional if results are explicitly about the tested naive policy and secondary to the reuse study. Alternatively move this diagnostic to an appendix.
- **Large/open-set galleries:** necessary for strong operational or internet-scale linkage claims; an important extension, but not automatically necessary for a clearly limited closed-set study.
- **Learned raw-input retraining:** now complete descriptively. A matched unit/raw comparison is still required for a causal normalization claim.
- **Another encoder:** would strengthen generalization beyond this ArcFace checkpoint. Without it, limit claims to this encoder rather than treating all face embeddings as established coverage.
- **Head-to-head wins:** needed for superiority claims, not for every empirical measurement paper. Literature comparison is still essential, and a fair baseline comparison may be requested by reviewers.
- **Every dataset in every plot:** not a scientific requirement. A clear coverage matrix and honest separation of study scopes are required for readers to understand what the plots support.

The "NOT CLAIMED" box should remain substantively true. A more positive presentation would lead with "Contribution: controlled reuse-conditioned set linkage" and then state these boundaries briefly. Removing the boundaries would not make the evidence stronger.

## Where the numbers live

[Trained follow-up](../experiments/scheme_followup_2026-09-18/README.md), [raw audit and complete failures](../experiments/norm_native_audit_2026-09-18/README.md), [closest research and assumptions](../docs/literature/closest_work_2026-09-18.md), [manuscript](paper_draft.md). No raw faces, embeddings or secret keys are included in the report.