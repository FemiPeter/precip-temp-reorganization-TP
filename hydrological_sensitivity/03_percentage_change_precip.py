"""
03_percentage_change_precip.py
==============================
Computes the percentage change in precipitation (ΔP%) for each CMIP6
model relative to the piControl baseline:

    ΔP% = ((P(1pctCO2) − P(piControl)) / P(piControl)) × 100

Input files must be matched by filename across the two experiment folders.
Output preserves the subfolder structure of the input.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
FOLDER_1PCTCO2   = "data/cmip6/moving_avg/pr/1pctco2"      # 1pctCO2 precipitation
FOLDER_PICONTROL = "data/cmip6/moving_avg/pr/picontrol"    # piControl precipitation
OUTPUT_FOLDER    = "data/cmip6/moving_avg/pr/delta_pr_pct" # ΔP% output
# ─────────────────────────────────────────────────────────────────────────────

import os
import pandas as pd


def process_files(folder1, folder2, output_folder):
    for root, _, files in os.walk(folder1):
        for file in files:
            if not file.endswith(".csv"):
                continue

            file1_path    = os.path.join(root, file)
            relative_path = os.path.relpath(file1_path, folder1)
            file2_path    = os.path.join(folder2, relative_path)
            output_path   = os.path.join(output_folder, relative_path)

            if not os.path.exists(file2_path):
                print(f"  [SKIP] No matching piControl file for: {relative_path}")
                continue

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            series1            = pd.read_csv(file1_path, header=None).squeeze()
            series2            = pd.read_csv(file2_path, header=None).squeeze()
            pct_change         = ((series1 - series2) / series2) * 100
            pct_change.to_csv(output_path, index=False, header=False)

            print(f"  ΔP% saved: {relative_path}")


process_files(FOLDER_1PCTCO2, FOLDER_PICONTROL, OUTPUT_FOLDER)
print("Precipitation percentage change calculation complete.")
