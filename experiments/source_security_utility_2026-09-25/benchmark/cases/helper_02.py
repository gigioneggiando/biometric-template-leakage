from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect, correlated_biohash
def helper(secret, sample):
    renamed = derive
    return renamed(secret, 'domain', derive(secret, 'hidden', sample) & 3)
def implementation(embedding, master, record_id, config):
    result = helper(master, record_id)
    return protect(embedding, result, config)
