"""Build a standalone static-analysis addendum from frozen aggregate results."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/static_policy_2026-09-25"


def load_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def page(title: str, number: int):
    figure = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    figure.text(.07, .95, title, fontsize=20, weight="bold", va="top", family="DejaVu Serif")
    figure.text(.07, .91, "KEY-SCOPE STATIC ANALYSIS  |  RESEARCH ADDENDUM  |  25 SEPTEMBER 2026",
                fontsize=8, color="#52615a")
    figure.text(.07, .035, f"Exploratory independent study | Not a security certificate | {number}/3",
                fontsize=8, color="#52615a")
    return figure


def paragraph(figure, top: float, title: str, content: str) -> None:
    figure.text(.07, top, title, fontsize=12, weight="bold", va="top")
    wrapped = "\n".join(textwrap.fill(line, width=91) for line in content.split("\n"))
    figure.text(.07, top - .03, wrapped, fontsize=10, va="top", linespacing=1.5)


def table(figure, box: list[float], columns: list[str], rows: list[list[str]], widths: list[float]):
    axis = figure.add_axes(box)
    axis.axis("off")
    result = axis.table(cellText=rows, colLabels=columns, colWidths=widths,
                        cellLoc="left", colLoc="left", bbox=[0, 0, 1, 1])
    result.auto_set_font_size(False)
    result.set_fontsize(9)
    for (row, _), cell in result.get_celld().items():
        cell.set_edgecolor("#d3d9d5")
        cell.set_linewidth(.4)
        if row == 0:
            cell.set_facecolor("#e8eeeb")
            cell.set_text_props(weight="bold")
    return result


def build_report(destination: Path) -> None:
    effects = load_rows(STUDY / "policy_effects.csv")
    primary = [row for row in effects if row["primary"] == "True"]
    native = [row for row in load_rows(STUDY / "native_utility.csv") if row["condition"] == "independent_unseen_keys"]
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    if manifest["status"] != "completed" or len(primary) != 8 or len(native) != 8:
        raise ValueError("A complete frozen study is required")
    passed = sum(float(row["lower95"]) > 0 and float(row["holm_p"]) < .05 for row in primary)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({"font.family": "DejaVu Sans", "pdf.fonttype": 42}), PdfPages(destination) as output:
        figure = page("Static Analysis of Protection Policies", 1)
        paragraph(figure, .87, "Contribution and scope",
                  "KSSA v1 audits the experiment configuration before biometric data are loaded. It maps declared key "
                  "scope to explicit findings and proposes a separate fresh-key comparison. This is a configuration "
                  "analyzer, not a general source-code analyzer or a new biometric transform. Manish proposed this "
                  "direction for discussion with Sani; professor approval and research priority are not established.")
        paragraph(figure, .70, "Algorithm",
                  "1. Parse the YAML scheme/condition matrix; reject unsupported required fields.\n"
                  "2. Classify each pair: fresh-declared, shared across splits, shared projection, unknown.\n"
                  "3. Emit reuse, correlation, disclosure and scheme-assumption findings.\n"
                  "4. Block known policy risks; otherwise require review, never certify security.\n"
                  "5. Propose fresh keys and hide slot labels; preserve all other experimental settings.\n"
                  "Cost: O(S*C) scope classifications for S schemes and C conditions.")
        table(figure, [.07, .29, .86, .18], ["Finding", "Decision / interpretation"], [
            ["KEY_REUSE", "Block: hidden transforms recur across identity splits"],
            ["KEY_CORRELATION", "Block: a nonzero projection component is shared"],
            ["SLOT_DISCLOSURE", "Block: transform-group labels are exposed"],
            ["Unknown / malformed", "Block: unsupported policy cannot be certified"],
            ["PolyProtect / Haar assumptions", "Review: key freshness is insufficient evidence"],
            ["Runtime assumptions", "Review: secrecy, input norms and utility unverified"],
        ], [.38, .62])
        paragraph(figure, .25, "Prospective matched experiment",
                  "MOBIO and FEI; IoM-GRP and PolyProtect; two overlapping identity partitions; three model seeds; "
                  "one and ten records. Compare pool 4 with the analyzer-generated fresh-key candidate using the same "
                  "inputs, set seed, key seed, model seeds and training caps (120 epochs, patience 30). The mechanisms "
                  "produce different key draws. All 16 cells / 96 trained endpoints completed in "
                  f"{manifest['wall_seconds']:.2f} seconds, within the 3,600-second budget.")
        output.savefig(figure)
        plt.close(figure)

        figure = page("Measured Reduction in Learned Linkage", 2)
        paragraph(figure, .87, "Primary endpoint: pool 4 minus fresh, ten records",
                  f"{passed}/8 planned contrasts have positive paired 95% intervals and Holm-adjusted p < .05. "
                  "Each row uses three newly trained mean-pool MLP seeds. Intervals resample model seeds and identity "
                  "clusters; p-values use identity sign-flips of seed-mean differences. No security equivalence follows.")
        table_rows = [[row["dataset"], row["scheme"], row["split_seed"][-2:],
                       f"{100 * float(row['before_top1']):.2f}", f"{100 * float(row['after_top1']):.2f}",
                       f"{100 * float(row['reduction']):.2f}",
                       f"[{100 * float(row['lower95']):.2f}, {100 * float(row['upper95']):.2f}]"] for row in primary]
        table(figure, [.07, .50, .86, .23], ["Data", "Scheme", "Split*", "Before %", "After %", "Drop pp", "95% CI (pp)"],
              table_rows, [.10, .17, .08, .12, .12, .12, .29])
        figure.text(.07, .475, "*Split suffixes 31/43 denote seeds 92531/92543. All eight Holm p = 0.004.", fontsize=9)
        axis = figure.add_axes([.29, .17, .64, .26])
        for index, row in enumerate(primary):
            center = 100 * float(row["reduction"])
            axis.plot([100 * float(row["lower95"]), 100 * float(row["upper95"])], [index, index],
                      color="#28745c", linewidth=2)
            axis.plot(center, index, "o", color="#28745c")
        axis.set_yticks(range(len(primary)), [f"{row['dataset']} {row['scheme']} {row['split_seed'][-2:]}" for row in primary], fontsize=8)
        axis.invert_yaxis()
        axis.set_xlim(0, 102)
        axis.set_xlabel("Absolute reduction in top-1 linkage (percentage points)", fontsize=9)
        axis.grid(axis="x", color="#d3d9d5", linewidth=.5)
        axis.spines[["top", "right"]].set_visible(False)
        figure.text(.07, .09, "Chance: MOBIO 3.33%, FEI 2.50%. Every fresh learned CI includes chance; none proves equivalence.", fontsize=8.5)
        output.savefig(figure)
        plt.close(figure)

        figure = page("Residual Risk and Reproducibility", 3)
        paragraph(figure, .87, "Native cross-record linkage is a different endpoint",
                  "Fresh PolyProtect still has descriptive native top-1 above chance in both datasets. This new native "
                  "comparison is not null-tested or corrected. It supports retaining a review warning, not certifying "
                  "unlinkability. These are cosine comparisons of protected gallery/probe records, not authorized "
                  "authentication under compatible keys.")
        table(figure, [.07, .46, .86, .25], ["Dataset", "Scheme", "Split seed", "Native top-1 %", "Chance %"],
              [[row["dataset"], row["scheme"], row["split_seed"], f"{100 * float(row['native_top1']):.2f}",
                f"{100 * float(row['chance']):.2f}"] for row in native], [.15, .23, .18, .26, .18])
        paragraph(figure, .42, "What this evaluation does not establish",
                  "One pool draw, overlapping partitions, three model seeds and small closed galleries limit inference. "
                  "Baseline training uses paired access to the same hidden pool and known target grouping. Rules were "
                  "motivated by earlier results, not evaluated on a blinded vulnerability corpus. No general detection "
                  "accuracy, deployed authentication utility, new-transform superiority or universal privacy is claimed. "
                  "SCface was not rerun because its local embeddings were unavailable.")
        paragraph(figure, .24, "Audit trail and use",
                  "Protocol: docs/protocols/static_policy_2026-09-25.md\n"
                  "Results: experiments/static_policy_2026-09-25/README.md\n"
                  "CLI: python -m biometrics_ai.protection.policy --config <policy.yaml>\n"
                  "--enforce: exit 2 for blocking findings; exit 3 for unresolved review.\n"
                  "Source/config/input hashes and software versions were recorded before execution. Public research "
                  "seeds are not production secrets. Candidate policy changes require manual review and legitimate "
                  "matching validation. Original studies and the September report are preserved.")
        output.savefig(figure)
        plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/Static_Policy_Analysis_2026-09-25.pdf")
    args = parser.parse_args()
    build_report(args.out)
    print(f"Three-page static policy addendum: {args.out}")


if __name__ == "__main__":
    main()
