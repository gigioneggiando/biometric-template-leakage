import random
from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect, correlated_biohash
def implementation(embedding, master, record_id, config):
    generator = random.Random(record_id)
    token = generator.randrange(4)
    return protect(embedding, token, config)
