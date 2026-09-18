from pathlib import Path
import runpy

import numpy as np
import pytest

pd = pytest.importorskip("pandas")
pytest.importorskip("matplotlib")

ROOT = Path(__file__).resolve().parents[2]
TABLE = runpy.run_path(str(ROOT / "scripts/figures/build_cross_dataset_table.py"))
DIAGRAMS = runpy.run_path(str(ROOT / "scripts/figures/make_diagrams.py"))
FIGURES = runpy.run_path(str(ROOT / "scripts/figures/make_figures.py"))


def test_comparison_preserves_every_source_row_and_endpoint():
    table = TABLE["build_table"]()
    for _, _, _, relative, identities in TABLE["SOURCES"]:
        source = pd.read_csv(ROOT / "experiments" / relative)
        actual = table[table["source_file"] == relative]
        assert len(actual) == len(source)
        np.testing.assert_allclose(actual["top1_mean"], source["top1_mean"])
        np.testing.assert_allclose(actual["top1_over_chance_10"], source["top1_mean"] * identities)
        if "one_record_top1_mean" in source:
            np.testing.assert_allclose(actual["amplification_pp"], 100 * (source["top1_mean"] - source["one_record_top1_mean"]))
        else:
            assert actual["one_record_top1_mean"].isna().all()
    lfw_pool10 = table[(table["dataset"] == "LFW") & (table["pool_size"] == "10")]
    assert not lfw_pool10["interval_excludes_chance"].item()


@pytest.mark.parametrize("fault", ["missing", "duplicate", "percent", "nan", "condition", "reversed"])
def test_comparison_rejects_invalid_sources(tmp_path, monkeypatch, fault):
    build_table = TABLE["build_table"]
    source_spec = TABLE["SOURCES"][0]
    monkeypatch.setitem(build_table.__globals__, "SOURCES", [source_spec])
    source = pd.read_csv(ROOT / "experiments" / source_spec[3])
    destination = tmp_path / source_spec[3]
    destination.parent.mkdir(parents=True)
    if fault == "missing":
        with pytest.raises(FileNotFoundError):
            build_table(tmp_path)
        return
    if fault == "duplicate":
        source = pd.concat([source, source.iloc[[0]]])
    elif fault == "percent":
        source.loc[0, "top1_mean"] = 76.9
    elif fault == "nan":
        source.loc[0, "top1_mean"] = np.nan
    elif fault == "condition":
        source.loc[0, "condition"] = "unknown"
    elif fault == "reversed":
        source.loc[0, "minimum_clustered_lower"] = 1.0
        source.loc[0, "maximum_clustered_upper"] = 0.0
    source.to_csv(destination, index=False)
    with pytest.raises(ValueError):
        build_table(tmp_path)


def test_diagrams_export_without_text_collisions(tmp_path):
    for name in ("fig_architecture", "fig_attack_detail", "fig_threat_model"):
        DIAGRAMS[name](tmp_path)
        assert (tmp_path / f"{name}.pdf").stat().st_size > 1000
        assert (tmp_path / f"{name}.png").stat().st_size > 1000


def test_detail_section_heading_does_not_touch_nodes(tmp_path, monkeypatch):
    from matplotlib.patches import FancyBboxPatch

    def inspect(fig, ax, out, name):
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        heading = next(text for text in ax.texts if text.get_text() == "B  TWO AGGREGATION PATHS")
        bounds = heading.get_window_extent(renderer).padded(2)
        assert not any(bounds.overlaps(patch.get_window_extent(renderer)) for patch in ax.patches if isinstance(patch, FancyBboxPatch))
        DIAGRAMS["plt"].close(fig)

    monkeypatch.setitem(DIAGRAMS["fig_attack_detail"].__globals__, "save_diagram", inspect)
    DIAGRAMS["fig_attack_detail"](tmp_path)


@pytest.mark.parametrize("name", ["fig_results_overview", "fig_pool_curves", "fig_amplification",
                                 "fig_pooled_boundary", "fig_controls", "fig_fresh_exposures",
                                 "fig_scheme_pilots", "fig_pilot_uncertainty", "fig_pilot_native_utility", "fig_pilot_equivalence",
                                 "fig_followup_amplification", "fig_followup_native_controls",
                                 "fig_native_norm_audit", "fig_followup_failures"])
