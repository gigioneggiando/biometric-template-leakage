"""Frozen, manually labelled source cases for the 2026-09-25 holdout."""
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
        "case": "fresh_direct_record",
        "label": "fresh",
        "rationale": "The unique record identifier is the complete varying KDF input.",
        "source": implementation(
            "token = derive(master, 'face-template', record_id)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_affine_record",
        "label": "fresh",
        "rationale": "Five times the record identifier plus thirteen is injective over integers.",
        "source": implementation(
            "allocation = 5 * record_id + 13\n"
            "token = derive(master, 'face-template', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_nested_derivation",
        "label": "fresh",
        "rationale": "Both nested derivations preserve the record-dependent domain separation.",
        "source": implementation(
            "inner = derive(master, 'participant', record_id)\n"
            "token = derive(master, 'template', inner)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_reverse_affine",
        "label": "fresh",
        "rationale": "Subtracting a unique integer identifier from a constant remains injective.",
        "source": implementation(
            "allocation = 1000003 - record_id\n"
            "token = derive(master, 'face-template', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_helper_alias",
        "label": "fresh",
        "rationale": "The local helper and alias preserve the unique record identifier.",
        "source": HEADER
        + "def record_key(secret, item):\n"
        + "    local_derive = derive\n"
        + "    return local_derive(secret, 'record', 7 * item - 3)\n"
        + "def implementation(embedding, master, record_id, config):\n"
        + "    token = record_key(master, record_id)\n"
        + "    return protect(embedding, token, config)\n",
    },
    {
        "case": "fresh_correlated_zero_shared",
        "label": "fresh",
        "rationale": "The fixed key contributes zero output dimensions; all emitted dimensions use the record key.",
        "source": implementation(
            "unused = derive(master, 'unused', 0)\n"
            "private = derive(master, 'private', record_id)\n"
            "return correlated_biohash(embedding, unused, private, 0, config)"
        ),
    },
    {
        "case": "fresh_two_projection_blocks",
        "label": "fresh",
        "rationale": "Both concatenated projection blocks are derived from the unique record identifier.",
        "source": implementation(
            "first_key = derive(master, 'first', record_id)\n"
            "second_key = derive(master, 'second', record_id + 1009)\n"
            "first = basis(512, 16, first_key, True)\n"
            "second = basis(512, 48, second_key, True)\n"
            "matrix = np.concatenate([first, second], axis=1)\n"
            "return embedding @ matrix >= 0",
            "import numpy as np\n"
            "from biometrics_ai.protection.biohash import _orthonormal_projection as basis\n",
        ),
    },
    {
        "case": "fresh_single_projection",
        "label": "fresh",
        "rationale": "The only projection block uses a key derived injectively from the record identifier.",
        "source": implementation(
            "token = derive(master, 'projection', record_id)\n"
            "matrix = basis(512, 64, token, True)\n"
            "return embedding @ matrix >= 0",
            "from biometrics_ai.protection.biohash import _orthonormal_projection as basis\n",
        ),
    },
    {
        "case": "reuse_fixed_key",
        "label": "reuse",
        "rationale": "Every record receives the same constant-derived key.",
        "source": implementation(
            "token = derive(master, 'face-template', 17)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_modulo_pool",
        "label": "reuse",
        "rationale": "Modulo eight restricts all records to eight recurring key slots.",
        "source": implementation(
            "slot = record_id % 8\n"
            "token = derive(master, 'face-template', slot)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_mask_pool",
        "label": "reuse",
        "rationale": "The bit mask restricts all records to sixteen recurring key slots.",
        "source": implementation(
            "slot = record_id & 15\n"
            "token = derive(master, 'face-template', slot)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_zero_product",
        "label": "reuse",
        "rationale": "Multiplication by zero removes all record dependence.",
        "source": implementation(
            "slot = record_id * 0\n"
            "token = derive(master, 'face-template', slot)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_helper_pool",
        "label": "reuse",
        "rationale": "The helper maps every record into one of four recurring slots.",
        "source": HEADER
        + "def pooled_key(secret, item):\n"
        + "    return derive(secret, 'pool', (item + 11) % 4)\n"
        + "def implementation(embedding, master, record_id, config):\n"
        + "    token = pooled_key(master, record_id)\n"
        + "    return protect(embedding, token, config)\n",
    },
    {
        "case": "reuse_correlated_prefix",
        "label": "reuse",
        "rationale": "Sixteen output dimensions share a fixed projection even though the suffix is fresh.",
        "source": implementation(
            "shared = derive(master, 'shared', 0)\n"
            "private = derive(master, 'private', record_id)\n"
            "return correlated_biohash(embedding, shared, private, 16, config)"
        ),
    },
    {
        "case": "reuse_projection_prefix",
        "label": "reuse",
        "rationale": "The first concatenated projection block is fixed across all records.",
        "source": implementation(
            "shared_key = derive(master, 'first', 0)\n"
            "private_key = derive(master, 'second', record_id)\n"
            "first = basis(512, 16, shared_key, True)\n"
            "second = basis(512, 48, private_key, True)\n"
            "matrix = np.concatenate([first, second], axis=1)\n"
            "return embedding @ matrix >= 0",
            "import numpy as np\n"
            "from biometrics_ai.protection.biohash import _orthonormal_projection as basis\n",
        ),
    },
    {
        "case": "reuse_after_nested_derivation",
        "label": "reuse",
        "rationale": "Reducing an intermediate record-derived value modulo four creates a recurring pool.",
        "source": implementation(
            "intermediate = derive(master, 'participant', record_id)\n"
            "slot = intermediate % 4\n"
            "token = derive(master, 'template', slot)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_equivalent_branches",
        "label": "fresh",
        "rationale": "Both branches derive the key from the complete unique record identifier.",
        "source": implementation(
            "if record_id % 2:\n"
            "    token = derive(master, 'odd', record_id)\n"
            "else:\n"
            "    token = derive(master, 'even', record_id)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_keyword_arguments",
        "label": "fresh",
        "rationale": "Named arguments do not change the injective record-dependent derivation.",
        "source": implementation(
            "token = derive(master_key=master, domain='record', value=record_id)\n"
            "return protect(embedding=embedding, key=token, config=config)"
        ),
    },
    {
        "case": "fresh_tuple_selection",
        "label": "fresh",
        "rationale": "Selecting the first tuple element returns the unchanged unique record identifier.",
        "source": implementation(
            "inputs = (record_id, 0)\n"
            "token = derive(master, 'record', inputs[0])\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "fresh_bounded_loop",
        "label": "fresh",
        "rationale": "Adding and subtracting the same loop constants leaves the identifier unchanged.",
        "source": implementation(
            "allocation = record_id\n"
            "for offset in (3, 5):\n"
            "    allocation = allocation + offset\n"
            "    allocation = allocation - offset\n"
            "token = derive(master, 'record', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_branch_constants",
        "label": "reuse",
        "rationale": "The branch chooses between only two fixed keys.",
        "source": implementation(
            "if record_id % 2:\n"
            "    token = derive(master, 'pool', 0)\n"
            "else:\n"
            "    token = derive(master, 'pool', 1)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_floor_division",
        "label": "reuse",
        "rationale": "Consecutive record identifiers share the same quotient and therefore the same key.",
        "source": implementation(
            "slot = record_id // 4\n"
            "token = derive(master, 'group', slot)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_dictionary_pool",
        "label": "reuse",
        "rationale": "The dictionary lookup maps all records to one of four fixed key labels.",
        "source": implementation(
            "slots = {0: 19, 1: 23, 2: 29, 3: 31}\n"
            "allocation = slots[record_id % 4]\n"
            "token = derive(master, 'pool', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
    {
        "case": "reuse_self_subtraction",
        "label": "reuse",
        "rationale": "Subtracting the identifier from itself always produces zero.",
        "source": implementation(
            "allocation = record_id - record_id\n"
            "token = derive(master, 'pool', allocation)\n"
            "return protect(embedding, token, config)"
        ),
    },
]
