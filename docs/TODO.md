# Research completion checklist

This document separates tasks that need human authorization, licenses, hardware, or author contact from tasks that the repository can perform once those blockers are removed. Never commit biometric data, model weights, keys, tokens, credentials, or private paths to Git.

## Latest extension: 2026-09-12

- [x] Record user-reported Sani approval for paper-specified IoM-GRP and PolyProtect and freeze parameters before running.
- [x] Implement/test both schemes, key semantics and native-matching diagnostics.
- [x] Complete 16 MOBIO/FEI one-seed pilot cells (48 runs) in 277.89 seconds, below the one-hour budget.
- [x] Add paired identity intervals and exploratory equivalence sensitivity; retain identity scores privately.
- [x] Export a 633-row inventory from 25 local multi-exposure artifacts and refresh the 12-figure/eight-slide package.
- [x] Correct the theory's side-information corollary and document PolyProtect's existing multiplicity literature.
- [x] Prepare the [official access checklist](datasets/access_request_checklist.md) and [independent review checklist](review/scheme_pilot_review_2026-09-12.md).
- [x] Complete the second additional dataset: authorized SCface received and evaluated on 2026-09-18 (see update below); AgeDB remains optional.
- [ ] Approve and freeze full multi-seed confirmation; no such training was authorized in this session.
- [ ] Investigate fresh PolyProtect native protected-gallery identification; do not claim privacy from learned attacks near chance.
- [ ] Approve equivalence margins, seed uncertainty and multiplicity analysis; reconcile all historical sources with the local inventory.
- [ ] Obtain independent human theory, implementation and novelty review, plus Sani's scientific/visual approval.

## Latest extension: 2026-09-18

- [x] Receive the authorized SCface archive directly from Sani; document local setup and hashes ([docs/setup/SCFACE_LOCAL_DATA.md](setup/SCFACE_LOCAL_DATA.md)).
- [x] Add SCface loader, protocol builder, and tests (`src/biometrics_ai/data/scface.py`, `tests/unit/test_scface.py`).
- [x] Extract embeddings and validate the unprotected mugshot-to-surveillance ArcFace baseline (84.375% top-1 over 544 test probes).
- [x] Run the preregistered SCface BioHash key-pool study, frozen at `69a93e4` (pools 1/2/3 pass the all-seed clustered-interval criterion; pools 4/5/7/10 and fresh keys do not).
- [x] Run one-seed IoM-GRP/PolyProtect engineering pilots on SCface (8 cells, 24 model runs, 128.22 seconds on CPU), also frozen at `69a93e4`.
- [x] Extend the cross-dataset comparison table, figures, and eight-slide presentation to include SCface.
- [x] Refresh the September dataset report and all 20 tracked READMEs against `4352eeb`; distinguish current aggregate SCface evidence from the 633-row local inventory, which has no SCface rows.
- [ ] Obtain authorized AgeDB access if pursued as an optional third dataset.
- [ ] Approve and freeze full multi-seed confirmation across MOBIO/FEI/SCface; no such training was authorized in this session.

Historical milestones below retain their dates; current host CUDA availability must be checked separately. The new pilots ran on CPU.

## Priority 0: MOBIO dataset

- [x] A project member opens the official dataset page: <https://www.idiap.ch/en/scientific-research/data/mobio>.
- [x] Complete registration, access request, and Idiap license acceptance using an authorized academic identity.
- [x] Download MOBIO face components only from the authorized source. Do not use mirrors, shared credentials, or access-control workarounds.
- [x] Store the dataset outside this repository under `%USERPROFILE%\ResearchData\MOBIO`.
- [x] Create the local manifest from the authorized root:

```powershell
$env:MOBIO_ROOT = "$env:USERPROFILE\ResearchData\MOBIO"
python scripts\data\prepare_mobio.py --root $env:MOBIO_ROOT
```

- [x] Document the local path, exact archive list, checksums, extracted layout, and commands for Luigi in `docs/setup/MOBIO_LOCAL_DATA.md`. Do not send or commit images, video, embeddings, or manifests containing personal paths.

