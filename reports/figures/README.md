# Figures

**Updated: 2026-09-18**, using integration `4352eeb` and the separately hash-frozen [MOBIO/FEI follow-up](../../experiments/scheme_followup_2026-09-18/README.md). Includes SCface (protocol freeze `69a93e4`), 73 earlier conditions / 12 source-separated studies, 24 one-seed scheme pilot cells, and 216 new multi-seed follow-up endpoints.

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
| `fig_attack_detail` | Nested exposure construction, pooling/DeepSets tensors and layers, training targets/loss, and held-out gallery linkage | - |
| `fig_threat_model` | Three key regimes (fresh, recurring pool of k, single shared key) and the evaluation protocol | - |
| `fig_results_overview` | All 73 conditions from 12 completed key-pool studies; one-record and ten-record top-1; missing endpoints and interval failures explicit | `experiments/cross_dataset_key_pool_summary.csv` |
| `fig_pool_curves` | (a) chance-normalized 10-record top-1 for MOBIO, LFW, FEI, SCface; (b) separate initial/dense MLP-Hash studies with seed-SD bars | `experiments/*/key_pool*_summary.csv`, `dense_key_pool_sweep*_summary.csv`, `mlphash_key_pool*_summary.csv` |
| `fig_amplification` | 1-record vs 10-record chance-normalized top-1 per condition; filled = recurring pool, hollow = fresh keys | same as above |
| `fig_pooled_boundary` | MOBIO pooled curve over three identity partitions with per-pool pass counts | `dense_key_pool_pooled_analysis.csv` |
| `fig_controls` | (a) slot-known vs hidden vs shuffled-record controls; (b) partial projection-sharing sweep; (c) same-image fresh-key control | `mobio_mechanism_controls`, `mobio_correlation_controls` |
| `fig_fresh_exposures` | Fresh-key vs shared-key top-1 as a function of records per person, BioHash and MLP-Hash | `results_summary.csv`, `mlphash_results_summary.csv` |
| `fig_scheme_pilots` | One-seed MOBIO/FEI/SCface IoM-GRP and PolyProtect linkage, single/mean/DeepSets, with clustered 95% intervals | `experiments/scheme_extension_pilot/results_summary.csv`, `experiments/scface_scheme_extension_pilot/results_summary.csv` |
| `fig_pilot_uncertainty` | Paired ten-minus-one mean-pool gains and 95% identity-bootstrap intervals | `experiments/scheme_extension_pilot/paired_uncertainty.csv`, `experiments/scface_scheme_extension_pilot/paired_uncertainty.csv` |
| `fig_pilot_native_utility` | Separate protected-gallery matching diagnostic, including fresh PolyProtect discrepancy | `experiments/scheme_extension_pilot/native_utility.csv`, `experiments/scface_scheme_extension_pilot/native_utility.csv` |
| `fig_pilot_equivalence` | Fresh-key 90% interval sensitivity with illustrative +/-2-point band | `experiments/scheme_extension_pilot/equivalence_sensitivity.csv`, `experiments/scface_scheme_extension_pilot/equivalence_sensitivity.csv` |
| `fig_followup_amplification` | Eight primary pool-4 paired gains, crossed model-seed/identity intervals and Holm-adjusted tests | `experiments/scheme_followup_2026-09-18/seed_identity_contrasts.csv` |
| `fig_followup_native_controls` | Native fresh PolyProtect permutation controls and separate synthetic radial sensitivity | `experiments/scheme_followup_2026-09-18/native_null_controls.csv`, `norm_sensitivity.csv` |
| `fig_native_norm_audit` | Genuine unit/raw/shuffled/fixed-radius native matching with conditional 95% intervals | `experiments/norm_native_audit_2026-09-18/native_norm_controls.csv` |
| `fig_followup_failures` | Uncertain pool-4 DeepSets gains and significant shared-key PolyProtect losses; post-hoc family 48 | `experiments/norm_native_audit_2026-09-18/failure_analysis.csv` |

PDF (vector, Type 42 fonts) and PNG (220 dpi) are both written. All diagram and plot exports reject overlapping text, clipped labels, and en/em dashes or Unicode minus characters. Diagram exports also check text padding inside boxes. These geometric checks supplement visual review, not scientific or professor approval.

## Captions and interpretation

**Architecture.** The [overview](fig_architecture.pdf) separates the data/protection path from attacker training and evaluation. Icons identify source identity, embedding, key, records, network and gallery. The companion [detailed attacker](fig_attack_detail.pdf) defines nested exposure construction, pooling and DeepSets branches, tensor dimensions, exact layers, normalized exposed-embedding mean targets, cosine-plus-MSE loss, optimizer and held-out gallery scoring. Both appear as separate pages in the September report. The four schemes produce binary, categorical or real-valued templates; not every scheme has been run on every dataset. Icons and bit patterns are original schematic primitives, not face data or measured templates. Vector PDFs are the publication sources.

**Key regimes.** Fresh keys are unique to source records and disjoint across splits. Recurring pools reuse hidden transforms across identity splits; a shared key is the k=1 case, not a known-key attack. Colours identify transforms schematically. The idealized invariance proposition additionally requires rotational invariance and source-independent postprocessing; chance-compatible experiments do not prove privacy.

