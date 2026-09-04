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

## 2026-08-26 (Month 1 robustness strengthening)

- Task: strengthen the real-data single-template conclusion without starting Month 2 or using synthetic evidence.
- Design: crossed three deterministic identity assignments (`20260826-20260828`), three stable `sample_id`-scoped key seeds (`20260826-20260828`), and three model seeds (`7/17/27`) on larger LFW and CFP frontal. Stable sample-ID keys keep identity assignment and key randomness as separate factors; every run retained unique, split-disjoint keys.
- Statistics: summarized model runs within each split/key cell before study-level ranges. Added deterministic 2,000-resample identity-clustered percentile intervals for top-1, retaining all probes from each sampled identity.
- Result: independent-key cell means were `2.59-3.58%` on larger LFW versus `3.33%` chance and `0.81-1.11%` on CFP frontal versus `1.00%` chance. All 54 independent-key run-level clustered intervals included chance. Fixed-transform cell means remained `66.54-77.41%` and `91.70-94.74%`, respectively.
- Interpretation: the negative single-template result is robust to the tested identity assignment, key randomness, and optimizer randomness. Cells share fixed datasets, so this is descriptive sensitivity evidence, not 27 independent replications per condition, an equivalence test, or proof of irreversibility. Run-level interval checks were not multiplicity-adjusted.
- Artifacts: detailed 108-run outputs remain gitignored; four study summaries and all 36 split/key cell aggregates are tracked under `experiments/month1_real_datasets/`.
- Validation: 15 tests passed; dependencies, Python compilation, YAML/CSV/link parsing, editor diagnostics, detailed-to-tracked aggregate equality, all 18 key audits, and `git diff --check` passed. The refactored runner reproduced every prior LFW YuNet scientific metric exactly across all six attacker runs.

## 2026-09-04 (MOBIO acquisition and exploratory multi-exposure run)

- Data: eight authorized face-only MOBIO archives were downloaded on 2026-09-03, then extracted, moved outside Git to `%USERPROFILE%\ResearchData\MOBIO`, and validated on 2026-09-04. The 118,362 files include 28,800 selected still images from all 150 identities. Archive filenames, official MD5 values, byte sizes, extracted counts, and Luigi's setup commands are recorded in `docs/setup/MOBIO_LOCAL_DATA.md`. Compressed archives were removed after extraction; Zenodo metadata and `MD5SUM.TXT` were retained. Local data, manifests, embeddings, models, and detailed results remain ignored.
- Protocol: selected one image from each of 12 sessions per identity, assigned 90/30/30 train/validation/test identities, and extracted 1,799/1,800 YuNet-aligned ArcFace embeddings. The unprotected single-template baseline reached `100%` top-1 on 30 test identities.
- Preregistration: fixed nested 1/2/5/10 sets, eight repeats per identity, one held-out gallery image, per-image split-disjoint BioHash keys, model seeds 7/17/27, mean/max/DeepSets baselines, clustered intervals, and a five-point minimum amplification threshold before running.
- Result: independent unseen-key top-1 ranged `2.64-4.17%` against `3.33%` chance. All 10-exposure models reached `3.33%`; DeepSets AUROC was `0.4988`, EER `49.81%`, and its change from one exposure was `-0.83` points. Every run-level clustered interval included chance, so the amplification criterion failed.
- Controls: the unprotected 10-exposure oracle reached `100%` top-1. Shared-key mean pooling increased from `73.47%` at one exposure to `87.36%` at five, showing that the pipeline can exploit reusable-transform leakage.
- Interpretation: no multi-exposure identity amplification was detected for independently keyed local BioHash templates. This strengthens a negative result but is not irreversibility proof or a positive breakthrough. Confirm with new protocol/key seeds and another transform before publication-level claims.

## 2026-09-04 (MLP-Hash cross-scheme confirmation)

