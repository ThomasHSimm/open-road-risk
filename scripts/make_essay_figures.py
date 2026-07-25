"""Figures for 'What does a road-risk model actually predict?'.

All four figures are CONCEPTUAL. They use illustrative values chosen to make a
structural point, never Open Road Risk results. This is deliberate: the essay is
the argument layer, and figures containing project metrics would need
regenerating every time a model run changes. Numeric results stay on the pages
that own them.

Usage:
    python make_essay_figures.py --out quarto/assets
"""

from __future__ import annotations

import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

NAVY = "#0E1C2B"
INK = "#16283C"
AMBER = "#F5A623"
RED = "#D1495B"
TEAL = "#22808D"
GREY = "#6B7A8A"
LGREY = "#C9D2DA"
PALE = "#EEF3F7"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.edgecolor": GREY,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": GREY,
        "ytick.color": GREY,
        "axes.titlecolor": NAVY,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


def save(fig, out, name):
    path = os.path.join(out, name + ".png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------------------
# Figure 1 — the same five roads, ranked three ways
# ---------------------------------------------------------------------------
LINKS = [
    # name,               AADT,  km,  observed, modelled expectation
    ("Motorway", 60000, 8.0, 42, 38.0),
    ("Urban A road", 12000, 2.0, 18, 20.0),
    ("Rural A road", 7000, 5.0, 15, 19.0),
    ("Rural B road", 1200, 3.5, 6, 5.0),
    ("Urban minor road", 900, 0.4, 4, 2.2),
]
COLOURS = {
    "Motorway": NAVY,
    "Urban A road": TEAL,
    "Rural A road": GREY,
    "Rural B road": AMBER,
    "Urban minor road": RED,
}


def estimands():
    rows = []
    for name, aadt, km, obs, exp in LINKS:
        # ten years of exposure, in million vehicle-kilometres
        exposure = aadt * km * 365 * 10 / 1e6
        rows.append(
            {
                "name": name,
                "count": obs,
                "rate": obs / exposure * 100,  # per 100M vehicle-km
                "oe": obs / exp,
            }
        )
    return rows


def f01_three_questions(out):
    rows = estimands()
    keys = [
        ("count", "Observed count\nWhere have collisions happened?"),
        ("rate", "Exposure-adjusted rate\nHow many per unit of travel?"),
        ("oe", "Observed vs expected\nMore than the model predicts?"),
    ]
    ranks = {}
    for k, _ in keys:
        order = sorted(rows, key=lambda r: -r[k])
        for i, r in enumerate(order):
            ranks.setdefault(r["name"], []).append(i + 1)

    fig, ax = plt.subplots(figsize=(10.6, 5.0))
    xs = [0, 1, 2]
    for name, ys in ranks.items():
        c = COLOURS[name]
        ax.plot(
            xs,
            ys,
            color=c,
            lw=2.6,
            marker="o",
            ms=11,
            markerfacecolor="white",
            markeredgewidth=2.6,
            zorder=3,
        )
        ax.text(
            -0.09, ys[0], name, ha="right", va="center", fontsize=11.5, color=c, fontweight="bold"
        )
        ax.text(
            2.09, ys[2], name, ha="left", va="center", fontsize=11.5, color=c, fontweight="bold"
        )
        for x, y in zip(xs, ys):
            ax.text(
                x,
                y,
                str(y),
                ha="center",
                va="center",
                fontsize=9.5,
                color=c,
                fontweight="bold",
                zorder=4,
            )

    for x, (_, label) in zip(xs, keys):
        ax.text(
            x,
            0.30,
            label,
            ha="center",
            va="center",
            fontsize=11,
            color=NAVY,
            fontweight="bold",
            linespacing=1.5,
        )

    ax.set_xlim(-1.35, 3.35)
    ax.set_ylim(5.6, 0.05)
    ax.axis("off")
    ax.text(
        1,
        5.52,
        "Rank position (1 = highest priority) for the same five road links",
        ha="center",
        fontsize=10.5,
        color=GREY,
        style="italic",
    )
    fig.tight_layout()
    save(fig, out, "essay-three-questions")


# ---------------------------------------------------------------------------
# Figure 2 — exposure is observed in a few places, needed everywhere
# ---------------------------------------------------------------------------
def f02_exposure(out):
    fig = plt.figure(figsize=(11.2, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.16)

    # --- left: schematic network with a handful of counters
    ax = fig.add_subplot(gs[0, 0])
    rng = np.random.default_rng(11)
    # minor road mesh
    for v in np.linspace(0.08, 0.92, 9):
        ax.plot([0.04, 0.96], [v, v], color=LGREY, lw=1.1, zorder=1)
        ax.plot([v, v], [0.04, 0.96], color=LGREY, lw=1.1, zorder=1)
    # major roads
    majors = [
        ([0.04, 0.96], [0.50, 0.50]),
        ([0.50, 0.50], [0.04, 0.96]),
        ([0.06, 0.94], [0.14, 0.88]),
    ]
    for xs, ys in majors:
        ax.plot(xs, ys, color=NAVY, lw=4.2, solid_capstyle="round", zorder=2)
    # counters sit on major roads only
    counters = [(0.22, 0.50), (0.72, 0.50), (0.50, 0.28), (0.50, 0.80), (0.30, 0.40), (0.78, 0.76)]
    for cx, cy in counters:
        ax.plot(
            cx,
            cy,
            marker="o",
            ms=11,
            color=AMBER,
            markeredgecolor="white",
            markeredgewidth=1.6,
            zorder=4,
        )
    ax.set_title("Traffic is counted here", fontsize=12.5, pad=10)
    ax.text(
        0.5,
        -0.07,
        "Counters (amber) sit on major roads. Every grey link still\n"
        "needs an exposure value before its risk can be compared.",
        ha="center",
        va="top",
        transform=ax.transAxes,
        fontsize=10,
        color=GREY,
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # --- right: propagation chain
    ax2 = fig.add_subplot(gs[0, 1])
    chain = [
        ("Counted traffic", "measured, sparse, biased to major roads", TEAL),
        ("Modelled traffic", "estimated for the rest of the network", AMBER),
        ("Exposure baseline", "entered as if it were known exactly", AMBER),
        ("Expected collisions", "inherits the estimate, and its error", RED),
        ("Published ranking", "a single position, with no interval", RED),
    ]
    y = 0.93
    for i, (head, sub, c) in enumerate(chain):
        ax2.add_patch(
            plt.Rectangle(
                (0.02, y - 0.135), 0.96, 0.135, facecolor=PALE, edgecolor="none", zorder=1
            )
        )
        ax2.plot([0.02, 0.02], [y - 0.135, y], color=c, lw=4, zorder=2)
        ax2.text(0.07, y - 0.042, head, fontsize=11.5, fontweight="bold", color=NAVY, va="center")
        ax2.text(0.07, y - 0.100, sub, fontsize=10, color=GREY, va="center")
        if i < len(chain) - 1:
            ax2.add_patch(
                FancyArrowPatch(
                    (0.5, y - 0.145),
                    (0.5, y - 0.178),
                    arrowstyle="-|>",
                    mutation_scale=13,
                    color=GREY,
                    lw=1.2,
                )
            )
        y -= 0.188
    ax2.set_title("Its uncertainty is needed everywhere", fontsize=12.5, pad=10)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    save(fig, out, "essay-exposure-propagation")


# ---------------------------------------------------------------------------
# Figure 3 — what a sparse count outcome looks like
# ---------------------------------------------------------------------------
def f03_sparsity(out):
    rng = np.random.default_rng(7)
    cols, rows_n = 60, 34
    n = cols * rows_n
    grid = np.zeros(n)
    positives = int(round(n * 0.024))
    grid[rng.choice(n, positives, replace=False)] = 1
    grid = grid.reshape(rows_n, cols)

    fig, ax = plt.subplots(figsize=(11.0, 3.6))
    for r in range(rows_n):
        for c in range(cols):
            filled = grid[r, c] > 0
            ax.add_patch(
                plt.Rectangle(
                    (c, rows_n - r), 0.82, 0.82, facecolor=RED if filled else PALE, edgecolor="none"
                )
            )
    ax.set_xlim(-0.5, cols + 0.5)
    ax.set_ylim(0.4, rows_n + 1.4)
    ax.axis("off")
    ax.set_title(
        "Each square is one road link in one year. Red squares recorded a collision.",
        fontsize=12,
        pad=12,
    )
    ax.text(
        cols / 2,
        0.1,
        "Roughly one link-year in forty. A model that predicts 'no collision' everywhere\n"
        "is right almost all of the time, which is why accuracy is the wrong question.",
        ha="center",
        va="top",
        fontsize=10.5,
        color=GREY,
    )
    fig.tight_layout()
    save(fig, out, "essay-sparsity")


# ---------------------------------------------------------------------------
# Figure 4 — three different generalisation questions
# ---------------------------------------------------------------------------
def f04_validation(out):
    rng = np.random.default_rng(3)
    pts = rng.uniform(0.06, 0.94, (420, 2))
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.9))

    # panel 1 — familiar place
    ax = axes[0]
    test = rng.random(len(pts)) < 0.2
    ax.scatter(pts[~test, 0], pts[~test, 1], s=13, color=LGREY)
    ax.scatter(pts[test, 0], pts[test, 1], s=13, color=RED)
    ax.set_title("A familiar place", fontsize=12)
    ax.text(
        0.5,
        -0.10,
        "Test links sit among their neighbours.\nThe easiest question, and the most flattering.",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9.8,
        color=GREY,
    )

    # panel 2 — new place
    ax = axes[1]
    cx, cy, r = 0.68, 0.62, 0.24
    d = np.hypot(pts[:, 0] - cx, pts[:, 1] - cy)
    ax.scatter(pts[d > r + 0.08, 0], pts[d > r + 0.08, 1], s=13, color=LGREY)
    ax.scatter(pts[d < r, 0], pts[d < r, 1], s=13, color=TEAL)
    buf = (d >= r) & (d <= r + 0.08)
    ax.scatter(pts[buf, 0], pts[buf, 1], s=13, facecolors="white", edgecolors=LGREY, linewidths=0.7)
    ax.add_patch(plt.Circle((cx, cy), r + 0.08, fill=False, ls="--", color=GREY, lw=1.2))
    ax.set_title("A genuinely new place", fontsize=12)
    ax.text(
        0.5,
        -0.10,
        "A whole area is held out, with a buffer.\nNeighbours can no longer leak across.",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9.8,
        color=GREY,
    )

    for ax in axes[:2]:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        for s in ax.spines.values():
            s.set_color(LGREY)

    # panel 3 — a future year
    ax = axes[2]
    years = list(range(2015, 2025))
    for i, yr in enumerate(years):
        c = AMBER if yr < 2024 else RED
        ax.add_patch(plt.Rectangle((i + 0.1, 0.42), 0.8, 0.22, facecolor=c, edgecolor="none"))
        ax.text(i + 0.5, 0.34, str(yr)[2:], ha="center", va="top", fontsize=9, color=GREY)
    ax.text(4.5, 0.72, "train", ha="center", fontsize=10.5, color=AMBER, fontweight="bold")
    ax.text(9.5, 0.72, "test", ha="center", fontsize=10.5, color=RED, fontweight="bold")
    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(0.05, 1.0)
    ax.axis("off")
    ax.set_title("A future year", fontsize=12)
    ax.text(
        0.5,
        0.16,
        "The operational question for a screening tool:\ndoes last year's model still rank next year?",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9.8,
        color=GREY,
    )

    fig.tight_layout()
    save(fig, out, "essay-validation-questions")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="quarto/assets")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    f01_three_questions(args.out)
    f02_exposure(args.out)
    f03_sparsity(args.out)
    f04_validation(args.out)


if __name__ == "__main__":
    main()
