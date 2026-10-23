# TerraObserver — openEO Terra Observation System 24/7

**Earth-observation intelligence for protecting water, ecosystems, land and communities.**

TerraObserver is a Terraforming Planet research initiative to connect **openEO, Copernicus satellite data, reproducible geospatial analysis, and responsibly supervised AI agents** into an evidence-first environmental observation system. Its long-term goal is to help people discover meaningful environmental changes, assess potential threats, understand uncertainty, and investigate responsible ways to restore damaged ecosystems.

**Mission:** observe → measure → verify → explain → prioritize → support human-led restoration.

> **Project status — 22 October 2026:** This repository is an **early-stage integration and documentation hub**, not yet a deployed 24/7 processing service. The functioning research code, publicly documented experiments, and preliminary monitoring workflows referenced below live in linked Terraforming Planet repositories. Integrating, validating, and operating them as one reliable service is the work of this project. No ESA endorsement or affiliation is claimed.

## Why this project exists

Rivers change course, lakes and wetlands shrink or expand, forests experience stress, glaciers retreat, coastlines evolve, and extreme events threaten lives and infrastructure. Satellite archives contain valuable evidence, but turning that evidence into reproducible measurements and practical decisions is difficult.

TerraObserver aims to make this process accessible to researchers, local communities, NGOs, educators, water managers, and environmental protection teams. Rather than asking AI to guess what a satellite image means, the system is designed to collect traceable observations, compare relevant periods and sensors, quantify defensible indicators, and identify what still needs independent investigation.

The long-term ambition is **environmental recovery**, not observation for its own sake: better information about water balance, floodplains, drylands, vegetation, wetlands, glaciers and river connectivity can support carefully assessed restoration or adaptation projects.

## What “24/7” means — and does not mean

The intended service will be capable of **scheduled, event-triggered and continuously supervised workflow orchestration**, subject to data availability, infrastructure, cost limits and provider permissions.

It **does not** mean that every location has an uninterrupted high-resolution live satellite video feed. Optical and radar acquisitions depend on satellite orbits, revisit intervals, weather and cloud conditions, acquisition scheduling, publication delays and licences.

Every displayed product should show its **actual acquisition time**, **publication/retrieval time**, source and processing status. A frequently refreshing dashboard must never describe old imagery as a live observation. The service should report **NO_DATA**, **DELAYED**, **INCOMPLETE** or **INSUFFICIENT_EVIDENCE** when appropriate.

## Research priorities

- **Water security:** rivers, lakes, ponds, reservoirs, wetlands, surface-water extent, shoreline movement and connectivity between water bodies.
- **Floods and drought:** change indicators, seasonal context, exposed riverbeds, floodplain dynamics, hydrological evidence and historical comparisons.
- **Forests and land:** vegetation change, wildfire context, land-cover disturbance, erosion, soil-moisture indicators and ecosystem stress.
- **Cryosphere and polar regions:** glaciers, snow, ice and associated changes in regional water systems.
- **Drylands and restoration research:** former watercourses and paleochannels, desert hydrology, retention possibilities and constraints on ecological interventions.
- **Coastal and ocean environments:** coastline and wetland changes, estuaries and relevant public oceanographic context.
- **Hazards and community resilience:** investigate official event feeds and post-event impacts; support professional verification and human decision-making.

The project does **not** claim to predict the exact place and time of earthquakes, infer the cause of a change from imagery alone, or autonomously operate dams, sluices, pumps, channels or emergency infrastructure.

## Scientific data and processing

| Source / technology | Intended use | Essential limitation |
| --- | --- | --- |
| **Copernicus Data Space / openEO** | Bounded, reproducible processing of EO collections, including Sentinel-1 radar and suitable optical datasets | Coverage, permissions, collection availability and processing must be checked |
| **Sentinel-1 SAR** | Radar backscatter and water/flood-change candidates, including cloudy and nighttime conditions | Backscatter is not direct water depth; geometry, vegetation and surface conditions matter |
| **Sentinel-2 MSI** | Multispectral land, vegetation and surface-water mapping | Cloud/shadow masks, seasonal matching and band-dependent resolution are necessary |
| **USGS/NASA Landsat** | Long-term historical comparisons of land and water | Different generations of sensors and acquisition conditions must be harmonized |
| **NASA GIBS, EONET and FIRMS** | Public imagery, event context and active-fire observations, where appropriately licensed | Event feeds and image layers have their own timestamps, confidence and limitations |
| **NOAA and public meteorological sources** | Weather, storm and climate context | Refresh cadence and spatial resolution differ across products |
| **SWOT, SMAP, GRACE/GRACE-FO and DEM/bathymetry products** | Research context for water elevation, soil moisture, regional storage, terrain and watershed assessment | Each sensor measures different quantities and scales; catalogue presence does not prove completed analysis |

