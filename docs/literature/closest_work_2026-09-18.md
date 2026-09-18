# Closest-work comparison: 18 September 2026

## Defensible distinction

The candidate contribution is a **controlled hidden-transform-reuse study of learned same-person set linkage**, with identity-disjoint training, separate source images, fresh/shared/finite-pool conditions, mechanism controls, and corrected paired inference. Eight primary pool-4 mean-pooling contrasts improve from one to ten records. This combination distinguishes our experiment from the examined studies; it is not an exhaustive priority claim, a new protection scheme, or a head-to-head accuracy win.

| Work and inspected evidence | What was already shown | Our addition and limits |
|---|---|---|
| Li and Hu, 2014, [10.1002/cpe.3042](https://doi.org/10.1002/cpe.3042); publisher abstract/metadata | Cryptanalysis of four cancelable fingerprint schemes using multiple transformed templates **and corresponding transformation parameters**. | Hidden parameters, learned linkage and different face images. Multiple-record vulnerability itself is not new. Full attacks were not reimplemented. |
| PolyProtect, 2022, [accepted v3](https://arxiv.org/html/2110.00434v3), III, IV-A, IV-C3, IV-D | Polynomial protection; numerical inversion using 1-10 versions of the **same embedding**, fully disclosed parameters. Different-image pairwise linkage under naive random parameters, reduced by stricter score-conditioned parameter selection. | Hidden recurring system-wide pools and learned aggregation of different images. Our native result is not a new discovery of residual linkage or a refutation of the stricter recommended selection policy. |
| benchmark_cb, [preprint](https://arxiv.org/html/2302.13286v1), [journal](https://doi.org/10.1186/s13640-025-00679-y) | Recognition, score-based unlinkability and estimated mutual information across schemes/modalities; sample-specific keys for unlinkability and a stolen-key setting. | Learned one-to-ten contrasts under recurring hidden pools. Independent-key evaluation and cross-scheme benchmarking are not new. Published metrics are not interchangeable with our top-1. |
| Guo, Shehata and Du, FaceLinkGen, [v3, 3 September 2026](https://arxiv.org/html/2602.02914v3), sections 3-6 | Adaptive identity extraction using paired original/protected data and frozen ArcFace teacher distillation. Service-provider and De-ID threats with unknown per-query randomness. | Fixed keyed templates, controlled reuse and same-person set aggregation. Identity distillation and the warning that failed attacks do not prove privacy are prior art. No numerical superiority claim: galleries and data scale differ. |
| Jin et al., IoM, [1703.05455](https://arxiv.org/abs/1703.05455), [DOI](https://doi.org/10.1109/TIFS.2017.2753172) | GRP/URP ranking protection explicitly emphasizes magnitude independence. | Our natural-scale check validates local GRP code; scale invariance is not a new finding. |
| Otroshi Shahreza, Shkel and Marcel, 2024, [10.1109/ACCESS.2024.3433536](https://doi.org/10.1109/ACCESS.2024.3433536) | Metadata verifies prior work specifically on linkability of multiple protected templates using maximal leakage. | Full text was not verified in this revision. We do not claim it omits a specific setting or equate empirical top-1 with maximal leakage. |

## Corrections and boundaries

- The earlier Li/Hu DOI `10.1002/cpe.2999` identifies an unrelated semantic-association article. Correct: `10.1002/cpe.3042`, 26(8), 1593-1605; online 2013, print 2014.
- FaceLinkGen v3 is *FaceLinkGen: A Re-evaluation of Identity Leakage in Privacy-Preserving Face Recognition and Face Anonymization Systems Using Simple Distillation*. Authors: Wenqi Guo, Mohamed Shehata, Shan Du. Targets: MinusFace, PartialFace, DecoyFace; TIP-IM, PerceptFace, Protego, WDP. It excludes FracFace because of paper/code inconsistency. Earlier v1 notes are not the current specification.
- PolyProtect III/IV-A agree with local windows, zero padding, unique nonzero coefficients in [-50,50], and permuted exponents 1-5. Our 512-D ArcFace differs from its 128-D Facenet/Idiap inputs. We do not implement IV-D's stricter score-conditioned parameter selection.
- This is a source-grounded comparison and separate computational check, not independent human review or official-code interoperability certification. Global firstness is not established.

## Deployment assumptions

Persistent account/session pseudonyms could group retained enrollment or verification records without revealing the owner's real identity. Retention and stable grouping are assumptions, not measured prevalence in products.

Paired training data could come from an authorized enrollment/query interface using consented faces, or a service provider seeing source images and protected outputs. Crucially, recurring-pool training must query the **same realized hidden pool** later used for targets. A separate proxy with unrelated keys does not satisfy this assumption. Key values and slots are hidden; identities are split-disjoint, but recurring transforms deliberately are not.

A gallery could use lawful public or consented reference images. Ours is a small closed set of 25-40 people with guaranteed target membership and separate gallery images. Open-set search, internet-scale distractors, cross-provider transfer, unknown record grouping and real-product attack access are not demonstrated. Fresh independent transforms can impair legitimate matching too; they are not a validated drop-in defense.