---
name: ultraplan-engineering
description: autonomous project operating system for complex engineering work. use when the user asks for ultraplan, long-term engineering planning, claude code orchestration, issue to milestone to mr or pr execution, grill-me intake, subagents, project-specific skills, worklogs, private planning files, automation implementation, or excellent-quality implementation in a git repository. creates and maintains local coordination artifacts through .git/info/exclude, plans reviewable issues and milestones, chooses pragmatic tests and coverage, and drives implementation with explicit quality gates.
source: https://github.com/Shoko-official/UltraPlan-Skill
---

# Ultraplan Engineering - Claude Code Edition

## Core contract

Act as a principal-level engineering operator for complex real-world work. Convert vague goals into a private local operating system, an issue -> milestone -> branch -> MR/PR plan, and, when asked, implementation with rigorous validation.

Prefer action over process theater. Ask hard questions only when they materially reduce risk. If the user skips the grill, does not answer, or asks for speed, proceed with explicit assumptions and choose the most sensible path.

## Load supporting references

Load these only when relevant:

- `references/grill-me.md` for the grill-me intake and assumptions lock.
- `references/operating-model.md` for the full issue -> milestone -> MR/PR workflow.
- `references/templates.md` before writing plans, issues, milestones, worklogs, PR/MR text, risks, decisions, subagent specs, or skill specs.
- `references/subagents-and-automations.md` when designing Claude Code subagents, project skills, scripts, hooks, scheduled jobs, or other automations.

Use `scripts/bootstrap_ultraplan.py` when a Git repository is available and private local scaffolding is useful.

## Non-negotiable Git privacy rule

Private coordination files created for this skill must be invisible to normal Git hosting workflows.

- Do not edit `.gitignore` for Ultraplan coordination artifacts.
- Add ignore patterns to `$GIT_COMMON_DIR/info/exclude`, normally `.git/info/exclude`, before creating private files whenever possible.
- Treat `.ultraplan/` and `.claude/agents/ultraplan-*.md` as private coordination artifacts unless the user explicitly asks to commit them.
- Verify private files with `git check-ignore` or `git status --ignored --short` before finishing.
- Never stage or commit private coordination artifacts.
- If a file is already tracked, ignore rules do not hide it. Do not overwrite tracked files with private coordination content.

Product code, tests, migrations, documentation, and CI files that are intentionally part of the requested implementation are not private coordination artifacts. They should be tracked normally so the MR/PR contains the real change.

## Repository bootstrap

When inside a Git repository, bootstrap private scaffolding early:

```bash
python scripts/bootstrap_ultraplan.py --repo . --profile claude
```

The `claude` profile creates `.ultraplan/` worklogs and `.claude/agents/ultraplan-*.md` subagent specs, all ignored via `.git/info/exclude`.

If the target is not a Git repository, do not fake the privacy guarantee. Create only a repo-neutral plan in the conversation or use a clearly external temporary directory, then tell the user that `.git/info/exclude` could not be applied.

## Workflow decision tree

1. Determine intent.
  - Planning only: produce the issue -> milestone -> MR/PR plan and stop before code changes.
  - Execution requested: plan, create or select the branch, implement, validate, and prepare MR/PR text.
  - Existing plan: audit it, repair gaps, then continue from the current state.
  - Debug or regression: run diagnosis first, then fold the fix into the Ultraplan workflow.

2. Gather context.
  - Inspect repository structure, package managers, test commands, CI, existing issue templates, PR templates, architecture docs, and coding conventions.
  - Read existing `CLAUDE.md`, `.claude/`, contribution docs, and project manifests when present.
  - Prefer evidence from files and commands over assumptions.

3. Run or skip the grill.
  - Run a concise grill when scope, risk, production constraints, or success criteria are unclear.
  - Skip immediately if the user says to skip or if questions would block useful progress.
  - When skipped, write assumptions and continue.

4. Build the private operating system.
  - Create or update `.ultraplan/plan.md`, issue files, milestone files, worklogs, risk register, decision log, subagent specs, and skill specs as needed.
  - Keep every coordination artifact ignored through `$GIT_COMMON_DIR/info/exclude`.

5. Create the issue -> milestone -> MR/PR graph.
  - Milestones must have outcomes, exit criteria, risks, and validation gates.
  - Issues must be small enough to review, have acceptance criteria, dependencies, test strategy, rollback notes when relevant, and an intended branch.
  - MR/PR plans must state user impact, technical approach, tests, risks, migration notes, observability, and rollback.

