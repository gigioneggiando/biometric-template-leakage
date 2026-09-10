# Candidate face-dataset selection

**Decision date:** 2026-09-10  
**Status:** official-source desk review complete; selection proposed, not yet approved  
**Scope:** two primary datasets and one contingency dataset for the post-meeting multi-exposure generalization study

## Recommendation

| Role | Dataset | Why it adds evidence | Gate before use |
|---|---|---|---|
| Primary A | FEI | High-resolution, balanced, controlled images with exactly 14 pose/expression records for each of 200 identities; official downloads are active | Download the four official archives; verify hashes, filenames, and at least 10 ArcFace-valid images per identity |
| Primary B | SCface | Guaranteed repeated captures under different surveillance cameras, distances, illumination, pose, and visible/IR conditions | Sani or another full-time staff member must submit the institutional request and sign the release agreement |
| Third dataset / contingency | AgeDB | In-the-wild longitudinal age variation | Obtain the password; count identities with at least 10 usable images; audit possible celebrity overlap with the ArcFace training population |
| Deferred large-scale option | QMUL-SurvFace | Native low-resolution surveillance faces at substantially larger scale | Use only if a later scale test is needed and its provenance, terms, duplicates, and ArcFace positive control pass |

This combination is recommended because it starts with a small, high-resolution, immediately obtainable dataset, adds a rigorously documented surveillance dataset, and retains longitudinal age as a different third stressor. It should not be replaced by three similar celebrity datasets merely to increase the dataset count.

Approval of this shortlist does not approve a paper claim. Each dataset must still pass the repository's dataset gate and unprotected ArcFace positive control.

## Required protocol fit

The existing multi-exposure experiment needs:

- stable identity labels;
- at least 10 independently selected, usable records for every retained identity;
- enough retained identities for identity-disjoint train, validation, and test partitions;
- a deterministic record-selection rule fixed before protected-template results are inspected;
- lawful research access without redistributing images, embeddings, or sensitive manifests;
- acceptable face-detection and ArcFace identification performance before protection is applied.

The protocol should initially select exactly 12 records per identity, matching the LFW extension, when the source data permit it. Ten records feed the maximum-exposure set and the remaining records support gallery or reserve construction. Dataset-specific alternatives must be written into a preregistered protocol rather than decided after inspecting attack results.

## Candidate A: FEI

