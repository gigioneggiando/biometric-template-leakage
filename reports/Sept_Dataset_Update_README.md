# The September PDF, explained simply

Read this beside the [19-page PDF](Sept_Dataset_Update.pdf). Updated 19 September 2026, using results available through commit `4831d99`. The [detailed guide](Sept_Dataset_Update_guide.md) keeps the older exact numerical tables. This README explains every current page without requiring machine-learning knowledge.

## The whole idea

Imagine a face is turned into a list of 512 numbers. A secret recipe changes that list before it is stored. We ask: if someone gets several changed lists belonging to the same person, can a trained computer match that person to a small list of candidate people?

The computer is not given the secret recipe. But it gets powerful help: training examples made with the same pool of secret recipes, and information about which records belong together. This is an experiment under those assumptions, not a claim that every real system is vulnerable.

## Words used in the pictures

- **Template:** the changed list of numbers. It is not a face photograph.
- **Record/exposure:** one protected list from one picture. Ten records are ten clues about one person, not ten different people.
- **Gallery:** candidate people the computer chooses between. The gallery picture is kept out of the clues.
- **Top-1:** how often the computer's first choice is the right person. 40% means about 40 correct choices out of 100 queries, not 40% of a face recovered.
- **Chance:** blind guessing. There are 30 MOBIO candidates, 25 LFW, 40 FEI and 26 SCface, so chance is 3.33%, 4%, 2.50% and 3.85% respectively.
- **Fresh:** a different secret recipe for each source record. **Pool 4:** four recipes are reused across records and people. **Pool 1:** one hidden recipe reused everywhere, not a disclosed key.
- **Model seed:** a different random training start. **Split:** a different assignment of people to training and testing. **Pool seed:** different secret recipes and assignments. These are different kinds of repetition.
- **Percentage points:** 10% to 30% is a gain of 20 points. It is not a final accuracy of 20%.
- **Error bar:** uncertainty or variation, depending on the caption. Most show a 95% confidence interval. Page 18 instead shows variation across three training starts. They are not the same thing.
- **p-value:** a check against a particular no-effect explanation. A small value is evidence against that explanation, not proof of a big effect. **Holm** adjusts for checking several questions together.

A result near chance does not prove that nobody could attack the system. A missing experiment is not a zero score. And a higher score on one dataset does not mean it is an easier or better system: candidate counts and pictures differ.

## Page 1: The four collections of pictures

MOBIO has **150 people**, LFW **125**, FEI **200**, and SCface **130**. The three split numbers tell us how many people teach the attacker, help choose the trained model, and finally test it. Those groups do not overlap within an experiment.

The valid-picture counts are **1,799/1,800**, **1,500/1,500**, **2,378/2,400**, and **2,851/2,860**. The missing pictures failed extraction; these fractions are not attack accuracy.

SCface tests mugshot references against surveillance pictures. Its old unprotected reference gets **84.375%**, or **459 of 544 probes**, right. That is a separate task from combining ten protected records.

**73 conditions**, **72 pilots**, **216 original endpoints**, **144 pool-study fits**, **72 baseline evaluations**, and **672 extended endpoints** count different experiment packages. They are not independent people and must not be added up as a sample size.

## Page 2: How the experiment works

Follow the arrows: pictures -> face-number lists -> protection -> sets of records -> trained attacker -> predicted face-number list -> gallery choice.

**512-D** means 512 coordinates. **128 bits**, **512 bits**, **300 codes**, **4,800 entries**, and **170 real numbers** describe different protected formats, not security guarantees. IoM has 300 choices among 16 options, expanded to 300 x 16 = 4,800 entries for training.

Most studies shrink each face list to length one before protection. The new raw study skips that step. **1/2/5/10** is the number of clues. **Eight sets per person** are repeated selections that can reuse pictures, not eight independent people.

## Page 3: Two ways to combine clues

The top route averages the protected lists, then tries to reconstruct an identity vector. DeepSets, the lower route, first learns features from each list and then averages those features. The one-record model is the baseline.

**B x n x d** means number of sets in a batch x records in each set x numbers in each record. **256** is a hidden layer's width; **512** is the reconstructed vector's width. These are model sizes.

