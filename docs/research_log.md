# Research log

## 2026-08-25

- Task: initialized reproducible research repository from the master prompt.
- Sources checked: arXiv records for benchmark_cb and FaceLinkGen; official GaFaR, Arc2Face, MOBIO pages; official InsightFace repository.
- Commands: `git ls-remote` against official repositories; local environment inspection; synthetic tests pending.
- Result: GaFaR, InsightFace, Arc2Face commits resolved. The stated `https://github.com/otroshi/benchmark_cb` URL returned 404. No verified FaceLinkGen code release was found from the arXiv record.
- Decision: implement a labelled local engineering baseline while preserving exact reproduction as blocked by upstream/MOBIO access.
- Next: run unit/integration tests and synthetic smoke test; recover/confirm benchmark_cb source with authors before claiming a reproduction.

## 2026-08-25 (verification)

- Task: verified local implementation and staged synthetic pipeline.
- Commands: `python -m pytest`; `python scripts/diagnostics/system_info.py`; `python scripts/reproduce/run_smoke_test.py`.
- Result: five tests passed. CPU-only environment (PyTorch 2.11.0; CUDA unavailable to PyTorch). Synthetic 1/2/5/10 runs completed and artifacts were written under `results/`.
- Interpretation: no stable multi-exposure gain was observed in one small synthetic seed. This is expectedly weak engineering evidence and is not a real-data result or a test of the research hypothesis.
- Next: obtain authorized MOBIO and a corrected official benchmark_cb source; verify the FaceLinkGen PDF protocol before reproduction work.

## 2026-08-26 (Month 1 LFW fallback)

- Task: followed the proposal's Month 1 plan on LFW while MOBIO authorization remains pending: ArcFace plus BioHash, identity-disjoint splits, a single-template MLP, metrics, and first leakage results.
- Source audit: the official arXiv TeX still points to `https://github.com/otroshi/benchmark_cb`; `git ls-remote` returned 404, the repository is absent from the author's eight public repositories, and author/Idiap code searches found no replacement. Paper face targets were transcribed from Tables I, II, and IV.
- Data/model: downloaded funneled LFW through scikit-learn and selected 60 identities with 6 images each using seed `20260826`; acquired official InsightFace `buffalo_l` under its non-commercial research terms and verified archive, recognition-model, and detector SHA-256 hashes.
- Extraction: OpenCV SCRFD plus ArcFace produced 359/360 finite, unit-normalized 512-D embeddings. One test image had no detected face. Repeat extraction was exact; mean same-identity cosine was `0.628` versus `0.0056` for sampled different identities.
- Protocol: 36/12/12 identity-disjoint train/validation/test identities, 12 test gallery identities, and 59 probes. The leakage checker passed for all 360 planned rows. The primary condition used one independent key per image with disjoint split key pools.
- Result: unprotected top-1 `98.31%`, EER `0.85%`. The three-seed fixed-transform MLP reached top-1 `53.11% +/- 2.59%`. The independent unseen-key MLP reached top-1 `9.60% +/- 0.98%`, AUROC `0.5139 +/- 0.0188`, and EER `49.13% +/- 3.40%` against top-1 chance `8.33%`.
- Statistical check: independent-key top-1 counts were 5/59, 6/59, and 6/59; one-sided exact binomial `p` values were `0.552`, `0.369`, and `0.369`. No useful single-template identity recovery was detected in the primary condition.
- Validation: eight tests passed; `pip check` found no broken requirements; model hashes matched; rerunning seed 7 in both conditions reproduced every scientific metric exactly (`max difference = 0.0`).
- Environment: Windows 11 build 26200, Python 3.13.5, PyTorch 2.8.0 CPU. PyTorch 2.9+ was avoided on Windows due the open upstream `c10.dll` loader regression (`pytorch/pytorch#166628`). ONNX Runtime also failed native initialization on this host, motivating the validated OpenCV backend.
- Interpretation: this is engineering validation, not a `benchmark_cb` or FaceLinkGen reproduction. The negative single-template result establishes the weak baseline needed for the proposed novelty but does not test the 2/5/10-exposure hypothesis.
- Next: implement real-embedding set construction and compare 1/2/5/10 exposures with multiple protocol seeds; continue waiting for MOBIO approval and request the missing official benchmark source from the authors.

## 2026-08-26 (Month 1 cross-dataset continuation)

- Task: followed the instruction to continue Month 1 on other real datasets without starting the 2/5/10-exposure experiment. Synthetic data was excluded from scientific evidence.
- Data: acquired and hash-verified Olivetti faces (40 identities, 400 images) and CFP (500 identities, 5,000 frontal plus 2,000 profile images). CFP's official archive contains no explicit license file, so no dataset files are redistributed. MOBIO remains blocked pending authorized access.
- Detector decision: the existing SCRFD checkpoint failed dataset-suitability probes on Olivetti and CFP. Added hash-pinned OpenCV Zoo YuNet five-landmark detection rather than lowering thresholds or guessing CFP landmark mappings. YuNet extracted 400/400 Olivetti, 4,999/5,000 CFP frontal, 1,983/2,000 CFP profile, and 360/360 LFW-small embeddings.
- Protocols: deterministic seed `20260826`, identity-disjoint 60/20/20 splits, one gallery image per test identity, and all remaining test images as probes. Leakage checks passed. A larger LFW protocol added 150 identities x 10 images, 1,500/1,500 successful extractions, 30 gallery identities, and 270 probes.
- Result: independent unseen-key top-1 stayed at chance on all six variants: LFW SCRFD `9.60%` vs `8.33%`, LFW YuNet `6.67%` vs `8.33%`, larger LFW `3.83%` vs `3.33%`, Olivetti `11.57%` vs `12.50%`, CFP frontal `1.15%` vs `1.00%`, and CFP profile `1.02%` vs `1.00%`. AUROC remained near `0.5` and EER near `50%`.
- Statistical check: per-seed top-1 exact binomial tests were descriptive because probes share identities; no seed rejected chance (`p >= 0.1205`).
- Positive control: fixed-transform MLP top-1 ranged from `51.11%` to `91.00%`, showing that the pipeline recovers identity signal when the transform is reusable.
- Ablation: independent-key 64/128/256-bit results remained at chance on LFW and Olivetti. The larger LFW result also removed the original 59-probe small-sample concern without changing the conclusion.
- Interpretation: convergent evidence across three real datasets, pose, detector, sample size, and template dimension supports a robust negative single-template baseline. It does not establish universal irreversibility and does not test the proposed multi-exposure novelty.
- Validation: 11 tests passed; `pip check`, Python compilation, YAML/CSV/link parsing, model/dataset hash verification, five protocol leakage audits, aggregate-to-detail comparisons, `git diff --check`, and editor diagnostics passed. GNU Make is unavailable on this Windows host, so target wiring was validated directly and the underlying Python commands were run.
- Decision: Month 1 is complete. Keep Month 2 paused until explicit approval; continue waiting for MOBIO authorization and the corrected official `benchmark_cb` source.
