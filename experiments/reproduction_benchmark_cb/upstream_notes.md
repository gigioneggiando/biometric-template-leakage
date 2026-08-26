# Upstream notes

The official arXiv TeX source names `https://github.com/otroshi/benchmark_cb`. On 2026-08-26:

- `git ls-remote` returned repository not found.
- The author's public GitHub profile listed eight repositories and no replacement benchmark repository.
- GitHub code searches in the author and Idiap scopes found no match for the repository name, DOI, or arXiv identifier.

The paper itself verifies these face-protocol facts: ArcFace on 150 MOBIO subjects; 1,516,300 mated and 22,952 non-mated comparisons; all sample combinations for mated comparisons; and the first sample per subject for non-mated comparisons. It defines `normal` with user-specific keys and `stolen-token` with disclosed/non-user-specific key material. Its MI calculation applies PCA to 100 dimensions and a multivariate-Gaussian entropy estimate.

Do not infer an executable command from the paper. Recover an authorized source archive or corrected official URL, record its commit/license, and inspect its configs before adding an invocation.