The target comes from the exposed training pictures, not the secret test person's gallery image. **0.001**, **0.0001**, and **0.1** are training settings, not success rates. **120 epochs** is a training limit, not necessarily the number used before early stopping.

Page 16 adds a third comparison: reconstruct each record using the one-record model, then average those predictions.

## Page 4: The older big table of results

The left half uses one clue; the right half uses ten. Read across a row to change the number of reused recipes. A cell such as **33.2** means about 33.2% correct first choices, averaged across three training starts.

For SCface pool 3, the computer goes from **5.29% to 33.17%**: a **27.88-point** increase. Fresh keys give about **3.85%**, near blind guessing among 26 people.

Grey means no available measurement. A star means not every training start's interval passed the old above-chance rule; it does not mean secure. Colors account for different chance rates, but the printed numbers are ordinary percentages. Each row is a study, so several MOBIO rows are not several new datasets.

## Page 5: Checking why the clues help

Left: telling the model which recipe slot was used changes scores by **-0.83 to +4.44 points**, not by a huge amount. Replacing nine clues with other people's records gives **3.33%**, suggesting that same-person clues matter. The shuffled control uses a different attacker, so it is not a perfectly isolated model comparison.

Middle: the horizontal axis is the fraction of 128 projection columns shared by the construction. **25% means 32 shared columns**, not 25% of secret keys revealed. More sharing often gives higher scores, but the two sweeps use different partitions and are not perfectly smooth.

Right: using ten copies of one image with different fresh keys and using ten different images both give **3.33%**. That result does not prove all fresh-key systems are safe.

## Page 6: The original carefully repeated gain

Each dot shows ten-record mean-pooling accuracy minus one-record accuracy, using pool 4. Dots to the right of zero mean extra clues helped. The bar is a 95% interval resampling training starts and people.

FEI IoM gains are **28.23/25.83 points**; FEI PolyProtect **23.96/21.35**. MOBIO IoM gains are **37.36/40.83**; MOBIO PolyProtect **21.25/29.31**. The two values are different identity assignments, not two entirely independent populations.

All eight corrected p-values are **0.004**. They repeat partly because the permutation test has limited numerical resolution, not because all effects are identical. This study fixed the hidden pool; page 16 tests new pools.

## Page 7: A different attack and a size check

Left: no learned reconstruction is used. The computer directly compares protected probes with a protected gallery. PolyProtect scores **10.91-14.55% on MOBIO** and **10.11-11.64% on FEI**, above their chance levels. A/B are splits; 1/2/3 are three key draws. All 12 corrected tests have **p=0.006**.

Right: inputs are made half as large or twice as large. IoM outputs change by **zero**; PolyProtect changes by roughly **0.51-0.52** or **1.11-1.23** in relative vector distance. These are changes in numbers, not identification percentages. This artificial test alone cannot show that natural vector lengths reveal identity.

## Page 8: Earlier trial runs

The columns are MOBIO, FEI and SCface; the rows are IoM and PolyProtect. Grey squares use one record, blue circles use ten with mean pooling, and green triangles use ten with DeepSets.

The horizontal labels **1/4/8** count recipes in the pool, not records. Fresh is a different condition. Taller points mean more successful identification. The bars describe uncertainty across people for just **one training start**.

For example, SCface IoM pool 4 goes from **28.37%** with one record to **62.98%** with ten-record mean pooling. That is a pilot finding; the new, more repeated SCface study is on page 17. The separate **12.73/13.73/10.66%** caption values are native matching, not those learned curves.

## Page 9: What is new, and what is not

Researchers already knew that multiple records can help, learned models can extract identity, and naive PolyProtect settings can retain links. We must not claim to invent those ideas.

Our useful question is narrower: **when hidden recipes are reused, how much does combining different pictures help, and when does it fail?** The new independent pools and simple baseline make that question more credible.

The literature comparison used the author's full thesis chapter for the maximal-linkability work. The publisher version was blocked, so its exact identity remains unverified. The local stricter-policy test on page 19 is not proof that every recommended PolyProtect policy is broken.

## Page 10: What help does the attacker need?

It must know which records belong together, have training examples from the **same hidden pool**, and have a gallery that contains the target. It does not receive the key values.

