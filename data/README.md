# Data handling

`raw/`, `interim/`, and `processed/` are ignored. Never commit biometric images, templates, model weights, or access credentials.

MOBIO is a manual-access dataset. Follow [MOBIO setup](../docs/setup/MOBIO.md), then run `python scripts/data/prepare_mobio.py --root <authorized-path>`.

LFW, Olivetti faces, and CFP are real-data engineering fallbacks and must never be reported as MOBIO or paper reproductions. Their downloaders verify available source artifacts before use:

- `python scripts/data/download_lfw.py` uses scikit-learn's documented funneled LFW fetcher.
- `python scripts/data/download_olivetti.py` verifies cache SHA-256 `47398b319d88c78459514b30b87c562313aad345b5c6a387b678d7f8177be4ba`.
- `python scripts/data/download_cfp.py` verifies official archive SHA-256 `666b87635e6af028177ac72a85f03099fac263baf09c21f333fa445f930f65b1` before extraction. The official host uses HTTP and the archive has no explicit license file, so the hash is mandatory and redistribution is not assumed.

Deterministic splits, failure handling, commands, and results are documented in [the Month 1 real-dataset protocol](../docs/protocols/real_datasets_month1.md). Synthetic identities remain useful for tests but are excluded from scientific evidence.
