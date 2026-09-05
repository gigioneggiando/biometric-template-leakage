from pathlib import Path

import numpy as np
import pytest
import torch

from biometrics_ai.aggregation.models import PooledTemplateMLP
from biometrics_ai.data.multiexposure import ExposureSetConfig, build_real_exposure_sets, shuffle_non_anchor_records
from scripts.train import run_real_multiexposure


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


def test_system_key_pool_recurs_across_identity_splits(monkeypatch: pytest.MonkeyPatch):
    embeddings = np.ones((6, 4), dtype=np.float32)
    metadata = [
        {"sample_id": str(index), "sample_index": index % 3, "split": split}
        for index, split in enumerate(("train", "train", "val", "val", "test", "test"))
    ]

    monkeypatch.setattr(
        run_real_multiexposure,
        "biohash",
        lambda embedding, key, config: np.full(config.output_dim, key % 251, dtype=np.uint8),
    )
    templates, audit = run_real_multiexposure.protect_embeddings(
        embeddings,
        metadata,
        "system_key_pool_2",
        key_seed=31,
        template_dim=2,
    )

    assert np.array_equal(templates[0], templates[2])
    assert np.array_equal(templates[1], templates[4])
    assert not np.array_equal(templates[0], templates[1])
    assert audit == {
        "scheme": "biohash",
        "unique_keys": 2,
        "split_key_disjoint": False,
        "key_scope": "system-wide recurring",
        "key_pool_size": 2,
    }


def test_key_pool_evidence_compares_recurring_pools_with_fresh_keys():
    def model(top1: float, lower: float) -> dict:
        return {
            "summary": {"top1_linkage": {"mean": top1}},
            "runs": [{"top1_identity_clustered_interval": {"lower": lower}}],
        }

    conditions = {
        "system_key_pool_1": {"exposures": {"10": {"models": {"mean_mlp": model(0.7, 0.5)}}}},
        "system_key_pool_10": {"exposures": {"10": {"models": {"mean_mlp": model(0.3, 0.2)}}}},
        "independent_unseen_keys": {"exposures": {"10": {"models": {"mean_mlp": model(0.03, 0.0)}}}},
    }
    metadata = [{"identity_id": str(index), "split": "test"} for index in range(30)]
    config = {
        "primary_analysis": "key_pool_boundary",
        "conditions": ["system_key_pool_1", "system_key_pool_10", "independent_unseen_keys"],
        "amplification_threshold": 0.05,
    }

    evidence = run_real_multiexposure.evaluate_primary_evidence(conditions, metadata, config)

    assert evidence["analysis"] == "key_pool_boundary"
    assert evidence["all_recurring_pools_exclude_chance"]
    assert evidence["all_recurring_pools_meet_minimum_effect"]


def test_descriptive_control_uses_configured_model():
    model = {
        "summary": {"top1_linkage": {"mean": 0.4}},
        "runs": [{"top1_identity_clustered_interval": {"lower": 0.2}}],
    }
    conditions = {
        "random_key_pool_3": {
            "exposures": {
                "10": {"models": {"deepsets": model}},
            }
        }
    }
    metadata = [{"identity_id": str(index), "split": "test"} for index in range(30)]

    evidence = run_real_multiexposure.evaluate_primary_evidence(
        conditions,
        metadata,
        {"primary_analysis": "descriptive_control", "control_model": "deepsets"},
    )

    assert evidence["control_model"] == "deepsets"
    assert evidence["conditions"]["random_key_pool_3"]["ten_record_top1_mean"] == 0.4


