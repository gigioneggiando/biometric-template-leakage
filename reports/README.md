# Research package

## Pizza explanation and utility replication

Start with the [eight-page pizza PDF](Pizza_Algorithm_Explained_2026-09-25.pdf).
It explains the source analyzer in simple terms with pizza diagrams and plain
ASCII punctuation. The [new utility study](../experiments/utility_replication_2026-09-25/README.md)
completed 96 evaluations: 2/4 utility gates pass, both on MOBIO. FEI remains
inconclusive. No new joint security pass is claimed.

Pages 7 and 8 now explain the [new-participant audit](../experiments/new_participant_joint_2026-09-25/README.md)
and [algorithm-linked joint protocol](../docs/protocols/new_participant_joint_2026-09-25.md).
No unused FEI/MOBIO participants were found in the available inputs. The user
confirmed no new authorized cohort is available, so this is preparation only.
No new participants or joint results have been added; the proposed 500-person
target still needs feasibility and power approval.

The [reviewer packet](../experiments/source_review_2026-09-25/README.md) is prepared,
not externally labeled. The [internal proof/prior-work memo](../docs/review/source_proof_novelty_2026-09-25.md)
records assumptions and existing methods; independent proof and novelty review
remain pending. The replication ran while these reviews were pending.

Regenerate with `python -m scripts.figures.make_pizza_algorithm_report`.

## Source analysis and utility: 2026-09-25

