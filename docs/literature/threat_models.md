# Threat-model comparison

| System | Protected template access | Protection/key knowledge | FR backbone | Multiple observations | Output goal | Main metric |
|---|---|---|---|---|---|---|
| benchmark_cb | yes | paper has known-/unknown-key scenarios | known for benchmark | no | recognition/privacy evaluation | EER, unlinkability, irreversibility |
| Breaking Template Protection | yes | full-disclosure/high knowledge | paper-specific | no | face reconstruction | reconstruction and recognition |
| GaFaR | raw FR template | white- or black-box variants | target FR varies | no | 3D-assisted face reconstruction | identity similarity/attack success |
| FaceLinkGen | PPFR representation | near-zero to stronger knowledge variants | ArcFace-compatible teacher | no | identity embedding/linkage | matching and regeneration success |
| Proposed K0 | protected templates | scheme family known; keys unknown and unseen | documented public backbone | yes, 1/2/5/10 | identity embedding | cosine, EER, TAR, top-k |
| Proposed K1 | protected templates | scheme hyperparameters known; keys unknown/unseen | documented public backbone | yes, 1/2/5/10 | identity embedding | same as K0 |
| Proposed R-k (key reuse) | protected templates | scheme known; a hidden pool of k transforms recurs system-wide; slot labels hidden | documented public backbone | yes, 1/2/5/10 | identity embedding | same as K0 |
| Stolen-token preimage attacks (Nagar 2010; Lacharme 2013; Feng 2014; Dong 2019/2022; Wang 2020; Ghammam 2019; Durbet 2021) | one protected template | transform fully known | varies | no | preimage/impersonation | attack success rate |
| Record multiplicity on fuzzy vaults (Scheirer and Boult 2007; Merkle and Tams 2013) | two or more vault records | scheme known; no secret rotation | n/a | yes | template recovery | recovery rate |

K0 and K1 must use identity-disjoint attacker training/testing. K0 is the primary claim; a condition with seen identities and seen keys is only a debugging upper bound. R-k with k = 1 is the unknown-but-shared-token analogue of the stolen-token literature; k > 1 with hidden slot labels has no located precedent (see `docs/theory/multiplicity_invariance.md`).
