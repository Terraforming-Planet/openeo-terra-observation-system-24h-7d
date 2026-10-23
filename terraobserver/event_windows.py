"""Timestamp-based seismic/ocean retrospective windows. NO data fetch or prediction.

UTC event reference is externally verified before use. Windows are sampling
requests, not proof that a satellite or seabed sensor observed these dates.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone


def research_windows(event_utc: str) -> dict:
    if type(event_utc) is not str or len(event_utc) != 20 or not event_utc.endswith("Z"):
        raise ValueError("UTC_EVENT_TIME_REQUIRED")
    try:
        when = datetime.strptime(event_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError("UTC_EVENT_TIME_INVALID") from None
    if when.year < 2014 or when.year > 2100:
        raise ValueError("EVENT_OUTSIDE_RESEARCH_SCOPE")
    date = when.date()

    def period(start: int, end: int) -> dict:
        a, b = date + timedelta(days=start), date + timedelta(days=end)
        return {"startUTC": a.isoformat(), "endUTC": b.isoformat(),
                "availability": "NOT_QUERIED", "hasMeasurements": False}

    return {
        "revision": "terraobserver-event-centred-retrospective-v1",
        "eventTimeUTC": event_utc,
        "status": "PLAN_ONLY",
        "earthquakePrediction": False,
        "causalityEstablished": False,
        "interventionAuthorized": False,
        "windows": {
            "baseline": period(-42, -8),
            "closePreEvent": period(-7, -1),
            "eventDay": period(0, 0),
            "earlyResponse": period(1, 7),
            "recovery": period(8, 42),
        },
        "requirements": [
            "INDEPENDENT_VERIFIED_EVENT_CATALOG",
            "SOURCE_ACQUISITION_AVAILABILITY_AND_UTC",
            "TIDES_WIND_AND_SEASONAL_CONTROLS",
            "MATCHED_EVENT_FREE_REGIONS_AND_DATES",
            "GNSS_SAR_ALTIMETRY_DART_UNITS_NOT_INTERCHANGEABLE",
            "EXPLICIT_COST_AND_HUMAN_APPROVAL_BEFORE_BATCH",
        ],
    }
