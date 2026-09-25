import pytest

from biometrics_ai.protection.source_analysis import analyse_source


PREFIX = "from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect, correlated_biohash\n"


@pytest.mark.parametrize("expression,expected", [
    ("7", "reuse"), ("record_id % 4", "reuse"), ("record_id & 7", "reuse"),
    ("record_id * 0", "reuse"), ("record_id", "conditional_fresh"),
    ("3 * record_id + 9", "conditional_fresh"), ("9 - record_id", "conditional_fresh"),
    ("record_id // 4", "unknown"), ("record_id - record_id", "unknown"),
])
def test_tracks_arithmetic_not_configuration_names(expression, expected):
    source = PREFIX + f"def implementation(embedding, master, record_id, config):\n    value = {expression}\n    hidden = derive(master, 'domain', value)\n    return protect(embedding, hidden, config)\n"
    assert analyse_source(source, "implementation")["decision"] == expected


def test_helper_alias_and_hash_cannot_restore_lost_scope():
    source = PREFIX + """
def derive_slot(secret, index):
    local_alias = derive
    return local_alias(secret, 'namespace', index & 3)
def implementation(embedding, master, record_id, config):
    token = derive_slot(master, record_id)
    return protect(embedding, token, config)
"""
    result = analyse_source(source, "implementation")
    assert result["decision"] == "reuse"
    assert result["sinks"][0]["key"]["capacity"] == 4


def test_shared_component_despite_unique_private_keys():
    source = PREFIX + """
def implementation(embedding, master, record_id, config):
    common = derive(master, 'shared', 0)
    private = derive(master, 'private', record_id)
    return correlated_biohash(embedding, common, private, 16, config)
"""
    result = analyse_source(source, "implementation")
    assert result["decision"] == "reuse"
    assert [sink["key"]["scope"] for sink in result["sinks"]] == ["fixed", "record_injective"]


@pytest.mark.parametrize("statement", ["if record_id:\n        return protect(embedding, 0, config)",
                                        "for index in range(2):\n        master = index",
                                        "token = external(record_id)", "token = record_id[0]"])
def test_unsupported_constructs_never_pass(statement):
    source = PREFIX + f"def implementation(embedding, master, record_id, config):\n    {statement}\n    return protect(embedding, master, config)\n"
    result = analyse_source(source, "implementation")
    assert result["decision"] != "conditional_fresh"
    assert not result["complete"]


def test_no_execution_of_source():
    source = "raise RuntimeError('must not execute')\n" + PREFIX + "def implementation(record_id):\n    return record_id\n"
    assert analyse_source(source, "implementation")["decision"] == "unknown"


def test_unknown_external_kdf_does_not_inherit_trusted_name():
    source = "from attacker_module import generate_key as derive\n" + PREFIX.split("\n")[0].replace("generate_key as derive, ", "") + "\ndef implementation(embedding, master, record_id, config):\n    return protect(embedding, derive(master, 'domain', record_id), config)\n"
    assert analyse_source(source, "implementation")["decision"] == "unknown"


def test_uniform_reuse_formula_matches_enumeration():
    import itertools
    import numpy as np
    from biometrics_ai.evaluation.security_utility import uniform_reuse_envelope

    count = np.mean([sum(slots[first] == slots[second] for first, second in [(0, 1), (0, 2), (1, 2)])
                     for slots in itertools.product(range(4), repeat=3)])
    actual = uniform_reuse_envelope(2, 1, [1.0], [4])
    assert actual["expected_reused_component_mass"] == count == .75
    assert uniform_reuse_envelope(10, 100, [.25, .75], [1, None])["expected_reused_component_mass"] == 261.25
    assert uniform_reuse_envelope(10, 100, [1.0], [None])["ideal_bad_event_upper"] == 0


def test_threshold_handles_ties_without_optimistic_fmr():
    import numpy as np
    from biometrics_ai.evaluation.security_utility import validation_threshold

    values = np.array([.5] * 99 + [.9])
    threshold = validation_threshold(values, .01)
    assert np.mean(values >= threshold) == .01
    assert validation_threshold(np.ones(100), .01) > 1