- Method: implemented the public-paper MLP-Hash specification with three 1024-unit ReLU hidden layers, 512-bit output-mean binarization, and semi-orthogonal random projections. The implementation is not source-exact because the stated GitLab repository was unreachable and the paper's row-orthonormal instruction is impossible for its narrowing output layer.
- Protocol: repeated the MOBIO 1/2/5/10 study with key/set seed identifier `20260911`, model seeds 37/47/57, 1,799 unique split-disjoint keys, and the preregistered five-point amplification threshold. Runtime was 18.23 minutes.
- Result: independent-key one-record top-1 was `2.50% +/- 1.10%`; 10-record DeepSets was `3.33%`, AUROC `0.4998`, and EER `49.81%`, against `3.33%` chance. The amplification criterion failed. The 10-record unprotected oracle was `100%`; shared-key mean pooling peaked at `80.83%` at five records.
- Interpretation: the second null is predicted by rotational invariance. For fixed-norm inputs and independent hidden Haar-like projections, each protected record has the same distribution for every source, and independent multiplicity cannot add identity information. This is a scoped proposition, not universal irreversibility; key reuse/correlation, norm leakage, finite-key defects, and non-invariant transforms are the next boundary tests.

## 2026-09-04 (system-key-pool boundary)

- Protocol: preregistered BioHash sweep with globally recurring hidden transform pools of 1/2/5/10 keys, a fresh 1,799-key endpoint, key seed 90431, set seed 90437, and model seeds 67/77/87. Keys recur across identity splits but remain hidden from the attack model. Runtime was 7.14 minutes.
- Result: at 10 records, mean-pool top-1 was `66.39%`, `61.11%`, `47.64%`, and `33.89%` for pools 1/2/5/10, versus `2.92%` for fresh keys and `3.33%` chance. Corresponding AUROCs were `0.9692`, `0.9639`, `0.9351`, `0.9043`, and `0.4991`. Every recurring-pool run's clustered lower bound exceeded chance; all recurring pools exceeded the fresh endpoint by at least five points.
- Interpretation at completion: this was a positive leakage phase boundary under transform reuse, not a contradiction of the fresh-key result. Pool size 1 repeated the prior calibration; pools 2/5/10 established the initial session-aligned curve. The randomized assignment below was required to separate key reuse from session ordering; new splits and cross-scheme confirmation remain necessary.

## 2026-09-04 (randomized key-pool confirmation)

- Protocol: preregistered sample-ID-hashed assignment, independent of session index, with key seed 90503, set seed 90509, model seeds 97/107/117, and otherwise unchanged evaluation. Runtime was 7.30 minutes.
- Result: 10-record mean-pool top-1 was `77.50%`, `69.44%`, `46.94%`, and `5.56%` for pools 1/2/5/10; AUROC was `0.9754`, `0.9608`, `0.8927`, and `0.5257`. The fresh endpoint was also `5.56%` top-1 with AUROC `0.4992`. Pools 1/2/5 excluded chance in every clustered interval; pool 10 did not.
- Decision: the preregistered all-recurring-pools criterion failed. The confirmation supports severe leakage for small recurring transform pools and locates a protocol-specific boundary between 5 and 10, but does not confirm the original session-aligned pool-10 effect. Future claims and figures must show both runs and must not describe the initial curve as universal.

## 2026-09-04 (key-pool generalization: dense sweep, MLP-Hash, new partition)

