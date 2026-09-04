from pathlib import Path

import numpy as np
import torch

from biometrics_ai.aggregation.models import PooledTemplateMLP
from biometrics_ai.data.multiexposure import ExposureSetConfig, build_real_exposure_sets


def _inputs(tmp_path: Path):
    rng = np.random.default_rng(4)
    embeddings, templates, metadata = [], [], []
    for split, identity_count in (("train", 3), ("val", 1), ("test", 2)):
        for identity in range(identity_count):
            identity_id = f"{split}_{identity}"
            for sample in range(12):
                embedding = rng.normal(size=6)
                embeddings.append(embedding / np.linalg.norm(embedding))
                templates.append(rng.integers(0, 2, size=4))
                metadata.append(
                    {
                        "identity_id": identity_id,
                        "sample_id": f"{identity_id}_{sample}",
                        "sample_index": sample,
                        "split": split,
                        "source_image": str(tmp_path / f"{identity_id}_{sample}.jpg"),
                    }
                )
    return np.asarray(embeddings), np.asarray(templates), metadata


def test_real_exposure_sets_are_nested_and_hold_out_gallery(tmp_path: Path):
    embeddings, templates, metadata = _inputs(tmp_path)
    two = build_real_exposure_sets(embeddings, templates, metadata, "test", ExposureSetConfig(2, 3, 17))
    five = build_real_exposure_sets(embeddings, templates, metadata, "test", ExposureSetConfig(5, 3, 17))

    assert two["templates"].shape == (6, 2, 4)
    assert five["templates"].shape == (6, 5, 4)
    assert np.array_equal(two["templates"], five["templates"][:, :2])
    assert np.array_equal(two["set_ids"], five["set_ids"])
    assert len(two["gallery"]) == 2
    for gallery in two["gallery"]:
        assert not np.any(np.all(two["targets"] == gallery, axis=1))


def test_pooled_template_mlp_is_permutation_invariant():
    torch.manual_seed(3)
    values = torch.randn(2, 4, 5)
    for pooling in ("mean", "max"):
        model = PooledTemplateMLP(5, 3, pooling=pooling)
        assert torch.allclose(model(values), model(values[:, [2, 0, 3, 1]]), atol=1e-6)