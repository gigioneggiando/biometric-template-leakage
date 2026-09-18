# benchmark_cb face reproduction

**Status checked: 2026-09-18.** Commit `4352eeb` adds SCface and pilot results, not an upstream reproduction. Four-dataset BioHash studies, 72 historical scheme pilot endpoints and the separately hash-frozen [216-endpoint MOBIO/FEI follow-up](../scheme_followup_2026-09-18/README.md) remain independent studies. The new controls do not resolve the missing official source or exact protocol. See the [current status](../../reports/final_research_status.md). The source-availability check below retains its original date; no new upstream check or benchmark run is claimed.

Status: **NOT REPRODUCIBLE YET**. Authorized MOBIO data is prepared locally, but the specified official URL remained unavailable on 2026-08-26 and no renamed repository was found in the author/Idiap GitHub scopes. Paper targets are verified in `expected_results.csv`; no local benchmark value has been run. When the official source and exact configuration are recovered, pin the upstream commit in `external/manifests/upstream_sources.yaml`, copy only configurations/commands here, and run the exact ArcFace+MOBIO BioHash branch.

LFW or synthetic results may validate plumbing only and must be labelled engineering validation. The completed LFW Month 1 experiment is documented separately under `experiments/month1_lfw/`.
