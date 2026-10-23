# CODEX task — evidence-first openEO TerraObserver pilot and virtual Earth (23 October 2026)

## Objective
Extend this NEW documentation-only integration repository without rebuilding the already functioning Terra Observation System in `Terraforming-Planet/Polar-Sun-Moon-Analysis`. The future TerraObserver is a supervised **scheduled** environmental research service with a detailed 3D Earth dashboard; it is NOT a live world-wide satellite camera, not ESA-certified, not a hazard prediction authority, and not an autonomous dam/river controller.

## First source milestone (this branch)
Implement and locally test `terraobserver/safety.py`, `tests/test_safety.py` and a credential-free PR workflow. It calculates conservative bbox geodesic bounds, validates explicit dates and band/acquisition-count assumptions, enforces AOI-dependent resolution, hard 50M *estimated* pixels per tile and bounded tiling. Return `DRY_RUN_ONLY`; no OIDC access, provider create/start job or charges. Do not turn a green mock test into a claim of real observation. This specifically addresses `docs/VALIDATION_RULES.md` following Incident #1, where a too-large Sahara operation OOM'd and consumed 76 credits.

## Second milestone, gated by real account access
1. Reuse `Polar-Sun-Moon-Analysis/scripts/cdse/run_flood_detection.py` instead of copying scientific algorithms by memory. Discover collection IDs, bands, orbit directions, temporal availability and backend capabilities from authenticated CDSE openEO APIs before submitting. Verify actual platform policy and cost quote.
2. Pilot AOI from `terra_observer_s1_pilot.md` in southern Poland: compare 2024-08-25…09-09 with 2024-09-14…09-22 using VV Sentinel-1 backscatter after verifying acquisition coverage, orbit and units. Check ratio numerator/denominator and masks, preserve source product IDs, job ID, processing graph, actual output GeoTIFF with hash, measured credit usage and errors.
3. Use a permanent queue **only after** safe idempotent claim/submit/status recovery, explicit spend and concurrency caps, result hashes, job timeout and interruption handling are tested. Across geography, tile sufficiently to avoid executor OOM. Provider expenses must not be incurred from a PR or a vague cron schedule.
4. Keep observation evidence labels: OBSERVED, DERIVED, MODEL_ESTIMATE, HYPOTHESIS, UNKNOWN, CONFIRMED. Surface source and acquisition UTC, publication UTC, processing delay, sensor limitations and uncertainty; never call old imagery "live".
5. Integrate existing Terra 3D globe and environmental layers for water, rivers, wetlands, glacier, drought, storm and forest research with mobile-safe rendering. Six thematic spheres/lenses may be an interactive visualization metaphor; preserve accurate Earth geography and verified measurements. Event-specific safety alerts are human-reviewed.
6. Provide real reproducible source/test/CI evidence, bounded API cost and provider output before claiming "24/7 TerraObserver online". Crosslink WORLDIFACT 3D only at the UI/data contract boundary; R2 customer models are NOT openEO satellite measurements.

## Required tests
- Continent-sized AOI at 100m rejects **before** create_job/start_job.
- Small valid AOI dry-run returns finite computed costs (pixels only; actual provider credits UNKNOWN).
- Date and acquisition count validation, bounds/NaN/antimeridian behavior, tile cap, no-data, duplicate-job and budget halt.
- Authentication and runtime secrets remain server-side, never in GitHub docs/logs or the browser.
- One real completed pilot with fully checked source metadata, GeoTIFF checksum and provenance before production merge/marketing.

## Current state
The safety planner and offline CI are real source and tests, not a running openEO scheduler. Worldwide monitoring and full 3D product remain staged roadmap tasks. No uncontrolled paid jobs or "silent" ESA connection.
