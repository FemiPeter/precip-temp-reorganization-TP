"""
07_final_summary.py
===================
Aggregates the per-grid-point percentile results into three summary CSVs:

  FULL_BIN_SUMMARY.csv               — % of H=True per precipitation/temp band
  FULL_BIN_SUMMARY_row_counts.csv    — number of grid cells per band
  FULL_BIN_SUMMARY_averages.csv      — mean Percentage per band

These are the inputs used for the bar-chart figures.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
PARENT_DIR     = "output/autumn/prec_bin/bin_summary/prec_percentiles"
OUTPUT_DIR     = "output/autumn"
TEMP_FILES     = ["20th_T.csv", "40th_T.csv", "60th_T.csv", "80th_T.csv", "100th_T.csv"]
# ─────────────────────────────────────────────────────────────────────────────

import os
import pandas as pd

os.makedirs(OUTPUT_DIR, exist_ok=True)

results_dict   = {}
row_count_dict = {}
average_dict   = {}

for folder_name in sorted(os.listdir(PARENT_DIR)):
    folder_path = os.path.join(PARENT_DIR, folder_name)
    if not os.path.isdir(folder_path):
        continue

    folder_results    = {}
    folder_row_counts = {}
    folder_averages   = {}

    for temp_file in TEMP_FILES:
        file_path = os.path.join(folder_path, temp_file)
        if not os.path.isfile(file_path):
            continue

        df = pd.read_csv(file_path)

        pct_true      = (df["H"].sum() / len(df) * 100) if len(df) > 0 else 0.0
        row_count     = len(df)
        avg_percentage = df["Percentage"].mean()

        folder_results[temp_file]    = pct_true
        folder_row_counts[temp_file] = row_count
        folder_averages[temp_file]   = avg_percentage

    results_dict[folder_name]   = folder_results
    row_count_dict[folder_name] = folder_row_counts
    average_dict[folder_name]   = folder_averages

# Convert to DataFrames and save
results_df   = pd.DataFrame(results_dict).T
row_count_df = pd.DataFrame(row_count_dict).T
averages_df  = pd.DataFrame(average_dict).T

results_df.to_csv(  os.path.join(OUTPUT_DIR, "FULL_BIN_SUMMARY.csv"))
row_count_df.to_csv(os.path.join(OUTPUT_DIR, "FULL_BIN_SUMMARY_row_counts.csv"))
averages_df.to_csv( os.path.join(OUTPUT_DIR, "FULL_BIN_SUMMARY_averages.csv"))

print(f"Summaries saved to: {OUTPUT_DIR}")
