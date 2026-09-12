"""Build an editable review deck and matching PDF without biometric images."""
from __future__ import annotations

from pathlib import Path
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import pandas as pd
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
    presentation.core_properties.subject = "Research review draft, 2026-09-12"
    with PdfPages(out / "research_review.pdf") as pdf:
        for number, title in enumerate([
            "Hidden keys and repeated biometric records",
            "Experimental architecture",
            "Dataset and protection coverage",
            "What changes between key regimes?",
            "All completed key-pool studies",
            "Mechanism and correlation controls",
            "Fresh-key endpoints across datasets",
            "Ready to draft; not yet ready to submit",
        ], start=1):
            slide = presentation.slides.add_slide(presentation.slide_layouts[6])
            fig = plt.figure(figsize=(WIDTH, HEIGHT), dpi=120, facecolor="white")
            add_text(slide, fig, title, 0.6, 0.3, 12.1, 0.6, size=25, bold=True)
            add_text(slide, fig, f"Research review draft | 12 September 2026 | {number}/8", 0.6, 7.07, 12.1, 0.3, size=11, color="#666666")
            if number == 1:
                add_text(slide, fig, "Can multiple protected records reveal identity when keys remain hidden?",
                         0.6, 1.45, 12.1, 0.7, size=20)
                add_text(slide, fig, "Fresh independent keys: chance-compatible results in the tested attacks.\n\n"
                         "Recurring transforms: large gains from multiple same-identity records.\n\n"
                         "Boundary location changes with the dataset and identity partition.",
                         0.6, 2.55, 12.1, 3.1, size=19)
                add_text(slide, fig, "Independent study. No exact benchmark reproduction or universal privacy claim.",
                         0.6, 6.3, 12.1, 0.45, size=13)
            elif number in (2, 4, 5, 6):
                name, caption = {
                    2: ("fig_architecture", "Train on separate identities. Reconstruct an embedding, then link to a held-out gallery."),
                    4: ("fig_threat_model", "Key values stay hidden in every regime. Recurring transforms are shared across identity splits."),
                    5: ("fig_results_overview", "65 conditions from 11 studies. Missing endpoints stay blank; interval failures remain visible."),
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
                ]
                for row_index, row in enumerate(rows):
                    for column, value in enumerate(row):
                        add_text(slide, fig, value, [0.6, 2.6, 4.6, 7.1, 10.0][column], 1.5 + row_index * 0.58,
                                 [1.8, 1.8, 2.3, 2.7, 2.7][column], 0.5, size=15, bold=row_index == 0)
                add_text(slide, fig, "BioHash: 128 bits; all three datasets.\n"
                         "MLP-Hash: 512 bits; MOBIO only; paper-specified, not source-exact.\n"
                         "Haar-sign-corrected BioHash: MOBIO implementation control.",
                         0.6, 4.35, 12.1, 1.6, size=17)
                add_text(slide, fig, "FEI: 22 low-illumination failures; all identities retain a gallery image plus 10 exposures.",
                         0.6, 6.3, 12.1, 0.45, size=13)
            elif number == 7:
                add_figure(slide, fig, "fig_fresh_exposures", x=0.4, y=1.3, width=6.1, height=4.9)
                lines = ["BioHash, 10-record mean-pool endpoint:"]
                sources = [("MOBIO", "key_pool_split_replication_summary.csv"), ("LFW", "key_pool_boundary_summary.csv"), ("FEI", "key_pool_boundary_summary.csv")]
                for dataset, source in sources:
                    row = table[(table["dataset"] == dataset) & (table["pool_size"] == "fresh") & table["source_file"].str.endswith("/" + source)].iloc[0]
                    lines.append(f"{dataset}: {100 * row['top1_mean']:.2f}% (chance {100 / row['test_identities']:.2f}%)")
                add_text(slide, fig, "\n\n".join(lines), 6.8, 1.8, 5.9, 3.4, size=15)
                add_text(slide, fig, "Chance inclusion is not equivalence.\nNo universal privacy guarantee.",
                         6.8, 5.4, 5.9, 0.9, size=16, bold=True)
            else:
                add_text(slide, fig, "Completed: three datasets, two schemes on MOBIO, reuse and mechanism controls.",
                         0.6, 1.4, 12.1, 0.6, size=17)
                add_text(slide, fig, "Before submission:\n"
                         "1. Approve and obtain the next dataset; approve two additional schemes.\n"
                         "2. Freeze the extension protocol, then run pilots and confirmation.\n"
                         "3. Define equivalence margins; strengthen paired uncertainty analysis.\n"
                         "4. Review theory, finite-key assumptions, norm controls and novelty.\n"
                         "5. Obtain Sani's scientific and presentation review.",
                         0.6, 2.35, 12.1, 3.4, size=17)
                add_text(slide, fig, "A/A* is a venue ambition, not an established property or an acceptance prediction.",
                         0.6, 6.3, 12.1, 0.45, size=13)
            slide.notes_slide.notes_text_frame.text = (
                "Evidence baseline: commit 655ae1ecc2c9fc0aa80c828fe0303753296f66df. "
                "FEI run recorded base commit d1e4ceb3f975fb47d9a8321c47484bb1411f5239 with FEI additions uncommitted.\n"
                "Sources: experiments/cross_dataset_key_pool_summary.csv; experiments/fei_multiexposure/README.md; "
                "experiments/mobio_mechanism_controls/results_summary.csv; experiments/mobio_correlation_controls/results_summary.csv.\n"
                "Configuration: configs/attacks/fei_key_pool_boundary.yaml. See reports/figures/README.md for figure captions "
                "and docs/ROADMAP.md for pending gates. Diagram symbols are schematic, not biometric examples."
            )
            pdf.savefig(fig)
            plt.close(fig)
    presentation.save(out / "research_review.pptx")
    print(f"8-slide review deck and PDF -> {out}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "reports/slides")
    build_presentation(parser.parse_args().out)


if __name__ == "__main__":
    main()