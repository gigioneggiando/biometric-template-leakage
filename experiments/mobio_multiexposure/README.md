# MOBIO multi-exposure study

Classification: **exploratory independent study, not a `benchmark_cb` reproduction**.

The protocol was fixed in `docs/protocols/multi_exposure.md` before this run. It uses 1,799 ArcFace embeddings from 150 identity-disjoint MOBIO subjects, one held-out gallery image per identity, eight nested exposure sets per identity, 128-bit BioHash templates, and model seeds 7/17/27. Every source image has one fixed key; all 1,799 keys are unique and split-disjoint. Each exposure level has 720 train, 240 validation, and 240 test sets.

## Primary result

The preregistered exposure-amplification criterion was not met. Under independent unseen keys, the common one-exposure MLP achieved `4.17% +/- 1.91%` top-1 against `3.33%` chance. At 10 exposures, mean-pool, max-pool, and DeepSets each achieved `3.33%` top-1; DeepSets AUROC was `0.4988` and EER was `49.81%`. Every run-level identity-clustered 95% interval included chance. DeepSets changed by `-0.83` percentage points from 1 to 10 exposures, below the preregistered `+5` point threshold.

Results were consistent at two and five exposures across mean pooling, max pooling, and DeepSets. Mean cosine to the exposed-image target increased slightly with more records, but genuine and impostor gallery scores remained indistinguishable, so this is not identity recovery.

## Validity controls

The unprotected averaged-embedding oracle achieved `100%` top-1 at 10 exposures. The shared-key calibration reached `73.47%` top-1 at one exposure and mean pooling peaked at `87.36%` with five exposures (AUROC `0.9849`, EER `5.99%`). These controls show that the face embeddings contain identity signal and the learned pipeline exploits it when the transform is reusable.

## Interpretation

The result is a strong exploratory negative: no identity leakage amplification was detected from up to 10 independently keyed BioHash templates under unseen identities and unseen keys. It does not prove irreversibility. The local BioHash implementation has not been cross-checked against unavailable `benchmark_cb` code, repeated sets share source records, and this run fixes one protocol assignment and one key seed. Confirmation requires new protocol/key seeds and ideally another cancelable transform before a strong paper claim.

Full metrics remain local under `results/mobio_multiexposure/`. The tracked summary is `results_summary.csv`. Reproduce with:

```powershell
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py `
  --config configs\attacks\mobio_multiexposure.yaml
```
