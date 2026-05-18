"""
02_summarize_bins.py
====================
Computes summary statistics (sum, mean, median, frequency) for each
bin column produced by 01_bin_data.py.

Run once per season / dataset by updating the USER CONFIGURATION block.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
INPUT_FOLDER  = "output/autumn/tmean_bin"          # output from 01_bin_data.py
OUTPUT_FOLDER = "output/autumn/tmean_bin/bin_summary"
# ─────────────────────────────────────────────────────────────────────────────

import os
import pandas as pd
from tqdm import tqdm

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

input_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".csv")]

for input_file in tqdm(input_files, desc="Summarising bins"):
    df = pd.read_csv(os.path.join(INPUT_FOLDER, input_file))

    summary_rows = []
    for column in df.columns:
        col_data = df[column].dropna()
        if col_data.empty:
            continue
        summary_rows.append({
            "Interval":  column,
            "Sum":       col_data.sum(),
            "Mean":      col_data.mean(),
            "Median":    col_data.median(),
            "Frequency": col_data.count(),
        })

    summary_df = pd.DataFrame(summary_rows)
    out_file   = os.path.join(OUTPUT_FOLDER, input_file.replace(".csv", "_summary.csv"))
    summary_df.to_csv(out_file, index=False)
    print(f"  Saved: {out_file}")
