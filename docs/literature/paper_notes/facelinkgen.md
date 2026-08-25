# FaceLinkGen

The 2026 arXiv abstract describes identity extraction from PPFR representations for linkage/matching and optional regeneration, arguing that pixel reconstruction scores are insufficient privacy evidence. It reports results across PartialFace, MinusFace, and FracFace and describes a near-zero-knowledge condition.

No official FaceLinkGen repository was verified in this audit. The master prompt's listed CASIA-WebFace, LFW, TPDNE, Antelopev2/ArcFace-compatible teacher, and optional Arc2Face must be checked against the PDF before implementation. The core transferable idea is a student aligned to a teacher identity space evaluated on held-out identities; regeneration is explicitly non-blocking.

Arc2Face has a public MIT implementation at `foivospar/Arc2Face`, but it requires separately acquired Hugging Face/antelopev2 assets and a CUDA Stable Diffusion setup.
