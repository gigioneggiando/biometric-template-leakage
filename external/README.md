# External source policy

**Status checked: 2026-09-18**, against `4352eeb`. SCface aggregate results and scheme pilots are now integrated, but no official `benchmark_cb` or FaceLinkGen result has been reproduced. See the [current research status](../reports/final_research_status.md).

Third-party repositories are not vendored. Each source must be cloned into `external/` at the pinned commit in `manifests/upstream_sources.yaml`. The benchmark_cb entry is deliberately unresolved because the specified URL was unavailable during audit.

The new [216-endpoint MOBIO/FEI follow-up](../experiments/scheme_followup_2026-09-18/README.md) uses the same paper-specified local IoM-GRP/PolyProtect implementations. Its [execution manifest](../experiments/scheme_followup_2026-09-18/execution_manifest.json) records base `4352eeb` and separate pre-execution source/configuration hashes. It introduces no verified upstream implementation or source-exact reproduction; existing upstream pins and blockers are unchanged.

Source availability was last explicitly rechecked on 2026-08-26; the current documentation date is not a new upstream verification. IoM-GRP, PolyProtect and MLP-Hash are paper-specified local implementations, not source-exact reproductions. Authorized dataset archives remain private, with acquisition dates and setup links in the [data policy](../data/README.md). Do not delete pinned source manifests or archive provenance as part of figure cleanup.