def test_random_key_pool_assignment_is_stable_and_not_session_bound(monkeypatch: pytest.MonkeyPatch):
    embeddings = np.ones((40, 8), dtype=np.float32)
    metadata = [
        {"sample_id": f"sample_{index}", "sample_index": index % 4, "split": "train"}
        for index in range(40)
    ]
    pool = [run_real_multiexposure.generate_key(41, "system_pool", index) for index in range(2)]
    pool_slots = {key: slot for slot, key in enumerate(pool)}
    monkeypatch.setattr(
        run_real_multiexposure,
        "biohash",
        lambda embedding, key, config: np.full(config.output_dim, pool_slots[key], dtype=np.uint8),
    )
    first, first_audit = run_real_multiexposure.protect_embeddings(
        embeddings,
        metadata,
        "random_key_pool_2",
        key_seed=41,
        template_dim=4,
    )
    second, second_audit = run_real_multiexposure.protect_embeddings(
        embeddings,
        metadata,
        "random_key_pool_2",
        key_seed=41,
        template_dim=4,
    )

    assert np.array_equal(first, second)
    assert first_audit == second_audit
    assert first_audit["key_scope"] == "system-wide recurring randomized"
    expected_slots = [
        run_real_multiexposure.generate_key(41, "pool_assignment", row["sample_id"]) % 2
        for row in metadata
    ]
    assert np.array_equal(first[:, 0], expected_slots)
    assert len(set(first[::4, 0])) == 2


def test_key_slot_known_appends_one_hot_slot(monkeypatch: pytest.MonkeyPatch):
    embeddings = np.ones((12, 8), dtype=np.float32)
    metadata = [
        {"sample_id": f"sample_{index}", "sample_index": index, "split": "train"}
        for index in range(12)
    ]
    monkeypatch.setattr(
        run_real_multiexposure,
        "biohash",
        lambda embedding, key, config: np.zeros(config.output_dim, dtype=np.uint8),
    )

    templates, audit = run_real_multiexposure.protect_embeddings(
        embeddings,
        metadata,
        "random_key_pool_3",
        key_seed=43,
        template_dim=4,
        protection={"scheme": "biohash", "include_key_slot": True},
    )

    expected_slots = [
        run_real_multiexposure.generate_key(43, "pool_assignment", row["sample_id"]) % 3
        for row in metadata
    ]
    assert templates.shape == (12, 7)
    assert np.array_equal(templates[:, 4:], np.eye(3, dtype=np.float32)[expected_slots])
    assert audit["attacker_key_slot_known"] is True


def test_shuffle_non_anchor_preserves_anchor_and_uses_other_identities():
    identities = np.repeat(np.asarray(["a", "b", "c"]), 2)
    templates = np.zeros((6, 4, 1), dtype=np.float32)
    for row, identity in enumerate(identities):
        templates[row, :, 0] = ord(identity)
    exposure_set = {
        "templates": templates,
        "identity_ids": identities,
        "targets": np.zeros((6, 2)),
        "set_ids": np.arange(6),
        "gallery": np.zeros((3, 2)),
        "gallery_identity_ids": np.asarray(["a", "b", "c"]),
    }

    shuffled = shuffle_non_anchor_records(exposure_set, seed=47)

    assert np.array_equal(shuffled["templates"][:, 0], templates[:, 0])
    for row, identity in enumerate(identities):
        assert np.all(shuffled["templates"][row, 1:, 0] != ord(identity))
    assert sorted(shuffled["templates"][:, 1, 0]) == sorted(templates[:, 1, 0])


def test_reassign_identity_splits_preserves_counts_and_disjointness(tmp_path: Path):
    _, _, metadata = _inputs(tmp_path)
    original = {split: {r["identity_id"] for r in metadata if r["split"] == split} for split in ("train", "val", "test")}

    reassigned = run_real_multiexposure.reassign_identity_splits(metadata, seed=5)
    again = run_real_multiexposure.reassign_identity_splits(metadata, seed=5)
    new = {split: {r["identity_id"] for r in reassigned if r["split"] == split} for split in ("train", "val", "test")}

    assert reassigned == again
    assert {s: len(v) for s, v in new.items()} == {s: len(v) for s, v in original.items()}
    assert not (new["train"] & new["val"] or new["train"] & new["test"] or new["val"] & new["test"])
    assert new != original
    for row, row_before in zip(reassigned, metadata):
        assert row["identity_id"] == row_before["identity_id"]
        same_identity = [r["split"] for r in reassigned if r["identity_id"] == row["identity_id"]]
        assert len(set(same_identity)) == 1
