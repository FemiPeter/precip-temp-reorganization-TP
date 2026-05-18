"""
03_split_prec_percentiles.py
============================
Splits each summary CSV (from 02_summarize_bins.py) into 10 sub-folders,
one per precipitation percentile band (10th_P … 100th_P).

Each folder contains one file per grid point, holding the 5 temperature-bin
rows that correspond to that precipitation percentile.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
INPUT_DIRECTORY  = "output/autumn/prec_bin/bin_summary"
OUTPUT_DIRECTORY = "output/autumn/prec_bin/bin_summary"   # folders created inside here
ROWS_PER_FILE    = 5    # one row per temperature percentile band
# ─────────────────────────────────────────────────────────────────────────────

import os
import csv
from tqdm import tqdm


def ordinal_suffix(n):
    """Return ordinal label, e.g. 10 → '10th_P', 21 → '21st_P'."""
    if 11 <= (n % 100) <= 13:
        return f"{n}th_P"
    return {1: f"{n}st_P", 2: f"{n}nd_P", 3: f"{n}rd_P"}.get(n % 10, f"{n}th_P")


os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

csv_files = [f for f in os.listdir(INPUT_DIRECTORY) if f.endswith(".csv")]

for file_name in tqdm(csv_files, desc="Splitting precipitation percentiles"):
    input_path             = os.path.join(INPUT_DIRECTORY, file_name)
    base_name              = os.path.splitext(file_name)[0]

    with open(input_path, newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        data   = list(reader)

    for i in range(10):
        folder_name = ordinal_suffix((i + 1) * 10)
        folder_path = os.path.join(OUTPUT_DIRECTORY, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        out_path = os.path.join(folder_path, f"{base_name}.csv")
        row_slice = data[i * ROWS_PER_FILE : (i + 1) * ROWS_PER_FILE]

        with open(out_path, "w", newline="") as out_fh:
            writer = csv.writer(out_fh)
            writer.writerow(header)
            writer.writerows(row_slice)

print("Done — precipitation percentile folders created.")
