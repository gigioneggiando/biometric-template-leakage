# Multiplicity invariance under fresh rotationally invariant keys

Status: formal statement and proof sketch, written 2026-09-04. Not yet independently reviewed. The assumptions are stated so that every experiment in this repository can be classified as inside or outside the theorem.

## Setting

- Embedding space $\mathbb{R}^d$ with $d = 512$. A source image yields an embedding $x \in S^{d-1}$ (unit L2 norm). The extractor in `src/biometrics_ai/face/arcface.py` normalizes every embedding, so this holds in the pipeline.
- Identity $Y$ is a random variable; the embeddings $x_1, \dots, x_n$ of $n$ exposures are arbitrary (possibly dependent) functions of $Y$ and nuisance variables.
- A key $K$ selects a linear map $P_K \in \mathbb{R}^{m \times d}$ and, optionally, further key material $K'$ used by a fixed measurable post-processing map $g$. The protected record is $T = g(P_K x, K')$.
- $(K, K')$ is independent of $(Y, x_1, \dots, x_n)$.

Definition (rotationally invariant projection law). The law of $P_K$ is *right-rotation invariant* if $P_K R \overset{d}{=} P_K$ for every $R \in O(d)$.

Examples satisfying the definition: (i) i.i.d. Gaussian rows; (ii) the first $m$ rows of a Haar-distributed $Q \in O(d)$; (iii) a Haar-distributed element of the Stiefel manifold $V_m(\mathbb{R}^d)$ (orthonormal rows). Case (iii) is the idealized BioHash projection; case (ii) applied column-wise is the idealized MLP-Hash widening layer.

## Lemma 1 (single-record invariance)

If $P_K$ is right-rotation invariant and $x, y \in S^{d-1}$, then $P_K x \overset{d}{=} P_K y$.

Proof. Choose $R \in O(d)$ with $R x = y$ (exists because both are unit vectors). Then $P_K y = (P_K R) x \overset{d}{=} P_K x$. $\square$

Consequently the conditional law of $P_K x$ given $x$ does not depend on $x$, so $P_K x \perp x$ whenever $P_K$ is independent of $x$.

## Theorem 1 (fresh-key multiplicity invariance)

Let $K_1, \dots, K_n$ be mutually independent, each with a right-rotation-invariant projection law, and independent of $(Y, x_1, \dots, x_n)$. Let $T_i = g_i(P_{K_i} x_i, K_i')$ with $K_i'$ independent of everything else. Then

$$(T_1, \dots, T_n) \perp (Y, x_1, \dots, x_n), \qquad \text{hence} \qquad I(Y; T_1, \dots, T_n) = 0 \text{ for every } n.$$

Proof. Condition on $(x_1, \dots, x_n) = (a_1, \dots, a_n)$. By independence of the keys, $(P_{K_1} a_1, \dots, P_{K_n} a_n)$ has product law with factors $\mathcal{L}(P_{K_i} a_i)$. By Lemma 1 each factor equals $\mathcal{L}(P_{K_i} e_1)$, independent of $a_i$. The conditional law of $(P_{K_i} x_i)_i$ therefore does not depend on the conditioning value, so $(P_{K_i} x_i)_i \perp (x_1, \dots, x_n)$. Applying the fixed maps $g_i$ with independent $K_i'$ preserves independence. Since $Y \to (x_i)_i \to (T_i)_i$ is a Markov chain, $I(Y; T_{1:n}) \le I((x_i)_i; T_{1:n}) = 0$. $\square$

Corollary 1 (attack bound). For any attacker $\mathcal{A}$ that receives $T_{1:n}$ and any side information $Z$ independent of $Y$ (training data from other identities, the protection algorithm, unlimited compute), the identity-linkage accuracy against a gallery of $N$ identities with uniform prior is exactly $1/N$. Pooling more fresh-key records does not change this.

Corollary 2 (norm leakage bound). If embeddings are not normalized, write $x_i = r_i u_i$ with $r_i = \lVert x_i \rVert$. Then $I(Y; T_{1:n}) \le I(Y; r_1, \dots, r_n)$. Only the norms can leak.

## What the theorem does not say

The theorem is silent about every setting below. Each is an experimental question, not a consequence of the theorem.

1. **Key reuse.** If $K_i = K_j$ for some $i \ne j$, Lemma 1 no longer gives a product law. For sign projections with a shared Haar matrix, $\Pr[\operatorname{sign}(q^\top x_i) \ne \operatorname{sign}(q^\top x_j)] = \theta_{ij}/\pi$ for each row $q$ (Goemans–Williamson), so the Hamming distance between shared-key records is an unbiased estimator of the angle between the sources. The shared-key control (pool size 1) leaks strongly, as expected. Recurring pools of size $k > 1$ with hidden slot labels are outside the theorem; their leakage is the subject of the key-pool experiments.
2. **Correlated keys.** Keys derived from a common seed with insufficient entropy, or keys that share a subspace.
3. **Non-invariant projection laws.** Structured, sparse, or learned projections; any transform whose law depends on the input direction.
4. **Deviations in the implementation from the idealized law.** See below.
5. **Side channels.** Key leakage, verification scores, score-based hill climbing, binary accept/reject oracles (Rahimi, Osadchy, Dunkelman, IJCB 2025).

## Implementation caveat: QR sign convention

Both `biohash.py` and `mlphash.py` draw a Gaussian matrix and take the Q factor of `numpy.linalg.qr`. Householder QR without sign correction does not produce a Haar-distributed Q (Mezzadri, 2007): the columns of Q are Haar up to a diagonal sign matrix that is correlated with the input. Under a rotation $x \mapsto Rx$ the projected vector transforms as $x^\top Q_{R^\top G} D$ for a data-dependent sign matrix $D$, so exact right-rotation invariance is not proven for the code as written. The observed chance-level results are consistent with invariance holding to within measurement precision, but the theorem strictly covers the sign-corrected construction ($Q \leftarrow Q \,\operatorname{diag}(\operatorname{sign}(\operatorname{diag} R))$). A sign-corrected variant should be added as a preregistered configuration before the theorem is cited as covering the exact implementation. Changing the default would alter every template and break reproduction of prior runs, so this is recorded as an open item rather than silently patched.

Update (2026-09-04): an opt-in `haar_sign_corrected` flag was added to `BioHashConfig` and run under preregistration (`configs/attacks/mobio_haar_corrected_key_pool.yaml`). Fresh-key 10-record top-1 was `2.64%` (chance `3.33%`), pool 1 `74.58%`, pool 5 `48.06%`, matching the default construction within seed noise. The theorem therefore covers a configuration that was actually executed, and the default construction behaves identically in the tested regime.

## Relation to prior work (checked 2026-09-04)

- Record multiplicity attacks were formalized for fuzzy vaults (Scheirer and Boult, 2007; Merkle and Tams, arXiv 1312.5225), where records share the enrolled biometric but not a random rotation. The present theorem concerns salted projection schemes, where the record law is source-independent under fresh keys.
- Learning-based and optimization-based preimage attacks on BioHashing, IoM, and related projection schemes (Nagar, Nandakumar, Jain, 2010; Lacharme, Cherrier, Rosenberger, 2013; Feng, Lim, Yuen, Pattern Recognition 2014; Dong, Jin, Teoh, BTAS 2019; Wang et al., 2020; Ghammam, Karabina, Lacharme, Atighehchi, 2019/2020; Durbet et al., 2021) assume the stolen-token scenario, i.e. a known transform. Our pool-size-1 condition is the unknown-but-shared-token analogue of that setting.
- Unlinkability frameworks (Gomez-Barrero et al., 2018) measure cross-key linkability of score distributions. They do not analyze a learning attacker with hidden recurring transform pools of varying cardinality.
- We found no prior statement of the fresh-key multiplicity invariance for fixed-norm deep embeddings, nor an empirical curve of key-blind leakage versus the number of recurring hidden transforms. Search coverage: arXiv API, Semantic Scholar API (rate-limited), DuckDuckGo. IEEE Xplore and Google Scholar full-text search were not available; the novelty claim must be rechecked against those before submission.
