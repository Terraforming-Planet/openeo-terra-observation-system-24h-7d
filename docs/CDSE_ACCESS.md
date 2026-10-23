# CDSE access and fork verification

Verified on 2026-10-23. This is an integration audit, not a satellite observation,
completed processing job, coverage check or provider cost quote.

## Reusable public API audit

From this repository, with Python 3.10 or newer:

```sh
python -B -m unittest discover -s tests -p 'test_*.py' -v
python -B -m terraobserver.cdse --output /tmp/cdse-audit-unique-run
```

Choose a new output directory for each run. The command records public metadata,
SHA-256 hashes, validation results and a UTC timestamp. It returns a nonzero exit
status for an incomplete audit. No extra dependency or account is required.
Only fixed metadata endpoints and `POST /validation` are accessible through
this helper; it cannot submit jobs or call the synchronous processing endpoint.
Provider error bodies and signed links are not printed. Output snapshots should
remain outside the source checkout.

CDSE discovery at `https://openeo.dataspace.copernicus.eu/.well-known/openeo`
advertises production API 1.2 at
`https://openeo.dataspace.copernicus.eu/openeo/1.2/`. The host root serves a web
application; appending `/collections` or `/validation` there gives the wrong
route. API 1.3 is advertised as non-production. The helper pins the verified
production endpoint; recheck discovery before changing it.

The official Python client also resolves discovery:

```python
import openeo
connection = openeo.connect("https://openeo.dataspace.copernicus.eu/")
dem_metadata = connection.describe_collection("COPERNICUS_30")
```

## Evidence from the live backend

- 146 advertised processes and 138 catalogue collections.
- `COPERNICUS_30` exposes band `DEM`.
- `SENTINEL1_GRD` exposes `VV` and `sat:orbit_state` values ascending/descending.
- `slope`, `sar_backscatter`, `run_udf`, resampling and spatial/temporal
  aggregation are advertised. Remote user-defined processes depend on the
  backend and their particular implementation; a catalogue entry alone does
  not establish compatibility or task suitability.
- DEM slope and Sentinel-2 NDWI example graphs passed `POST /validation` with
  zero errors. They were not executed. The explicit 2025-06-01 to 2025-06-02
  NDWI interval is a historical API fixture, not a current-monitoring request.
  Cloud masking and a science-specific acquisition review remain necessary.
- No job-estimation endpoint was advertised in the inspected capabilities.
  Do not invent a total credit estimate from metadata or fixed job overhead.

openEO is extensible; it is incorrect to claim that it can *only* download raw
data or can never execute a hydrological algorithm. A suitable UDF/UDP or a
backend extension may implement one. Test 02 nevertheless remains limited to
terrain observations and visualizations; no hydrological routing was performed.

## Authentication and network status

The CDSE provider advertises device-code with PKCE for headless login. Public
metadata access succeeded. This does not prove authenticated account access.
The latest device-login attempt ended with `OidcException` without delivering
an authenticated session. Login must be completed interactively again when
reading private job metadata. Do not reuse an expired device code, log tokens
or assume that a process-memory token survives a new execution.

Approved HTTPS/443 hosts already include `openeo.dataspace.copernicus.eu`,
`identity.dataspace.copernicus.eu`, `catalogue.dataspace.copernicus.eu`,
`s3.waw3-1.openeo.v1.dataspace.copernicus.eu` and `api.github.com`. API reads and
the result-host connection now work. A result-host root response is not proof
that private asset downloads work. `stac.dataspace.copernicus.eu` remains
unapproved. No additional domain was enabled for this audit. A bare 403 status
cannot, on its own, distinguish proxy policy from API authorization.

## Fork setup and checks

| Fork | Source commit | Check |
| --- | --- | --- |
| openeo-python-client | `43d53d6c44f617f4e70b803fcd4c4eba29d107c6` | 468 selected capability/connection/OIDC tests passed; 2 warnings |
| openeo-api | `1881dae18b3c2c417f1305774cf295c81d60d400` | Specification lint and documentation build passed; lint warnings retained |
| openeo.org | `37f86e17d5c8b9255e50f92cb7c603a19989f5a9` | Website build passed after submodule initialization and supported Node proxy configuration |

The Python fork is installed separately in `/workspace/openeo-fork-venv`
with `pip install -e '.[tests]'`. Stable 0.53.0 remains in
`/workspace/terra-observer-venv`. Selected tests:

```sh
/workspace/openeo-fork-venv/bin/python -m pytest tests/rest/test_capabilities.py tests/rest/test_connection.py tests/rest/auth/test_oidc.py -q
```

API fork setup uses `npm install --package-lock=false`, because this revision
has no lockfile, followed by `npm test` and `npm run build`. Website setup:

```sh
git submodule update --init --recursive
npm ci --ignore-scripts
NODE_USE_ENV_PROXY=1 npm test
```

Verified with Node 24.19.0. Without Node's supported proxy option, the website's
HTTPS download fails in this environment and its error handler triggers
`fs.unlink` without a callback. With the correct proxy configuration, downloads
and the complete VitePress build succeed. Fork source files were not modified.
The `openeo-api` repository is a specification, not a deployed processing server.
Forking these projects grants source control, not additional CDSE account rights
or compute credits.
