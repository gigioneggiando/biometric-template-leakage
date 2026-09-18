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
from matplotlib.text import Text
import pandas as pd
import numpy as np

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
    "axes.unicode_minus": False,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.4,
    "lines.markersize": 4.5,
    "pdf.fonttype": 42,
    "figure.dpi": 220,
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
    ("SCface (n=26)", EXP / "scface_multiexposure/key_pool_boundary_summary.csv", 1 / 26, C["red"], "X"),
]
MLPHASH = [
    EXP / "mobio_multiexposure/mlphash_key_pool_summary.csv",
    EXP / "mobio_multiexposure/mlphash_key_pool_dense_summary.csv",
]


def load_pool_table(path: Path) -> pd.DataFrame | None:
    df = pd.read_csv(path)
    df["pool"] = df["condition"].str.extract(r"_(\d+)$").astype(float)
    df.loc[df["condition"] == "independent_unseen_keys", "pool"] = float("nan")
    return df


def pct(x):
    return 100 * x


def save_figure(fig, out: Path, name: str) -> None:
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    outside_ticks = set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            lower, upper = sorted(axis.get_view_interval())
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                if not lower <= tick.get_loc() <= upper:
                    outside_ticks.update((tick.label1, tick.label2))
    texts = [text for text in fig.findobj(Text) if text.get_visible() and text.get_text() and text not in outside_ticks]
    bounds = [text.get_window_extent(renderer) for text in texts]
    for index, (text, bound) in enumerate(zip(texts, bounds)):
        if any(symbol in text.get_text() for symbol in ("\u2014", "\u2013", "\u2212")):
            raise ValueError(f"Unsupported dash in {name}: {text.get_text()}")
        if not fig.bbox.contains(bound.x0, bound.y0) or not fig.bbox.contains(bound.x1, bound.y1):
            raise ValueError(f"Text outside {name}: {text.get_text()}")
        for other, other_bound in zip(texts[index + 1:], bounds[index + 1:]):
            if bound.overlaps(other_bound):
                raise ValueError(f"Overlapping text in {name}: {text.get_text()} / {other.get_text()}")
    fig.savefig(out / f"{name}.pdf")
    fig.savefig(out / f"{name}.png")
    plt.close(fig)


