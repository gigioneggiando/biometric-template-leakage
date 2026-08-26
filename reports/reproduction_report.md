# Reproduction report

## benchmark_cb

- Citation: Shahreza et al., *Benchmarking of Cancelable Biometrics for Deep Templates*, arXiv:2302.13286; DOI `10.1186/s13640-025-00679-y`.
- Level: **NOT REPRODUCIBLE YET**.
- Exact code/data: no verified upstream commit; MOBIO not locally authorized.
- Published targets verified from official arXiv TeX: ArcFace/MOBIO unprotected EER `0.02%`; BioHash EER `0.02%` normal and `0.04%` stolen-token; BioHash MI `39.63` normal and `98.81` stolen-token.
- Our benchmark result: `TODO / not run`.
- Lesson: do not substitute LFW or a local BioHash variant for the exact MOBIO benchmark.

## FaceLinkGen

- Citation: Guo and Du, *FaceLinkGen*, arXiv:2602.02914 (2026).
- Level: **NOT REPRODUCIBLE YET**.
- Exact code/data: no verified official code; paper details require extraction before direct implementation.
- Published/our result: abstract reports matching/regeneration figures; local result is `TODO / not run`.

## Engineering validation

`make smoke-test` runs the synthetic pipeline for plumbing only. The completed Month 1 real-image single-template baseline covers LFW, Olivetti, and CFP. Independent unseen-key results remained compatible with chance across dataset, detector, pose, sample-size, template-dimension, and crossed identity/key/model seed checks, while fixed-transform calibrations learned strong identity signal. These are **CONCEPTUAL/ENGINEERING VALIDATION**, not publication reproductions or substitutes for MOBIO.
