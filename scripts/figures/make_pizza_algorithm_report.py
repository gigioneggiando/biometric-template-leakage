"""Build a plain-language, ASCII-only explanation with original pizza diagrams."""
from __future__ import annotations

import json
import math
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Wedge

from scripts.figures.make_static_policy_report import load_rows, table

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "reports/Pizza_Algorithm_Explained_2026-09-25.pdf"
INK = "#20342d"
GREEN = "#267558"
RED = "#bc403b"


def page(title: str, number: int):
    figure = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    figure.text(.075, .95, title, fontsize=23, weight="bold", va="top", color=INK,
                family="DejaVu Serif")
    figure.text(.075, .905, "THE PIZZA EXPLANATION  |  UPDATED 26 SEPTEMBER 2026", fontsize=9, color=GREEN)
    figure.text(.075, .04, f"Research prototype. Not a security certificate.                             {number} / 9",
                fontsize=9, color=INK)
    return figure


def paragraph(figure, top: float, heading: str, body: str):
    if not (heading + body).isascii():
        raise ValueError("Use simple ASCII punctuation")
    figure.text(.075, top, heading, fontsize=14, weight="bold", va="top", color=INK)
    figure.text(.075, top - .032, textwrap.fill(body, width=75), fontsize=12,
                va="top", linespacing=1.45, color=INK)


def pizza(figure, left: float, bottom: float, label: str, pattern: int = 0, shared: bool = False):
    axis = figure.add_axes([left, bottom, .24, .205])
    axis.set_aspect("equal")
    axis.set_xlim(-1.2, 1.2)
    axis.set_ylim(-1.4, 1.2)
    axis.axis("off")
    axis.add_patch(Circle((0, 0), 1, facecolor="#d7a44e", edgecolor=INK, linewidth=1.2))
    axis.add_patch(Circle((0, 0), .87, facecolor="#f5da83", edgecolor="none"))
    if shared:
        axis.add_patch(Wedge((0, 0), .88, 0, 90, facecolor="#b5d8c6", edgecolor=GREEN))
    for angle in range(0, 360, 45):
        radians = math.radians(angle)
        axis.plot([0, .98 * math.cos(radians)], [0, .98 * math.sin(radians)],
                  color="#ae823c", linewidth=.7)
    for index in range(7):
        radians = math.radians(index * 137 + pattern * 31)
        radius = .28 if index < 2 else .64
        axis.add_patch(Circle((radius * math.cos(radians), radius * math.sin(radians)),
                              .095, facecolor=RED, edgecolor="white", linewidth=.5))
    axis.text(0, -1.25, label, fontsize=10, ha="center", color=INK)