**Completed 2026-09-04:** access is authorized, the external structure and 118,362-file inventory are valid, `data/manifest.json` was created locally, and the reproducible handoff is documented. This is not yet a MOBIO reproduction: the exact `benchmark_cb` protocol is still required.

## Priority 1: official benchmark_cb source

- [ ] Recover the corrected official repository or contact the authors of *Benchmarking of Cancelable Biometrics for Deep Templates*.
- [ ] Request or record: official updated URL; exact commit/tag used for the paper; license; environment/dependencies; face branch ArcFace + MOBIO command/configuration; and exact known-key/unknown-key definitions.
- [ ] Do not substitute an unverified third-party fork.
- [ ] Give the technical lead the URL or an authorized source archive. Do not commit the archive.

**Done when:** the official commit is recorded in `external/manifests/upstream_sources.yaml`, the source is inspectable, and the face/MOBIO command is verified.

## Priority 2: ArcFace / InsightFace checkpoint

- [x] Choose a legally usable ArcFace-compatible checkpoint for engineering validation: official InsightFace `buffalo_l`, non-commercial research use only. This does not select the future MOBIO reproduction checkpoint.
- [x] Preserve source URL, filenames, SHA-256 hashes, model terms, training-data note, and acquisition date.
- [x] Store weights under gitignored `models/`.
- [x] Create an isolated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,face]"
```

- [x] Create an input CSV with `sample_id`, `identity_id`, `source_image`, and `split` columns.
- [x] Extract embeddings only from authorized data. The completed real-dataset commands are documented in `docs/protocols/real_datasets_month1.md`.

```powershell
python scripts\train_or_extract\extract_arcface.py `
  --input-csv path\to\samples.csv `
  --model-root models `
  --model-name antelopev2 `
  --output data\processed\embeddings\<dataset>\antelopev2
```

**Done for Month 1 engineering validation:** local manifests identify checkpoint hashes, preprocessing, and inputs for LFW, Olivetti, and CFP; all embeddings remain uncommitted. Checkpoint selection for exact MOBIO reproduction remains pending upstream recovery.

## Priority 3: real-dataset engineering fallback

- [x] While MOBIO is pending, download LFW using the documented fetcher:

```powershell
python scripts\data\download_lfw.py
```

- [x] Use LFW only to test ArcFace extraction, splits, metrics, and protected-template plumbing.
- [x] Acquire and hash-verify the public Olivetti and CFP research datasets without redistributing them.
- [x] Run deterministic identity-disjoint protocols on LFW, Olivetti, and CFP.
- [x] Label every fallback output as `engineering validation`, never as a `benchmark_cb`, MOBIO, or FaceLinkGen reproduction.

**Done:** acquisition, local manifests, protocol checks, and experiments work on all three datasets. Do not add biometric data to Git.

## Priority 4: GPU environment

- [x] Check whether the machine has a supported NVIDIA GPU:

```powershell
nvidia-smi
```

- [x] Install and validate CUDA-compatible PyTorch `2.8.0+cu128` in the isolated environment.
- [x] Verify CUDA through Python (RTX 2060 detected and used by the experiment runner):

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no CUDA device')"
python scripts\diagnostics\system_info.py
```

- [ ] Share `results/system_info.json` internally without committing it if it contains sensitive host details.

**Completed 2026-09-05:** PyTorch reports CUDA available; the MOBIO runner records `device: cuda` per trained model. Host-specific system information remains local.

## Month 1 real-dataset baseline

