from biometrics_ai.data.synthetic import SyntheticConfig, build_sets


def test_synthetic_sets_are_identity_and_key_disjoint():
    config = SyntheticConfig(identities=20, samples_per_identity=10, embedding_dim=16, template_dim=8)
    train = build_sets(config, "train", 5, "train")
    test = build_sets(config, "test", 5, "test")
    assert not set(train["identity_ids"]) & set(test["identity_ids"])
    assert not set(train["key_ids"].flat) & set(test["key_ids"].flat)
