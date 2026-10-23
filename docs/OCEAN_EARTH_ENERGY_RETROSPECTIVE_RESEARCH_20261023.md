# TerraObserver — Ocean & Earth Energy Retrospective Research (23 October 2026)

## Mission

**Observe the planet over time; help communities protect water, people and ecosystems; consider restoration only after the evidence and harm analysis are adequate.** The same water, atmospheric circulation, ocean currents and natural hazards cross national borders. This research prioritizes affordable public-good data, safer scientific instrumentation, community access, humanitarian needs and international collaboration. It does not claim that humanity can currently control tectonic earthquakes, global currents, hurricanes, tornadoes, clouds or the ocean.

The starting proposal is to investigate *weeks before an earthquake*, not only a single post-event image. Use archived observations to ask whether any changes in seawater level, ocean currents, seabed deformation, land elevation, wetland/runoff conditions or atmospheric conditions are measurable. Importantly, **a pre-event correlation is not proof of a precursor or a physical cause**.

## Precisely testable hypothesis register (initial; NOT findings)

H1. Multi-sensor measurements of pre-/post-event **surface displacement** may help characterize the geometry of an offshore tectonic event. Sentinel-1 InSAR interferograms can capture line-of-sight land displacement when repeated passes and phase coherence permit. InSAR is not a direct measurement of deep-ocean current speed or pressure.

H2. Some offshore earthquakes cause **vertical seafloor displacement**, displacing overlying water and potentially causing tsunamis; other earthquakes do not. Compare official USGS event magnitude, depth, fault geometry and NOAA tsunami records against sea-level gauges, DART bottom-pressure time series and appropriately sampled satellite altimetry. Do not treat ordinary sea-surface anomalies as an earthquake precursor.

H3. Surface current and temperature/sea-level anomalies may have seasonal, tidal, weather-driven, ENSO and long-term climate explanations. Compare candidate anomalies with appropriate ocean circulation models and unaffected matched control regions and event-free periods. Reject unsupported causal attribution.

H4. Long-term seafloor morphology and bathymetry can affect wave propagation, turbulence, currents and coastal flood exposure. Map ocean basins, ridges, underwater slopes and continental shelves using independently identified geophysical/bathymetric products. Large mid-ocean ridges and major mountains form over geological timescales through tectonics and other geological processes; **human extraction must not be assumed to have created them**. Human dredging, mining and coastal engineering may create local changes where established by specific evidence.

H5. Water restoration, floodplain reconnection, runoff management or protection of existing wetland systems might reduce *specific local harms* when carefully designed. Large-scale diversion of rivers, changing ocean circulation or deliberate geoengineering has substantial unquantified risks to downstream communities and ecosystems, and is **not authorized** by any AI recommendation.

All hypotheses begin as **HYPOTHESIS**. Publish null findings, missing coverage, statistical uncertainty and failed replications. No short-term deterministic earthquake predictions, hurricane control, dam/pump commands or claims to stop ocean currents.

## Event-centred retrospective study

For every independently sourced event, preserve the exact event **UTC** time, magnitude, depth, location, catalogue revision and product metadata; make explicit the instrument-specific sampling limitations.

| Window | Time relative to event | Scientific purpose |
| --- | --- | --- |
| Historical context | Same season in multiple earlier years (where data exist) | Seasonal baseline and controls |
| Baseline | Day -42 through -8 | Typical range, coverage, weather, tides |
| Close pre-event | Day -7 through -1 | Exploratory candidate changes; NOT prediction |
| Event interval | Event day and high-resolution in situ hours | Co-/immediate post-event dynamics |
| Early response | Day +1 through +7 | Tsunami, coastal flooding, shoreline and deformation effects |
| Recovery | Day +8 through +42 | Persistence, sediment, shoreline or ecosystem conditions |
| Long-term | Months, years and selected decadal data | Recovery/restoration trends; sensor harmonization needed |

Select exact product granularity per instrument. DART and tide gauges may be subhourly whereas a satellite may have no pass near the event. Never interpolate a nonexistent pass or label a years-old map as live.

### Data sources to combine (subject to coverage, licence and permissions)