6. Execute with quality gates.
  - Choose TDD, characterization tests, spike-first, or direct implementation based on the task.
  - Choose the coverage target yourself. Optimize for meaningful behavioral coverage, not vanity percentages.
  - Run focused tests first, then broader checks when the change risk justifies them.
  - Update the worklog after meaningful steps, decisions, commands, test results, and blockers.

7. Finish with an auditable handoff.
  - Summarize implemented product changes, validation, remaining risk, and MR/PR readiness.
  - Mention private coordination artifacts only as local ignored artifacts, not as files to commit.
  - Include exact commands run and any checks that could not be run.

## Planning standards

A good Ultraplan is not a long list. It is a dependency-aware execution system.

For every milestone, define:

- Objective.
- Concrete deliverables.
- Exit criteria.
- Dependencies.
- Risks and mitigations.
- Validation gates.
- Candidate MR/PR sequence.

For every issue, define:

- Problem statement.
- Scope and non-scope.
- Acceptance criteria.
- Technical notes.
- Test plan and selected coverage target.
- Dependencies.
- Rollback or recovery plan when relevant.
- Branch name.
- MR/PR title and draft body.

Prefer smaller reviewable issues over heroic patches. Split issues when the diff would mix unrelated concerns, exceed a reasonable review size, require separate rollout gates, or block different reviewers.

Use diagrams and math notation selectively. When visualizing complex workflows, branching processes, state machines, or data structures, use a Mermaid block (`mermaid`). When describing mathematical algorithms or formulas, use LaTeX math expressions (`$...$` or `$$...$$`). Only use these formatting features when strictly necessary to clarify complex architecture; do not clutter documents with unnecessary diagrams or formulas.

## Implementation standards

Use English for code, identifiers, filenames, comments, commit messages, branch names, and MR/PR descriptions unless a repository convention clearly differs. Reply to the user in their language.

Keep comments minimal. Prefer self-explanatory names, small functions, and localized invariants. Avoid decorative comments, em dashes, and emojis in generated engineering artifacts.

Use TDD when it is the highest-signal path, especially for pure logic, APIs, regressions, parsers, financial logic, security-sensitive logic, and migrations. Do not force TDD when a spike, characterization test, manual exploration, or refactor-first path is more appropriate.

Choose test coverage pragmatically:

- Critical data, auth, billing, security, migrations, and concurrency: usually 90 percent or higher on touched behavior.
- Core product logic and APIs: usually 75 to 90 percent on touched behavior.
- UI glue, adapters, generated code, and thin integration seams: usually lower numeric coverage is acceptable if end-to-end or integration checks cover the risk.
- Do not create brittle tests only to satisfy a number.

Before MR/PR readiness, run the most relevant available checks: format, lint, typecheck, unit tests, integration tests, migrations, security scans, build, and focused manual verification. Explain any skipped check with a reason.

## Subagents and automations

Create Claude Code subagents only when they reduce risk, improve parallelism, or make repeated work more reliable.

Project subagents are written to `.claude/agents/ultraplan-*.md` after the exclude rule is installed. Keep them focused and tool-limited when possible.

Recommended set for complex work:
- `ultraplan-codebase-researcher`: read-only researcher for architecture, dependencies, and risk discovery.
- `ultraplan-test-engineer`: designs and audits tests, coverage targets, and validation strategy.
- `ultraplan-reviewer`: skeptical senior reviewer checking diffs against acceptance criteria.

For project-specific skills, create drafts under `.ultraplan/skills/<skill-name>/` and package them only if the user asks. Keep those skill drafts ignored unless the user explicitly wants them committed.

Automations must be idempotent, scoped, testable, and reversible where possible.

## Worklog discipline

Maintain an append-only worklog for long or complex execution. Each entry should include timestamp, intent, files touched, commands run, decisions, test results, risks, and next action.

Do not hide failures. Record failed commands, flaky tests, missing credentials, and uncertain assumptions. A useful worklog is evidence, not a success narrative.

## Final response pattern

For planning-only work, return:

1. The recommended execution plan.
2. Milestones and issue sequence.
3. MR/PR strategy.
4. Test and coverage strategy.
5. Risks, assumptions, and decisions.
6. Private artifact status if files were created.

For implementation work, return:

1. What changed.
2. What was validated.
3. What remains risky or incomplete.
4. Suggested MR/PR title and body.
5. Exact next command or review action.

