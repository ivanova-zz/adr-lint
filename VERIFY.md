# Verification

## CLI against DECISIONS.md

Command:

```text
$ python3 adr_lint.py DECISIONS.md
ADR index
Number | Title | Status | Date
ADR-0001 | Зберігати стан у файлах, а не в памʼяті процесу | accepted | 2026-01-14
ADR-0002 | Формат журналу рішень | accepted | 2026-01-20
ADR-0003 | Нумерація наскрізна, номери не перевикористовуються | accepted | 2026-02-02
ADR-0004 | Відмова від окремої бази для журналу | rejected | 2026-02-18
ADR-0005 | Валідатор запускається у CI | draft | 2026-03-05
ADR-0003 | Політика зберігання артефактів складання | accepted | 2026-03-19

Problems
E1 | ADR-0003 | ADR-0003 is duplicated
E2 | ADR-0003 | expected sections Context, Decision, Alternatives, Consequences in this order; found: Context, Decision, Consequences
E3 | ADR-0004 | invalid status 'rejected'
E3 | ADR-0005 | invalid status 'draft'
E4 | ADR-0005 | reference ADR-0011 does not exist
```
Command:

```text
$ echo $?
1
```

## Tests

Command:

```text
$ pytest -q
.......                                                                  [100%]
12 passed in 0.04s
```