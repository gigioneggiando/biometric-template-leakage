# The September PDF, explained simply

Read this beside the [19-page PDF](Sept_Dataset_Update.pdf). Guide updated **20 September 2026**; experiment results are available through commit `4831d99`. The [detailed guide](Sept_Dataset_Update_guide.md) keeps additional numerical tables. Start with the picture explanation on each page, then use its number key when something is unclear. You do not need to know machine learning.

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
- **Model:** the computer's trained guessing rule. **MLP** and **DeepSets** are two kinds of guessing machine. **Encoder:** the machine that first turns a face into a number list. **Embedding/vector:** that number list, not a recovered photograph.
- **Model seed:** a numbered starting shuffle for training. **Split/partition:** who goes into the learning, practice and final-test groups. **Pool seed:** a starting shuffle for the secret recipes and their assignments. Repeating one kind does not repeat all three.
- **Baseline:** a simple method used for comparison. **Native matching:** compare protected clues directly. **Learned matching:** train a machine to predict an unprotected face-number list, then compare it with the gallery. These are different tests.
- **Cell:** one experiment setting, like a row on a worksheet. **Fit:** one training run. **Endpoint:** one measured model result. **Summary:** several results combined. None of these words means a new person.
- **Percentage points:** 10% to 30% is a gain of 20 points. It is not a final accuracy of 20%.
- **Error bar:** the little whisker through a dot. Usually it shows uncertainty in an estimated result. Page 18 is different: its whiskers show how much three training runs varied.
- **95% confidence interval:** a range built by a method intended to cover the true quantity about 95 times out of 100 repeated studies, under its assumptions. It is not a promise about this one range, and does not mean 95% of people were identified.
- **Bootstrap:** make many pretend versions of the test by re-picking from the people already tested, allowing repeats. Re-pick a person's records together so ten clues are not counted as ten new people. A **crossed** bootstrap also re-picks training starts, and sometimes pools.
- **Null:** a particular "nothing useful is happening" explanation to test. Sometimes that means guessing at chance; sometimes it means two methods have no difference. Check which question the caption asks.
- **p-value:** ask, "If that null explanation were true, how often would this test produce evidence this extreme or more?" Smaller values count more against that explanation. They do **not** tell us the chance that our conclusion is wrong.
- **Holm correction:** checking many questions gives more chances for a lucky-looking result. Holm makes the pass rule stricter to allow for that. A **family of 8**, for example, means eight questions were checked together.
- **0.05:** the comparison line used for the statistical checks here. A corrected p-value below it passes that rule. Passing does not mean a large effect; not passing does not prove no effect. **Paired** means the methods are compared using matching people or records.

A result near chance does not prove that nobody could attack the system. A missing experiment is not a zero score. And a higher score on one dataset does not mean it is an easier or better system: candidate counts and pictures differ.

## How to read any picture or number

1. Read the title: what question is this picture asking?
2. Read the labels along the bottom and side. They tell you what moves and what is measured.
3. Find the legend: it tells you what each color, line or shape means. Colors do not always mean the same thing on different pages.
4. Look at the dot, then its whisker. A dot is the estimate; a long whisker means more uncertainty or variation, as the caption explains.
5. Read the dotted or dashed reference line. It often means blind guessing; on difference plots, zero means the two methods tied.

**Rulers are not extra results.** Labels such as `0, 20, 40, 60, 80, 100` are tick marks, like centimeters on a ruler. On an accuracy axis they mean percentages. On a difference axis they mean percentage points. A negative difference means a method did worse, not that it identified a negative number of people. A confidence whisker can extend below 0 or above 100; that is an uncertainty calculation, not an observed impossible accuracy.

**What about numbers beside dots?** `28.23 pp` means an improvement of 28.23 percentage points. `p=0.004` is a separate statistical check, not another accuracy. `N=30` means 30 candidate people. `1/26` means one correct choice out of 26 possible choices when guessing blindly. Slashes can instead separate settings, such as `1/2/5/10` records; read the label.

**Small-print footers:** `19 September 2026` dates the report's experiment update. `1/19` through `19/19` are page numbers. `4352eeb`, `15e4384` and `4831d99` are Git version labels, like labels on saved drafts, not measurements. A later source-recovery check is dated `2026-09-20`. A page reference such as "page 18" tells you where to turn, not how many tests ran.

**Unprinted values:** many curves show dots without writing out each value. Use their axes to see the pattern; do not invent exact decimals from their height. Page 4 is different: its heatmap prints individual scores, and its number table below gives their row and column meanings. The same ruler rule above explains every repeated axis tick throughout the report.

## Page 1: The four collections of pictures

MOBIO has **150 people**, LFW **125**, FEI **200**, and SCface **130**. The three split numbers tell us how many people teach the attacker, help choose the trained model, and finally test it. Those groups do not overlap within an experiment.

The valid-picture counts are **1,799/1,800**, **1,500/1,500**, **2,378/2,400**, and **2,851/2,860**. The missing pictures failed extraction; these fractions are not attack accuracy.

**Read the table like a school register:**

| Collection | People in total | Learn / practice / final test | Pictures usable / selected | Pictures not usable |
|---|---:|---|---|---:|
| MOBIO | 150 | 90 / 30 / 30 | 1,799 / 1,800 | 1 |
| LFW | 125 | 75 / 25 / 25 | 1,500 / 1,500 | 0 |
| FEI | 200 | 120 / 40 / 40 | 2,378 / 2,400 | 22 |
| SCface | 130 | 78 / 26 / 26 | 2,851 / 2,860 | 9 |

"Practice" is validation: it helps choose which trained version to keep. The final-test people do not teach the model. SCface still has all **130 people** after the **9** picture failures. "Session" means different visits; "pose" means how a face is turned; "camera/distance" means where it was photographed.

