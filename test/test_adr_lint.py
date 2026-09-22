from adr_lint import parse_adrs, lint_adrs, main


VALID_ADR = """\
## ADR-0001 - Use ClickHouse
Status: accepted
Date: 2026-04-11

### Context
Context text.

### Decision
Decision text.

### Alternatives
Alternative text.

### Consequences
Consequences text.
"""


def test_parse_adr():
    adrs = parse_adrs(VALID_ADR)

    assert len(adrs) == 1
    assert adrs[0]["number"] == "0001"
    assert adrs[0]["title"] == "Use ClickHouse"
    assert adrs[0]["status"] == "accepted"
    assert adrs[0]["date"] == "2026-04-11"


def test_valid_adr_has_no_problems():
    adrs = parse_adrs(VALID_ADR)

    assert lint_adrs(adrs) == []


def test_e1_duplicate_number():
    text = VALID_ADR + "\n" + VALID_ADR.replace(
        "Use ClickHouse",
        "Another decision",
    )

    problems = lint_adrs(parse_adrs(text))

    assert any(code == "E1" for code, _, _ in problems)


def test_e2_missing_or_wrong_sections():
    text = VALID_ADR.replace(
        "### Alternatives\nAlternative text.\n\n",
        "",
    )

    problems = lint_adrs(parse_adrs(text))

    assert any(code == "E2" for code, _, _ in problems)


def test_e3_invalid_status():
    text = VALID_ADR.replace(
        "Status: accepted",
        "Status: done",
    )

    problems = lint_adrs(parse_adrs(text))

    assert any(code == "E3" for code, _, _ in problems)


def test_e4_missing_reference():
    text = VALID_ADR.replace(
        "Decision text.",
        "Decision follows ADR-9999.",
    )

    problems = lint_adrs(parse_adrs(text))

    assert any(code == "E4" for code, _, _ in problems)


def test_e4_existing_reference_is_valid():
    second = VALID_ADR.replace(
        "ADR-0001",
        "ADR-0002",
    ).replace(
        "Use ClickHouse",
        "Use Kafka",
    ).replace(
        "Decision text.",
        "Based on ADR-0001.",
    )

    problems = lint_adrs(parse_adrs(VALID_ADR + "\n" + second))

    assert not any(code == "E4" for code, _, _ in problems)

def test_e2_wrong_section_order():
    text = VALID_ADR.replace(
        """### Decision
Decision text.

### Alternatives
Alternative text.
""",
        """### Alternatives
Alternative text.

### Decision
Decision text.
""",
    )

    problems = lint_adrs(parse_adrs(text))

    assert any(code == "E2" for code, _, _ in problems)

def test_e2_extra_section():
    text = VALID_ADR.replace(
        "### Consequences\nConsequences text.",
        """### Consequences
Consequences text.

### Notes
Extra text.""",
    )

    problems = lint_adrs(parse_adrs(text))

    assert any(code == "E2" for code, _, _ in problems)

def test_main_prints_index_and_problems(tmp_path, capsys):
    invalid_adr = VALID_ADR.replace(
        "Status: accepted",
        "Status: invalid",
    )

    path = tmp_path / "DECISIONS.md"
    path.write_text(invalid_adr, encoding="utf-8")

    exit_code = main(["adr_lint.py", str(path)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "ADR-0001 | Use ClickHouse | invalid | 2026-04-11" in captured.out
    assert "E3 | ADR-0001 | invalid status 'invalid'" in captured.out

def test_main_returns_1_for_missing_file():
    assert main(["adr_lint.py", "missing.md"]) == 1


def test_main_returns_1_for_wrong_argument_count():
    assert main(["adr_lint.py"]) == 1