**All-study overview.** Cells show absolute top-1 percentages, averaged over three model seeds. Colour uses `(top1 - chance) / (1 - chance)` to account descriptively for gallery size, not to equate dataset difficulty. Grey cells are untested or unavailable in compact sources. An asterisk means not all seed-level clustered lower bounds strictly exceed chance; it is not an equivalence verdict or the full preregistered pass rule. Rows are individual source studies: initial/dense MLP-Hash and session-aligned/random assignment are not merged. Both earliest BioHash compact summaries lack one-record endpoints. This overview covers key-pool studies, not single-template engineering validation or every control; the supporting figures cover the remaining multi-exposure studies.

**Pool curves and amplification.** Lines join conditions within a source study only and do not imply monotonicity or interpolation evidence. MLP-Hash bars show SD across model seeds, not an identity-level confidence interval. The amplification plot is descriptive; paired uncertainty remains to be added. Filled markers denote recurring pools; hollow markers denote fresh keys. Chance ratios can differ simply because gallery sizes differ.

**Pooled boundary.** Shading is the observed minimum/maximum across available partition studies, not a confidence band. Pool 5 has two partitions; the other displayed pools have three. Labels give the number of partitions passing the interval criterion over the number available. Failure to pass does not establish a null regime.

**Controls.** Slot-known attacks receive transform identifiers, not secret transform values. Hidden/known use DeepSets; shuffled-non-anchor uses mean pooling and is a separate control. Correlation studies share projection columns; coarse and fine sweeps have different partitions. The same-image control holds the input embedding fixed while varying fresh keys. Chance is 1/30.

**Fresh exposure curves.** Values are the maximum observed seed-mean top-1 over tested attacker architectures at each exposure, including the shared-key curves. This is a descriptive envelope selected using test performance, not a validation-selected deployable attacker or unbiased primary endpoint.

## Review package

**Historical pilots.** The four pilot plots describe one model seed per endpoint, with a 120-epoch cap, not a controlled ranking against earlier three-seed studies. Paired intervals condition on that seed/partition and are not multiplicity-adjusted. Fresh points are disconnected from finite-pool curves. Native utility uses a protected gallery and different probes; subsequent MOBIO/FEI null calibration appears in the follow-up, while SCface remains a one-seed diagnostic. The shaded equivalence band is illustrative, not approved; no +/-1-point endpoint passes. See the [MOBIO/FEI pilot report](../../experiments/scheme_extension_pilot/README.md) and the [SCface pilot report](../../experiments/scface_scheme_extension_pilot/README.md).

**Bounded follow-up.** The two follow-up plots summarize three model seeds and two overlapping identity partitions on MOBIO/FEI, under matched 120-epoch caps. All eight pool-4 primary paired gains have positive crossed 95% intervals and Holm p = 0.004. All 12 native permutation tests have Holm p = 0.006. Native matching uses a protected gallery, not the learned attack's gallery; radial stress measures synthetic scale sensitivity, not natural norm leakage. Training key/set seeds are fixed, partitions are not independent replications, and chance-compatible fresh endpoints do not establish equivalence.

**Raw-norm revision.** The [audit](../../experiments/norm_native_audit_2026-09-18/README.md) re-extracts 4,177 records and validates separate formula/matcher computations. The four-arm plot averages three fixed key seeds; intervals resample identities only. Native family 16 has Holm p = 0.0032, but paired raw-unit gains survive only on FEI and raw-shuffled differences do not. The failure plot is selected for interpretation from all 48 published contrasts, not a new primary family: eight pool-4 mean gains and four shared-key PolyProtect DeepSets losses survive two-sided Holm correction. Pointwise intervals are not simultaneous. No independent human review or identity-specific norm leakage is established.

The [complete figure appendix](../slides/figure_appendix.pdf) collects all 17 current vector figures. The 73-condition overview covers earlier studies only; pilot and follow-up plots remain separate.

The [14-page September update](../Sept_Dataset_Update.pdf) is generated by the same command as the deck, with a [plain-language page guide](../Sept_Dataset_Update_guide.md). It preserves vector diagrams and searchable labels; heatmap cells remain intentional raster layers. Retain current PNG/PDF pairs, editable deck and appendix; only stale local audit previews are disposable.

[Ten-slide PDF](../slides/research_review.pdf) and [editable PowerPoint](../slides/research_review.pptx) are generated together. Slide text/tables are editable; figures are PNGs with Python sources and separate vector PDFs. No biometric photographs are included. Native PowerPoint rendering needs a check on the presenting machine; matching PDFs have text-region and nonblank-page tests.

Install optional tools with `python -m pip install -e ".[presentation]"` (includes `pypdf` for vector page composition). Run `python -m pytest tests/unit/test_figures.py -q` to validate source preservation, metric ranges, table freshness, figure layout, and slide/report PDF export. A separate [per-seed inventory](../../experiments/multiexposure_run_matrix.csv) covers 849 rows from 49 locally available artifacts, including 48 MOBIO/FEI pilot and 216 follow-up endpoints but no SCface rows. All previous 633 rows were preserved exactly. The [coverage audit](../../experiments/scheme_followup_2026-09-18/coverage_audit.csv) identifies legacy-schema and unavailable-detail gaps; SCface aggregate CSVs feed figures directly. Full historical migration remains pending. A partial local scan must not silently erase historical coverage.
