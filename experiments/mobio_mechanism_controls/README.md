# MOBIO key-reuse mechanism controls

Status: **COMPLETED EXPLORATORY CONTROLS; NOT A PAPER REPRODUCTION**.

Both controls were preregistered in `docs/protocols/multi_exposure.md` before inspection and use the existing MOBIO selected-still pipeline: 150 identities, 12 sessions, identity-disjoint 90/30/30 splits, one held-out gallery image, eight sets per identity, 128-bit BioHash, and three model seeds. Chance top-1 is `3.33%` over 30 test identities. Full metrics remain local under `results/`.

## Corrected key-slot-known control

The paired runs use the same split/key/set/model seeds. A DeepSets attacker receives either protected templates alone or each template concatenated with the one-hot identifier of its recurring transform before per-record encoding.

| pool | hidden slot top-1 | known slot top-1 | difference | hidden AUROC | known AUROC |
|---|---:|---:|---:|---:|---:|
| 3 | 55.28% | 57.08% | +1.81 pp | 0.952 | 0.950 |
| 4 | 46.25% | 50.69% | +4.44 pp | 0.925 | 0.933 |
| 5 | 32.92% | 33.61% | +0.69 pp | 0.873 | 0.869 |
| 7 | 23.75% | 22.92% | -0.83 pp | 0.853 | 0.806 |
| fresh | 3.33% | N/A | N/A | 0.499 | N/A |

The hidden-slot baseline independently replicates the reuse curve on a new identity partition, while its fresh endpoint remains exactly at chance. Explicit slot labels improve top-1 by at most `4.44` points and do not move the boundary. This suggests that implicit mixture identification is not the primary bottleneck for the tested DeepSets attacker; recurring transforms expose identity structure even without slot labels.

An earlier mean-pool pair is deliberately excluded. Mean pooling occurred before the MLP, so appended one-hot labels retained only a slot histogram and not the template-to-slot association. Its configs are marked invalid, the protocol correction is recorded, and no result from that pair supports a claim.

## Shuffled non-anchor control

Every 10-record test set retains one correctly assigned target record but replaces records 2-10 with records from other identities, position by position. Record count and marginal template distribution are preserved.

| condition | 1-record top-1 | shuffled 10-record top-1 | 10-record AUROC |
|---|---:|---:|---:|
| recurring pool 3 | 18.19% | 3.33% | 0.499 |
| recurring pool 4 | 4.03% | 3.33% | 0.503 |
| fresh keys | 3.75% | 3.33% | 0.500 |

All three shuffled 10-record conditions equal chance for every model seed, and every identity-clustered interval includes chance. The large recurring-pool gain therefore requires multiple records from the same identity; it is not explained by set size, global transform frequencies, or the runner alone. The negative amplification for pool 3 (`18.19%` to `3.33%`) is expected because nine nuisance identities overwhelm its one informative anchor under mean pooling.

Reproduce with:

```powershell
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\mobio_key_slot_deepsets_baseline.yaml
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\mobio_key_slot_deepsets_known.yaml
.\.venv\Scripts\python.exe scripts\train\run_real_multiexposure.py --config configs\attacks\mobio_shuffled_record_control.yaml
```
