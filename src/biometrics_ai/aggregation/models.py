from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


class SingleTemplateMLP(nn.Module):
    def __init__(self, input_dim: int, output_dim: int, hidden_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(input_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, output_dim))

    def forward(self, templates: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        if templates.ndim == 3:
            templates = templates[:, 0]
        return F.normalize(self.net(templates.float()), dim=-1)


class PooledTemplateMLP(nn.Module):
    def __init__(self, input_dim: int, output_dim: int, hidden_dim: int = 256, pooling: str = "mean"):
        super().__init__()
        if pooling not in {"mean", "max"}:
            raise ValueError("pooling must be 'mean' or 'max'")
        self.pooling = pooling
        self.net = nn.Sequential(nn.Linear(input_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, output_dim))

    def forward(self, templates: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        if templates.ndim != 3:
            raise ValueError("PooledTemplateMLP expects (batch, exposures, features)")
        if mask is not None:
            valid = mask.unsqueeze(-1)
            if self.pooling == "mean":
                pooled = (templates * valid).sum(dim=1) / valid.sum(dim=1).clamp_min(1)
            else:
                pooled = templates.masked_fill(~valid, float("-inf")).max(dim=1).values
        elif self.pooling == "mean":
            pooled = templates.mean(dim=1)
        else:
            pooled = templates.max(dim=1).values
        return F.normalize(self.net(pooled.float()), dim=-1)


class DeepSetsExtractor(nn.Module):
    """Permutation-invariant extractor with an explicit valid-exposure mask."""
    def __init__(self, input_dim: int, output_dim: int, hidden_dim: int = 256):
        super().__init__()
        self.phi = nn.Sequential(nn.Linear(input_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, hidden_dim), nn.ReLU())
        self.rho = nn.Sequential(nn.Linear(hidden_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, output_dim))

    def forward(self, templates: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        encoded = self.phi(templates.float())
        if mask is None:
            pooled = encoded.mean(dim=1)
        else:
            weights = mask.to(encoded.dtype).unsqueeze(-1)
            pooled = (encoded * weights).sum(dim=1) / weights.sum(dim=1).clamp_min(1)
        return F.normalize(self.rho(pooled), dim=-1)
