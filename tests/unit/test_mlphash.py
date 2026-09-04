import numpy as np

from biometrics_ai.protection import MLPHashConfig, mlphash, mlphash_batch


def test_mlphash_is_deterministic_and_key_dependent():
    vector = np.linspace(-1.0, 1.0, 16, dtype=np.float32)
    config = MLPHashConfig(input_dim=16, output_dim=8, hidden_dim=32, hidden_layers=3)

    assert np.array_equal(mlphash(vector, 1, config), mlphash(vector, 1, config))
    assert not np.array_equal(mlphash(vector, 1, config), mlphash(vector, 2, config))


def test_mlphash_batch_matches_individual_templates():
    embeddings = np.eye(8, dtype=np.float32)
    config = MLPHashConfig(input_dim=8, output_dim=6, hidden_dim=16, hidden_layers=3)
    expected = np.stack([mlphash(embedding, 11, config) for embedding in embeddings])

    assert np.array_equal(mlphash_batch(embeddings, 11, config), expected)
    assert mlphash_batch(embeddings, 11, config).shape == (8, 6)