def fig_results_overview(out: Path) -> None:
    table = pd.read_csv(EXP / "cross_dataset_key_pool_summary.csv")
    studies = table["source_file"].drop_duplicates().tolist()
    study_labels = {
        "mobio_multiexposure/key_pool_boundary_summary.csv": "MOBIO / BioHash / session-aligned",
        "mobio_multiexposure/random_key_pool_confirmation_summary.csv": "MOBIO / BioHash / random confirmation",
        "mobio_multiexposure/key_pool_split_replication_summary.csv": "MOBIO / BioHash / split B",
        "mobio_multiexposure/dense_key_pool_sweep_summary.csv": "MOBIO / BioHash / dense A",
        "mobio_multiexposure/dense_key_pool_sweep_partition2_summary.csv": "MOBIO / BioHash / dense 2",
        "mobio_multiexposure/dense_key_pool_sweep_partition3_summary.csv": "MOBIO / BioHash / dense 3",
        "mobio_multiexposure/haar_corrected_key_pool_summary.csv": "MOBIO / Haar BioHash",
        "mobio_multiexposure/mlphash_key_pool_summary.csv": "MOBIO / MLP-Hash / initial",
        "mobio_multiexposure/mlphash_key_pool_dense_summary.csv": "MOBIO / MLP-Hash / dense",
        "lfw_multiexposure/key_pool_boundary_summary.csv": "LFW / BioHash",
        "fei_multiexposure/key_pool_boundary_summary.csv": "FEI / BioHash",
        "scface_multiexposure/key_pool_boundary_summary.csv": "SCface / BioHash",
    }
    if set(studies) != set(study_labels):
        raise ValueError("Update overview labels for the source inventory")
    labels = [study_labels[study] for study in studies]
    pools = [str(pool) for pool in range(1, 11)] + ["fresh"]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.4), sharey=True)
    cmap = plt.get_cmap("cividis").with_extremes(bad="#EFEFEF")
    for ax, metric, title in zip(axes, ["one_record_top1_mean", "top1_mean"], ["(a) One record", "(b) Ten records"]):
        values = np.full((len(studies), len(pools)), np.nan)
        rates = values.copy()
        failures = np.zeros(values.shape, dtype=bool)
        for row_index, study in enumerate(studies):
            subset = table[table["source_file"] == study]
            for _, record in subset.iterrows():
                column = pools.index(str(record["pool_size"]))
                rates[row_index, column] = record[metric]
                chance = 1 / record["test_identities"]
                values[row_index, column] = (record[metric] - chance) / (1 - chance)
                failures[row_index, column] = not record["interval_excludes_chance"]
        image = ax.imshow(values, cmap=cmap, vmin=-0.05, vmax=1, aspect="auto")
        for row_index, column in np.ndindex(values.shape):
            if np.isfinite(values[row_index, column]):
                suffix = "*" if metric == "top1_mean" and failures[row_index, column] else ""
                ax.text(column, row_index, f"{100 * rates[row_index, column]:.1f}{suffix}",
                        ha="center", va="center", fontsize=6.5,
                        color="white" if values[row_index, column] < 0.48 else "black")
        ax.set_xticks(range(len(pools)), [*pools[:-1], "Fresh"], fontsize=7)
        ax.set_yticks(range(len(studies)), labels, fontsize=8)
        ax.set_title(title, loc="left")
        ax.set_xlabel("Hidden transforms in pool, k")
        ax.grid(False)
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.subplots_adjust(left=0.30, right=0.98, top=0.88, bottom=0.30, wspace=0.06)
    fig.suptitle("Earlier three-seed key-pool studies", y=0.97, fontsize=12)
    color_ax = fig.add_axes([0.50, 0.17, 0.32, 0.022])
    fig.colorbar(image, cax=color_ax, orientation="horizontal", ticks=[0, 0.5, 1])
    color_ax.set_xlabel("Chance-adjusted score: (top-1 - chance) / (1 - chance)", fontsize=8)
    fig.text(0.30, 0.035, "Cells: top-1 (%), 3-seed means. Grey: unavailable. *: not all seed intervals exclude chance.\n"
             "Gallery sizes: MOBIO 30; LFW 25; FEI 40; SCface 26. Rows are separate studies, not matched replications.", fontsize=8)
    save_figure(fig, out, "fig_results_overview")


# --- Figure 1: leakage vs pool size across datasets ----------------------

def fig_pool_curves(out: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.8), sharey=False)
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
    ax.set_xlabel("Recurring hidden transforms in pool, $k$")
    ax.set_ylabel("10-record top-1 / chance")
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12.5])
    ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Fresh"])
    ax.set_title("(a) BioHash across datasets")
    ax.legend(frameon=False, ncol=1, loc="upper left", handlelength=1.5, fontsize=7, bbox_to_anchor=(0, -0.30))

    # (b) MLP-Hash on MOBIO
    ax = axes[1]
    for path, label, colour, marker in zip(MLPHASH, ["Initial study", "Dense study"], [C["purple"], C["blue"]], ["o", "s"]):
        df = load_pool_table(path)
        pools = df.dropna(subset=["pool"]).sort_values("pool")
        fresh = df[df["condition"] == "independent_unseen_keys"]
        ax.errorbar(pools["pool"], pct(pools["top1_mean"]), yerr=pct(pools["top1_std"]),
                    marker=marker, color=colour, label=f"{label}, 10 records", capsize=2)
        ax.plot(pools["pool"], pct(pools["one_record_top1_mean"]), marker=marker, color=colour, linestyle=":", alpha=0.7, label=f"{label}, 1 record")
        ax.scatter([12.5] * len(fresh), pct(fresh["top1_mean"]), marker=marker, color=colour, edgecolor="black", zorder=5, linewidth=0.6)
    ax.axhline(100 / 30, color=C["grey"], linestyle="--", linewidth=0.9)
    ax.set_xlabel("Recurring hidden transforms in pool, $k$")
    ax.set_ylabel("Top-1 linkage (%)")
    ax.set_xticks([1, 2, 3, 4, 5, 10, 12.5])
    ax.set_xticklabels(["1", "2", "3", "4", "5", "10", "Fresh"])
    ax.set_title("(b) MLP-Hash, MOBIO (N = 30)")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0, -0.30), fontsize=7, title="Bars: seed SD, not confidence intervals", title_fontsize=7)
    fig.tight_layout()
    save_figure(fig, out, "fig_pool_curves")


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
    ax.set_title("BioHash record-count gains")
    # collapse legend to dataset names with filled/hollow explanation
    handles, labels = ax.get_legend_handles_labels()
    keep = [(h, l.replace(", recurring", "")) for h, l in zip(handles, labels) if "recurring" in l]
    leg = ax.legend([h for h, _ in keep], [l for _, l in keep], frameon=False, loc="lower right", fontsize=7, title="filled: recurring pool\nhollow: fresh keys", title_fontsize=7)
    leg._legend_box.align = "left"
    fig.tight_layout()
    save_figure(fig, out, "fig_amplification")


