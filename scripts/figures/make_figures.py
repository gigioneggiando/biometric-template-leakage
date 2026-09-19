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


def fig_followup_amplification(out: Path) -> None:
    table = pd.read_csv(EXP / "scheme_followup_2026-09-18/seed_identity_contrasts.csv")
    table = table[table["primary"]].sort_values(["dataset", "scheme", "split_seed"]).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10.5, 5.0))
    for position, row in table.iterrows():
        color = C["blue"] if row["scheme"] == "IoM-GRP" else C["red"]
        ax.errorbar(100 * row["gain"], position,
                    xerr=[[100 * (row["gain"] - row["lower95"])], [100 * (row["upper95"] - row["gain"])]],
                    fmt="o", color=color, capsize=3)
        ax.text(57, position, f"{100 * row['gain']:.2f} pp; p={row['holm_p']:.3f}", fontsize=8, va="center")
    labels = [f"{row.dataset} / {row.scheme} / split {row.split_seed}" for row in table.itertuples()]
    ax.set_yticks(range(len(table)), labels)
    ax.invert_yaxis()
    ax.axvline(0, color=C["grey"], ls="--", lw=1)
    ax.set_xlim(-2, 80)
    ax.set_xlabel("Ten-record minus one-record top-1 (percentage points)")
    ax.set_title("Pool-4 mean-pool amplification: three seeds, two identity partitions", pad=12)
    fig.subplots_adjust(left=0.32, right=0.98, top=0.87, bottom=0.23)
    fig.text(0.03, 0.09, "Bars: crossed model-seed / identity bootstrap 95% intervals. Tests: identity sign-flips, Holm family of 8.", fontsize=8)
    fig.text(0.03, 0.045, "Matched 120-epoch caps; key/set seeds fixed. Partitions are separate sensitivity analyses, not independent replications.", fontsize=8)
    save_figure(fig, out, "fig_followup_amplification")


