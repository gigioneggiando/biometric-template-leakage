"""Render the source-analysis and security/utility pilot, including failed gates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.figures.make_static_policy_report import load_rows, paragraph, table

STUDY = ROOT / "experiments/source_security_utility_2026-09-25"


def page(title: str, number: int):
    figure = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    figure.text(.07, .95, title, fontsize=20, weight="bold", va="top", family="DejaVu Serif")
    figure.text(.07, .91, "SOURCE ANALYSIS AND TRUSTED VERIFICATION  |  25 SEPTEMBER 2026",
                fontsize=8, color="#52615a")
    figure.text(.07, .035, f"Exploratory pilot | Independent review pending | {number}/4", fontsize=8, color="#52615a")
    return figure


def build_report(destination: Path) -> None:
    benchmark = json.loads((STUDY / "benchmark/summary.json").read_text())
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    effects = [row for row in load_rows(STUDY / "security_utility_effects.csv") if row["primary"] == "True"]
    if manifest["status"] != "completed" or len(effects) != 2:
        raise ValueError("Complete primary results required")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({"font.family": "DejaVu Sans", "pdf.fonttype": 42}), PdfPages(destination) as output:
        figure = page("Source-Level Key-Provenance Analysis", 1)
        paragraph(figure, .87, "What is implemented",
                  "A bounded Python AST interpreter traces the declared record identifier through assignments, "
                  "integer arithmetic, aliases and helper calls into protection sinks. It detects finite key pools "
                  "hidden by modulo/masking and shared matrix blocks assembled through concatenation. It does not "
                  "need a YAML condition name or execute the analyzed source.")
        table(figure, [.07, .52, .86, .18], ["Abstract value", "Meaning under the stated contracts"], [
            ["fixed", "Same value within the audited record context"],
            ["record-injective", "Distinct integer IDs give distinct idealized keys"],
            ["bounded(K)", "At most K values; reuse possible, not always observed"],
            ["unknown", "Unsupported behavior; never treated as securely fresh"],
        ], [.27, .73])
        paragraph(figure, .47, "Conditional soundness, not a certificate",
                  "An expression-by-expression induction supports fixedness, cardinality and injectivity only for "
                  "the supported straight-line subset, unique integer IDs, fixed context inputs, reviewed callee "
                  "contracts and an ideal collision-free KDF. Real research keys are 64-bit truncated hashes. "
                  "Freshness does not establish key secrecy, independent matrices, unlinkability or production safety.")
        paragraph(figure, .29, "Coverage and engineering checks",
                  "Branches, loops, recursion, dynamic calls and arbitrary numerical correlation are not modeled. "
                  "The existing branch-heavy experiment runner returns unknown; the three executable study recipes "
                  "are covered. Module-binding regressions found after execution were fixed; the executed analyzer "
                  "is archived with its original hash. All 24 benchmark predictions remain unchanged after the fix.")
        paragraph(figure, .15, "Research status",
                  "A domain-specific prototype, not a proven new general analysis method. Abstract interpretation "
                  "and key-freshness principles are established prior work; specialist priority review remains open.")
        output.savefig(figure)
        plt.close(figure)

        figure = page("Proposed Mathematical Construction", 2)
        paragraph(figure, .87, "Exposure reuse mass",
                  "Let E contain target-training and unordered target-target record pairs. Component j occupies "
                  "fraction w_j of the protected output; Z_rj identifies its realized transform for record r. "
                  "The proposed functional counts expected weighted repeated components, not leaked identity bits.")
        figure.text(.09, .72, r"$\mathcal{R}_E = \sum_{(r,s)\in E}\sum_j w_j\,\Pr[Z_{rj}=Z_{sj}]$", fontsize=17)
        figure.text(.09, .65, r"$\mathcal{R}_E = (nm+n(n-1)/2)\sum_j w_j/K_j$", fontsize=17)
        paragraph(figure, .60, "When the closed form applies",
                  "The second expression assumes IID uniform slots in pools K_j, n target records and m training "
                  "records. Ideal fresh components contribute zero; a fixed shared fraction rho gives |E|*rho. "
                  "Biased allocations require their actual collision probabilities. A capacity bound alone does "
                  "not give an upper privacy bound. A separate unweighted collision union bound is derived only "
                  "for independent hidden isotropic components; it is often vacuous and excludes PolyProtect "
                  "and the repository's dependent correlated-projection construction.")
        paragraph(figure, .37, "Utility-constrained acceptance criterion",
                  "L is attack top-1, U is legitimate TAR, F is legitimate FMR. A policy change is accepted only "
                  "if leakage falls, utility is noninferior within a fixed margin, and FMR stays below a ceiling.")
        figure.text(.09, .23, r"$\mathcal{G}_{\delta,\tau}=\mathbf{1}\{\mathrm{LCB}(L_b-L_c)>0\}$", fontsize=15)
        figure.text(.09, .185, r"$\quad\times\mathbf{1}\{\mathrm{LCB}(U_c-U_b)\geq-\delta\}$", fontsize=15)
        figure.text(.09, .14, r"$\quad\times\mathbf{1}\{\mathrm{UCB}(F_c)\leq\tau\}$", fontsize=15)
        figure.text(.07, .08, "These combine established expectation, coupling and noninferiority ideas; novelty is not certified.", fontsize=8.5)
        output.savefig(figure)
        plt.close(figure)

        figure = page("Benchmark and Independent-Review Gap", 3)
        paragraph(figure, .87, "24 source cases, two baseline approaches",
                  "A separate runtime oracle enumerates component keys for 64 record IDs per case. Source fixtures "
                  "include constants, affine/helper variants, hidden pools, shared prefixes, explicit matrix "
                  "assembly and unsupported constructs. All cases were authored in this session: these are "
                  "development/stress checks, not independently labeled or genuinely held-out evidence.")
        rows = []
        for label, key in [("Source interpreter", "source"), ("YAML checker", "configuration"), ("Bandit 1.8.6", "bandit")]:
            counts = benchmark["metrics"][key]
            rows.append([label, *[str(counts[field]) for field in ["tp", "fp", "tn", "fn", "abstain"]]])
        table(figure, [.07, .57, .86, .13], ["Method", "TP", "FP", "TN", "FN", "Abstain"], rows,
              [.40, .12, .12, .12, .12, .12])
        paragraph(figure, .52, "Do not hide abstentions",
                  "The source interpreter classifies 20/24 cases (83.3% coverage). It detects 13/17 observed-reuse "
                  "cases (76.5% when abstentions count as undetected), with four reuse cases left unknown. The "
                  "seven conditional-fresh cases have no repeated labels in this finite runtime domain; this is "
                  "not proof over every integer input or a real-world false-positive estimate.")
        paragraph(figure, .34, "What the baseline comparison means",
                  "The YAML baseline receives the same declared fresh-key condition, so it cannot see hidden "
                  "implementation changes. Bandit is a general Python security scanner, not a biometric-reuse "
                  "analyzer. Its one warning is B311 for a non-cryptographic RNG, not an inferred transform-reuse "
                  "finding. This comparison does not establish superiority over specialist static-analysis tools.")
        paragraph(figure, .15, "External validation still required",
                  "Case sources, runtime labels, predictions, raw Bandit JSON and a blank independent-reviewer "
                  "label column are exported. An external reviewer must supply labels and new constructions "
                  "without tuning the analyzer to them before journal-level generalization can be claimed.")
        output.savefig(figure)
        plt.close(figure)

        figure = page("Leakage Falls; Utility Gate Is Unmet", 4)
        paragraph(figure, .87, "Matched pilot: 18 trained endpoints",
                  f"Completed in {manifest['wall_seconds']:.2f} seconds. MOBIO/FEI; sign-corrected 64-bit BioHash; "
                  "pool 4, 16/64 shared projection, fresh keys; three joint key/model seeds; one identity partition. "
                  "The trusted verifier re-encodes each raw probe under the claimed enrollment key. Thresholds "
                  "use validation identities only; test identities remain held out. Keys are outside the attacker database.")
        table(figure, [.07, .62, .86, .08], ["Data", "Attack b/c %", "TAR b/c %", "FMR b/c %"],
              [[row["dataset"], f"{100*float(row['before_leakage']):.2f} / {100*float(row['after_leakage']):.2f}",
                f"{100*float(row['before_tar']):.2f} / {100*float(row['after_tar']):.2f}",
                f"{100*float(row['before_fmr']):.2f} / {100*float(row['after_fmr']):.2f}"] for row in effects],
              [.14, .29, .29, .28])
        table(figure, [.07, .45, .86, .10], ["Data", "Leakage drop LCB", "TAR change LCB", "FMR UCB", "Gate"],
              [[row["dataset"], f"{100*float(row['leakage_reduction_lower']):.2f} pp",
                f"{100*float(row['tar_difference_lower']):.2f} pp", f"{100*float(row['after_fmr_upper']):.2f}%",
                "PASS" if row["gate_pass"] == "True" else "FAIL"] for row in effects], [.13, .27, .26, .20, .14])
        paragraph(figure, .41, "The fixed acceptance criterion fails on utility uncertainty",
                  "The TAR lower bound must be at least -3 points. Neither dataset meets it, despite similar or "
                  "higher average TAR. Both meet positive leakage-reduction and <=2% FMR upper-bound conditions. "
                  "Six one-sided bounds use Bonferroni tail allocation .05/6 and 10,000 crossed seed/identity "
                  "bootstrap draws. Margins were fixed before execution and were not relaxed after failure.")
        paragraph(figure, .22, "Conclusion and costs",
                  "Reduced learned leakage is supported here; utility noninferiority is not demonstrated. The "
                  "architecture requires a trusted raw-probe path and external key custody. It does not defend "
                  "against key-service compromise or unrestricted compatible-output queries. Uncertainty is "
                  "conditional on the enrollment gallery; three joint seeds and one partition are limited. "
                  "No universal privacy, deployment readiness or journal novelty claim follows.")
        figure.text(.07, .07, "Full protocol, provenance, numerical tables and theory: experiments/source_security_utility_2026-09-25/", fontsize=8)
        output.savefig(figure)
        plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "reports/Source_Security_Utility_2026-09-25.pdf")
    args = parser.parse_args()
    build_report(args.out)
    print(f"Four-page source/security/utility report: {args.out}")


if __name__ == "__main__":
    main()