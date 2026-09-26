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


@pytest.mark.parametrize("version", [2, 3])
@pytest.mark.parametrize("placement", ["return", "assignment", "helper", "nested"])
def test_branch_local_sinks_never_claim_cross_path_freshness(version, placement):
    from biometrics_ai.protection.source_analysis_v3 import analyse_source_v3
    from biometrics_ai.protection.biohash import generate_key

    analyze = analyse_source_v2 if version == 2 else analyse_source_v3
    call = "protect(embedding, derive(master, 'same', {index}), config)"
    prefix = ""
    if placement == "helper":
        prefix = "def finish(embedding, master, index, config):\n    return " + call.format(index="index") + "\n"
        call = "finish(embedding, master, {index}, config)"
    odd = call.format(index="record_id")
    even = call.format(index="record_id + 1")
    if placement == "assignment":
        body = f"if record_id % 2:\n    result = {odd}\nelse:\n    result = {even}\nreturn result"
    elif placement == "nested":
        body = f"if record_id >= 0:\n    if record_id % 2:\n        return {odd}\n    else:\n        return {even}\nelse:\n    return {odd}"
    else:
        body = f"if record_id % 2:\n    return {odd}\nelse:\n    return {even}"
    program = PREFIX + prefix + source(body).removeprefix(PREFIX)
    result = analyze(program, "implementation")
    assert result["decision"] == "unknown"
    assert not result["complete"]
    assert any("cross-path" in finding["message"] for finding in result["findings"])
    namespace = {}
    exec(program, namespace)
    namespace["protect"] = lambda embedding, key, config: key
    keys = [namespace["implementation"](None, 92591, record, None) for record in range(8)]
    assert len(set(keys)) == 4
    assert keys[0] == keys[1] == generate_key(92591, "same", 1)


@pytest.mark.parametrize("version", [2, 3])
def test_unsupported_branch_predicate_cannot_be_ignored(version):
    from biometrics_ai.protection.source_analysis_v3 import analyse_source_v3

    analyze = analyse_source_v2 if version == 2 else analyse_source_v3
    program = source(
        "if external_check(record_id):\n"
        "    unused = 1\n"
        "else:\n"
        "    unused = 2\n"
        "return protect(embedding, derive(master, 'x', record_id), config)"
    )
    result = analyze(program, "implementation")
    assert result["decision"] == "unknown"
    assert not result["complete"]


def test_branch_reuse_remains_flagged_but_incomplete():
    result = analyse_source_v2(source(
        "if record_id % 2:\n"
        "    return protect(embedding, 7, config)\n"
        "else:\n"
        "    return protect(embedding, 9, config)"
    ), "implementation")
    assert result["decision"] == "reuse"
    assert not result["complete"]
