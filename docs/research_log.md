# Research log

## 2026-09-18 (raw-norm audit and manuscript revision)

- User requested closest-work comparison, justified attacker access, implementation checks, genuine raw-input controls, complete follow-up inference/failures and revised PDF.
- Froze the new protocol and executed sources against `15e4384`; completed in 254.157 seconds within 3,600 seconds. Re-extracted all 4,177 MOBIO/FEI records; normalized maximum error 2.98e-8. Private raw arrays remain ignored.
- Separate scalar PolyProtect matches all 48 cells exactly; independent cosine rankings agree, with no ties, gallery overlap or order dependence. Sampled IoM natural-scale comparisons change zero of 38,400 codes.
- Native raw top-1 15.58-16.66%; raw-unit paired correction survives only on FEI. Raw-shuffled adjusted p >= 0.7584; norm-only oracle tests do not survive correction. Identity-specific norm leakage is not established.
- All 48 trained follow-up contrasts exported with crossed intervals, seed ranges and leave-one-out sensitivity: eight pool-4 mean gains and four shared-key PolyProtect DeepSets losses survive post-hoc Holm family 48 (p = 0.0192). Original primary family unchanged.
- Primary literature check corrects Li/Hu DOI to 10.1002/cpe.3042 and updates FaceLinkGen to v3. PolyProtect already studies 1-10 records and naive-parameter residual linkage. Candidate novelty is controlled hidden-pool set aggregation, not those general ideas. Same-pool training access and closed-gallery membership are explicit assumptions.
- Manuscript narrowed to three claims; report expanded to 14 pages, deck to ten slides, appendix to 17 figures, with a plain-language page guide. No new raw-input learned training, stronger parameter-policy test or independent human review is claimed. [Audit report](../experiments/norm_native_audit_2026-09-18/README.md).
- Validation: 62 focused scheme/figure tests pass; 32 earlier and 33 new executed source hashes remain unchanged. All 14 rendered PDF pages visually inspected; separate formula/matcher tests and aggregate-family checks pass. No editor diagnostics in touched Python files. Native PowerPoint rendering remains a presenting-machine check.

## 2026-09-18 (bounded multi-seed follow-up, after the visual refresh)

- Authorization: user explicitly allowed up to one hour of local compute and selected available MOBIO/FEI data; SCface embeddings were unavailable on this host.
- Freeze: [protocol](protocols/scheme_followup_2026-09-18.md), configuration and 32 source/configuration/protocol SHA-256 hashes recorded before execution against base `4352eeb`, with dirty-worktree status explicit. All hashes matched after execution.
- Execution: `python scripts/train/run_scheme_followup.py` completed all 24 cells / 216 endpoints in 859.625 seconds total (848.657 seconds training), CPU, eight Torch threads. Two identity assignments, three model seeds, two schemes, fresh/shared/pool-4, single/mean/DeepSets, matched 120-epoch caps.
- Result: eight primary pool-4 amplification contrasts have positive crossed seed/identity bootstrap intervals and Holm p = 0.004. Twelve fresh PolyProtect native gallery-label permutation tests have Holm p = 0.006. IoM-GRP is invariant to tested positive radial scales; PolyProtect is sensitive. Native matching is a distinct task, and radial stress is not natural norm leakage.
- Inventory: all previous 633 rows compared unchanged before exporting 849 rows from 49 artifacts. Coverage audit identifies two legacy-schema MOBIO sources and unavailable SCface detailed artifacts; aggregate SCface results are retained.
- Presentation: split architecture overview and detailed attacker; replace submission/A-ranking commentary with findings and scientific scope; add two follow-up plots, making 15 figures. Old pilots remain separate.
- Reporting fix: new exports distinguish trained-model `seed` from `bootstrap_seed`; earlier pilot paired tables had bootstrap seed 91223 in their seed column. Historical numeric results were not rewritten.
- Scope: overlapping partitions and fixed training key/set seeds; no new SCface/LFW training, natural norm extraction, full exposure matrix, approved equivalence margin or independent human review. [Complete results](../experiments/scheme_followup_2026-09-18/README.md).

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
- Second dataset: funneled LFW downloaded (127 identities with >= 12 images); a 125 x 12 protocol with 75/25/25 identity-disjoint splits was built (seed 20260904) and 1,500/1,500 embeddings extracted with the same hash-pinned YuNet and ArcFace models. Key-pool run preregistered before inspection.

## 2026-09-04 (LFW second-dataset replication)

