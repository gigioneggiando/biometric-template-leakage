# Candidate template-protection selection

**Decision date:** 2026-09-10  
**Status:** paper, source, license, and implementation-fit review complete; selection proposed, not yet approved  
**Scope:** two additional face-template protection families for the post-meeting multi-exposure study

**Dated update, 2026-09-12:** the user reported Sani's approval of both primaries. Paper-specified implementations and 16 MOBIO/FEI pilot cells are complete under the [frozen pilot protocol](../protocols/scheme_extension_pilot_2026-09-12.md); [results](../../experiments/scheme_extension_pilot/README.md) remain engineering diagnostics. This update supersedes the original proposed status without changing the historical review. Full confirmation, independent review and patent/commercial-use clearance are not implied.

## Recommendation

| Role | Scheme | Transformation family | Source status | Decision |
|---|---|---|---|---|
| Primary P1 | IoM-GRP | Gaussian random projections followed by index-of-maximum categorical hashing | Exact paper available; later face-oriented reference implementation available but unlicensed; included in `benchmark_cb` | Implement independently from the paper and classify as paper-specified, not source-exact |
| Primary P2 | PolyProtect | User-parameterized multivariate polynomial mapping of real-valued face embeddings | Exact paper and official Idiap reproduction repository identified; maintained GPL-3.0 Kotlin implementation with tests available | Implement independently from the paper; use the external implementation only for black-box behavioral checks if licensing permits |
| Backup | SWG-MinHash | Partial Walsh transformation plus sliding-window comparison/MinHash-style binary encoding | Python/ArcFace framework available under Apache-2.0 | Retain as backup until implementation defects and missing method tests are resolved |

The two primaries cover different output and transformation families: IoM-GRP produces categorical rank codes, while PolyProtect produces lower-dimensional real-valued polynomial templates. This is a stronger generalization than adding two more sign-threshold random projections.

## Selection requirements

Each scheme must:

- accept the existing fixed 512-dimensional ArcFace embeddings without retraining the face model;
- expose explicit per-record auxiliary data that can be assigned as fresh, shared, or drawn from a recurring pool;
- have a primary paper precise enough for an independent implementation;
- produce a fixed-format representation usable by the existing set attackers;
- support deterministic reproduction from a stored non-secret seed identifier;
- have matching and protection-utility checks independent from the leakage attacker;
- fit the RTX 2060 experiment budget without a new large-scale training corpus.

## Primary P1: IoM-GRP