- Protocol: three runs preregistered together before inspection (see `docs/protocols/multi_exposure.md`), all with sample-ID-hashed randomized pool assignment and a new secondary endpoint, multiplicity amplification = 10-record mean-pool top-1 minus 1-record single-MLP top-1. Runtimes 7.82, 81.05, and 4.69 minutes.
- Dense sweep (BioHash, pools 3/4/6/7/8/9, seeds 90521/90527, models 127/137/147): 10-record top-1 `65.00/54.03/17.36/34.44/10.42/3.89%`, fresh `5.56%`. Pools 3/4/7 passed both criteria; 6/8/9 failed. One-record top-1 was `27.5%` for pool 3 and `3.2-4.2%` for pools 4-9. Amplification: pool 4 `+50.6` points, pool 7 `+30.3`, pool 9 `+0.7`.
- MLP-Hash (pools 1/2/5/10, seeds 90533/90539, models 157/167/177): `71.39/68.89/22.92/1.94%`, fresh `3.06%`. Pools 1/2 passed. Pool 5 exceeded the five-point margin but a clustered lower bound reached `0.0`, so it fails the interval criterion; its seed spread was large (std `19.9` points). Pool 10 failed.
- New identity partition (split seed 90551, keys 90557/90563, models 187/197/207; 90/30/30 preserved): `81.67/73.89/51.11/5.56%`, fresh `3.61%`. Pools 1/2/5 passed, pool 10 failed, reproducing the first randomized run within seed noise. Pool 5 amplification `+46.8` points from a 1-record rate of `4.3%`.
- Fresh-key controls: 1-record versus 10-record top-1 was `3.2%` vs `5.6%`, `2.9%` vs `3.1%`, and `4.0%` vs `3.6%`; no amplification, consistent with Theorem 1 in `docs/theory/multiplicity_invariance.md`.
- Interpretation: the reuse boundary is not a BioHash artefact and not a partition artefact. Under recurring hidden transforms, multiplicity converts chance-level single records into high linkage; under fresh keys it does not. The boundary location (about 7-9 transforms for BioHash, about 5 for MLP-Hash) is protocol-specific and noisy; pool 6 below pool 7 shows that single-seed points near the boundary must not be over-read.
- Theory note: while writing the proof it was found that `numpy.linalg.qr` without sign correction is not exactly Haar (Mezzadri 2007). The theorem covers the sign-corrected construction; a preregistered sign-corrected variant is now an open item.

## 2026-09-04 (boundary resolution: partitions 2/3, Haar-corrected, MLP-Hash 3/4)

- Partition 2 (split seed 90583): pools 3-9 gave `48.61/48.61/40.28/36.39/30.42/14.17/6.39%`, fresh `1.53%`. Pools 3-7 passed both criteria; 8/9 failed.
- Partition 3 (split seed 90599): pools 3-9 gave `56.39/51.94/8.06/8.61/8.89/3.89/6.67%`, fresh `4.44%`. Pools 3/4 passed; pools 5-9 failed. This partition collapses two pool sizes earlier than partitions A and 2.
- Pooled preregistered rule over three partitions (`dense_key_pool_pooled_analysis.csv`): pools 3 and 4 pass in 3/3 partitions (pooled `56.67%` and `51.53%`); pool 7 passes in 2/3 (`24.58%`); pools 5 and 6 pass in 1/3 or 1/2 (`24.17%`, `20.79%`); pools 8 and 9 pass in 0/3 (`9.49%`, `5.65%`); fresh pooled `3.84%`. Conclusion: robust reuse regime at k <= 4; partition-dependent transition at k = 5-7; null at k >= 8 for this protocol.
- Haar sign-corrected BioHash (exactly-Haar construction covered by Theorem 1): pool 1 `74.58%` (1-record `75.00%`), pool 5 `48.06%` (1-record `3.47%`), fresh `2.64%` (1-record `3.06%`). Both pools passed; behaviour matches the default QR construction, so the implementation caveat does not change any conclusion.
- MLP-Hash pools 3/4: `54.31%` and `37.78%`, fresh `3.47%`; 1-record `3.06%` and `4.58%`. Both passed. Combined with the earlier run, the MLP-Hash boundary lies between 4 (pass) and 5 (interval failure), i.e. slightly earlier than BioHash.
- Second dataset: funneled LFW downloaded (127 identities with >= 12 images); a 125 x 12 protocol with 75/25/25 identity-disjoint splits was built (seed 20260904) and 1,500/1,500 embeddings extracted with the same hash-pinned YuNet and ArcFace models. Key-pool run preregistered before inspection; results pending at time of writing.
