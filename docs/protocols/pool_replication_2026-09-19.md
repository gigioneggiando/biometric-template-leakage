# Independent-pool replication and matched aggregation baseline

Protocol recorded before execution on 19 September 2026. This is a new bounded follow-up, not a replacement for the frozen 18 September results. Computational execution does not constitute independent human review.

## Questions and fixed design

1. Does the one-to-ten mean-pooling gain persist across independently generated recurring pools?
2. Does protected-input mean pooling improve on averaging independently reconstructed records from the matched single-record attacker?

Use MOBIO and FEI, IoM-GRP and PolyProtect, identity assignments 91831 and 91843, and pool size 4. Draw three new pools with key seeds 91901, 91907 and 91909; do not select seeds by performance. Hold set seed 91867, eight nested sets, model seeds 601/607/613, optimizer, normalized targets, encoder, 120-epoch cap and patience 30 fixed to the earlier follow-up. This yields 24 dataset/scheme/partition/pool cells and 144 trained endpoints (single and mean, three model seeds); 72 additional prediction-mean endpoints require no additional training. No private key, embedding, identity or per-identity score is published.

For each trained single-record model, apply the same checkpoint independently to each of the ten protected records, average its normalized predictions and normalize again. Compare this output with the same held-out gallery used by the input-mean model. This baseline has the same paired training access and inference records; its training objective is single-record reconstruction, intentionally not a set-trained objective. Do not claim a match in parameter count across protection schemes or an exhaustive state-of-the-art comparison.

## Analysis

Report per-pool accuracy and gains, plus pool/model-seed/identity crossed bootstrap intervals with 4,000 draws. Pair identities, exposure sets, model seeds and pools for differences. Treat each partition separately because assignments overlap. The eight primary summaries are mean-input ten minus single one, one for each dataset/scheme/partition. Report the direct mean-input ten minus prediction-mean ten comparison as a separate eight-summary secondary family. Report uncertainty and all signs without choosing favorable pools. Three pools and three model seeds provide limited uncertainty estimation; no universal key-distribution or deployment claim follows. Do not reuse identity-only p-values as if they tested a population of random pools. No significance threshold is used to select which results are published.

## Boundaries and execution

Use a one-hour maximum wall-clock budget, save each completed cell and report any incomplete matrix explicitly. Preserve old frozen sources; implement a separate runner using existing low-level training/protection utilities. Freeze source/configuration hashes and input-file hashes before training, and refuse to overwrite a completed execution. Test prediction averaging, pool-axis resampling and key-dependent template changes before the full run.

SCface remains supporting historical and one-seed pilot evidence unless authorized embeddings and camera-aware metadata are verified locally. Its existing aggregates must not be promoted to matched confirmation. LFW remains historical BioHash evidence. A coverage diagram must display these differences explicitly. No raw-input retraining, stricter PolyProtect policy, open-set gallery or new encoder is part of this study.