- Result (10-record mean-pool top-1, chance `4.00%`): pools 1/2/3/4/5/7/10 gave `73.17 / 63.17 / 62.50 / 42.50 / 41.00 / 32.00 / 25.33%`; fresh keys `4.00%` with zero seed variance, AUROC `0.505`; 1-record fresh `4.67%`. Oracle `100%`. Runtime 5.66 minutes.
- Criteria: pools 1-7 passed; pool 10 exceeded fresh by `21.3` points but one clustered lower bound equalled chance, so it fails the interval criterion.
- Interpretation: the fresh-key null and reuse amplification transfer to public in-the-wild images. The decay with pool size is slower than on MOBIO (pool 10 `25.3%` versus `5.6%`) and single-record leakage persists to pool 7 (`11.7%`), so the boundary is dataset-dependent. This is the first cross-dataset confirmation of the central claim.

## 2026-09-05 (key-slot and shuffled-record mechanism controls)

- Preregistration: committed configs and implementation before execution. The first key-slot pair was then found invalid for its intended interpretation because mean pooling discarded each template-to-slot association before the MLP. The invalid configs were retained and marked; a corrected DeepSets pair with new split/key/set seeds `90767/90779/90787` and model seeds `419/421/431` was committed before inspecting corrected results.
- Corrected key-slot result: hidden-slot 10-record top-1 for pools 3/4/5/7 was `55.28/46.25/32.92/23.75%`, fresh `3.33%`; slot-known was `57.08/50.69/33.61/22.92%`. Differences `+1.81/+4.44/+0.69/-0.83` points. Runtimes 2.81 and 2.29 minutes on CUDA.
- Shuffled control: every set retained one correct anchor and received nine non-anchor records from other identities. Pool 3, pool 4, and fresh-key 10-record top-1 were all exactly `3.33%` for every seed; AUROC `0.4994/0.5029/0.5001`. Runtime 1.67 minutes on CUDA.
- Interpretation: the new hidden-slot baseline independently replicates the reuse curve. Explicit slot labels do not materially shift its boundary. Shuffling eliminates the gain, so multiplicity amplification requires multiple same-identity records rather than set size, global transform frequencies, or the runner alone. Same-image, norm, and key-correlation controls remain open.

## 2026-09-06 (same-image and correlated-key controls)

- Preregistration and implementation: added an exact same-image/different-fresh-key set constructor and a sign-corrected BioHash construction with an exact system-wide shared projection prefix plus orthogonal private columns. Tests verify nested fresh keys, shared prefixes, and projection orthonormality. The coarse sweep and same-image control were committed before execution; the fine sweep was committed on a new partition after the coarse 25% point was classified as suggestive.
- Same-image result: the paired different-image fresh baseline and the identical-image/different-fresh-key control both gave exactly `3.33%` 10-record top-1 for every seed. The same-image AUROC was `0.4997`; its one-record mean was `3.19%`. Session/image variation does not explain the fresh-key null.
- Coarse correlation sweep (shared dimensions 0/32/64/96/128): 10-record top-1 was `3.33/9.44/46.39/61.11/71.67%`, with one-record `3.33/3.33/39.17/50.83/69.17%`. The 25% point was unstable; 50% and above were large for every seed.
- Independent fine sweep (0/16/24/32/40/48/56/64 shared dimensions): 10-record top-1 was `3.33/3.75/6.94/7.64/14.17/35.83/49.31/42.64%`; AUROC was `0.503/0.532/0.574/0.601/0.656/0.846/0.877/0.885`. Results were consistently large from 37.5% shared dimensions onward. The 18.75-31.25% region was seed-sensitive, and 43.75% exceeded 50%, so no sharp or monotonic threshold is claimed.
- Interpretation: the fresh-key null survives removal of image/session variation, while controlled violations of key independence create a graded leakage regime. Correlation increases both single-record leakage and additional multi-record amplification. The construction is a mechanism probe, not a standard key-derivation implementation or `benchmark_cb` reproduction. Norm leakage remains open.

## 2026-09-10 (meeting with Sani: generalization roadmap)