def test_security_improvement_alone_cannot_pass_utility_gate():
    from biometrics_ai.evaluation.security_utility import acceptance_gate

    assert acceptance_gate(.3, -.01, .015, .03, .02)
    assert not acceptance_gate(.3, -.04, .015, .03, .02)
    assert not acceptance_gate(.3, -.01, .025, .03, .02)
    assert not acceptance_gate(0, -.01, .015, .03, .02)


def test_benchmark_oracle_does_not_use_static_predictions():
    from scripts.diagnostics.benchmark_source_analysis import corpus, runtime_label

    cases = {case["case"]: case["source"] for case in corpus()}
    assert runtime_label(cases["expression_05"])["oracle"] == "no_reuse_observed"
    assert runtime_label(cases["expression_02"])["oracle"] == "reuse_observed"
    assert runtime_label(cases["branch_reuse"])["oracle"] == "reuse_observed"
    assert analyse_source(cases["branch_reuse"], "implementation")["decision"] == "unknown"


def test_executable_recipes_match_analyzed_scope_and_batch_projection():
    import time
    import numpy as np
    from pathlib import Path
    from scripts.diagnostics import source_policy_recipes as recipes
    from scripts.train.run_source_security_utility import protect
    from threadpoolctl import threadpool_limits

    source = Path(recipes.__file__).read_text()
    values = np.random.default_rng(81).normal(size=(4, 512)).astype(np.float32)
    with threadpool_limits(limits=1):
        for policy, decision in [("recurring", "reuse"), ("partial", "reuse"), ("separated", "conditional_fresh")]:
            assert analyse_source(source, policy)["decision"] == decision
            assert protect(values, policy, 71, time.monotonic() + 30).shape == (4, 64)


