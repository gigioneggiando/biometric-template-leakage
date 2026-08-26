# Comparison

| Metric | Paper value | Our value | Absolute difference | Relative difference | Status | Explanation |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Unprotected face EER, normal | 0.02% | TODO / not run | N/A | N/A | NOT REPRODUCIBLE YET | authorized MOBIO and verified upstream source pending |
| BioHash face EER, normal | 0.02% | TODO / not run | N/A | N/A | NOT REPRODUCIBLE YET | authorized MOBIO and verified upstream source pending |
| BioHash face EER, stolen-token | 0.04% | TODO / not run | N/A | N/A | NOT REPRODUCIBLE YET | paper scenario must be reproduced exactly |
| BioHash face MI, normal | 39.63 | TODO / not run | N/A | N/A | NOT REPRODUCIBLE YET | paper uses PCA to 100 dimensions and a Gaussian MI estimate |
| BioHash face MI, stolen-token | 98.81 | TODO / not run | N/A | N/A | NOT REPRODUCIBLE YET | paper uses PCA to 100 dimensions and a Gaussian MI estimate |

Values were transcribed from Tables I, II, and IV in the official `arXiv:2302.13286v1` TeX source on 2026-08-26. The LFW Month 1 result is intentionally excluded because its dataset, checkpoint, protection implementation, dimensions, attacker objective, and comparison protocol differ.
