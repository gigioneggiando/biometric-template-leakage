"""Executable policy recipes, analyzed as source rather than YAML condition names."""
from biometrics_ai.protection.biohash import biohash, correlated_biohash, generate_key


def pool_key(master, record_id):
    assigned = generate_key(master, "assignment", record_id)
    slot = assigned % 4
    return generate_key(master, "transform", slot)


def fresh_key(master, record_id):
    return generate_key(master, "transform", record_id)


def common_key(master):
    return generate_key(master, "common", 0)


def recurring(embedding, master, record_id, config):
    token = pool_key(master, record_id)
    return biohash(embedding, token, config)


def partial(embedding, master, record_id, config):
    shared = common_key(master)
    private = fresh_key(master, record_id)
    return correlated_biohash(embedding, shared, private, 16, config)


def separated(embedding, master, record_id, config):
    token = fresh_key(master, record_id)
    return biohash(embedding, token, config)