# Figures

All plots are generated from tracked compact result files; nothing is transcribed by hand. Regenerate with:

```powershell
.\.venv\Scripts\python.exe scripts\figures\build_cross_dataset_table.py
.\.venv\Scripts\python.exe scripts\figures\make_figures.py
.\.venv\Scripts\python.exe scripts\figures\make_diagrams.py
```

| File | Content | Source data |
|---|---|---|
| `fig_architecture` | Pipeline: image, detection/alignment, ArcFace, keyed protection, multi-record set, key-blind attacker, gallery linkage | - |
| `fig_threat_model` | Three key regimes (fresh, recurring pool of k, single shared key) and the evaluation protocol | - |
| `fig_pool_curves` | (a) chance-normalized 10-record top-1 vs pool size for MOBIO (4 partitions), LFW, FEI; (b) MLP-Hash on MOBIO with 1-record curve and clustered-interval band | `experiments/*/key_pool*_summary.csv`, `dense_key_pool_sweep*_summary.csv`, `mlphash_key_pool*_summary.csv` |
| `fig_amplification` | 1-record vs 10-record chance-normalized top-1 per condition; filled = recurring pool, hollow = fresh keys | same as above |
| `fig_pooled_boundary` | MOBIO pooled curve over three identity partitions with per-pool pass counts | `dense_key_pool_pooled_analysis.csv` |
| `fig_controls` | (a) slot-known vs hidden vs shuffled-record controls; (b) partial projection-sharing sweep | `mobio_mechanism_controls`, `mobio_correlation_controls` |
| `fig_fresh_exposures` | Fresh-key vs shared-key top-1 as a function of records per person, BioHash and MLP-Hash | `results_summary.csv`, `mlphash_results_summary.csv` |

PDF (vector, Type 42 fonts) and PNG (220 dpi) are both written. The canonical cross-dataset table used for the text is `experiments/cross_dataset_key_pool_summary.csv`.
