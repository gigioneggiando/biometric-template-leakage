.PHONY: test smoke-test system-info proposed-small lfw-protocol lfw-large-protocol cfp-protocol olivetti-protocol month1-lfw month1-lfw-yunet month1-lfw-large month1-cfp month1-cfp-profile month1-olivetti month1-dimension-sweeps

test:
	python -m pytest

smoke-test:
	python scripts/reproduce/run_smoke_test.py

system-info:
	python scripts/diagnostics/system_info.py

proposed-small:
	python scripts/train/run_multiexposure.py --config configs/attacks/proposed_synthetic.yaml

lfw-protocol:
	python scripts/data/prepare_lfw.py

lfw-large-protocol:
	python scripts/data/prepare_lfw.py --output data/interim/lfw_large_month1_protocol.csv --identities 150 --samples-per-identity 10

cfp-protocol:
	python scripts/data/prepare_cfp.py

olivetti-protocol:
	python scripts/data/prepare_olivetti.py

month1-lfw:
	python scripts/train/run_lfw_month1.py --config configs/attacks/month1_lfw.yaml

month1-lfw-yunet:
	python scripts/train/run_lfw_month1.py --config configs/attacks/month1_lfw_yunet.yaml

month1-lfw-large:
	python scripts/train/run_lfw_month1.py --config configs/attacks/month1_lfw_large.yaml

month1-cfp:
	python scripts/train/run_lfw_month1.py --config configs/attacks/month1_cfp.yaml

month1-cfp-profile:
	python scripts/train/run_lfw_month1.py --config configs/attacks/month1_cfp_profile.yaml

month1-olivetti:
	python scripts/train/run_lfw_month1.py --config configs/attacks/month1_olivetti.yaml

month1-dimension-sweeps:
	python scripts/train/run_month1_dimension_sweep.py --base-config configs/attacks/month1_lfw_yunet.yaml --output-root results/month1_sweeps/lfw_yunet
	python scripts/train/run_month1_dimension_sweep.py --base-config configs/attacks/month1_olivetti.yaml --output-root results/month1_sweeps/olivetti
