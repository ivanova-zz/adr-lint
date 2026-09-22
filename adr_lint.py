#!/usr/bin/env python3

import re
import sys
from pathlib import Path


ADR_HEADER_RE = re.compile(r"^## ADR-(\d{4}) - (.+)$")
STATUS_RE = re.compile(r"^Status:\s*(\S+)\s*$")
DATE_RE = re.compile(r"^Date:\s*(\S+)\s*$")
SECTION_RE = re.compile(r"^###\s+(.+?)\s*$")
ADR_REFERENCE_RE = re.compile(r"\bADR-(\d{4})\b")

ALLOWED_STATUSES = {"proposed", "accepted", "superseded"}

REQUIRED_SECTIONS = [
    "Context",
    "Decision",
    "Alternatives",
    "Consequences",
]


def parse_adrs(text: str) -> list[dict]:
    adrs = []
    current = None

    for line_no, line in enumerate(text.splitlines(), start=1):
        header = ADR_HEADER_RE.match(line)

        if header:
            if current is not None:
                adrs.append(current)

            current = {
                "number": header.group(1),
                "title": header.group(2).strip(),
                "status": None,
                "date": None,
                "sections": [],
                "body_lines": [],
                "line": line_no,
            }
            continue

        if current is None:
            continue

        current["body_lines"].append(line)

        if current["status"] is None:
            match = STATUS_RE.match(line)
            if match:
                current["status"] = match.group(1)

        if current["date"] is None:
            match = DATE_RE.match(line)
            if match:
                current["date"] = match.group(1)

        match = SECTION_RE.match(line)
        if match:
            current["sections"].append(match.group(1))

    if current is not None:
        adrs.append(current)

    return adrs


def lint_adrs(adrs: list[dict]) -> list[tuple[str, str, str]]:
    problems = []

    seen = {}
    for adr in adrs:
        number = adr["number"]

        if number in seen:
            problems.append(
                (
                    "E1",
                    number,
                    f"ADR-{number} is duplicated",
                )
            )
        else:
            seen[number] = adr["line"]

    for adr in adrs:
        if adr["sections"] != REQUIRED_SECTIONS:
            actual = ", ".join(adr["sections"]) or "none"
            problems.append(
                (
                    "E2",
                    adr["number"],
                    "expected sections "
                    f"{', '.join(REQUIRED_SECTIONS)} in this order; "
                    f"found: {actual}",
                )
            )

    for adr in adrs:
        if adr["status"] not in ALLOWED_STATUSES:
            problems.append(
                (
                    "E3",
                    adr["number"],
                    f"invalid status {adr['status']!r}",
                )
            )

    existing_numbers = {adr["number"] for adr in adrs}

    for adr in adrs:
        body = "\n".join(adr["body_lines"])

        references = set(ADR_REFERENCE_RE.findall(body))

        for referenced_number in sorted(references):
            if referenced_number not in existing_numbers:
                problems.append(
                    (
                        "E4",
                        adr["number"],
                        f"reference ADR-{referenced_number} does not exist",
                    )
                )

    return problems


def print_index(adrs: list[dict]) -> None:
    print("ADR index")
    print("Number | Title | Status | Date")

    for adr in adrs:
        print(
            f"ADR-{adr['number']} | "
            f"{adr['title']} | "
            f"{adr['status'] or '-'} | "
            f"{adr['date'] or '-'}"
        )


def print_problems(problems: list[tuple[str, str, str]]) -> None:
    print()
    print("Problems")

    if not problems:
        print("No problems found.")
        return

    for code, number, message in problems:
        print(f"{code} | ADR-{number} | {message}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {Path(argv[0]).name} <DECISIONS.md>", file=sys.stderr)
        return 1

    path = Path(argv[1])

    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")

    adrs = parse_adrs(text)
    problems = lint_adrs(adrs)

    print_index(adrs)
    print_problems(problems)

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))