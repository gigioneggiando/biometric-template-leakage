import numpy as np
import pytest

from scripts.train import run_lfw_month1


def test_independent_keys_are_unique_and_split_disjoint(monkeypatch: pytest.MonkeyPatch):
    embeddings = np.eye(3, dtype=np.float32)
    metadata = [
        {"split": "train"},
        {"split": "val"},
        {"split": "test"},
    ]
    templates, audit = run_lfw_month1.protect_embeddings(
        embeddings,
        metadata,
        "independent_unseen_keys",
        key_seed=7,
        template_dim=2,
    )
    assert templates.shape == (3, 2)
    assert audit == {"unique_keys": 3, "split_key_disjoint": True}

    monkeypatch.setattr(run_lfw_month1, "generate_key", lambda *_: 1)
    with pytest.raises(RuntimeError, match="overlapping split key pools"):
        run_lfw_month1.protect_embeddings(
            embeddings,
            metadata,
            "independent_unseen_keys",
            key_seed=7,
            template_dim=2,
        )