"""Read-only AOI tiling and openEO job-size admission. No API calls or billing.

Estimates are planning bounds, NOT satellite acquisitions, observations, provider
quotes or permissions to submit. Cloud/ocean/polar artifacts need separate QA.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from math import ceil, cos, isfinite, radians

EARTH_KM_PER_DEGREE = 111.32
PIXEL_LIMIT_PER_JOB = 50_000_000
MAX_TILES = 25_000


class Refused(ValueError):
    """No provider request should be submitted for this unsafe plan."""


@dataclass(frozen=True)
class BBox:
    west: float
    south: float
    east: float
    north: float

    def validate(self) -> None:
        values = (self.west, self.south, self.east, self.north)
        if any(type(v) not in (float, int) or not isfinite(v) for v in values):
            raise Refused("INVALID_BBOX_NUMBERS")
        if not (-180 <= self.west < self.east <= 180 and
                -85 <= self.south < self.north <= 85):
            raise Refused("INVALID_BBOX_OR_POLAR_EXTENT")


def dimensions_km(aoi: BBox) -> tuple[float, float]:
    aoi.validate()
    # For latitude ranges that include the equator, use a conservative maximum
    # longitudinal width. No area is inferred from a Web Mercator projection.
    near_equator = min(abs(aoi.south), abs(aoi.north))
    if aoi.south <= 0 <= aoi.north:
        near_equator = 0
    return ((aoi.east - aoi.west) * EARTH_KM_PER_DEGREE * cos(radians(near_equator)),
            (aoi.north - aoi.south) * EARTH_KM_PER_DEGREE)


def minimum_resolution_m(aoi: BBox) -> int:
    side = max(dimensions_km(aoi))
    if side < 100:
        return 10
    if side < 500:
        return 50
    if side < 2000:
        return 250
    return 1000


def estimated_pixels(aoi: BBox, resolution_m: int, bands: int, acquisitions: int) -> int:
    if any(type(v) is not int or v <= 0 for v in (resolution_m, bands, acquisitions)):
        raise Refused("INVALID_RESOLUTION_BANDS_OR_ACQUISITIONS")
    if bands > 20 or acquisitions > 365:
        raise Refused("UNBOUNDED_BANDS_OR_ACQUISITIONS")
    width_km, height_km = dimensions_km(aoi)
    return ceil(width_km * 1000 / resolution_m) * ceil(height_km * 1000 / resolution_m) * bands * acquisitions


def _date(value: str) -> date:
    if type(value) is not str or len(value) != 10:
        raise Refused("INVALID_EXPLICIT_DATE")
    try:
        result = date.fromisoformat(value)
    except ValueError:
        raise Refused("INVALID_EXPLICIT_DATE") from None
    if result.isoformat() != value:
        raise Refused("INVALID_EXPLICIT_DATE")
    return result


def plan_tiles(aoi: BBox, *, start: str, end: str, resolution_m: int,
               bands: int, acquisitions_per_tile: int, max_tiles: int = MAX_TILES) -> dict:
    """Return deterministic, never-executable research tiles for human review.

    'acquisitions_per_tile' is an assumed upper-bound planning value: official
    catalogue metadata must replace it before any billed submission.
    """
    aoi.validate()
    start_day, end_day = _date(start), _date(end)
    if end_day <= start_day or (end_day - start_day).days > 366:
        raise Refused("INVALID_OR_UNBOUNDED_TIME_RANGE")
    if type(max_tiles) is not int or not 1 <= max_tiles <= MAX_TILES:
        raise Refused("INVALID_TILE_LIMIT")
    if type(resolution_m) is not int or resolution_m < minimum_resolution_m(aoi):
        raise Refused("RESOLUTION_TOO_FINE_FOR_AOI")
    estimated_pixels(aoi, resolution_m, bands, acquisitions_per_tile)
    # Maximum tile side 2 degrees. Further bisect any tile whose *estimated*
    # image volume exceeds the limit. No cluster or backend access occurs here.
    nx = ceil((aoi.east - aoi.west) / 2)
    ny = ceil((aoi.north - aoi.south) / 2)
    if nx * ny > max_tiles:
        raise Refused("TILE_COUNT_EXCEEDS_BUDGET")
    stack = []
    for ix in range(nx):
        west = aoi.west + (aoi.east - aoi.west) * ix / nx
        east = aoi.west + (aoi.east - aoi.west) * (ix + 1) / nx
        for iy in range(ny):
            south = aoi.south + (aoi.north - aoi.south) * iy / ny
            north = aoi.south + (aoi.north - aoi.south) * (iy + 1) / ny
            stack.append(BBox(west, south, east, north))
    tiles = []
    while stack:
        box = stack.pop()
        pixels = estimated_pixels(box, resolution_m, bands, acquisitions_per_tile)
        if pixels <= PIXEL_LIMIT_PER_JOB:
            tiles.append({**box.__dict__, "estimatedPixels": pixels})
        else:
            if len(stack) + len(tiles) + 2 > max_tiles:
                raise Refused("TILE_COUNT_EXCEEDS_BUDGET")
            width, height = dimensions_km(box)
            if width >= height:
                mid = (box.west + box.east) / 2
                stack.extend([BBox(box.west, box.south, mid, box.north), BBox(mid, box.south, box.east, box.north)])
            else:
                mid = (box.south + box.north) / 2
                stack.extend([BBox(box.west, box.south, box.east, mid), BBox(box.west, mid, box.east, box.north)])
    if len(tiles) > max_tiles:
        raise Refused("TILE_COUNT_EXCEEDS_BUDGET")
    tiles.sort(key=lambda t: (t["south"], t["west"], t["north"], t["east"]))
    return {
        "revision": "terraobserver-evidence-plan-v1",
        "status": "DRY_RUN_ONLY",
        "maySubmitToProvider": False,
        "reason": "BACKEND_COLLECTION_ORBIT_COST_AND_HUMAN_APPROVAL_REQUIRED",
        "acquisitionsAreEstimated": True,
        "evidenceClass": "HYPOTHESIS",
        "timeRangeUTC": [start, end],
        "resolutionMeters": resolution_m,
        "numberOfTiles": len(tiles),
        "estimatedTotalPixels": sum(x["estimatedPixels"] for x in tiles),
        "tiles": tiles,
    }
