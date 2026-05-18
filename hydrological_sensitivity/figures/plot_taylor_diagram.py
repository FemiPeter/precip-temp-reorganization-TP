"""
figures/plot_taylor_diagram.py
==============================
Taylor diagram for evaluating CMIP6 model performance against
observations, using normalised standard deviation, centred RMSE,
and Pearson correlation coefficient.

Requires the `skill_metrics` package:
    pip install skill_metrics

Input:  CSV with columns:
          Model Names | Correlation Coefficient (R) |
          Normalized Standard Deviation (NSD) | Root Mean Squared Error (RMSE)
Output: taylor_diagram.png

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
INPUT_CSV  = "output/hs/taylor/tas_taylor_combined.csv"
OUTPUT_PNG = "output/figures/taylor_diagram.png"
VARIABLE   = "Surface Temperature (tas)"   # used in the plot title
# ─────────────────────────────────────────────────────────────────────────────

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import skill_metrics as sm

os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)

data         = pd.read_csv(INPUT_CSV)
model_names  = data["Model Names"].tolist()
ccoef_models = data["Correlation Coefficient (R)"].tolist()
sdev_models  = data["Normalized Standard Deviation (NSD)"].tolist()
rmse_models  = data["Root Mean Squared Error (RMSE)"].tolist()

# Include reference observation point (origin)
sdev  = np.array([1.0]  + sdev_models)
crmsd = np.array([0.0]  + rmse_models)
ccoef = np.array([1.0]  + ccoef_models)

# Assign unique colour + marker to each model
COLORS  = ["r", "g", "b", "c", "m", "y", "k"]
SYMBOLS = ["s", "^", ">", "D", "p", "*", "h", "v", "<", "X", "d", "P", "8", "o"]

MARKERS = {
    model: {
        "labelColor": COLORS[i % len(COLORS)],
        "symbol":     SYMBOLS[i % len(SYMBOLS)],
        "size":       7,
        "faceColor":  COLORS[i % len(COLORS)],
        "edgeColor":  COLORS[i % len(COLORS)],
    }
    for i, model in enumerate(model_names)
}

plt.figure(num=1, figsize=(8, 6))

sm.taylor_diagram(
    sdev, crmsd, ccoef,
    markers=MARKERS,
    markerLegend="on",
    styleOBS="-", colOBS="red", markerobs="o",
    tickRMS=[0.5, 1.0, 1.5],
    tickRMSangle=115,
    showlabelsRMS="on",
    titleRMS="off",
    titleOBS="Ref",
)

plt.gca().set_ylabel("Normalised Standard Deviation")
plt.title(
    f"Taylor Diagram — {VARIABLE}",
    fontsize=13, fontweight="bold", pad=40, loc="left",
)

plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
print(f"Saved: {OUTPUT_PNG}")
plt.show()