- Decision: validate the central fresh-key versus transform-reuse/correlation finding on two additional facial-biometric datasets; retain a third candidate if access and compute permit.
- Decision: add two template-protection schemes beyond BioHash and MLP-Hash, chosen only after source, specification, license, and key-semantics review.
- Decision: prepare a concise English slide/results package covering the architecture, threat model, methods, datasets, protection schemes, metrics, results, controls, limitations, and reproduction status.
- Planning action: added `docs/ROADMAP.md` with dataset/scheme gates, a staged pilot-to-confirmation matrix, acceptance criteria, milestones, and presentation requirements; expanded `docs/TODO.md` with assignable tasks.
- No new experiment or scientific result was produced by this planning update.

## 2026-09-10 (official-source dataset review)

- Reviewed official dataset pages, terms, access routes, published counts, protocol fit, variation, expected compute, and known or plausible overlap with the `buffalo_l` WebFace600K training population.
- Proposed AgeDB and SCface as primary datasets: AgeDB adds longitudinal age variation; SCface supplies 32 captures per identity across camera, distance, pose, illumination, and visible/IR conditions.
- Proposed QMUL-SurvFace as a contingency/third pilot for native low-resolution surveillance and scale. Its per-identity distribution, near-duplicate rate, source-dataset terms, and ArcFace positive control remain gating checks.
- Excluded IJB-A/B/C and VGGFace2 from new acquisition because the official distributors state that distribution/downloads are no longer available. Deferred CMU Multi-PIE because its official acquisition link is currently ineffective and the source reports more than 305 GB.
- Added `docs/datasets/candidate_selection_2026-09-10.md`. No data were downloaded and no experimental result was produced.

## 2026-09-10 (quality/access revision and protection review)

- Tightened the dataset criteria around guaranteed record count, visual/acquisition quality, active official distribution, provenance, and immediate RTX 2060 feasibility. Added FEI as Primary A: 200 identities x 14 colour 640 x 480 images, balanced by source-reported binary sex, with four active official archives totalling about 344 MB.
- Revised the proposed dataset set to FEI + SCface as primaries and AgeDB as the third/contingency dataset. QMUL-SurvFace was demoted to a later scale test because native low resolution, source-dataset provenance, duplicate structure, and ArcFace utility add avoidable first-stage risk.
- Audited IoM-GRP, PolyProtect, SWG-MinHash/CBEF, Bloom-filter face BTP, IoM-URP, IronMask, SecureTL, and SecureVector. Proposed paper-specified IoM-GRP and PolyProtect as distinct primary schemes.
- Verified external heads: PolyProtect Kotlin `535bdd2c886af2d02f03ac12296ba01196cfdd34` (GPL-3.0), face/LSH reference `6225f119726bc1c0711a37a5dffccf4325cb7f53` (no license), and CBEF `686c31f76dc10ff955def2650156684350c6d8ed` (Apache-2.0).
- CBEF audit: 21 scoped method/verification/metric tests passed; full collection failed on an undeclared `cv2` import, and SWG lacks a dedicated upstream unit test. PolyProtect's external Gradle tests could not start because Android SDK configuration is absent locally. These are source/environment findings, not local scheme implementations or scientific results.

## 2026-09-12 (FEI third dataset and figure package)

- Acquisition: downloaded the four official FEI `originalimages_part1-4.zip` archives (86.9/89.2/88.2/89.3 MB) from the official page, hashed them (SHA-256 recorded outside Git), extracted to `%USERPROFILE%\ResearchData\FEI\originalimages`: 2,800 JPEG, 200 subjects, 14 poses each. The first attempt at part 4 was truncated by a transfer interruption and was re-downloaded before hashing.
- Protocol: added `src/biometrics_ai/data/fei.py`, `scripts/data/prepare_fei_protocol.py`, and `tests/unit/test_fei.py`. 200 identities x 12 images, seed 20260912, 120/40/40 identity-disjoint split. Extraction with the hash-pinned YuNet/ArcFace models gave 2,378/2,400; all 22 failures are the low-illumination pose 14 and every identity retains >= 11 embeddings. Preregistered in `docs/protocols/multi_exposure.md` before the run.
- Result (10-record mean-pool top-1, chance `2.50%`): pools 1/2/3/4/5/7/10 gave `76.88 / 63.44 / 54.79 / 47.50 / 37.50 / 23.65 / 3.96%`; fresh keys `1.77%` (1-record `2.29%`), AUROC `0.502`; oracle `100%`; runtime 8.65 min. Pools 1-7 passed both criteria; pool 10 failed. Single records are at chance from pool 3 onward (`2.4-3.8%`) while ten records recover `24-55%`.
- Interpretation: third dataset and second public dataset consistent with Theorem 1 under fresh keys and with the reuse-amplification signature. FEI boundary (7-10) matches MOBIO partitions A/2; LFW remains the outlier with pool 10 still at `25%`. FEI is single-session, so it tests pose rather than session variation.
- Figures: added `scripts/figures/make_figures.py`, `make_diagrams.py`, and `build_cross_dataset_table.py`. All plots read tracked compact CSVs; `experiments/cross_dataset_key_pool_summary.csv` (55 rows) is the canonical table. Architecture and threat-model diagrams are drawn as vector graphics with no raster assets.

