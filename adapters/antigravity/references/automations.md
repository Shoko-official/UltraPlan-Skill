# Automations

Use this when the project benefits from repeatable local machinery.

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

## Project-specific skills

Create project-specific skill drafts under `.ultraplan/skills/<skill-name>/` when repeated project workflows deserve reusable instructions.

Each skill draft should include a `SKILL.md` with name and trigger description, a `references/` directory for project knowledge, and a `scripts/` directory only for deterministic helpers.

Keep skill drafts ignored unless the user explicitly wants them committed.
