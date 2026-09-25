# Static policy analysis and matched remediation

Completed 2026-09-25: **16 cells, 96 newly trained endpoints, 352.766 seconds**.
This is a new exploratory independent study, not a re-labeling of historical
results or an exact published reproduction. Sani suggested exploring an algorithmic
contribution, and Manish proposed this static-analysis direction. Sani has not yet
reviewed this specific implementation or its conclusions; independent priority
review remains open. The hash-frozen protocol's stronger attribution is retained as
a historical artifact and corrected here rather than edited after execution.

Open the [three-page PDF addendum](../../reports/Static_Policy_Analysis_2026-09-25.pdf).
The [prospective protocol](../../docs/protocols/static_policy_2026-09-25.md) fixes
the matrix, primary family, interpretation and failure conditions before execution.

## Algorithm

[Key-Scope Static Analysis, KSSA v1](../../src/biometrics_ai/protection/policy.py)
interprets the repository's YAML protection configuration without loading biometric
data or training an attacker. It is **configuration-level static analysis**, not
general source-code/dataflow analysis, a cryptographic proof, or a new transform.

1. Validate required scheme/condition declarations against the supported runner language.
2. Classify each scheme/condition pair as fresh-declared, shared across splits,
   shared projection, or unknown.
3. Report KEY_REUSE for global/recurring pools, KEY_CORRELATION for nonzero shared
   projections, and SLOT_DISCLOSURE for exposed key-slot labels. Unknown/invalid
   required declarations block analysis; no numeric pool size is deemed safe.
4. Retain NATIVE_LINKAGE_REVIEW for PolyProtect, HAAR_ASSUMPTION for uncorrected
   BioHash, and RUNTIME_ASSUMPTIONS for every policy. Output is block or review,
   never a security certificate. This is not exhaustive parameter-schema validation.
5. Propose a separate fresh-key configuration and remove explicit slot disclosure.
   Leave the original policy and all other experimental settings unchanged.

The scope-classification work is O(S*C) for S schemes and C conditions, apart from
string parsing and output size. Six synthetic runtime-agreement tests compare the
abstract classification with actual key audits; the broader unit suite includes
invalid inputs, unknown conditions, non-mutating recommendations and residual-risk
warnings. These fixtures do not establish real-world detector precision/recall.
The rules were informed by prior studies and are not a blinded discovery benchmark.

## Measured effectiveness

The evaluator uses the analyzer's proposed fresh condition, reruns the baseline
pool-4 condition and candidate with identical data, identity splits, key/set seeds,
training seeds, architecture and epoch caps, and compares paired identity scores.
Different key mechanisms still produce different key draws. Both arms are newly
trained; neither is copied from an earlier study.

MOBIO and FEI, IoM-GRP and PolyProtect; two overlapping identity assignments; three
model seeds (701/709/719); one-record single MLP and ten-record mean-pool MLP;
120-epoch cap and patience 30. Primary contrasts are baseline-minus-candidate at
ten records. Each cell below averages three seeds. Values are percentages except
the reduction and interval, which are percentage points.

| Dataset | Scheme | Split seed | Pool-4 top-1 | Fresh top-1 | Reduction | Paired 95% CI | Holm p |
|---|---|---:|---:|---:|---:|---|---:|
| MOBIO | IoM-GRP | 92531 | 95.42 | 3.33 | 92.08 | [81.66, 99.86] | 0.004 |
| MOBIO | PolyProtect | 92531 | 75.00 | 2.92 | 72.08 | [58.33, 84.58] | 0.004 |
| FEI | IoM-GRP | 92531 | 97.08 | 2.60 | 94.48 | [87.08, 99.79] | 0.004 |
| FEI | PolyProtect | 92531 | 85.62 | 1.88 | 83.75 | [73.44, 92.50] | 0.004 |
| MOBIO | IoM-GRP | 92543 | 98.33 | 3.89 | 94.44 | [86.11, 100.00] | 0.004 |
| MOBIO | PolyProtect | 92543 | 77.64 | 5.56 | 72.08 | [58.47, 84.03] | 0.004 |
| FEI | IoM-GRP | 92543 | 96.77 | 2.50 | 94.27 | [86.88, 99.69] | 0.004 |
| FEI | PolyProtect | 92543 | 87.71 | 2.19 | 85.52 | [76.25, 93.23] | 0.004 |