def test_same_key_verification_is_not_direct_cross_key_matching():
    import time
    import numpy as np
    from scripts.train.run_source_security_utility import verification_scores
    from threadpoolctl import threadpool_limits

    random = np.random.default_rng(29)
    identities = random.normal(size=(3, 512)).astype(np.float32)
    values = np.repeat(identities, 2, axis=0)
    metadata = [{"split": "test", "identity_id": str(index // 2), "sample_index": index % 2}
                for index in range(6)]
    with threadpool_limits(limits=1):
        result = verification_scores(values, metadata, "test", "separated", 53, time.monotonic() + 30)
    assert np.all(result["scores"][result["matches"]] == 1)
    assert np.all(result["scores"][~result["matches"]] < 1)


def test_composed_projection_exposes_shared_component_without_named_correlated_scheme():
    from scripts.diagnostics.benchmark_source_analysis import corpus, runtime_label

    cases = {case["case"]: case["source"] for case in corpus()}
    source = cases["assembled_blocks_True"]
    result = analyse_source(source, "implementation")
    assert result["decision"] == "reuse"
    assert result["sinks"][0]["weight"] == .25
    assert result["sinks"][1]["weight"] == .75
    assert runtime_label(source)["oracle"] == "reuse_observed"
    assert analyse_source(cases["assembled_blocks_False"], "implementation")["decision"] == "conditional_fresh"
    assert runtime_label(cases["assembled_blocks_False"])["oracle"] == "no_reuse_observed"


def test_reimport_cannot_inherit_trusted_contract():
    source = PREFIX + "from unknown_module import replacement as derive\n" + "def implementation(embedding, master, record_id, config):\n    return protect(embedding, derive(master, 'domain', record_id), config)\n"
    assert analyse_source(source, "implementation")["decision"] == "unknown"


def test_later_import_overrides_local_helper_summary():
    source = "from biometrics_ai.protection.biohash import biohash\ndef helper(master, record_id):\n    return record_id\nfrom unknown_module import replacement as helper\ndef implementation(embedding, master, record_id, config):\n    return biohash(embedding, helper(master, record_id), config)\n"
    assert analyse_source(source, "implementation")["decision"] == "unknown"


def test_rebound_entry_cannot_use_stale_function_body():
    source = PREFIX + "def implementation(embedding, master, record_id, config):\n    return protect(embedding, record_id, config)\nfrom unknown_module import replacement as implementation\n"
    assert analyse_source(source, "implementation")["decision"] == "unknown"


def test_completed_benchmark_predictions_unchanged_after_binding_fix():
    import csv
    import json
    from pathlib import Path
    from scripts.diagnostics.benchmark_source_analysis import runtime_label

    study = Path(__file__).resolve().parents[2] / "experiments/source_security_utility_2026-09-25/benchmark"
    cases = json.loads((study / "corpus.json").read_text())
    with (study / "benchmark.csv").open(newline="") as handle:
        observed = {row["case"]: row for row in csv.DictReader(handle)}
    for case in cases:
        assert analyse_source(case["source"], "implementation")["decision"] == observed[case["case"]]["source_decision"]
        assert runtime_label(case["source"])["oracle"] == observed[case["case"]]["oracle"]


def test_executed_sources_remain_verifiable():
    import hashlib
    import json
    from pathlib import Path
    import zipfile

    root = Path(__file__).resolve().parents[2]
    study = root / "experiments/source_security_utility_2026-09-25"
    manifest = json.loads((study / "execution_manifest.json").read_text())
    assert manifest["status"] == "completed"
    assert manifest["trained_endpoints"] == 18
    with zipfile.ZipFile(study / "executed_source_analysis.zip") as archive:
        for relative, expected in manifest["source_sha256"].items():
            content = (root / relative).read_bytes()
            if relative == "src/biometrics_ai/protection/source_analysis.py":
                content = archive.read("source_analysis.py")
            assert hashlib.sha256(content).hexdigest() == expected, relative


def test_security_utility_exports_match_endpoints_and_fixed_gate():
    import csv
    from pathlib import Path
    import numpy as np
    from biometrics_ai.evaluation.security_utility import acceptance_gate

    study = Path(__file__).resolve().parents[2] / "experiments/source_security_utility_2026-09-25"
    with (study / "endpoints.csv").open(newline="") as handle:
        endpoints = list(csv.DictReader(handle))
    with (study / "security_utility_effects.csv").open(newline="") as handle:
        effects = list(csv.DictReader(handle))
    assert len(endpoints) == 18
    for row in effects:
        for policy, prefix in [("recurring", "before"), (row["candidate"], "after")]:
            selected = [entry for entry in endpoints if entry["dataset"] == row["dataset"] and entry["policy"] == policy]
            assert len(selected) == 3
            for metric, column in [("leakage", "attacker_top1"), ("tar", "tar"), ("fmr", "fmr")]:
                assert float(row[f"{prefix}_{metric}"]) == pytest.approx(np.mean([float(entry[column]) for entry in selected]))
        passed = acceptance_gate(float(row["leakage_reduction_lower"]), float(row["tar_difference_lower"]),
                                 float(row["after_fmr_upper"]), .03, .02)
        assert passed == (row["gate_pass"] == "True")
    assert all(float(row["validation_fmr"]) <= .01 for row in endpoints)


def test_source_report_layout_and_rendering(tmp_path, monkeypatch):
    pytest.importorskip("matplotlib")
    pdfium = pytest.importorskip("pypdfium2")
    import numpy as np
    from scripts.figures import make_source_security_report as report

    original = report.PdfPages.savefig

    def inspect(pdf, figure, **kwargs):
        figure.canvas.draw()
        renderer = figure.canvas.get_renderer()
        boxes = [artist.get_window_extent(renderer) for artist in figure.texts]
        for index, box in enumerate(boxes):
            assert figure.bbox.contains(box.x0, box.y0) and figure.bbox.contains(box.x1, box.y1)
            assert not any(box.overlaps(other) for other in boxes[index + 1:])
        for axis in figure.axes:
            for artist in axis.tables:
                for cell in artist.get_celld().values():
                    text_box = cell.get_text().get_window_extent(renderer)
                    cell_box = cell.get_window_extent(renderer).padded(1)
                    assert cell_box.contains(text_box.x0, text_box.y0) and cell_box.contains(text_box.x1, text_box.y1)
        return original(pdf, figure, **kwargs)

    monkeypatch.setattr(report.PdfPages, "savefig", inspect)
    destination = tmp_path / "source_report.pdf"
    report.build_report(destination)
    with pdfium.PdfDocument(destination) as document:
        assert len(document) == 4
        for page in document:
            text_page = page.get_textpage()
            try:
                assert len(text_page.get_text_range()) > 300
            finally:
                text_page.close()
            assert np.std(np.asarray(page.render(scale=.7).to_pil())) > 10