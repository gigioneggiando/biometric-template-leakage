# Local audit and independent review gates

This is an assistant's local technical audit, not independent human review, professor approval, or a novelty certification. The user authorized one hour of pilots only; the 16 cells finished in 277.89 seconds. No full confirmation or new-data acquisition was launched.

## Theory and related work

The [multiplicity-invariance proof](../theory/multiplicity_invariance.md) now requires the key and postprocessing randomness to be jointly independent of the identity, source vectors and allowed side information. Independence of side information from identity alone is insufficient: independent uniform signs Y,K with T=KY and Z=K give marginal independence of both T and Z from Y, but together reveal Y. With valid conditional invariance, templates give no improvement over the Bayes decision using Z alone, not necessarily unconditional chance. Finite empirical accuracy need not equal its expectation.

Ideal Gaussian IoM-GRP satisfies the rotational-invariance premise. Finite PRNG support, numerical arithmetic and key-dependent side information require separate treatment. PolyProtect is not covered. Positive scaling leaves zero-threshold BioHash and IoM-GRP unchanged, so a norm-information upper bound is not evidence that those outputs actually reveal norms.

The primary PolyProtect paper already evaluates record multiplicity (one to ten records, Section 4.3) with disclosed coefficients/exponents. Hidden-parameter learned linkage is a different threat model, but record multiplicity itself is not novel. Sources: [PolyProtect](https://doi.org/10.1109/TBIOM.2022.3140472), [IoM](https://doi.org/10.1109/TIFS.2017.2753172). This audit is not an exhaustive literature search. Exact benchmark reproduction remains blocked by the unavailable official source. Independent implementation from a paper does not imply patent or commercial-use clearance.

## Statistical interpretation

Paired identity-bootstrap differences now align identities across endpoints and reuse the same resampled identity indices. The new pilot retains private per-identity scores so these contrasts can be checked. Intervals condition on a single trained model seed and identity assignment; they omit training-seed uncertainty and multiple-comparison adjustment. Historical runs lacking retained scores cannot acquire paired uncertainty from aggregate means alone.

Fresh-key equivalence sensitivity uses strict containment of a 90% interval within illustrative +/-1/2/5 percentage-point bands. No endpoint meets +/-1 point; only one of 12 meets +/-2 points. Do not select a margin after observing which one passes. Native fresh-key PolyProtect protected-gallery identification is above chance and needs its own uncertainty and null-calibration study; near-chance learned unprotected-gallery attacks cannot establish unlinkability.

## Proposed confirmation, not yet authorized

| Decision | Proposed next step | Gate |
|---|---|---|
| Dataset coverage | Existing MOBIO/LFW/FEI plus SCface, or approved AgeDB contingency | Authorized access and gallery-plus-ten eligibility |
| Scheme coverage | BioHash, MLP-Hash, IoM-GRP, PolyProtect on each accepted dataset | Source/specification and native-utility review |
| Primary endpoints | Single MLP at 1; mean-pool MLP at 2/5/10; DeepSets secondary | Agree attacker, metric and contrasts before runs |
| Transform conditions | Fresh, pool 1/4/8; add boundary points only with rationale | Freeze key/set seeds and parameter settings |
| Replication | At least three new model seeds and multiple identity assignments | New compute budget and sealed configuration commit |
| Statistics | Identity-paired contrasts, seed variability, prospective equivalence margins | Reviewer-approved margin, power and multiplicity plan |
| Controls | PolyProtect native matching, same-image and shuffled-record controls; justified norm-sensitive construction | Distinguish protected/unprotected gallery tasks |
| Synthesis | Reconcile all historical compact sources with the 633-row local matrix | Coverage audit and missing-artifact recovery |

Pilot-informed choices are legitimate for a new prospectively frozen study, but cannot retroactively turn the pilot into confirmation. Do not pool incompatible gallery sizes, stages, training budgets or identity assignments for a scheme ranking.

## Independent reviewer checklist

- [ ] Named theory reviewer checks conditional independence, norm statements, finite-key caveats and proof/counterexample.
- [ ] Named methods reviewer compares both implementations to primary algorithms and reviews parameter sensitivity.
- [ ] Named statistics reviewer approves equivalence margins, power, identity/seed uncertainty and multiple-comparison handling.
- [ ] Named literature reviewer searches current IEEE Xplore/Scholar and related biometric linkage/record-multiplicity work, recording queries and nearest competing claims.
- [ ] Sani reviews the scientific scope and the PDF/PowerPoint on the presenting machine.
- [ ] Record reviewer, date, finding, response and approval before closing each gate.

No independent reviewer has signed off. A manuscript can be developed now; submission readiness and A/A* suitability remain unestablished.