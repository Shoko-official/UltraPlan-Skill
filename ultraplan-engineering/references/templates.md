# Ultraplan templates

Use these templates as defaults. Adapt structure when the project has stronger conventions.

## Plan overview

```markdown
# Ultraplan: [project or goal]

## Mission
[one paragraph]

## Non-goals
- [non-goal]

## Assumptions
- [assumption]

## Milestone graph
| Milestone | Outcome | Issues | Exit gate |
| --- | --- | --- | --- |
| M0 | [outcome] | ISSUE-001 | [gate] |

## MR/PR sequence
| MR/PR | Branch | Base | Issues | Purpose |
| --- | --- | --- | --- | --- |
| PR-001 | feat/issue-001-slug | main | ISSUE-001 | [purpose] |

## Validation strategy
[tests, coverage, manual checks]

## Risks
| Risk | Impact | Mitigation | Reopen trigger |
| --- | --- | --- | --- |
```

## Milestone

```markdown
# M[number]: [title]

## Outcome
[deliverable]

## Included issues
- ISSUE-[number]: [title]

## Entry criteria
- [criterion]

## Exit criteria
- [criterion]

## Validation gates
- [check]

## Risks and mitigations
- [risk]: [mitigation]

## MR/PR sequence
- [branch] -> [target]
```

## Issue

```markdown
# ISSUE-[number]: [title]

## Problem
[problem]

## Scope
- [scope]

## Non-scope
- [non-scope]

## Acceptance criteria
- [observable result]

## Technical approach
[approach]

## Tests and coverage
Target: [percentage or qualitative target]
Rationale: [why]
Checks:
- [check]

## Dependencies
- [dependency]

## Risk and rollback
Risk: [risk]
Mitigation: [mitigation]
Rollback: [rollback]

## Branch
[branch]

## MR/PR draft
Title: [title]
Body: [summary]
```

## Worklog entry

```markdown
## [YYYY-MM-DD HH:MM TZ] [short intent]

### Context
[what was known]

### Actions
- [action]

### Files touched
- [path]: [reason]

### Commands
```bash
[command]
```

### Results
- [result]

### Decisions
- [decision and rationale]

### Risks or blockers
- [risk or blocker]

### Next
- [next action]
```

## Decision record

```markdown
# ADR-[number]: [decision]

## Status
proposed | accepted | superseded

## Context
[forces and constraints]

## Decision
[choice]

## Consequences
Positive:
- [effect]

Negative:
- [effect]

## Revisit when
[trigger]
```

## MR/PR body

```markdown
## Summary
- [change]

## Issue
Closes ISSUE-[number]

## Approach
[technical approach]

## Validation
- [command and result]

## Risk
[risk level and reason]

## Rollback
[rollback plan]

## Notes for reviewers
- [focus area]
```

## Automation brief

```markdown
# Automation: [name]

## Purpose
[why automation exists]

## Trigger
[manual, hook, CI, schedule, or command]

## Inputs
- [input]

## Outputs
- [output]

## Safety
- Idempotency: [how]
- Dry run: [yes/no and how]
- Rollback: [how]
- Secrets: [none or source]

## Validation
- [test or check]
```

## Subagent brief

```markdown
# Subagent: [name]

## Use when
[delegation trigger]

## Inputs
- [input]

## Outputs
- [output]

## Tools
- [allowed tools]

## Constraints
- [constraint]

## Done when
- [criterion]
```

## Project skill brief

```markdown
# Skill: [name]

## Trigger
[when it should be used]

## Reusable workflow
[steps]

## Resources needed
- scripts: [deterministic helpers]
- references: [domain knowledge]
- assets: [templates or files]

## Validation
[how to test the skill]
```
