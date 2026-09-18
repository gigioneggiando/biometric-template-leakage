"""Build an editable review deck and matching PDF without biometric images."""
from __future__ import annotations

from pathlib import Path
import argparse
from io import BytesIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import pandas as pd
import pypdfium2 as pdfium
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / "reports/figures"
WIDTH, HEIGHT = 13.333333, 7.5
FONT = "Times New Roman"


def add_text(slide, fig, text, x, y, width, height, size=18, bold=False, color="#222222"):
    if not text.isascii():
        raise ValueError(f"Non-ASCII slide label: {text}")
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(width), Inches(height))
    frame = shape.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    frame.word_wrap = False
    for index, line in enumerate(text.split("\n")):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.font.name = FONT
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = RGBColor.from_string(color.lstrip("#"))
        paragraph.space_after = Pt(0)
        paragraph.line_spacing = 1.4
    artist = fig.text(x / WIDTH, 1 - y / HEIGHT, text, fontsize=size, family=FONT,
                      weight="bold" if bold else "normal", color=color, va="top", linespacing=1.4)
    fig.canvas.draw()
    bound = artist.get_window_extent(fig.canvas.get_renderer())
    region = matplotlib.transforms.Bbox.from_bounds(x * fig.dpi, (HEIGHT - y - height) * fig.dpi,
                                                    width * fig.dpi, height * fig.dpi).padded(0.5)
    if not region.contains(bound.x0, bound.y0) or not region.contains(bound.x1, bound.y1):
        raise ValueError(f"Slide text exceeds its region: {text}")


def add_figure(slide, fig, name, x=0.6, y=1.05, width=12.1, height=5.35):
    path = FIGURES / f"{name}.png"
    with Image.open(path) as image:
        ratio = image.width / image.height
    image_width = min(width, height * ratio)
    image_height = image_width / ratio
    left = x + (width - image_width) / 2
    top = y + (height - image_height) / 2
    slide.shapes.add_picture(str(path), Inches(left), Inches(top), width=Inches(image_width), height=Inches(image_height))
    ax = fig.add_axes([left / WIDTH, 1 - (top + image_height) / HEIGHT, image_width / WIDTH, image_height / HEIGHT])
    ax.imshow(plt.imread(path))
    ax.axis("off")


