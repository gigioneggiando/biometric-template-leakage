# Multi-exposure protocol

An exposure is one independently protected representation under an independent key. The main condition samples different images of the same identity and assigns a different key to each; the controlled condition holds the image fixed and varies only keys. These conditions must be reported separately.

Attack training, validation, and testing use identity-disjoint partitions. Keys are also split: every test key is absent from training. Evaluation reports four diagnostic cells: seen identities/seen keys, unseen identities/seen keys, seen identities/unseen keys, and unseen identities/unseen keys. The last is the main key-agnostic claim. Exposure counts are 1, 2, 5, and 10, with mean/max/DeepSets/attention comparisons planned after validated baselines.