SCface tests mugshot references against surveillance pictures. Its old unprotected reference gets **84.375%**, or **459 of 544 probes**, right. That is a separate task from combining ten protected records.

**73 conditions**, **72 pilots**, **216 original endpoints**, **144 pool-study fits**, **72 baseline evaluations**, and **672 extended endpoints** count different experiment packages. They are not independent people and must not be added up as a sample size.

**The smaller count labels:** the **73** settings belong to **12** earlier studies. The pilots have **24 cells**, with **3** model choices per cell, giving **72** model endpoints, each using just **one** training start. A pilot is an early trial, not strong confirmation. The later **216**, **144 + 72**, and **672** counts belong to separate studies explained on pages 6, 16 and 17. The SCface blind-guessing line is **1/26 = 3.846%**, because its final gallery has **26** people. **544** counts individual test pictures in the old unprotected check, not people.

## Page 2: How the experiment works

Follow the arrows: pictures -> face-number lists -> protection -> sets of records -> trained attacker -> predicted face-number list -> gallery choice.

**512-D** means 512 coordinates. **128 bits**, **512 bits**, **300 codes**, **4,800 entries**, and **170 real numbers** describe different protected formats, not security guarantees. IoM has 300 choices among 16 options, expanded to 300 x 16 = 4,800 entries for training.

Most studies shrink each face list to length one before protection. The new raw study skips that step. **1/2/5/10** is the number of clues. **Eight sets per person** are repeated selections that can reuse pictures, not eight independent people.

**Read the numbered boxes:** **1** separates the people into groups; **2** turns pictures into face-number lists; **3** applies a secret recipe; **4** gathers clues; **5** learns to guess a face-number list; **6** produces that guess; **7** chooses the closest gallery person. These box numbers are step labels, not scores. A/B separate the two halves of the diagram.

**Every size and setting in the boxes:**

| Printed label | Plain meaning |
|---|---|
| 5-landmark alignment | Use five face landmarks to position the face before measuring it. This is not five people. |
| ArcFace `w600k_r50` | A pretrained model's name. The embedded numbers identify the model, not this experiment's people or accuracy. YuNet finds the face; ArcFace measures it. |
| 512-D | Each unprotected face list has 512 number slots. |
| BioHash: 128 bits | Its protected list has 128 yes/no slots. |
| MLP-Hash: 512 bits | Its protected list has 512 yes/no slots. |
| IoM-GRP: 300 codes, q=16 | Make 300 choices; each choice selects one of 16 options. |
| One-hot d=4,800 | Write each choice as 16 switches, only one on. That gives 300 x 16 = 4,800 switches. |
| PolyProtect: 170 reals | Its protected list has 170 ordinary numbers, which need not be just 0 or 1. |
| Window m=5, overlap=2 | Process five input numbers together; neighboring groups share two input positions. |
| Batch x n x d | Several sets at once; n clues in each set; d numbers in each clue. |
| 8 nested sets; n=1, 2, 5, 10 | Make eight repeated selections per person. Within a repeat, the smaller selection is contained in the larger one. Counts used depend on the study. |
| d -> 256 -> 512 | The guessing machine takes d numbers, processes them through 256 internal units, and outputs 512 numbers. |
| L2-normalized | Rescale the whole output list to length one, keeping its direction. The 2 names a way to measure length; it is not two records. |
| Top-1 / top-5 | Is the correct person the first choice, or anywhere in the first five choices? |
| 2 splits x 3 seeds; 120 epochs | Try two people-group assignments and three training starts. Training can make at most 120 passes through its training sets. |

`T = f(key, x)` says "apply the secret recipe, using the key, to face list x; call the result T." `K` counts recipes in the pool. **Mean** averages numbers; **max** keeps the largest number in each slot. **AUROC** measures how well scores separate matches from nonmatches across decision cutoffs. **EER** is the error rate where false matches and missed matches balance. **TAR at FAR** counts accepted genuine matches at a chosen false-match rate. These labels list evaluation tools; this box does not report numerical results for them.

## Page 3: Two ways to combine clues

The top route averages the protected lists, then tries to reconstruct an identity vector. DeepSets, the lower route, first learns features from each list and then averages those features. The one-record model is the baseline.

**B x n x d** means number of sets in a batch x records in each set x numbers in each record. **256** is a hidden layer's width; **512** is the reconstructed vector's width. These are model sizes.

The target comes from the exposed training pictures, not the secret test person's gallery image. **0.001**, **0.0001**, and **0.1** are training settings, not success rates. **120 epochs** is a training limit, not necessarily the number used before early stopping.

Page 16 adds a third comparison: reconstruct each record using the one-record model, then average those predictions.

**The picture, step by step:** A builds the clue sets. B offers two routes through the guessing machine. C teaches it using training faces. D tests whether its guess finds the right gallery person. The gallery stays out of the clue set, so the machine cannot simply copy the answer picture.

**The shapes and formulas are sizes and instructions, not success scores:**

