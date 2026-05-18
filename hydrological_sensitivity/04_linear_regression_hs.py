"""
04_linear_regression_hs.py
==========================
Estimates Hydrological Sensitivity (HS) for each CMIP6 model by
regressing percentage precipitation change (ΔP%) against temperature
change (ΔT) using Ordinary Least Squares (OLS).

The slope of the regression (in %/°C) is the model's HS estimate.
Confidence intervals, p-values, and R² are also recorded.

Matched files in the precipitation and temperature folders are paired
by filename. Results are saved to a single summary CSV.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
PRECIP_FOLDER  = "data/cmip6/moving_avg/pr/delta_pr_pct"   # ΔP% files
TEMP_FOLDER    = "data/cmip6/moving_avg/tas/delta_tas"      # ΔT files
OUTPUT_CSV     = "output/hs/all_models_hs.csv"
# ─────────────────────────────────────────────────────────────────────────────

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)


def perform_regression(precip_file, temp_file):
    precipitation = np.loadtxt(precip_file).reshape(-1, 1)
    temperature   = np.loadtxt(temp_file).reshape(-1, 1)

    # sklearn for slope / intercept / R²
    model     = LinearRegression().fit(temperature, precipitation)
    pred      = model.predict(temperature)
    slope     = model.coef_[0][0]
    intercept = float(model.intercept_)
    r2        = r2_score(precipitation, pred)
    mse       = mean_squared_error(precipitation, pred)

    # statsmodels for p-value and CI
    X        = sm.add_constant(temperature)
    sm_model = sm.OLS(precipitation, X).fit()
    p_value  = sm_model.pvalues[1]
    ci       = sm_model.conf_int()[1]
    margin   = (ci[1] - ci[0]) / 2

    return {
        "slope":                            slope,
        "intercept":                        intercept,
        "r2":                               r2,
        "mse":                              mse,
        "p_value":                          p_value,
        "significant":                      p_value < 0.05,
        "confidence_interval_lower_bound":  ci[0],
        "confidence_interval_upper_bound":  ci[1],
        "margin_of_error":                  margin,
        "slope_pct_per_degC":               slope * 100,
    }


precip_files = {f for f in os.listdir(PRECIP_FOLDER) if f.endswith(".csv")}
temp_files   = {f for f in os.listdir(TEMP_FOLDER)   if f.endswith(".csv")}
matched      = sorted(precip_files & temp_files)

records = []
for fname in matched:
    result = perform_regression(
        os.path.join(PRECIP_FOLDER, fname),
        os.path.join(TEMP_FOLDER, fname),
    )
    result["model_file"] = fname
    records.append(result)
    print(f"  {fname}: slope = {result['slope_pct_per_degC']:.2f} %/°C")

pd.DataFrame(records).to_csv(OUTPUT_CSV, index=False)
print(f"\nResults saved to: {OUTPUT_CSV}")
