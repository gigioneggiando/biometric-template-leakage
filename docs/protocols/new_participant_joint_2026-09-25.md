# New-participant joint evaluation linked to source analysis

Version 1, prepared 2026-09-25 before any new-cohort outcomes. Status: blocked on
authorized new data, independent review and sample-size approval. The user has
confirmed that no new authorized cohort is currently available and requested
protocol/report preparation only. No recruitment, download or new experiment has
been performed. This is a proposed fixed design, not an externally registered or
fully approved confirmatory protocol. Any change requires a dated new version
before accessing new-cohort test outcomes.

## Question and link to the algorithm

Does the preselected source-guided change from a four-key pool to per-record
derivation reduce the tested attack while retaining matching within a three-point
tolerance on genuinely new people, with controlled false matches?

| Stage | Repository implementation | Required evidence |
|---|---|---|
| Inspect source | `analyse_source` on executable `recurring` and `separated` recipes | JSON traces, source and analyzer hashes; complete reuse and conditional_fresh decisions respectively |
| Select change | Replace finite-pool assignment with record-specific derivation | Preselected recipe pair; no test-driven search; no claim that an automatic general source rewrite exists |
| Admit participants | Cohort provenance and duplicate/identity review | New people relative to all earlier development, training, validation and test inputs, not just a previous test split |
| Apply recipes | Existing pilot projection/protection functions | Every experimental template agrees with the directly executed audited recipe; explicit row-to-record-ID map |
| Test both goals | Mean-MLP attack plus trusted-key verification | Same test people, raw records, enrollment images, key draws and comparison arms |
| Decide | Three simultaneous bounds | All attack-reduction, TAR-retention and FMR criteria pass together |

The [local audit](../../experiments/new_participant_joint_2026-09-25/cohort_audit.json)
contains the actual analyzer traces: recurring and partial are reuse; separated
is conditional_fresh. It verifies unchanged prior FEI/MOBIO input hashes and
finds zero eligible new IDs. The analyzer flags implementation structure; the
key-policy change is the intervention, and empirical measurements determine its
effect. A successful policy comparison alone would not establish detector accuracy,
novelty or superiority over a human who selected the same change. The separate
independent source-case review remains necessary.

## Data admission and collection handoff

The current local FEI raw directory contains 2,800 images from 200 participant IDs.
The embedding file contains 2,378 records from all 200 IDs. More views, augmentation,
new splits or relabeling cannot create new participants. MOBIO's current 1,799
embeddings contain 150 IDs, all previously used. These statements concern the
available files, not every possible dataset release. The available LFW data is
not certified new, and another dataset must not be silently labeled an FEI extension.

An institution/data owner must supply an authorized cohort and record:

- Dataset name, version, official source, permission reference, permitted processing
  machines/collaborators, storage period and aggregate publication terms. For new
  collection, obtain the applicable ethics approval and informed consent before
  collection. Do not upload faces or credentials into chat or the public repository.
- Stable pseudonymous person IDs, capture/session IDs and provenance for every
  image. Keep the identifying linkage and permission documents in restricted storage.
- A reviewed crosswalk against all prior cohorts, including historical training and
  validation people. File hashes find exact duplicate images, not all same-person
  overlap. Different dataset prefixes are not proof of independent people. Human
  data-owner review must resolve aliases and unresolved overlap before admission.
- At least 11 distinct usable photographs per included person: one enrollment image
  plus ten exposures. No duplicates or augmented copies as extra observations.
  Prefer capture-session diversity; disclose same-session limitations. Freeze
  timestamp/session-based ordering before inspecting protected matching outcomes.
- The same buffalo_l recognition model and YuNet preprocessing as the pilot, with
  model hashes recorded. Use the first 11 successful distinct images in the frozen
  order per person. Exclude insufficient records before splitting; report attempted,
  failed and excluded counts. Validate finite 512-dimensional unit embeddings.
- Capture and population characteristics, available consent-compatible demographic
  coverage, and unresolved recognition-model pretraining overlap. New to our study
  does not mean absent from the pretrained model's training data.

These checks are not all implemented by the lightweight local overlap audit. That
audit intentionally never certifies new people on the strength of new IDs alone.
Admission needs a signed provenance decision and its immutable hash.

## Fixed design proposed for approval

One named new cohort only. Target 500 eligible new people: 200 train, 100 validation,
200 test. This gives five times the 40 FEI test identities in the earlier partition,
but is a planning target, not a demonstrated 80% or 90% power calculation. Under a
simple independent-person approximation, only the identity-related error component
would scale like sqrt(40/200); key, gallery and cohort uncertainties do not disappear.

Before enrollment or execution, a statistician/domain owner must evaluate this
target using a paired hierarchical simulation informed only by older data, varying
identity and key heterogeneity and expected changes. Specify and approve a target
power (proposed 80% joint-gate power) and assess interval coverage. No such simulation
or approval is claimed here. If it rejects the target, revise this protocol before
new test outcomes exist. Do not enroll additional people until the gate passes.

