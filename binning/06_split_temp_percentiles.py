"""
06_split_temp_percentiles.py
============================
Within each precipitation-percentile folder (10th_P … 100th_P), merges
rows from all grid-point files by temperature percentile band and writes
five new files: 20th_T.csv, 40th_T.csv, 60th_T.csv, 80th_T.csv, 100th_T.csv.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
MAIN_FOLDER = "output/autumn/prec_bin/bin_summary/prec_percentiles"
TEMP_LABELS = ["20th_T", "40th_T", "60th_T", "80th_T", "100th_T"]
# ─────────────────────────────────────────────────────────────────────────────

import os
import re
import csv


def sort_key(filename):
    """Sort files numerically by the first integer in the filename."""
    match = re.search(r"(\d+)", filename)
    return int(match.group(1)) if match else float("inf")


for subfolder in os.listdir(MAIN_FOLDER):
    subfolder_path = os.path.join(MAIN_FOLDER, subfolder)
    if not os.path.isdir(subfolder_path):
        continue

    csv_files = sorted(
        [f for f in os.listdir(subfolder_path) if f.endswith(".csv")],
        key=sort_key,
    )

    # Collect one row per file for each temperature position
    row_data = {i: [] for i in range(1, len(TEMP_LABELS) + 1)}
    header   = None

    for filename in csv_files:
        filepath = os.path.join(subfolder_path, filename)
        with open(filepath, newline="") as fh:
            reader = csv.reader(fh)
            if header is None:
                header = next(reader)
            else:
                next(reader)                        # skip header
            for i, row in enumerate(reader, start=1):
                if i in row_data:
                    row_data[i].append(row)

    # Write one output file per temperature percentile
    for i, label in enumerate(TEMP_LABELS, start=1):
        out_path = os.path.join(subfolder_path, f"{label}.csv")
        with open(out_path, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(header)
            writer.writerows(row_data[i])

    print(f"  {subfolder}: temperature percentile files written.")

print("Done — temperature percentile split complete.")