The earlier [four-page PDF](Source_Security_Utility_2026-09-25.pdf) and
[full source/security/utility study](../experiments/source_security_utility_2026-09-25/README.md)
extend the configuration prototype with source-derived key/component provenance,
proposed mathematical criteria, a 24-case benchmark against YAML rules and Bandit,
and 18 new learned/legitimate-verification endpoints. **Both datasets fail the
fixed utility-noninferiority gate**, despite reduced leakage and similar average
matching accuracy. Independent source labels and research-priority review remain
open. See [the formal model](../docs/theory/source_scope_and_utility.md) and
[manuscript Section 4.2](paper_draft.md#42-source-derived-component-scope-and-utility-constrained-remediation).

The later [frozen 24-case holdout](../experiments/source_holdout_2026-09-25/README.md)
has 100% selective accuracy and no false-fresh decision, but fails its preregistered
coverage gate: 16 decisions and eight abstentions give 66.67% coverage.
[V2 development evaluation](../experiments/source_holdout_v2_2026-09-25/README.md)
corrects the invalid keyword case and improves valid-case coverage from 69.57% to
95.65% without an observed error. It is not an unseen confirmation.
The [frozen v2 confirmation](../experiments/source_holdout_v2_confirmation_2026-09-25/README.md)
passes all gates on 20 new valid cases: 19 correct decisions, one abstention, 95%
coverage and no false-fresh result. It remains internally authored.
[V3 real-protection integration](../experiments/source_real_integration_2026-09-25/README.md)
adds BioHash, IoM-GRP and PolyProtect contracts and correctly resolves all six
executable recurring/fresh recipes. Combined frozen coverage is 25/26 with no
observed error; the intraprocedural baseline resolves 6/26 and makes one error.

The prospective [MOBIO/SCface utility confirmation](../experiments/scface_utility_confirmation_2026-09-25/README.md)
adds 96 evaluations on new keys and identity reassignments. All four FMR bounds
pass, but zero of four cells pass the three-point TAR noninferiority criterion.
This strengthens the analyzer evaluation while leaving the remediation's utility
claim unresolved.

The updated algorithm briefing is available as a [four-slide PDF](slides/algorithm_update_2026-09-25.pdf)
and [PowerPoint](slides/algorithm_update_2026-09-25.pptx). Regenerate both with
`python scripts/figures/make_algorithm_update_deck.py`.

Regenerate with `python scripts/figures/make_source_security_report.py`.

## Static-analysis update: 2026-09-25

Start with the [three-page static-analysis PDF](Static_Policy_Analysis_2026-09-25.pdf),
[algorithm and full results](../experiments/static_policy_2026-09-25/README.md), and
[revised manuscript](paper_draft.md). KSSA v1 statically audits protection configs
and proposes a separate fresh-key comparison. A new 96-endpoint MOBIO/FEI rerun
finds eight corrected ten-record linkage reductions of 72.08-94.48 percentage
points. Native PolyProtect risk remains; fresh keys are not a security certificate
or a validated drop-in authentication defense. Research priority is not established.

Regenerate the addendum with `python scripts/figures/make_static_policy_report.py`.
The [internal algorithm review](../docs/review/algorithm_review_2026-09-25.md)
separates the demonstrated result from the remaining novelty and validation work.
The earlier report and slides below remain the historical September package.

## Historical finalized experiment update

The latest package is a **19-page report, 15-slide deck and 22-figure appendix**, integrating results through `4831d99`. Start with the [simple page-by-page README](Sept_Dataset_Update_README.md), then open the [PDF](Sept_Dataset_Update.pdf). The [detailed guide](Sept_Dataset_Update_guide.md) retains older exact tables.

The [672-endpoint extension](../experiments/scheme_followup_2026-09-19_full/README.md) strengthens MOBIO/SCface coverage with exposures 1/2/5/10 and pools 1/4/8. All eight planned gains pass correction; SCface is no longer only a pilot. [Raw learned retraining](../experiments/raw_input_attacker_2026-09-19/README.md) and [local stricter selection](../experiments/polyprotect_stricter_audit_2026-09-19/README.md) add negative findings. Raw/unit studies are not matched causal comparisons; the local policy is not an exact official reproduction. No experiments were rerun for this presentation refresh.

The experimental core is stronger and sufficient to finish a narrowly scoped manuscript for coauthor review. It does not establish universal privacy, method superiority, exhaustive novelty, or submission acceptance. Private inputs were not re-audited on this host. The historical notes below describe the earlier package, not the latest coverage.

**Updated: 2026-09-19.** Historical integration: `4352eeb`; SCface freeze `69a93e4`. Four datasets contribute at different evidence levels; pilots are not confirmation. The new [independent-pool study](../experiments/pool_replication_2026-09-19/README.md) adds 144 fits and 72 prediction-mean evaluations in 254.188 seconds. IoM gains persist across tested pools; PolyProtect is pool-sensitive, and no input-pooling superiority is established. SCface remains supporting pilot evidence.

The earlier [bounded follow-up](../experiments/scheme_followup_2026-09-18/README.md) adds 216 endpoints across three seeds/two partitions in 859.63 seconds, frozen against `4352eeb`. The [raw-norm/native audit](../experiments/norm_native_audit_2026-09-18/README.md), frozen against `15e4384`, re-extracts 4,177 records and checks all 48 paired contrasts in 254.157 seconds. The current package has a 16-page report, 12-slide deck and 19 figures. Raw norms do not establish identity-specific leakage; four significant shared-key DeepSets regressions are retained.

## Start here

- [September dataset update: 19 pages, architecture, results and scientific scope](Sept_Dataset_Update.pdf)
- [Independent pools, simple baseline, full numerical results and reproduction](../experiments/pool_replication_2026-09-19/README.md)
- [Each page explained in plain language](Sept_Dataset_Update_guide.md)
- [Closest research, precise contribution and attacker access](../docs/literature/closest_work_2026-09-18.md)
- [Current findings and scientific scope](final_research_status.md)
- [Completed 216-endpoint follow-up: results, controls and provenance](../experiments/scheme_followup_2026-09-18/README.md)
- [Architecture overview](figures/fig_architecture.pdf) and [detailed attacker](figures/fig_attack_detail.pdf)
- [Working manuscript](paper_draft.md)
- [Figure index, captions, and regeneration commands](figures/README.md)
- [15-slide PDF](slides/research_review.pdf)
- [Editable review deck](slides/research_review.pptx)
- [Complete 22-figure vector appendix](slides/figure_appendix.pdf)
- [New scheme pilot results and caveats](../experiments/scheme_extension_pilot/README.md)
- [SCface added-dataset study](../experiments/scface_multiexposure/README.md) and [SCface scheme pilots](../experiments/scface_scheme_extension_pilot/README.md)
- [Local per-seed run inventory](../experiments/multiexposure_run_matrix.csv)
- [Dataset access checklist](../docs/datasets/access_request_checklist.md)
- [Local audit and independent review gates](../docs/review/scheme_pilot_review_2026-09-12.md)
- [Cross-study key-pool table](../experiments/cross_dataset_key_pool_summary.csv)
- [Research roadmap](../docs/ROADMAP.md)

## File ownership

| Folder | Contents |
|---|---|
| `src/biometrics_ai/` | Reusable data, protection, attack, and evaluation code |
| `scripts/` | Dataset preparation, experiments, diagnostics, and figure builders |
| `configs/` | Versioned experiment and protection settings |
| `tests/` | Synthetic fixtures, numerical checks, and artifact validation |
| `experiments/` | Shareable compact results and study-specific interpretation |
| `docs/` | Protocols, approvals, source reviews, setup instructions, and research log |
| `reports/figures/` | Generated vector PDFs and PNG previews; source in `scripts/figures/` |
| `reports/slides/` | Generated PDF and editable PowerPoint review package |
| `results/`, data folders, model folders | Ignored local artifacts; never stage biometric records or weights |

Existing paths are preserved so historical configurations and citations continue to work. Generated previews used only for quality checks stay under ignored `results/figure_audit/`. Pilots must remain separate from confirmatory evidence, including in figures and slides.

The September PDF is regenerated by [the presentation builder](../scripts/figures/make_presentation.py), using source PDFs to retain vector architecture and searchable plot labels. The appendix, editable deck and figure PNG/PDF pairs serve distinct purposes and are current, not obsolete duplicates. Replace generated outputs in place; remove superseded audit screenshots only. Preserve historical compact results, protocols, licensed archives and model manifests.

The local per-seed inventory has 849 rows from 49 artifacts, retaining all previous 633 rows. It excludes SCface because its detailed run artifacts are not present on this host; two earliest MOBIO sources have legacy schemas outside the inventory. The [coverage audit](../experiments/scheme_followup_2026-09-18/coverage_audit.csv) states these gaps. Current SCface aggregate CSVs remain tracked. Acquisition records are linked from the [data README](../data/README.md).

## Approval and access

On 2026-09-12 the user reported Sani's approval of paper-specified IoM-GRP and PolyProtect and authorized pilots first, with at most one hour of new local training in this session. On 2026-09-18 Sani supplied the authorized SCface archive directly; AgeDB access remains unavailable. Dataset acquisition and independent human scientific review remain external gates; a local audit cannot substitute for either.

The later one-hour authorization selected available MOBIO/FEI embeddings for the bounded follow-up. All 24 cells completed in 859.63 seconds; no new SCface/LFW training was performed. The resulting exports passed 42 focused figure/scheme tests, README link checks and rendered-PDF inspection. These checks validate the package, not scientific equivalence, independent review or the unfinished full roadmap.
