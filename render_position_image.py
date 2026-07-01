#!/usr/bin/env python3
"""
Render a static top-view position image for the demo page.

The visual style matches the position animation used in infer_hrtf.py:
- top view
- dashed outer circle
- head marker at the center
- source dots on the circle

Example:
  python3 render_position_image.py \
    --positions "230,320,50,140" \
    --output "assets/static/Cristina Vane - So Easy/position.png"

  python3 render_position_image.py \
    --positions "0,90,180,270" \
    --output "assets/static/AM Contra - Heart Peripheral/position.png"
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np


SOURCE_ORDER = ["drums", "bass", "other", "vocals"]
SOURCE_COLORS = {
    "drums": "#d95f02",
    "bass": "#1b9e77",
    "other": "#7570b3",
    "vocals": "#e7298a",
}


def azimuth_to_xy(angle_deg: float, radius: float = 1.0) -> tuple[float, float]:
    theta = np.deg2rad(float(angle_deg))
    return radius * float(np.sin(theta)), radius * float(np.cos(theta))


def parse_positions(text: str) -> list[float]:
    vals = [x.strip() for x in text.split(",") if x.strip()]
    if len(vals) != len(SOURCE_ORDER):
        raise ValueError(
            f"--positions needs {len(SOURCE_ORDER)} azimuths, got {len(vals)}"
        )
    return [float(v) for v in vals]


def build_figure(positions: Iterable[float], output_path: Path) -> None:
    pos_vals = list(positions)
    fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=120)
    fig.patch.set_facecolor("white")

    ax.set_aspect("equal")
    ax.set_xlim(-1.14, 1.14)
    ax.set_ylim(-1.14, 1.14)
    ax.axis("off")

    circle = plt.Circle(
        (0, 0),
        1.0,
        fill=False,
        linewidth=1.6,
        linestyle="--",
        color="#555555",
        alpha=0.6,
    )
    head = plt.Circle((0, 0), 0.12, color="#222222")
    ax.add_patch(circle)
    ax.add_patch(head)
    ax.arrow(
        0,
        0.12,
        0,
        0.16,
        width=0.015,
        head_width=0.07,
        head_length=0.06,
        length_includes_head=True,
        color="#222222",
    )
    for name, angle in zip(SOURCE_ORDER, pos_vals):
        x, y = azimuth_to_xy(angle, radius=1.0)
        ax.scatter(
            [x],
            [y],
            s=320,
            color=SOURCE_COLORS.get(name, "#444444"),
            edgecolors="white",
            linewidths=1.2,
            zorder=3,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--positions",
        required=True,
        help='Comma-separated azimuths in the order "drums,bass,other,vocals".',
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the output PNG.",
    )
    args = parser.parse_args()

    positions = parse_positions(args.positions)
    build_figure(positions, Path(args.output).expanduser())


if __name__ == "__main__":
    main()
