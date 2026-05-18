"""
01_bin_data.py
==============
Bins gridded daily precipitation and temperature into combined percentile
intervals (10 precipitation bins × 5 temperature bins).

Run this script once per season (or for the annual dataset) by updating
the USER CONFIGURATION block below.

Output
------
For each input grid-point CSV file, two result CSVs are saved:
  - <name>_temperature_result.csv
  - <name>_precipitation_result.csv

Each CSV has 50 columns (one per combined bin), labelled:
  precip<low>-<high>_temp<low>-<high>

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ──────────────────────────────────────────────────────
TEMPERATURE_FOLDER       = "data/temp/autumn"        # input temperature CSVs
PRECIPITATION_FOLDER     = "data/prec/autumn"        # input precipitation CSVs
TEMPERATURE_OUTPUT_FOLDER = "output/autumn/tmean_bin"
PRECIPITATION_OUTPUT_FOLDER = "output/autumn/prec_bin"
# ────────────────────────────────────────────────────────────────────────────

import os
import numpy as np
import pandas as pd
from tqdm import tqdm


def find_matching_temperature_file(precipitation_file, temperature_folder):
    """Return the temperature file path that matches a given precipitation filename."""
    temperature_filename = os.path.basename(precipitation_file)
    temperature_filepath = os.path.join(temperature_folder, temperature_filename)
    return temperature_filepath if os.path.exists(temperature_filepath) else None


def process_files(temperature_file, precipitation_file):
    """Bin one pair of temperature/precipitation CSV files into percentile categories."""

    temperature_df   = pd.read_csv(temperature_file,   header=None)
    precipitation_df = pd.read_csv(os.path.join(PRECIPITATION_FOLDER, precipitation_file), header=None)

    # Keep only wet-day values (precipitation >= 0.1 mm)
    valid_mask           = precipitation_df >= 0.1
    precipitation_values = precipitation_df.values.flatten()[valid_mask.values.flatten()]
    temperature_values   = temperature_df.values.flatten()[valid_mask.values.flatten()]

    # Define bin edges from percentiles
    precip_pct   = np.percentile(precipitation_values, np.linspace(0, 100, 11))
    temp_pct     = np.percentile(temperature_values,   np.linspace(0, 100, 6))

    precip_intervals = [(precip_pct[i], precip_pct[i + 1]) for i in range(10)]
    temp_intervals   = [(temp_pct[i],   temp_pct[i + 1])   for i in range(5)]

    n_bins = len(precip_intervals) * len(temp_intervals)
    temperature_categories   = [[] for _ in range(n_bins)]
    precipitation_categories = [[] for _ in range(n_bins)]

    def get_category(precip, temp):
        if precip < 0.1:
            return -1
        for i, (p_lo, p_hi) in enumerate(precip_intervals):
            if p_lo <= precip <= p_hi:
                for j, (t_lo, t_hi) in enumerate(temp_intervals):
                    if t_lo <= temp <= t_hi:
                        return i * len(temp_intervals) + j
        return -1

    total = temperature_df.size
    with tqdm(total=total, desc=f"Binning {os.path.basename(precipitation_file)}", leave=False) as pbar:
        for row in range(len(temperature_df)):
            for col in range(len(temperature_df.columns)):
                cat = get_category(precipitation_df.iloc[row, col], temperature_df.iloc[row, col])
                if cat != -1:
                    temperature_categories[cat].append(temperature_df.iloc[row, col])
                    precipitation_categories[cat].append(precipitation_df.iloc[row, col])
                pbar.update(1)

    col_names = [
        f"precip{p[0]:.4f}-{p[1]:.4f}_temp{t[0]:.4f}-{t[1]:.4f}"
        for p in precip_intervals
        for t in temp_intervals
    ]

    temp_result_df  = pd.DataFrame(temperature_categories).T
    prec_result_df  = pd.DataFrame(precipitation_categories).T
    temp_result_df.columns  = col_names
    prec_result_df.columns  = col_names

    base = os.path.splitext(os.path.basename(precipitation_file))[0]
    temp_result_df.to_csv(os.path.join(TEMPERATURE_OUTPUT_FOLDER,   f"{base}_temperature_result.csv"),   index=False)
    prec_result_df.to_csv(os.path.join(PRECIPITATION_OUTPUT_FOLDER, f"{base}_precipitation_result.csv"), index=False)


# ── MAIN ──────────────────────────────────────────────────────────────────────
os.makedirs(TEMPERATURE_OUTPUT_FOLDER,   exist_ok=True)
os.makedirs(PRECIPITATION_OUTPUT_FOLDER, exist_ok=True)

precipitation_files = [f for f in os.listdir(PRECIPITATION_FOLDER) if f.endswith(".csv")]

for prec_file in tqdm(precipitation_files, desc="Processing grid files"):
    temp_file = find_matching_temperature_file(prec_file, TEMPERATURE_FOLDER)
    if temp_file is None:
        print(f"  [SKIP] No matching temperature file for: {prec_file}")
        continue
    process_files(temp_file, prec_file)
