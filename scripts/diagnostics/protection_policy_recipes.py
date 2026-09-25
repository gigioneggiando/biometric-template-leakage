"""Executable integration recipes for all analyzed protection sinks."""
from biometrics_ai.protection.biohash import biohash, generate_key
from biometrics_ai.protection.iomgrp import iomgrp_encoded
from biometrics_ai.protection.polyprotect import polyprotect


def pooled_key(master, record_id):
    assignment = generate_key(master, "assignment", record_id)
    slot = assignment % 4
    return generate_key(master, "transform", slot)


def fresh_key(master, record_id):
    return generate_key(master, "transform", record_id)


def biohash_recurring(embedding, master, record_id, config):
    token = pooled_key(master, record_id)
    return biohash(embedding, token, config)


def biohash_fresh(embedding, master, record_id, config):
    token = fresh_key(master, record_id)
    return biohash(embedding, token, config)


def iomgrp_recurring(embedding, master, record_id, config):
    token = pooled_key(master, record_id)
    return iomgrp_encoded(embedding, token, config)


def iomgrp_fresh(embedding, master, record_id, config):
    token = fresh_key(master, record_id)
    return iomgrp_encoded(embedding, token, config)


def polyprotect_recurring(embedding, master, record_id, config):
    token = pooled_key(master, record_id)
    return polyprotect(embedding, token, config)


def polyprotect_fresh(embedding, master, record_id, config):
    token = fresh_key(master, record_id)
    return polyprotect(embedding, token, config)
