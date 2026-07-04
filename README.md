# UltraPlan Skill

**Autonomous project operating system for complex engineering work.**

UltraPlan converts vague goals into a structured, dependency-aware execution system: issues -> milestones -> branches -> MR/PR -> ship. It works as a skill or rule for AI coding agents - Claude Code, OpenAI Codex, Antigravity, Cursor, and Windsurf - giving them a principled operating model for long-running, high-stakes engineering work.

---

## What it does

UltraPlan gives your AI agent a **principal-level engineering mindset**, not just code generation. When triggered, it:

- Runs a targeted intake ("grill") to surface hidden constraints and assumptions
- Maps the repository -- package managers, tests, CI, architecture, risky seams
- Decomposes the goal into a milestone graph with exit criteria and risk registers
- Designs small, reviewable issues with acceptance criteria, test plans, and rollback notes
- Executes with quality gates: TDD, characterization tests, or spike-first depending on risk
- Produces MR/PR-ready changes with worklog, validation summary, and reviewer notes
- Keeps all coordination artifacts private (`.ultraplan/`, `.claude/agents/ultraplan-*.md`) via `.git/info/exclude` -- never committed

---

## Compatibility

| Runtime | Supported | Adapter |
|---------|-----------|--------|
| [Claude Code](https://docs.anthropic.com/claude/docs/claude-code) | ✅ Full | `adapters/claude-code/` - subagents, project skills |
| [OpenAI Codex](https://platform.openai.com/docs/guides/codex) | ✅ Full | `adapters/codex/` - AGENTS.md instruction artifacts |
| [Antigravity](https://deepmind.google/technologies/antigravity/) | ✅ Full | `adapters/antigravity/` - auto-loaded from skills path |
| [Cursor](https://cursor.com) | ✅ Full | `adapters/cursor/ultraplan.mdc` - MDC project rule |
| [Windsurf](https://windsurf.com) | ✅ Full | `adapters/windsurf/ultraplan.md` - Cascade project rule |

---

## Skill structure

Each runtime has its own isolated adapter under `adapters/`:

```
adapters/
+-- antigravity/      SKILL.md + references/ + scripts/
+-- claude-code/      SKILL.md + references/ + scripts/
+-- codex/            SKILL.md + AGENTS.md + references/ + scripts/
+-- cursor/           ultraplan.mdc + INSTALL.md
+-- windsurf/         ultraplan.md + INSTALL.md

ultraplan-engineering/   (canonical source, Antigravity-compatible)
```

Every adapter's `SKILL.md` frontmatter includes `source: https://github.com/Shoko-official/UltraPlan-Skill` so the repo stays traceable wherever the skill is distributed.

---

## Installation

### Option 1 - Python installer (recommended, no security warnings)

Requires Python 3.8+ and git. No pip, no execution policy.

```bash
git clone https://github.com/Shoko-official/UltraPlan-Skill.git
python UltraPlan-Skill/install.py
```

`install.py` auto-detects which runtimes are installed and copies the right adapter to each. Use `--dry-run` to preview first:

```bash
python UltraPlan-Skill/install.py --dry-run
python UltraPlan-Skill/install.py --runtime claude-code,cursor
```

### Option 2 - Per-runtime GitHub release (download zip)

Each runtime has a dedicated release with a pre-packaged zip:

| Runtime | Release tag | What to do with the zip |
|---------|-------------|------------------------|
| Antigravity | [`v1.1.0-antigravity`](https://github.com/Shoko-official/UltraPlan-Skill/releases/tag/v1.1.0-antigravity) | Extract to `~/.gemini/config/skills/ultraplan-engineering/` |
| Claude Code | [`v1.1.0-claude-code`](https://github.com/Shoko-official/UltraPlan-Skill/releases/tag/v1.1.0-claude-code) | Extract to `~/.claude/skills/ultraplan-engineering/` |
| Codex | [`v1.1.0-codex`](https://github.com/Shoko-official/UltraPlan-Skill/releases/tag/v1.1.0-codex) | Extract to `~/.codex/skills/ultraplan-engineering/` |
| Cursor | [`v1.1.0-cursor`](https://github.com/Shoko-official/UltraPlan-Skill/releases/tag/v1.1.0-cursor) | Copy `ultraplan.mdc` to `.cursor/rules/` in your project |
| Windsurf | [`v1.1.0-windsurf`](https://github.com/Shoko-official/UltraPlan-Skill/releases/tag/v1.1.0-windsurf) | Copy `ultraplan.md` to `.windsurf/rules/` in your project |

### Option 3 - Let your AI self-install

Open `PROMPTS.md` and paste the prompt for your runtime into a chat.
The AI will clone the repo and install the right adapter automatically.

### Option 4 - Manual (no tools required)

| Runtime | Source path | Target path |
|---------|-------------|-------------|
| Antigravity | `adapters/antigravity/` | `~/.gemini/config/skills/ultraplan-engineering/` |
| Claude Code | `adapters/claude-code/` | `~/.claude/skills/ultraplan-engineering/` |
| Codex | `adapters/codex/` | `~/.codex/skills/ultraplan-engineering/` |
| Cursor | `adapters/cursor/ultraplan.mdc` | `.cursor/rules/ultraplan.mdc` (in project) |
| Windsurf | `adapters/windsurf/ultraplan.md` | `.windsurf/rules/ultraplan.md` (in project) |

---

## Quick start

Once installed, trigger UltraPlan by describing your engineering goal. The skill fires when you mention relevant keywords: `ultraplan`, `long-term planning`, `issue to milestone`, `MR/PR plan`, etc.

**Planning only:**
```
We need to add OAuth2 login to our API. Use ultraplan, planning only first,
no code changes yet. The API is Python/FastAPI, pytest, deployed on Kubernetes.
Strict backward compatibility required.
```

UltraPlan will ask 6-8 targeted questions (or skip if you say "just proceed"), map the repository, and produce a milestone graph with issues, branches, MR/PR sequence, and risk register.

**Execution:**
```
Approved. Execute M1 -- implement the auth middleware issue first, TDD approach.
```

---

## Bootstrap script

For Git repositories, each adapter ships `scripts/bootstrap_ultraplan.py`. Run it after install to create private local scaffolding:

```bash
# From the adapter directory, or anywhere if the script is on PATH:
python bootstrap_ultraplan.py --repo . --profile claude   # Claude Code
python bootstrap_ultraplan.py --repo . --profile codex    # Codex
python bootstrap_ultraplan.py --repo . --profile none     # Antigravity / any other
```

| Profile | What it creates |
|---------|----------------|
| `claude` | `.ultraplan/` + `.claude/agents/ultraplan-*.md` subagents |
| `codex` | `.ultraplan/` + `.codex/ultraplan/` instruction artifacts |
| `none` | `.ultraplan/` worklogs and plans only |

All artifacts are registered in `.git/info/exclude` and are never committed.

Cursor and Windsurf do not use the bootstrap script.

---

## Design principles

**Prefer action over process theater.** UltraPlan asks hard questions only when they materially reduce risk. If you skip the intake or ask for speed, it proceeds with explicit documented assumptions.

**Git privacy guarantee.** All coordination files (`.ultraplan/`, agent specs, worklogs) are invisible to Git. They live in your working copy only.

**Coverage is a risk control.** UltraPlan chooses coverage targets from risk -- 90%+ for auth/billing/security, 75-90% for core logic, lower for thin adapters. No vanity numbers.

**Worklog discipline.** Every execution maintains an append-only worklog: commands, decisions, failures, next actions. Failures are never hidden.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT -- see [LICENSE](LICENSE).
