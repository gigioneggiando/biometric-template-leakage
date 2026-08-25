# Template protection protocol

The runnable local `biohash_reference` configuration projects an L2-normalized embedding through a key-derived orthonormal matrix and binarizes at zero. Key identifiers are deterministically derived from `master_seed`, split name, and exposure index. They are independent across train/validation/test scopes and are saved only as experiment metadata.

This is a controlled reference implementation for the proposed pipeline. It is **not** asserted to be parameter-equivalent to the benchmark_cb BioHash implementation until its upstream source/commit is recovered. Protected binary vectors are fed to the attacker as floating `0/1` values; matching semantics for a benchmark reproduction must instead follow upstream exactly.