Freeze the eligible roster, deterministic selection and split membership before
training. If more than 500 people qualify, use a seed-92951 shuffle of sorted stable
IDs and keep the first 500, then a seed-92953 shuffle assigns 200/100/200. If fewer
qualify, stop: do not shrink the test cohort or loosen the tolerance after observing
results. A different cohort is an external generalization study, not a direct FEI
replication. Register its name, provenance and interpretation before the test.

| Setting | Fixed proposed value |
|---|---|
| Arms | Audited recurring pool 4 and separated per-record keys |
| Representation | 512-dimensional unit embeddings; sign-corrected 64-bit BioHash |
| Key seeds | 92901, 92903, 92907, 92909, 92917, 92921, 92927, 92933, 92941, 92947, 92957, 92959 |
| Model seeds, paired in listed order | 94101, 94103, 94107, 94109, 94117, 94121, 94127, 94133, 94141, 94147, 94157, 94159 |
| Attacker | Existing mean_mlp, hidden 256, learning rate 0.001, weight decay 0.0001, cosine + 0.1 MSE |
| Training | Maximum 120 epochs, patience 30, validation selection only |
| Exposures | Ten non-enrollment records, eight sets per person, set seed 92971 |
| Planned endpoints | 24 attacker fits and 24 corresponding verification evaluations |
| Verification threshold | Separate threshold per arm/key seed from validation impostors, target FMR 1% |
| Joint gate | Attack reduction lower > 0; TAR change lower >= -0.03; candidate FMR upper <= 0.02 |
| Bounds | Three one-sided bounds, alpha 0.05/3 each, 20,000 resamples, analysis seed 92983 |
| Compute limit | 3,600 seconds for the fixed experiment, excluding acquisition/extraction |

The 12 key/model seeds are paired joint draws, not a 12-by-12 factorial study.
The same draw pairs the two policy arms. Enrollment selection and exposures are
identical between arms. With exactly ten exposure candidates, the eight permuted
sets give the mean-pool model the same set; they are not eight independent samples.
People, not set repetitions, are the statistical clusters. No partial-sharing arm,
seed selection, architecture search or second cohort enters the primary family.

## Matched attack and legitimate verification

The attacker gets paired protected records and unprotected training targets for
training identities, known grouping and ten stored protected records per target.
It does not get target raw probes, keys or a compatible-encoding service. Recurring
train and test records use the same realized pool, as in the original attack model.
The test is closed-set identification against 200 unprotected enrollment vectors;
chance is 0.5%, unlike the earlier 40-person FEI gallery. Compare arms within this
study, not raw percentages or chance levels across studies.

The trusted verifier re-encodes each raw probe with the claimed enrollment's key,
using keys held outside the leaked template database, and compares Hamming agreement.
Validation chooses thresholds; test never adjusts them. Every test person must have
both attack and matching outcomes in both arms. Export paired identity-balanced
top-1, TAR and FMR with consistent identity ordering, enrollment/exposure manifests
and seed labels. Treat genuine/impostor comparisons as dependent, not independent
Bernoulli trials. The key service and its query restrictions remain strong assumptions.

Use the existing paired-mean interval procedure on seed-by-person matrices, drawing
the joint seed axis and the person axis with replacement. Report the three
Bonferroni-allocated bounds and all point estimates. These are approximate,
gallery-conditional bounds; threshold estimation and a fresh gallery population are
not resampled. Larger cohorts do not turn them into a finite-sample proof.
Application-owner approval of the tolerances and this conditional estimand is required.

All three criteria must pass in this one matched run. Otherwise report which gate
failed, including inconclusive noninferiority. Never borrow an attack bound from
the old pilot to pair with new utility. A pass supports the specified attack,
cohort and trusted verifier only, not general biometric privacy.

## Execution and stopping gates

Before any test outcomes, freeze protocol, reviewed participant manifest, input
and model hashes, exact source snapshot, environment, complete analyzer traces,
split/record-ID mapping, approved sample-size rationale and reviewer decisions.
Any unsupported source finding or failure of source/runtime parity blocks the run.
The existing prototype is not a deployment secret-key generator.

On timeout, missing records, insufficient participants, failed parity, incomplete
paired metrics or metadata-hash mismatch, preserve partial outputs and mark the
study incomplete. Do not calculate a primary success from available seed subsets.
Do not change seeds, exclusions or thresholds to rescue a negative result. A repair
or rerun requires a new dated record and disclosure of any test exposure. No new
runner has been certified against an unavailable cohort; implement and test that
orchestration after data admission, without modifying the historical frozen runners.

Publish aggregate counts and results only. Keep identity-level arrays, source faces,
keys and participant crosswalks restricted. Preserve the earlier pilot's 0/2 joint
gates and replication's 2/4 utility gates as separate historical results.