"""Architecture and protocol diagrams for the paper, drawn as vector graphics.

Two figures:
  1. fig_architecture: image -> detect/align -> ArcFace -> normalize -> keyed
     protection -> multi-record set -> key-blind attacker -> gallery linkage.
  2. fig_threat_model: the three key regimes (fresh, recurring pool of k,
     shared) and the identity/key-disjoint evaluation protocol.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Rectangle, Wedge
import numpy as np

ROOT = Path(__file__).resolve().parents[2]

INK = "#222222"
GREY = "#8C8C8C"
LIGHT = "#F4F4F4"
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
RED = "#D55E00"
PURPLE = "#CC79A7"

plt.rcParams.update({"font.family": "serif", "pdf.fonttype": 42})


# ---------------------------------------------------------------- primitives

def box(ax, x, y, w, h, title, sub=None, fc="white", ec=INK, lw=1.0, ts=7.6, ss=6.3, radius=0.07):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}", fc=fc, ec=ec, lw=lw))
    ty = y + h * (0.63 if sub else 0.5)
    ax.text(x + w / 2, ty, title, ha="center", va="center", fontsize=ts, color=INK, weight="bold")
    if sub:
        ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center", fontsize=ss, color=GREY)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=0.9, style="-|>"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=8, color=color, lw=lw, shrinkA=0, shrinkB=0))


def icon_face(ax, cx, cy, r=0.13, color=INK):
    ax.add_patch(Wedge((cx, cy - r * 1.35), r * 1.25, 0, 180, fc="white", ec=color, lw=0.9))
    ax.add_patch(Circle((cx, cy + r * 0.15), r, fc="white", ec=color, lw=0.9))


def icon_vector(ax, cx, cy, n=10, w=0.5, h=0.11, color=BLUE, seed=0):
    vals = np.random.default_rng(seed).uniform(0.25, 1.0, n)
    cw = w / n
    for i, v in enumerate(vals):
        ax.add_patch(Rectangle((cx - w / 2 + i * cw, cy - h / 2), cw, h, fc=color, ec="white", lw=0.4, alpha=0.3 + 0.7 * v))


def icon_bits(ax, cx, cy, n=12, w=0.55, h=0.11, seed=1, color=INK, zorder=3):
    bits = np.random.default_rng(seed).integers(0, 2, n)
    cw = w / n
    for i, b in enumerate(bits):
        ax.add_patch(Rectangle((cx - w / 2 + i * cw, cy - h / 2), cw, h, fc=color if b else "white", ec=color, lw=0.5, zorder=zorder))


def icon_key(ax, cx, cy, color=ORANGE, s=1.0):
    ax.add_patch(Circle((cx - 0.09 * s, cy), 0.065 * s, fc="white", ec=color, lw=1.3))
    ax.plot([cx - 0.025 * s, cx + 0.16 * s], [cy, cy], color=color, lw=1.6, solid_capstyle="round")
    ax.plot([cx + 0.10 * s, cx + 0.10 * s], [cy, cy - 0.05 * s], color=color, lw=1.3)
    ax.plot([cx + 0.15 * s, cx + 0.15 * s], [cy, cy - 0.05 * s], color=color, lw=1.3)


def icon_net(ax, cx, cy, color=PURPLE, s=1.0):
    layers = [3, 4, 2]
    xs = np.linspace(cx - 0.22 * s, cx + 0.22 * s, len(layers))
    pts = []
    for x, n in zip(xs, layers):
        ys = np.linspace(cy - 0.14 * s, cy + 0.14 * s, n)
        pts.append([(x, y) for y in ys])
    for a, b in zip(pts, pts[1:]):
        for (x0, y0) in a:
            for (x1, y1) in b:
                ax.plot([x0, x1], [y0, y1], color=color, lw=0.4, alpha=0.6)
    for layer in pts:
        for (x, y) in layer:
            ax.add_patch(Circle((x, y), 0.024 * s, fc="white", ec=color, lw=0.9))


def icon_gallery(ax, cx, cy, color=INK):
    for dx in (-0.17, 0.0, 0.17):
        ax.add_patch(Rectangle((cx + dx - 0.06, cy - 0.10), 0.12, 0.20, fc="white", ec=color, lw=0.9))
        ax.add_patch(Circle((cx + dx, cy + 0.03), 0.028, fc=color, ec=color))
        ax.plot([cx + dx - 0.035, cx + dx + 0.035], [cy - 0.05, cy - 0.05], color=color, lw=0.8)


# --------------------------------------------------------- Figure: pipeline

def fig_architecture(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.4)
    ax.axis("off")

    # ---- top row: enrolment / protection pipeline
    y, h, w, gap = 3.95, 0.95, 2.06, 0.33
    stages = [
        ("Face image", "MOBIO · LFW · FEI"),
        ("Detect & align", "YuNet, 5 landmarks"),
        ("ArcFace", "buffalo_l, 512-D, unit norm"),
        ("Keyed protection", "BioHash · MLP-Hash"),
        ("Protected record", "binary template"),
    ]
    xs = [0.2 + i * (w + gap) for i in range(len(stages))]
    for x, (t, s) in zip(xs, stages):
        box(ax, x, y, w, h, t, s, ts=7.2, ss=6.0)
    for x0, x1 in zip(xs, xs[1:]):
        arrow(ax, x0 + w + 0.02, y + h / 2, x1 - 0.02, y + h / 2)

    iy = y + h + 0.55
    cx = [x + w / 2 for x in xs]
    icon_face(ax, cx[0], iy)
    ax.add_patch(Rectangle((cx[1] - 0.22, iy - 0.24), 0.44, 0.48, fc="none", ec=INK, lw=0.8, ls=(0, (2, 2))))
    icon_face(ax, cx[1], iy, r=0.10)
    icon_vector(ax, cx[2], iy, seed=3)
    ax.text(cx[2], iy + 0.36, r"$x\,/\,\|x\|_2$", ha="center", fontsize=8, color=INK)
    icon_key(ax, cx[3], iy)
    ax.text(cx[3], iy + 0.38, "secret key  k", ha="center", fontsize=6.8, color=ORANGE)
    arrow(ax, cx[3], iy - 0.16, cx[3], y + h + 0.02, color=ORANGE)
    icon_bits(ax, cx[4], iy, seed=5)
    ax.text(cx[4], iy + 0.38, r"$T = g(P_k\,x)$", ha="center", fontsize=7.5, color=INK)

    # ---- connector: protected records of one person, collected from several services
    ymid = 3.05
    arrow(ax, cx[4], y - 0.02, cx[4], ymid, style="-")
    arrow(ax, cx[4], ymid, 1.20, ymid, style="-")
    arrow(ax, 1.20, ymid, 1.20, 2.35, style="-|>")
    ax.text(6.0, ymid + 0.13, "n protected records of the same person, each from a different image and a different service",
            ha="center", fontsize=6.6, color=GREY)

    # ---- bottom row: attack
    y2, h2 = 0.95, 0.95
    for i in range(3):
        ax.add_patch(FancyBboxPatch((0.30 + 0.09 * (2 - i), y2 + 0.09 * i), 1.80, 0.78, boxstyle="round,pad=0,rounding_size=0.05",
                                    fc=LIGHT if i < 2 else "white", ec=INK, lw=0.9, zorder=i))
    icon_bits(ax, 1.20, y2 + 0.18 + 0.50, n=12, w=1.1, h=0.14, seed=11, zorder=5)
    ax.text(1.20, y2 + 0.18 + 0.22, "n records", ha="center", fontsize=7.2, weight="bold", color=INK, zorder=5)
    ax.text(1.20, y2 - 0.22, "n = 1, 2, 5, 10", ha="center", fontsize=6.3, color=GREY)

    bx = [2.95, 6.35, 8.75]
    bw = [2.95, 1.95, 2.35]
    box(ax, bx[0], y2, bw[0], h2, "Key-blind attacker", "MLP · mean / max pool · DeepSets", ts=7.2, ss=6.0)
    box(ax, bx[1], y2, bw[1], h2, "Prediction", "512-D embedding", ts=7.2, ss=6.0)
    box(ax, bx[2], y2, bw[2], h2, "Gallery", "unprotected, 1 image / identity", ts=7.2, ss=6.0)
    icon_net(ax, bx[0] + bw[0] / 2, y2 + h2 + 0.45)
    icon_vector(ax, bx[1] + bw[1] / 2, y2 + h2 + 0.45, w=0.9, seed=8, color=GREEN)
    icon_gallery(ax, bx[2] + bw[2] / 2, y2 + h2 + 0.45)

    arrow(ax, 2.30, y2 + h2 / 2, bx[0] - 0.02, y2 + h2 / 2)
    arrow(ax, bx[0] + bw[0] + 0.02, y2 + h2 / 2, bx[1] - 0.02, y2 + h2 / 2)
    arrow(ax, bx[1] + bw[1] + 0.02, y2 + h2 / 2, bx[2] - 0.02, y2 + h2 / 2)
    ax.text((bx[1] + bw[1] + bx[2]) / 2, y2 + h2 / 2 + 0.17, "cosine", ha="center", fontsize=6.3, color=GREY)

    ax.text(bx[0], y2 - 0.22, "trained on records of disjoint identities; knows the scheme, never a key",
            fontsize=6.3, color=GREY, va="top")
    ax.text(bx[2] + bw[2], y2 - 0.46, "top-1 / top-5 · AUROC · EER", fontsize=6.3, color=GREY, va="top", ha="right")

    fig.savefig(out / "fig_architecture.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(out / "fig_architecture.png", bbox_inches="tight", pad_inches=0.05, dpi=220)
    plt.close(fig)


# ------------------------------------------------------ Figure: threat model

def fig_threat_model(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    panels = [
        (0.25, "Fresh keys", "a new key for every record", "covered by Theorem 1", GREEN, [ORANGE, BLUE, PURPLE, GREEN, RED]),
        (3.45, "Recurring pool of k keys", "slot label hidden from attacker", "empirical boundary", ORANGE, [ORANGE, BLUE, ORANGE, PURPLE, BLUE]),
        (6.65, "Single shared key", "k = 1", "stolen-token analogue", RED, [ORANGE] * 5),
    ]
    pw, ph, py = 3.10, 3.15, 1.55
    for x, title, sub, tag, col, key_colors in panels:
        ax.add_patch(FancyBboxPatch((x, py), pw, ph, boxstyle="round,pad=0,rounding_size=0.08", fc="white", ec=col, lw=1.3))
        ax.text(x + pw / 2, py + ph - 0.24, title, ha="center", fontsize=7.4, weight="bold", color=INK)
        ax.text(x + pw / 2, py + ph - 0.47, sub, ha="center", fontsize=6.6, color=GREY)
        rows = np.linspace(py + ph - 0.85, py + 0.80, 5)
        for i, ry in enumerate(rows):
            icon_face(ax, x + 0.42, ry + 0.03, r=0.085)
            arrow(ax, x + 0.66, ry, x + 0.96, ry, lw=0.6, color=GREY)
            icon_key(ax, x + 1.22, ry, color=key_colors[i], s=0.8)
            arrow(ax, x + 1.44, ry, x + 1.72, ry, lw=0.6, color=GREY)
            icon_bits(ax, x + 2.35, ry, n=10, w=1.05, h=0.12, seed=20 + i)
        ax.text(x + pw / 2, py + 0.30, tag, ha="center", fontsize=7.3, color=col, style="italic")
    ax.text(3.45 + pw / 2, py + 0.55, "same colour = same hidden transform", ha="center", fontsize=6.2, color=GREY)

    results = [
        (r"$I(Y;\,T_1,\ldots,T_n)=0$", "top-1 at chance for every n"),
        ("1 record at chance, 10 records not", "leakage falls as k grows"),
        ("transform is learnable", "70-80 % top-1"),
    ]
    for (x, *_rest, col, _k), (a, b) in zip(panels, results):
        ax.text(x + pw / 2, 1.12, a, ha="center", fontsize=7.6, color=col, weight="bold")
        ax.text(x + pw / 2, 0.86, b, ha="center", fontsize=6.6, color=GREY)

    ax.plot([0.25, 9.75], [0.62, 0.62], color=GREY, lw=0.6)
    ax.text(0.25, 0.40, "Protocol", fontsize=7.2, weight="bold", color=INK, va="center")
    ax.text(1.20, 0.40, "identity-disjoint train / val / test  ·  test keys never seen in training  ·  one held-out gallery image per identity",
            fontsize=6.4, color=GREY, va="center")
    ax.text(1.20, 0.16, "8 nested record sets per identity  ·  3 model seeds  ·  identity-clustered 95 % intervals  ·  preregistered pass / fail per condition",
            fontsize=6.4, color=GREY, va="center")

    fig.savefig(out / "fig_threat_model.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(out / "fig_threat_model.png", bbox_inches="tight", pad_inches=0.05, dpi=220)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "reports/figures")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fig_architecture(args.out)
    fig_threat_model(args.out)
    print(f"diagrams written to {args.out}")


if __name__ == "__main__":
    main()