Access to each provider is subject to its published API, licensing, quotas, security and availability requirements.

### Proposed evidence workflow

1. **Define the question:** region or area of interest (AOI), phenomenon, seasons, time windows and relevant uncertainty.
2. **Discover official sources:** select appropriate collections and sensors, checking coverage, temporal range, access and quality.
3. **Design the openEO process:** construct and review the processing graph, spatial/temporal filters, cloud masks, radar or spectral steps and output formats.
4. **Execute and monitor jobs:** submit bounded processing tasks; record job identifiers, retries, errors, resource use and outputs.
5. **Measure changes:** calculate comparable indices, mapped areas, backscatter differences, morphology or other justified indicators.
6. **Cross-check:** compare complementary sources and, where needed, rainfall, discharge, field measurements, DEM, bathymetry and authoritative records.
7. **Verify evidence:** preserve source metadata, product IDs, acquisition timestamps, AOI, resolution, parameters, hashes and uncertainty.
8. **Use AI as an assistant:** summarize established findings, propose alternative explanations and identify missing evidence — never fabricate measurements or causes.
9. **Human review:** distinguish preliminary signals from verified conclusions, and require qualified review before consequential advice or intervention.
10. **Publish reproducible results:** maps, time series, evidence reports and restoration-research questions with explicit limitations.

### Evidence classification

Reports should clearly separate:

- **OBSERVED** — documented source observations or official measurements;
- **DERIVED** — reproducible values computed from observations;
- **MODEL_ESTIMATE** — outputs dependent on assumptions and model limitations;
- **HYPOTHESIS** — possible, unverified explanations;
- **UNKNOWN / INSUFFICIENT_EVIDENCE** — absent, conflicting or inadequate evidence;
- **CONFIRMED** — findings supported by sufficient independent or authoritative verification.

For example, mapping a lake's surface area does **not** directly establish its water volume. A narrowing river channel does **not** establish the cause, prove an obstruction or justify dredging. Scientific and environmental decisions require additional evidence and local professional assessment.

## AI agents: two complementary layers

### 1. Existing Terra Agentic EO foundation

The [Polar-Sun-Moon-Analysis / Terra Observation System](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis) repository documents a provenance-first research coordinator built with the OpenAI Agents SDK:

- **Terra Agentic EO Coordinator** — plans and synthesizes bounded investigations.
- **EO Source Scout** — recommends official/public data sources from a controlled, machine-readable registry.
- **EO Evidence Verifier** — checks what repository evidence actually supports.
- **Deterministic tools** — perform calculations and guard against unsupported scientific claims.

A [published Vistula TEST 014 demonstration](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis/blob/main/docs/published/agentic-eo/vistula-test-014-live.md) documents manager/specialist execution and explicitly refuses to label dataset integrity as proof of water loss or hydrological causation.

### 2. openEO Agent alpha — intended integration

The [openEO Agent alpha integration note](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis/blob/main/docs/OPENEO_AGENT_ALPHA_INTEGRATION.md) identifies a **planned complementary role** for the openEO Agent assistant from the VITO/openEO ecosystem:

- explore appropriate EO datasets and collections;
- draft and explain openEO process graphs;
- help diagnose failed or inefficient processing jobs;
- compare alternative computational strategies;
- prepare bounded, reproducible satellite-data experiments.

The openEO Agent assistant and the OpenAI Agents SDK coordinator are **different tools**. Neither is a replacement for official source metadata, executed processing, independent validation or expert judgment. Alpha access is not evidence of scientific certification, operational integration or partnership with ESA.

## What has already been demonstrated elsewhere in this project ecosystem

This new repository draws on documented work, not a hypothetical greenfield design:

1. **Real openEO processing code:** an existing [Sentinel-1 before/after flood-change script](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis/blob/main/scripts/cdse/run_flood_detection.py) connects to the Copernicus openEO backend, authenticates with OIDC and produces candidate radar-backscatter change outputs. [Published metadata](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis/blob/main/docs/data/copernicus/flood_detection/run_metadata.json) documents a July 2026 run. It is **not a validated flood warning**.
2. **3D Earth and environmental research UI:** the [public Terra Observation demonstration](https://terraforming-planet.github.io/Polar-Sun-Moon-Analysis/) supports exploratory satellite and environmental research workflows.
3. **Recorded GPU research:** [NVIDIA L4 Training #3](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis) reports **200,016 processed geospatial/time windows across 75 research regions**. These are processing/training windows, **not 200,016 independent scenes, measured environmental changes or proof of detection accuracy**.
4. **Water-measurement utilities:** the upstream [terra_water measurement module](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis/blob/main/terra_water/measurement.py) includes Landsat reflectance/QA handling, Sentinel-2 quality masking, MNDWI and mapped-water-area sensitivity bounds.
5. **Scheduled public-data workflows:** the upstream repository defines [15-minute hazard refresh](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis/blob/main/.github/workflows/refresh-hazard-data.yml) and [global safety feed](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis/blob/main/.github/workflows/global-safety-monitor.yml) schedules. Scheduled configuration alone is **not proof of uninterrupted 24/7 uptime**.
6. **Restoration decision-support foundation:** [TerraWater AI](https://github.com/teslaeco/Terraforming-Planet-TerraWater-AI-Global-Water-Recovery) provides a related evidence-first water-recovery concept and early application scaffold.

### Research locations and demonstration themes

- **Vistula, Poland — TEST 014:** multi-decade dataset integrity and temporal coverage; environmental loss and cause remain unverified.
- **Olszówka / Gardeja, Poland:** lakes, forest ponds and watershed connectivity as a proposed local research case.
- **Aral Sea, Lake Chad, Lake Mead and Great Salt Lake:** long-term water-change investigation contexts.
- **Okavango Delta, wetlands, drylands, Himalaya–Tibet and polar environments:** future multi-sensor environmental comparison and restoration-research contexts.

These are research cases or candidate regions, not a declaration that every location already has a completed, validated monitoring pipeline.

## Current safe openEO planning implementation (source milestone — 23 October 2026)

The new `terraobserver/safety.py` module performs **offline, no-charge** AOI validation and deterministic bounded tiling. It rejects a Sahara-sized request at unacceptably fine 100 m resolution, invalid/relative dates and excessive pixels before any provider interaction. It returns `DRY_RUN_ONLY`, not a batch-job ID, result image, measured observation, budget approval or claim of working 24/7 monitoring. A dedicated CI suite tests these protections. The openEO Agent/Sentinel-1 pilot still requires verified dataset coverage, authentication, orbit selection, backend cost quote and owner-approved execution.

The scientific source of truth remains the existing [Terra Observation System](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis). The [Codex integration task](docs/CODEX_TERRAOBSERVER_OPENEO_P0_20261023.md) specifies the steps needed to advance this source milestone safely, including 3D Earth integration without inventing environmental measurements.

## Ocean circulation, seismic-event context and long-term environmental stewardship — new research track

The [Ocean & Earth Energy Retrospective Research protocol](docs/OCEAN_EARTH_ENERGY_RETROSPECTIVE_RESEARCH_20261023.md) adds a concrete scientific investigation plan: **42 days before and 42 days after a documented offshore earthquake**, with a close seven-day pre-event window, event-time observations, multiple historical same-season controls, and careful cross-checks of InSAR deformation, tide gauges, NOAA DART seafloor pressure, satellite sea-surface height and vetted bathymetry. A new tested pure Python module, \`terraobserver/event_windows.py\`, plans these windows without downloading data, spending openEO credits or claiming an earthquake forecast.

We propose long-duration research into water distribution, ocean/river dynamics, seabed topography, climate and energy exchanges, with public-good access for communities and scientifically responsible restoration. **No capability to safely control ocean currents, earthquakes, clouds, tornadoes or planetary water circulation is claimed.** Any real intervention requires independent peer review, downstream impact analysis, applicable permits and informed affected-community consultation.

As of the April 2026 GEBCO_2026 grid, **28.7% of the seafloor has modern-standard mapping**; this is a specific map-quality measure, not a claim that every other square kilometre is entirely unexplored. Our priority is accurate observations and modelling, not unsupported claims about human extraction causing major tectonic mountain systems or pre-earthquake ocean anomalies being predictive.

## Target 24/7 architecture

    Research question / monitored AOI / event trigger
                      |
             Scheduler + job queue
                      |
       Official catalogues and source adapters
                      |
           openEO / CDSE batch processing
                      |
        Provenance + measurements + validation
                      |
         Terra Agentic EO evidence coordinator
                      |
       Map / reports / reviewable alert candidates
                      |
       Researchers, communities, qualified experts
                      |
     Field verification and restoration decisions

Planned operational components include job persistence across disconnections, controlled retries, provider rate limits, budget ceilings, observability, alert deduplication, dataset versioning, secure server-side secrets and retention rules. Processing frequency must be chosen **per provider and scientific use case**, not confused with satellite acquisition frequency.

## Development roadmap

| Stage | Work | Status |
| --- | --- | --- |
| **0 — Research inventory** | Reuse and document existing Terra/openEO workflows, datasets, evidence and AI-agent architecture | Existing foundation documented in linked repositories |
| **1 — Controlled openEO Agent case** | Select one AOI, review process graph, execute a documented openEO job and preserve outputs | Planned for this repository |
| **2 — Scientific validation** | Add matched-season comparisons, cross-sensor checks, uncertainty, deterministic tests and provenance reports | Planned |
| **3 — Persistent orchestration** | Add scheduler, durable queue, monitoring, failure recovery, cost controls and secure provider configuration | Planned |
| **4 — Public TerraObserver dashboard** | Integrate maps, 3D Earth, time series, event context, traceable report links and human-reviewed alerts | Planned |
| **5 — Restoration research network** | Support expert collaboration, field validation, local impact studies and responsible intervention planning | Long-term goal |

The first milestone should be deliberately small: **one authenticated openEO job, one reproducible environmental case, one source-backed report and a clearly recorded success/failure outcome.**

## Related Terraforming Planet projects

**Earth observation and water research**
- [Polar-Sun-Moon-Analysis — Terra Observation System](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis) — main scientific, satellite-data, Agentic EO and visualization foundation.
- [TerraWater AI — Global Water Recovery](https://github.com/teslaeco/Terraforming-Planet-TerraWater-AI-Global-Water-Recovery) — water-system evidence and restoration decision support.
- [Earth Surface Mass & Water Redistribution](https://github.com/Terraforming-Planet/Earth-Surface-Mass-Water-Redistribution) — associated Earth-system research notes and hypotheses, not a validated live EO feed.
- [Polar-Sun-Moon-Analysis-Terra](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis-Terra) — NASA JPL Horizons polar Sun/Moon analysis, an adjacent scientific module.

**AI, visualization and resilience**
- [ForgeMCP — Multi-Agent Research & Game Studio](https://github.com/Terraforming-Planet/ForgeMCP-Multi-Agent-Research---Game-Studio) — supervised agent/tool research and evidence workflows.
- [TerraMind Rescue Planet](https://github.com/Terraforming-Planet/TerraMind-Rescue-Planet-Offline-Gemma-AI-for-Disaster-Survival-and-Solar-Resilience-) — separate offline-first emergency-assistance prototype.
- [WORLDIFACT](https://github.com/teslaeco/WORLDIFACT) — separate 3D world/model experimentation; potential visualization inspiration, **not** an integrated satellite processing backend.

The broader [Terraforming Planet organization](https://github.com/Terraforming-Planet) and [teslaeco account](https://github.com/teslaeco) also contain work on PV systems, graphics, simulation, games and AI experiments. Those projects are not automatically dependencies of TerraObserver.

## How to participate

This repository currently contains project documentation rather than a runnable application. For existing code and reproducible examples, start with the [Terra Observation System repository](https://github.com/Terraforming-Planet/Polar-Sun-Moon-Analysis) and its documentation.

We welcome research-oriented collaboration from Earth-observation specialists, hydrologists, ecologists, GIS developers, engineers, educators and open-source contributors. Useful contributions include:

- documented public datasets and legal processing paths;
- reproducible openEO graphs, small verified test cases and quality checks;
- uncertainty-aware multi-sensor comparisons and reference measurements;
- privacy-preserving engineering and reliable job orchestration;
- restoration proposals explicitly gated by ecological, hydrological, legal and field review.

Please do not publish account credentials, API tokens, precise private-person locations or unlicensed imagery. In particular, no person tracking, face recognition, surveillance targeting, covert monitoring or autonomous control of critical infrastructure is part of this project's purpose.

## Scientific and operational disclaimer

TerraObserver is a research and decision-support initiative. It is **not** an official warning service, a certified disaster predictor, a replacement for local authorities, or a system that independently authorizes physical changes to rivers, ecosystems or infrastructure.

The original repository does not yet contain a licence file. Although the intention is open collaboration, **public visibility does not itself grant reuse rights**; an explicit licence should be selected and added before external reuse is assumed.

---

**Terraforming Planet — observe the Earth, protect its resources, restore what can be responsibly restored.**

## Support this project

💚 [Support WORLDIFACT & Terraforming Planet](SUPPORT.md) — voluntary one-time contribution through [Stripe](https://buy.stripe.com/bJedR863q4if06D1YY1wY00). Support helps explore open-source 3D/AI and research into water resources, degraded drylands and evidence-based natural hazard observation. No subscriptions, AI credits or guaranteed research outcomes are included.