| Printed expression | Read it like this |
|---|---|
| T: B x n x d | B sets, n clues per set, d number slots per clue. The four d values are 128, 512, 4,800 and 170, explained on page 2. |
| B x d; baseline n=1 | Pooling leaves one protected list per set. The baseline starts with only one clue. |
| Linear d -> 256; 256 -> 512 | Two processing steps: first 256 internal units, then the 512-number guess. |
| phi: d -> 256 -> 256; B x n x 256 | DeepSets first turns each clue into 256 learned features using the same rule for every clue. |
| sum(m * phi(T)) / sum(m); B x 256 | Add the valid clue features and divide by the number of valid clues: an average. m marks which clues are valid; all n are valid here. |
| rho: 256 -> 256 -> 512; B x 512 | Turn the averaged features into one 512-number guess per set. Phi and rho are names for the two learned processing rules. |
| ReLU | Keep positive internal values; replace negative ones with zero. |
| z = output / length(output) | Rescale the guess to length one. The printed double bars and subscript 2 are the length notation. |
| u = normalize(mean(...)) | The training answer is the length-one average of the exposed training face lists. It is not the gallery picture. |
| 1 - cosine(z, u) | Compare the direction of the guess z with answer u. A perfect direction match has cosine 1, so this part becomes 0. |
| + 0.1 x MSE(z, u) | Also punish differences between corresponding number slots. Square them, average them, and give this part a weight of one tenth. |
| Adam; lr 0.001 | Adam is the update rule. 0.001 sets its learning-step scale; it is not 0.001% accuracy. |
| Weight decay 0.0001 | A small setting that discourages overly large learned weights. It is not a measured error rate. |
| G: N x 512; scores = z G^T | The gallery has N people, each represented by 512 numbers. Compare the guess with every gallery list and rank the scores. The superscript T means arrange the table for multiplication. |
| 3 seeds x 2 partitions; 120 epochs | Three training starts for each of two assignments of people; at most 120 training passes per run, possibly fewer if training stops early. |

**Permutation-invariant** means reordering the same clues does not change the pooled answer. **Loss** is the training mistake score: smaller is better. **Minimum validation loss** means choose the saved model that made the smallest practice-group mistake, not the one that looked best on the final test. Top-1/top-5 and the other matching labels mean the same as on page 2.

## Page 4: The older big table of results

The left half uses one clue; the right half uses ten. Read across a row to change the number of reused recipes. A cell such as **33.2** means about 33.2% correct first choices, averaged across three training starts.

For SCface pool 3, the computer goes from **5.29% to 33.17%**: a **27.88-point** increase. Fresh keys give about **3.85%**, near blind guessing among 26 people.

Grey means no available measurement. A star means not every training start's interval passed the old above-chance rule; it does not mean secure. Colors account for different chance rates, but the printed numbers are ordinary percentages. Each row is a study, so several MOBIO rows are not several new datasets.

**Every printed heatmap score:** each list follows the pool order in its row, left to right. For example, in the SCface row, the third pool is **3**, its one-clue score is **5.3%**, and its ten-clue score is **33.2%**. Those are the rounded versions of **5.29%** and **33.17%**. All scores below are percentages averaged over **3** training starts. A `*` keeps the same warning as the picture. A pool absent from a row is a grey cell in the picture; `Not available` means the whole one-clue row is blank.

| Study, in picture order | Pool order | One-clue scores (%) | Ten-clue scores (%) |
|---|---|---|---|
| MOBIO / BioHash / session-aligned | 1, 2, 5, 10, Fresh | Not available | 66.4, 61.1, 47.6, 33.9, 2.9* |
| MOBIO / BioHash / random confirmation | 1, 2, 5, 10, Fresh | Not available | 77.5, 69.4, 46.9, 5.6*, 5.6* |
| MOBIO / BioHash / split B | 1, 2, 5, 10, Fresh | 76.0, 35.0, 4.3, 4.3, 4.0 | 81.7, 73.9, 51.1, 5.6*, 3.6* |
| MOBIO / BioHash / dense A | 3, 4, 6, 7, 8, 9, Fresh | 27.5, 3.5, 3.5, 4.2, 4.0, 3.2, 3.2 | 65.0, 54.0, 17.4*, 34.4, 10.4*, 3.9*, 5.6* |
| MOBIO / BioHash / dense 2 | 3, 4, 5, 6, 7, 8, 9, Fresh | 22.4, 7.6, 6.4, 6.4, 5.0, 3.2, 2.5, 2.4 | 48.6, 48.6, 40.3, 36.4, 30.4, 14.2*, 6.4*, 1.5* |
| MOBIO / BioHash / dense 3 | 3, 4, 5, 6, 7, 8, 9, Fresh | 5.8, 5.4, 4.9, 4.6, 5.7, 3.1, 4.7, 3.8 | 56.4, 51.9, 8.1*, 8.6*, 8.9*, 3.9*, 6.7*, 4.4* |
| MOBIO / Haar BioHash | 1, 5, Fresh | 75.0, 3.5, 3.1 | 74.6, 48.1, 2.6* |
| MOBIO / MLP-Hash / initial | 1, 2, 5, 10, Fresh | 52.1, 33.6, 4.4, 4.6, 2.9 | 71.4, 68.9, 22.9*, 1.9*, 3.1* |
| MOBIO / MLP-Hash / dense | 3, 4, Fresh | 3.1, 4.6, 3.1 | 54.3, 37.8, 3.5* |
| LFW / BioHash | 1, 2, 3, 4, 5, 7, 10, Fresh | 70.7, 37.3, 23.8, 16.8, 11.5, 11.7, 4.3, 4.7 | 73.2, 63.2, 62.5, 42.5, 41.0, 32.0, 25.3*, 4.0* |
| FEI / BioHash | 1, 2, 3, 4, 5, 7, 10, Fresh | 74.6, 36.4, 3.8, 3.4, 2.8, 2.4, 3.0, 2.3 | 76.9, 63.4, 54.8, 47.5, 37.5, 23.6, 4.0*, 1.8* |
| SCface / BioHash | 1, 2, 3, 4, 5, 7, 10, Fresh | 40.7, 22.4, 5.3, 4.0, 5.1, 4.2, 3.2, 4.3 | 81.6, 61.1, 33.2, 20.5*, 5.9*, 1.9*, 3.0*, 3.8* |

