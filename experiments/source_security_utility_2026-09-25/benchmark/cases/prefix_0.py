from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect, correlated_biohash
def implementation(embedding, master, record_id, config):
    common = derive(master, 'common', 0)
    private = derive(master, 'private', record_id)
    return correlated_biohash(embedding, common, private, 0, config)
