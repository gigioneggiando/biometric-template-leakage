# Threat-model comparison

| System | Protected template access | Protection/key knowledge | FR backbone | Multiple observations | Output goal | Main metric |
|---|---|---|---|---|---|---|
| benchmark_cb | yes | paper has known-/unknown-key scenarios | known for benchmark | no | recognition/privacy evaluation | EER, unlinkability, irreversibility |
| Breaking Template Protection | yes | full-disclosure/high knowledge | paper-specific | no | face reconstruction | reconstruction and recognition |
| GaFaR | raw FR template | white- or black-box variants | target FR varies | no | 3D-assisted face reconstruction | identity similarity/attack success |
| FaceLinkGen | PPFR representation | near-zero to stronger knowledge variants | ArcFace-compatible teacher | no | identity embedding/linkage | matching and regeneration success |
| Proposed K0 | protected templates | scheme family known; keys unknown and unseen | documented public backbone | yes, 1/2/5/10 | identity embedding | cosine, EER, TAR, top-k |
| Proposed K1 | protected templates | scheme hyperparameters known; keys unknown/unseen | documented public backbone | yes, 1/2/5/10 | identity embedding | same as K0 |

K0 and K1 must use identity-disjoint attacker training/testing. K0 is the primary claim; a condition with seen identities and seen keys is only a debugging upper bound.
