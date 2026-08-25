# MOBIO acquisition and preparation

Official source: <https://www.idiap.ch/en/scientific-research/data/mobio>. MOBIO is accessed through Idiap's registration/license process; this repository neither downloads it nor contains it.

After approval and local download, set `MOBIO_ROOT` to the dataset root and run:

```powershell
python scripts/data/prepare_mobio.py --root $env:MOBIO_ROOT
```

The script validates the root, inventories files, computes a bounded checksum sample, and writes `data/manifest.json`. It does not alter or copy the dataset. The expected exact directory layout, subject/sample counts, preprocessing, and protocol index must be taken from the recovered benchmark_cb source; do not guess them from a generic MOBIO layout.

Troubleshooting: a missing root means authorization/download is incomplete; a successful manifest does not mean the benchmark protocol is prepared. Do not report LFW results as MOBIO results.
