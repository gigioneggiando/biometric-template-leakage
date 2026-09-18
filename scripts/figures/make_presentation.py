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
            "What changes between key regimes?",
            "Earlier three-seed key-pool studies",
            "Mechanism and correlation controls",
            "Approved scheme pilots: one seed",
            "Ready to draft; not yet ready to submit",
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
                add_text(slide, fig, "Independent study. No exact benchmark reproduction or universal privacy claim.",
                         0.6, 6.3, 12.1, 0.45, size=13)
            elif number in (2, 4, 5, 6):
                name, caption = {
                    2: ("fig_architecture", "Train on separate identities. Reconstruct an embedding, then link to a held-out gallery."),
                    4: ("fig_threat_model", "Key values stay hidden in every regime. Recurring transforms are shared across identity splits."),
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
                         "IoM-GRP: 300 categorical codes (q=16); MOBIO/FEI/SCface pilots.\n"
                         "PolyProtect: 170 real values (m=5, overlap=2); MOBIO/FEI/SCface pilots.",
                         0.6, 4.15, 12.1, 1.85, size=16)
                add_text(slide, fig, "SCface: mugshot gallery and visible surveillance probes; 9 detection failures, all identities eligible.",
                         0.6, 6.3, 12.1, 0.45, size=13)
            elif number == 7:
                add_figure(slide, fig, "fig_scheme_pilots")
                native = pd.read_csv(ROOT / "experiments/scheme_extension_pilot/native_utility.csv")
                native = native[(native["scheme"] == "PolyProtect") & (native["condition"] == "independent_unseen_keys")].set_index("dataset")
                scface_native = pd.read_csv(ROOT / "experiments/scface_scheme_extension_pilot/native_utility.csv")
                scface_native = scface_native[(scface_native["scheme"] == "PolyProtect") &
                                              (scface_native["condition"] == "independent_unseen_keys")].iloc[0]
                caveat = (f"Fresh PolyProtect native top-1: MOBIO {100 * native.loc['MOBIO', 'native_top1']:.2f}%, "
                          f"FEI {100 * native.loc['FEI', 'native_top1']:.2f}%, "
                          f"SCface {100 * scface_native['native_top1']:.2f}%; separate diagnostic.")
                add_text(slide, fig, caveat,
                         0.6, 6.58, 12.1, 0.4, size=12)
            else:
                add_text(slide, fig, "Completed: two added datasets, two new schemes, 24 pilot cells, paired intervals.",
                         0.6, 1.4, 12.1, 0.6, size=17)
                add_text(slide, fig, "Before submission:\n"
                         "1. Freeze and authorize staged confirmation; one-seed pilots are not confirmation.\n"
                         "2. Decide whether AgeDB adds enough value for a third added dataset.\n"
                         "3. Approve statistical margins and a multiple-comparison plan.\n"
                         "4. Independently review the corrected theorem and related work.\n"
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
                "and docs/ROADMAP.md for pending gates. Diagram symbols are schematic, not biometric examples.\n"
                "New pilot code freeze: d5f4e89. Configuration: configs/attacks/scheme_extension_pilot.yaml. "
                "Sources: experiments/scheme_extension_pilot/{results_summary,paired_uncertainty,equivalence_sensitivity,native_utility}.csv. "
                "SCface protocol and pilot freeze: 69a93e4; sources under experiments/scface_multiexposure and "
                "experiments/scface_scheme_extension_pilot. "
                "One-seed CPU pilots, 120-epoch cap; not a controlled ranking against earlier 400-epoch, three-seed studies. "
                "See figure_appendix.pdf for all figures, including native matching and uncertainty."
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
    inventory = pd.read_csv(ROOT / "experiments/multiexposure_run_matrix.csv")
    titles = ["September dataset and experiment update", "Experimental architecture",
              "Model definitions and evaluation protocol", "Cross-dataset key-reuse boundary",
              "Mechanism controls and interpretation", "Additional schemes: one-seed pilots",
              "Paired multi-record gains and uncertainty", "Native matching is a separate diagnostic",
              "Evidence provenance and submission gates"]
    figure_names = {2: "fig_architecture", 4: "fig_results_overview", 5: "fig_controls",
                    6: "fig_scheme_pilots", 7: "fig_pilot_uncertainty", 8: "fig_pilot_native_utility"}
    presentation = Presentation()
    writer = PdfWriter()
    for number, title in enumerate(titles, start=1):
        slide = presentation.slides.add_slide(presentation.slide_layouts[6])
        fig = plt.figure(figsize=(WIDTH, HEIGHT), dpi=120, facecolor="white")
        add_text(slide, fig, title, 0.6, 0.3, 12.1, 0.6, size=25, bold=True)
        add_text(slide, fig, f"18 September 2026 | Commit: 4352eeb | Research draft | {number}/{len(titles)}",
                 0.6, 7.07, 12.1, 0.3, size=11, color="#666666")
        if number == 1:
            add_text(slide, fig, "Four multi-exposure datasets; FEI and SCface complete the two-added-dataset target.",
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
                     "SCface access supplied by Sani on 2026-09-18; acquisition is complete.\n"
                     "Mugshot gallery / surveillance exposures; all 130 identities remain eligible after 9 detection failures.\n"
                     "Unprotected SCface top-1: 84.375% over 544 test probes; chance: 1/26 = 3.846%.\n"
                     f"Evidence: {len(table)} key-pool conditions / {table['source_file'].nunique()} studies; "
                     f"{len(pilots)} one-seed model endpoints / 24 scheme pilot cells.\n"
                     "AgeDB is optional and not acquired. Multi-seed scheme confirmation remains open.",
                     0.6, 4.55, 12.1, 1.95, size=15)
        elif number == 2:
            add_text(slide, fig, "Icons are schematic; no biometric images or secret keys are included. Detailed model definitions follow.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 3:
            add_text(slide, fig,
                     "INPUTS AND MODELS\n"
                     "T: batch x n x d. Single MLP: d -> 256 -> ReLU -> 512 -> L2 normalization.\n"
                     "Mean / max MLP: pool records first, then the same MLP. Key-pool endpoint: mean MLP.\n"
                     "DeepSets phi: d -> 256 -> ReLU -> 256 -> ReLU; masked mean across records.\n"
                     "DeepSets rho: 256 -> 256 -> ReLU -> 512 -> L2 normalization; permutation-invariant.\n"
                     "BioHash: 128 bits. MLP-Hash: 512 bits. IoM-GRP: 300 codes, q=16, one-hot d=4,800.\n"
                     "PolyProtect: 170 real values; window 5, overlap 2; outside the rotational-invariance theorem.\n\n"
                     "TRAINING AND EVALUATION\n"
                     "Paired source embeddings supervise training; loss = mean(1 - cosine) + 0.1 x MSE.\n"
                     "Adam: learning rate 0.001, weight decay 0.0001; best validation-loss checkpoint.\n"
                     "SCface BioHash: 3 seeds, 400-epoch cap, patience 60. Scheme pilots: 1 seed, 120 / 30.\n"
                     "Eight nested sets per identity; gallery image excluded. Test identities never used for training.\n"
                     "Fresh keys: source-record and split-disjoint. Recurring pools deliberately reuse hidden transforms.\n"
                     "Cosine gallery linkage; top-1/top-5, AUROC, EER, TAR; 2,000 identity-bootstrap resamples.\n"
                     "95% intervals condition on the identity partition/model seed; no multiplicity adjustment.",
                     0.6, 1.15, 12.1, 5.25, size=14)
            add_text(slide, fig, "Sources: src/biometrics_ai/aggregation/models.py; scripts/train/run_real_multiexposure.py; configs/attacks/scface*.yaml",
                     0.6, 6.58, 12.1, 0.4, size=10)
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
            add_text(slide, fig, f"{len(pilots)} model endpoints: MOBIO / FEI / SCface; IoM-GRP / PolyProtect; pools 1/4/8 and fresh keys.",
                     0.6, 1.05, 12.1, 0.4, size=14)
            add_text(slide, fig, "One seed per endpoint, 120-epoch cap. No controlled ranking against earlier three-seed, 400-epoch studies.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 7:
            values = gains[gains["dataset"] == "SCface"].set_index("scheme")
            add_text(slide, fig,
                     f"SCface pool-4 mean-pool gains: IoM-GRP +{100 * values.loc['IoM-GRP', 'estimate']:.2f} points; "
                     f"PolyProtect +{100 * values.loc['PolyProtect', 'estimate']:.2f} points.",
                     0.6, 1.05, 12.1, 0.4, size=14)
            add_text(slide, fig, "Paired 95% identity-bootstrap intervals, conditional on one seed/partition; unadjusted. These are pilots, not confirmation.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        elif number == 8:
            values = " / ".join(f"{100 * fresh_native.loc[dataset, 'native_top1']:.2f}%" for dataset in ("MOBIO", "FEI", "SCface"))
            add_text(slide, fig, f"Fresh-key PolyProtect native top-1: {values} on MOBIO / FEI / SCface.\n"
                     "Above-chance native identification needs investigation; learned attacks near chance do not imply unlinkability.",
                     0.6, 1.05, 12.1, 0.65, size=14)
            add_text(slide, fig, "Protected-gallery diagnostic with different probes; not the learned unprotected-gallery endpoint. No universal privacy claim.",
                     0.6, 6.58, 12.1, 0.4, size=12)
        else:
            add_text(slide, fig,
                     "PROVENANCE\n"
                     "Latest result integration: 4352eeb (2026-09-18). SCface protocol freeze: 69a93e4.\n"
                     "MOBIO / FEI scheme pilot freeze: d5f4e89 (2026-09-12). Original run dates remain unchanged.\n"
                     "Sources: experiments/cross_dataset_key_pool_summary.csv and both scheme pilot directories.\n"
                     f"Local per-seed inventory: {len(inventory)} rows / {inventory['source_metrics'].nunique()} artifacts; SCface absent locally.\n"
                     "All 12 current vector figures: reports/slides/figure_appendix.pdf; regenerators: scripts/figures/.\n\n"
                     "REQUIRED BEFORE SUBMISSION\n"
                     "1. Authorize and freeze multi-seed, multi-partition confirmation with matched training budgets.\n"
                     "2. Approve equivalence margins and a seed-uncertainty / multiple-comparison plan.\n"
                     "3. Investigate native PolyProtect linkage and norm-sensitive controls; reconcile historical coverage.\n"
                     "4. Obtain independent novelty, theorem and implementation review, then Sani's scientific review.\n"
                     "5. Select a venue and check its reporting, reproducibility, ethics and dataset-use requirements.\n\n"
                     "A/A* is a venue ambition, not a verified quality label or acceptance prediction.\n"
                     "No source-exact benchmark reproduction, confirmation, or universal privacy result is claimed.",
                     0.6, 1.15, 12.1, 5.45, size=14)
        buffer = BytesIO()
        fig.savefig(buffer, format="pdf")
        plt.close(fig)
        buffer.seek(0)
        page = writer.add_page(PdfReader(buffer).pages[0])
        if number in figure_names:
            source = PdfReader(FIGURES / f"{figure_names[number]}.pdf").pages[0]
            top = 1.05 if number == 2 else 1.9
            available_height = 5.3 if number == 2 else 4.5
            scale = min(12.1 * 72 / float(source.mediabox.width), available_height * 72 / float(source.mediabox.height))
            left = 0.6 * 72 + (12.1 * 72 - float(source.mediabox.width) * scale) / 2
            bottom = (HEIGHT - top - available_height) * 72 + (available_height * 72 - float(source.mediabox.height) * scale) / 2
            page.merge_transformed_page(source, Transformation().scale(scale).translate(left, bottom))
    writer.add_metadata({"/Title": "September Dataset Update - 18 September 2026",
                         "/Subject": "Four-dataset evidence update; one-seed pilots; submission gates"})
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
