import pytest

from biometrics_ai.protection.source_analysis_v2 import analyse_source_v2


PREFIX = "from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect\n"


def source(body):
    return PREFIX + "def implementation(embedding, master, record_id, config):\n" + "\n".join(
        f"    {line}" for line in body.splitlines()
    ) + "\n"


@pytest.mark.parametrize(
    "body, expected",
    [
        ("value = record_id - record_id\ntoken = derive(master, 'x', value)\nreturn protect(embedding, token, config)", "reuse"),
        ("value = record_id // 4\ntoken = derive(master, 'x', value)\nreturn protect(embedding, token, config)", "reuse"),
        ("pair = (record_id, 0)\ntoken = derive(master, 'x', pair[0])\nreturn protect(embedding, token, config)", "conditional_fresh"),
        ("slots = {0: 7, 1: 11}\ntoken = derive(master, 'x', slots[record_id % 2])\nreturn protect(embedding, token, config)", "reuse"),
    ],
)
def test_v2_adds_arithmetic_and_container_rules(body, expected):
    assert analyse_source_v2(source(body), "implementation")["decision"] == expected


def test_v2_binds_real_keyword_names_and_rejects_invented_names():
    valid = source(
        "token = derive(master_seed=master, split='x', index=record_id)\n"
        "return protect(embedding=embedding, key=token, config=config)"
    )
    invalid = source(
        "token = derive(master_key=master, domain='x', value=record_id)\n"
        "return protect(embedding=embedding, key=token, config=config)"
    )
    assert analyse_source_v2(valid, "implementation")["decision"] == "conditional_fresh"
    assert analyse_source_v2(invalid, "implementation")["decision"] == "unknown"


def test_v2_unrolls_only_literal_bounded_loops():
    program = source(
        "allocation = record_id\n"
        "for offset in (3, 5):\n"
        "    allocation = allocation + offset\n"
        "    allocation = allocation - offset\n"
        "token = derive(master, 'x', allocation)\n"
        "return protect(embedding, token, config)"
    )
    assert analyse_source_v2(program, "implementation")["decision"] == "conditional_fresh"


def test_v2_branch_join_detects_reuse_but_does_not_assume_cross_path_injectivity():
    reuse = source(
        "if record_id % 2:\n"
        "    token = derive(master, 'pool', 0)\n"
        "else:\n"
        "    token = derive(master, 'pool', 1)\n"
        "return protect(embedding, token, config)"
    )
    unresolved_fresh = source(
        "if record_id % 2:\n"
        "    token = derive(master, 'odd', record_id)\n"
        "else:\n"
        "    token = derive(master, 'even', record_id)\n"
        "return protect(embedding, token, config)"
    )
    assert analyse_source_v2(reuse, "implementation")["decision"] == "reuse"
    assert analyse_source_v2(unresolved_fresh, "implementation")["decision"] == "unknown"