**What the names mean:** "session-aligned" uses the earlier session-based setup; "random confirmation" is a separate random-pool check. "Split B" and "dense 2/3" identify different assignments of people. "Dense" means more nearby pool sizes were tested, not denser face images. "Haar" names a correction to how BioHash's random directions are generated. These row names do not make the studies perfectly matched comparisons.

**The color ruler is different from the numbers inside squares.** Its formula is `(accuracy - chance) / (1 - chance)`, using fractions rather than percentages. **0.0** means chance, **1.0** means perfect identification, and **0.5** is halfway between them. For a 30-person gallery, halfway is about **51.67%**, not 50%. Below-chance scores can fall below zero on this color scale. The gallery sizes **30, 25, 40, 26** explain why the color adjustment is needed.

**The caption's pass/fail list:** for SCface, pools **1/2/3** passed the old rule in every training start; pools **4/5/7/10** did not. "Failed the rule" does not mean safe or exactly equal to guessing. **73 conditions / 12 studies** counts the source settings, not 73 new people. Panels **(a)** and **(b)** mean one and ten clues, respectively.

## Page 5: Checking why the clues help

Left: telling the model which recipe slot was used changes scores by **-0.83 to +4.44 points**, not by a huge amount. Replacing nine clues with other people's records gives **3.33%**, suggesting that same-person clues matter. The shuffled control uses a different attacker, so it is not a perfectly isolated model comparison.

Middle: the horizontal axis is the fraction of 128 projection columns shared by the construction. **25% means 32 shared columns**, not 25% of secret keys revealed. More sharing often gives higher scores, but the two sweeps use different partitions and are not perfectly smooth.

Right: using ten copies of one image with different fresh keys and using ten different images both give **3.33%**. That result does not prove all fresh-key systems are safe.

**Read all three pictures:** (a) asks whether knowing which recipe slot made a clue helps; (b) asks whether recipes sharing some internal directions leak more; (c) asks whether repeated pictures explain the fresh-key result. Their rulers are separate.

**Number key:** in (a), **3, 4, 5, 7** are pool sizes. **Records 2-10** means replace the last nine clues, leaving clue 1 as the correct person's anchor. **-0.83** means 0.83 points worse and **+4.44** means 4.44 points better when slot labels are supplied. In (b), **0 to 100%** counts shared projection columns: zero means none; 100 means all **128**. These percentages are not identification scores; identification is on the vertical ruler. "Coarse" and "fine" mean widely spaced and more closely spaced settings, and the fine sweep also changes the people split. In (c), both written **3.33%** labels are the same chance-level result; the vertical **0, 2, 4, 6, 8, 10** labels are percentage ticks, not clue counts. **30** gallery people makes chance **1/30**, about **3.33%**. **Three seeds** means three training starts, not three groups of new people.

## Page 6: The original carefully repeated gain

**The picture asks: how much did nine extra clues help?** Subtract the one-clue score from the ten-clue score. A dot to the right of zero means an improvement. Its whisker is the uncertainty range from re-picking training starts and people, as explained at the top of this guide.

FEI IoM gains are **28.23/25.83 points**; FEI PolyProtect **23.96/21.35**. MOBIO IoM gains are **37.36/40.83**; MOBIO PolyProtect **21.25/29.31**. The two values are different identity assignments, not two entirely independent populations.

All eight corrected p-values are **0.004**. They repeat partly because the permutation test has limited numerical resolution, not because all effects are identical. This study fixed the hidden pool; page 16 tests new pools.

**Every labeled dot:**

| Dataset / recipe | Split 91831 gain | Split 91843 gain | Corrected p-value for each |
|---|---:|---:|---:|
| FEI / IoM-GRP | +28.23 points | +25.83 points | 0.004 |
| FEI / PolyProtect | +23.96 points | +21.35 points | 0.004 |
| MOBIO / IoM-GRP | +37.36 points | +40.83 points | 0.004 |
| MOBIO / PolyProtect | +21.25 points | +29.31 points | 0.004 |

**91831/91843** are replay labels for the two assignments of people, not people counts. **216 endpoints** come from **24 settings x 3 model choices x 3 training starts**. The settings cover **2 datasets x 2 recipes x 2 splits x 3 key conditions** (fresh, one shared key, pool 4). The **8** main questions are **2 datasets x 2 recipes x 2 splits**, all about pool-4 mean pooling. **120** is the training-pass limit. **95%** describes the interval method, not accuracy. **0.004** passes the **0.05** rule after correction. The ruler **0 to 80** is improvement in points; it is not final identification accuracy. "Identity sign-flips" means the check makes pretend comparisons by reversing people's difference signs, to test a no-difference explanation.

The ruler writes **0, 10, 20, 30, 40, 50, 60, 70, 80**. Every step is ten points; these are not nine extra experiment results.

## Page 7: A different attack and a size check

Left: no learned reconstruction is used. The computer directly compares protected probes with a protected gallery. PolyProtect scores **10.91-14.55% on MOBIO** and **10.11-11.64% on FEI**, above their chance levels. A/B are splits; 1/2/3 are three key draws. All 12 corrected tests have **p=0.006**.

Right: inputs are made half as large or twice as large. IoM outputs change by **zero**; PolyProtect changes by roughly **0.51-0.52** or **1.11-1.23** in relative vector distance. These are changes in numbers, not identification percentages. This artificial test alone cannot show that natural vector lengths reveal identity.

**Read the labels:** left panel **(a)** measures how often protected clues find the right protected-gallery person. **A/1, A/2, A/3** use split **91831**; **B/1, B/2, B/3** use split **91843**. Key labels **1/2/3** stand for randomization seeds **91873/91879/91883**. The experiment has **2 datasets x 2 splits x 3 key seeds = 12 tests**, so **12/12** means all passed the corrected check. **p <= 0.006** means none of their corrected p-values is larger than 0.006. The **0.0, 2.5, 5.0, ... 20.0** labels are percent ruler marks; "identity-balanced" gives each person equal weight.

