# Changelog

All notable changes to UltraPlan-Skill are documented here.

## [1.1.0] - 2026-07-04

### Added

**Runtime adapters** (five isolated variants - zero cross-contamination)
- `adapters/antigravity/` - bootstrap `--profile none`, private artifacts `.ultraplan/` only
- `adapters/claude-code/` - bootstrap `--profile claude`, private artifacts `.ultraplan/` + `.claude/agents/ultraplan-*.md`
- `adapters/codex/` - bootstrap `--profile codex`, private artifacts `.ultraplan/` + `.codex/ultraplan/` + optional root `AGENTS.md`
- `adapters/cursor/ultraplan.mdc` - Cursor MDC format, `alwaysApply: true`, no bootstrap
- `adapters/windsurf/ultraplan.md` - Windsurf rules format, no bootstrap
- `source:` field in every adapter frontmatter linking back to this repo

**Distribution**
- `install.py` - cross-platform Python installer (stdlib only, no pip, no execution policy)
- `install.ps1` rewritten - thin wrapper around `install.py`, no `irm | iex`
- `install.sh` rewritten - thin wrapper around `install.py`, no `curl | bash`
- `PROMPTS.md` - one self-install prompt per runtime (Antigravity, Claude Code, Codex, Cursor, Windsurf, Universal)
- Per-runtime GitHub releases: `v1.1.0-antigravity`, `v1.1.0-claude-code`, `v1.1.0-codex`, `v1.1.0-cursor`, `v1.1.0-windsurf`
- README install section rewritten: 4 options, all 5 runtimes covered

---

## [1.0.0] - 2026-07-04


Initial public release.

### Added

**Core skill**
- `ultraplan-engineering/SKILL.md`: Main skill definition with frontmatter trigger fields (`name`, `description`) and full operating instructions for autonomous project engineering
- `ultraplan-engineering/agents/openai.yaml`: OpenAI Codex agent spec for the UltraPlan skill

**Reference library**
- `ultraplan-engineering/references/grill-me.md`: Targeted intake questionnaire (6-12 questions) and assumptions lock template for when intake is skipped
- `ultraplan-engineering/references/operating-model.md`: Complete 6-phase operating model -- repository map, mission, milestone graph, issue design, branch/MR/PR sequence, execution loop, review and hardening, coverage selection guide
- `ultraplan-engineering/references/subagents-and-automations.md`: Subagent selection rules, default Claude Code subagent templates (researcher, test engineer, reviewer), Codex instruction artifact policy, project-specific skill policy, automation policy
- `ultraplan-engineering/references/templates.md`: Ready-to-use templates for plans, milestones, issues, worklogs, decision records, MR/PR bodies, automation briefs, subagent briefs, and project skill briefs

**Bootstrap script**
- `ultraplan-engineering/scripts/bootstrap_ultraplan.py`: Python script that creates private local scaffolding in a Git repository (`.ultraplan/`, Claude Code subagents, Codex instruction artifacts) and registers all private files in `.git/info/exclude`

**Installation**
- `install.ps1`: Windows PowerShell installer -- supports `--DryRun` and `--Runtime` flags
- `install.sh`: macOS / Linux bash installer -- supports `--dry-run` and `--runtime` flags

**Repository**
- `README.md`: Full documentation -- what UltraPlan is, compatibility table, skill structure, installation, quick-start, bootstrap usage, design principles
- `LICENSE`: MIT license
- `CONTRIBUTING.md`: Contribution guide with skill file conventions
- `.gitattributes`: Line-ending normalization (LF)
