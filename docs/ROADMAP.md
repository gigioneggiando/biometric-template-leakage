# Research roadmap after the 2026-09-10 meeting

This roadmap records Sani's requested next phase. It does not change the interpretation of existing results and does not authorize unsupported reproduction or SOTA claims.

## Progress update: 2026-09-18

FEI and SCface are both complete as added datasets beyond MOBIO/LFW: FEI has 200 identities, 2,378 successful embeddings; SCface has 130 identities, 2,851 successful embeddings from a mugshot-gallery/surveillance-probe protocol. Both cover BioHash endpoints 1 and 10 with three model seeds. The user reported approval of IoM-GRP/PolyProtect; both paper-specified implementations and one-seed pilot cells are complete on MOBIO/FEI (16 cells) and SCface (8 cells). This is pilot-grade, single-identity-assignment evidence, not the roadmap's cross-scheme confirmation requirement. Sani supplied the authorized SCface archive directly on 2026-09-18; AgeDB access remains unavailable, see the [request checklist](datasets/access_request_checklist.md).

The subsequent [bounded follow-up](../experiments/scheme_followup_2026-09-18/README.md), authorized for one hour, completed 216 endpoints on MOBIO/FEI with two new identity assignments and three model seeds in 859.63 seconds. Eight primary pool-4 contrasts have Holm p = 0.004 and positive crossed intervals; twelve native PolyProtect controls have Holm p = 0.006. Synthetic radial controls do not complete the natural norm-leakage experiment. SCface embeddings were unavailable locally, so no new SCface training occurred.

The package includes three diagrams, twelve result plots, [an eight-slide PDF](../reports/slides/research_review.pdf), [editable PowerPoint](../reports/slides/research_review.pptx) and [15-figure appendix](../reports/slides/figure_appendix.pdf). Earlier studies, pilots and the bounded follow-up remain separate. The inventory now contains 849 rows / 49 artifacts, preserving all previous 633 rows. A [coverage audit](../experiments/scheme_followup_2026-09-18/coverage_audit.csv) identifies legacy-schema and unavailable-detail gaps; full historical migration remains incomplete. Approved equivalence margins, full cross-dataset confirmation and independent review remain open.

## Meeting decisions

The next evidence package must:

1. validate the fresh-key and transform-reuse findings on **two or three additional facial-biometric datasets**;
2. validate the findings with **two additional face-template protection schemes** beyond BioHash and MLP-Hash; and
3. produce a concise shareable slide/results package explaining the architecture, threat model, methods, protocol, results, controls, and limitations.

The additional datasets and schemes must be selected through the gates below before large runs begin.

## Target evidence matrix

| Axis | Current evidence | Required extension |
|---|---|---|
| Multi-exposure datasets | MOBIO, LFW, FEI, SCface | Two primary datasets (FEI, SCface) added; AgeDB remains an optional third if access and compute permit |
| Protection schemes | BioHash and paper-specified MLP-Hash | Add 2 schemes with distinct transformation families |
| Key conditions | Fresh, shared/reused pools, controlled correlation | Preserve comparable fresh/reuse endpoints for every scheme |
| Exposures | 1, 2, 5, 10 | Preserve 1 and 10 as mandatory endpoints; run 2 and 5 in full confirmation |
| Attackers | Single MLP, mean/max pooling, DeepSets | Keep the same baselines; add scheme-specific inputs only when justified |
| Evaluation | Top-k, AUROC, EER, TAR@FAR, clustered intervals | Add equivalence analysis and cross-dataset/cross-scheme aggregation |

CFP and Olivetti currently support single-template engineering validation. They do not count as new multi-exposure confirmation datasets unless a preregistered protocol demonstrates sufficient identities and at least ten valid records per identity.

## Phase 1: freeze the extension protocol

### 1.1 Dataset selection gate

Select two primary datasets and one contingency candidate. Record the decision in a dated protocol before acquisition or result inspection.

Required selection criteria:

- facial biometrics with stable identity labels;
- enough identities and at least ten usable images or media samples per selected identity;
- meaningful variation in pose, age, illumination, capture device, or environment;
- lawful research access, documented terms, and no redistribution of biometric data;
- feasible download size, preprocessing cost, and runtime;
- no hidden overlap with the training data of the selected face model where this can be audited;
- a defensible identity-disjoint train/validation/test split;
- enough test identities for a meaningful chance baseline and uncertainty estimate.