Right panel **(b)** stretches number lists, not faces. **0.5 x** means halve every input number; **2 x** means double it. Its **0.0 to 1.6** ruler measures relative change, not accuracy: a value of 1 means the change is as large as the original protected list's length. **L2** names the distance rule. The test uses **32 held-out records per dataset/split**, not 32 new datasets. Keys stay fixed so this comparison changes size, not recipe. The **95%** bars on the left use people as the uncertainty units. Shuffling gallery labels asks whether correct name assignments explain the matching result.

The left ruler writes **0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0**: steps of 2.5 percentage points. The right writes **0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6**: steps of 0.2 in relative change. They measure different things, so do not compare their heights as if the rulers were the same.

## Page 8: Earlier trial runs

The columns are MOBIO, FEI and SCface; the rows are IoM and PolyProtect. Grey squares use one record, blue circles use ten with mean pooling, and green triangles use ten with DeepSets.

The horizontal labels **1/4/8** count recipes in the pool, not records. Fresh is a different condition. Taller points mean more successful identification. The bars describe uncertainty across people for just **one training start**.

For example, SCface IoM pool 4 goes from **28.37%** with one record to **62.98%** with ten-record mean pooling. That is a pilot finding; the new, more repeated SCface study is on page 17. The separate **12.73/13.73/10.66%** caption values are native matching, not those learned curves.

**Number key:** the six panels are **3 datasets x 2 protection recipes**. **N=30**, **N=40** and **N=26** are the MOBIO, FEI and SCface gallery sizes. Each has **4 key conditions** (pool **1**, **4**, **8**, and Fresh), giving **24 settings**; **3 models** per setting give **72 endpoints**. Here "one seed" really means just one training start per endpoint, not a three-start repeat. **120** is the maximum training passes. **1 record**, **10 records, mean**, and **10 records, DeepSets** name the three plotted methods. The vertical **0 to 100** ruler is percent correct, and the dashed line is chance for that dataset. **95%** whiskers describe uncertainty across people with that single training start held fixed.

**The three caption scores belong to a different test:** **12.73% = MOBIO**, **13.73% = FEI**, **10.66% = SCface**, all from direct protected-gallery matching. Do not read them as the heights of the learned curves. This is an early practice round, not the final repeated test.

## Page 9: What is new, and what is not

Researchers already knew that multiple records can help, learned models can extract identity, and naive PolyProtect settings can retain links. We must not claim to invent those ideas.

Our useful question is narrower: **when hidden recipes are reused, how much does combining different pictures help, and when does it fail?** The new independent pools and simple baseline make that question more credible.

The literature comparison used the author's full thesis chapter for the maximal-linkability work. The publisher version was blocked, so its exact identity remains unverified. The local stricter-policy test on page 19 is not proof that every recommended PolyProtect policy is broken.

**This page is a reading list, not a results graph.** **2022** is the PolyProtect publication year. **1-10-record inversion** means that earlier work studied reconstructing inputs using between one and ten records; it is not our accuracy. **FaceLinkGen v3** names version 3 of another work. **5.4** is a thesis section, not a score of 5.4. **Access 2024** identifies a journal publication/year. **2026-09-18** in the literature-document path is a date label. "One-to-ten benefit" means comparing one clue with ten. None of these bibliographic numbers is evidence that we beat the earlier work.

## Page 10: What help does the attacker need?

It must know which records belong together, have training examples from the **same hidden pool**, and have a gallery that contains the target. It does not receive the key values.

We tested **25-40 possible people**, not searching everyone on the internet. We did not test unknown grouping, open-set rejection, or training with an unrelated provider's keys. These strong assumptions belong in the paper.

**Imagine a small class register:** the answer must be one of the people already on it. The four possible gallery sizes are **25, 26, 30 and 40**, depending on dataset. That is what the printed **25-40** range means; it is not an accuracy range. "Closed set" means the right person is guaranteed to be listed. "Open set" would allow "none of these people," which was not tested. "Paired examples" means seeing a training face-number list together with the protected clue made from it. The hidden recipes used for those examples must be the same pool used for the test clues.

## Page 11: Checking the measuring tools

The protection formula was calculated separately and matching was checked another way. **48 cells** means combinations of datasets, splits, input versions and key seeds, not 48 people.

**1.33e-15** is a tiny score difference near floating-point precision, and predictions agreed. **4,177** raw embeddings were re-extracted in the older MOBIO/FEI audit. Normalized coordinates differed by at most **2.98e-8**, another tiny number.

None of **38,400 sampled IoM codes** changed under raw/unit scaling. These are code entries, not people. This is computational checking, not an independent scientist's review or proof that every bug is impossible.

**This page checks the measuring tool before trusting its scores.** Think of adding the same sum in two different ways. Agreement is useful, but does not prove every question was set up correctly.

| Printed number | What it counts or measures |
|---|---|
| 48 matched cells | 2 datasets x 2 people splits x 4 input versions x 3 key seeds. The methods use matching settings so their calculations can be compared. |
| Zero after float32 casting | Both protection calculations give the same output when stored using the same 32-bit number format. This is not zero leakage. |
| 1.33e-15 | 0.00000000000000133: the largest difference between two matching-score calculations. Very tiny; their final person choices agreed. |
| Zero gallery/probe overlap | The answer picture was not also used as the query picture in the checked matching setup. |
| Zero ties, reversed-gallery changes, duplicate fresh keys | The checked scores did not tie; reversing gallery order did not change the chosen person; fresh keys did not duplicate. Each zero belongs to a different check. |
| Three-key averages | Average results from three key seeds, not from three people. |
| 4,177 | All 1,799 MOBIO plus 2,378 FEI records were re-extracted for this audit. |
| 2.98e-8 | 0.0000000298: the largest checked normalized-coordinate difference after re-extraction. This is not identification accuracy. |
| Zero of 38,400 codes | None of the sampled IoM choice codes changed when raw vectors were rescaled to unit length. It is not 38,400 independent faces. |

