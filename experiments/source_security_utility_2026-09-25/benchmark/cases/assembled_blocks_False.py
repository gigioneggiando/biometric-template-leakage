from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect, correlated_biohash
import numpy as np
from biometrics_ai.protection.biohash import _orthonormal_projection as basis
def implementation(embedding, master, record_id, config):
    first = basis(512, 16, derive(master, 'first', record_id), True)
    second = basis(512, 48, derive(master, 'second', record_id), True)
    assembled = np.concatenate([first, second], axis=1)
    return embedding @ assembled >= 0
