# Proposed experiment readiness

Implemented now: deterministic key generation, a BioHash reference interface, identity/key-disjoint synthetic test data and real LFW/Olivetti/CFP/MOBIO protocols, single-template MLP and masked permutation-invariant DeepSets extraction, ArcFace extraction, gallery/probe linkage and verification metrics, leakage checks, and run artifacts.

The Month 1 single-template baseline is complete over three real datasets, six protocol variants, and three model seeds. It found no useful recovery under independent unseen keys and strong positive fixed-transform calibrations. The 64/128/256-bit sweep was also null. Synthetic data is excluded from this conclusion.

The authorized MOBIO face data is prepared locally. Preregistered 1/2/5/10 runs with BioHash and paper-specified MLP-Hash both detected no amplification under independent unseen keys. BioHash changed from `4.17%` at one record to `3.33%` for 10-record DeepSets; MLP-Hash changed from `2.50%` to `3.33%`, against `3.33%` chance. AUROC remained near `0.5`, while shared-key and unprotected controls were strong.

The resulting paper direction combines a scoped multiplicity-invariance result with a positive deployment boundary. For fixed-norm embeddings protected by independent hidden rotationally invariant projections, fresh-key multiplicity cannot restore identity information. In a sample-randomized confirmation, 10-record mean-pool top-1 remained `77.50%/69.44%/46.94%` for recurring pools of 1/2/5 hidden transforms, then fell to `5.56%` for pool 10 and fresh keys. This identifies a severe small-pool reuse regime while rejecting the stronger all-pools claim. Exact `benchmark_cb` claims remain blocked by its unavailable source.
