# MOBIO multi-exposure study

Classification: **exploratory independent study, not a `benchmark_cb` reproduction**.

The protocol was fixed in `docs/protocols/multi_exposure.md` before this run. It uses 1,799 ArcFace embeddings from 150 identity-disjoint MOBIO subjects, one held-out gallery image per identity, eight nested exposure sets per identity, 128-bit BioHash templates, and model seeds 7/17/27. Every source image has one fixed key; all 1,799 keys are unique and split-disjoint. Each exposure level has 720 train, 240 validation, and 240 test sets.

## Primary result

The preregistered exposure-amplification criterion was not met. Under independent unseen keys, the common one-exposure MLP achieved `4.17% +/- 1.91%` top-1 against `3.33%` chance. At 10 exposures, mean-pool, max-pool, and DeepSets each achieved `3.33%` top-1; DeepSets AUROC was `0.4988` and EER was `49.81%`. Every run-level identity-clustered 95% interval included chance. DeepSets changed by `-0.83` percentage points from 1 to 10 exposures, below the preregistered `+5` point threshold.

Results were consistent at two and five exposures across mean pooling, max pooling, and DeepSets. Mean cosine to the exposed-image target increased slightly with more records, but genuine and impostor gallery scores remained indistinguishable, so this is not identity recovery.

## Validity controls

The unprotected averaged-embedding oracle achieved `100%` top-1 at 10 exposures. The shared-key calibration reached `73.47%` top-1 at one exposure and mean pooling peaked at `87.36%` with five exposures (AUROC `0.9849`, EER `5.99%`). These controls show that the face embeddings contain identity signal and the learned pipeline exploits it when the transform is reusable.

## Interpretation

The result is a strong exploratory negative: no identity leakage amplification was detected from up to 10 independently keyed BioHash templates under unseen identities and unseen keys. It does not prove irreversibility. The local BioHash implementation has not been cross-checked against unavailable `benchmark_cb` code, repeated sets share source records, and this run fixes one protocol assignment and one key seed.

## Cross-scheme confirmation

A preregistered paper-specified MLP-Hash run used a new key/set seed identifier (`20260911`), model seeds 37/47/57, 512-bit outputs, three 1024-unit ReLU hidden layers, and the same identity-disjoint MOBIO evaluation. The independent-key one-record reference reached `2.50% +/- 1.10%` top-1. Ten-record DeepSets reached `3.33%` top-1, AUROC `0.4998`, and EER `49.81%`; its clustered intervals did not exclude `3.33%` chance and the preregistered amplification criterion failed. The 10-record unprotected oracle reached `100%`, while shared-key mean pooling reached `80.83%` at five records.

This confirms the multiplicity null across a linear sign-projection scheme and a nonlinear random-network scheme. MLP-Hash is labelled paper-specified, not source-exact, because the authors' GitLab source was unavailable and the paper's row-orthonormal instruction is dimensionally impossible at its narrowing output layer.

## Key-reuse boundary

The preregistered system-key-pool sweep produced a strong positive boundary result. With 10 exposed records, mean-pool top-1 was `66.39%`, `61.11%`, `47.64%`, and `33.89%` for globally recurring hidden transform pools of 1, 2, 5, and 10 keys, respectively. With 1,799 fresh split-disjoint keys it fell to `2.92%`, below `3.33%` chance. AUROC declined from `0.9692` to `0.9043` across recurring pools and reached `0.4991` with fresh keys. Every recurring-pool run had an identity-clustered lower bound above chance and exceeded the fresh-key endpoint by more than the preregistered five-point margin.

This is evidence of a deployment boundary, not a break of the fresh-key guarantee: hidden transforms become learnable when they recur across training and test identities. Pool size 1 duplicates the shared-key control; pools 2/5/10 establish the initial degradation curve. Because this assignment is deterministic by session/sample index, it was followed by a preregistered randomized confirmation.

The confirmation assigned pool slots by a deterministic hash of sample ID, independent of session index. Ten-record mean-pool top-1 was `77.50%`, `69.44%`, and `46.94%` for pools 1/2/5, with all clustered intervals excluding chance. Pool 10 fell to `5.56%` with AUROC `0.5257`, matching the fresh endpoint's `5.56%` top-1 and failing the preregistered interval and five-point criteria. The defensible result is therefore severe leakage under small recurring pools, with a boundary between 5 and 10 transforms under this protocol. It is not evidence for a smooth universal curve; the session-aligned pool-10 result was partly confounded.

Full metrics remain local under `results/mobio_multiexposure/`, `results/mobio_multiexposure_mlphash/`, `results/mobio_key_pool_boundary/`, and `results/mobio_random_key_pool_confirmation/`. Compact tracked summaries are stored beside this file. Reproduce with:

```powershell
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py `
  --config configs\attacks\mobio_multiexposure.yaml
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py `
  --config configs\attacks\mobio_multiexposure_mlphash.yaml
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py `
  --config configs\attacks\mobio_key_pool_boundary.yaml
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py `
  --config configs\attacks\mobio_random_key_pool_confirmation.yaml
```
