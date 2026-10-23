"""No network, no provider charges: regression fixtures for planned openEO jobs."""
import unittest
from terraobserver.safety import BBox, Refused, dimensions_km, estimated_pixels, minimum_resolution_m, plan_tiles, PIXEL_LIMIT_PER_JOB


class PlanSafetyTests(unittest.TestCase):
    def test_small_aoi_dry_run_is_not_an_execution(self):
        result = plan_tiles(BBox(18.8, 50.0, 18.82, 50.02), start="2024-09-14",
                            end="2024-09-22", resolution_m=10, bands=1,
                            acquisitions_per_tile=4)
        self.assertEqual(result["status"], "DRY_RUN_ONLY")
        self.assertFalse(result["maySubmitToProvider"])
        self.assertEqual(result["numberOfTiles"], 1)
        self.assertGreater(result["estimatedTotalPixels"], 0)
        self.assertEqual(result["timeRangeUTC"], ["2024-09-14", "2024-09-22"])

    def test_sahara_at_100m_refused_before_provider_dispatch(self):
        sahara = BBox(-16, 15, 36, 33)
        self.assertEqual(minimum_resolution_m(sahara), 1000)
        with self.assertRaisesRegex(Refused, "RESOLUTION_TOO_FINE_FOR_AOI"):
            plan_tiles(sahara, start="2024-06-01", end="2024-06-05",
                       resolution_m=100, bands=2, acquisitions_per_tile=10)

    def test_large_region_tiles_obey_hard_pixel_ceiling(self):
        aoi = BBox(16, 48, 19, 52)
        plan = plan_tiles(aoi, start="2024-09-01", end="2024-09-25",
                          resolution_m=250, bands=2, acquisitions_per_tile=10)
        self.assertGreater(plan["numberOfTiles"], 1)
        self.assertTrue(all(p["estimatedPixels"] <= PIXEL_LIMIT_PER_JOB for p in plan["tiles"]))
        self.assertGreater(plan["estimatedTotalPixels"], 0)

    def test_fine_resolution_date_and_geometry_refuse(self):
        for box in [BBox(-181, 0, 1, 1), BBox(1, 0, 1, 1), BBox(0, -86, 1, 0),
                    BBox(float("nan"), 0, 1, 1)]:
            with self.assertRaises(Refused):
                box.validate()
        for start,end in [("today","2024-09-22"), ("2024-09-01","2024-09-01"),
                          ("2024-09-10","2024-09-01"), ("2024-01-01","2025-06-01")]:
            with self.assertRaises(Refused):
                plan_tiles(BBox(18, 50, 18.1, 50.1), start=start, end=end,
                           resolution_m=10, bands=1, acquisitions_per_tile=1)

    def test_cost_and_acquisition_estimates_cannot_be_faked(self):
        box = BBox(16, 50, 16.1, 50.1)
        self.assertGreater(dimensions_km(box)[0], 0)
        for item in [0, -1, 1.5, True, 366]:
            with self.assertRaises(Refused):
                estimated_pixels(box, 10, 2, item)
        for count in [0, 21, False]:
            with self.assertRaises(Refused):
                estimated_pixels(box, 10, count, 1)
        with self.assertRaisesRegex(Refused, "TILE_COUNT_EXCEEDS_BUDGET"):
            plan_tiles(BBox(16, 50, 19, 53), start="2024-01-01", end="2024-01-10",
                       resolution_m=250, bands=1, acquisitions_per_tile=1,
                       max_tiles=1)

    def test_original_open_eo_pilot_requires_orbit_and_cost_review(self):
        p=plan_tiles(BBox(16.7,50.08,18.0,50.5),start="2024-08-25",end="2024-09-09",
                     resolution_m=250,bands=1,acquisitions_per_tile=10)
        self.assertIn("APPROVAL",p["reason"])
        self.assertTrue(p["acquisitionsAreEstimated"])



from terraobserver.event_windows import research_windows


class EarthOceanRetrospectiveWindowTests(unittest.TestCase):
    def test_6_week_event_windows_are_dry_run_only(self):
        v=research_windows("2024-09-16T06:24:00Z")
        self.assertEqual(v["status"], "PLAN_ONLY")
        self.assertFalse(v["earthquakePrediction"])
        self.assertFalse(v["causalityEstablished"])
        self.assertFalse(v["interventionAuthorized"])
        self.assertEqual(v["windows"]["baseline"],
                         {"startUTC": "2024-08-05", "endUTC": "2024-09-08",
                          "availability": "NOT_QUERIED", "hasMeasurements": False})
        self.assertEqual(v["windows"]["closePreEvent"]["endUTC"], "2024-09-15")
        self.assertEqual(v["windows"]["recovery"]["endUTC"], "2024-10-28")
        self.assertTrue(all(not entry["hasMeasurements"] for entry in v["windows"].values()))

    def test_year_boundary_and_leap_day(self):
        v=research_windows("2024-01-02T01:03:59Z")
        self.assertEqual(v["windows"]["baseline"]["startUTC"], "2023-11-21")
        self.assertEqual(v["windows"]["recovery"]["endUTC"], "2024-02-13")
        leap=research_windows("2024-02-29T00:00:00Z")
        self.assertEqual(leap["windows"]["closePreEvent"]["endUTC"],"2024-02-28")

    def test_strict_utc_no_fabricated_event_time_or_prediction(self):
        for event in ("2026-10-22", "today", "2024-02-30T00:00:00Z",
                      "2024-09-16T06:24:00+02:00", "2024-09-16T06:24:00",
                      "2012-04-12T00:00:00Z", "not-a-time"):
            with self.assertRaises(ValueError):
                research_windows(event)


if __name__ == "__main__":
    unittest.main()
