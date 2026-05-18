"""
plot_seasonal_bar.py
====================
2×2 grouped bar chart of precipitation-bin frequency (%) by temperature
percentile — one subplot per season.

Input:  Four FULL_BIN_SUMMARY_averages.csv files (one per season)
Output: seasonal_frequency_bar.png

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
# (file path, subplot label) — update paths to match your output directory
SEASON_FILES = [
    ("output/winter/FULL_BIN_SUMMARY_averages.csv",  "(b) Winter"),
    ("output/spring/FULL_BIN_SUMMARY_averages.csv",  "(c) Spring"),
    ("output/summer/FULL_BIN_SUMMARY_averages.csv",  "(d) Summer"),
    ("output/autumn/FULL_BIN_SUMMARY_averages.csv",  "(e) Autumn"),
]
OUTPUT_PNG = "output/figures/seasonal_frequency_bar.png"
Y_MAX      = 50
DPI        = 700
# ─────────────────────────────────────────────────────────────────────────────

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)

bar_width = 0.15
colormap  = cm.coolwarm

fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharex=True, sharey=True)
axes = axes.flatten()

for idx, (filepath, title) in enumerate(SEASON_FILES):
    data         = pd.read_csv(filepath)
    category_col = data.columns[0]
    data_columns = data.columns[1:]
    x            = np.arange(len(data))
    ax           = axes[idx]

    for i, column in enumerate(data_columns):
        color  = colormap(i / len(data_columns))
        offset = (i - len(data_columns) / 2) * bar_width
        ax.bar(x + offset, data[column], bar_width, label=column, color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(data[category_col], rotation=45, ha="right", fontsize=20)
    ax.set_yticks(np.arange(0, Y_MAX + 1, 10))
    ax.set_yticklabels(np.arange(0, Y_MAX + 1, 10), fontsize=20)
    ax.set_ylim(0, Y_MAX)
    ax.set_title(title, fontsize=25, fontweight="bold", loc="left")
    ax.grid(axis="y", linestyle="--", linewidth=0.7)

    if idx % 2 == 0:
        ax.set_ylabel("Frequency (%)", fontsize=25)

# Shared x-axis labels
for col_pos, x_pos in enumerate([0.25, 0.75]):
    fig.text(x_pos, 0.02, "Precipitation Percentile", ha="center", fontsize=25)

# Shared legend
handles, labels = axes[-1].get_legend_handles_labels()
fig.legend(
    handles, labels,
    title="Temperature Percentile", title_fontsize=25,
    loc="lower center", bbox_to_anchor=(0.5, -0.1),
    fontsize=25, ncol=len(data_columns),
)

fig.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(OUTPUT_PNG, dpi=DPI, bbox_inches="tight")
print(f"Saved: {OUTPUT_PNG}")
plt.show()