# --- Figure 3: pooled boundary across three MOBIO partitions -------------

def fig_pooled_boundary(out: Path) -> None:
    path = EXP / "mobio_multiexposure/dense_key_pool_pooled_analysis.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    pools = df[df["pool_size"] != "fresh"].copy()
    pools["k"] = pools["pool_size"].astype(int)
    fresh = df[df["pool_size"] == "fresh"].iloc[0]
    fig, ax = plt.subplots(figsize=(3.4, 3.5))
    ax.fill_between(pools["k"], pct(pools["min_10_record_top1"]), pct(pools["max_10_record_top1"]), color=C["blue"], alpha=0.15, linewidth=0, label="range over available partitions")
    ax.plot(pools["k"], pct(pools["pooled_10_record_top1"]), marker="o", color=C["blue"], label="10 records, pooled mean")
    ax.plot(pools["k"], pct(pools["pooled_1_record_top1"]), marker="o", color=C["blue"], linestyle=":", alpha=0.7, label="1 record, pooled mean")
    ax.axhspan(pct(fresh["min_10_record_top1"]), pct(fresh["max_10_record_top1"]), color=C["grey"], alpha=0.15, linewidth=0)
    ax.axhline(pct(fresh["pooled_10_record_top1"]), color=C["grey"], linestyle="--", linewidth=0.9, label="fresh keys (3 partitions)")
    ax.axhline(100 / 30, color=C["black"], linewidth=0.6, alpha=0.5, label="chance 3.33%")
    for _, r in pools.iterrows():
        ax.text(r["k"], pct(r["max_10_record_top1"]) + 2.5, f"{int(r['partitions_intervals_exclude_chance'])}/{int(r['partitions'])}", ha="center", fontsize=7, color=C["blue"])
    ax.set_xlabel("Recurring hidden transforms in pool, $k$")
    ax.set_ylabel("Top-1 linkage (%)")
    ax.set_xticks(pools["k"])
    ax.set_ylim(-4, 75)
    ax.set_title("MOBIO boundary (N = 30)")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0, -0.35), fontsize=7)
    fig.tight_layout()
    save_figure(fig, out, "fig_pooled_boundary")


# --- Figure 4: mechanism controls -----------------------------------------

def fig_controls(out: Path) -> None:
    mech = EXP / "mobio_mechanism_controls/results_summary.csv"
    corr = EXP / "mobio_correlation_controls/results_summary.csv"
    if not (mech.exists() and corr.exists()):
        return
    m = pd.read_csv(mech)
    c = pd.read_csv(corr)
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.8))
    fig.suptitle("MOBIO mechanism controls (30 gallery identities; chance 3.33%)", fontsize=11)

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
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0, -0.30), fontsize=7)

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
    ax.set_title("(b) Shared projection columns")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0, -0.30), fontsize=7)

    ax = axes[2]
    same = c[c["study"] == "same_image"]
    ax.bar([0, 1], same["ten_record_top1_percent"], color=[C["grey"], C["blue"]], width=0.5)
    ax.axhline(100 / 30, color=C["black"], linestyle="--", linewidth=0.9)
    ax.set_xticks([0, 1], ["Different images", "Same image"])
    ax.set_ylim(0, 10)
    ax.set_ylabel("10-record top-1 (%)")
    ax.set_title("(c) Fresh keys, image control")
    for index, value in enumerate(same["ten_record_top1_percent"]):
        ax.text(index, value + 0.4, f"{value:.2f}%", ha="center", fontsize=8)
    fig.tight_layout()
    save_figure(fig, out, "fig_controls")


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
    ax.set_title("Fresh and shared keys: MOBIO (N = 30)")
    ax.legend(frameon=False, fontsize=6.5, loc="center left")
    fig.tight_layout()
    save_figure(fig, out, "fig_fresh_exposures")


