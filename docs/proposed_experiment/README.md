# Proposed experiment readiness

Implemented now: deterministic key generation, a BioHash reference interface, identity/key-disjoint synthetic test data and real LFW/Olivetti/CFP/MOBIO protocols, single-template MLP and masked permutation-invariant DeepSets extraction, ArcFace extraction, gallery/probe linkage and verification metrics, leakage checks, and run artifacts.

The Month 1 single-template baseline is complete over three real datasets, six protocol variants, and three model seeds. It found no useful recovery under independent unseen keys and strong positive fixed-transform calibrations. The 64/128/256-bit sweep was also null. Synthetic data is excluded from this conclusion.

The authorized MOBIO face data is prepared locally. A preregistered exploratory 1/2/5/10 run completed on 2026-09-04 with mean pooling, max pooling, and DeepSets. It detected no amplification under independent unseen keys: the one-exposure reference was `4.17%` top-1 versus `3.33%` chance, and all 10-exposure models were exactly at chance. Shared-key and unprotected controls were strong. This is a useful negative finding, not a breakthrough or irreversibility proof; confirmation across new protocol/key seeds and another protection scheme is required. Exact `benchmark_cb` claims remain blocked by its unavailable source.
