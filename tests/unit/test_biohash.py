import numpy as np
from biometrics_ai.protection import BioHashConfig, biohash, generate_key


def test_key_generation_is_deterministic_and_scoped():
    assert generate_key(7, "train", 1) == generate_key(7, "train", 1)
    assert generate_key(7, "train", 1) != generate_key(7, "test", 1)


def test_biohash_repeatability_and_key_difference():
    vector = np.ones(16, dtype=np.float32)
    config = BioHashConfig(16, 8)
    assert np.array_equal(biohash(vector, 1, config), biohash(vector, 1, config))
    assert not np.array_equal(biohash(vector, 1, config), biohash(vector, 2, config))
