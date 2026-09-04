# Multi-exposure protocol

An exposure is one independently protected representation under an independent key. The main condition samples different images of the same identity and assigns a different key to each; the controlled condition holds the image fixed and varies only keys. These conditions must be reported separately.

Attack training, validation, and testing use identity-disjoint partitions. Keys are also split: every test key is absent from training. Evaluation reports four diagnostic cells: seen identities/seen keys, unseen identities/seen keys, seen identities/unseen keys, and unseen identities/unseen keys. The last is the main key-agnostic claim. Exposure counts are 1, 2, 5, and 10, with mean/max/DeepSets/attention comparisons planned after validated baselines.

## MOBIO preregistration (2026-09-04)

The first real-data multi-exposure run is an independent engineering study, not a `benchmark_cb` reproduction. It uses the fixed `mobio_multiexposure_protocol.csv`: 150 identities, 12 distinct sessions per identity, seed `20260904`, and 90/30/30 train/validation/test identities. The one failed detection is excluded before set construction.

For every identity, the lowest available `sample_index` is a gallery image and is never an attack exposure or training target. The remaining images form the exposure pool. Eight deterministic permutations are generated per identity with set seed `20260904`; exposure levels 1/2/5/10 use nested prefixes of each permutation. This yields 720/240/240 attack sets for train/validation/test at every exposure level. Repeated sets overlap and are treated as measurements clustered by identity, not independent subjects.

Each source image receives one fixed 128-bit BioHash generated with key seed `20260904`, its data split, and sample ID. Keys never cross identity splits. The primary condition uses different images and independent keys. A shared-key run is only a positive calibration and cannot support a key-agnostic claim. Same-image/different-key experiments are deferred and must be labelled separately.

The target for supervised attack training is the L2-normalized mean ArcFace embedding of the images in that exposure set. Evaluation compares each predicted embedding with the held-out gallery image for all 30 test identities. Models are mean-pool MLP, max-pool MLP, and DeepSets; the one-exposure MLP is the common level-1 reference. Hidden dimension is 256, learning rate `0.001`, weight decay `0.0001`, cosine plus `0.1` MSE loss, at most 400 epochs, patience 60, and model seeds 7/17/27.

Report top-1/top-5 linkage, AUROC, EER, TAR at FAR `1e-2` and `1e-3`, target cosine, normalized L2, and 2,000-resample identity-clustered 95% intervals. The primary descriptive endpoint is DeepSets top-1 linkage at 10 exposures versus the common one-exposure MLP under independent unseen keys. Evidence of exposure amplification requires the 10-exposure clustered interval to exclude 30-way chance (`3.33%`) and an absolute mean top-1 increase of at least five percentage points over level 1. This first run is exploratory; confirmation requires new protocol/key/model seeds.

## MLP-Hash cross-scheme preregistration (2026-09-04)

The cross-scheme confirmation repeats the MOBIO 1/2/5/10 study using MLP-Hash, fixed key/set seed identifier `20260911`, and model seeds 37/47/57. The seed identifier is not an execution date. It retains the same identity split and held-out-gallery design to isolate protection-scheme effects. The primary endpoint and five-point amplification threshold are unchanged; this is a cross-scheme robustness test, not an independent dataset replication.

The implementation follows the public MLP-Hash paper: three ReLU hidden layers of width 1024 for 512-D ArcFace input, a 512-bit output, key-seeded random semi-orthogonal projections, and output-mean binarization. The paper says each projection is row-orthonormal, which is impossible for its narrowing 1024-to-512 output layer. We therefore use orthonormal rows when widening and orthonormal columns when narrowing. The authors' stated GitLab source was unavailable at preregistration, so results must be labelled `paper-specified, not source-exact`.

## System-key-pool boundary preregistration (2026-09-04)

The boundary study tests the multiplicity-invariance assumption that keys are fresh and independent. It uses BioHash, the fixed MOBIO identity split, key seed 90431, set seed 90437, model seeds 67/77/87, and the unchanged 1/2/5/10 exposure construction and training settings. No architecture or threshold is selected from boundary results.

Globally recurring hidden transform pools contain 1, 2, 5, or 10 keys. A source record receives key `sample_index mod pool_size`, so each transform recurs across training, validation, and test identities while its value remains hidden from the attack model. The fresh independent unseen-key condition is rerun as the endpoint control. This is a seen-transform deployment-misconfiguration threat model, not evidence against the fresh unseen-key proposition.

The primary descriptive curve is 10-record mean-pool top-1 versus key-pool size, ending at fresh keys. Evidence that key reuse breaks the ideal guarantee requires a recurring-pool identity-clustered interval above `3.33%` chance and an absolute top-1 increase of at least five points over the fresh-key endpoint. Mean/max/DeepSets and lower exposure counts are secondary diagnostics.

## Randomized key-pool confirmation preregistration (2026-09-04)

The first boundary result assigns transforms by `sample_index mod pool_size`, which may confound key recurrence with session ordering. Before inspecting a randomized result, a confirmation was fixed with key seed 90503, set seed 90509, model seeds 97/107/117, and the same pools, exposure levels, models, metrics, and success criterion. Each sample is assigned reproducibly to a pool slot by hashing its sample ID with a separate assignment scope. This breaks the session-to-key mapping while retaining system-wide recurrence across identity splits.
