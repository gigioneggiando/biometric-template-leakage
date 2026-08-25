# Research log

## 2026-08-25

- Task: initialized reproducible research repository from the master prompt.
- Sources checked: arXiv records for benchmark_cb and FaceLinkGen; official GaFaR, Arc2Face, MOBIO pages; official InsightFace repository.
- Commands: `git ls-remote` against official repositories; local environment inspection; synthetic tests pending.
- Result: GaFaR, InsightFace, Arc2Face commits resolved. The stated `https://github.com/otroshi/benchmark_cb` URL returned 404. No verified FaceLinkGen code release was found from the arXiv record.
- Decision: implement a labelled local engineering baseline while preserving exact reproduction as blocked by upstream/MOBIO access.
- Next: run unit/integration tests and synthetic smoke test; recover/confirm benchmark_cb source with authors before claiming a reproduction.

## 2026-08-25 (verification)

- Task: verified local implementation and staged synthetic pipeline.
- Commands: `python -m pytest`; `python scripts/diagnostics/system_info.py`; `python scripts/reproduce/run_smoke_test.py`.
- Result: five tests passed. CPU-only environment (PyTorch 2.11.0; CUDA unavailable to PyTorch). Synthetic 1/2/5/10 runs completed and artifacts were written under `results/`.
- Interpretation: no stable multi-exposure gain was observed in one small synthetic seed. This is expectedly weak engineering evidence and is not a real-data result or a test of the research hypothesis.
- Next: obtain authorized MOBIO and a corrected official benchmark_cb source; verify the FaceLinkGen PDF protocol before reproduction work.
