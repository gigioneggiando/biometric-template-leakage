# Data handling

**Status checked: 2026-09-18**, against `4352eeb`. Four multi-exposure datasets are now used: MOBIO (1,799 embeddings), LFW (1,500), FEI (2,378), and SCface (2,851). See the [current evidence](../reports/final_research_status.md).

`raw/`, `interim/`, and `processed/` are ignored. Never commit biometric images, templates, model weights, or access credentials.

MOBIO is a manual-access dataset. Follow [MOBIO setup](../docs/setup/MOBIO.md), then run `python scripts/data/prepare_mobio.py --root <authorized-path>`.

LFW, Olivetti faces, and CFP are real-data engineering fallbacks and must never be reported as MOBIO or paper reproductions. Their downloaders verify available source artifacts before use:

- `python scripts/data/download_lfw.py` uses scikit-learn's documented funneled LFW fetcher.
- `python scripts/data/download_olivetti.py` verifies cache SHA-256 `47398b319d88c78459514b30b87c562313aad345b5c6a387b678d7f8177be4ba`.
- `python scripts/data/download_cfp.py` verifies official archive SHA-256 `666b87635e6af028177ac72a85f03099fac263baf09c21f333fa445f930f65b1` before extraction. The official host uses HTTP and the archive has no explicit license file, so the hash is mandatory and redistribution is not assumed.

Deterministic splits, failure handling, commands, and results are documented in [the Month 1 real-dataset protocol](../docs/protocols/real_datasets_month1.md). Synthetic identities remain useful for tests but are excluded from scientific evidence.

## Current authorized archives

- MOBIO acquisition was completed on 2026-09-04; preserve the eight-file archive inventory and checksums in the [local handoff](../docs/setup/MOBIO_LOCAL_DATA.md).
- FEI's four official image archives were acquired on 2026-09-12. Archive hashes remain in the private external data directory; the [study](../experiments/fei_multiexposure/README.md) records selection and 22 detection failures.
- Sani supplied SCface on 2026-09-18. The [setup record](../docs/setup/SCFACE_LOCAL_DATA.md) records the archive checksum, extraction and protocol. Nine detection failures leave all 130 identities eligible; the held-out gallery contains 26 test identities.
- AgeDB is optional and not acquired. Do not infer authorization from a public URL or copy an archive into Git.

Private archives, embeddings and original experiment artifacts are retained for reproducibility. Only superseded generated report previews are eligible for presentation cleanup.
