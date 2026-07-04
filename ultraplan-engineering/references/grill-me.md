# Grill-me intake

Use this file when the goal is ambiguous, high stakes, or likely to create expensive rework.

## Rules

Ask direct questions that expose weak assumptions. Do not ask generic preference questions. Limit the first grill to 6 to 12 questions unless the user explicitly asks for deeper interrogation.

If the user says to skip the grill, does not answer, or asks for autonomy, stop asking and proceed with an assumptions lock.

## Grill question bank

Choose questions from these categories.

### Outcome and scope

- What user, business, or operational outcome must improve?
- What is explicitly out of scope for this iteration?
- What would make the work a failure even if the code ships?
- Which tradeoff is acceptable: speed, correctness, maintainability, cost, or compatibility?

### Production constraints

- What environments must keep working during the change?
- Are there uptime, latency, data loss, or backward compatibility constraints?
- What existing behavior must not change?
- What rollout or rollback path is required?

### Architecture and data

- Which modules, services, schemas, queues, APIs, or jobs are likely involved?
- Are there migrations, data backfills, or compatibility windows?
- Are there invariants that must be preserved?
- Which integration is the least trusted?

### Security and compliance

- Does this touch auth, permissions, secrets, payments, PII, audit logs, or network boundaries?
- What abuse case should the design resist?
- Which logs or traces must not expose sensitive data?

### Testing and validation

- What is the strongest signal that the implementation works?
- Which existing tests are trusted, flaky, slow, or missing?
- What should be validated manually because automation would be misleading?
- What coverage target is justified by the risk?

### Team and review flow

- Who needs to review the MR/PR?
- Should this land as one MR/PR or a sequence?
- Are there release windows, feature flags, or dependency freezes?
- What documentation or changelog must accompany the code?

## Assumptions lock

When the grill is skipped or incomplete, write:

```markdown
# Assumptions lock

## Chosen assumptions

- [assumption and why it is reasonable]

## Risks created by these assumptions

- [risk and mitigation]

## Decisions made autonomously

- [decision and evidence]

## Reopen triggers

- [condition that would require replanning]
```

Do not wait for confirmation unless the next step is destructive, irreversible, credentialed, or explicitly requires user approval.
