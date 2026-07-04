# Ultraplan operating model

Use this for end-to-end planning and implementation.

## Phase 0: Repository map

Collect only useful facts:

- Repository root and active branch.
- Package managers and build tools.
- Test, lint, typecheck, format, migration, and security commands.
- Existing `AGENTS.md`, `CLAUDE.md`, contribution docs, issue templates, PR templates, CI workflows, release docs, and architecture docs.
- Main modules, service boundaries, data stores, background jobs, public APIs, and risky integration points.
- Current Git status and untracked ignored coordination files.

Prefer commands such as:

```bash
git status --short --branch
find . -maxdepth 3 -name AGENTS.md -o -name CLAUDE.md -o -name package.json -o -name pyproject.toml -o -name go.mod -o -name Cargo.toml -o -name pom.xml -o -name build.gradle -o -name Makefile
```

Adjust commands to the platform and repository size.

## Phase 1: Mission and constraints

Write a one-page mission before decomposing work:

- Goal.
- Non-goals.
- User impact.
- System impact.
- Constraints.
- Assumptions.
- Success metrics.
- Failure modes.

If the mission cannot be written clearly, run the grill or create an assumptions lock.

## Phase 2: Milestone graph

Create milestones around reviewable outcomes, not calendar guesses.

Default sequence for complex engineering:

1. M0 Discovery and guardrails.
2. M1 Test harness and safety net.
3. M2 Core implementation.
4. M3 Integration, migration, and observability.
5. M4 Hardening, documentation, and rollout.

Change this sequence when the domain demands a different dependency structure.

Each milestone must include:

- Outcome.
- Issues included.
- Entry criteria.
- Exit criteria.
- Validation gates.
- Risks and mitigations.
- Rollback or stop criteria.

## Phase 3: Issue design

An issue is ready only if it can be implemented and reviewed independently.

Use this shape:

```markdown
# ISSUE-[number]: [title]

## Problem
[why this exists]

## Scope
[included work]

## Non-scope
[excluded work]

## Acceptance criteria
- [observable criterion]

## Technical approach
[implementation notes]

## Tests and coverage
[target and rationale]

## Dependencies
[upstream and downstream]

## Risk and rollback
[risk, mitigation, recovery]

## Branch
[type]/issue-[number]-[slug]

## MR/PR plan
[title and expected review notes]
```

Split an issue when it mixes domains, requires different reviewers, has separable rollout risk, or creates a diff too large for careful review.

## Phase 4: Branch and MR/PR sequence

Prefer one branch per issue. Use repository conventions if present. Otherwise use:

- `feat/issue-001-short-slug`
- `fix/issue-002-short-slug`
- `refactor/issue-003-short-slug`
- `test/issue-004-short-slug`
- `chore/issue-005-short-slug`

For stacked work, state the base branch and dependency clearly. Avoid unnecessary stacked branches when the project does not support them well.

MR/PR readiness requires:

- Focused diff.
- Acceptance criteria satisfied.
- Tests or explicit validation complete.
- Risk and rollback explained.
- No private `.ultraplan`, `.claude/agents/ultraplan-*`, `.codex/ultraplan`, or local `AGENTS.md` artifacts staged.

## Phase 5: Execution loop

For each issue:

1. Re-read the issue and current worklog.
2. Inspect affected code and existing tests.
3. Choose implementation path: TDD, characterization first, spike first, refactor first, or direct fix.
4. Implement the smallest coherent change.
5. Run focused checks.
6. Broaden validation based on risk.
7. Update worklog and issue status.
8. Prepare MR/PR text.

Do not continue piling changes onto a failing base. Stop and diagnose when tests fail in surprising ways.

## Phase 6: Review and hardening

Before final handoff, run a self-review:

- Does the change solve the stated issue and avoid hidden scope creep?
- Are new abstractions justified by repeated use or clear boundaries?
- Are errors, timeouts, nulls, empty states, permissions, and concurrency handled where relevant?
- Are logs useful and safe?
- Are tests meaningful and not overfit to implementation details?
- Can the change be rolled back or disabled?
- Are private coordination artifacts ignored and unstaged?

## Coverage selection guide

Choose and state a target for touched behavior:

- 90 percent or higher for auth, billing, security, data integrity, migrations, concurrency, financial logic, or irreversible side effects.
- 75 to 90 percent for core product logic, APIs, services, and reusable libraries.
- 50 to 75 percent for UI glue, thin adapters, feature flag wiring, and low-risk integration seams, provided higher-level checks cover user behavior.
- No numeric target for generated code or trivial config when checks provide little value.

Coverage is a risk control. Do not optimize for a number at the expense of useful tests.

## Private versus product files

Private coordination files belong to the local operating system and must be ignored:

- `.ultraplan/**`
- `.claude/agents/ultraplan-*.md`
- `.codex/ultraplan/**`
- local root `AGENTS.md` created only for the current agent session

Product files are the actual implementation and should be tracked:

- Source code.
- Tests.
- Migrations.
- Documentation intended for users or maintainers.
- CI and release automation intended to run for the project.

If unsure whether a file is private or product, decide based on whether reviewers need it for the delivered change. If reviewers do not need it, keep it private.
