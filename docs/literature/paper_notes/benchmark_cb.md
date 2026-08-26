# benchmark_cb

Research question: benchmark recognition, unlinkability, and irreversibility of cancelable schemes on DNN templates. The paper evaluates BioHashing, MLP Hashing, Bloom Filters, IoM-URP, IoM-GRP, and Rand-Hash across face, voice, finger vein, and iris. The face branch uses ArcFace on 150 MOBIO subjects, with 1,516,300 mated and 22,952 non-mated comparisons.

The paper's `normal` recognition scenario uses user-specific keys. Its `stolen-token` scenario assumes disclosed/non-user-specific key material. For recognition, all sample combinations form mated comparisons and the first sample per subject forms non-mated comparisons. For irreversibility, protected and unprotected matrices are reduced to 100 PCA dimensions and mutual information is estimated under a multivariate-Gaussian approximation.

Verified face targets from the official TeX are: unprotected EER `0.02%`; BioHash EER `0.02%` normal / `0.04%` stolen-token; MLP-Hash `0.02%` / `0.02%`; Bloom Filters `2.19%` / `35.40%`; IoM-GRP `0.02%` / `0.04%`; IoM-URP `0.72%` / `1.10%`; Rand-Hash `0.02%` / `0.08%`. BioHash MI is `39.63` normal / `98.81` stolen-token. These are literature targets, not local results.

The official TeX names `https://github.com/otroshi/benchmark_cb`, but that URL returned 404 on 2026-08-26 and no renamed source was found in the author's current public repositories or author/Idiap code searches. No upstream commit or command is therefore represented as locally verified. A faithful run still needs authorized MOBIO, source recovery from the authors, and exact preprocessing/configuration details.

Our setting differs: benchmark_cb evaluates individual protected templates and protection criteria; the proposed study learns identity leakage from a set under independent unknown keys.