- [x] Confirm the proposal's Weeks 1-4 requirements from the research PDF.
- [x] Build deterministic identity-disjoint LFW, Olivetti, and CFP train/validation/test splits.
- [x] Extract and sanity-check ArcFace-compatible embeddings.
- [x] Apply one protection scheme and keep fixed-transform versus independent-key conditions separate.
- [x] Train a single-template MLP over three seeds and report cosine, normalized L2, AUROC, EER, TAR@FAR, and top-k linkage.
- [x] Test primary top-1 counts against chance and record a negative result without overstating it.
- [x] Test robustness across frontal/profile views, SCRFD/YuNet preprocessing, 60/150-identity LFW subsets, and 64/128/256-bit templates.
- [x] Cross three identity assignments, three key seeds, and three model seeds on larger LFW and CFP frontal.
- [x] Add identity-clustered bootstrap intervals and preserve cell-first descriptive summaries.
- [x] Document protocol, hashes, commands, aggregate results, limitations, and novelty implications.
- [x] Receive explicit authorization to begin the MOBIO experimentation phase (2026-09-04).
- [x] Run and analyze the preregistered exploratory MOBIO 1/2/5/10 comparison.

## Priority 5: benchmark_cb reproduction

- [ ] Run the unprotected ArcFace baseline on the exact MOBIO protocol first.
- [ ] Confirm that EER/ROC are scientifically plausible against the paper before applying protection.
- [ ] Run BioHash using the verified upstream code.
- [ ] Reproduce at least one paper privacy metric only after understanding its code and definition.
- [ ] Populate `experiments/reproduction_benchmark_cb/reproduced_results.csv` and `comparison.md` with actual values, configurations, seeds, and discrepancy explanations.
- [ ] Classify each result only as `EXACT REPRODUCTION`, `CLOSE REPRODUCTION`, `PARTIAL REPRODUCTION`, `CONCEPTUAL REPRODUCTION`, or `NOT REPRODUCIBLE YET`.
- [ ] Consider MLP-Hash and IoM-GRP only after BioHash has been validated.

**Done when:** each result traces to an upstream commit, protocol, authorized dataset, checkpoint, configuration, seed, and local artifacts.

## Priority 6: FaceLinkGen

- [ ] Search for an official repository, release, supplement, or author communication for *FaceLinkGen*.
- [ ] Before implementation, verify the PPFR method, representation shape/preprocessing, student architecture, teacher identity model, loss weights, CASIA-WebFace split, LFW/TPDNE protocol, and linkage/verification metrics.
- [ ] If official code is absent but the paper is sufficiently specified, implement a documented minimal reproduction.
- [ ] If essential details are absent, do not call the local MLP/DeepSets model a FaceLinkGen reproduction; retain it as a conceptual baseline.

**Done when:** the experiment identifies the PPFR source, teacher, student, data, splits, and evaluation protocol verifiably.

## Priority 7: proposed multi-exposure experiment

**Status (2026-09-06):** BioHash and MLP-Hash fresh-key runs, key-pool boundary replications, LFW replication, mechanism controls, same-image fresh-key control, and coarse/fine key-correlation sweeps are complete.

- [x] Create identity-disjoint train/validation/test splits on authorized MOBIO data.
- [x] Generate disjoint train/validation/test key pools.
- [x] Confirm the absence of critical identity/sample collisions and audit all 1,799 keys.
- [x] Run 1, 2, 5, and 10 independent exposures.
- [x] Keep the first run restricted to different images with different keys; defer same-image controls explicitly.
- [x] Evaluate MLP, mean/max pooling, and DeepSets baselines.
- [x] Report cosine similarity, normalized L2, AUROC, EER, TAR@FAR, top-1/top-5, and unseen-key results.
- [x] Run three model seeds and report mean, standard deviation, and identity-clustered intervals.
- [x] Use unseen identities plus unseen keys as the primary condition.
- [x] Confirm the fresh-key null with paper-specified MLP-Hash and new key/set/model seeds.
- [x] Run the preregistered system-key-pool boundary and its sample-randomized confirmation.
- [x] Confirm with new protocol seeds (three partitions on the 3-9 sweep), MLP-Hash pools 1-5 and 10, and a Haar sign-corrected variant.
- [x] Report the LFW second-dataset key-pool run (`experiments/lfw_multiexposure/`).
- [x] Add a shuffled-non-anchor control; all 10-record conditions collapsed to exact chance.
- [x] Add a corrected key-aware (slot-label-known) DeepSets attacker paired with a hidden-slot baseline.
- [x] Add a paired same-image/different-fresh-key control.
- [x] Add coarse and independent-partition fine key-correlation controls.
- [ ] Add the non-normalized/norm-leakage control.
- [ ] Recheck the novelty claim against IEEE Xplore and Google Scholar before submission.

