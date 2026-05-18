"""
04_calculate_percentage.py
==========================
Adds a 'Percentage' column to every CSV inside the precipitation-percentile
folder tree (output from 03_split_prec_percentiles.py).

Percentage = (row Frequency / total Frequency for that file) × 100

Files are updated in-place.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
MAIN_FOLDER = "output/autumn/prec_bin/bin_summary/prec_percentiles"
# ─────────────────────────────────────────────────────────────────────────────

import os
import pandas as pd
from tqdm import tqdm

csv_files = [
    os.path.join(root, f)
    for root, _, files in os.walk(MAIN_FOLDER)
    for f in files if f.endswith(".csv")
]

for csv_path in tqdm(csv_files, desc="Calculating percentages"):
    df = pd.read_csv(csv_path)
    total = df["Frequency"].sum()
    df["Percentage"] = (df["Frequency"] / total * 100) if total > 0 else 0.0
    df.to_csv(csv_path, index=False)

print(f"Percentage column added to {len(csv_files)} files.")
