# Decisions

## Validation of ADR sections

### Context

The specification says that every ADR must contain exactly four level-three sections and lists them in a required order. E2 is described more briefly as checking whether all four required sections are present.

### Decision

Treat E2 as requiring exactly these four level-three sections and in exactly this order: Context, Decision, Alternatives, Consequences. Additional level-three sections also trigger E2.

### Alternatives

One option was to check only that the four required section names occur somewhere, ignoring order and additional sections.

### Consequences

The implementation follows the stricter wording of the format section. ADRs with reordered or additional level-three sections are reported as E2.