The official-source review is recorded in [datasets/candidate_selection_2026-09-10.md](datasets/candidate_selection_2026-09-10.md). The proposed selection is not approved until Sani reviews it and the post-download eligibility gates pass.

| Proposed role | Candidate | Scientific value | Blocking checks |
|---|---|---|---|
| Primary A | FEI | High-resolution controlled pose/expression variation; exactly 14 images for each of 200 identities | Official archive hashes; >=10 successful ArcFace embeddings per identity |
| Primary B | SCface | Controlled camera, distance, pose, visible/IR, and resolution variation | Institutional letter and full-time staff signature; detector success; agreement scope |
| Third dataset / contingency | AgeDB | Longitudinal age variation and multiple in-the-wild images per identity | Archive password; eligible identities with >=10 usable images; celebrity/model-training overlap |
| Deferred scale test | QMUL-SurvFace | Native low-resolution surveillance images at larger scale | Terms/provenance clarification; eligible identity and duplicate audit; ArcFace positive control |
| Backup only | CelebA identities | Large in-the-wild collection and acquisition diversity | Identity annotations on request; frequency filtering; strong model-training overlap risk |

IJB-A/B/C and VGGFace2 are not acquisition candidates because their official distributors no longer provide downloads. CMU Multi-PIE is deferred because the current acquisition route is broken/unclear and the official site reports more than 305 GB.

Do not treat CALFW/CPLFW as independent-dataset confirmation without documenting their overlap with LFW.

Dataset acceptance criteria:

- official source and terms recorded;
- archives/files hashed locally and kept outside Git;
- deterministic loader and manifest validation implemented;
- eligible-identity/sample counts documented before model runs;
- split and sample-selection seeds frozen;
- face-detection/extraction success and failure counts reported;
- unprotected ArcFace baseline validates usable identity signal;
- no identity, image, key, or protected-record leakage across splits;
- a compact, non-sensitive dataset card committed.

### 1.2 Protection-scheme selection gate

The source and implementation-fit review is recorded in [protections/candidate_selection_2026-09-10.md](protections/candidate_selection_2026-09-10.md). Paper-specified IoM-GRP and PolyProtect were approved according to the user on 2026-09-12 and implemented for the frozen pilot. SWG-MinHash remains backup; the other candidates remain deferred. Full confirmation and independent source/specification review are separate gates.

Required checks for each candidate:

- primary paper and exact algorithm identified;
- official code, commit, license, and dependencies recorded when available;
- classification stated as source-exact, close, partial, paper-specified, or conceptual;
- input normalization, output representation, dimensionality, and hyperparameters frozen;
- fresh-key, shared-key, recurring-pool, and attacker-knowledge semantics defined;
- deterministic same-input/same-key behavior tested;
- different-key sensitivity and train/test key separation tested;
- output shape, range, entropy, and degenerate-template checks implemented;
- computational cost estimated before the full matrix.

No local approximation may be labelled as an exact reproduction.

## Phase 2: implement and validate inputs

For each accepted dataset:

- add acquisition instructions without embedding credentials or restricted URLs;
- add loader, protocol builder, validation tests, and a small synthetic fixture;
- extract ArcFace embeddings with the existing hash-pinned pipeline;
- record detector failures and demographic/capture limitations available in the source documentation;
- generate identity-disjoint manifests and keep all biometric artifacts gitignored.

For each accepted protection scheme:

- implement it behind the existing protection interface;
- add unit and invariance/key-scope tests;
- create versioned configuration files;
- run synthetic and small real-data smoke checks;
- validate the unprotected and reusable-transform positive controls before interpreting a fresh-key null.

## Phase 3: staged experiment plan

### Stage A: feasibility pilot

Run every new dataset/scheme combination with:

- one-record and ten-record endpoints;
- fresh independent keys;
- recurring pools 4 and 8;
- single-record MLP and ten-record mean-pool/DeepSets;
- one fixed split and one model seed for runtime and failure detection only.

Pilot outputs are engineering diagnostics, not paper evidence. A combination advances only if the unprotected and reusable-transform controls work and no split/key leakage is detected.

### Stage B: confirmatory matrix

For every accepted combination:

