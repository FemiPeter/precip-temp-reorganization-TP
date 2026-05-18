"""
05_add_boolean_flag.py
======================
Adds a boolean column 'H' to each CSV in the percentile folder tree.
H = True for the row with the highest Percentage value (the dominant
temperature bin for that precipitation percentile).

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

for csv_path in tqdm(csv_files, desc="Adding boolean flag"):
    df = pd.read_csv(csv_path)
    df["H"] = df["Percentage"] == df["Percentage"].max()
    df.to_csv(csv_path, index=False)

print(f"Boolean flag 'H' added to {len(csv_files)} files.")
