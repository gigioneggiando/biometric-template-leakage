# Model weights

Weights are intentionally ignored. InsightFace code is MIT licensed, but each checkpoint's training-data and redistribution terms must be independently checked. Arc2Face is optional; its official implementation and model download instructions are documented in `docs/literature/paper_notes/facelinkgen.md`.

The Month 1 real-dataset studies use the official InsightFace `buffalo_l` release asset (`ResNet50@WebFace600K`). InsightFace states that its provided pretrained models are available for non-commercial research only. Review those terms before running:

```powershell
python scripts\setup\download_buffalo_l.py --accept-research-only-license
```

The script verifies archive SHA-256 `80ffe37d8a5940d59a7384c201a2a38d4741f2f3c51eef46ebb28218a7b0ca2f`, detector SHA-256 `5838f7fe053675b1c7a08b633df49e7af5495cee0493c7dcf6697200b85b5b91`, and recognition-model SHA-256 `4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43`. These files are not redistributed by this repository.

Olivetti and CFP require the Apache-2.0 OpenCV Zoo YuNet detector because the bundled SCRFD checkpoint was unsuitable in dataset probes. Acquire and verify it with:

```powershell
python scripts\setup\download_yunet.py
```

YuNet model SHA-256 is `8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4`. The same model was used for the LFW preprocessing robustness checks.
