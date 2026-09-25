from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect, correlated_biohash
def implementation(embedding, master, record_id, config):
    allocation = 0
    token = derive(master, 'protection', allocation)
    return protect(embedding, token, config)
