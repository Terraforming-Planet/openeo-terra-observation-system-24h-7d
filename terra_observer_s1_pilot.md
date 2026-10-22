# TerraObserver — openEO Pilot: Sentinel-1 SAR Change Detection (Southern Poland)

## Status: NOT EXECUTED — pending approval

## Project context
- Parent project: Terraforming Planet / TerraObserver
- Repos: Polar-Sun-Moon-Analysis, openeo-terra-observation-system-24h-7d
- Purpose: exploratory candidate-change raster from Sentinel-1 backscatter,
  NOT a verified flood warning or environmental-cause inference.

## Backend
Copernicus Data Space Ecosystem (CDSE) openEO: https://openeo.dataspace.copernicus.eu/

## Parameters
- AOI (WGS84 bbox): west 16.7, south 50.08, east 18.0, north 50.5
- Baseline period: 2024-08-25 to 2024-09-09
- Comparison period: 2024-09-14 to 2024-09-22
- Collection: SENTINEL1_GRD
- Band: VV
- Orbit filter: descending (assumed for geometric consistency — verify actual
  orbit coverage for this AOI/date range before running; ascending may be the
  only one available, or both may need separate handling)
- Backscatter coefficient: sigma0-ellipsoid (CDSE does not currently support
  gamma0-terrain for this collection, per community examples)
- Temporal reduction: median_time() per period
- Change metric: ratio of comparison median / baseline median (linear scale,
  not yet converted to dB — can be added with 10*log10(ratio) if desired)
- Output: GeoTIFF

## Known limitations / unknowns (unverified without live connection)
- Actual number and orbit direction of Sentinel-1 acquisitions over this AOI
  in these date windows is unknown until queried against the live backend.
- Approximate processing cost not yet estimated — depends on AOI pixel count
  at native resolution (no resampling applied in this version) times two
  periods times sar_backscatter cost.
- No cloud/water/urban masking applied — this is raw candidate change only.
- No thresholding or classification applied, per instruction.

## Traceability requirements (to log in a final run)
Collection ID, product IDs, acquisition timestamps (UTC), AOI, orbit property,
sar_backscatter settings, job ID, output download links, and credit cost
should all be recorded against this pilot in Polar-Sun-Moon-Analysis provenance
log before being treated as anything more than a preliminary signal.

## Python code (openEO Python client)

def sar_change_detection(connection):
    spatial_extent = {"west": 16.7, "south": 50.08, "east": 18.0, "north": 50.5}

    baseline_cube = connection.load_collection(
        "SENTINEL1_GRD",
        spatial_extent=spatial_extent,
        temporal_extent=["2024-08-25", "2024-09-09"],
        bands=["VV"],
        properties={"sat:orbit_state": lambda x: x == "descending"},
    )
    baseline_cube = baseline_cube.sar_backscatter(coefficient="sigma0-ellipsoid")
    baseline_median = baseline_cube.median_time()

    comparison_cube = connection.load_collection(
        "SENTINEL1_GRD",
        spatial_extent=spatial_extent,
        temporal_extent=["2024-09-14", "2024-09-22"],
        bands=["VV"],
        properties={"sat:orbit_state": lambda x: x == "descending"},
    )
    comparison_cube = comparison_cube.sar_backscatter(coefficient="sigma0-ellipsoid")
    comparison_median = comparison_cube.median_time()

    change_raster = comparison_median / baseline_median

    result = change_raster.save_result(format="GTiff")
    return result.to_json()

## Next step
Review this pilot. If approved, I will create and start the job
(create_and_start_job), then report job ID, status, cost estimate once
available, and download links on completion.