We tested **25-40 possible people**, not searching everyone on the internet. We did not test unknown grouping, open-set rejection, or training with an unrelated provider's keys. These strong assumptions belong in the paper.

## Page 11: Checking the measuring tools

The protection formula was calculated separately and matching was checked another way. **48 cells** means combinations of datasets, splits, input versions and key seeds, not 48 people.

**1.33e-15** is a tiny score difference near floating-point precision, and predictions agreed. **4,177** raw embeddings were re-extracted in the older MOBIO/FEI audit. Normalized coordinates differed by at most **2.98e-8**, another tiny number.

None of **38,400 sampled IoM codes** changed under raw/unit scaling. These are code entries, not people. This is computational checking, not an independent scientist's review or proof that every bug is impossible.

## Page 12: Does a vector's natural length explain matching?

Four versions are compared: length one, original raw length, lengths shuffled among records, and one common length. Blue circles and green squares are two identity assignments.

Unit-input native matching is around **11-12%**; raw is **15.58-16.66%**. But shuffled lengths do about as well. Only FEI's raw-versus-unit paired gain survives correction. We therefore do **not** establish that each person's natural length reveals their identity.

The **0.0032** p-value tests matching against a label-shuffling null, not whether raw beats shuffled. Those are separate tests. Page 18 is a different experiment: it trains an attacker on raw-input protected records.

## Page 13: Results that did not improve

Left: pool-4 DeepSets gains are uncertain after correcting all 48 comparisons; none passes that larger family. A bar can sit above zero while its multiple-test-adjusted p-value does not pass 0.05.

Right: with one shared PolyProtect key, DeepSets loses **15.42, 20.42, 24.17 and 24.86 points** against the one-record model. All four losses pass the corrected test at **0.0192**.

These are decreases, not negative accuracies. They show why the paper cannot say that more clues or a fancier model always helps. The cause of the losses has not been isolated.

## Page 14: The message so far

Hidden reuse can make multiple records useful to the tested attacker, but the effect depends on the scheme, data and actual pool. Fresh-key failures do not prove privacy. Native and learned matching answer different questions.

The earlier **216 endpoints**, **eight primary gains**, and **15-25-point losses** are summaries of earlier pages, not new experiments. SCface now also has the expanded study on page 17. Pages 18-19 add negative results, not universal defenses or universal scheme breaks.

## Page 15: Why some datasets appear in some graphs

This is a coverage map, not a scoreboard. Columns are the four datasets; rows are different study types. Colored cells mean completed work. Grey means not run in that particular study.

All four have historical BioHash results. MOBIO/FEI have the three-pool baseline study. MOBIO/SCface have the new 1/2/5/10-record study, raw learned study and stricter-selection audit. LFW and FEI were not silently added to those new experiments.

Numbers inside cells tell you how many seeds, splits or pools were used. They do not tell you accuracy. We should not fill a missing cell with a result from another protocol.

## Page 16: New secret pools and a simple alternative

Left: colored dots are three new pools. Black diamonds average them; bars include uncertainty across pools, training starts and people. IoM gains stay positive in all **12 dataset/split/pool combinations**, from **21.56 to 42.36 points**. PolyProtect ranges from **-3.23 to +72.40**, so its average hides large pool dependence.

Right: compare averaging protected inputs with averaging predictions from the one-record model. Every direct comparison interval includes zero. We cannot claim input averaging is better, or that both methods are exactly equal.

The baseline sees the same test records and gallery, but uses one-record training rather than set training. **Three pools** are useful evidence, not enough to claim universal robustness.

## Page 17: More clues and a stronger SCface study

Eight panels separate MOBIO/SCface, IoM/PolyProtect and identity split A/B. Along the bottom, **1, 2, 5, 10** is the number of records. The height is identification accuracy. Four colors mean fresh keys or pools of 1, 4, 8 recipes. Bars are crossed seed/person 95% intervals.

This study has **32 cells x 7 model/exposure combinations x 3 training starts = 672 endpoints**. The graph shows the single-record baseline and mean pooling; DeepSets is also in the tables. All **56 fresh summaries**, including both aggregators, have intervals containing chance. That is not proof of equality to chance.

The planned pool-4 gains are:

