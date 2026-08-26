import numpy as np
from biometrics_ai.protection import BioHashConfig, biohash, biohash_batch, generate_key


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
