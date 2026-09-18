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


def save_diagram(fig, ax, out: Path, name: str) -> None:
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    texts = [text for text in ax.texts if text.get_text()]
    bounds = [text.get_window_extent(renderer) for text in texts]
    for index, (text, bound) in enumerate(zip(texts, bounds)):
        if any(symbol in text.get_text() for symbol in ("\u2014", "\u2013", "\u2212")):
            raise ValueError(f"Unsupported dash in {name}: {text.get_text()}")
        if not ax.bbox.contains(bound.x0, bound.y0) or not ax.bbox.contains(bound.x1, bound.y1):
            raise ValueError(f"Text outside diagram: {text.get_text()}")
        for patch in ax.patches:
            if isinstance(patch, FancyBboxPatch):
                container = patch.get_window_extent(renderer)
                if container.contains(*bound.get_points().mean(axis=0)):
                    inner = container.expanded(0.96, 0.96)
                    if not inner.contains(bound.x0, bound.y0) or not inner.contains(bound.x1, bound.y1):
                        raise ValueError(f"Text crosses box padding: {text.get_text()}")
        for other, other_bound in zip(texts[index + 1:], bounds[index + 1:]):
            if bound.overlaps(other_bound):
                raise ValueError(f"Overlapping text: {text.get_text()} / {other.get_text()}")
    fig.savefig(out / f"{name}.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(out / f"{name}.png", bbox_inches="tight", pad_inches=0.05, dpi=220)
    plt.close(fig)


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
    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.text(0.2, 8.7, "A  DATA AND PROTECTION", fontsize=10, weight="bold", color=BLUE)
    stages = [
        (0.2, "1  Identity-disjoint data", "MOBIO / LFW / FEI / SCface\nTrain / val / test people differ\nGallery never in exposures"),
        (3.45, "2  Fixed face encoder", "YuNet; 5-landmark alignment\nArcFace w600k_r50; 512-D\nUnit norm; frozen backbone"),
        (6.7, "3  Keyed protection", "Template T = f(key, x)\nFresh / pool / shared key\nSecret key values withheld"),
        (9.95, "4  Exposure records", "Input: batch x n x d\n8 nested sets per identity\nn = 1, 10 (initial: 1, 2, 5, 10)"),
    ]
    for left, title, detail in stages:
        ax.add_patch(FancyBboxPatch((left, 6.4), 2.85, 1.65, boxstyle="round,pad=0,rounding_size=0.05", fc="white", ec=BLUE, lw=1.1))
        ax.text(left + 1.425, 7.78, title, ha="center", va="center", fontsize=8.5, weight="bold", color=INK)
        ax.text(left + 1.425, 7.4, detail, ha="center", va="top", fontsize=7.5, linespacing=1.65, color=INK)
    for left, *_ in stages[:-1]:
        arrow(ax, left + 2.87, 7.2, left + 3.23, 7.2, color=BLUE)
    icon_face(ax, 1.625, 8.32, r=0.11, color=BLUE)
    icon_vector(ax, 4.875, 8.32, w=0.8)
    icon_key(ax, 8.125, 8.32, s=1.1)
    icon_bits(ax, 11.375, 8.32, w=0.8)
    ax.text(0.2, 5.98, "OUTPUT d", fontsize=8, weight="bold", color=INK)
    ax.text(1.7, 5.98, "BioHash: 128 bits  |  MLP-Hash: 512 bits  |  IoM-GRP: 300 codes (q=16; one-hot d=4,800)", fontsize=8, color=INK)
    ax.text(1.7, 5.62, "PolyProtect: 170 reals (window m=5, overlap=2). Scheme coverage differs by dataset.", fontsize=8, color=INK)
    ax.plot([0.2, 12.8], [5.28, 5.28], color=GREY, lw=0.6, ls="--")
    ax.text(0.2, 4.88, "B  KEY-BLIND ATTACK AND EVALUATION", fontsize=10, weight="bold", color=GREEN)
    ax.text(0.2, 4.48, "Attacker observes protected records, not keys or slot labels; slots are revealed only in a labelled control.", fontsize=8, color=INK)
    arrow(ax, 12.85, 6.38, 12.85, 4.08, color=BLUE, style="-")
    arrow(ax, 12.85, 4.08, 0.12, 4.08, color=BLUE, style="-")
    arrow(ax, 0.12, 4.08, 0.12, 2.86, color=BLUE, style="-")
    arrow(ax, 0.12, 2.86, 0.35, 2.86, color=BLUE)
    attacks = [
        (0.4, "5  Supervised attacker", "Single / mean / max MLP: d -> 256 -> 512\nDeepSets: encode, mean, decode\nSource embeddings: train targets only"),
        (4.65, "6  Reconstructed embedding", "L2-normalized prediction in 512-D\nTrain on non-test identities\nSelect checkpoint by validation loss"),
        (8.9, "7  Held-out gallery linkage", "Cosine scores vs. unprotected gallery\nTop-1 / top-5 / AUROC / EER / TAR\nIdentity-clustered bootstrap intervals"),
    ]
    for left, title, detail in attacks:
        ax.add_patch(FancyBboxPatch((left, 1.95), 3.85, 1.7, boxstyle="round,pad=0,rounding_size=0.05", fc="white", ec=GREEN, lw=1.1))
        ax.text(left + 1.925, 3.38, title, ha="center", va="center", fontsize=8.5, weight="bold", color=INK)
        ax.text(left + 1.925, 3.0, detail, ha="center", va="top", fontsize=7.5, linespacing=1.65, color=INK)
    icon_net(ax, 2.325, 3.87, color=GREEN, s=0.8)
    icon_vector(ax, 6.575, 3.87, w=0.8, color=GREEN)
    icon_gallery(ax, 10.825, 3.87)
    arrow(ax, 4.27, 2.86, 4.63, 2.86, color=GREEN)
    arrow(ax, 8.52, 2.86, 8.88, 2.86, color=GREEN)
    ax.text(0.4, 1.5, "KEY DESIGN", fontsize=8, weight="bold", color=INK)
    ax.text(2.25, 1.5, "Fresh: source-record keys are split-disjoint. Pool K: hidden transforms recur across identity splits.", fontsize=8, color=INK)
    ax.text(0.4, 1.05, "REPLICATION", fontsize=8, weight="bold", color=INK)
    ax.text(2.25, 1.05, "MOBIO / FEI follow-up: 2 identity partitions x 3 model seeds; matched 120-epoch training caps.", fontsize=8, color=INK)
    ax.text(0.4, 0.6, "DESIGN", fontsize=8, weight="bold", color=INK)
    ax.text(2.25, 0.6, "Same-identity aggregation under controlled transform reuse; detailed attacker paths in the companion figure.", fontsize=8, color=INK)
    save_diagram(fig, ax, out, "fig_architecture")


def fig_attack_detail(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 7.3))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.text(0.2, 9.65, "A  MATCHED EXPOSURE CONSTRUCTION", fontsize=11, weight="bold", color=BLUE)
    ax.text(0.2, 9.15, "One identity, n source records; nested subsets from one fixed permutation per repeat; gallery excluded.", fontsize=9)
    ax.text(0.2, 8.72, "Fresh: independent source-record keys. Pool K: hidden transforms recur across identity splits. No keys or slots in model input.", fontsize=8.5)
    ax.text(0.2, 8.27, "T: B x n x d     d = 128 BioHash; 512 MLP-Hash; 4,800 one-hot IoM-GRP; 170 PolyProtect", fontsize=9, weight="bold")
    ax.plot([0.2, 13.8], [8.05, 8.05], color=GREY, lw=0.7)
    ax.text(0.2, 7.80, "B  TWO AGGREGATION PATHS", fontsize=11, weight="bold", color=GREEN)

    nodes = [
        (0.3, 5.86, 2.65, "Protected record set", "T: B x n x d\nBinary / one-hot / real\nOne identity per set", BLUE),
        (3.4, 6.16, 3.0, "Template-level pooling", "Mean or max across n\nB x d\nSingle baseline: n = 1", GREEN),
        (6.9, 6.16, 3.0, "Reconstruction MLP", "Linear d -> 256; ReLU\nLinear 256 -> 512\nB x 512", GREEN),
        (3.4, 3.94, 3.0, "Shared record encoder", "phi: d -> 256 -> 256\nReLU after each layer\nB x n x 256", ORANGE),
        (6.9, 3.94, 3.0, "Masked feature mean", "sum(m * phi(T)) / sum(m)\nB x 256\nPermutation-invariant", ORANGE),
        (10.4, 3.94, 3.1, "Set decoder", "rho: 256 -> 256 -> 512\nHidden ReLU\nB x 512", ORANGE),
    ]
    for left, bottom, width, title, detail, color in nodes:
        ax.add_patch(FancyBboxPatch((left, bottom), width, 1.45, boxstyle="round,pad=0,rounding_size=0.04", fc="white", ec=color, lw=1.2))
        ax.text(left + width / 2, bottom + 1.18, title, ha="center", va="center", fontsize=9, weight="bold")
        ax.text(left + width / 2, bottom + 0.84, detail, ha="center", va="top", fontsize=8, linespacing=1.35)
    arrow(ax, 2.97, 6.88, 3.38, 6.88, color=GREEN)
    arrow(ax, 6.42, 6.88, 6.88, 6.88, color=GREEN)
    arrow(ax, 1.62, 5.84, 1.62, 4.66, color=ORANGE, style="-")
    arrow(ax, 1.62, 4.66, 3.38, 4.66, color=ORANGE)
    arrow(ax, 6.42, 4.66, 6.88, 4.66, color=ORANGE)
    arrow(ax, 9.92, 4.66, 10.38, 4.66, color=ORANGE)
    box(ax, 10.4, 6.16, 3.1, 1.45, "Unit embedding", "z = output / ||output||2", ec=INK, ts=9, ss=8)
    arrow(ax, 9.92, 6.88, 10.38, 6.88, color=GREEN)
    arrow(ax, 11.95, 5.41, 11.95, 6.14, color=ORANGE)
    ax.text(0.3, 3.52, "Primary: mean-pool MLP. Secondary: DeepSets. m masks valid records; all n records are valid in these runs.", fontsize=8.5)
    ax.plot([0.2, 13.8], [3.19, 3.19], color=GREY, lw=0.7)
    ax.text(0.2, 2.76, "C  SUPERVISION", fontsize=10, weight="bold", color=BLUE)
    ax.text(7.3, 2.76, "D  HELD-OUT IDENTITY LINKAGE", fontsize=10, weight="bold", color=GREEN)
    ax.text(0.2, 2.31, "Target u = normalize(mean of exposed source embeddings).", fontsize=8.5)
    ax.text(0.2, 1.87, "Loss = mean[1 - cosine(z, u)] + 0.1 x MSE(z, u).", fontsize=8.5)
    ax.text(0.2, 1.43, "Adam: lr 0.001; weight decay 0.0001; hidden width 256.", fontsize=8.5)
    ax.text(0.2, 0.99, "Train identities only; select minimum validation loss; freeze test.", fontsize=8.5)
    ax.text(7.3, 2.31, "Scores = z G^T; G: N x 512 unprotected unit gallery.", fontsize=8.5)
    ax.text(7.3, 1.87, "Rank identities; top-1/top-5, AUROC, EER, TAR at FAR.", fontsize=8.5)
    ax.text(7.3, 1.43, "Follow-up: 3 model seeds x 2 identity partitions; 120 epochs.", fontsize=8.5)
    ax.text(7.3, 0.99, "Crossed seed/identity intervals; paired primary contrasts.", fontsize=8.5)
    ax.text(0.2, 0.37, "B: batch size; n: exposure count; d: template input width; N: test gallery identities. Source targets are not inference inputs.", fontsize=8.3, color=INK)
    save_diagram(fig, ax, out, "fig_attack_detail")


