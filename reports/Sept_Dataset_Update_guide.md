# September report: each page explained simply

Companion to the [14-page report](Sept_Dataset_Update.pdf), revised 18 September 2026. A **template** is a list of numbers describing a face; protection changes that list using a secret key. **Top-1** means choosing the correct person on the first try. **Chance** means random guessing among the gallery's people. Percentage points measure a difference: 10% to 30% is a 20-point increase.

## Page 1: What data did we test?

We use four face datasets with different challenges: sessions, everyday pictures, poses, and surveillance cameras. People used to teach the attacker are different from people used to test it. The newer careful training study contains 216 measured model results on MOBIO and FEI. That does not mean 216 different datasets or independent experiments.

## Page 2: The whole system

A face becomes a number list. A secret key changes that list. The attacker sees changed lists and tries to work out which gallery person they belong to. The diagram shows the route through the system; the attacker is not handed the secret keys.

## Page 3: How the attacker combines clues

We compare one protected record with ten records from the same person. One method averages the records before learning; DeepSets learns about each record before combining them. The training target comes from the exposed pictures, never the separate gallery picture.

## Page 4: What happens when keys are reused?

Imagine a system repeatedly choosing from a small box of secret keys. The attacker can learn patterns even without seeing the keys. The colored table shows older results: how much reuse matters changes across datasets. Grey means not tested; a failed statistical rule does not mean safe.

## Page 5: Are extra records really helping?

We deliberately change parts of the experiment. Replacing most records with other people's records removes the gain. Giving the attacker key-slot names adds little in these controls. These tests help narrow the explanation, but they do not prove every part of it.

## Page 6: The main result repeated carefully

We repeat training with three random starts and two ways to divide people. In all eight planned pool-4 mean-pooling comparisons, ten records help more than one. Gains are about 21-41 percentage points and survive a correction for testing several questions. The partitions overlap, so they are not two completely independent groups of people.

## Page 7: A different way to match records

Instead of teaching a model, we directly compare protected records with a protected gallery. Fresh-key PolyProtect still matches better than random guessing in these tests. Artificially shrinking or growing input lists changes PolyProtect but not IoM. This older artificial-size test alone cannot show that natural face-list sizes reveal identity.

## Page 8: Earlier trial runs

These are smaller trial experiments, including SCface. They helped decide what to investigate next. Most use one random training start, so we keep them apart from the stronger three-start study instead of pretending they have equal reliability.

## Page 9: What is actually different from earlier research?

Other researchers already showed that several records can help, that learned attacks can extract identity, and that naive PolyProtect settings can retain links. Our contribution is the controlled question: **how does hidden key reuse change the benefit of combining different pictures of one person?** We are not claiming to have invented those earlier ideas or beaten their results in a fair head-to-head contest.

## Page 10: What must the attacker have?

It needs to know which records belong together, perhaps from an account label; paired training examples from the **same hidden key pool**; and a gallery containing the target. These are strong assumptions. A training system with unrelated keys does not qualify. We test small lists of 25-40 possible people, not finding anybody anywhere on the internet.

## Page 11: Did we check our measuring tools?

We calculate the protection formula another way and compare two ways of matching. Their predictions agree, with no reused gallery pictures, score ties or gallery-order problems in these checks. We also re-extract 4,177 raw face lists and verify they match the old lists after normalization. This checks computation; it is not an outside scientist's review or proof that every possible bug is absent.

## Page 12: Does the natural size of a face list reveal identity?

The old lists were all resized to length one. We recover their genuine original sizes and compare four versions: unit length, original size, shuffled sizes, and one common size. Raw matching is about 16%, compared with about 11-12% for unit lists. But shuffled sizes work similarly, and only FEI's raw-versus-unit improvement survives correction. We found a scale effect, not proof that each person's natural size reveals who they are. We did not retrain learned attackers on raw inputs.

## Page 13: When does the approach fail?

We report all 48 one-versus-ten comparisons, including bad outcomes. Eight pool-4 average-first gains remain convincing. The more complicated DeepSets method has less certain pool-4 gains, and it becomes about 15-25 points worse in four shared-key PolyProtect cases. More clues and a more complicated model do not automatically give a better answer. We have not yet isolated why those losses occur.

## Page 14: What can we honestly conclude?

Hidden reuse can make several same-person records much more useful to an attacker in this setup. That benefit is not universal. Native matching and learned matching are different tests, and natural norm leakage was not demonstrated. Most importantly: **our attacker failing to do better than guessing does not prove nobody could succeed.** Wider tests, stronger parameter policies and independent human review remain unfinished.

## Where the numbers live

[Trained follow-up](../experiments/scheme_followup_2026-09-18/README.md), [raw audit and complete failures](../experiments/norm_native_audit_2026-09-18/README.md), [closest research and assumptions](../docs/literature/closest_work_2026-09-18.md), [manuscript](paper_draft.md). No raw faces, embeddings or secret keys are included in the report.