- freeze the protocol before inspecting results;
- run 1/2/5/10 exposures;
- run fresh keys plus a justified recurring-pool sweep covering robust, transition, and null regimes;
- use at least three model seeds and multiple identity assignments where dataset size permits;
- report chance-normalized top-1, top-5, AUROC, EER, TAR@FAR, and identity-clustered uncertainty;
- add formal equivalence analysis for the fresh-key endpoint;
- retain the same primary attacker and metric definitions across datasets and schemes;
- record runtime, GPU memory, failed samples, and exact configuration hashes.

### Stage C: targeted controls

Run controls needed to explain inconsistencies:

- non-normalized/norm-leakage control;
- same-image/fresh-key and shuffled-non-anchor controls where applicable;
- transform-slot-known comparison for schemes with recurring discrete slots;
- correlation or partial-reuse sweep only when the scheme exposes a defensible correlation parameter;
- failure analysis by pose, quality, capture condition, and eligible-sample count when metadata allows.

## Phase 4: cross-dataset and cross-scheme synthesis

Produce one canonical aggregate table with one row per dataset, scheme, key condition, exposure count, split, and seed. Every plotted point must be generated from this table.

Required analyses:

- absolute and chance-normalized linkage performance;
- 1-to-10-record amplification;
- fresh versus recurring-transform difference;
- robust/transition/null reuse regimes per dataset and scheme;
- heterogeneity of the boundary across datasets;
- heterogeneity across protection families;
- sensitivity to identity assignment and seed;
- explicit negative and failed-confirmation results.

Do not average incompatible gallery sizes without chance normalization or a hierarchical analysis.

## Phase 5: shareable architecture and results package

Create a 6-8 slide English deck plus PDF with the following content:

1. research question, threat model, and exact claim boundary;
2. architecture: image -> detection/alignment -> ArcFace -> normalization -> protection scheme/key -> multi-record set -> attacker -> gallery linkage -> metrics;
3. dataset table with identities, eligible samples, conditions, splits, and extraction success;
4. protection-scheme table with transformation family, key scope, output, source status, and configuration;
5. fresh-key result across all datasets and schemes;
6. transform-reuse/correlation result and multiplicity amplification;
7. mechanism controls, theoretical scope, limitations, and failed criteria;
8. conclusions and remaining decisions.

Presentation requirements:

- generate plots and tables from tracked compact result files, never by manual transcription;
- label independent studies separately from exact or partial reproductions;
- show chance baselines and test-gallery sizes on every linkage plot;
- distinguish exploratory, preregistered, and confirmatory runs;
- include an architecture diagram and a reproducibility appendix;
- include configuration/commit references for every headline result;
- export editable slides and a PDF;
- perform a final visual check for overflow, unreadable labels, and inconsistent numbers.

## Milestones

| Milestone | Deliverable | Exit criterion |
|---|---|---|
| G0: scope frozen | Dated dataset/scheme decision record | 2 primary datasets, 1 contingency, and 2 schemes approved |
| G1: data ready | Dataset cards, loaders, manifests, extraction summaries | Every accepted dataset passes validation and unprotected baseline |
| G2: schemes ready | Implementations, configs, tests, source classification | Two new schemes pass functional and key-scope checks |
| G3: pilot complete | Feasibility matrix and resource estimate | Valid combinations selected without using pilot as paper evidence |
| G4: confirmation complete | Frozen runs and canonical aggregate table | Required seeds/splits/metrics complete with no leakage audit failures |
| G5: interpretation reviewed | Cross-dataset/scheme analysis and theorem review | Claims match evidence and limitations are explicit |
| G6: package ready | 6-8 slides, PDF, figures, result tables, appendix | All numbers trace to configs, commits, and compact artifacts |

## Immediate next actions

1. Ask Sani to approve FEI + SCface as primaries and AgeDB as the third/contingency dataset in the [dated dataset memo](datasets/candidate_selection_2026-09-10.md).
2. FEI and SCface acquisition and their first BioHash endpoint runs are complete. Obtain authorized AgeDB access before acquisition if the third dataset is pursued; do not rerun FEI or SCface simply to regenerate figures.
3. Ask Sani to approve paper-specified IoM-GRP + PolyProtect using the [dated protection memo](protections/candidate_selection_2026-09-10.md).
4. Extract and freeze the IoM-GRP and PolyProtect parameter settings before implementation.
5. Freeze the extension protocol and estimated compute budget after dataset eligibility audits.
6. Implement one dataset and one scheme at a time; do not launch the full Cartesian product before pilots pass.
