# Figures

All plots are generated from tracked compact result files; nothing is transcribed by hand. Regenerate with:

```powershell
.\.venv\Scripts\python.exe scripts\figures\build_cross_dataset_table.py
.\.venv\Scripts\python.exe scripts\figures\make_figures.py
.\.venv\Scripts\python.exe scripts\figures\make_diagrams.py
.\.venv\Scripts\python.exe scripts\figures\make_presentation.py
```

| File | Content | Source data |
|---|---|---|
| `fig_architecture` | Pipeline: image, detection/alignment, ArcFace, keyed protection, multi-record set, key-blind attacker, gallery linkage | - |
| `fig_threat_model` | Three key regimes (fresh, recurring pool of k, single shared key) and the evaluation protocol | - |
| `fig_results_overview` | All 65 conditions from 11 completed key-pool studies; one-record and ten-record top-1; missing endpoints and interval failures explicit | `experiments/cross_dataset_key_pool_summary.csv` |
| `fig_pool_curves` | (a) chance-normalized 10-record top-1 for MOBIO, LFW, FEI; (b) separate initial/dense MLP-Hash studies with seed-SD bars | `experiments/*/key_pool*_summary.csv`, `dense_key_pool_sweep*_summary.csv`, `mlphash_key_pool*_summary.csv` |
| `fig_amplification` | 1-record vs 10-record chance-normalized top-1 per condition; filled = recurring pool, hollow = fresh keys | same as above |
| `fig_pooled_boundary` | MOBIO pooled curve over three identity partitions with per-pool pass counts | `dense_key_pool_pooled_analysis.csv` |
| `fig_controls` | (a) slot-known vs hidden vs shuffled-record controls; (b) partial projection-sharing sweep; (c) same-image fresh-key control | `mobio_mechanism_controls`, `mobio_correlation_controls` |
| `fig_fresh_exposures` | Fresh-key vs shared-key top-1 as a function of records per person, BioHash and MLP-Hash | `results_summary.csv`, `mlphash_results_summary.csv` |
| `fig_scheme_pilots` | One-seed MOBIO/FEI IoM-GRP and PolyProtect linkage, single/mean/DeepSets, with clustered 95% intervals | `experiments/scheme_extension_pilot/results_summary.csv` |
| `fig_pilot_uncertainty` | Paired ten-minus-one mean-pool gains and 95% identity-bootstrap intervals | `experiments/scheme_extension_pilot/paired_uncertainty.csv` |
| `fig_pilot_native_utility` | Separate protected-gallery matching diagnostic, including fresh PolyProtect discrepancy | `experiments/scheme_extension_pilot/native_utility.csv` |
| `fig_pilot_equivalence` | Fresh-key 90% interval sensitivity with illustrative +/-2-point band | `experiments/scheme_extension_pilot/equivalence_sensitivity.csv` |

PDF (vector, Type 42 fonts) and PNG (220 dpi) are both written. All diagram and plot exports reject overlapping text, clipped labels, and en/em dashes or Unicode minus characters. Diagram exports also check text padding inside boxes. These geometric checks supplement visual review, not scientific or professor approval.

## Captions and interpretation

**Architecture.** Source images are detected/aligned with YuNet, embedded with ArcFace and normalized, then protected under hidden keys. A supervised attacker learns from paired templates and embeddings of training identities and predicts an embedding from a set of protected records. Cosine linkage uses a held-out gallery of test identities. The four schemes produce binary, categorical or real-valued templates; not every scheme has been run on every dataset. Icons and bit patterns are original schematic primitives, not face data or measured templates.

**Key regimes.** Fresh keys are unique to source records and disjoint across splits. Recurring pools reuse hidden transforms across identity splits; a shared key is the k=1 case, not a known-key attack. Colours identify transforms schematically. The idealized invariance proposition additionally requires rotational invariance and source-independent postprocessing; chance-compatible experiments do not prove privacy.

**All-study overview.** Cells show absolute top-1 percentages, averaged over three model seeds. Colour uses `(top1 - chance) / (1 - chance)` to account descriptively for gallery size, not to equate dataset difficulty. Grey cells are untested or unavailable in compact sources. An asterisk means not all seed-level clustered lower bounds strictly exceed chance; it is not an equivalence verdict or the full preregistered pass rule. Rows are individual source studies: initial/dense MLP-Hash and session-aligned/random assignment are not merged. Both earliest BioHash compact summaries lack one-record endpoints. This overview covers key-pool studies, not single-template engineering validation or every control; the supporting figures cover the remaining multi-exposure studies.

**Pool curves and amplification.** Lines join conditions within a source study only and do not imply monotonicity or interpolation evidence. MLP-Hash bars show SD across model seeds, not an identity-level confidence interval. The amplification plot is descriptive; paired uncertainty remains to be added. Filled markers denote recurring pools; hollow markers denote fresh keys. Chance ratios can differ simply because gallery sizes differ.

**Pooled boundary.** Shading is the observed minimum/maximum across available partition studies, not a confidence band. Pool 5 has two partitions; the other displayed pools have three. Labels give the number of partitions passing the interval criterion over the number available. Failure to pass does not establish a null regime.

**Controls.** Slot-known attacks receive transform identifiers, not secret transform values. Hidden/known use DeepSets; shuffled-non-anchor uses mean pooling and is a separate control. Correlation studies share projection columns; coarse and fine sweeps have different partitions. The same-image control holds the input embedding fixed while varying fresh keys. Chance is 1/30.

**Fresh exposure curves.** Values are the maximum observed seed-mean top-1 over tested attacker architectures at each exposure, including the shared-key curves. This is a descriptive envelope selected using test performance, not a validation-selected deployable attacker or unbiased primary endpoint.

## Review package

**New pilots.** The four added plots describe one model seed per endpoint, with a 120-epoch cap, not a controlled ranking against earlier three-seed studies. Paired intervals condition on that seed/partition and are not multiplicity-adjusted. Fresh points are disconnected from finite-pool curves. Native utility uses a protected gallery and different probes; its PolyProtect fresh-key result needs separate investigation. The shaded equivalence band is illustrative, not approved; no +/-1-point endpoint passes. See the [pilot report](../../experiments/scheme_extension_pilot/README.md).

The [complete figure appendix](../slides/figure_appendix.pdf) collects all 12 current vector figures. The 65-condition overview covers earlier studies only; pilot plots remain separate.

[Eight-slide PDF](../slides/research_review.pdf) and [editable PowerPoint](../slides/research_review.pptx) are generated together. Native slide text/tables are editable; figure panels are embedded PNGs with editable Python sources and separate vector PDFs. No FEI or MOBIO photographs are included. PowerPoint's native rendering should be checked on the presenting machine; the matching PDF has automated text-region and nonblank-page checks.

Install optional tools with `python -m pip install -e ".[presentation]"`. Run `python -m pytest tests/unit/test_figures.py -q` to validate source preservation, metric ranges, table freshness, figure layout, and slide/PDF export. A separate [per-seed inventory](../../experiments/multiexposure_run_matrix.csv) now covers 633 locally available rows, but full historical reconciliation and migration of all plots remain pending. Rebuild it with `python scripts/figures/build_run_matrix.py` only when the private source artifacts are available.
