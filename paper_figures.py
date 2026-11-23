"""Draw README figures using the figures4papers publication conventions."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parent
BLUE, PLUM, INK, GRAY, PALE = "#0F4D92", "#915883", "#252c36", "#637084", "#eaf0f7"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False,
    "axes.spines.right": False, "axes.linewidth": .8, "legend.frameon": False,
    "text.color": INK, "svg.fonttype": "none", "svg.hashsalt": "portfolio-paper",
    "pdf.fonttype": 42, "savefig.facecolor": "white",
})


def read_csv(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def save(fig, name):
    path = ROOT / "figures" / name
    path.parent.mkdir(exist_ok=True)
    svg = path.with_suffix(".svg")
    fig.savefig(svg, metadata={"Date": None})
    svg.write_bytes(("\n".join(line.rstrip() for line in
                                svg.read_text(encoding="utf-8").splitlines())+"\n").encode("utf-8"))
    fig.savefig(path.with_suffix(".pdf"), metadata={"CreationDate": None})
    plt.close(fig)


def icon(ax, kind, x):
    left, bottom = x+.60, .85
    if kind in {"file", "grid", "table", "book", "camera", "chip", "check"}:
        shape = FancyBboxPatch((left, bottom), 1.06, .77, boxstyle="round,pad=.05",
                               edgecolor=BLUE, facecolor=PALE, linewidth=1.2)
        ax.add_patch(shape)
        if kind == "check":
            ax.plot([left+.23, left+.45, left+.84], [1.19, 1.01, 1.43], color=PLUM, lw=2.5)
        elif kind == "camera":
            ax.add_patch(Circle((left+.53, 1.23), .23, edgecolor=BLUE, facecolor="white", linewidth=1.5))
            ax.add_patch(Circle((left+.53, 1.23), .095, color=PLUM))
            ax.add_patch(Rectangle((left+.13, 1.62), .29, .10, color=BLUE))
        elif kind in {"grid", "table"}:
            for r in range(3):
                for c in range(4):
                    ax.add_patch(Rectangle((left+.10+c*.225, .96+r*.20), .16, .12,
                                           color=PLUM if (r+c)%4==0 else BLUE, alpha=.65))
        elif kind == "chip":
            ax.add_patch(Rectangle((left+.29, 1.02), .48, .43, facecolor="white", edgecolor=BLUE))
            for i in range(4):
                ax.plot([left+.18+i*.23]*2, [.73, .86], color=PLUM, lw=1.3)
                ax.plot([left+.18+i*.23]*2, [1.61, 1.74], color=PLUM, lw=1.3)
        else:
            for i in range(3):
                ax.plot([left+.19, left+.86-i*.09], [1.45-i*.17]*2,
                        color=PLUM if i==0 else BLUE, lw=1.5)
            if kind == "book":
                ax.plot([left+.54]*2, [.89, 1.58], color=BLUE, lw=.8)
    elif kind in {"wave", "radio", "chart"}:
        t = np.linspace(0, 1, 41)
        if kind == "wave":
            ax.plot(left+t, 1.21 + .22*np.sin(4*np.pi*t)*(.45+.55*t), lw=1.6, color=BLUE)
            ax.plot([left, left+1], [1.21]*2, color=PLUM, ls=":", lw=1)
        elif kind == "radio":
            for radius in (.22, .41, .60):
                angle = np.linspace(.22*np.pi, .78*np.pi, 30)
                ax.plot(left+.53 + radius*np.cos(angle), .99+radius*np.sin(angle), color=BLUE, lw=1.3)
            ax.add_patch(Circle((left+.53, 1), .07, color=PLUM))
        else:
            for i, height in enumerate([.24, .43, .66]):
                ax.add_patch(Rectangle((left+.12+i*.29, .86), .19, height,
                                       color=PLUM if i==2 else BLUE))
            ax.plot([left, left+1.08], [.86]*2, color=INK, lw=.8)
    elif kind == "arm":
        xx, yy = [left+.09, left+.49, left+.93], [.92, 1.63, 1.22]
        ax.plot(xx, yy, color=BLUE, lw=5, solid_capstyle="round")
        ax.scatter(xx, yy, color=PLUM, s=30, zorder=3)
        ax.plot([left+.86, left+1.04], [1.08, 1.08], lw=2, color=BLUE)
    elif kind == "marker":
        ax.add_patch(Rectangle((left+.15, .82), .78, .78, color=BLUE))
        for r,c in [(0,0),(0,3),(1,1),(2,2),(3,0),(3,1)]:
            ax.add_patch(Rectangle((left+.25+c*.15, .92+r*.15), .14, .14, color="white"))
    else:
        raise ValueError(kind)


def pipeline():
    fig, ax = plt.subplots(figsize=(8.6, 2.16))
    fig.subplots_adjust(left=.015, right=.985, bottom=.04, top=.98)
    ax.set(xlim=(0, 10), ylim=(.12, 2.57))
    ax.axis("off")
    for i, (heading, detail, symbol) in enumerate(STAGES):
        x = .07 + 2.52*i
        ax.add_patch(FancyBboxPatch((x, 2.03), 2.25, .41,
                                   boxstyle="round,pad=0,rounding_size=.2", color=BLUE))
        ax.text(x+1.125, 2.235, heading, ha="center", va="center", color="white", weight="bold")
        icon(ax, symbol, x)
        ax.text(x+1.125, .49, detail, ha="center", color=GRAY)
        if i < 3:
            ax.annotate("", (x+2.46, 1.24), (x+2.06, 1.24),
                        arrowprops={"arrowstyle": "-|>", "color": BLUE, "lw": 1})
    save(fig, "paper-workflow")


def letter(ax, value):
    ax.text(-.15, 1.08, value, transform=ax.transAxes, fontsize=13, weight="bold")


STAGES = [["I   Collect","Published benchmarks","book"],["II   Curate","Traceable catalog fields","table"],["III   Validate","Source and integrity checks","check"],["IV   Compare","Common evaluation protocol","chart"]]


def results():
    rows = sorted(read_csv("data/derived/field_presence.csv"),
                  key=lambda row: (float(row["percent_nonempty"]), row["field"]))
    fig, ax = plt.subplots(figsize=(8.6, 3.75))
    coverage = [float(row["percent_nonempty"]) for row in rows]
    ax.barh(range(len(rows)), coverage,
            color=[PLUM if value < 50 else BLUE for value in coverage], height=.63)
    ax.set(yticks=range(len(rows)),
           yticklabels=[row["field"].replace("_", " ").capitalize() for row in rows],
           xlabel="Historical workbook records with a value (%)", xlim=(0, 104),
           xticks=[0, 25, 50, 75, 100])
    fig.subplots_adjust(left=.21, right=.97, bottom=.16, top=.97)
    save(fig, "paper-results")


if __name__ == "__main__":
    pipeline()
    results()
