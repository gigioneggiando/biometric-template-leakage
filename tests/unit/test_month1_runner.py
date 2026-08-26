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


def test_resplit_metadata_is_deterministic_and_identity_disjoint():
    metadata = [
        {"identity_id": f"person_{identity}", "sample_index": sample, "split": "train"}
        for identity in range(10)
        for sample in range(2)
    ]
    first = run_lfw_month1.resplit_metadata(metadata, seed=17)
    second = run_lfw_month1.resplit_metadata(metadata, seed=17)
    different_seed = run_lfw_month1.resplit_metadata(metadata, seed=18)
    assert first == second
    assert [row["split"] for row in first] != [row["split"] for row in different_seed]
    split_ids = {
        split: {row["identity_id"] for row in first if row["split"] == split}
        for split in ("train", "val", "test")
    }
    assert [len(split_ids[split]) for split in ("train", "val", "test")] == [6, 2, 2]
    assert split_ids["train"].isdisjoint(split_ids["val"] | split_ids["test"])
    assert split_ids["val"].isdisjoint(split_ids["test"])


def test_sample_scoped_keys_are_stable_across_resplits_and_reordering():
    embeddings = np.eye(6, dtype=np.float32)
    metadata = [
        {
            "sample_id": f"sample_{identity}",
            "identity_id": f"person_{identity}",
            "sample_index": 0,
            "split": "train",
        }
        for identity in range(6)
    ]
    first_metadata = run_lfw_month1.resplit_metadata(metadata, seed=17)
    second_metadata = run_lfw_month1.resplit_metadata(metadata, seed=18)
    first_templates, first_audit = run_lfw_month1.protect_embeddings(
        embeddings,
        first_metadata,
        "independent_unseen_keys",
        key_seed=7,
        template_dim=2,
        independent_key_scope="sample_id",
    )
    second_templates, second_audit = run_lfw_month1.protect_embeddings(
        embeddings,
        second_metadata,
        "independent_unseen_keys",
        key_seed=7,
        template_dim=2,
        independent_key_scope="sample_id",
    )
    assert np.array_equal(first_templates, second_templates)
    assert first_audit == second_audit == {"unique_keys": 6, "split_key_disjoint": True}

    order = np.asarray([5, 3, 1, 4, 2, 0])
    reordered_metadata = [second_metadata[int(index)] for index in order]
    reordered_templates, reordered_audit = run_lfw_month1.protect_embeddings(
        embeddings[order],
        reordered_metadata,
        "independent_unseen_keys",
        key_seed=7,
        template_dim=2,
        independent_key_scope="sample_id",
    )
    expected_by_id = {
        row["sample_id"]: template for row, template in zip(second_metadata, second_templates, strict=True)
    }
    for row, template in zip(reordered_metadata, reordered_templates, strict=True):
        assert np.array_equal(template, expected_by_id[row["sample_id"]])
    assert reordered_audit == first_audit