def build_presentation(out: Path) -> None:
    table = pd.read_csv(ROOT / "experiments/cross_dataset_key_pool_summary.csv")
    out.mkdir(parents=True, exist_ok=True)
    presentation = Presentation()
    presentation.slide_width, presentation.slide_height = Inches(WIDTH), Inches(HEIGHT)
    presentation.core_properties.title = "Hidden keys and repeated biometric records"
    presentation.core_properties.subject = "Research review draft, 2026-09-18"
    with PdfPages(out / "research_review.pdf") as pdf:
        for number, title in enumerate([
            "Hidden keys and repeated biometric records",
            "Experimental architecture",
            "Dataset and protection coverage",
            "Set reconstruction and gallery linkage",
            "Earlier three-seed key-pool studies",
            "Mechanism and correlation controls",
            "Replicated multi-record amplification",
            "Native linkage and radial sensitivity",
        ], start=1):
            slide = presentation.slides.add_slide(presentation.slide_layouts[6])
            fig = plt.figure(figsize=(WIDTH, HEIGHT), dpi=120, facecolor="white")
            add_text(slide, fig, title, 0.6, 0.3, 12.1, 0.6, size=25, bold=True)
            add_text(slide, fig, f"Research review draft | 18 September 2026 | {number}/8", 0.6, 7.07, 12.1, 0.3, size=11, color="#666666")
            if number == 1:
                add_text(slide, fig, "Can multiple protected records reveal identity when keys remain hidden?",
                         0.6, 1.45, 12.1, 0.7, size=20)
                add_text(slide, fig, "Fresh-key learned attacks: uncertainty remains; no equivalence claim.\n\n"
                         "Recurring transforms: large gains from multiple same-identity records.\n\n"
                         "Boundary location changes with the dataset and identity partition.",
                         0.6, 2.55, 12.1, 3.1, size=19)
                add_text(slide, fig, "Four datasets; hidden-key protocols; matched MOBIO/FEI follow-up with 216 trained endpoints.",
                         0.6, 6.3, 12.1, 0.45, size=13)
            elif number in (2, 4, 5, 6):
                name, caption = {
                    2: ("fig_architecture", "Train on separate identities. Reconstruct an embedding, then link to a held-out gallery."),
                    4: ("fig_attack_detail", "Two aggregation paths; shared training objective; held-out identity linkage. Key values remain hidden."),
                    5: ("fig_results_overview", f"{len(table)} conditions from {table['source_file'].nunique()} earlier studies. New one-seed pilots are reported separately."),
                    6: ("fig_controls", "Slot identifiers are not key values. Coarse and fine correlation sweeps use separate partitions."),
                }[number]
                add_figure(slide, fig, name)
                add_text(slide, fig, caption, 0.6, 6.58, 12.1, 0.4, size=12)
            elif number == 3:
                rows = [
                    ["Dataset", "Identities", "Train/val/test", "Embeddings", "Variation"],
                    ["MOBIO", "150", "90/30/30", "1,799 / 1,800", "Sessions"],
                    ["LFW", "125", "75/25/25", "1,500 / 1,500", "In-the-wild"],
                    ["FEI", "200", "120/40/40", "2,378 / 2,400", "Pose/expression"],
                    ["SCface", "130", "78/26/26", "2,851 / 2,860", "Camera/distance"],
                ]
                for row_index, row in enumerate(rows):
                    for column, value in enumerate(row):
                        add_text(slide, fig, value, [0.6, 2.6, 4.6, 7.1, 10.0][column], 1.5 + row_index * 0.5,
                                 [1.8, 1.8, 2.3, 2.7, 2.7][column], 0.5, size=15, bold=row_index == 0)
                add_text(slide, fig, "BioHash: 128 bits; four datasets; includes a Haar-sign control on MOBIO.\n"
                         "MLP-Hash: 512 bits; MOBIO; paper-specified, not source-exact.\n"
                         "IoM-GRP: 300 codes (q=16); PolyProtect: 170 reals (m=5, overlap=2).\n"
                         "Both: MOBIO/FEI three-seed, two-partition follow-up; SCface one-seed pilots.",
                         0.6, 4.15, 12.1, 1.85, size=16)
                add_text(slide, fig, "SCface: mugshot gallery and visible surveillance probes; 9 detection failures, all identities eligible.",
                         0.6, 6.3, 12.1, 0.45, size=13)
            elif number == 7:
                add_figure(slide, fig, "fig_followup_amplification")
                add_text(slide, fig, "MOBIO / FEI; IoM-GRP / PolyProtect; 3 model seeds x 2 identity partitions; matched 120-epoch caps.",
                         0.6, 6.58, 12.1, 0.4, size=12)
            else:
                add_figure(slide, fig, "fig_followup_native_controls")
                add_text(slide, fig, "Protected-gallery matching is distinct from learned linkage. Radial sensitivity does not establish natural norm leakage.",
                         0.6, 6.58, 12.1, 0.4, size=12)
            slide.notes_slide.notes_text_frame.text = (
                "Evidence baseline: commit 655ae1ecc2c9fc0aa80c828fe0303753296f66df. "
                "FEI run recorded base commit d1e4ceb3f975fb47d9a8321c47484bb1411f5239 with FEI additions uncommitted.\n"
                "Sources: experiments/cross_dataset_key_pool_summary.csv; experiments/fei_multiexposure/README.md; "
                "experiments/mobio_mechanism_controls/results_summary.csv; experiments/mobio_correlation_controls/results_summary.csv.\n"
                "Configuration: configs/attacks/fei_key_pool_boundary.yaml. See reports/figures/README.md for figure captions "
                "and docs/ROADMAP.md for pending gates. Diagram symbols are schematic, not biometric examples.\n"
                "New pilot code freeze: d5f4e89. Configuration: configs/attacks/scheme_extension_pilot.yaml. "
                "Sources: experiments/scheme_extension_pilot/{results_summary,paired_uncertainty,equivalence_sensitivity,native_utility}.csv. "
                "SCface protocol and pilot freeze: 69a93e4; sources under experiments/scface_multiexposure and "
                "experiments/scface_scheme_extension_pilot. "
                "One-seed CPU pilots, 120-epoch cap; not a controlled ranking against earlier 400-epoch, three-seed studies. "
                "See figure_appendix.pdf for all figures, including native matching and uncertainty."
                " Follow-up: experiments/scheme_followup_2026-09-18; 216 endpoints, two identity partitions, three model seeds. "
                "Pre-execution source/config hashes: execution_manifest.json; base commit 4352eeb, dirty working tree recorded. "
                "Primary sign-flip tests: Holm family 8; native gallery-label permutations: Holm family 12."
            )
            pdf.savefig(fig)
            plt.close(fig)
    presentation.save(out / "research_review.pptx")
    with pdfium.PdfDocument.new() as appendix:
        for source in sorted(FIGURES.glob("fig_*.pdf")):
            with pdfium.PdfDocument(source) as document:
                appendix.import_pages(document)
        appendix.save(out / "figure_appendix.pdf")
    print(f"8-slide review deck, PDF, and complete figure appendix -> {out}")


