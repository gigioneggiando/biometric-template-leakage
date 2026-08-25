from __future__ import annotations

import json
import platform
import subprocess
from pathlib import Path
import torch


def main() -> None:
    gpu = []
    if torch.cuda.is_available():
        for index in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(index)
            gpu.append({"index": index, "name": props.name, "vram_bytes": props.total_memory})
    try:
        driver = subprocess.check_output(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"], text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        driver = None
    output = {"os": platform.platform(), "python": platform.python_version(), "pytorch": torch.__version__,
              "cuda_available": torch.cuda.is_available(), "cuda_version": torch.version.cuda, "gpu": gpu, "driver_version": driver}
    Path("results").mkdir(exist_ok=True)
    Path("results/system_info.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