def report_pages():
    effects = load_rows(ROOT / "experiments/utility_replication_2026-09-25/effects.csv")
    if len(effects) != 4:
        raise ValueError("Expected all four fixed replication cells")
    audit = json.loads((ROOT / "experiments/new_participant_joint_2026-09-25/cohort_audit.json").read_text())
    if audit["new_experiment_run"] or audit["status"] != "blocked_pending_new_authorized_participants":
        raise ValueError("Review the report wording before reporting new-cohort results")
    figures = []
    figure = page("A recipe inspector for face data", 1)
    paragraph(figure, .84, "Imagine a pizza shop", "A customer has a favorite pizza. Think of that recipe as their face features. The shop uses a secret preparation pattern to turn those features into a coded record. That pattern stands for a key.")
    pizza(figure, .075, .48, "Face features", 0)
    pizza(figure, .38, .48, "Secret key pattern", 2)
    pizza(figure, .685, .48, "Protected record", 4)
    paragraph(figure, .43, "What could go wrong?", "If the shop keeps reusing the same pattern, coded records can share structure. A stranger who collects records might learn to link them to people. The amount of leakage depends on the protection method and the attacker.")
    paragraph(figure, .25, "What does our algorithm do?", "It reads the preparation instructions: the source code. It follows where keys come from and checks for repeated patterns. This is static analysis. It does not need to run the recipe or read someone's face to inspect the code.")
    figures.append(figure)

    figure = page("How the inspector reads a recipe", 2)
    paragraph(figure, .84, "A small example", "Order 100 chooses pattern 0. Order 101 chooses pattern 1. Order 104 chooses pattern 0 again. The instruction 'order number modulo 4' means the remainder after division by four: only four possible choices.")
    paragraph(figure, .66, "1. Start at the record number", "The inspector assumes each record has a distinct integer number. Other inputs, such as the master seed, stay fixed in the context being inspected.")
    paragraph(figure, .51, "2. Follow the key through the code", "It tracks assignments, simple arithmetic, renamed functions and supported helper calls. A secret derivation function cannot turn four possible inputs into more than four possible outputs.")
    paragraph(figure, .35, "3. Check the protection step", "A constant means one pattern. A bounded pool means only a limited set. A record-specific derivation preserves distinctness only under the stated ideal assumptions. Shared projection pieces are checked separately.")
    paragraph(figure, .18, "4. Give an honest answer", "The answer is reuse, unknown, or conditionally fresh. Unsupported code gets an unknown result. Conditionally fresh does not mean secret, independent, unlinkable or approved for deployment.")
    figures.append(figure)

    figure = page("A fresh pizza can share a slice", 3)
    pizza(figure, .075, .63, "Record A", 1, True)
    pizza(figure, .38, .63, "Record B", 3, True)
    pizza(figure, .685, .63, "Record C", 5, True)
    paragraph(figure, .58, "Look at the green quarter", "The rest of each preparation pattern may change while one quarter stays shared. In our code this can be a shared block of projection columns. The inspector follows those blocks, not just the final key's name. The drawing represents shared structure, not identical face bits.")
    paragraph(figure, .37, "A simple counting idea", "Imagine four records, giving six pairs. If each pair shares exactly one quarter of its pattern, the weighted reuse count is 6 times 1/4, which is 1.5. If reuse is random, multiply each shared size by its probability and add across the pairs being studied.")
    paragraph(figure, .17, "What that number does not say", "This counts expected repeated structure. It does not say that 1.5 bits of identity leaked. A small shared part could still be informative. The uniform-pool formula needs uniform, independent choices; source code alone does not prove that.")
    figures.append(figure)

    figure = page("The right customer must still match", 4)
    paragraph(figure, .84, "The trusted chef has the right pattern", "When a customer returns, the verifier obtains a new face sample and uses the enrolled record's key to encode it for comparison. This assumes a trusted key service and raw-probe path. The attacker in this study has stored templates, not that service.")
    paragraph(figure, .63, "Check 1: less success for the attacker", "A candidate should lower the tested attacker's identification success. The uncertainty bound must support a reduction. Beating one tested attacker does not prove resistance to every possible attacker.")
    paragraph(figure, .45, "Check 2: keep genuine matches", "True acceptance is the fraction of genuine attempts accepted. We allow at most a three percentage point drop. For example, 96% to 93% is three points. We compare an uncertainty bound with this tolerance, not only the average.")
    paragraph(figure, .27, "Check 3: limit wrong matches", "False matches accept the wrong person. We require their upper uncertainty bound to be at most 2%. The matching threshold is chosen using validation data at a 1% false-match target, then left unchanged for the test data. All three checks are needed for the joint gate.")
    figures.append(figure)

    figure = page("What happened in the experiments?", 5)
    paragraph(figure, .84, "First pilot: neither joint gate passed", "The tested attack became less successful on both MOBIO and FEI. But the uncertainty in genuine matching was too large to pass our three-point tolerance. Similar average matching rates were not enough.")
    figure.text(.075, .715, "New replication: 2 of 4 utility checks passed", fontsize=14,
                weight="bold", va="top", color=INK)
    rows = [[row["dataset"], row["split_seed"],
             f"{100 * float(row['baseline_tar']):.2f}%",
             f"{100 * float(row['candidate_tar']):.2f}%",
             f"{100 * float(row['tar_lower']):.2f}",
             "Pass" if row["utility_pass"] == "True" else "Not passed"] for row in effects]
    table(figure, [.075, .50, .85, .18],
          ["Dataset", "Split", "Pool match", "Fresh match", "Lower\nchange*", "Utility"],
          rows, [.15, .13, .16, .16, .17, .23])
    figure.text(.075, .475, "*Lower uncertainty bound, in percentage points. Required: at least -3.00.", fontsize=9, color=INK)
    paragraph(figure, .43, "What the new test found", "We compared a four-key pool with record-specific keys. We fixed 12 new key seeds and two new splits per dataset before running 96 utility evaluations. MOBIO passed in both splits. FEI did not: its lower changes were below -3.00 points. All four false-match upper bounds were below 2%.")
    paragraph(figure, .23, "What we can conclude", "Matching looks promising in this setting, but retained utility is not established across both datasets. This follow-up did not train new attackers. We cannot combine an old attack result with new matching results and call it a new joint security pass. The splits reuse people; they are not independent populations.")
    figures.append(figure)

    figure = page("What still needs independent review?", 6)
    paragraph(figure, .84, "1. Ask other inspectors", "A separate archive contains 24 code cases and blank forms, without our predictions or answers. Two external reviewers should label their own copies and explain disagreements. They should also supply new cases. Preparing the packet is not the same as receiving independent labels.")
    paragraph(figure, .63, "2. Check the mathematics and prior work", "An internal review lists the assumptions and gaps. Abstract interpretation, cryptographic misuse analysis and probability bounds already exist. Our candidate contribution is their specific connection to biometric key reuse and matching tests. Global novelty and proof correctness are not independently certified.")
    paragraph(figure, .42, "3. Decide the next experiment before running it", "An external reviewer and application owner should review the model and tolerances. A further confirmation should fix data, keys, attacks, sample size and stopping rules in advance. The completed replication was prospective, but ran while external review was still pending.")
    paragraph(figure, .21, "The one-sentence takeaway", "Read the recipe, flag repeated preparation patterns, test both privacy and matching, and keep 'not yet proved' separate from 'safe'.")
    figure.text(.075, .095, "Technical details: docs/review/source_proof_novelty_2026-09-25.md\nData and protocol: experiments/utility_replication_2026-09-25/README.md",
                fontsize=8, linespacing=1.5, color=INK)
    figures.append(figure)

    figure = page("More pizzas are not more people", 7)
    paragraph(figure, .84, "A regular customer is still the same person", "Giving an existing customer a new order number does not make them a new customer. More photographs, new random seeds and new train/test splits do not create independent participants either.")
    rows = [[row["dataset"], str(row["participants"]), str(row["previously_seen_participants"]),
             str(row["eligible_not_seen_by_id"])] for row in audit["cohorts"]]
    table(figure, [.075, .57, .85, .12], ["Local data", "People", "Already used", "New eligible IDs"],
            rows, [.23, .20, .25, .32])
    paragraph(figure, .52, "Our local check found no new FEI or MOBIO IDs", "The embedding metadata exactly match files used in the earlier study. The raw FEI folder also contains only 200 participant IDs. Its extra photographs cannot solve the need for genuinely new people. Different labels in another dataset also need an overlap check.")
    paragraph(figure, .31, "What we need next", "An authorized new cohort with stable person IDs, permission for this research and at least 11 distinct usable photographs per person. Its people must be checked against all earlier cohorts, including training and validation. Another dataset is a new-cohort test, not automatically more FEI data.")
    paragraph(figure, .11, "Current status", "No new participants added. No new-cohort experiment run.")
    figures.append(figure)

    figure = page("Linking the new test to the algorithm", 8)
    paragraph(figure, .84, "1. Inspect the recipe before serving", "Your analyzer flags the four-pattern recipe as reuse. The record-specific recipe is conditionally fresh. We preserve these code traces and select this exact change before looking at the new test results. Scanning finds the risk; changing the key policy is the intervention.")
    paragraph(figure, .64, "2. Bring genuinely new customers", "The proposed target is 500 eligible new people: 200 for training, 100 for validation and 200 kept for the final test. This target needs feasibility and statistical power review. It is not a guarantee that the study will pass.")
    paragraph(figure, .46, "3. Test both sides of the same order", "On the same 200 test people, compare the original and changed recipe using 12 paired key/model draws. Measure attacker success and legitimate matching together. Train 24 attack models, select matching thresholds on validation people, and do not tune on the test people.")
    paragraph(figure, .26, "4. Require all three checks together", "The bounds must support less attacker success, no more than a three-point loss in genuine acceptance, and false matches at most 2%. Keep failures and uncertainty. Do not combine an old attack result with new matching to claim a pass.")
    figure.text(.075, .105, "PROTOCOL PREPARED ONLY. Waiting for authorized data and review.\nFull design: docs/protocols/new_participant_joint_2026-09-25.md",
                fontsize=9, linespacing=1.5, color=INK)
    figures.append(figure)

    regression = json.loads((ROOT / "experiments/source_branch_fix_2026-09-26/regression.json").read_text())
    confirmation = load_rows(ROOT / "experiments/scface_utility_confirmation_2026-09-25/effects.csv")
    if regression["changed_predictions"] != 0 or len(confirmation) != 4 or any(row["utility_pass"] != "False" for row in confirmation):
        raise ValueError("Review the update wording against changed evidence")
    figure = page("A safer inspector, not a safety proof", 9)
    paragraph(figure, .84, "Two order queues can reuse one pattern", "Imagine odd order numbers keep their number, while even numbers add one. Orders 0 and 1 now both use pattern 1. Our review found that separate recipe branches could hide this collision from v2 and v3. Eight records used only four actual keys.")
    paragraph(figure, .63, "The inspector now says unknown", "Protection calls inside branches now require further review instead of a freshness claim. Unsupported conditions also raise a warning. All 69 historical case evaluations keep the same predictions after the fix. This is internal regression evidence, not independent validation or a proof for all Python programs.")
    paragraph(figure, .42, "The later matching study still did not pass", "Luigi's 96 MOBIO/SCface utility evaluations passed the false-match ceiling, but 0 of 4 cells passed the three-point genuine-matching tolerance. The earlier MOBIO passes did not hold across these new splits. No attack was retrained in that study, and no joint security pass follows.")
    paragraph(figure, .21, "What is ready, and what must wait", "The branch repair and portable source-hash checks are ready. Original results and executed source bytes are preserved. Independent validation is deferred to you and your reviewers. New authorized people, a justified sample size and a joint attack/matching test remain necessary.")
    figure.text(.075, .085, "Repair record: experiments/source_branch_fix_2026-09-26/README.md", fontsize=8, color=INK)
    figures.append(figure)
    return figures


def build_report(destination: Path = OUTPUT):
    figures = report_pages()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(destination, metadata={"Title": "A recipe inspector for face data", "Author": "Biometric template leakage research"}) as pdf:
        for figure in figures:
            pdf.savefig(figure)
            plt.close(figure)
    return destination


if __name__ == "__main__":
    print(build_report())