def build_dataset_update(destination: Path) -> None:
    from pypdf import PdfReader, PdfWriter, Transformation

    table = pd.read_csv(ROOT / "experiments/cross_dataset_key_pool_summary.csv")
    scface = table[table["dataset"] == "SCface"].set_index("pool_size")
    pilot_dirs = [ROOT / "experiments" / name for name in
                  ("scheme_extension_pilot", "scface_scheme_extension_pilot")]
    pilots = pd.concat([pd.read_csv(folder / "results_summary.csv") for folder in pilot_dirs])
    paired = pd.concat([pd.read_csv(folder / "paired_uncertainty.csv") for folder in pilot_dirs])
    gains = paired[(paired["condition"] == "random_key_pool_4") &
                   (paired["model"] == "mean_mlp") & (paired["contrast"] == "ten_minus_one")]
    native = pd.concat([pd.read_csv(folder / "native_utility.csv") for folder in pilot_dirs])
    fresh_native = native[(native["scheme"] == "PolyProtect") &
                          (native["condition"] == "independent_unseen_keys")].set_index("dataset")
    followup = ROOT / "experiments/scheme_followup_2026-09-18"
    contrasts = pd.read_csv(followup / "seed_identity_contrasts.csv")
    primary = contrasts[contrasts["primary"]]
    native_controls = pd.read_csv(followup / "native_null_controls.csv")
    endpoints = pd.read_csv(followup / "seed_identity_endpoints.csv")
    model_runs = pd.read_csv(followup / "results_summary.csv")
    titles = ["September dataset and experiment update", "Experimental architecture",
              "Detailed attacker: aggregation and reconstruction", "Cross-dataset key-reuse boundary",
              "Mechanism controls and interpretation", "Multi-seed, multi-partition validation",
              "Native linkage and radial sensitivity", "Earlier cross-dataset scheme pilots",
              "Findings and study scope"]
    figure_names = {2: "fig_architecture", 3: "fig_attack_detail", 4: "fig_results_overview", 5: "fig_controls",
                    6: "fig_followup_amplification", 7: "fig_followup_native_controls", 8: "fig_scheme_pilots"}
    presentation = Presentation()
    writer = PdfWriter()
    for number, title in enumerate(titles, start=1):
        slide = presentation.slides.add_slide(presentation.slide_layouts[6])
        fig = plt.figure(figsize=(WIDTH, HEIGHT), dpi=120, facecolor="white")
        add_text(slide, fig, title, 0.6, 0.3, 12.1, 0.6, size=25, bold=True)
        add_text(slide, fig, f"18 September 2026 | Base commit: 4352eeb; follow-up source/config hashes recorded | {number}/{len(titles)}",
                 0.6, 7.07, 12.1, 0.3, size=11, color="#666666")
        if number == 1:
            add_text(slide, fig, "Identity-disjoint evaluation across session, pose and camera variation.",
                     0.6, 1.15, 12.1, 0.5, size=17)
            rows = [
                ["Dataset", "Identities", "Train / val / test", "Valid / selected", "Variation"],
                ["MOBIO", "150", "90 / 30 / 30", "1,799 / 1,800", "Sessions"],
                ["LFW", "125", "75 / 25 / 25", "1,500 / 1,500", "In-the-wild"],
                ["FEI", "200", "120 / 40 / 40", "2,378 / 2,400", "Pose / expression"],
                ["SCface", "130", "78 / 26 / 26", "2,851 / 2,860", "Camera / distance"],
            ]
            for row_index, row in enumerate(rows):
                for column, value in enumerate(row):
                    add_text(slide, fig, value, [0.6, 2.4, 4.15, 7.2, 9.9][column], 1.95 + row_index * 0.48,
                             [1.7, 1.7, 2.9, 2.6, 2.8][column], 0.45, size=14, bold=row_index == 0)
            add_text(slide, fig,
                     "SCface: mugshot-to-surveillance linkage under capture-domain shift.\n"
                     "Mugshot gallery / surveillance exposures; all 130 identities remain eligible after 9 detection failures.\n"
                     "Unprotected SCface top-1: 84.375% over 544 test probes; chance: 1/26 = 3.846%.\n"
                     f"Evidence: {len(table)} key-pool conditions / {table['source_file'].nunique()} studies; "
                     f"{len(pilots)} one-seed model endpoints / 24 scheme pilot cells.\n"
                     f"New MOBIO/FEI follow-up: {len(model_runs)} trained endpoints; 3 model seeds x 2 identity partitions.",
                     0.6, 4.55, 12.1, 1.95, size=15)
        elif number == 2:
            add_text(slide, fig, "System overview: fixed encoder, hidden-key protection, same-identity exposure sets and held-out gallery linkage.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 3:
            add_text(slide, fig, "Mean pooling is the primary endpoint; DeepSets is secondary. Target is the normalized mean of exposed embeddings, not the gallery.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 4:
            add_text(slide, fig,
                     f"SCface: pool 3 rises from {100 * scface.loc['3', 'one_record_top1_mean']:.2f}% to "
                     f"{100 * scface.loc['3', 'top1_mean']:.2f}% top-1; fresh keys give {100 * scface.loc['fresh', 'top1_mean']:.2f}%.\n"
                     "SCface pools 1/2/3 pass the all-seed interval criterion; 4/5/7/10 fail. Failure is not equivalence.",
                     0.6, 1.05, 12.1, 0.65, size=14)
            add_text(slide, fig, f"{len(table)} conditions / {table['source_file'].nunique()} source-separated, three-seed studies. Grey: unavailable. *: interval failure. Pilots excluded.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 5:
            add_text(slide, fig,
                     "MOBIO: slot labels change DeepSets by -0.83 to +4.44 points; shuffled records collapse to 3.33% chance.\n"
                     "Same-image fresh-key sets also give 3.33%. Projection-sharing effects depend on construction and partition.",
                     0.6, 1.05, 12.1, 0.65, size=14)
            add_text(slide, fig, "Sources: experiments/mobio_mechanism_controls and mobio_correlation_controls. Three model seeds; chance 1/30.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 6:
            add_text(slide, fig, f"{len(model_runs)} trained endpoints; fresh, shared and pool-4 keys; 3 model seeds x 2 identity partitions.\n"
                     f"All {len(primary)} planned pool-4 amplification tests pass Holm correction (maximum adjusted p = {primary['holm_p'].max():.3f}).",
                     0.6, 1.05, 12.1, 0.65, size=14)
            add_text(slide, fig, "Matched 120-epoch caps. Crossed-bootstrap intervals include model-seed and identity resampling within each partition.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 7:
            add_text(slide, fig,
                     f"Fresh PolyProtect native identification exceeds the gallery-label null in {len(native_controls)} / {len(native_controls)} tests.\n"
                     f"Maximum Holm-adjusted p = {native_controls['holm_p'].max():.3f}; three fresh-key seeds per dataset and identity partition.",
                     0.6, 1.05, 12.1, 0.65, size=14)
            add_text(slide, fig, "IoM-GRP is invariant to the tested positive scales. PolyProtect is scale-sensitive; natural norm leakage was not tested.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 8:
            values = " / ".join(f"{100 * fresh_native.loc[dataset, 'native_top1']:.2f}%" for dataset in ("MOBIO", "FEI", "SCface"))
            add_text(slide, fig, f"Earlier one-seed pilots: {len(pilots)} model endpoints on MOBIO / FEI / SCface, including pool 8.\n"
                     f"Separate native fresh-key PolyProtect diagnostic: {values} top-1, respectively.",
                     0.6, 1.05, 12.1, 0.65, size=14)
            add_text(slide, fig, "Pilot intervals condition on one seed and partition; not confirmation. New replicated MOBIO/FEI results are on page 6.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        else:
            add_text(slide, fig,
                     "TRANSFORM REUSE AND RECORD MULTIPLICITY\n"
                     "Recurring hidden transforms support substantial identity linkage from multiple protected records.\n"
                     "The transition depends on dataset and identity partition, rather than a universal pool-size threshold.\n"
                     "SCface pool 3: 5.29% single-record versus 33.17% ten-record top-1; chance is 3.846%.\n\n"
                     "MECHANISM\n"
                     "Shuffled-identity sets remove the MOBIO gain; record count alone does not explain the effect.\n"
                     "Slot-label controls and partial projection sharing separate transform reuse from key disclosure.\n"
                     "Mean pooling and DeepSets test aggregation at the template and learned-feature levels.\n\n"
                     "STATISTICAL AND THREAT-MODEL SCOPE\n"
                     "BioHash evidence spans four datasets and three model seeds per study.\n"
                     f"New scheme follow-up: {len(model_runs)} endpoints; all {len(primary)} primary contrasts pass Holm correction.\n"
                     "Native protected-gallery matching and learned embedding linkage measure different attack surfaces.\n"
                     "Fresh-key learned intervals include chance; they do not establish equivalence or general unlinkability.\n\n"
                     "Scope: fixed key/set seeds for training; two overlapping identity assignments; SCface remains one-seed for new schemes.\n"
                     "Follow-up protocol and pre-execution hashes: experiments/scheme_followup_2026-09-18/execution_manifest.json.",
                     0.6, 1.15, 12.1, 5.45, size=14)
        buffer = BytesIO()
        fig.savefig(buffer, format="pdf")
        plt.close(fig)
        buffer.seek(0)
        page = writer.add_page(PdfReader(buffer).pages[0])
        if number in figure_names:
            source = PdfReader(FIGURES / f"{figure_names[number]}.pdf").pages[0]
            top = 1.05 if number in (2, 3) else 1.9
            available_height = 5.3 if number in (2, 3) else 4.5
            scale = min(12.1 * 72 / float(source.mediabox.width), available_height * 72 / float(source.mediabox.height))
            left = 0.6 * 72 + (12.1 * 72 - float(source.mediabox.width) * scale) / 2
            bottom = (HEIGHT - top - available_height) * 72 + (available_height * 72 - float(source.mediabox.height) * scale) / 2
            page.merge_transformed_page(source, Transformation().scale(scale).translate(left, bottom))
    writer.add_metadata({"/Title": "September Dataset Update - 18 September 2026",
                         "/Subject": "Identity-disjoint multi-record linkage: architecture, results and study scope"})
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp.pdf")
    writer.write(temporary)
    temporary.replace(destination)
    print(f"{len(titles)}-page vector dataset update -> {destination}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "reports/slides")
    parser.add_argument("--dataset-update", type=Path, default=ROOT / "reports/Sept_Dataset_Update.pdf")
    args = parser.parse_args()
    build_presentation(args.out)
    build_dataset_update(args.dataset_update)


if __name__ == "__main__":
    main()
