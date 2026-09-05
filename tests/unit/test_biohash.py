import numpy as np
from biometrics_ai.protection import BioHashConfig, biohash, biohash_batch, correlated_biohash, generate_key


def test_key_generation_is_deterministic_and_scoped():
    assert generate_key(7, "train", 1) == generate_key(7, "train", 1)
    assert generate_key(7, "train", 1) != generate_key(7, "test", 1)


def test_biohash_repeatability_and_key_difference():
    vector = np.ones(16, dtype=np.float32)
    config = BioHashConfig(16, 8)
    assert np.array_equal(biohash(vector, 1, config), biohash(vector, 1, config))
    assert not np.array_equal(biohash(vector, 1, config), biohash(vector, 2, config))


def test_biohash_batch_matches_individual_templates():
    embeddings = np.eye(4, dtype=np.float32)
    config = BioHashConfig(4, 2)
    expected = np.stack([biohash(embedding, 11, config) for embedding in embeddings])
    assert np.array_equal(biohash_batch(embeddings, 11, config), expected)


def test_haar_sign_correction_is_orthonormal_and_direction_invariant():
    from biometrics_ai.protection.biohash import _orthonormal_projection

    projection = _orthonormal_projection(64, 16, "k", haar_sign_corrected=True)
    assert np.allclose(projection.T @ projection, np.eye(16), atol=1e-5)
    default = _orthonormal_projection(64, 16, "k", haar_sign_corrected=False)
    assert np.allclose(np.abs(default), np.abs(projection), atol=1e-6)

    # Empirical Lemma 1: the projected law of any fixed unit vector is the same up to Monte Carlo error.
    rng = np.random.default_rng(0)
    x, y = rng.normal(size=64), rng.normal(size=64)
    x, y = x / np.linalg.norm(x), y / np.linalg.norm(y)
    first = np.array([(x @ _orthonormal_projection(64, 16, f"a{i}", True) >= 0).mean() for i in range(400)])
    second = np.array([(y @ _orthonormal_projection(64, 16, f"a{i}", True) >= 0).mean() for i in range(400)])
    assert abs(first.mean() - 0.5) < 0.03 and abs(second.mean() - 0.5) < 0.03


def test_correlated_projection_shares_exact_prefix_and_remains_orthonormal():
    from biometrics_ai.protection.biohash import _correlated_orthonormal_projection

    first = _correlated_orthonormal_projection(32, 12, "shared", "private-a", 4)
    second = _correlated_orthonormal_projection(32, 12, "shared", "private-b", 4)

    assert np.array_equal(first[:, :4], second[:, :4])
    assert not np.array_equal(first[:, 4:], second[:, 4:])
    assert np.allclose(first.T @ first, np.eye(12), atol=1e-5)
    assert np.allclose(second.T @ second, np.eye(12), atol=1e-5)

    embedding = np.arange(32, dtype=np.float32)
    embedding /= np.linalg.norm(embedding)
    config = BioHashConfig(32, 12, haar_sign_corrected=True)
    one = correlated_biohash(embedding, "shared", "private-a", 4, config)
    two = correlated_biohash(embedding, "shared", "private-b", 4, config)
    assert np.array_equal(one[:4], two[:4])
