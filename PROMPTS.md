# Prompts

## 1

Read RULES.md, spec.md, README.md and DECISIONS.md.

Do not modify the three input files.

Summarize the required behavior of adr-lint and identify any ambiguities before writing code.

## 2

Implement the smallest Python CLI that satisfies spec.md.

Do not add extra flags, formats or configuration.

Add tests for parsing and E1-E4.

## 3

Run the test suite and run adr-lint against DECISIONS.md.

If anything fails, fix only the cause of the failure and show the resulting diff.