**Done when:** 1/2/5/10 exposure plots and tables are reproducible from configuration, seed, code, and protocol with no identity, key, or metadata leakage.

## Priority 8: post-meeting generalization and presentation package

**Requested by Sani on 2026-09-10.** The complete execution plan and gates are in [ROADMAP.md](ROADMAP.md).

### Freeze scope

- [x] Complete an official-source desk review and propose two primary facial-biometric datasets plus one contingency dataset. The quality/access review selects FEI + SCface as primaries and AgeDB as the third candidate; see [datasets/candidate_selection_2026-09-10.md](datasets/candidate_selection_2026-09-10.md).
- [x] Record official sources, current access paths, published counts, variation, stated terms, acquisition size where published, expected pilot cost, and model-overlap risks for the candidate set.
- [ ] Ask Sani to approve FEI and SCface as primary datasets and AgeDB as the contingency/third dataset.
- [x] Download the four official FEI original-image archives, hash them, and audit ArcFace-valid counts without committing data (2026-09-12: 2,800 images, 200 identities, 2,378/2,400 protocol embeddings, all identities >= 11 valid).
- [ ] Request the AgeDB archive password from the official maintainer using an academic email address.
- [ ] Ask Sani or another full-time staff member to submit the SCface institutional letter and signed release agreement.
- [ ] If QMUL-SurvFace is activated as a later scale test, clarify collaborator sharing, derived-data, and aggregate-publication terms with the official contact first.
- [ ] Confirm that each selected dataset supports at least ten valid records per identity and identity-disjoint splits.
- [x] Review IoM-GRP, PolyProtect, SWG-MinHash, Bloom Filters, IoM-URP, IronMask, SecureTL, and SecureVector for paper, source, license, implementation, and protocol fit. See [protections/candidate_selection_2026-09-10.md](protections/candidate_selection_2026-09-10.md).
- [x] Propose paper-specified IoM-GRP and PolyProtect as two additional schemes with distinct categorical-ranking and polynomial transformation families.
- [x] Extract and freeze primary IoM-GRP and PolyProtect parameters from their papers before implementation (pilot freeze `d5f4e89`).
- [ ] Obtain Sani's approval of the dataset/scheme decision record before full experiments.

### Implement datasets

- [x] Add acquisition documentation and a non-sensitive dataset card for dataset A (FEI: `experiments/fei_multiexposure/README.md`).
- [x] Add deterministic loader, validation, split construction, and tests for dataset A (`src/biometrics_ai/data/fei.py`, `tests/unit/test_fei.py`).
- [x] Extract embeddings and validate the unprotected ArcFace baseline for dataset A (oracle `100%`).
- [x] Run the preregistered FEI BioHash key-pool study (tested pools 1/2/3/4/5/7 pass; pool 10 fails; fresh results are chance-compatible).
- [x] Add acquisition documentation and a non-sensitive dataset card for dataset B (SCface: `docs/setup/SCFACE_LOCAL_DATA.md`, `experiments/scface_multiexposure/README.md`).
- [x] Add deterministic loader, validation, split construction, and tests for dataset B (`src/biometrics_ai/data/scface.py`, `tests/unit/test_scface.py`).
- [x] Extract embeddings and validate the unprotected ArcFace baseline for dataset B (mugshot-to-surveillance oracle 84.375% top-1 over 544 test probes).
- [x] Run the preregistered SCface BioHash key-pool study (tested pools 1/2/3 pass; pools 4/5/7/10 fail; fresh results are chance-compatible).
- [ ] Repeat the dataset tasks for contingency dataset C only if approved and feasible.