**Official source:** [Centro Universitario FEI face database](https://fei.edu.br/~cet/facedatabase.html).

### Verified facts

- 2,800 colour images of 200 identities, exactly 14 images per identity.
- Original resolution is 640 x 480 pixels, with a homogeneous white background, about 10% scale variation, and pose rotation covering approximately 180 degrees.
- The population comprises FEI students and staff aged 19 to 40, with exactly 100 male and 100 female subjects as described by the source.
- Four official original-image ZIP archives are currently linked, totalling approximately 344 MB.
- Use is granted for research purposes; redistribution or reproduction of the database is not permitted.

### Scientific role

FEI is the best first implementation target. It is small enough for rapid auditing, guarantees more than 10 raw records per identity, has clear labels and controlled high-resolution acquisition, and supports a 120/40/40 identity split with 2.5% test-gallery chance. Its pose sweep tests whether the leakage boundary depends on pose while avoiding Internet-celebrity provenance.

### Unresolved checks

- Extreme profiles may fail face detection. Confirm that enough identities retain at least 10 valid ArcFace embeddings before freezing the split.
- The images appear to be from one acquisition protocol rather than longitudinal sessions. Treat FEI as a controlled pose/expression test, not a session-generalization dataset.
- Exact archive hashes are not published on the page and must be calculated locally after download.
- No identity-level audit against WebFace600K is possible. Institutional volunteers make overlap less likely than celebrity datasets, but absence is not proven.

### Acquisition action

Download the four `originalimages_part*.zip` archives only from the official FEI page, store them outside Git, calculate SHA-256 hashes, and retain the official research-use notice. Do not use the two-image aligned frontal subset because it cannot support the 10-record protocol.

## Candidate B: SCface

**Official sources:** [University of Zagreb SCface page](https://www.scface.org/) and [release agreement](https://www.scface.org/SCface_release_agreement.pdf).

### Verified facts

- 4,160 static visible and infrared images of 130 subjects.
- Every subject has 32 images: 21 surveillance images from seven camera modes at three distances, nine controlled pose images, one visible mugshot, and one infrared mugshot.
- The source documents uncontrolled illumination, multiple camera qualities, distances of 1.00, 2.60, and 4.20 metres, and nine poses.
- Access is free but case-by-case. The request requires a cover letter on institutional letterhead and a signed release agreement.
- The agreement must be signed by a full-time staff member; a student signature is explicitly not accepted.
- The agreement forbids redistribution. Only images of subject IDs 001, 002, 045, and 102 may appear in publications without additional approval.
- The documented population is 115 male and 15 female subjects, all described by the source as Caucasian, aged 20 to 75. This limitation must be reported.

### Scientific role

SCface provides a clean multi-exposure design in which every identity exceeds the raw 10-record requirement. Its camera, distance, pose, visible/IR, and resolution variation allows a controlled explanation of where ArcFace extraction or template-linkage performance changes.

### Unresolved checks

- Confirm that the granted agreement permits processing by every named collaborator and on the intended university/personal machines. The agreement restricts dissemination even within an organization.
- Predefine whether the primary protocol uses only the 21 surveillance images or mixes surveillance, pose, and mugshot conditions.
- Verify detector success, particularly for distant and infrared images, before fixing the eligible identity set.
- No identity-level overlap audit with WebFace600K is available. The source population is institutional volunteers rather than Internet celebrities, which lowers the expected risk, but this is an inference rather than verified absence.

### Acquisition action

Ask Sani to prepare the institutional cover letter, review and sign the official agreement, and submit both documents to the official contact. The team must store the approval and data privately and follow the image-publication restriction when preparing slides.

## Candidate C: AgeDB

**Official sources:** [Imperial College iBUG dataset page](https://ibug.doc.ic.ac.uk/resources/agedb/) and [CVPR Workshops paper](https://openaccess.thecvf.com/content_cvpr_2017_workshops/w33/html/Moschoglou_AgeDB_The_First_CVPR_2017_paper.html).

### Verified facts

- 16,488 images of 568 identities, with identity, age, and gender annotations.
- The images are of public figures collected from the Internet and span large age differences.
- The dataset is restricted to non-commercial research.
- The official page prohibits publication or redistribution of the annotations and derived data, except internal copies at one site in the same organization.
- The archive link is present, but its password must be requested by email from the address on the official page.

### Scientific role

AgeDB tests whether the fresh-key null and recurring-transform leakage survive age-related appearance changes. This variation is not isolated by the current MOBIO and LFW experiments.

### Unresolved checks

- The publication reports about 29 images per identity on average, but an average does not establish how many identities have at least 10 usable images. Compute the exact distribution after authorized acquisition.
- `buffalo_l` uses a ResNet-50 trained on WebFace600K and its official model card reports AgeDB-30 benchmark accuracy. An identity-level training-overlap audit is not currently available. Treat possible celebrity overlap as a limitation and do not describe AgeDB as training-independent.
- Record whether the downloaded archive contains the full identity annotations needed for the proposed identity-disjoint split.
- Estimate extracted size, detector failure rate, and runtime from a small authorized pilot.

### Acquisition action

One project member should email the AgeDB maintainer from an academic address, state the university affiliation and non-commercial research purpose, request the archive password, and retain the response privately. Do not commit the password, archive, annotations, images, embeddings, or a manifest containing personal paths.

## Deferred large-scale option: QMUL-SurvFace

**Official source:** [Queen Mary University of London project page](https://qmul-survface.github.io/).

### Verified facts

- 463,507 face images of 15,573 identities from real, uncooperative surveillance scenes.
- The images are natively low resolution rather than artificially downsampled.
- The official page currently provides dataset and evaluation-code links and lists the package as 389 MB.
- It is made available for research purposes. The images were collected from existing person re-identification datasets, and copyright remains with the original owners.

### Scientific role

QMUL-SurvFace is a useful third dataset if a pilot shows that low-resolution crops retain enough unprotected identity signal. It adds scale and a difficult surveillance domain beyond the smaller controlled SCface dataset.

### Unresolved checks

- The mean is about 29.8 images per identity, but the official summary does not state the full per-identity distribution. Count identities with at least 10 valid records.
- Determine whether multiple images are adjacent or near-duplicate video frames. The 10 exposures must not be a trivial burst of the same frame.
- Audit the original re-identification dataset identifiers and terms. The project page's research notice is not evidence that images can be redistributed or shown in slides.
- Run a small extraction pilot. If the unprotected ArcFace control is weak, the dataset cannot support conclusions about the protection schemes under the current architecture.
- Process only an identity-balanced subset for the first pilot; embedding all 463,507 images is unnecessary before feasibility is established.

### Acquisition action

Before downloading, send the official contact a short clarification covering research use, local sharing among the named university collaborators, derived embeddings, and publication of aggregate results. After clarification, download only from an official link and hash the archive locally.

## Alternatives reviewed

| Dataset | Decision | Reason |
|---|---|---|
| CMU Multi-PIE | Defer | Excellent pose, illumination, expression, and session coverage, but the official site reports more than 305 GB and its acquisition link currently redirects to a generic Wellspring search page. Request a current official route before reconsidering it. |
| CelebA | Backup only | The official source provides 202,599 images and 10,177 identities, but identity labels are released on request and the exact >=10 distribution must be checked. Internet-celebrity identities create a material overlap risk with WebFace600K. |
| IJB-B / IJB-C | Reject for new acquisition | NIST states that distribution of IJB-A, IJB-B, and IJB-C ended on 2023-03-14. Use only if the university already has an authorized copy and its agreement covers this project. |
| VGGFace2 | Reject for new acquisition | The official Oxford page states that its download links are no longer available. Do not use unofficial mirrors. |
| CALFW / CPLFW | Reject as independent confirmation | Both derive from LFW and therefore do not supply an independent dataset population. |
| CASIA-WebFace | Defer | It is primarily a face-model training corpus; official access, provenance, current terms, and overlap with the selected recognition model require a separate audit. |

## Engineering triage

Scores are planning estimates, not experimental results. `3` is favourable and `0` is blocking.

| Candidate | >=10 protocol fit | Complementary variation | Current access path | RTX 2060 pilot feasibility | Model-overlap confidence | Total / 15 |
|---|---:|---:|---:|---:|---:|---:|
| FEI | 3 | 2 | 3 | 3 | 2 | 13 |
| SCface | 3 | 3 | 2 | 3 | 2 | 13 |
| AgeDB | 2 | 3 | 2 | 3 | 1 | 11 |
| QMUL-SurvFace | 2 | 3 | 1 | 2 | 2 | 10 |
| CelebA | 2 | 2 | 2 | 2 | 0 | 8 |
| CMU Multi-PIE | 3 | 3 | 0 | 0 | 2 | 8 |
| VGGFace2 | 3 | 3 | 0 | 0 | 0 | 6 |
| IJB-C | 3 | 3 | 0 | 1 | 2 | 9 |

`Model-overlap confidence` measures confidence that overlap can be avoided or clearly characterized, not proof of no overlap. A zero access score is sufficient to prevent selection regardless of the numerical total.

## Approval proposal for Sani

Request approval for:

1. **FEI and SCface as the two primary datasets**, conditional on the ArcFace eligibility audit and SCface approval.
2. **AgeDB as the third dataset/contingency**, conditional on access, eligible-identity counts, and explicit reporting of possible model overlap.
3. **QMUL-SurvFace only as a later large-scale stress test**, not as a primary quality-controlled dataset.
4. Excluding IJB-C and VGGFace2 because no current official distribution is available.

## Actions after approval

1. Download and audit FEI from the active official links.
2. Submit the SCface institutional request and AgeDB email in parallel.
3. Store each authorized dataset outside Git and record archive hashes locally.
4. Implement metadata-only audit scripts before extracting all embeddings.
5. Record identity counts at thresholds 1, 2, 5, 10, and 12; duplicate statistics; and capture-condition coverage.
6. Freeze identity partitions, record selection, and seeds before protected-template runs.
7. Run detection/extraction and the unprotected ArcFace control on a small pilot.
8. Advance only datasets whose positive controls work and whose license and split audits pass.

## Sources and retrieval date

All sources were checked on 2026-09-10:

- AgeDB: <https://ibug.doc.ic.ac.uk/resources/agedb/>
- AgeDB paper: <https://openaccess.thecvf.com/content_cvpr_2017_workshops/w33/html/Moschoglou_AgeDB_The_First_CVPR_2017_paper.html>
- SCface: <https://www.scface.org/>
- SCface agreement: <https://www.scface.org/SCface_release_agreement.pdf>
- FEI: <https://fei.edu.br/~cet/facedatabase.html>
- QMUL-SurvFace: <https://qmul-survface.github.io/>
- CMU Multi-PIE: <https://www.cs.cmu.edu/afs/cs/project/PIE/MultiPie/Multi-Pie/Home.html>
- CelebA: <https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html>
- IJB-C distribution status: <https://www.nist.gov/itl/tted/btg/ijb-c-dataset-request-form>
- VGGFace2: <https://www.robots.ox.ac.uk/~vgg/data/vgg_face2/>
- InsightFace model pack and training-data label: <https://github.com/deepinsight/insightface/blob/master/python-package/README.md>
