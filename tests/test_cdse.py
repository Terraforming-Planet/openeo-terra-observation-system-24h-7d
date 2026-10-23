"""Offline tests: no account, network, jobs or charges."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

from terraobserver.cdse import DiagnosticError, NoRedirect, audit, request_json, validate_graph


class CdseAuditTests(unittest.TestCase):
    def test_validation_uses_versioned_production_api(self):
        with patch("urllib.request.build_opener") as opener:
            opener.return_value.open.return_value.__enter__.return_value.read.return_value = b'{"errors": []}'
            self.assertTrue(validate_graph({"process_graph": {}})["valid"])
            request = opener.return_value.open.call_args.args[0]
            self.assertEqual(request.full_url, "https://openeo.dataspace.copernicus.eu/openeo/1.2/validation")
            self.assertEqual(request.get_method(), "POST")

    def test_processing_routes_refused_before_network(self):
        with patch("urllib.request.build_opener") as opener:
            for path, payload in [("/jobs", {}), ("/result", {}), ("/jobs/j-123/results", {}),
                                  ("/jobs", None), ("https://example.org/", None)]:
                with self.assertRaisesRegex(DiagnosticError, "ENDPOINT_NOT_ALLOWED"):
                    request_json(path, payload)
            opener.assert_not_called()

    def test_no_cross_host_redirect(self):
        with self.assertRaisesRegex(DiagnosticError, "REDIRECT_REFUSED"):
            NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.org/private")

    def test_http_error_does_not_disclose_provider_body_or_url(self):
        error = urllib.error.HTTPError("https://private.example/?secret=hidden", 403,
                                      "hidden", {}, io.BytesIO(b"hidden"))
        with patch("urllib.request.build_opener") as opener:
            opener.return_value.open.side_effect = error
            with self.assertRaises(DiagnosticError) as caught:
                request_json("/")
            self.assertEqual(str(caught.exception), "HTTP_403")

    def test_validation_requires_explicit_errors_array(self):
        with self.assertRaises(DiagnosticError):
            validate_graph({}, lambda *_: {"unexpected": True})
        self.assertFalse(validate_graph({}, lambda *_: {"errors": [{"message": "hidden"}]})["valid"])
        self.assertTrue(validate_graph({}, lambda *_: {"errors": []})["valid"])

    def test_oversized_metadata_refused(self):
        with patch("terraobserver.cdse.MAX_RESPONSE_BYTES", 4), patch("urllib.request.build_opener") as opener:
            opener.return_value.open.return_value.__enter__.return_value.read.return_value = b"12345"
            with self.assertRaisesRegex(DiagnosticError, "RESPONSE_SIZE_LIMIT"):
                request_json("/")

    def test_partial_audit_is_not_reported_as_complete_and_cannot_overwrite(self):
        def fake(path, payload=None):
            if path == "/collections/COPERNICUS_30":
                raise DiagnosticError("HTTP_503")
            if payload is not None:
                return {"errors": []}
            return {}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "audit"
            report = audit(output, fake)
            self.assertFalse(report["complete"])
            self.assertEqual(report["new_jobs"], 0)
            self.assertEqual(len(report["validation"]), 2)
            self.assertFalse(report["observations_downloaded"])
            self.assertEqual(json.loads((output / "report.json").read_text()), report)
            with self.assertRaises(FileExistsError):
                audit(output, fake)


if __name__ == "__main__":
    unittest.main()