"Scalar" means calculating the recipe in small steps. "Matrix" means calculating with number tables. "Cosine" compares directions. "Zero padding" fills missing positions with zeros. These checks concern the local implementation; they are not a certificate from the original authors or an independent scientist.

## Page 12: Does a vector's natural length explain matching?

Four versions are compared: length one, original raw length, lengths shuffled among records, and one common length. Blue circles and green squares are two identity assignments.

Unit-input native matching is around **11-12%**; raw is **15.58-16.66%**. But shuffled lengths do about as well. Only FEI's raw-versus-unit paired gain survives correction. We therefore do **not** establish that each person's natural length reveals their identity.

The **0.0032** p-value tests matching against a label-shuffling null, not whether raw beats shuffled. Those are separate tests. Page 18 is a different experiment: it trains an attacker on raw-input protected records.

**Four ways to prepare the same clues:** Unit makes every face list length **1**; Raw keeps its original length; Shuffled norms hands lengths to different records; Fixed radius gives every record the training group's middle length. If a person's own length explained the gain, mixing up whose length belongs to whom should matter. Here that explanation was not established.

**Number key:** there are **2 datasets x 2 splits x 4 input versions = 16** matching-versus-shuffled-label questions. **All 16** pass that check with corrected **p=0.0032**. Each point averages **3** fixed key seeds. The **95%** whiskers re-pick people; the vertical **0, 5, 10, 15, 20, 25** marks are percentages. **15.58-16.66%** gives the raw-matching range, not its improvement. For the separate raw-minus-shuffled question, every corrected **p >= 0.7584**, above the **0.05** rule: these tests do not establish a difference. That does not prove the methods are equal.

**A caption that needs context:** "No learned raw-input attack was retrained" refers only to this older audit. Page 18 reports a later, separate learned raw-input study. This page compares protected clues directly; it does not train the reconstruction attacker.

## Page 13: Results that did not improve

Left: pool-4 DeepSets gains are uncertain after correcting all 48 comparisons; none passes that larger family. A bar can sit above zero while its multiple-test-adjusted p-value does not pass 0.05.

Right: with one shared PolyProtect key, DeepSets loses **15.42, 20.42, 24.17 and 24.86 points** against the one-record model. All four losses pass the corrected test at **0.0192**.

These are decreases, not negative accuracies. They show why the paper cannot say that more clues or a fancier model always helps. The cause of the losses has not been isolated.

**Read the two rulers separately:** the left runs **0, 10, 20, 30, 40** points; the right runs **-40, -30, -20, -10, 0**. Both subtract the one-clue result from the ten-clue result. On the right, farther left means a bigger loss. **A/B** are the two people assignments, not model grades.

**Why do the p-values differ from page 6?** Page 6 asks **8** planned main questions. This later look asks **48** questions together, in either direction: improvement or worsening. It uses a stricter correction because it checked more things. The smallest corrected p-value for the left-panel DeepSets gains is **0.0576**, which is above **0.05**. All **4** right-panel losses pass at **0.0192**; all **8** pool-4 mean-pooling gains also pass this larger family at **0.0192**. The **95%** whiskers are built for each result separately, so looking at one whisker is not the same as passing the many-question check. "Leave-one-seed-out" means repeat a summary after leaving out one training start, to see whether that start drives the finding.

## Page 14: The message so far

Hidden reuse can make multiple records useful to the tested attacker, but the effect depends on the scheme, data and actual pool. Fresh-key failures do not prove privacy. Native and learned matching answer different questions.

The earlier **216 endpoints**, **eight primary gains**, and **15-25-point losses** are summaries of earlier pages, not new experiments. SCface now also has the expanded study on page 17. Pages 18-19 add negative results, not universal defenses or universal scheme breaks.

**All numbers on this summary page:** SCface **pool 3** means three hidden recipes; **5.29% -> 33.17%** compares one clue with ten; **3.846%** is blind guessing among 26 people. **15.42-24.86** is the exact range behind the rounded "15-25-point losses." **Four datasets** means MOBIO, LFW, FEI and SCface. The **216 endpoints / 8 primary contrasts** refer to the original follow-up on page 6, even though the page calls it "new"; the later **672**-endpoint extension is page 17. **Three new pools** is the small repetition study on page 16; **one encoder** means the same face-measuring model was used throughout.

**33/33 sources verified** means every one of the 33 files listed in the extended experiment's saved checklist matched its recorded digital fingerprint on the experiment machine. That includes the three files that could not initially be matched on this computer. This is a source-file check, not 33 successful attacks or proof of the whole scientific conclusion. The archive verification is documented by the experiment-machine check; independent human scientific review is still needed.

## Page 15: Why some datasets appear in some graphs

This is a coverage map, not a scoreboard. Columns are the four datasets; rows are different study types. Colored cells mean completed work. Grey means not run in that particular study.

All four have historical BioHash results. MOBIO/FEI have the three-pool baseline study. MOBIO/SCface have the new 1/2/5/10-record study, raw learned study and stricter-selection audit. LFW and FEI were not silently added to those new experiments.

Numbers inside cells tell you how many seeds, splits or pools were used. They do not tell you accuracy. We should not fill a missing cell with a result from another protocol.

