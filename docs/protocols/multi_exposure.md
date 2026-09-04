# Multi-exposure protocol

An exposure is one independently protected representation under an independent key. The main condition samples different images of the same identity and assigns a different key to each; the controlled condition holds the image fixed and varies only keys. These conditions must be reported separately.

Attack training, validation, and testing use identity-disjoint partitions. Keys are also split: every test key is absent from training. Evaluation reports four diagnostic cells: seen identities/seen keys, unseen identities/seen keys, seen identities/unseen keys, and unseen identities/unseen keys. The last is the main key-agnostic claim. Exposure counts are 1, 2, 5, and 10, with mean/max/DeepSets/attention comparisons planned after validated baselines.

## MOBIO preregistration (2026-09-04)

The first real-data multi-exposure run is an independent engineering study, not a `benchmark_cb` reproduction. It uses the fixed `mobio_multiexposure_protocol.csv`: 150 identities, 12 distinct sessions per identity, seed `20260904`, and 90/30/30 train/validation/test identities. The one failed detection is excluded before set construction.

For every identity, the lowest available `sample_index` is a gallery image and is never an attack exposure or training target. The remaining images form the exposure pool. Eight deterministic permutations are generated per identity with set seed `20260904`; exposure levels 1/2/5/10 use nested prefixes of each permutation. This yields 720/240/240 attack sets for train/validation/test at every exposure level. Repeated sets overlap and are treated as measurements clustered by identity, not independent subjects.

Each source image receives one fixed 128-bit BioHash generated with key seed `20260904`, its data split, and sample ID. Keys never cross identity splits. The primary condition uses different images and independent keys. A shared-key run is only a positive calibration and cannot support a key-agnostic claim. Same-image/different-key experiments are deferred and must be labelled separately.

The target for supervised attack training is the L2-normalized mean ArcFace embedding of the images in that exposure set. Evaluation compares each predicted embedding with the held-out gallery image for all 30 test identities. Models are mean-pool MLP, max-pool MLP, and DeepSets; the one-exposure MLP is the common level-1 reference. Hidden dimension is 256, learning rate `0.001`, weight decay `0.0001`, cosine plus `0.1` MSE loss, at most 400 epochs, patience 60, and model seeds 7/17/27.

Report top-1/top-5 linkage, AUROC, EER, TAR at FAR `1e-2` and `1e-3`, target cosine, normalized L2, and 2,000-resample identity-clustered 95% intervals. The primary descriptive endpoint is DeepSets top-1 linkage at 10 exposures versus the common one-exposure MLP under independent unseen keys. Evidence of exposure amplification requires the 10-exposure clustered interval to exclude 30-way chance (`3.33%`) and an absolute mean top-1 increase of at least five percentage points over level 1. This first run is exploratory; confirmation requires new protocol/key/model seeds.
