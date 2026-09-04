# MOBIO single-template baseline

Classification: **independent engineering validation, not a `benchmark_cb` reproduction**.

The authorized local MOBIO selected-still bundle contains 28,800 images from all 150 identities (192 per identity). The initial bounded protocol selects one image from each of 12 sessions per identity with seed `20260904`, then assigns identities to 90 train / 30 validation / 30 test. YuNet plus the hash-pinned `buffalo_l` ArcFace recognition model extracted 1,799 of 1,800 embeddings; `m120_07_p03_i0_0` had no detected face.

The 30-identity test split has 30 gallery images and 330 probes. Unprotected ArcFace achieved `100%` top-1, AUROC `1.0`, and EER `0%`, establishing a strong source representation. With one shared BioHash key, the learned inverse reached `81.21% +/- 3.19%` top-1 over three model seeds. With one independent unseen key per sample, it reached `3.33% +/- 0.30%` top-1 against `3.33%` chance, AUROC `0.4992`, and EER `50.28%`.

This extends the prior LFW/Olivetti/CFP negative single-template result to MOBIO under identity-disjoint evaluation. It does not establish irreversibility. The subsequent preregistered 1/2/5/10 experiment is documented under `experiments/mobio_multiexposure/`.

Local outputs are under `results/month1_mobio/` and remain Git-ignored. Run with:

```powershell
.\.venv\Scripts\python.exe scripts\train\run_lfw_month1.py `
  --config configs\attacks\month1_mobio.yaml
```
