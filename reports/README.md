# Research package

## Start here

- [Current evidence and submission gates](final_research_status.md)
- [Working manuscript](paper_draft.md)
- [Figure index, captions, and regeneration commands](figures/README.md)
- [Eight-slide PDF](slides/research_review.pdf)
- [Editable review deck](slides/research_review.pptx)
- [Cross-study key-pool table](../experiments/cross_dataset_key_pool_summary.csv)
- [Research roadmap](../docs/ROADMAP.md)

## File ownership

| Folder | Contents |
|---|---|
| `src/biometrics_ai/` | Reusable data, protection, attack, and evaluation code |
| `scripts/` | Dataset preparation, experiments, diagnostics, and figure builders |
| `configs/` | Versioned experiment and protection settings |
| `tests/` | Synthetic fixtures, numerical checks, and artifact validation |
| `experiments/` | Shareable compact results and study-specific interpretation |
| `docs/` | Protocols, approvals, source reviews, setup instructions, and research log |
| `reports/figures/` | Generated vector PDFs and PNG previews; source in `scripts/figures/` |
| `reports/slides/` | Generated PDF and editable PowerPoint review package |
| `results/`, data folders, model folders | Ignored local artifacts; never stage biometric records or weights |

Existing paths are preserved so historical configurations and citations continue to work. Generated previews used only for quality checks stay under ignored `results/figure_audit/`. Pilots must remain separate from confirmatory evidence, including in figures and slides.

## Approval and access

On 2026-09-12 the user reported Sani's approval of paper-specified IoM-GRP and PolyProtect and authorized pilots first, with at most one hour of new local training in this session. No SCface or AgeDB access is available. Dataset acquisition and independent human scientific review remain external gates; a local audit cannot substitute for either.