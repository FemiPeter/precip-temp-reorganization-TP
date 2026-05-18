"""
01_moving_average.py
====================
Applies a 10-year moving average to all CMIP6 model CSV files
(precipitation and temperature) to smooth inter-annual variability
before hydrological sensitivity calculations.

Processes all CSV files recursively, preserving the subfolder structure
from the input directory in the output directory.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
INPUT_FOLDER  = "data/cmip6/raw"          # raw annual model CSVs
OUTPUT_FOLDER = "data/cmip6/moving_avg"   # smoothed output
WINDOW        = 10                        # moving average window (years)
# ─────────────────────────────────────────────────────────────────────────────

import os
import pandas as pd


def calculate_moving_average(data, window):
    return data.rolling(window).mean()


def process_directory(input_dir, output_dir, window):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if not file.endswith(".csv"):
                continue

            input_path    = os.path.join(root, file)
            relative_path = os.path.relpath(input_path, input_dir)
            output_path   = os.path.join(output_dir, relative_path)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            df             = pd.read_csv(input_path, header=None)
            moving_avg_df  = df.apply(lambda col: calculate_moving_average(col, window))
            moving_avg_df.dropna(how="all", inplace=True)
            moving_avg_df.to_csv(output_path, index=False, header=False)

            print(f"  Processed: {relative_path}")


process_directory(INPUT_FOLDER, OUTPUT_FOLDER, WINDOW)
print("Moving average calculation complete.")
