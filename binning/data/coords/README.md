# data/coords/

This folder contains the spatial reference files required by the plotting scripts.

## Files

| File | Description |
|------|-------------|
| `TP_cood.csv` | Grid-point coordinates for the Tibetan Plateau (columns: longitude, latitude). No header row. |
| `tp_roi.shp` (+ sidecar files) | Tibetan Plateau boundary shapefile used for clipping and map overlays. |

## Note on the coordinate dataset

The gridded precipitation and temperature data were interpolated to a
0.25° × 0.25° resolution following Cuo et al. (2013, 2017).
`TP_cood.csv` contains the longitude/latitude pairs for every grid cell
within the TP domain and corresponds row-for-row with the input CSV files
used by the binning pipeline.
