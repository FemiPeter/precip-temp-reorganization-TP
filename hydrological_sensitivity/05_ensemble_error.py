"""
05_ensemble_error.py
====================
Computes the ensemble mean hydrological sensitivity (HS) and its
95% confidence interval by propagating the uncertainty from individual
model regression slopes.

The ensemble margin of error is derived from the sum of model-level
variances (estimated from each model's 95% CI), giving a combined
standard error for the ensemble mean slope.

Appends the ensemble mean row to the model results CSV from
04_linear_regression_hs.py.

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
INPUT_CSV  = "output/hs/all_models_hs.csv"           # from 04_linear_regression_hs.py
OUTPUT_CSV = "output/hs/all_models_hs_ensemble.csv"  # with ensemble mean appended
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
import pandas as pd

df = pd.read_csv(INPUT_CSV)

# Ensemble mean slope
ensemble_mean = df["slope"].mean()

# Propagate uncertainty: variance per model from its 95% CI margin of error
df["variance"] = (df["margin_of_error"] / 1.96) ** 2
ensemble_variance = df["variance"].sum() / (len(df) ** 2)
ensemble_se       = np.sqrt(ensemble_variance)
ensemble_margin   = 1.96 * ensemble_se

ensemble_ci_lower = ensemble_mean - ensemble_margin
ensemble_ci_upper = ensemble_mean + ensemble_margin

ensemble_row = pd.DataFrame([{
    "model_file":                       "Ensemble Mean",
    "slope":                            ensemble_mean,
    "confidence_interval_lower_bound":  ensemble_ci_lower,
    "confidence_interval_upper_bound":  ensemble_ci_upper,
    "margin_of_error":                  ensemble_margin,
}])

df_out = pd.concat([df, ensemble_row], ignore_index=True)
df_out.to_csv(OUTPUT_CSV, index=False)

print(f"Ensemble Mean HS : {ensemble_mean:.3f} ± {ensemble_margin:.3f} %/°C")
print(f"95% CI           : [{ensemble_ci_lower:.3f}, {ensemble_ci_upper:.3f}]")
print(f"Saved to         : {OUTPUT_CSV}")
