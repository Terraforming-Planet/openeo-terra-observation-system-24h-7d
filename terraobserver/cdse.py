"""Public CDSE metadata and graph validation; never submits processing jobs.

Run: python -m terraobserver.cdse --output /path/to/new-audit
Only standard-library modules are required. No credentials are read or stored.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

# Production API 1.2, verified via /.well-known/openeo on 2026-10-23.
# The host root serves the web application, not the API. 1.3 is non-production.
BASE_URL = "https://openeo.dataspace.copernicus.eu/openeo/1.2"
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
GET_PATHS = frozenset({
    "/", "/processes", "/collections", "/credentials/oidc", "/file_formats",
    "/udf_runtimes", "/processing_parameters", "/collections/COPERNICUS_30",
    "/collections/SENTINEL1_GRD", "/collections/SENTINEL2_L2A",
})


class DiagnosticError(RuntimeError):
    """Sanitized error: never includes response bodies, credentials or URLs."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise DiagnosticError("REDIRECT_REFUSED")


def request_json(path: str, payload: dict | None = None) -> dict:
    if (payload is None and path not in GET_PATHS) or (payload is not None and path != "/validation"):
        raise DiagnosticError("ENDPOINT_NOT_ALLOWED")
    data = None if payload is None else json.dumps(payload, allow_nan=False).encode()
    request = urllib.request.Request(BASE_URL + path, data=data, headers={
        "Accept": "application/json", "Content-Type": "application/json",
        "User-Agent": "TerraObserver-Metadata-Audit/1.0",
    })
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise DiagnosticError("RESPONSE_SIZE_LIMIT")
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise DiagnosticError("INVALID_JSON_OBJECT")
        return value
    except urllib.error.HTTPError as error:
        # A 403 by itself cannot identify a proxy versus API authorization error.
        raise DiagnosticError(f"HTTP_{error.code}") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise DiagnosticError("NETWORK_ERROR") from None
    except (ValueError, UnicodeError):
        raise DiagnosticError("INVALID_JSON") from None


def validate_graph(graph: dict, transport=request_json) -> dict:
    result = transport("/validation", graph)
    errors = result.get("errors")
    if not isinstance(errors, list):
        raise DiagnosticError("VALIDATION_RESPONSE_MISSING_ERRORS")
    # Do not reproduce provider message text; arbitrary graphs may contain URLs.
    return {"valid": not errors, "error_count": len(errors), "executed": False}


def band_names(metadata: dict) -> list[str]:
    dimensions = metadata.get("cube:dimensions", {})
    return [name for dimension in dimensions.values() if dimension.get("type") == "bands"
            for name in dimension.get("values", []) if isinstance(name, str)]


def audit(output: Path, transport=request_json) -> dict:
    # Each snapshot is immutable; never silently mix results from different runs.
    output.mkdir(parents=True, exist_ok=False)
    report = {"backend": BASE_URL, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "new_jobs": 0, "authenticated": False, "observations_downloaded": False,
              "metadata": {}, "validation": {}}
    for path in sorted(GET_PATHS):
        name = path.strip("/").replace("/", "-") or "capabilities"
        try:
            value = transport(path)
            encoded = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
            (output / (name + ".json")).write_bytes(encoded)
            summary = {"status": "OK", "sha256": hashlib.sha256(encoded).hexdigest()}
            if path == "/processes":
                summary["count"] = len(value.get("processes", []))
            if path == "/collections":
                summary["count"] = len(value.get("collections", []))
            if path.startswith("/collections/"):
                summary["bands"] = band_names(value)
                summary["orbit_states"] = value.get("summaries", {}).get("sat:orbit_state", [])
            report["metadata"][name] = summary
        except DiagnosticError as error:
            report["metadata"][name] = {"status": str(error)}
    examples = Path(__file__).resolve().parent.parent / "examples" / "cdse"
    for path in sorted(examples.glob("*-graph.json")):
        graph = json.loads(path.read_text())
        (output / path.name).write_text(json.dumps(graph, indent=2) + "\n")
        try:
            report["validation"][path.stem] = validate_graph(graph, transport)
        except DiagnosticError as error:
            report["validation"][path.stem] = {"status": str(error), "executed": False}
    report["complete"] = (len(report["validation"]) == 2
                          and all(v["status"] == "OK" for v in report["metadata"].values())
                          and all(v.get("valid") for v in report["validation"].values()))
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = audit(args.output)
    except (OSError, ValueError):
        print(json.dumps({"status": "LOCAL_INPUT_OR_OUTPUT_ERROR"}))
        return 1
    print(json.dumps(report, indent=2))
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