def load_pilot_table(name: str) -> pd.DataFrame:
    paths = [EXP / "scheme_extension_pilot" / name, EXP / "scface_scheme_extension_pilot" / name]
    table = pd.concat([pd.read_csv(path) for path in paths if path.exists()], ignore_index=True)
    if table.empty or set(table["stage"]) != {"pilot"}:
        raise ValueError("Pilot figures require explicitly labelled pilot rows")
    if "seed" in table:
        cells = [column for column in ("dataset", "scheme", "condition", "exposures", "model") if column in table]
        if table.groupby(cells)["seed"].nunique().max() != 1:
            raise ValueError("Each pilot endpoint must contain exactly one model seed")
    return table


def fig_scheme_pilots(out: Path) -> None:
    data = load_pilot_table("results_summary.csv")
    order = ["random_key_pool_1", "random_key_pool_4", "random_key_pool_8", "independent_unseen_keys"]
    fig, axes = plt.subplots(2, 3, figsize=(10.2, 5.6), sharex=True, sharey=True)
    styles = [(1, "single_mlp", "1 record", C["grey"], "s", ":"),
              (10, "mean_mlp", "10 records, mean", C["blue"], "o", "-"),
              (10, "deepsets", "10 records, DeepSets", C["green"], "^", "--")]
    for row_index, scheme in enumerate(["IoM-GRP", "PolyProtect"]):
        for column, dataset in enumerate(["MOBIO", "FEI", "SCface"]):
            ax = axes[row_index, column]
            subset = data[(data["dataset"] == dataset) & (data["scheme"] == scheme)]
            for exposures, model, label, colour, marker, style in styles:
                selected = subset[(subset["exposures"] == exposures) & (subset["model"] == model)].set_index("condition").loc[order]
                values = 100 * selected["top1"].to_numpy()
                errors = np.stack([values - 100 * selected["lower95"].to_numpy(), 100 * selected["upper95"].to_numpy() - values]).clip(min=0)
                ax.errorbar([1, 4, 8], values[:3], yerr=errors[:, :3], marker=marker, linestyle=style,
                            color=colour, capsize=2, label=label)
                ax.errorbar([11], values[3:], yerr=errors[:, 3:], marker=marker, linestyle="none", color=colour, capsize=2)
            identities = int(subset["test_identities"].iloc[0])
            ax.axhline(100 / identities, color=C["black"], linestyle="--", linewidth=0.7)
            ax.set_title(f"{dataset} / {scheme} (N={identities})")
            ax.set_xticks([1, 4, 8, 11], ["1", "4", "8", "Fresh"])
            ax.set_ylim(-2, 105)
            if column == 0:
                ax.set_ylabel("Top-1 linkage (%)")
            if row_index == 1:
                ax.set_xlabel("Hidden transforms in pool, k")
    fig.suptitle("New protection schemes: one-seed pilots", y=0.98, fontsize=11)
    fig.text(0.5, 0.925, "120-epoch cap; bars: identity-clustered 95% intervals; dashed baseline: chance", ha="center", fontsize=8)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.01))
    fig.tight_layout(rect=(0, 0.09, 1, 0.90))
    save_figure(fig, out, "fig_scheme_pilots")


