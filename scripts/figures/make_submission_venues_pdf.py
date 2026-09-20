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
        ("IEEE SaTML 2027", "Not listed", "22 Sep abstract; 29 Sep paper"),
        ("CVPR 2027", "CORE A*", "10 Nov register; 16 Nov paper"),
        ("IEEE S&P 2027", "CORE A*", "10 Nov register; 17 Nov paper"),
        ("PETS / PoPETs 2027", "CORE A", "Paper 30 Nov 2026"),
        ("USENIX Security 2027", "CORE A*", "19 Jan register; 26 Jan paper"),
    ]
    text = "\n".join(value for row in rows for value in row)
    if not text.isascii():
        raise ValueError("Handout text must use simple ASCII characters")

    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    fig.text(0.08, 0.94, "Possible places for our paper", fontsize=20, weight="bold", family="DejaVu Sans")
    fig.text(0.08, 0.905, "I checked the official calls and CORE 2023 rankings.", fontsize=10.5,
             family="DejaVu Sans", color="#333333")
    fig.text(0.92, 0.895, "20 September 2026", fontsize=10, family="DejaVu Sans",
             color="#444444", ha="right")

    column_labels = ["Conference", "Ranking", "Deadline"]
    table = ax.table(
        cellText=rows,
        colLabels=column_labels,
        colWidths=[0.32, 0.20, 0.48],
        cellLoc="left",
        colLoc="left",
        bbox=[0.08, 0.53, 0.84, 0.31],
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
        elif row == 4:
            cell.set_facecolor("#F1F7F3")
        else:
            cell.set_facecolor("white")

    fig.text(0.08, 0.465, "Our thoughts", fontsize=12, weight="bold", family="DejaVu Sans")
    note = (
        "PETS looks like the most realistic ranked conference for this paper. It is CORE A and its topic includes "
        "information leakage and privacy attacks. CVPR and IEEE S&P are CORE A*, but the current paper may not fit their "
        "main contribution well enough. SaTML fits the topic, but the deadline is very close and it is not listed in CORE 2023."
    )
    fig.text(0.08, 0.43, note, fontsize=10, family="DejaVu Sans", va="top", wrap=True)

    fig.text(0.08, 0.32, "Journal option", fontsize=12, weight="bold", family="DejaVu Sans")
    journal_note = (
        "IEEE T-BIOM is still my first journal choice because it directly covers biometric security. IEEE TIFS is another "
        "strong journal, but it has a higher security novelty bar. Both accept regular papers throughout the year. CORE A and "
        "A* are conference labels, so I did not give these journals a CORE rank."
    )
    fig.text(0.08, 0.285, journal_note, fontsize=10, family="DejaVu Sans", va="top", wrap=True)

    fig.text(0.08, 0.19, "Question for us", fontsize=12, weight="bold", family="DejaVu Sans")
    fig.text(0.08, 0.155,
             "Should we prepare for PETS by 30 November, or submit the longer version to IEEE T-BIOM?",
             fontsize=10.5, family="DejaVu Sans")
    fig.text(0.08, 0.115,
             "Before choosing, we should confirm which ranking list our department uses. CORE is not the only system.",
             fontsize=9.5, family="DejaVu Sans")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, format="pdf", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build_pdf()
    print(f"One-page venue sheet -> {OUTPUT}")