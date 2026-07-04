# Subagents and automations

Use this when the project benefits from parallel specialists or repeatable local machinery.

## Subagent selection rule

Create a subagent only when one of these is true:

- It keeps noisy exploration out of the main context.
- It enforces a stricter tool boundary.
- It repeats across multiple issues or milestones.
- It allows safe parallel work.
- It provides a review perspective that the main agent is likely to miss.

Do not create a subagent just to make the plan look sophisticated.

## Default Claude Code subagents

When Claude Code project subagents are useful, create ignored files under `.claude/agents/` with names prefixed by `ultraplan-`.

Recommended set:

```markdown
---
name: ultraplan-codebase-researcher
description: Read-only codebase researcher for architecture, dependencies, tests, and risk discovery before implementation.
tools: Read, Grep, Glob, Bash
model: sonnet
---
You are a codebase research specialist. Map only the facts needed for the current issue. Return concise findings, relevant paths, commands discovered, risks, and open questions. Do not edit files.
```

```markdown
---
name: ultraplan-test-engineer
description: Designs and audits tests, coverage targets, fixtures, and validation strategy for high-risk engineering work.
tools: Read, Grep, Glob, Bash, Edit, Write
model: sonnet
---
You are a pragmatic test engineer. Prefer behavior tests over implementation tests. Choose coverage targets from risk. Add or update focused tests when useful. Avoid brittle tests that only satisfy a number.
```

```markdown
---
name: ultraplan-reviewer
description: Reviews diffs for correctness, maintainability, security, rollback, and MR/PR readiness after implementation.
tools: Read, Grep, Glob, Bash
model: sonnet
---
You are a skeptical senior reviewer. Inspect the diff against the issue and acceptance criteria. Report blockers, risky assumptions, missing tests, and simplifications. Do not edit files.
```

Add narrower agents only when the repo needs them, such as `ultraplan-security-reviewer`, `ultraplan-migration-planner`, `ultraplan-observability-engineer`, or `ultraplan-release-manager`.

## Codex local instruction artifacts

Use Codex-compatible Markdown instructions when helpful. Prefer a private ignored file under `.codex/ultraplan/AGENTS.md` or `.ultraplan/codex/AGENTS.md` for drafts.

Create root `AGENTS.md` only when all conditions are true:

- No tracked root `AGENTS.md` exists.
- The file is useful for the current Codex session.
- `/AGENTS.md` has been added to `$GIT_COMMON_DIR/info/exclude` first.
- The user has not asked to avoid root files.

Recommended sections:

```markdown
# AGENTS.md

## Project context
[short architecture and goal]

## Commands
- Install: [command]
- Test: [command]
- Lint: [command]
- Typecheck: [command]

## Code style
- English identifiers and comments.
- Minimal comments.
- Follow existing repository conventions.

## Testing
- Add or update tests for touched behavior.
- Choose coverage from risk.

## PR rules
- Keep diffs reviewable.
- Explain validation and rollback.
- Do not stage `.ultraplan/`, `.codex/ultraplan/`, or `.claude/agents/ultraplan-*`.
```

## Project-specific skills

Create project-specific skill drafts only when repeated project workflows deserve reusable instructions. Keep them under `.ultraplan/skills/<skill-name>/` unless the user explicitly wants a committed skill source.

Good candidates:

- Domain-specific test generation.
- Migration planning for the project's database.
- Release checklist generation.
- API compatibility review.
- Incident or regression diagnosis.
- Repository-specific frontend or backend conventions.

Each skill draft should include:

- `SKILL.md` with name and trigger description.
- `references/` for project knowledge.
- `scripts/` only for deterministic helpers.
- A short validation plan.

## Automation policy

Implement automation when it removes repeated manual risk or produces stronger evidence than prose.

Automation must have:

- Clear owner and trigger.
- Idempotent behavior.
- Dry-run mode when state changes are possible.
- Explicit input and output paths.
- Failure mode that stops safely.
- Minimal dependencies.
- Test or smoke check.

Private local automations belong under `.ultraplan/automations/` and must be ignored. Product automations, such as CI workflows or release scripts required by the feature, should be tracked normally and reviewed in the MR/PR.

## Common automation ideas

- Repository map generator.
- Test command detector.
- Coverage report summarizer.
- Worklog appender.
- Issue file generator.
- PR body renderer.
- Migration dry-run wrapper.
- Diff risk scanner.
- Dependency or API compatibility checker.

Do not schedule recurring work unless the environment provides a scheduling tool and the user explicitly asks for scheduling.
