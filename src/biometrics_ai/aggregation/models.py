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