| Dataset / scheme | Split A gain | Split B gain | Corrected p, A / B |
|---|---:|---:|---|
| MOBIO / IoM | +32.50 points | +27.22 points | 0.004 / 0.004 |
| MOBIO / PolyProtect | +58.19 points | +53.47 points | 0.004 / 0.004 |
| SCface / IoM | +16.19 points | +34.29 points | 0.006 / 0.004 |
| SCface / PolyProtect | +5.93 points | +5.77 points | 0.034 / 0.011 |

All eight pass their planned correction. SCface is therefore no longer only a pilot for these schemes. Its PolyProtect pool-4 gain is much smaller than MOBIO's.

Pool 8 is not automatically safer: SCface PolyProtect ten-record accuracy rises from **10.26/10.10%** at pool 4 to **49.36/57.21%** at pool 8. However, those are different pool realizations. We have not proved that increasing pool size itself causes the increase.

## Page 18: Training with original-length face vectors

These plots show **raw-input results only**. Grey is one record; blue is ten-record mean pooling; green is ten-record DeepSets. Each bar is the standard deviation across three training starts, **not a confidence interval**. The dotted/dashed chance line is the guessing reference.

Pool-4 ten-record mean accuracy is **91.11% MOBIO / 67.63% SCface for IoM**, but only **3.61% / 3.85% for PolyProtect**. The tested raw PolyProtect attacker did not show a useful mean-pooling gain. This is an important boundary to report, not evidence to hide.

Do not subtract these scores from page 17 and call the difference a normalization effect. The studies use different key seeds, record selections and identity assignments. Raw vectors also change how training targets are averaged: long vectors get more weight. A matched unit/raw run would be needed to isolate those effects. This study is descriptive and does not prove raw input is safer.

## Page 19: Trying a stricter recipe-selection rule

This returns to direct protected-gallery matching. Our local rule tries **20 candidate parameter choices**, uses **200 development pairs**, and favors scores inside **[-0.5, 0.5]**. Development people are separate from test people. It is one local interpretation of the paper's rule, not an exact official-code reproduction.

The dot shows stricter accuracy minus naive accuracy. **Left of zero would mean less leakage.** MOBIO rises from **13.13% to 16.26%**, a **+3.13-point** change; SCface falls from **10.44% to 10.12%**, a **-0.32-point** change.

The intervals are **[0.10, 6.16]** and **[-2.19, 1.47] points**. The corrected paired p-values are **0.1344** and **0.7556**, so neither establishes a change at 0.05. Both versions still match above their label-shuffling null (**0.0008** after correction). That is not proof that every stricter policy fails.

## Is the paper stronger now?

**Yes, as a careful empirical paper.** It has more repeated SCface evidence, intermediate record counts, a larger-pool check, a simple baseline, and honest negative results. Better evidence does not mean every accuracy number gets larger.

The experimental core is now enough to finish a bounded manuscript and send it for coauthor review. It is not a guarantee of acceptance or a finished submission. **Update, 2026-09-20: the three source files flagged as unrecoverable from this checkout, Git history, or the earlier source archive have since been recovered directly from the experiment machine and independently re-verified against the manifest (33/33 files match); [the status report has the resolution](final_research_status.md#provenance-check).** Keep the claims conditional on same-pool training, this encoder, small galleries and tested policies. Finish the references, venue formatting, ethics/data-use statement and human scientific review. A causal raw-versus-unit explanation would need a matched new experiment; it is not required if we report this study descriptively.

No new training was run for this presentation update. Aggregate tables, completed manifests and source code were checked. Private SCface inputs are absent on this host, so their contents were not independently re-audited here. The preparation code assigns mugshots index 0 and the trainer keeps them as galleries; the frozen protocol records the intended camera split.

## Where to look next

- [Extended-study tables and protocol](../experiments/scheme_followup_2026-09-19_full/README.md)
- [Raw learned results](../experiments/raw_input_attacker_2026-09-19/README.md)
- [Stricter-selection results](../experiments/polyprotect_stricter_audit_2026-09-19/README.md)
- [Detailed page guide and older exact tables](Sept_Dataset_Update_guide.md)
- [All 22 figures](slides/figure_appendix.pdf) and [15-slide overview](slides/research_review.pdf)

Footer commit identifiers label versions of the work. They are not scores. No raw faces, private embeddings or secret keys are included in these documents.