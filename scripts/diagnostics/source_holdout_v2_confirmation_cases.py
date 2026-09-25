"""Frozen confirmation cases for source-analysis v2."""
from __future__ import annotations


HEADER = (
    "from biometrics_ai.protection.biohash import generate_key as derive, "
    "biohash as protect, correlated_biohash\n"
)


def implementation(body: str, extra: str = "") -> str:
    return HEADER + extra + (
        "def implementation(embedding, master, record_id, config):\n"
        + "\n".join(f"    {line}" for line in body.splitlines())
        + "\n"
    )


CASES = [
    {
        "case": "fresh_real_keywords",
        "label": "fresh",
        "rationale": "The real API keyword names bind the complete unique record identifier.",
        "source": implementation(
            "token = derive(master_seed=master, split='record', index=record_id)\n"
            "return protect(embedding=embedding, key=token, config=config)"
        ),
    },
    {
        "case": "fresh_list_selection",
        "label": "fresh",
        "rationale": "The fixed list index selects the unchanged record identifier.",
        "source": implementation(
            "candidates = [17, record_id, 19]\n"
            "token = derive(master, 'record', candidates[1])\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_dictionary_selection",
        "label": "fresh",
        "rationale": "The fixed dictionary key selects an injective affine record expression.",
        "source": implementation(
            "candidates = {0: record_id + 2, 1: 23}\n"
            "token = derive(master, 'record', candidates[0])\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_literal_loop",
        "label": "fresh",
        "rationale": "A finite sequence of constant additions preserves injectivity.",
        "source": implementation(
            "allocation = record_id\n"
            "for delta in (2, 4, 6):\n"
            "    allocation = allocation + delta\n"
            "token = derive(master, 'record', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_helper_keywords",
        "label": "fresh",
        "rationale": "Keyword binding into a local helper preserves the record identifier.",
        "source": HEADER
        + "def make_key(secret, item):\n"
        + "    return derive(secret, 'record', item * 9 + 4)\n"
        + "def implementation(embedding, master, record_id, config):\n"
        + "    token = make_key(secret=master, item=record_id)\n"
        + "    return protect(embedding, token, config)\n",
    },
    {
        "case": "fresh_default_config",
        "label": "fresh",
        "rationale": "Omitting the default protection configuration does not alter key provenance.",
        "source": implementation(
            "token = derive(master, 'record', record_id)\n"
            "return protect(embedding, token)"
        ),
    },
    {
        "case": "fresh_projection_keywords",
        "label": "fresh",
        "rationale": "The keyword-bound projection key depends injectively on the record identifier.",
        "source": implementation(
            "token = derive(master, 'projection', record_id)\n"
            "matrix = basis(input_dim=512, output_dim=64, key=token, haar_sign_corrected=True)\n"
            "return embedding @ matrix >= 0",
            "from biometrics_ai.protection.biohash import _orthonormal_projection as basis\n",
        ),
    },
    {
        "case": "fresh_floor_identity",
        "label": "fresh",
        "rationale": "Integer floor division by one is the identity function.",
        "source": implementation(
            "allocation = record_id // 1\n"
            "token = derive(master, 'record', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_negative_affine",
        "label": "fresh",
        "rationale": "Multiplication by negative three and a constant shift remain injective.",
        "source": implementation(
            "allocation = record_id * -3 - 7\n"
            "token = derive(master, 'record', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_projection_default_flag",
        "label": "fresh",
        "rationale": "The projection's default flag is fixed and its key remains record-injective.",
        "source": implementation(
            "token = derive(master, 'projection', record_id + 31)\n"
            "matrix = basis(512, 64, token)\n"
            "return embedding @ matrix >= 0",
            "from biometrics_ai.protection.biohash import _orthonormal_projection as basis\n",
        ),
    },
    {
        "case": "reuse_negative_floor_division",
        "label": "reuse",
        "rationale": "Floor division by negative three maps multiple identifiers to each quotient.",
        "source": implementation(
            "allocation = record_id // -3\n"
            "token = derive(master, 'group', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_fixed_dictionary_selection",
        "label": "reuse",
        "rationale": "The fixed lookup selects the same key label for every record.",
        "source": implementation(
            "slots = {0: 5, 1: 7}\n"
            "token = derive(master, 'pool', slots[0])\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_bounded_dictionary_selection",
        "label": "reuse",
        "rationale": "The bounded lookup selects one of three recurring fixed labels.",
        "source": implementation(
            "slots = {0: 5, 1: 7, 2: 11}\n"
            "token = derive(master, 'pool', slots[record_id % 3])\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_fixed_list_selection",
        "label": "reuse",
        "rationale": "The fixed list selection is independent of the record identifier.",
        "source": implementation(
            "slots = [13, 17]\n"
            "token = derive(master, 'pool', slots[0])\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_helper_keywords",
        "label": "reuse",
        "rationale": "The helper's modulo operation restricts allocation to five recurring slots.",
        "source": HEADER
        + "def make_key(secret, item):\n"
        + "    return derive(secret, 'pool', item % 5)\n"
        + "def implementation(embedding, master, record_id, config):\n"
        + "    token = make_key(secret=master, item=record_id)\n"
        + "    return protect(embedding, token, config)\n",
    },
    {
        "case": "reuse_correlated_keywords",
        "label": "reuse",
        "rationale": "Eight emitted dimensions use a fixed shared projection key.",
        "source": implementation(
            "shared = derive(master, 'shared', 0)\n"
            "private = derive(master, 'private', record_id)\n"
            "return correlated_biohash(embedding=embedding, shared_key=shared, private_key=private, shared_dimensions=8, config=config)"
        ),
    },
    {
        "case": "reuse_projection_keywords",
        "label": "reuse",
        "rationale": "The keyword-bound projection key is fixed across records.",
        "source": implementation(
            "token = derive(master, 'projection', 0)\n"
            "matrix = basis(input_dim=512, output_dim=64, key=token)\n"
            "return embedding @ matrix >= 0",
            "from biometrics_ai.protection.biohash import _orthonormal_projection as basis\n",
        ),
    },
    {
        "case": "reuse_nested_self_subtraction",
        "label": "reuse",
        "rationale": "Subtracting the same affine expression from itself always yields zero.",
        "source": implementation(
            "allocation = (record_id + 1) - (record_id + 1)\n"
            "token = derive(master, 'pool', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_loop_then_modulo",
        "label": "reuse",
        "rationale": "The loop preserves dependence, but the final modulo restricts it to four slots.",
        "source": implementation(
            "allocation = record_id\n"
            "for delta in (2, 3):\n"
            "    allocation = allocation + delta\n"
            "slot = allocation % 4\n"
            "token = derive(master, 'pool', slot)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_branch_mixed_pools",
        "label": "reuse",
        "rationale": "Both control-flow paths select from finite recurring pools.",
        "source": implementation(
            "if record_id % 2:\n"
            "    token = derive(master, 'odd-pool', record_id % 3)\n"
            "else:\n"
            "    token = derive(master, 'even-pool', record_id % 5)\n"
            "return protect(embedding, token, config)"
        ),
    },
]
