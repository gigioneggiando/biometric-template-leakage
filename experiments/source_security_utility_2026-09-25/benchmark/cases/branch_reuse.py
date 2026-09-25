from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect, correlated_biohash
def implementation(embedding, master, record_id, config):
    if record_id % 2:
        return protect(embedding, 3, config)
    return protect(embedding, 7, config)