def fig_pilot_uncertainty(out: Path) -> None:
    data = load_pilot_table("paired_uncertainty.csv")
    data = data[(data["contrast"] == "ten_minus_one") & (data["model"] == "mean_mlp")].sort_values(["dataset", "scheme", "condition"])
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    labels = []
    for position, (_, record) in enumerate(data.iterrows()):
        condition = "Fresh" if record["condition"] == "independent_unseen_keys" else "k=" + record["condition"].rsplit("_", 1)[1]
        labels.append(f"{record['dataset']} / {record['scheme']} / {condition}")
        estimate = 100 * record["estimate"]
        ax.errorbar(estimate, position, xerr=[[estimate - 100 * record["lower"]], [100 * record["upper"] - estimate]],
                    fmt="o", color=C["blue"] if record["scheme"] == "IoM-GRP" else C["orange"], capsize=2)
    ax.axvline(0, color=C["black"], linestyle="--", linewidth=0.8)
    ax.set_yticks(range(len(labels)), labels, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlabel("10-record minus 1-record top-1 (percentage points)")
    ax.set_title("Paired mean-pool gains: one-seed pilots, 95% intervals")
    fig.tight_layout()
    save_figure(fig, out, "fig_pilot_uncertainty")


def fig_pilot_native_utility(out: Path) -> None:
    data = load_pilot_table("native_utility.csv")
    order = ["random_key_pool_1", "random_key_pool_4", "random_key_pool_8", "independent_unseen_keys"]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5), sharey=True)
    for ax, scheme in zip(axes, ["IoM-GRP", "PolyProtect"]):
        for dataset, colour, marker in [("MOBIO", C["blue"], "o"), ("FEI", C["orange"], "s"),
                                        ("SCface", C["green"], "^")]:
            selected = data[(data["dataset"] == dataset) & (data["scheme"] == scheme)].set_index("condition").loc[order]
            identities = int(selected["test_identities"].iloc[0])
            ax.plot([1, 4, 8], 100 * selected["native_top1"].iloc[:3], marker=marker, color=colour, label=f"{dataset}, N={identities}")
            ax.scatter([11], 100 * selected["native_top1"].iloc[3:], marker=marker, color=colour)
            ax.axhline(100 / identities, color=colour, linestyle=":", linewidth=0.8)
        ax.set_xticks([1, 4, 8, 11], ["1", "4", "8", "Fresh"])
        ax.set_title(scheme)
        ax.set_xlabel("Hidden transforms in pool, k")
        ax.set_ylim(0, 105)
    axes[0].set_ylabel("Protected-gallery top-1 (%)")
    fig.suptitle("Native matching diagnostic, not learned embedding linkage", y=0.98, fontsize=10.5)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.tight_layout(rect=(0, 0.12, 1, 0.90))
    save_figure(fig, out, "fig_pilot_native_utility")


def fig_pilot_equivalence(out: Path) -> None:
    data = load_pilot_table("equivalence_sensitivity.csv")
    data = data[data["margin"] == 0.02].sort_values(["dataset", "scheme", "exposures", "model"])
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    ax.axvspan(-2, 2, color=C["grey"], alpha=0.15, label="Illustrative +/-2 pp band; not an approved equivalence margin")
    labels = []
    for position, (_, record) in enumerate(data.iterrows()):
        model = {"single_mlp": "1 / single", "mean_mlp": "10 / mean", "deepsets": "10 / DeepSets"}[record["model"]]
        labels.append(f"{record['dataset']} / {record['scheme']} / {model}")
        estimate = 100 * record["estimate"]
        ax.errorbar(estimate, position, xerr=[[estimate - 100 * record["lower"]], [100 * record["upper"] - estimate]],
                    fmt="o", color=C["blue"] if record["scheme"] == "IoM-GRP" else C["orange"], capsize=2)
    ax.axvline(0, color=C["black"], linewidth=0.8)
    ax.set_yticks(range(len(labels)), labels, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("Fresh-key top-1 minus chance (percentage points)")
    ax.set_title("Fresh-key 90% intervals: exploratory pilot sensitivity")
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", frameon=False, fontsize=7)
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    save_figure(fig, out, "fig_pilot_equivalence")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "reports/figures")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fig_results_overview(args.out)
    fig_pool_curves(args.out)
    fig_amplification(args.out)
    fig_pooled_boundary(args.out)
    fig_controls(args.out)
    fig_fresh_exposures(args.out)
    fig_scheme_pilots(args.out)
    fig_pilot_uncertainty(args.out)
    fig_pilot_native_utility(args.out)
    fig_pilot_equivalence(args.out)
    print(f"figures written to {args.out}")


if __name__ == "__main__":
    main()
