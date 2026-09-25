# Internal proof and prior-work review

Date: 2026-09-25. Status: internal assistant review, not independent peer review.
No external reviewer has signed the proof, labels or novelty claim. This note
supplements, and does not rewrite, the frozen earlier theory and protocol.

## Review findings

1. The weighted reuse functional is valid as an expected count, by linearity of
   expectation. It is not a privacy bound or new probability identity. Weighting
   a component by size does not bound the identity information carried by it.
2. The uniform formula requires IID uniform label allocation. A static bound on
   pool cardinality does not establish that allocation law. For IID biased draws,
   the collision probability is the sum of squared slot probabilities. Deterministic
   record allocation needs a specified record distribution or actual pair labels.
3. The coupling envelope needs an explicit common probability space, independence
   of transform selection from identity and admissible side information, and a
   source-independent ideal view. The existing proof is a sketch conditional on
   these strong assumptions, not a machine-checked theorem for the actual program.
4. The source transfer rules are plausible on well-typed, normally terminating,
   straight-line executions under reviewed call contracts. The current untyped
   interpreter is not a general Python semantic proof. It does not establish
   correct input shapes, successful execution, all API preconditions, numerical
   independence or secrecy. Treat conditional_fresh as a conditional key-scope
   summary, not executable correctness or safety.
5. Key-capacity findings are conservative. A fixed expression reduced modulo K
   may retain a loose capacity K rather than one. Loose upper bounds can reduce
   precision without establishing actual collisions for a finite deployment.
6. A truncated 64-bit KDF is not injective over unbounded integers. The birthday
   qualification needs a random-function assumption and a bound on distinct calls.
   Real collision handling and production key generation remain outside the proof.
7. The source reader supports selected projection blocks, not arbitrary correlation.
   Equal component labels are a structural reuse signal. Unequal dependent transforms
   can still violate an ideal independence argument without being detected.
8. Bootstrap bounds with three or twelve key draws are approximate. Bonferroni
   controls multiplicity only to the extent the constituent bounds cover. Conditioning
   on the enrollment gallery and observed validation thresholds must remain explicit.
9. A trusted verifier with external key custody is a deployment assumption, not a
   newly proved biometric transform. Key-service compromise or unrestricted compatible
   encoding queries can defeat the intended attacker restriction.

## Verified prior-work anchors

These specific public pages were fetched on 2026-09-25. This is a targeted
first-pass comparison, not a systematic literature search or full-paper review.

| Source | Verified overlap | Consequence for our claim |
|---|---|---|
| [Cousot and Cousot, POPL 1977](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml) | Abstract interpretation summarizes concrete computations in an abstract domain | Abstract domains and transfer rules are established methodology |
| [CogniCryptSAST / CrySL](https://github.com/CROSSINGTUD/CryptoAnalysis) | CrySL-specified crypto misuse analysis; context, field and flow-sensitive analysis for Java/Android | Rule-guided cryptographic static analysis is not new; our narrower Python biometric scope needs comparison |
| [CryptoGuard](https://github.com/CryptoGuardOSS/cryptoguard) | Cryptographic misuse analysis of Java/Android; project links its CCS 2019 paper | General crypto misuse/dataflow claims require attribution and full-paper comparison |
| [Bandit 1.8.6](https://bandit.readthedocs.io/en/1.8.6/) | Python AST plugins for common security issues | The executed Bandit baseline is useful but does not establish superiority over specialized tools |

CogniCrypt and CryptoGuard were reviewed from their project descriptions, not run
against our Python fixtures. They target different languages and contracts. A fair
quantitative comparison would need a justified common task and equivalent semantics,
not interpreting their inability to parse Python as missed vulnerabilities.

Candidate contribution: source-derived biometric key/component provenance linked
to exposure-reuse accounting and a prospectively evaluated utility constraint.
Do not claim the first biometric source analyzer without a specialist search.
Do not call the reuse expression, union bound or noninferiority conjunction new
mathematics solely because the notation or application is new.

## External review checklist

Two reviewers should first receive only the answer-free case archive. Once labels
are locked, a mathematical reviewer can inspect the theory and implementation.
Record reviewer, date, source hashes, conflicts and access to prior results.

| Review item | Required evidence | Current status |
|---|---|---|
| Independent case labels | Two frozen forms, disagreements and adjudication | Pending |
| Unseen constructions | Externally authored cases labeled before model outputs | Pending |
| Source soundness | Precise typed subset, concrete semantics, transfer-rule proof or counterexamples | Internal sketch only |
| Collision envelope | Explicit coupling and side-information assumptions | Internal sketch only |
| Novelty | Specialist full-text comparison and dated search record | Targeted project-page review only |
| Practical utility margin | Domain-owner approval of the three-point tolerance and FMR ceiling | Pending |

Suggested search themes for the external review: biometric template-protection
static analysis; cryptographic key/nonce reuse dataflow; CrySL and cryptographic
misuse specifications; relational abstract interpretation; probabilistic information
flow; cancelable-biometric utility and unlinkability. Record actual queries, dates,
databases and inclusion decisions. No database search is claimed in this note.

The utility replication can proceed as a separately labeled exploratory study
while review is pending. It cannot be called a post-review confirmation or clear
the independent-review gates automatically.