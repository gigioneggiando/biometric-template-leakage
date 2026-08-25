.PHONY: test smoke-test system-info proposed-small

test:
	python -m pytest

smoke-test:
	python scripts/reproduce/run_smoke_test.py

system-info:
	python scripts/diagnostics/system_info.py

proposed-small:
	python scripts/train/run_multiexposure.py --config configs/attacks/proposed_synthetic.yaml