**Read it like a homework checklist:** a colored square says "we did this kind of work for this collection." Grey says "not in this study," not "the score was zero." Here is every row and number label:

| Row | Where work was done | What its numbers mean |
|---|---|---|
| BioHash historical | All four datasets | 3 model seeds: three training starts. |
| MLP-Hash historical | MOBIO only | 3 model seeds: three training starts. |
| IoM / PolyProtect pilots | MOBIO, FEI, SCface | 1 model seed: an early trial with one training start. |
| Original scheme follow-up | MOBIO, FEI | 3 seeds / 2 splits: three starts for each of two people assignments. |
| Native / raw-norm audit | MOBIO, FEI | 3 keys / 2 splits: three key seeds for each of two assignments; no attacker training here. |
| Independent-pool + baseline | MOBIO, FEI | 3 pools / 3 seeds / 2 splits: three recipe pools, three training starts, two assignments. |
| Extended exposure study | MOBIO, SCface | 3 seeds / 2 splits: three starts for each of two assignments. |
| Learned raw-input study | MOBIO, SCface | 3 seeds / 1 split: three starts, with only one saved assignment. |
| Stricter-selection audit | MOBIO, SCface | 3 keys / 1 split: three key seeds, one assignment; direct matching, not attacker training. |

The same people can appear again in a different split, so the splits are not fresh populations. "Coverage" means which work exists, not that every dataset used identical pictures or gallery rules.

## Page 16: New secret pools and a simple alternative

Left: colored dots are three new pools. Black diamonds average them; bars include uncertainty across pools, training starts and people. IoM gains stay positive in all **12 dataset/split/pool combinations**, from **21.56 to 42.36 points**. PolyProtect ranges from **-3.23 to +72.40**, so its average hides large pool dependence.

Right: compare averaging protected inputs with averaging predictions from the one-record model. Every direct comparison interval includes zero. We cannot claim input averaging is better, or that both methods are exactly equal.

The baseline sees the same test records and gallery, but uses one-record training rather than set training. **Three pools** are useful evidence, not enough to claim universal robustness.

**A simple comparison:** left asks "do ten clues beat one?" Right asks "is it better to average clues first, or make a guess from each clue and average the guesses?" On the right, zero means a tie between those two averaging methods, not zero identification.

**Every count and legend number:** **24 cells = 2 datasets x 2 recipes x 2 splits x 3 pool draws**. Each cell trains a one-clue and a ten-clue mean model with **3** starts, giving **144 fits**. Reusing the single-clue model for prediction averaging adds **72 evaluations**, not 72 more training runs. The labels **91901, 91907, 91909** name the three pool shuffles. **A/B = 91831/91843** name the two assignments of people. Each colored dot averages three starts; black diamonds average pools too. Their **95%** whiskers re-pick pools, starts and people. The ruler **-20, 0, 20, 40, 60, 80** measures percentage-point differences.

**The ranges:** IoM's **+21.56 to +42.36** points are positive in all **12** dataset/split/pool combinations. PolyProtect's **-3.23 to +72.40** means some settings worsen and some improve greatly. Different colors change both the actual recipes and which records use which recipe. This is not a test of pool size alone. "Pointwise" means each whisker is for one comparison; this figure does not claim a corrected many-comparison pass.

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

**Read the picture as eight small worksheets:** the top four use MOBIO, the bottom four SCface. Each row separates IoM/PolyProtect and splits A/B. **Grey = Fresh; green = pool 1; blue = pool 4; orange = pool 8.** Along the bottom, **1, 2, 5, 10** counts clues about one person; those are not pool sizes. Up the side, **0 to 100** is percent correct. The one-clue dot comes from the single model; the two-, five- and ten-clue dots use mean pooling. Joining them with lines helps your eyes follow the pattern; it does not test every number between them.

**Where all the counts come from:** **32 cells = 2 datasets x 2 recipes x 2 splits x 4 key conditions**. In each cell there is **1** single-record model plus **2** ways to combine clues (mean/DeepSets) at **3** clue counts (2, 5, 10), making **7** model/count choices. Each uses **3** training starts: **32 x 7 x 3 = 672** endpoints. The **56 fresh summaries = 2 datasets x 2 recipes x 2 splits x 7 choices** average those starts. Their **95%** intervals all include chance; this means a chance-level explanation remains compatible with these intervals, not that it is proven true.

**Eight planned gains:** the table above names every split's result. The printed **p=0.004-0.034** range runs from the smallest to the largest corrected p-value in that table; all are below **0.05**. SCface's **+16.19/+34.29** and **+5.93/+5.77** are improvements, not final accuracy. **One pool-8 draw** means only one realized set of eight recipes per condition, not eight independent pool experiments. A/B reuse the same population under different assignments.

## Page 18: Training with original-length face vectors

These plots show **raw-input results only**. Grey is one record; blue is ten-record mean pooling; green is ten-record DeepSets. Each bar is the standard deviation across three training starts, **not a confidence interval**. The dotted/dashed chance line is the guessing reference.

Pool-4 ten-record mean accuracy is **91.11% MOBIO / 67.63% SCface for IoM**, but only **3.61% / 3.85% for PolyProtect**. The tested raw PolyProtect attacker did not show a useful mean-pooling gain. This is an important boundary to report, not evidence to hide.

Do not subtract these scores from page 17 and call the difference a normalization effect. The studies use different key seeds, record selections and identity assignments. Raw vectors also change how training targets are averaged: long vectors get more weight. A matched unit/raw run would be needed to isolate those effects. This study is descriptive and does not prove raw input is safer.

**Imagine combining votes of different strengths:** when original-length lists are averaged to make a training answer, longer lists can pull the average more. Making every list length one changes that weighting as well as what goes into protection. That is one reason these two studies cannot answer "did length alone cause the score change?"

