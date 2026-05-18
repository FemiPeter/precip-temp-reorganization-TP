"""
plot_annual_bar.py
==================
Grouped bar chart of precipitation-bin frequency (%) by temperature
percentile for the annual dataset.

Input:  FULL_BIN_SUMMARY_averages.csv  (from 07_final_summary.py)
Output: annual_frequency_bar.png

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
INPUT_CSV  = "output/annual/FULL_BIN_SUMMARY_averages.csv"
OUTPUT_PNG = "output/figures/annual_frequency_bar.png"
Y_MAX      = 50      # maximum y-axis value (%)
DPI        = 700
# ─────────────────────────────────────────────────────────────────────────────

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)

data         = pd.read_csv(INPUT_CSV)
category_col = data.columns[0]
data_columns = data.columns[1:]

x         = np.arange(len(data))
bar_width = 0.15
colormap  = cm.coolwarm

fig, ax = plt.subplots(figsize=(12, 9))

for i, column in enumerate(data_columns):
    color = colormap(i / len(data_columns))
    offset = (i - len(data_columns) / 2) * bar_width
    ax.bar(x + offset, data[column], bar_width, label=column, color=color)

ax.set_xticks(x)
ax.set_xticklabels(data[category_col], rotation=45, ha="right", fontsize=20)
ax.tick_params(axis="y", labelsize=20)
ax.set_xlabel(category_col, fontsize=20)
ax.set_ylabel("Frequency (%)", fontsize=20)
ax.set_ylim(0, Y_MAX)
ax.set_title("", fontsize=25)
ax.grid(axis="y", linestyle="--", linewidth=0.7)

ax.legend(
    title="Temperature Percentile",
    title_fontsize=20,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.25),
    fontsize=18,
    ncol=len(data_columns),
)

plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=DPI, bbox_inches="tight")
print(f"Saved: {OUTPUT_PNG}")
plt.show()
