"""
plot_spatial_map.py
===================
Spatial map of precipitation-frequency (%) for each combination of
precipitation percentile (columns) × temperature percentile (rows),
plotted on the Tibetan Plateau using Cartopy.

Applicable to annual or any seasonal dataset by updating paths below.

Inputs
------
- Percentile CSV files organised as:
    <MAIN_DIRECTORY>/<precip_percentile_folder>/<temp_percentile_file>.csv
- Coordinate file:  data/coords/TP_cood.csv   (longitude, latitude columns)
- Shapefile:        data/coords/tp_roi.shp

Output
------
  output/figures/spatial_frequency_map.png

Paper
-----
Hydrological Sensitivity and the Reorganization of Precipitation
with Temperature over the Tibetan Plateau
Olowe & Cuo
"""

# ── USER CONFIGURATION ───────────────────────────────────────────────────────
MAIN_DIRECTORY   = "output/annual/prec_bin/bin_summary/prec_percentiles"
COORDINATES_CSV  = "data/coords/TP_cood.csv"          # cols: longitude, latitude
SHAPEFILE        = "data/coords/tp_roi.shp"
OUTPUT_PNG       = "output/figures/spatial_frequency_map.png"

PRECIP_FOLDERS   = ["10th_P", "20th_P", "30th_P", "40th_P", "50th_P",
                    "60th_P", "70th_P", "80th_P", "90th_P", "100th_P"]
TEMP_FILES       = ["20th_T", "40th_T", "60th_T", "80th_T", "100th_T"]

VMIN, VMAX = 0, 50   # colorbar range (%)
DPI        = 700
# ─────────────────────────────────────────────────────────────────────────────

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import geopandas as gpd
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)

# ── Load boundary shapefile ───────────────────────────────────────────────────
boundary = gpd.read_file(SHAPEFILE)

# ── Load coordinates ──────────────────────────────────────────────────────────
coords_raw = pd.read_csv(COORDINATES_CSV, header=None)
longitude  = coords_raw.iloc[:, 0]
latitude   = coords_raw.iloc[:, 1]

n_rows = len(TEMP_FILES)
n_cols = len(PRECIP_FOLDERS)

fig, axes = plt.subplots(
    n_rows, n_cols,
    figsize=(28, n_rows * 2),
    subplot_kw={"projection": ccrs.PlateCarree()},
)
axes = axes.flatten()

cmap = plt.cm.jet_r
sc   = None   # will hold the last scatter for the colorbar

for col, folder_name in enumerate(PRECIP_FOLDERS):
    subfolder = os.path.join(MAIN_DIRECTORY, folder_name)

    for row, file_stem in enumerate(TEMP_FILES):
        filename  = f"{file_stem}.csv"
        file_path = os.path.join(subfolder, filename)

        if not os.path.isfile(file_path):
            continue

        ax = axes[row * n_cols + col]

        # Load per-grid percentage values
        pct_data = pd.read_csv(file_path)["Percentage"]

        # Build GeoDataFrame and clip to TP boundary
        gdf = gpd.GeoDataFrame(
            coords_raw,
            geometry=gpd.points_from_xy(longitude, latitude),
            crs="EPSG:4326",
        )
        boundary_reproj = boundary.to_crs(gdf.crs)
        clipped = gpd.clip(gdf, boundary_reproj)
        merged  = clipped.merge(pct_data, left_index=True, right_index=True)

        sc = ax.scatter(
            merged.geometry.x,
            merged.geometry.y,
            c=merged["Percentage"],
            cmap=cmap,
            s=20,
            alpha=0.8,
            transform=ccrs.PlateCarree(),
            norm=plt.Normalize(vmin=VMIN, vmax=VMAX),
        )

        boundary_reproj.plot(
            ax=ax, facecolor="none", edgecolor="black",
            linewidth=0.5, transform=ccrs.PlateCarree(),
        )
        ax.coastlines()

        # Column titles (top row only)
        if row == 0:
            ax.set_title(folder_name, fontsize=18)

        # Row labels (left column only)
        if col == 0:
            ax.annotate(
                file_stem,
                xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 5, 0),
                xycoords=ax.yaxis.label, textcoords="offset points",
                size=18, ha="center", va="center", rotation=90,
            )

        # Tick formatting
        bounds = boundary_reproj.total_bounds
        x_ticks = np.round(np.linspace(bounds[0], bounds[2], 7)).astype(int)[1:-1:2]
        y_ticks = np.round(np.linspace(bounds[1], bounds[3], 3)).astype(int)

        if row == 0:
            ax.set_xticks(x_ticks, crs=ccrs.PlateCarree())
            ax.xaxis.set_major_formatter(LongitudeFormatter())
            ax.tick_params(axis="x", top=True, bottom=False, labeltop=True, labelbottom=False, labelsize=13)
        else:
            ax.set_xticks([])

        if col == n_cols - 1:
            ax.set_yticks(y_ticks, crs=ccrs.PlateCarree())
            ax.yaxis.set_major_formatter(LatitudeFormatter())
            ax.tick_params(axis="y", left=False, right=True, labelleft=False, labelright=True, labelsize=13)
        else:
            ax.set_yticks([])

# Remove unused axes
for i in range(n_cols * n_rows, len(axes)):
    fig.delaxes(axes[i])

plt.subplots_adjust(wspace=0.07, hspace=0.0)

# Colorbar
if sc is not None:
    cbar = fig.colorbar(sc, ax=axes, orientation="horizontal", pad=0.02, aspect=75,
                        ticks=np.arange(VMIN, VMAX + 1, 5))
    cbar.ax.tick_params(labelsize=25)
    cbar.set_label("Frequency (%)", fontsize=25)

# Panel label
fig.text(0.115, 0.88, "a", fontsize=40, fontweight="bold", transform=fig.transFigure)

plt.savefig(OUTPUT_PNG, dpi=DPI, bbox_inches="tight")
print(f"Saved: {OUTPUT_PNG}")
plt.show()
