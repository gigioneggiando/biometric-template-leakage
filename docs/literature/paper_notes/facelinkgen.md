# FaceLinkGen

Current source: [arXiv 2602.02914v3](https://arxiv.org/html/2602.02914v3), 3 September 2026, Wenqi Guo, Mohamed Shehata and Shan Du. Title: *FaceLinkGen: A Re-evaluation of Identity Leakage in Privacy-Preserving Face Recognition and Face Anonymization Systems Using Simple Distillation*. Paired original/protected examples train a student against a frozen ArcFace teacher. PPFR targets: MinusFace, PartialFace, DecoyFace; De-ID: TIP-IM, PerceptFace, Protego, WDP. V3 excludes FracFace because of paper/code inconsistency. Older local v1 descriptions are not the current specification.

No official FaceLinkGen implementation was reproduced here. V3 PPFR uses MS1M with 30,000 training, 2,000 validation and 2,000 test identities; its De-ID study includes a 107,676-person gallery. These are not directly comparable to our 25-40-person galleries. Paired identity distillation and failure-of-fixed-attacks caveats are prior art. See the [versioned comparison](../closest_work_2026-09-18.md).

Arc2Face has a public MIT implementation at `foivospar/Arc2Face`, but it requires separately acquired Hugging Face/antelopev2 assets and a CUDA Stable Diffusion setup.
