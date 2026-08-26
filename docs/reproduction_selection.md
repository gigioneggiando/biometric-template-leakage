# Reproduction target selection

| Candidate | Relevance | Code availability | Data availability | Compute practicality | Implementation time | Scientific value | Pipeline validation | Total / 35 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| benchmark_cb face | 5 | 1 | 2 | 4 | 3 | 5 | 5 | 25 |
| FaceLinkGen core | 5 | 1 | 2 | 2 | 2 | 5 | 5 | 22 |
| GaFaR checkpoint evaluation | 3 | 5 | 2 | 1 | 2 | 4 | 3 | 20 |
| Breaking Template Protection | 4 | 1 | 2 | 2 | 2 | 4 | 4 | 19 |

Selected targets are (1) benchmark_cb face and (2) FaceLinkGen identity extraction, matching the research brief. Neither can be honestly started as an exact reproduction today: the stated benchmark repository was unavailable and MOBIO is manual-access; FaceLinkGen code was not verified and the PDF protocol must be extracted before a faithful direct implementation. GaFaR is retained as the fallback if official checkpoint assets become available first.

The local synthetic pipeline and completed LFW Month 1 single-template study validate engineering constraints only. Neither is selected or reported as a paper reproduction target.