## 2026-09-12 (approved scheme pilots and evidence audit)

- Organized the existing research package in commit `15bb664`, preserving historical paths and excluding biometric artifacts. The earlier comparison was corrected to 65 conditions from 11 sources; it is a study-level table, not a per-seed canonical matrix. Earlier descriptions of all pools 1-7 passing on FEI refer only to tested pools 1/2/3/4/5/7; pools 6/8/9 were untested. Chance inclusion is not equivalence.
- The user reported Sani's approval of paper-specified IoM-GRP and PolyProtect, with pilots first and at most one hour of new training. No authorized SCface/AgeDB access is available. Prepared an official request checklist; no external request or agreement was submitted.
- Independently implemented IoM-GRP (m=300,q=16, categorical output encoded one-hot) and PolyProtect (window=5, overlap=2, unique nonzero coefficients in [-50,50], exponent permutation 1..5, raw 170-dimensional output). Primary algorithms, key scopes and pilot settings were frozen in commit `d5f4e89` before execution. Neither is a source-exact reproduction.
- All 16 MOBIO/FEI cells completed on CPU in 277.89 seconds, producing 48 model runs at exposures 1/10, pools 1/4/8/fresh, model seed 419 and 120-epoch cap. No full confirmation was launched. The previous GPU entry describes a different host/run state.
- Pool-4 paired ten-minus-one mean-pool gains: IoM-GRP MOBIO/FEI +37.92/+33.75 percentage points; PolyProtect +30.00/+58.13. All four 95% identity-bootstrap intervals exclude zero conditional on one seed/partition, without multiplicity correction. Full tables retain negative and near-zero gains elsewhere.
- Fresh-key interval sensitivity does not establish equivalence: none of 12 endpoints meets +/-1 point and only one meets the illustrative +/-2-point band. Native fresh PolyProtect protected-gallery top-1 is 12.73%/13.73% versus 3.33%/2.50% chance, despite learned unprotected-gallery linkage near chance. These are separate tasks; no privacy conclusion is justified.
- Corrected the theorem's side-information corollary: independence from identity alone does not suffice; joint independence of key randomness from sources and side information is required. Added a sign counterexample, finite-implementation caveats and the distinction between norm-information bounds and actual norm leakage. PolyProtect already studies disclosed-parameter record multiplicity; independent novelty/proof review remains pending.
- Exported 633 per-seed rows from 25 local multi-exposure artifacts, including all 48 pilots; five other-schema artifacts are excluded. Local coverage is not a guarantee of full historical reconciliation. No identities, templates, keys or weights were exported.
- Refreshed two diagrams, ten result plots, the eight-slide editable deck/PDF and a 12-figure vector appendix. New one-seed pilots stay separate from earlier three-seed studies. Access, full confirmation, approved statistical margins and independent human review remain submission gates.

## 2026-09-18 (SCface fourth dataset and scheme pilots)

