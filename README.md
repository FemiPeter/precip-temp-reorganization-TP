# precip-temp-reorganization-TP
Code for: Hydrological Sensitivity and the Reorganization of Precipitation with Temperature over the Tibetan Plateau (Olowe &amp; Cuo)


binning/ — Percentile-based binning pipeline for analysing precipitation reorganisation with temperature. Scripts are numbered in execution order:

01_bin_data.py — Bins gridded daily precipitation and temperature into combined percentile intervals (10 precipitation × 5 temperature bins). Applicable to annual or any seasonal subset by updating the input folder paths.
02_summarize_bins.py — Computes sum, mean, median, and frequency statistics for each bin column.
03_split_prec_percentiles.py — Splits the summary output into separate folders by precipitation percentile (10th_P through 100th_P).
04_calculate_percentage.py — Adds a frequency percentage column to each sub-file.
05_add_boolean_flag.py — Flags the temperature bin with the highest precipitation frequency per file (column H).
06_split_temp_percentiles.py — Reorganises files by temperature percentile (20th_T through 100th_T) within each precipitation percentile folder.
07_final_summary.py — Aggregates results into three summary CSVs: percentage of H=True, row counts, and average percentages across all bins.


## Citation

If you use this code in your research, please cite:

Jesufemi Olowe. (2026). FemiPeter/precip-temp-reorganization-TP: v1.0.0 — 
Initial release (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.20269001