**Eight of eight primary comparisons support a reduction** under the specified
access model. Crossed model-seed/identity bootstrap: 2,000 draws. Identity sign-flip
of seed-mean paired differences: 1,999 resamples; Holm correction over eight primary
tests. All fresh learned intervals include chance (MOBIO 3.33%, FEI 2.50%), but are
broad: chance inclusion is not equivalence. One-record comparisons are secondary;
their p-values in the export are uncorrected and do not enlarge the primary claim.

This measures the effectiveness of the **flag-and-change workflow** for a known
key-reuse mechanism. It does not show that the analyzer discovers unknown attacks,
outperforms other analyzers, or introduces a previously unknown fresh-key defense.
The tool itself does not modify templates or deployed key management.

## Residual risk and utility

Fresh PolyProtect native cross-record top-1 remains **10.30-13.33% on MOBIO** and
**7.80-8.97% on FEI**, descriptively above chance. Fresh IoM native values are
4.55-5.45% and 1.61-2.06%, respectively. These are uncorrected descriptive native
cosine results, not new significant-null claims. The analyzer therefore retains
its PolyProtect review warning after the reuse finding is removed.

Fresh per-record keys may impair legitimate matching or require compatible
re-encoding and key-management changes. No authenticated verification-utility
experiment was run. Public deterministic research seeds are not production secrets.
The static checker cannot verify secrecy, entropy, finite-precision fidelity,
unique record identifiers, actual norms, side channels, or deployment behavior.

Only one pool draw per scheme, two overlapping partitions, three model seeds,
unit-normalized embeddings and one learned architecture were tested. The attacker
has paired access to the same realized baseline pool, known grouping and a small
closed gallery. This is not an independent population sample or general privacy
guarantee. SCface was not rerun: its embeddings are absent on this host. No raw
images, embeddings, per-identity scores, secret keys or weights are exported here.

## Artifacts and commands

- [Policy findings before/after](policy_audit.json)
- [Separate proposed policy](recommended_policy.yaml) and [actual two-arm matrix](executed_matrix.yaml)
- [All 96 endpoint summaries](results_summary.csv)
- [Paired policy effects](policy_effects.csv), including all eight primary contrasts
- [Native cross-record diagnostics](native_utility.csv)
- [Secondary per-seed intervals](paired_uncertainty.csv) and [equivalence sensitivity](equivalence_sensitivity.csv)
- [Completion status](matrix_status.json) and [pre-execution provenance](execution_manifest.json)

From the repository root, with the project installed in the local environment:

```powershell
.\.venv\Scripts\python.exe -m biometrics_ai.protection.policy --config configs/attacks/static_policy_2026-09-25.yaml
.\.venv\Scripts\python.exe -m biometrics_ai.protection.policy --config experiments/static_policy_2026-09-25/recommended_policy.yaml --enforce
.\.venv\Scripts\python.exe -m pytest tests/unit/test_static_policy.py -q
.\.venv\Scripts\python.exe scripts/figures/make_static_policy_report.py
```

Audit mode returns JSON and exit 0. `--enforce` returns 2 for blocking findings or
3 for unresolved review, including fresh-key policies. It cannot silently approve
an unverified deployment. This gate is opt-in; exploratory runners still permit
deliberately insecure positive controls.

The original training command was:

```powershell
.\.venv\Scripts\python.exe scripts/train/run_static_policy_evaluation.py --config configs/attacks/static_policy_2026-09-25.yaml
```

Rerunning the same command intentionally refuses to overwrite frozen outputs.
For a new run use a new configuration filename, a matching protocol filename,
and new output_root/summary_dir paths. Existing local embeddings are required.

The manifest records base commit `ffab5aae7750a254249970c4154d134d4754b2ad`, a dirty
worktree containing the new algorithm, exact source/config/protocol hashes, input
hashes and software versions. The base commit alone does not contain this study.
Local detailed outputs stay in the ignored results directory. Historical studies,
their correction families and the prior September PDF are unchanged.