**Primary paper:** Z. Jin et al., *Ranking-Based Locality Sensitive Hashing-Enabled Cancelable Biometrics: Index-of-Max Hashing*, IEEE TIFS 13(2), 2018, DOI [10.1109/TIFS.2017.2753172](https://doi.org/10.1109/TIFS.2017.2753172). An author-posted version is available on [arXiv](https://arxiv.org/abs/1703.05455).

### Transformation

For an embedding dimension `d`, code length `m`, and group width `q`, a key defines `m*q` Gaussian projection vectors. The projected values are reshaped into `m` groups of size `q`; the protected code stores the argmax index from each group. Two codes are normally compared by the number or fraction of matching indices.

For this project:

- key material: the Gaussian projection matrix;
- fresh condition: an independently seeded matrix per record;
- shared condition: one matrix for all relevant records;
- recurring-pool condition: one of `k` fixed matrices assigned under the frozen allocation rule;
- protected representation for matching: integer indices in `[0, q)`;
- attacker input: one-hot encoding with shape `m*q`, not raw integer indices, so the attacker is not given an artificial ordinal distance between categories.

### Why select it

- It is a widely cited cancelable-biometric construction with a simple, auditable algorithm.
- `benchmark_cb` applies IoM-GRP to deep templates and reports face/MOBIO targets, so it connects the extension to the paper under study.
- It is scale-invariant and materially different from BioHash's sign bits.
- A later face-template cryptanalysis repository contains a PyTorch implementation derived from the paper pseudocode and applies GRP/URP-IoM to face embeddings. This is useful for cross-checking behavior.

### Limitations and source classification

- The original IoM paper evaluates fingerprint features, not ArcFace. Its use on deep face templates comes from later work, including `benchmark_cb`.
- No licensed implementation from the original authors was located.
- The reference implementation at <https://github.com/Cryptology-Algorithm-Lab/Analysis_LSH> has no license file at commit `6225f119726bc1c0711a37a5dffccf4325cb7f53`; its code must not be copied into this MIT repository.
- The missing `benchmark_cb` source prevents parameter-exact reproduction of its MOBIO IoM-GRP result.

The local implementation must therefore be labelled **paper-specified IoM-GRP**. It must be written independently from the published algorithm and tested against hand-computed examples.

### Initial parameter gate

Do not choose `m` and `q` from convenience alone. Extract the parameter grid from the IoM paper and `benchmark_cb` TeX, then preregister one primary setting and a compact sensitivity sweep. Verify code entropy, category occupancy, same-key genuine matching, different-key unlinkability, and memory cost of the one-hot attacker representation.

## Primary P2: PolyProtect

**Primary paper:** V. Krivokuca Hahn and S. Marcel, *Towards Protecting Face Embeddings in Mobile Face Verification Scenarios*, IEEE TBIOM 4(1), 2022, DOI [10.1109/TBIOM.2022.3140472](https://doi.org/10.1109/TBIOM.2022.3140472). The [Idiap publication record](https://publications.idiap.ch/publications/show/4770) links the paper and reproduction source.

**Source references:** official Idiap repository <https://gitlab.idiap.ch/bob/bob.paper.polyprotect_2021> and maintained GPL-3.0 Kotlin implementation <https://github.com/Simprints/Biometrics-SimPolyProtect>.

### Transformation

PolyProtect divides an ordered real-valued embedding into overlapping windows. Each output element is a sum of window elements raised to secret exponents and multiplied by secret non-zero coefficients. Its principal parameters are polynomial degree/window size `m`, overlap `o`, coefficient range, the coefficient vector, and a permutation of exponents.

For this project:

- key/auxiliary material: coefficient and exponent vectors;
- fresh condition: new independently generated valid coefficient/exponent vectors per record;
- shared condition: one vector pair for all relevant records;
- recurring-pool condition: one of `k` valid vector pairs assigned under the frozen allocation rule;
- protected representation: real-valued vector whose dimension depends on `m`, `o`, and input dimension;
- attacker input: the protected vector after only the normalization explicitly preregistered from training data.

### Why select it

- It was designed specifically for ordered neural-network face embeddings.
- It adds a nonlinear polynomial family rather than another binary projection.
- It is lightweight and requires no face-model retraining.
- The authors evaluate recognition, irreversibility, and unlinkability under a fully informed attacker, while the present experiment adds a different key-blind multi-record threat model.
- The maintained Kotlin implementation contains focused tests for auxiliary-data generation, transformation, dimensions, and similarity scoring.

### Limitations and source classification

- The official Idiap GitLab page was indexed and is referenced by the paper, but direct Git/HTTPS access timed out during the 2026-09-10 audit. Record an exact commit and license only after it becomes reachable.
- The accessible Simprints implementation is GPL-3.0 at commit `535bdd2c886af2d02f03ac12296ba01196cfdd34`. Its source cannot be copied into this MIT repository without resolving license compatibility.
- Its Gradle tests could not be executed on the audit machine because the Android SDK was not installed. This is an environment blocker, not a reported test failure.
- PolyProtect's original verification setting normally reuses the same auxiliary data for enrollment and query. Fresh per-record auxiliary data are an intentional extension for our leakage threat model and must not be presented as an original-paper protocol.

The local implementation must be labelled **paper-specified PolyProtect with a new multi-exposure key-allocation protocol**.

### Initial parameter gate

Start from paper-supported `m`, `o`, coefficient, and exponent policies. Before attack training, verify output scale and finite values, same-key utility, different-key score separation, protected dimension, coefficient/exponent uniqueness, and sensitivity to overlap. Fit any scaler only on training identities and report results with and without scaling if scaling materially changes leakage.

## Backup: SWG-MinHash

The 2025 partial-Walsh/sliding-window scheme is accompanied by <https://github.com/shuaichaosong/cbef>, an Apache-2.0 Python framework that accepts 512-dimensional ArcFace vectors. Commit `686c31f76dc10ff955def2650156684350c6d8ed` was audited.

It is promising but not a primary choice yet:

- 21 method/verification/metric tests passed locally;
- the full test collection failed because `experiment/base_experiment.py` imports `cv2`, which is absent from the declared requirements;
- the SWG implementation itself has no dedicated unit test in the repository;
- it mutates NumPy's global random seed and contains unused imports and encoding-damaged comments;
- the paper and source need a line-by-line parameter and algorithm consistency check.

It can replace a primary scheme if PolyProtect access/licensing or IoM parameter recovery blocks progress, after an independent validation suite is added.

## Alternatives reviewed

| Scheme | Decision | Reason |
|---|---|---|
| Bloom-filter face BTP | Defer | The available academic implementation is tied to LGBPHS features and the FERET protocol, not ArcFace embeddings. An ArcFace port would be a conceptual adaptation, not source-exact reproduction. |
| IoM-URP | Backup | Closely related to IoM-GRP and therefore adds less family diversity; its product/permutation construction also needs more numerical and parameter validation. |
| IronMask | Defer | Strong face-specific CVPR work and directly compatible with angular face templates, but no original-author implementation was located and the real-valued ECC/isometry protocol is substantially more complex. |
| SecureTL | Defer | MIT-licensed official face code exists, but it retrains/adapts the recognition model end to end. That changes the fixed-ArcFace architecture and adds a separate training-dataset requirement. |
| SecureVector / encrypted matching | Out of current scope | It protects matching cryptographically rather than exposing a keyed cancelable template with the same fresh/reuse semantics. |
| SWG-MinHash | Backup | Licensed, Python, and ArcFace-compatible, but the audited repository needs repairs and scheme-specific tests before scientific use. |

## Implementation order

1. Obtain Sani's approval for paper-specified IoM-GRP and PolyProtect.
2. Extract and record the exact primary hyperparameter settings before coding.
3. Implement IoM-GRP independently with hand-computed, determinism, key-separation, entropy, and matching tests.
4. Run a synthetic and MOBIO/LFW smoke pilot before combining IoM-GRP with new datasets.
5. Implement PolyProtect independently and cross-check only output dimensions and fixed examples against an authorized external reference.
6. Run the same utility and key-scope gates.
7. Freeze one-record and ten-record pilots across FEI and one existing dataset before starting the full Cartesian matrix.

No source-exact claim is permitted unless the exact upstream implementation, commit, license, configuration, and output agreement are established.

## Sources checked

All sources were checked on 2026-09-10:

- IoM-GRP paper: <https://arxiv.org/abs/1703.05455>
- IoM-GRP bibliographic record and DOI: <https://research.monash.edu/en/publications/ranking-based-locality-sensitive-hashing-enabled-cancelable-biome/>
- Later face/IoM reference implementation: <https://github.com/Cryptology-Algorithm-Lab/Analysis_LSH>
- PolyProtect paper and official source record: <https://publications.idiap.ch/publications/show/4770>
- PolyProtect technology page: <https://technology.idiap.ch/technologies/biometrics/polyprotect/>
- Maintained PolyProtect implementation: <https://github.com/Simprints/Biometrics-SimPolyProtect>
- Bloom-filter research code: <https://dasec.h-da.de/research/biometrics/multibiometric-bf-btp/>
- IronMask paper: <https://openaccess.thecvf.com/content/CVPR2021/html/Kim_IronMask_Modular_Architecture_for_Protecting_Deep_Face_Template_CVPR_2021_paper.html>
- SecureTL: <https://github.com/jtrpinto/SecureTL>
- SWG-MinHash/CBEF: <https://github.com/shuaichaosong/cbef>
