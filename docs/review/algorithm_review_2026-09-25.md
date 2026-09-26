# Review of the proposed source and policy analysis

Date: 2026-09-25  
Status: internal engineering and methods review; not professor or peer approval

## Amendment: 2026-09-26

The review below describes the earlier prototype. V2/v3 later added selected
control flow and scheme contracts, but a cross-branch false-fresh counterexample
was reproduced. The [dated correction](../../experiments/source_branch_fix_2026-09-26/README.md)
now blocks complete freshness from branch-local sinks and unsupported predicates.
The original source snapshot and results remain available; 69 overlapping
historical case evaluations retain their predictions after repair. This is
internal regression evidence, not a general soundness theorem. Portable provenance
checks now distinguish exact bytes from manifest-matching newline conversions.

The later MOBIO/SCface utility confirmation passes 0/4 cells. Independent validation
is deferred to the user and reviewers, and the data, power and joint-utility gates
remain open. A software repair does not establish successful biometric remediation.

## Verdict

The work is a useful research prototype and is presented more cautiously than the
message "lower security risk" suggests. The strongest component is the restricted
Python source interpreter, not the YAML-only KSSA checker. It traces key provenance,
abstains on unsupported constructs, links findings to executable recipes, and tests
both attacker success and legitimate matching.

It is not yet a defensible main paper contribution. The current evidence shows that
changing a known four-key reuse policy to per-record derivation reduces one tested
linkage attack. It does not show that the analyzer discovers previously unknown
flaws, generalizes to independently written systems, or preserves utility under the
fixed joint gate.

## Findings

1. **The central security comparison is expected, not independent discovery.**
   Earlier project experiments established high leakage for pool four and near-chance
   learned linkage for fresh keys. KSSA encodes that rule and the evaluation repeats
   the same intervention on new seeds and splits. This validates the workflow but is
   weak evidence of analyzer effectiveness or novelty.
2. **The joint security/utility claim currently fails.** The source-guided pilot
   passes the leakage and FMR bounds but fails TAR noninferiority on both MOBIO and
   FEI. The utility-only replication passes both MOBIO partitions and neither FEI
   partition. Therefore the candidate cannot be described as a generally improved
   security policy with retained utility.
3. **The analyzer benchmark is developmental.** Its 24 cases are same-author cases;
   the source analyzer records 13 true positives, seven true negatives and four
   abstentions against its finite-domain oracle. Independent labels and independently
   authored holdouts are still empty. Bandit and the YAML checker are scope baselines,
   not competitive biometric provenance analyzers.
4. **The implementation scope is narrow but honestly bounded.** Straight-line local
   Python, selected arithmetic, helpers and BioHash projection contracts are supported.
   Branches, loops, keyword calls, cross-module flows, general correlation and most
   real application code lead to abstention. `conditional_fresh` is not a security or
   unlinkability certificate.
5. **The threat model is strong and specific.** The learned attacker knows record
   grouping, trains on the same realized hidden pool, and searches a small closed
   gallery. The proposed trusted verifier assumes protected key custody and restricted
   compatible-encoding access. Key-service compromise, chosen-probe access, open-set
   recognition and unknown grouping remain outside the evidence.
6. **The public test claim needed repair.** One test required ignored private metadata
   files, so a clean checkout produced 195 passes and one failure. The test now verifies
   recorded hash syntax everywhere and verifies file content when private inputs are
   locally present. No frozen result or manifest hash was changed.
7. **Attribution needed refinement.** Sani suggested exploring an algorithmic
   contribution, while Manish proposed this particular static-analysis direction.
   Sani has not yet reviewed this implementation or its conclusions. The
   hash-frozen protocol retains its original wording as a historical artifact; the
   current documentation records the more precise distinction.

## Recommended v2

1. Freeze an answer-hidden benchmark containing independently authored programs,
   realistic negatives and explicit expected abstentions before changing inference
   rules. Use two independent reviewers and report agreement and adjudication.
2. Evaluate precision, recall, false positives, coverage and abstention separately.
   Add a simple domain-aware syntactic baseline; do not treat Bandit's different scope
   as evidence of superiority.
3. Test real integration code from multiple authors or projects. Preserve a held-out
   set that the analyzer developer cannot inspect until the implementation is frozen.
4. Extend language coverage only in response to frozen benchmark gaps: branches,
   loops, keyword calls, classes, dictionaries, inter-file calls and explicit
   contracts for additional protection schemes. Unsupported behavior must continue
   to fail closed.
5. Separate findings for definite reuse, bounded possible reuse, shared components,
   correlation, disclosure and unknown behavior. Do not convert pool capacity into a
   privacy bound without an allocation distribution.
6. Make remediation source-linked: emit a minimal witness trace, propose a separate
   patch, re-analyze the patched source, and verify runtime key labels before any
   attack experiment. Never label the rewrite secure solely from static output.
7. Run the joint leakage/TAR/FMR design on a genuinely new authorized cohort only
   after a power simulation and application-owner approval of the utility margin.
   Preserve the current failed gates rather than tuning thresholds to pass.
8. Add open-set, unknown-grouping and key-service-compromise experiments if deployment
   claims are planned. Otherwise keep the paper claim explicitly limited to the
   database-only attacker and trusted-verifier architecture.

## Positioning for Sani

Present this as a proposed **biometric key-provenance analysis and evidence workflow**,
not a new protection algorithm and not a completed security improvement. The pitch is:

> Can a fail-closed source analysis identify transform reuse, produce a traceable
> policy change, and prospectively demonstrate lower linkage without unacceptable
> authentication loss?

The answer is currently: reuse detection works on the authors' bounded corpus, the
tested attack falls after the policy change, but independent analyzer validation,
joint utility success, new-participant evidence and novelty review remain open.

## Prior-work anchors

- Kruger et al., [CrySL: Validating Correct Usage of Cryptographic APIs](https://arxiv.org/abs/1710.00564), establishes rule-guided, context- and flow-sensitive cryptographic misuse analysis at application scale. The contribution must therefore be biometric-specific provenance and evaluation, not generic crypto static analysis.
- Wang et al., [A Theoretical Analysis of Authentication, Privacy and Reusability Across Secure Biometric Systems](https://arxiv.org/abs/1112.5630), already frames authentication, leakage and reuse across multiple keyed systems. The project must distinguish its source-level operational contribution from this theoretical trade-off literature.
- Abdullahi et al., [Biometric template attacks and recent protection mechanisms: A survey](https://doi.org/10.1016/j.inffus.2023.102144), provides the broader attack and protection taxonomy needed for a systematic novelty review.
