"""Generate paper figures from tracked compact result files only.

Every point on every plot is read from `experiments/**/*.csv`; nothing is
transcribed by hand. Output goes to `reports/figures/` as PDF and PNG.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments"

# Muted, print-safe palette (Okabe-Ito).
C = {
    "blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "red": "#D55E00",
    "purple": "#CC79A7", "sky": "#56B4E9", "yellow": "#F0E442", "grey": "#7F7F7F", "black": "#000000",
}

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 9.5,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.4,
    "lines.markersize": 4.5,
    "pdf.fonttype": 42,
    "figure.dpi": 150,
})

# --- Data sources ---------------------------------------------------------

# (label, path, chance, colour, marker)
DATASETS = [
    ("MOBIO, partition B (n=30)", EXP / "mobio_multiexposure/key_pool_split_replication_summary.csv", 1 / 30, C["blue"], "o"),
    ("MOBIO, dense A (n=30)", EXP / "mobio_multiexposure/dense_key_pool_sweep_summary.csv", 1 / 30, C["sky"], "s"),
    ("MOBIO, dense 2 (n=30)", EXP / "mobio_multiexposure/dense_key_pool_sweep_partition2_summary.csv", 1 / 30, C["blue"], "^"),
    ("MOBIO, dense 3 (n=30)", EXP / "mobio_multiexposure/dense_key_pool_sweep_partition3_summary.csv", 1 / 30, C["blue"], "v"),
    ("LFW (n=25)", EXP / "lfw_multiexposure/key_pool_boundary_summary.csv", 1 / 25, C["orange"], "D"),
    ("FEI (n=40)", EXP / "fei_multiexposure/key_pool_boundary_summary.csv", 1 / 40, C["green"], "P"),
]
MLPHASH = [
    EXP / "mobio_multiexposure/mlphash_key_pool_summary.csv",
    EXP / "mobio_multiexposure/mlphash_key_pool_dense_summary.csv",
]


def load_pool_table(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    df = pd.read_csv(path)
    df["pool"] = df["condition"].str.extract(r"_(\d+)$").astype(float)
    df.loc[df["condition"] == "independent_unseen_keys", "pool"] = float("nan")
    return df


def pct(x):
    return 100 * x


# --- Figure 1: leakage vs pool size across datasets ----------------------

def fig_pool_curves(out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7), sharey=False)
    ax = axes[0]
    for label, path, chance, colour, marker in DATASETS:
        df = load_pool_table(path)
        if df is None:
            continue
        pools = df.dropna(subset=["pool"]).sort_values("pool")
        fresh = df[df["condition"] == "independent_unseen_keys"]
        # chance-normalized: top-1 / chance so different gallery sizes are comparable
        ax.plot(pools["pool"], pools["top1_mean"] / chance, marker=marker, color=colour, label=label, alpha=0.9)
        if not fresh.empty:
            ax.scatter([12.5], fresh["top1_mean"] / chance, marker=marker, color=colour, edgecolor="black", zorder=5, linewidth=0.6)
    ax.axhline(1.0, color=C["grey"], linestyle="--", linewidth=0.9)
    ax.text(12.5, 1.6, "fresh\nkeys", ha="center", fontsize=7.5, color=C["grey"])
    ax.set_xlabel("Recurring hidden transforms in pool, $k$")
    ax.set_ylabel("10-record top-1 / chance")
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12.5])
    ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "∞"])
    ax.set_title("(a) BioHash, three datasets, chance-normalized")
    ax.legend(frameon=False, ncol=1, loc="upper right", handlelength=1.5, fontsize=7, bbox_to_anchor=(1.0, 0.98))

    # (b) MLP-Hash on MOBIO
    ax = axes[1]
    frames = [load_pool_table(p) for p in MLPHASH]
    frames = [f for f in frames if f is not None]
    if frames:
        df = pd.concat(frames)
        pools = df.dropna(subset=["pool"]).sort_values("pool")
        fresh = df[df["condition"] == "independent_unseen_keys"]
        ax.plot(pools["pool"], pct(pools["top1_mean"]), marker="o", color=C["purple"], label="10 records (mean pool)")
        ax.plot(pools["pool"], pct(pools["one_record_top1_mean"]), marker="o", color=C["purple"], linestyle=":", alpha=0.7, label="1 record")
        ax.fill_between(pools["pool"], pct(pools["minimum_clustered_lower"]), pct(pools["maximum_clustered_upper"]), color=C["purple"], alpha=0.12, linewidth=0)
        ax.scatter([12.5] * len(fresh), pct(fresh["top1_mean"]), marker="o", color=C["purple"], edgecolor="black", zorder=5, linewidth=0.6)
    ax.axhline(100 / 30, color=C["grey"], linestyle="--", linewidth=0.9)
    ax.text(12.5, 8, "fresh\nkeys", ha="center", fontsize=7.5, color=C["grey"])
    ax.set_xlabel("Recurring hidden transforms in pool, $k$")
    ax.set_ylabel("Top-1 linkage (%)")
    ax.set_xticks([1, 2, 3, 4, 5, 10, 12.5])
    ax.set_xticklabels(["1", "2", "3", "4", "5", "10", "∞"])
    ax.set_title("(b) MLP-Hash on MOBIO (chance 3.33%)")
    ax.legend(frameon=False, loc="upper right", fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "fig_pool_curves.pdf")
    fig.savefig(out / "fig_pool_curves.png")
    plt.close(fig)


# --- Figure 2: multiplicity amplification (1 vs 10 records) --------------

def fig_amplification(out: Path) -> None:
    rows = []
    for label, path, chance, colour, marker in DATASETS:
        df = load_pool_table(path)
        if df is None or "one_record_top1_mean" not in df:
            continue
        short = label.split(" (")[0]
        for _, r in df.iterrows():
            key = "fresh" if pd.isna(r["pool"]) else f"k={int(r['pool'])}"
            rows.append({"dataset": short, "condition": key, "one": r["one_record_top1_mean"] / chance, "ten": r["top1_mean"] / chance, "colour": colour, "marker": marker})
    d = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(3.4, 3.2))
    lim = max(d["ten"].max(), d["one"].max()) * 1.08
    ax.plot([0, lim], [0, lim], color=C["grey"], linestyle="--", linewidth=0.9, zorder=1)
    for (ds, col, mk), g in d.groupby(["dataset", "colour", "marker"]):
        recurring = g[g["condition"] != "fresh"]
        fresh = g[g["condition"] == "fresh"]
        ax.scatter(recurring["one"], recurring["ten"], color=col, marker=mk, label=f"{ds}, recurring", alpha=0.85, zorder=3)
        ax.scatter(fresh["one"], fresh["ten"], color="white", edgecolor=col, marker=mk, linewidth=1.2, zorder=4, label=f"{ds}, fresh")
    ax.axvline(1, color=C["grey"], linewidth=0.6, alpha=0.6)
    ax.axhline(1, color=C["grey"], linewidth=0.6, alpha=0.6)
    ax.set_xlabel("1-record top-1 / chance")
    ax.set_ylabel("10-record top-1 / chance")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_title("Amplification appears only under reuse")
    # collapse legend to dataset names with filled/hollow explanation
    handles, labels = ax.get_legend_handles_labels()
    keep = [(h, l.replace(", recurring", "")) for h, l in zip(handles, labels) if "recurring" in l]
    leg = ax.legend([h for h, _ in keep], [l for _, l in keep], frameon=False, loc="lower right", fontsize=7, title="filled: recurring pool\nhollow: fresh keys", title_fontsize=7)
    leg._legend_box.align = "left"
    fig.tight_layout()
    fig.savefig(out / "fig_amplification.pdf")
    fig.savefig(out / "fig_amplification.png")
    plt.close(fig)


# --- Figure 3: pooled boundary across three MOBIO partitions -------------

def fig_pooled_boundary(out: Path) -> None:
    path = EXP / "mobio_multiexposure/dense_key_pool_pooled_analysis.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    pools = df[df["pool_size"] != "fresh"].copy()
    pools["k"] = pools["pool_size"].astype(int)
    fresh = df[df["pool_size"] == "fresh"].iloc[0]
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.fill_between(pools["k"], pct(pools["min_10_record_top1"]), pct(pools["max_10_record_top1"]), color=C["blue"], alpha=0.15, linewidth=0, label="range over 3 partitions")
    ax.plot(pools["k"], pct(pools["pooled_10_record_top1"]), marker="o", color=C["blue"], label="10 records, pooled mean")
    ax.plot(pools["k"], pct(pools["pooled_1_record_top1"]), marker="o", color=C["blue"], linestyle=":", alpha=0.7, label="1 record, pooled mean")
    ax.axhspan(pct(fresh["min_10_record_top1"]), pct(fresh["max_10_record_top1"]), color=C["grey"], alpha=0.15, linewidth=0)
    ax.axhline(pct(fresh["pooled_10_record_top1"]), color=C["grey"], linestyle="--", linewidth=0.9, label="fresh keys (3 partitions)")
    ax.axhline(100 / 30, color=C["black"], linewidth=0.6, alpha=0.5)
    ax.text(3.0, 100 / 30 - 2.6, "chance 3.33%", fontsize=7, color=C["black"], alpha=0.7, ha="left")
    for _, r in pools.iterrows():
        ax.text(r["k"], pct(r["max_10_record_top1"]) + 2.5, f"{int(r['partitions_intervals_exclude_chance'])}/{int(r['partitions'])}", ha="center", fontsize=7, color=C["blue"])
    ax.set_xlabel("Recurring hidden transforms in pool, $k$")
    ax.set_ylabel("Top-1 linkage (%)")
    ax.set_xticks(pools["k"])
    ax.set_ylim(-4, 75)
    ax.set_title("MOBIO boundary, three identity partitions")
    ax.legend(frameon=False, loc="upper right", fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "fig_pooled_boundary.pdf")
    fig.savefig(out / "fig_pooled_boundary.png")
    plt.close(fig)


# --- Figure 4: mechanism controls -----------------------------------------

def fig_controls(out: Path) -> None:
    mech = EXP / "mobio_mechanism_controls/results_summary.csv"
    corr = EXP / "mobio_correlation_controls/results_summary.csv"
    if not (mech.exists() and corr.exists()):
        return
    m = pd.read_csv(mech)
    c = pd.read_csv(corr)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6))

    ax = axes[0]
    m["k"] = m["condition"].str.extract(r"_(\d+)$").astype(float)
    hidden = m[(m["control"] == "hidden_slot") & m["k"].notna()].sort_values("k")
    known = m[(m["control"] == "known_slot") & m["k"].notna()].sort_values("k")
    shuf = m[(m["control"] == "shuffled_non_anchor") & m["k"].notna()].sort_values("k")
    ax.plot(hidden["k"], hidden["top1_mean_percent"], marker="o", color=C["blue"], label="slot hidden (DeepSets)")
    ax.plot(known["k"], known["top1_mean_percent"], marker="s", color=C["red"], linestyle="--", label="slot label given to attacker")
    ax.plot(shuf["k"], shuf["top1_mean_percent"], marker="x", color=C["grey"], label="records 2-10 from other identities")
    ax.axhline(100 / 30, color=C["black"], linewidth=0.6, alpha=0.5)
    ax.set_xlabel("Recurring hidden transforms in pool, $k$")
    ax.set_ylabel("10-record top-1 (%)")
    ax.set_xticks([3, 4, 5, 7])
    ax.set_ylim(0, 75)
    ax.set_title("(a) Slot label vs. shuffled records")
    ax.legend(frameon=False, loc="upper right", fontsize=7)

    ax = axes[1]
    fine = c[c["study"] == "fine"].sort_values("shared_fraction_percent")
    coarse = c[c["study"] == "coarse"].sort_values("shared_fraction_percent")
    ax.plot(coarse["shared_fraction_percent"], coarse["ten_record_top1_percent"], marker="o", color=C["green"], label="10 records, coarse sweep")
    ax.plot(fine["shared_fraction_percent"], fine["ten_record_top1_percent"], marker="^", color=C["green"], alpha=0.7, label="10 records, fine sweep (new split)")
    ax.plot(coarse["shared_fraction_percent"], coarse["one_record_top1_percent"], marker="o", color=C["green"], linestyle=":", alpha=0.6, label="1 record, coarse")
    ax.axhline(100 / 30, color=C["black"], linewidth=0.6, alpha=0.5)
    ax.set_xlabel("Projection columns shared system-wide (%)")
    ax.set_ylabel("Top-1 (%)")
    ax.set_ylim(0, 80)
    ax.set_title("(b) Partial projection sharing, Haar BioHash")
    ax.legend(frameon=False, loc="upper left", fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "fig_controls.pdf")
    fig.savefig(out / "fig_controls.png")
    plt.close(fig)


# --- Figure 5: exposure count under fresh keys (the null) ----------------

def fig_fresh_exposures(out: Path) -> None:
    files = {
        "BioHash": EXP / "mobio_multiexposure/results_summary.csv",
        "MLP-Hash": EXP / "mobio_multiexposure/mlphash_results_summary.csv",
    }
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    styles = {"BioHash": (C["blue"], "o"), "MLP-Hash": (C["purple"], "s")}
    for scheme, path in files.items():
        if not path.exists():
            continue
        df = pd.read_csv(path)
        col, mk = styles[scheme]
        fresh = df[df["condition"] == "independent_unseen_keys"]
        best = fresh.groupby("exposures")["top1_mean"].max().reset_index()
        ax.plot(best["exposures"], pct(best["top1_mean"]), marker=mk, color=col, label=f"{scheme}, fresh keys (best attacker)")
        shared = df[(df["condition"] == "shared_key_calibration")]
        if not shared.empty:
            b = shared.groupby("exposures")["top1_mean"].max().reset_index()
            ax.plot(b["exposures"], pct(b["top1_mean"]), marker=mk, color=col, linestyle="--", alpha=0.6, label=f"{scheme}, one shared key")
    ax.axhline(100 / 30, color=C["grey"], linestyle="--", linewidth=0.9)
    ax.text(10, 100 / 30 + 2.5, "chance 3.33%", fontsize=7, color=C["grey"], ha="right")
    ax.set_xlabel("Protected records per person, $n$")
    ax.set_ylabel("Top-1 linkage (%)")
    ax.set_xticks([1, 2, 5, 10])
    ax.set_ylim(0, 100)
    ax.set_title("More records do not help under fresh keys")
    ax.legend(frameon=False, fontsize=7, loc="center left")
    fig.tight_layout()
    fig.savefig(out / "fig_fresh_exposures.pdf")
    fig.savefig(out / "fig_fresh_exposures.png")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "reports/figures")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fig_pool_curves(args.out)
    fig_amplification(args.out)
    fig_pooled_boundary(args.out)
    fig_controls(args.out)
    fig_fresh_exposures(args.out)
    print(f"figures written to {args.out}")


if __name__ == "__main__":
    main()
