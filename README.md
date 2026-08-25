# Key-agnostic multi-exposure biometric template leakage

This repository investigates whether a learned, key-agnostic set model can recover an identity-discriminative embedding from multiple independently protected face templates. It is research infrastructure, not a service for identifying arbitrary people.

## Current status

- A deterministic, CPU-runnable synthetic engineering pipeline is implemented: BioHash reference protection, identity/key-disjoint splits, single-template and DeepSets attackers, verification/linkage metrics, leakage checks, and traceable run artifacts.
- No published result has been reproduced yet. The requested `benchmark_cb` GitHub URL returned 404 on 2026-08-25, and MOBIO requires authorized manual access. FaceLinkGen has no verified official repository at this time.
- Synthetic smoke-test output is explicitly **engineering validation, not paper reproduction**.

## Install and run

Use an isolated environment, then install the project and existing local dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
make test
make system-info
make smoke-test
```

The smoke test trains on synthetic identities at 1/2/5/10 exposures and writes artifacts under `results/`. Main GPU work requires an authorized face dataset, a documented InsightFace checkpoint, and a reviewed protocol; start with `python scripts/train/run_multiexposure.py --config configs/attacks/proposed_synthetic.yaml` only as an engineering baseline.

## Data and models

MOBIO must be obtained from its official Idiap access route. Set `MOBIO_ROOT` and run `python scripts/data/prepare_mobio.py --root $env:MOBIO_ROOT`; the script does not download or bypass access controls. LFW may be downloaded via `python scripts/data/download_lfw.py` for engineering work only. Data and model weights are ignored by Git.

Expected scale: CPU smoke tests are small; full ArcFace/MOBIO or FaceLinkGen reproductions need disk for image data/embeddings and likely a CUDA GPU. See [MOBIO setup](docs/setup/MOBIO.md), [reproduction selection](docs/reproduction_selection.md), and [final status](reports/final_research_status.md).
