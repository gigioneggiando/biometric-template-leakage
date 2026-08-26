# Proposed experiment readiness

Implemented now: deterministic key generation, a BioHash reference interface, identity/key-disjoint synthetic test data and real LFW/Olivetti/CFP protocols, single-template MLP and masked permutation-invariant DeepSets extraction, ArcFace extraction, gallery/probe linkage and verification metrics, leakage checks, and run artifacts.

The Month 1 single-template baseline is complete over three real datasets, six protocol variants, and three model seeds. It found no useful recovery under independent unseen keys and strong positive fixed-transform calibrations. The 64/128/256-bit sweep was also null. Synthetic data is excluded from this conclusion.

The proposed novelty claim remains untested. Month 2 is paused pending explicit approval; it must preregister 1/2/5/10 set construction, protocol seeds, aggregation baselines, and clustered statistical comparisons before running. MOBIO and exact `benchmark_cb` claims remain blocked separately.