- Acquisition: Sani supplied the authorized SCface project archive (`SCface_database.zip`, 1,546,981,520 bytes, SHA-256 `F9F819C5B9634F457F1FE683E88F7BDF054174DDDC60F2947DBEA2BDFAFB1D7F`) directly. Extracted `mugshot_frontal_cropped_all/` and `surveillance_cameras_all/` only; the latter's one infrared image and the nine pose mugshots per identity are excluded. See `docs/setup/SCFACE_LOCAL_DATA.md`.
- Protocol: added `src/biometrics_ai/data/scface.py`, `scripts/data/prepare_scface_protocol.py`, and `tests/unit/test_scface.py`. All 130 identities, the frontal mugshot as held-out gallery, 21 visible surveillance images (seven cameras, three distances) as exposure candidates, identity-disjoint 78/26/26 split, seed `20260918`. Extraction with the hash-pinned YuNet/ArcFace models gave 2,851/2,860; all 130 gallery mugshots succeeded and every identity retains at least 19 exposures. Preregistered in `docs/protocols/multi_exposure.md` before the run.
- Unprotected mugshot-to-surveillance oracle: `84.375%` top-1, `91.176%` top-5, AUROC `0.9474`, EER `10.827%` over 544 test probes, despite the cross-camera/cross-distance domain shift.
- BioHash result (10-record mean-pool top-1, chance `3.846%`), frozen at commit `69a93e4`: pools 1/2/3/4/5/7/10 gave `81.57/61.06/33.17/20.51/5.93/1.92/3.04%`; fresh keys `3.85%` (1-record `4.33%`), AUROC `0.502`; runtime 392.14 seconds on CUDA. Pools 1-3 passed the all-seed clustered-interval criterion; pools 4/5/7/10 did not.
- Scheme pilots: one-seed IoM-GRP/PolyProtect engineering pilots at pools 1/4/8/fresh, also frozen at `69a93e4`. All eight cells (24 model runs) completed in 128.22 seconds on CPU. Pool-4 paired ten-minus-one mean-pool gains: IoM-GRP `+34.62` points, PolyProtect `+41.83` points. Native fresh-key PolyProtect protected-gallery top-1 is `10.66%` versus `3.846%` chance; IoM-GRP is `4.60%`.
- Figures/docs: extended `build_cross_dataset_table.py`, `make_figures.py`, `make_diagrams.py`, and `make_presentation.py` to include SCface; `experiments/cross_dataset_key_pool_summary.csv` grew to 73 rows from 12 sources. Fixed a diagram text-overflow regression in `fig_architecture` caused by the longer dataset label. Updated `reports/README.md`, `reports/final_research_status.md`, `reports/figures/README.md`, `docs/ROADMAP.md`, `docs/TODO.md`, and `docs/datasets/access_request_checklist.md` to reflect SCface completion; AgeDB access remains unavailable.

## 2026-09-18 (September report, architecture and documentation refresh)

- Refreshed `reports/Sept_Dataset_Update.pdf` from the superseded five-page three-dataset update into a reproducible nine-page report. Evidence baseline: `4352eeb`; SCface protocol freeze: `69a93e4`; MOBIO/FEI pilot freeze: `d5f4e89`. Provenance labels use commit numbers only. The report now distinguishes 73 key-pool conditions / 12 studies from 24 one-seed pilot cells / 72 model endpoints.
- Redrew the architecture with separate data/protection and attacker/evaluation sections, schematic icons, explicit dimensions, hidden-key assumptions, training-only targets and uncertainty boundaries. A dedicated report page defines the MLP/DeepSets layers, training objective, optimizer and evaluation protocol. Source PDFs are composed with `pypdf==6.19.0`, preserving vector architecture and searchable plot labels; heatmap cells remain intentional raster layers. A/A* readiness is not claimed.
- Regenerated the comparison table, all 12 PDF/PNG figure pairs, eight-slide PDF/editable PPTX, vector appendix and September PDF with `scripts/figures/build_cross_dataset_table.py`, `make_figures.py`, `make_diagrams.py`, and `make_presentation.py`. No new training, dataset acquisition or result modification was performed.
- Updated all 20 tracked READMEs with current status/review dates, acquisition references and current-result links while preserving historical experiment dates. Removed stale SCface access requests and tightened unsupported claims about untested pools, equivalence and privacy. The local per-seed inventory remains 633 rows / 25 artifacts with no SCface rows; tracked SCface aggregate tables are included directly in figures. Detailed SCface artifacts are unavailable on this host, so the inventory was not overwritten by a partial scan.
- Deleted only 12 obsolete September 12 PNG previews from ignored `results/figure_audit/`: the eight old `fig_*.png` previews, `figure_appendix_final.png`, `pilot_slide_final.png`, `research_review_final.png`, and `slides_contact_sheet.png`. These had no file-specific repository references and the old contact sheet showed superseded three-dataset content. Current report formats, historical results, configurations, archive provenance, private data and model weights were retained. A fresh September report contact sheet is local and ignored.
- Validation: `python -m pytest tests/unit/test_figures.py -q` passed 22 tests before the commit-only wording change; its focused September-report test passed again afterward. All 20 READMEs were updated and all their local Markdown links resolved. `git diff --check` passed. Visual inspection covered the architecture and nine-page report contact sheet; export tests cover text bounds/collisions and nonblank rendered pages. Initial architecture text overflow was resolved by shorter labels and a wider canvas. Native PowerPoint rendering and independent scientific review remain human checks.
