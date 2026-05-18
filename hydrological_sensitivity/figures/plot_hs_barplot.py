"""
figures/plot_hs_barplot.py
==========================
Horizontal grouped bar chart of Hydrological Sensitivity (%/°C) for
each CMIP6 model and season, with 95% confidence interval error bars.

One bar group per model; five bars per group (Annual + four seasons).
The Ensemble Mean is included as the final model row.

Input:  One CSV per season (from 05_ensemble_error.py or equivalent)
Output: hs_barplot.png

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
SEASON_FILES = {
    "Annual": "output/hs/seasonal/regional_annual_E.csv",
    "Winter": "output/hs/seasonal/regional_winter_E.csv",
    "Spring": "output/hs/seasonal/regional_spring_E.csv",
    "Summer": "output/hs/seasonal/regional_summer_E.csv",
    "Autumn": "output/hs/seasonal/regional_autumn_E.csv",
}
OUTPUT_PNG   = "output/figures/hs_barplot.png"
X_MIN, X_MAX = -2, 11     # x-axis limits
DPI          = 700
# ─────────────────────────────────────────────────────────────────────────────

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns

sns.set(style="white")
os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)

# ── Load and combine data ─────────────────────────────────────────────────────
data_list = []
for season, path in SEASON_FILES.items():
    df = pd.read_csv(path)
    df["Season"] = season
    data_list.append(df)
data = pd.concat(data_list, ignore_index=True)

# Model order (inverted for horizontal bar readability)
models       = list(reversed(data["Name"].unique()))
season_order = list(SEASON_FILES.keys())

# Standard deviation of individual model slopes (excluding Ensemble Mean)
season_std = {
    s: data[(data["Season"] == s) & (data["Name"] != "Ensemble Mean")]["slope"].std()
    for s in season_order
}

colors = {
    "Annual": "gray",
    "Winter": "dodgerblue",
    "Spring": "limegreen",
    "Summer": "orangered",
    "Autumn": "darkorange",
}

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax     = plt.subplots(figsize=(10, 15))
bar_width   = 0.25
group_gap   = 1.5
y_positions = np.arange(len(models)) * group_gap

legend_handles, legend_labels = [], []

for i, season in enumerate(season_order):
    season_data = data[data["Season"] == season]
    slopes      = [
        season_data[season_data["Name"] == m]["slope"].values[0]
        if m in season_data["Name"].values else np.nan
        for m in models
    ]
    lower_err = (season_data["slope"] - season_data["confidence_interval_lower_bound"]).values
    upper_err = (season_data["confidence_interval_upper_bound"] - season_data["slope"]).values

    positions    = y_positions[::-1] + (i - 2) * bar_width
    valid        = ~np.isnan(slopes)
    slopes_arr   = np.array(slopes)

    bars = ax.barh(
        positions[valid], slopes_arr[valid],
        xerr=[lower_err[valid], upper_err[valid]],
        capsize=5, height=bar_width,
        color=colors[season], alpha=0.8, edgecolor="black",
        label=f"{season} (σ = {season_std[season]:.1f})",
    )
    legend_handles.append(bars[0])
    legend_labels.append(f"{season} (σ = {season_std[season]:.1f})")

    # Value labels
    for j, pos in enumerate(positions[valid]):
        sv  = slopes_arr[valid][j]
        ue  = upper_err[valid][j]
        le  = lower_err[valid][j]
        err = (ue + le) / 2
        ax.text(
            sv + ue + 0.2, pos - 0.037,
            f"{sv:.1f} ± {err:.1f}",
            ha="left", va="center", fontsize=10, fontweight="bold",
            path_effects=[path_effects.withStroke(linewidth=1, foreground="white")],
        )

# ── Formatting ────────────────────────────────────────────────────────────────
ax.axvline(0, color="gray", linestyle="--", alpha=0.5)
ax.set_yticks(y_positions[::-1])
ax.set_yticklabels(models, fontsize=16)
ax.set_ylabel("Model Name", fontsize=20, fontweight="bold")
ax.set_xlim(X_MIN, X_MAX)
ax.set_xlabel("Hydrological Sensitivity (%/°C)", fontsize=20, fontweight="bold")
ax.set_title("Tibetan Plateau Hydrological Sensitivity", fontsize=25, fontweight="bold", pad=20)
ax.tick_params(axis="x", labelsize=13.5)

min_y = min(y_positions) - bar_width * 4
max_y = max(y_positions) + bar_width * 4
ax.set_ylim(min_y + 0.1, max_y - 0.1)

ax.legend(legend_handles, legend_labels, loc="upper right", fontsize=15,
          frameon=True, shadow=True, fancybox=True)
ax.grid(False)
plt.subplots_adjust(top=0.97, bottom=0.01)

plt.savefig(OUTPUT_PNG, dpi=DPI, bbox_inches="tight")
print(f"Saved: {OUTPUT_PNG}")
plt.show()