def fig_followup_native_controls(out: Path) -> None:
    table = pd.read_csv(EXP / "scheme_followup_2026-09-18/native_null_controls.csv")
    norm = pd.read_csv(EXP / "scheme_followup_2026-09-18/norm_sensitivity.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), gridspec_kw={"width_ratios": [1.4, 1]})
    for dataset, color, marker in (("MOBIO", C["blue"], "o"), ("FEI", C["green"], "s")):
        subset = table[table["dataset"] == dataset].reset_index(drop=True)
        offset = -0.12 if dataset == "MOBIO" else 0.12
        positions = np.arange(len(subset)) + offset
        axes[0].errorbar(positions, 100 * subset["identity_balanced_top1"],
                         yerr=100 * np.vstack([subset["identity_balanced_top1"] - subset["lower95"],
                                               subset["upper95"] - subset["identity_balanced_top1"]]),
                         fmt=marker, color=color, capsize=3, label=dataset)
        axes[0].axhline(100 * subset["chance"].iloc[0], color=color, ls="--", lw=0.8)
    axes[0].set_xticks(range(6), ["A/1", "A/2", "A/3", "B/1", "B/2", "B/3"])
    axes[0].set_ylim(0, 22)
    axes[0].set_xlabel("Identity partition / fresh-key seed index")
    axes[0].set_ylabel("Identity-balanced native top-1 (%)")
    axes[0].set_title("(a) Fresh PolyProtect: protected-gallery matching")
    axes[0].legend(frameon=False, loc="upper right")
    for scheme, color, marker in (("IoM-GRP", C["blue"], "o"), ("PolyProtect", C["red"], "s")):
        for position, scale in enumerate([0.5, 2.0]):
            values = norm[(norm["scheme"] == scheme) & (norm["scale"] == scale)]["relative_l2_mean"]
            offset = -0.07 if scheme == "IoM-GRP" else 0.07
            axes[1].scatter(np.full(len(values), position + offset), values, color=color, marker=marker,
                            label=scheme if position == 0 else None)
    axes[1].set_xticks([0, 1], ["0.5 x input", "2 x input"])
    axes[1].set_ylabel("Mean relative template L2 change")
    axes[1].set_title("(b) Controlled radial stress")
    axes[1].legend(frameon=False, loc="upper left")
    axes[1].set_ylim(-0.08, 1.6)
    fig.subplots_adjust(left=0.075, right=0.97, top=0.88, bottom=0.27, wspace=0.38)
    fig.text(0.03, 0.13, f"Native tests: {len(table)} / {len(table)} Holm-adjusted p <= {table['holm_p'].max():.3f}; identity-clustered 95% intervals; dashed lines: chance.", fontsize=8)
    fig.text(0.03, 0.075, "A/B: splits 91831/91843. Key seeds 1/2/3: 91873/91879/91883. Gallery-label permutations preserve probe clusters.", fontsize=8)
    fig.text(0.03, 0.025, "Radial stress: 32 held-out records per dataset/partition, fixed keys; measures scale sensitivity, not natural norm leakage.", fontsize=8)
    save_figure(fig, out, "fig_followup_native_controls")


def fig_native_norm_audit(out: Path) -> None:
    table = pd.read_csv(EXP / "norm_native_audit_2026-09-18/native_norm_controls.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
    arms = ["unit", "raw", "norm_shuffled", "fixed_radius"]
    for axis, dataset in zip(axes, ["MOBIO", "FEI"]):
        for split, offset, color, marker, label in [(91831, -0.08, C["blue"], "o", "Partition A"),
                                                   (91843, 0.08, C["green"], "s", "Partition B")]:
            subset = table[(table["dataset"] == dataset) & (table["split_seed"] == split)].set_index("arm").loc[arms]
            axis.errorbar(np.arange(4) + offset, 100 * subset["top1"],
                          yerr=100 * np.vstack([subset["top1"] - subset["lower95"], subset["upper95"] - subset["top1"]]),
                          fmt=marker, color=color, capsize=3, label=label)
        axis.axhline(100 * subset["chance"].iloc[0], color="#777777", ls="--", lw=1)
        axis.set_xticks(range(4), ["Unit", "Raw", "Shuffled\nnorms", "Fixed\nradius"])
        axis.set_title(dataset)
        axis.set_ylim(0, 25)
        axis.legend(frameon=False, loc="upper left", ncol=2, fontsize=8)
    axes[0].set_ylabel("Native protected-gallery top-1 (%)")
    fig.subplots_adjust(left=0.08, right=0.97, top=0.9, bottom=0.29, wspace=0.12)
    fig.text(0.03, 0.12, "Three fixed key seeds averaged; identity-bootstrap 95% intervals. All 16 null tests: Holm p = 0.0032.", fontsize=8)
    fig.text(0.03, 0.07, "Raw minus unit survives paired correction only on FEI. Raw minus shuffled: all adjusted p >= 0.7584.", fontsize=8)
    fig.text(0.03, 0.025, "Natural identity-specific norm leakage is not established. No learned raw-input attack was retrained.", fontsize=8)
    save_figure(fig, out, "fig_native_norm_audit")


def fig_followup_failures(out: Path) -> None:
    table = pd.read_csv(EXP / "norm_native_audit_2026-09-18/failure_analysis.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.1), gridspec_kw={"width_ratios": [1.2, 1]})
    selected = table[(table["condition"] == "random_key_pool_4") & (table["model"] == "deepsets")].copy()
    failures = table[(table["condition"] == "random_key_pool_1") & (table["model"] == "deepsets") & (table["scheme"] == "PolyProtect")].copy()
    for axis, subset, title, color in [(axes[0], selected, "Pool-4 DeepSets: uncertain gains", C["blue"]),
                                       (axes[1], failures, "Shared-key PolyProtect: regressions", C["red"])]:
        subset = subset.reset_index(drop=True)
        positions = np.arange(len(subset))
        axis.errorbar(100 * subset["gain"], positions,
                      xerr=100 * np.vstack([subset["gain"] - subset["lower95"], subset["upper95"] - subset["gain"]]),
                      fmt="o", color=color, capsize=3)
        labels = [f"{row.dataset} {row.scheme if axis is axes[0] else ''} {'A' if row.split_seed == 91831 else 'B'}".strip()
                  for row in subset.itertuples()]
        axis.set_yticks(positions, labels, fontsize=8)
        axis.invert_yaxis()
        axis.axvline(0, color="#777777", lw=1, ls="--")
        axis.set_title(title, fontsize=10)
        axis.set_xlabel("Ten minus one top-1 (percentage points)", fontsize=9)
    fig.subplots_adjust(left=0.19, right=0.98, top=0.9, bottom=0.25, wspace=0.48)
    fig.text(0.03, 0.12, "All 48 contrasts reported; post-hoc two-sided Holm family 48. Pointwise crossed seed/identity 95% intervals.", fontsize=8)
    fig.text(0.03, 0.07, "Left: none survives correction (minimum p = 0.0576). Right: all four negative contrasts survive (p = 0.0192).", fontsize=8)
    fig.text(0.03, 0.025, "All eight pool-4 mean-pool gains remain significant (p = 0.0192). More records do not universally improve linkage.", fontsize=8)
    save_figure(fig, out, "fig_followup_failures")


def fig_dataset_coverage(out: Path) -> None:
    from matplotlib.colors import ListedColormap

    labels = ["BioHash historical", "MLP-Hash historical", "IoM / PolyProtect pilots",
              "Original scheme follow-up", "Native / raw-norm audit", "Independent-pool + baseline",
              "Extended exposure study", "Learned raw-input study", "Stricter-selection audit"]
    cells = [[2, 2, 2, 2], [2, 0, 0, 0], [1, 0, 1, 1], [3, 0, 3, 0], [3, 0, 3, 0], [4, 0, 4, 0],
             [3, 0, 0, 3], [2, 0, 0, 2], [2, 0, 0, 2]]
    text = [["3 model seeds"] * 4, ["3 model seeds", "Not run", "Not run", "Not run"],
            ["1 model seed", "Not run", "1 model seed", "1 model seed"],
            ["3 seeds / 2 splits", "Not run", "3 seeds / 2 splits", "Not run"],
            ["3 keys / 2 splits", "Not run", "3 keys / 2 splits", "Not run"],
                ["3 pools / 3 seeds\n2 splits", "Not run", "3 pools / 3 seeds\n2 splits", "Not run"],
                ["3 seeds / 2 splits", "Not run", "Not run", "3 seeds / 2 splits"],
                ["3 seeds / 1 split", "Not run", "Not run", "3 seeds / 1 split"],
                ["3 keys / 1 split", "Not run", "Not run", "3 keys / 1 split"]]
    fig, axis = plt.subplots(figsize=(10.5, 6.1))
    axis.imshow(cells, cmap=ListedColormap(["#eeeeee", "#f9e6b2", "#d5e9f5", "#bde5d8", "#83c6b4"]), vmin=0, vmax=4, aspect="auto")
    axis.set_xticks(range(4), ["MOBIO", "LFW", "FEI", "SCface"])
    axis.set_yticks(range(len(labels)), labels)
    axis.grid(False)
    axis.tick_params(length=0)
    for row, values in enumerate(text):
        for column, value in enumerate(values):
            axis.text(column, row, value, ha="center", va="center", fontsize=9)
    axis.set_title("Dataset coverage: evidence layers are not interchangeable", pad=16)
    fig.subplots_adjust(left=0.29, right=0.98, top=0.85, bottom=0.25)
    fig.text(0.03, 0.11, "SCface now has an extended study; coverage alone does not establish identical gallery protocols.", fontsize=9)
    fig.text(0.03, 0.055, "Grey = not run in this package, not zero accuracy. Identity partitions overlap; native audits do not train attackers.", fontsize=9)
    save_figure(fig, out, "fig_dataset_coverage")


def fig_pool_replication(out: Path) -> None:
    root = EXP / "pool_replication_2026-09-19"
    summaries = pd.read_csv(root / "crossed_contrasts.csv")
    pools = pd.read_csv(root / "pool_contrasts.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.3), sharey=True)
    contrasts = [("mean10_minus_single1", "(a) Ten-record gain over one record"),
                 ("mean10_minus_prediction10", "(b) Input mean minus prediction mean")]
    for axis, (contrast, title) in zip(axes, contrasts):
        subset = summaries[summaries["contrast"] == contrast].reset_index(drop=True)
        for position, row in subset.iterrows():
            axis.errorbar(100 * row["gain"], position, xerr=[[100 * (row["gain"] - row["lower95"])],
                          [100 * (row["upper95"] - row["gain"])]], fmt="D", color=C["black"], capsize=3)
            selected = pools[(pools["contrast"] == contrast) & (pools["dataset"] == row["dataset"]) &
                             (pools["scheme"] == row["scheme"]) & (pools["split_seed"] == row["split_seed"])].sort_values("key_seed")
            for offset, (_, pool), color in zip([-0.18, 0, 0.18], selected.iterrows(), [C["blue"], C["orange"], C["green"]]):
                axis.scatter(100 * pool["gain"], position + offset, color=color, s=18, zorder=4,
                             label=str(int(pool["key_seed"])) if position == 0 else None)
        axis.axvline(0, ls="--", color=C["grey"], lw=1)
        axis.set_xlim(-27, 83)
        axis.set_title(title, pad=12)
        axis.set_xlabel("Paired top-1 difference (percentage points)")
    labels = [f"{row.dataset} / {row.scheme} / {'A' if row.split_seed == 91831 else 'B'}"
              for row in subset.itertuples()]
    axes[0].set_yticks(range(len(labels)), labels)
    axes[0].invert_yaxis()
    axes[1].legend(title="Pool seed", loc="lower right", frameon=False, fontsize=7)
    fig.subplots_adjust(left=0.24, right=0.98, top=0.88, bottom=0.26, wspace=0.16)
    fig.text(0.03, 0.13, "Colored dots: individual pool draws, averaged over three model seeds. Black: mean and crossed pool/seed/identity 95% interval.", fontsize=8)
    fig.text(0.03, 0.08, "IoM gains persist across draws; PolyProtect is pool-sensitive. Every direct baseline-comparison interval includes zero.", fontsize=8)
    fig.text(0.03, 0.03, "Three pools only; pointwise uncertainty, no corrected significance claim. A/B: overlapping partitions 91831/91843.", fontsize=8)
    save_figure(fig, out, "fig_pool_replication")


def fig_extended_exposures(out: Path) -> None:
    table = pd.read_csv(EXP / "scheme_followup_2026-09-19_full/seed_identity_endpoints.csv")
    fig, axes = plt.subplots(2, 4, figsize=(12.8, 6.8), sharex=True, sharey=True)
    conditions = [("independent_unseen_keys", "Fresh", C["grey"]),
                  ("random_key_pool_1", "Pool 1", C["green"]),
                  ("random_key_pool_4", "Pool 4", C["blue"]),
                  ("random_key_pool_8", "Pool 8", C["orange"])]
    for row_index, dataset in enumerate(["MOBIO", "SCface"]):
        for column, (scheme, split) in enumerate([(scheme, split) for scheme in ["IoM-GRP", "PolyProtect"]
                                                  for split in [91831, 91843]]):
            axis = axes[row_index, column]
            subset = table[(table["dataset"] == dataset) & (table["scheme"] == scheme) &
                           (table["split_seed"] == split) & table["model"].isin(["single_mlp", "mean_mlp"])]
            for offset, (condition, label, color) in enumerate(conditions):
                values = subset[subset["condition"] == condition].sort_values("exposures")
                axis.errorbar(np.arange(4) + (offset - 1.5) * 0.045, 100 * values["top1_mean"],
                              yerr=100 * np.vstack([values["top1_mean"] - values["lower95"],
                                                    values["upper95"] - values["top1_mean"]]),
                              color=color, marker="o", markersize=3, capsize=1.5, lw=1, label=label)
            axis.axhline(100 * subset["chance"].iloc[0], color=C["black"], ls=":", lw=0.7)
            axis.set_title(f"{dataset} / {scheme} / {'A' if split == 91831 else 'B'}", fontsize=9)
            axis.set_xticks(range(4), [1, 2, 5, 10])
            axis.set_ylim(-3, 104)
            if row_index == 1:
                axis.set_xlabel("Records per person")
            if column == 0:
                axis.set_ylabel("Top-1 (%)")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.97))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.86, bottom=0.19, hspace=0.3, wspace=0.12)
    fig.text(0.03, 0.065, "Single MLP at 1 record; mean MLP at 2/5/10. Bars: crossed seed/identity 95% intervals; dotted line: chance.", fontsize=9)
    fig.text(0.03, 0.025, "A/B are overlapping identity assignments. One pool realization per condition; pool size is not an isolated causal effect.", fontsize=9)
    save_figure(fig, out, "fig_extended_exposures")


def fig_raw_learned(out: Path) -> None:
    table = pd.read_csv(EXP / "raw_input_attacker_2026-09-19/raw_input_results.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8), sharey=True)
    endpoints = [(1, "single_mlp", "Single, 1", C["grey"]),
                 (10, "mean_mlp", "Mean, 10", C["blue"]),
                 (10, "deepsets", "DeepSets, 10", C["green"])]
    for axis, dataset in zip(axes, ["MOBIO", "SCface"]):
        subset = table[table["dataset"] == dataset]
        for index, (_, model, label, color) in enumerate(endpoints):
            values = subset[subset["model"] == model].set_index(["scheme", "condition"]).loc[
                [(scheme, condition) for scheme in ["IoM-GRP", "PolyProtect"]
                 for condition in ["independent_unseen_keys", "random_key_pool_4"]]]
            axis.errorbar(np.arange(4) + (index - 1) * 0.17, 100 * values["top1_mean"],
                          yerr=100 * values["top1_std"], fmt="o", color=color, capsize=3, label=label)
        axis.set_xticks(range(4), ["IoM\nFresh", "IoM\nPool 4", "PolyProtect\nFresh", "PolyProtect\nPool 4"])
        axis.axhline(100 * subset["chance"].iloc[0], color=C["black"], ls="--", lw=0.8)
        axis.set_title(dataset)
        axis.set_ylim(-3, 103)
        axis.legend(frameon=False, fontsize=8, loc="upper right")
    axes[0].set_ylabel("Raw-input learned top-1 (%)")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.3, wspace=0.12)
    fig.text(0.03, 0.12, "Bars: standard deviation across three model seeds, NOT confidence intervals. One saved identity split; descriptive study.", fontsize=8.5)
    fig.text(0.03, 0.065, "PolyProtect is near chance in this run; IoM retains large pool-4 gains. No matched unit-input retraining at these seeds.", fontsize=8.5)
    fig.text(0.03, 0.02, "Different pool/set seeds and partitions prevent attributing cross-study accuracy differences solely to normalization.", fontsize=8.5)
    save_figure(fig, out, "fig_raw_learned")


def fig_stricter_selection(out: Path) -> None:
    table = pd.read_csv(EXP / "polyprotect_stricter_audit_2026-09-19/paired_contrasts.csv")
    fig, axis = plt.subplots(figsize=(10.5, 4.1))
    for position, row in table.iterrows():
        axis.errorbar(100 * row["gain"], position,
                      xerr=[[100 * (row["gain"] - row["lower95"])], [100 * (row["upper95"] - row["gain"])]],
                      fmt="o", color=C["blue"], capsize=4)
        axis.text(7, position, f"{100 * row['gain']:+.2f} pp; Holm p={row['holm_p']:.4f}", va="center", fontsize=10)
    axis.set_yticks(range(len(table)), table["dataset"])
    axis.set_ylim(-0.6, 1.6)
    axis.invert_yaxis()
    axis.set_xlim(-4, 13)
    axis.axvline(0, color=C["grey"], ls="--")
    axis.set_xlabel("Stricter minus naive native top-1 (percentage points)")
    axis.set_title("Local stricter selection: no corrected evidence of reduced linkage", pad=15)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.85, bottom=0.32)
    fig.text(0.03, 0.15, "Left of zero would mean less native linkage. Bars: identity-bootstrap 95% intervals, conditional on three key seeds.", fontsize=9)
    fig.text(0.03, 0.09, "20 candidates; 200 development pairs; score band [-0.5, 0.5]. Paired Holm family 2; neither comparison passes 0.05.", fontsize=9)
    fig.text(0.03, 0.03, "Local operationalization, not source-exact replication or a refutation of all stricter PolyProtect parameter policies.", fontsize=9)
    save_figure(fig, out, "fig_stricter_selection")


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
    fig_followup_amplification(args.out)
    fig_followup_native_controls(args.out)
    fig_native_norm_audit(args.out)
    fig_followup_failures(args.out)
    fig_dataset_coverage(args.out)
    fig_pool_replication(args.out)
    fig_extended_exposures(args.out)
    fig_raw_learned(args.out)
    fig_stricter_selection(args.out)
    print(f"figures written to {args.out}")


if __name__ == "__main__":
    main()