- **USGS** Earthquake Hazards event catalog, tectonic context, official uncertainties, aftershock forecasts (NOT deterministic earthquake prediction).
- **Copernicus Sentinel-1 / openEO-CDSE** repeated SAR/InSAR for deformation and radar change when coherence and geometry permit; Sentinel-2 / Landsat for coastal surface changes with season/cloud masks.
- **NOAA DART / NCEI**, sea-level/tide gauges, NOAA wave/tsunami data and tsunami warning centres. DART is a physical *bottom-pressure sensor connected to a surface buoy*; it is not remotely reading the seabed from space.
- **Altimetry (Sentinel-6, SWOT, others)** for appropriate sea-surface-height/topography products, subject to swath/revisit/resolution and legitimate uncertainty; external ocean reanalysis models for current velocities. Surface imagery alone does not measure all subsurface currents.
- **GEBCO 2026, Seabed 2030, official bathymetry** for seabed geometry and resolution/provenance confidence. GEBCO's **28.7% (April 2026) mapped to modern standards** means roughly 71.3% not at that standard; it does not imply 71.3% entirely unobserved ocean, nor that the GEBCO global grid is empty elsewhere.
- **GNSS ground stations / tide gauges / field hydrology / seabed instruments** where available. Satellite signals cannot independently resolve all ocean depths, vertical profiles or deep tectonic mechanisms.

### Bias controls, calculations and reporting

1. Pre-register AOI and event selection criteria; include **negative-control intervals** and nearby regions with no comparable event. Hold back events to avoid training/evaluation leakage and test false-positive rate.
2. Align instruments to UTC, common geodetic vertical datum, tide/wind/weather phase, similar seasons, spatial resolution and known errors. Never directly compare SAR backscatter ratios to wave height.
3. Treat 3D ocean current velocity, water levels, pressures and kinetic/potential energy as *different physical quantities with units and conservation constraints*; do not infer flow or stored energy from RGB pixels. Integrate uncertainty and error propagation.
4. Use the existing TerraObserver AOI planner before paid jobs; tile oceans/continents, estimate pixels and acquisition counts, check actual provider dataset availability and price. Set external budget, early OOM stop, retry idempotency and real provider receipt.
5. Link raw product/version IDs, acquisition time, retrieval time, orbit, SAR geometry, processing graph, transformations, code commit, cryptographic hashes, units, spatial validity mask, confidence interval and reviewer. Distinguish **OBSERVED, DERIVED, MODEL_ESTIMATE, HYPOTHESIS, UNKNOWN, CONFIRMED**.
6. Publish both reproducible visualizations and machine-readable evidence. AI may classify uncertainties, generate competing hypotheses and speed up triage but must not invent observed values or claim causal discovery from correlation.
7. Separate *research* from *intervention*: require hydrologists, oceanographers, seismologists, ecologists, affected communities, regulators, environmental-impact assessment and downstream/transboundary harm review before any field actuation or large-scale ecosystem intervention.
8. Never autonomously modify water infrastructure or perform weather/geoengineering control; an owner saying "restore" does not override scientific, legal and community safeguards.

## Public-good research priorities

- Revisit poorly surveyed seafloor with oceanographic ships, sonar, autonomous underwater vehicles, buoys, tide gauges and remote sensors, prioritizing equitable international data access and ecosystem conservation.
- Establish a reproducible baseline for rivers, drinking-water resources, floodplains, wetlands, coasts and ocean energy exchanges. Investigate how changes in water distribution affect vulnerable populations.
- Design **risk-reduction** and evidence-led restoration proposals that do not displace harm to communities who did not consent, including future generations.
- Encourage investment in research, resilience and ocean observation as a peaceful cross-border common good. This is a mission/value statement, not proof of technical ability to manipulate planetary systems.

## First bounded research deliverable

Choose ONE documented offshore earthquake with public DART/tide-gauge coverage. Retrieve a manageable event list and metadata, prepare **six-week before/after windows** and matched seasonal controls, inventory sources/units and actual availability, then submit **at most one approved small openEO batch** after cost/coverage preflight. Report coverage gaps honestly. Publish evidence/uncertainty and an accessible 3D Earth view; do not present it as a prediction or an automated ocean-control system.

## Authoritative reference starting points (URLs for reproducibility)

- USGS earthquake prediction limits: https://www.usgs.gov/faqs/can-you-predict-earthquakes
- USGS operational earthquake forecasting overview: https://www.usgs.gov/publications/developing-testing-and-communicating-earthquake-forecasts-current-practices-and-future
- ESA Sentinel-1 interferometry explanation: https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1/10_ways_Sentinel-1_data_lets_us_see_our_world
- NOAA tsunami mechanisms: https://www.noaa.gov/jetstream/tsunamis/tsunami-generation-earthquakes
- NOAA DART measurements: https://www.ndbc.noaa.gov/dart/system.shtml
- NOAA historic DART data: https://www.ncei.noaa.gov/products/natural-hazards/tsunamis-earthquakes-volcanoes/tsunamis/dart-ocean-bottom-pressure
- GEBCO 2026 28.7% coverage: https://www.gebco.net/news/release-gebco2026-grid
