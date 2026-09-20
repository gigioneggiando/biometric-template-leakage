"""Build a plain one-page venue handout for the research supervisor."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "reports/Paper_Submission_Venues_2026.pdf"


def build_pdf(destination: Path = OUTPUT) -> None:
    rows = [
        ("IEEE T-BIOM", "Submit now", "Rolling. No annual deadline.", "Best fit"),
        ("IEEE TIFS", "Submit now", "Rolling. No annual deadline.", "Ambitious"),
        ("Pattern Recognition", "Submit now", "Rolling. No annual deadline.", "Possible"),
        ("Computers & Security", "Submit now", "Rolling. No annual deadline.", "Good alternative"),
        ("IJCB 2026", "Closed", "10 April 2026. Deadline passed.", "Best conference fit"),
        ("IJCB 2027", "Wait for call", "Not announced as of 20 Sep 2026.", "Future option"),
    ]
    text = "\n".join(value for row in rows for value in row)
    if not text.isascii():
        raise ValueError("Handout text must use simple ASCII characters")

    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    fig.text(0.08, 0.93, "Where we can submit the paper", fontsize=22, weight="bold", family="DejaVu Sans")
    fig.text(0.08, 0.895, "Simple venue and deadline sheet for supervisor review", fontsize=11,
             family="DejaVu Sans", color="#444444")
    fig.text(0.92, 0.895, "20 September 2026", fontsize=10, family="DejaVu Sans",
             color="#444444", ha="right")

    column_labels = ["Venue", "When", "Due date", "Fit for this paper"]
    table = ax.table(
        cellText=rows,
        colLabels=column_labels,
        colWidths=[0.25, 0.16, 0.36, 0.23],
        cellLoc="left",
        colLoc="left",
        bbox=[0.08, 0.43, 0.84, 0.41],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    for (row, column), cell in table.get_celld().items():
        cell.set_edgecolor("#B8B8B8")
        cell.set_linewidth(0.7)
        cell.PAD = 0.04
        cell.get_text().set_fontfamily("DejaVu Sans")
        cell.get_text().set_wrap(True)
        if row == 0:
            cell.set_facecolor("#E8ECEF")
            cell.get_text().set_weight("bold")
        elif row == 1:
            cell.set_facecolor("#F1F7F3")
        else:
            cell.set_facecolor("white")

    fig.text(0.08, 0.36, "Recommended first choice", fontsize=13, weight="bold", family="DejaVu Sans")
    fig.text(0.08, 0.325,
             "Submit to IEEE T-BIOM after the professor and coauthors complete the final scientific review.",
             fontsize=10.5, family="DejaVu Sans")
    fig.text(0.08, 0.285,
             "Why: the paper is mainly about biometric template security, privacy, and identity linkage.",
             fontsize=10.5, family="DejaVu Sans")

    fig.text(0.08, 0.225, "Before submission", fontsize=13, weight="bold", family="DejaVu Sans")
    checks = [
        "1. Confirm the final claims, references, ethics statement, and permitted data use.",
        "2. Format the manuscript using the chosen venue's current author instructions.",
        "3. Submit to only one venue at a time.",
        "4. Recheck the venue website on submission day in case its rules changed.",
    ]
    for index, line in enumerate(checks):
        fig.text(0.08, 0.19 - index * 0.032, line, fontsize=10, family="DejaVu Sans")

    fig.text(0.08, 0.045,
             "Rolling means regular journal papers can be submitted throughout the year. It does not guarantee fast review or acceptance.",
             fontsize=8.5, family="DejaVu Sans", color="#444444")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, format="pdf", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build_pdf()
    print(f"One-page venue sheet -> {OUTPUT}")