# ------------------------------------------------------ Figure: threat model

def fig_threat_model(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    panels = [
        (0.25, "Fresh keys", "one key per source record", "no transform reuse", GREEN, [ORANGE, BLUE, PURPLE, GREEN, RED]),
        (3.45, "Recurring key pool", "k transforms; slot labels hidden", "reuse across train and test", ORANGE, [ORANGE, BLUE, ORANGE, PURPLE, BLUE]),
        (6.65, "Single shared key", "k = 1; key value still hidden", "shared-transform baseline", RED, [ORANGE] * 5),
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
    ax.text(3.45 + pw / 2, py + 0.55, "same colour = same transform", ha="center", fontsize=6.2, color=GREY)

    results = [
        ("Learned attacks inconclusive", "PolyProtect outside the theorem"),
        ("Multi-record gains observed", "boundary depends on dataset and split"),
        ("Strong linkage observed", "hidden does not mean unlearnable"),
    ]
    for (x, *_rest, col, _k), (a, b) in zip(panels, results):
        ax.text(x + pw / 2, 1.12, a, ha="center", fontsize=7.6, color=col, weight="bold")
        ax.text(x + pw / 2, 0.86, b, ha="center", fontsize=6.6, color=GREY)

    ax.plot([0.25, 9.75], [0.62, 0.62], color=GREY, lw=0.6)
    ax.text(0.25, 0.40, "Protocol", fontsize=7.2, weight="bold", color=INK, va="center")
    ax.text(1.45, 0.40, "Disjoint train / validation / test identities; one held-out gallery image per identity",
            fontsize=6.4, color=GREY, va="center")
    ax.text(1.45, 0.16, "8 sets per identity; 3 seeds earlier, 1 in pilots; identity-clustered intervals",
            fontsize=6.4, color=GREY, va="center")

    save_diagram(fig, ax, out, "fig_threat_model")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "reports/figures")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fig_architecture(args.out)
    fig_attack_detail(args.out)
    fig_threat_model(args.out)
    print(f"diagrams written to {args.out}")


if __name__ == "__main__":
    main()
