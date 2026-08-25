# Data handling

`raw/`, `interim/`, and `processed/` are ignored. Never commit biometric images, templates, model weights, or access credentials.

MOBIO is a manual-access dataset. Follow [MOBIO setup](../docs/setup/MOBIO.md), then run `python scripts/data/prepare_mobio.py --root <authorized-path>`.

LFW is only an engineering fallback and must never be reported as a MOBIO reproduction. `python scripts/data/download_lfw.py` uses scikit-learn's documented fetcher.
