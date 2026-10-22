VALIDATION_RULES.md - OpenEO Job Validation Rules (lessons from Incident #1 - OOM when processing the entire Sahara)

Purpose of the document: A set of technical rules that should be implemented in the task generation/launch logic (outside the AI model itself) to prevent a repeat of the "Incident #1" type of failure - executor memory overload when processing very large spatial extents.

1. Pixel limit before job starts

Before sending the job to the backend, you need to calculate the estimated pixel count:

liczba_pikseli = (szerokość_bbox_m / rozdzielczość_m) × (wysokość_bbox_m / rozdzielczość_m) × liczba_pasm × liczba_dat
Set a hard maximum threshold (e.g., 50–100 million pixels per batch job, to calibrate to cluster capacity).
If exceeded → block the launch and return a clear message ("too large range for this resolution, increase the resolution to X m or reduce the area").
2. Minimum resolution depends on the size of the area

Enter a threshold table/rule, e.g.:

bbox size (km)	Min. allowed resolution
< 100 km	10 m
100–500 km	50–100 m
500–2000 km	250–500 m
> 2000 km (e.g. the entire Sahara)	≥ 1000 m
The rule should be enforced automatically in the code generator, not left as a suggestion.

3. Time range validation

Never use hardcoded/obsolete dates as placeholders (like the incorrectly generated range "2024-06-01–2024-06-05" during patches).
Relative dates ("today", "last N days") must be resolved to specific dates before being stored in the final process graph, with the generation date explicitly provided.
4. Confirmation for high risk/high cost tasks

Before running a task that exceeds a threshold (e.g. estimated cost > X credits, time > Y minutes), require explicit user confirmation showing the estimate.
The estimate should be shown before create_and_start_job , not after, the failure.
5. Strategy for large areas: tiling instead of one task

For continental/supra-regional coverage:

Divide the area into tiles (e.g. 2°×2° grid or UTM-based), run as separate parallel or sequential tasks.
Combine results in a post-processing step (mosaicing), instead of one monolithic Spark job.
6. Monitoring and early termination

Set a timeout appropriate to the type of analysis to avoid situations like Incident #1 (45 minutes before error, 76 credits spent with no result).
Log and report early warning signals (e.g., first Executor Lost (OOM)) as a basis for automatic termination instead of waiting for all retries to be exhausted.
Related to Incident #1: None of the above rules existed at the time of the crash - the job validated despite the size of the area not being adequate to the specified resolution (100m for the entire Sahara), leading to the Spark stage failing 4 times and consuming 76 credits with no result.

Implementation status: To be implemented on the task generator/orchestrator logic side (beyond the scope of the conversational model itself).
