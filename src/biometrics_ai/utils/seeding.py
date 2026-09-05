"""Centralized deterministic seeding for experiment reproducibility."""
from __future__ import annotations

import os
import random
from dataclasses import asdict, dataclass

import numpy as np
import torch


@dataclass(frozen=True)
class SeedRecord:
    seed: int
    deterministic_algorithms: bool


def seed_everything(seed: int, deterministic: bool = True) -> SeedRecord:
    if deterministic:
        # CUDA 10.2+ needs this workspace setting for deterministic CuBLAS kernels.
        # Set it before CUDA is initialized by manual seeding or model execution.
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.use_deterministic_algorithms(True, warn_only=True)
        torch.backends.cudnn.benchmark = False
    return SeedRecord(seed=seed, deterministic_algorithms=deterministic)


def seed_record_dict(seed: int, deterministic: bool = True) -> dict:
    return asdict(seed_everything(seed, deterministic))