def test_result_figures_export_without_text_collisions(tmp_path, name):
    FIGURES[name](tmp_path)
    assert (tmp_path / f"{name}.pdf").stat().st_size > 1000
    assert (tmp_path / f"{name}.png").stat().st_size > 1000


def test_tracked_table_matches_rebuilt_sources():
    expected = TABLE["build_table"]()
    actual = pd.read_csv(ROOT / "experiments/cross_dataset_key_pool_summary.csv")
    pd.testing.assert_frame_equal(actual, expected, check_exact=False, atol=0.00000051, rtol=0)


def test_plot_validator_rejects_overlapping_text(tmp_path):
    plt = FIGURES["plt"]
    fig = plt.figure()
    fig.text(0.5, 0.5, "First")
    fig.text(0.5, 0.5, "Second")
    try:
        with pytest.raises(ValueError, match="Overlapping text"):
            FIGURES["save_figure"](fig, tmp_path, "collision")
    finally:
        plt.close(fig)


def test_dataset_update_contains_current_evidence_and_vector_figures(tmp_path):
    pytest.importorskip("pptx")
    pdfium = pytest.importorskip("pypdfium2")
    pypdf = pytest.importorskip("pypdf")
    presentation = runpy.run_path(str(ROOT / "scripts/figures/make_presentation.py"))
    destination = tmp_path / "Sept_Dataset_Update.pdf"
    presentation["build_dataset_update"](destination)
    document = pypdf.PdfReader(destination)
    assert len(document.pages) == 14
    text = "\n".join(page.extract_text() for page in document.pages)
    for expected in ("4352eeb", "15e4384", "SCface", "73", "72", "216", "33.17%", "10.66%", "not confirmation", "0.004", "0.006",
                     "4,177", "0.0192", "0.0032", "SAME realized hidden pool", "not independent human review", "not established"):
        assert expected in text
    assert "we have not tested it yet" not in text.lower()
    assert "luigi" not in text.lower()
    assert "colluto" not in text.lower()
    assert "REQUIRED BEFORE SUBMISSION" not in text
    assert "A/A*" not in text
    for page in document.pages:
        assert len(page.extract_text()) > 100
    assert not list(document.pages[1].images)
    assert not list(document.pages[2].images)
    assert "Shared record encoder" in document.pages[2].extract_text()
    assert "Key" in document.pages[1].extract_text()
    with pdfium.PdfDocument(destination) as rendered:
        for page in rendered:
            bitmap = page.render(scale=0.75)
            pixels = np.asarray(bitmap.to_pil())
            assert (pixels[..., :3] < 240).any(axis=2).mean() > 0.01
            bitmap.close()
            page.close()
    assert not destination.with_suffix(".tmp.pdf").exists()


def test_presentation_has_ten_nonblank_pages_and_editable_text(tmp_path):
    pptx = pytest.importorskip("pptx")
    pdfium = pytest.importorskip("pypdfium2")
    presentation = runpy.run_path(str(ROOT / "scripts/figures/make_presentation.py"))
    presentation["build_presentation"](tmp_path)
    deck = pptx.Presentation(tmp_path / "research_review.pptx")
    assert len(deck.slides) == 10
    for slide in deck.slides:
        text = " ".join(shape.text for shape in slide.shapes if shape.has_text_frame)
        assert len(text) > 70
        assert text.isascii()
        for shape in slide.shapes:
            assert shape.left >= 0 and shape.top >= 0
            assert shape.left + shape.width <= deck.slide_width
            assert shape.top + shape.height <= deck.slide_height
    with pdfium.PdfDocument(tmp_path / "research_review.pdf") as pdf:
        assert len(pdf) == 10
        for page in pdf:
            bitmap = page.render(scale=0.75)
            pixels = np.asarray(bitmap.to_pil())
            assert (pixels[..., :3] < 240).any(axis=2).mean() > 0.01
            bitmap.close()
            page.close()
    with pdfium.PdfDocument(tmp_path / "figure_appendix.pdf") as appendix:
        assert len(appendix) == 17
        for page in appendix:
            text_page = page.get_textpage()
            try:
                text = text_page.get_text_range()
                assert len(text) > 40
                assert not any(character in text for character in ("\u2013", "\u2014", "\u2212"))
            finally:
                text_page.close()
            bitmap = page.render(scale=0.75)
            pixels = np.asarray(bitmap.to_pil())
            assert (pixels[..., :3] < 240).any(axis=2).mean() > 0.01
            bitmap.close()
            page.close()