**Number key:** **24 summaries = 2 datasets x 2 recipes x 2 key conditions x 3 model/count choices**. **Three starts** per summary gives **72 fits**. There is **one** saved people assignment. **Single, 1** means one clue; **Mean, 10** means average ten clues; **DeepSets, 10** means learn features from ten clues before combining them. **Pool 4** means four recipes reused, not four clues. The vertical **0, 20, 40, 60, 80, 100** marks are accuracy percentages.

| Ten-clue mean model, pool 4 | MOBIO | SCface |
|---|---:|---:|
| IoM | 91.11% | 67.63% |
| PolyProtect | 3.61% | 3.85% |

**The whiskers here are different:** standard deviation describes the spread of the three training-start scores around their mean. It is not a **95% confidence interval** and does not give a corrected statistical pass. The dashed lines mark chance, about **3.33%** for MOBIO and **3.85%** for SCface. Near-chance performance of this tested model does not promise safety from other attacks.

## Page 19: Trying a stricter recipe-selection rule

This returns to direct protected-gallery matching. Our local rule tries **20 candidate parameter choices**, uses **200 development pairs**, and favors scores inside **[-0.5, 0.5]**. Development people are separate from test people. It is one local interpretation of the paper's rule, not an exact official-code reproduction.

The dot shows stricter accuracy minus naive accuracy. **Left of zero would mean less leakage.** MOBIO rises from **13.13% to 16.26%**, a **+3.13-point** change; SCface falls from **10.44% to 10.12%**, a **-0.32-point** change.

The intervals are **[0.10, 6.16]** and **[-2.19, 1.47] points**. The corrected paired p-values are **0.1344** and **0.7556**, so neither establishes a change at 0.05. Both versions still match above their label-shuffling null (**0.0008** after correction). That is not proof that every stricter policy fails.

**Read the picture:** choose a row, then find its dot. The dotted vertical line is **zero change**. Left would mean the stricter rule reduced matching; right would mean it increased matching. The **-4, -2, 0, 2, 4, 6, 8, 10, 12** tick marks are a difference ruler, not final percentages. The two whiskers show the ranges written above. Even though MOBIO's ordinary interval is above zero, its corrected p-value does not pass the two-question rule; the interval and correction are different checks.

| Printed setting or test | What it means |
|---|---|
| 20 candidates | Try 20 possible parameter choices for a key and score them using the development data. |
| 200 development pairs | Use 200 pairs from development people to judge the choices; these are not 200 final-test people. |
| Score band [-0.5, 0.5] | Prefer choices whose development similarity scores fall between minus one half and plus one half. These are similarity numbers, not accuracy percentages. |
| 3 fixed key seeds per dataset | Repeat direct matching with three saved key randomizations. No reconstruction model is trained on this page. |
| 13.13% -> 16.26%; +3.13 pp | MOBIO: stricter matching was 3.13 points higher in this measurement, not lower. |
| 10.44% -> 10.12%; -0.32 pp | SCface: stricter matching was 0.32 points lower in this measurement. |
| 95% intervals [0.10, 6.16] and [-2.19, 1.47] | Uncertainty ranges for the two gains. People are re-picked, while the three chosen key seeds remain fixed. |
| Holm family 2; 0.1344 and 0.7556 | Two questions: did the stricter rule change matching on MOBIO, and on SCface? Neither corrected p-value is below 0.05. |
| Four arms; Holm p=0.0008 | 2 datasets x 2 rules (naive/stricter). Each still beats its shuffled-gallery-label check. This is a different question from whether the rules differ. |

**Takeaway:** this particular stricter rule did not establish a reduction. "Naive" means simple random parameter selection here, not a judgment about a person. The rule is our local interpretation; it is not a test of every stricter policy or an exact copy of the original authors' software.

## Is the paper stronger now?

**Yes, as a careful empirical paper.** It has more repeated SCface evidence, intermediate record counts, a larger-pool check, a simple baseline, and honest negative results. Better evidence does not mean every accuracy number gets larger.

Think of it as a stronger school science report: more checks, more repeated trials, and an honest account of what did not work. It is enough to write up these specific findings for coauthors to review, not a promise that a journal will accept them.

**The missing-file worry is resolved in the experiment-machine check, dated 2026-09-20:** all **33/33** listed files matched their saved fingerprints, including the three that this computer could not initially match. See the [recovery account](final_research_status.md#provenance-check). The recovered archive is not included in this checkout, so this guide reports that documented check rather than claiming to have repeated it here.

The conclusion still needs its limits: the training examples use the same secret pool, one face encoder is tested, the gallery is small, and only the named recipes and settings were tested. Finish the references, journal formatting, explanation of permitted data use, and review by other scientists. To explain whether raw length alone causes an effect, another experiment would need to hold the other settings fixed. We can report the current observation without claiming to know its cause.

No new training was run to make this guide. The private SCface pictures and records are absent on this computer, so this update does not independently check their contents. The preparation code gives mugshots index **0** and uses them as gallery references; **0** is a record-position label, not a zero score. The saved protocol describes the intended camera split.

## Where to look next

- [Extended-study tables and protocol](../experiments/scheme_followup_2026-09-19_full/README.md)
- [Raw learned results](../experiments/raw_input_attacker_2026-09-19/README.md)
- [Stricter-selection results](../experiments/polyprotect_stricter_audit_2026-09-19/README.md)
- [Detailed page guide and older exact tables](Sept_Dataset_Update_guide.md)
- [All 22 figures](slides/figure_appendix.pdf) and [15-slide overview](slides/research_review.pdf)

Footer commit identifiers label versions of the work. They are not scores. No raw faces, private embeddings or secret keys are included in these documents.