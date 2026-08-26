import pytest

from scripts.train.run_month1_seed_robustness import summarize_cells, summarize_studies


def test_robustness_summary_preserves_factorial_cells():
    rows = []
    for split_seed in (1, 2):
        for key_seed in (3, 4):
            for model_seed, top1 in ((7, 0.1), (17, 0.2), (27, 0.3)):
                rows.append(
                    {
                        "study": "dataset",
                        "identity_split_seed": split_seed,
                        "key_seed": key_seed,
                        "model_seed": model_seed,
                        "condition": "independent_unseen_keys",
                        "chance_top1": 0.2,
                        "top1_linkage": top1,
                        "clustered_lower": 0.05,
                        "clustered_upper": 0.35,
                        "auroc": 0.5,
                        "eer": 0.5,
                    }
                )
    cells = summarize_cells(rows)
    assert len(cells) == 4
    assert all(cell["model_runs"] == 3 for cell in cells)
    assert all(cell["top1_mean"] == pytest.approx(0.2) for cell in cells)
    summary = summarize_studies(cells)
    assert len(summary) == 1
    assert summary[0]["study"] == "dataset"
    assert summary[0]["condition"] == "independent_unseen_keys"
    assert summary[0]["factorial_cells"] == 4
    assert summary[0]["model_runs_per_cell"] == 3
    assert summary[0]["chance_top1"] == 0.2
    assert summary[0]["cell_top1_mean"] == pytest.approx(0.2)
    assert summary[0]["cell_top1_std"] == 0.0
    assert summary[0]["cell_top1_min"] == pytest.approx(0.2)
    assert summary[0]["cell_top1_max"] == pytest.approx(0.2)
    assert summary[0]["all_run_clustered_intervals_include_chance"] is True