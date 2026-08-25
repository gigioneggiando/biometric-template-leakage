# Research completion checklist

This document separates tasks that need human authorization, licenses, hardware, or author contact from tasks that the repository can perform once those blockers are removed. Never commit biometric data, model weights, keys, tokens, credentials, or private paths to Git.

## Priority 0: MOBIO dataset

- [ ] A project member opens the official dataset page: <https://www.idiap.ch/en/scientific-research/data/mobio>.
- [ ] Complete registration, access request, and Idiap license acceptance using an authorized academic identity.
- [ ] Download MOBIO only from the authorized source. Do not use mirrors, shared credentials, or access-control workarounds.
- [ ] Store the dataset outside this repository, for example `D:\ResearchData\MOBIO`.
- [ ] Create the local manifest from the authorized root:

```powershell
$env:MOBIO_ROOT = "D:\ResearchData\MOBIO"
python scripts\data\prepare_mobio.py --root $env:MOBIO_ROOT
```

- [ ] Share the local path and any command error with the technical lead. Do not send or commit images, video, embeddings, or manifests containing personal paths.

**Done when:** access is authorized, the local structure is valid, and `data/manifest.json` is created locally. This is not yet a MOBIO reproduction: the exact `benchmark_cb` protocol is still required.

## Priority 1: official benchmark_cb source

- [ ] Recover the corrected official repository or contact the authors of *Benchmarking of Cancelable Biometrics for Deep Templates*.
- [ ] Request or record: official updated URL; exact commit/tag used for the paper; license; environment/dependencies; face branch ArcFace + MOBIO command/configuration; and exact known-key/unknown-key definitions.
- [ ] Do not substitute an unverified third-party fork.
- [ ] Give the technical lead the URL or an authorized source archive. Do not commit the archive.

**Done when:** the official commit is recorded in `external/manifests/upstream_sources.yaml`, the source is inspectable, and the face/MOBIO command is verified.

## Priority 2: ArcFace / InsightFace checkpoint

- [ ] Choose a legally usable ArcFace-compatible checkpoint. The initial candidate is an InsightFace/`antelopev2` setup, but model-weight and training-data terms must be reviewed separately from code licensing.
- [ ] Preserve: source URL, filename, SHA-256, license, training-data notes, and acquisition date.
- [ ] Store weights under `models/` or a controlled local archive. `models/` is ignored by Git.
- [ ] Create an isolated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,face]"
```

- [ ] Create an input CSV with `sample_id`, `identity_id`, `source_image`, and `split` columns.
- [ ] Extract embeddings only from authorized data:

```powershell
python scripts\train_or_extract\extract_arcface.py `
  --input-csv path\to\samples.csv `
  --model-root models `
  --model-name antelopev2 `
  --output data\processed\embeddings\<dataset>\antelopev2
```

**Done when:** local manifests reproducibly identify checkpoint, preprocessing, and inputs; embeddings are not committed.

## Priority 3: LFW engineering fallback

- [ ] If MOBIO is still pending, download LFW using the documented fetcher:

```powershell
python scripts\data\download_lfw.py
```

- [ ] Use LFW only to test ArcFace extraction, splits, metrics, and protected-template plumbing.
- [ ] Label every LFW output as `engineering validation`, never as a `benchmark_cb` or MOBIO reproduction.

**Done when:** acquisition and the local manifest work. Do not add LFW data to Git.

## Priority 4: GPU environment

- [ ] Check whether the machine has a supported NVIDIA GPU:

```powershell
nvidia-smi
```

- [ ] Create a separate environment with a CUDA-compatible PyTorch build selected from the official PyTorch site. Do not replace the working CPU environment until GPU validation succeeds.
- [ ] Verify CUDA through Python:

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no CUDA device')"
python scripts\diagnostics\system_info.py
```

- [ ] Share `results/system_info.json` internally without committing it if it contains sensitive host details.

**Done when:** PyTorch reports CUDA available and records GPU model/VRAM. CPU is sufficient for smoke tests but not extended reproductions.

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

- [ ] Create identity-disjoint train/validation/test splits on authorized data.
- [ ] Generate disjoint train/validation/test key pools.
- [ ] Confirm the absence of critical collisions with `scripts/diagnostics/check_leakage.py`.
- [ ] Run 1, 2, 5, and 10 independent exposures.
- [ ] Keep separate: same image with different keys, and different images of the same identity with different keys.
- [ ] Evaluate linear/MLP, mean/max pooling, and DeepSets first; add attention/Set Transformer only after baseline validation.
- [ ] Report cosine similarity, normalized L2, AUROC, EER, TAR@FAR, top-1/top-5, and seen-key versus unseen-key results.
- [ ] Run multiple seeds and report mean, standard deviation, and confidence/bootstrap intervals.
- [ ] Do not use seen identities or seen keys as evidence of generalization. The primary condition is unseen identities plus unseen keys.

**Done when:** 1/2/5/10 exposure plots and tables are reproducible from configuration, seed, code, and protocol with no identity, key, or metadata leakage.

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
```

Smoke-test results are synthetic engineering validation, not a published reproduction or a conclusion about biometric leakage.
