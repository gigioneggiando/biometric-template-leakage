# Approved scheme-extension pilot

Frozen 2026-09-12 before implementation and result inspection. The user reports Sani approved paper-specified IoM-GRP and PolyProtect. Authorization is for pilots first and at most one hour of new local training in this session, not the full confirmation matrix. No authorized SCface/AgeDB data are available.

## Sources and frozen settings

- IoM-GRP: Jin et al., DOI 10.1109/TIFS.2017.2753172, author paper at <https://arxiv.org/pdf/1703.05455>, GRP algorithm and timing table. Use 300 groups of 16 independent standard-Gaussian projections each, on 512-dimensional unit ArcFace embeddings. Native output: 300 zero-based categorical indices. Attacker input: 4,800-dimensional one-hot encoding. Ties use the first index. This adapts the paper's fingerprint setting to the existing face protocol; it is not a benchmark_cb reproduction.
- PolyProtect: Krivokuca Hahn and Marcel, DOI 10.1109/TBIOM.2022.3140472, Sections 3 and 4.1, official PDF at <https://publications.idiap.ch/attachments/papers/2022/Krivokuca_IEEET-BIOM_2022.pdf>. Use window size 5, overlap 2, unique nonzero integer coefficients sampled without replacement from [-50,50], and a random permutation of exponents 1-5. Reuse the coefficient/exponent vectors across windows; zero-pad only the incomplete final window. The 512-D input maps to 170 real values. Use raw protected values for the primary pilot, with no data-fitted scaler or per-record output normalization. This is a paper-specified algorithm with a new key-allocation and ArcFace protocol, not the original 128-D verification experiment.
- Implement independently from the papers. Do not copy unlicensed or GPL implementation code. Official technology material lists PolyProtect patents; research approval is not patent clearance or a commercial-use license.

## Functional and utility gates

Before training: deterministic same-key outputs; batch/single consistency; finite output; valid categories or polynomial dimensions; hand-computed projection/polynomial fixtures; fresh-key uniqueness and split separation; original algorithms unchanged. Check zero/degenerate templates, category occupancy or coordinate variance, and same-key native matching. Native utility uses categorical equality for IoM-GRP and cosine for PolyProtect. Different-key matching is a diagnostic, not proof of unlinkability. Reject nonfinite or entirely degenerate inputs before training.

## Pilot matrix

Use the existing authorized MOBIO and FEI embeddings and frozen identity splits. Per scheme and dataset, run fresh keys and randomized pools 1, 4, and 8, with 1/10 exposures, eight nested repeats, one model seed 419, single MLP at one exposure, and mean-pool MLP plus DeepSets at ten. Use key seed 91217, set seed 91219, hidden size 256, Adam learning rate .001, weight decay .0001, cosine plus .1 MSE, 120 maximum epochs, patience 30, and 2,000 identity-clustered bootstrap resamples. Save each completed cell; enforce a wall-clock deadline between runs. A partial matrix remains partial if the time budget expires. No automatic promotion to confirmation.

Retain per-identity top-1 scores privately for paired one-to-ten and fresh-to-reuse analysis. Publish only aggregate study/condition/exposure/model/seed metrics. Pilot results are engineering evidence for feasibility and design choices, not independent confirmation or new privacy guarantees. A weak learned reuse control is a reason for follow-up, not to reinterpret fresh-key failure as privacy.

## Inference and follow-up

Report paired identity-bootstrap differences and their 95% intervals, conditional on this one model seed. For fresh-key means, provide exploratory 90% interval containment within chance +/- 1, 2, and 5 percentage points. These margins are sensitivity values, not a scientifically approved equivalence margin. Do not claim population equivalence or privacy from a pilot; freeze a justified primary margin and familywise/multiple-comparison strategy before confirmation.

The broader confirmation requires new model seeds, 1/2/5/10 exposures, multiple identity assignments, and approved additional data. Its launch is outside this session's pilot budget. Independent human proof/novelty review remains open. In particular, PolyProtect Section 4.3 already studies record multiplicity with disclosed parameters; the candidate contribution must distinguish hidden parameter values and learned linkage from that prior work.