### Implement protection schemes

- [x] Record primary sources, paper parameters and paper-specified classification for IoM-GRP and PolyProtect.
- [x] Implement both schemes with determinism, key-scope, shape, range and nondegeneracy checks.
- [x] Run existing unprotected calibration and new shared/reused/fresh pilot diagnostics on MOBIO/FEI/SCface.
- [ ] Complete category-occupancy/entropy and parameter-sensitivity audits before confirmation.

### Run evidence matrix

- [ ] Run the Stage A one-seed pilot over each new dataset/scheme combination; label it engineering diagnostics.
- [ ] Exclude or repair combinations whose positive controls, extraction, or leakage audits fail.
- [ ] Freeze the confirmatory protocol before inspecting Stage B results.
- [ ] Run 1/2/5/10 exposures with fresh and recurring transforms over at least three model seeds.
- [ ] Add multiple identity assignments where dataset size permits.
- [ ] Complete the non-normalized/norm-leakage control.
- [ ] Add equivalence analysis for fresh-key results.
- [ ] Produce the canonical cross-dataset/cross-scheme aggregate table and failure analysis.

### Prepare material for Sani and the paper

- [x] Create and review the end-to-end architecture diagram (`reports/figures/fig_architecture.pdf`, `fig_threat_model.pdf`).
- [x] Generate current dataset and protection-scheme comparison tables in the review deck; proposed extensions remain pending.
- [x] Generate fresh-key, reuse-boundary, amplification, and correlation figures from tracked results (`scripts/figures/make_figures.py`).
- [x] Produce the earlier 73-condition/12-study table, 72 new-scheme pilot rows, and a 633-row local per-seed inventory. Full historical reconciliation remains pending.
- [x] Prepare an eight-slide English review deck and matching PDF (`reports/slides/research_review.pptx`, `reports/slides/research_review.pdf`).
- [x] Include threat model, methods, controls, theoretical scope, limitations, and reproduction status.
- [x] Check diagram/plot text bounds, box padding, overlaps, and unsupported dashes; validate editable slide content and rendered PDF pages.
- [ ] Verify every headline number against a configuration, commit, and compact result artifact.
- [ ] Perform a final visual and scientific review with Gigi, Manish, and Sani.

**Done when:** two additional datasets and two additional schemes have passed the confirmatory protocol, the optional third dataset has an explicit use/defer decision, and the reviewed slide/results package traces every claim to reproducible evidence.

## Git checks before every commit

- [ ] Confirm data, weights, and secrets are ignored:

```powershell
git check-ignore -v data\raw\anything.jpg
git check-ignore -v models\arcface.onnx
git status
git diff --cached --stat
```

- [ ] Commit only code, configurations, documentation, synthetic fixtures, and small non-sensitive summaries.
- [ ] Never commit `data/raw`, `data/interim`, `data/processed`, `models`, `.env`, embeddings, protected templates, or biometric-sensitive results.

## Local commands already working

```powershell
python -m pytest
python scripts\diagnostics\system_info.py
python scripts\reproduce\run_smoke_test.py
python scripts\setup\download_buffalo_l.py --verify-only
python scripts\setup\download_yunet.py --verify-only
python scripts\diagnostics\check_leakage.py --manifest data\interim\lfw_month1_protocol.csv
python scripts\train\run_lfw_month1.py --config configs\attacks\month1_lfw.yaml
python scripts\train\run_lfw_month1.py --config configs\attacks\month1_cfp.yaml
python scripts\train\run_lfw_month1.py --config configs\attacks\month1_olivetti.yaml
python scripts\train\run_month1_dimension_sweep.py --base-config configs\attacks\month1_lfw_yunet.yaml --output-root results\month1_sweeps\lfw_yunet
python scripts\train\run_month1_seed_robustness.py --config configs\attacks\month1_seed_robustness.yaml
```

Synthetic runs are pipeline tests only. LFW, Olivetti, and CFP results are engineering validation, not published reproductions, and support only the documented single-template conclusion.
