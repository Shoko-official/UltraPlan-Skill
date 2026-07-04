# UltraPlan Skill

**Autonomous project operating system for complex engineering work.**

UltraPlan converts vague goals into a structured, dependency-aware execution system: issues -> milestones -> branches -> MR/PR -> ship. It works as a skill for AI coding agents -- Claude Code, OpenAI Codex, and Antigravity -- giving them a principled operating model for long-running, high-stakes engineering work.

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

| Runtime | Supported | Notes |
|---------|-----------|-------|
| [Claude Code](https://docs.anthropic.com/claude/docs/claude-code) | Yes | Full support -- subagents, hooks, project skills |
| [OpenAI Codex](https://platform.openai.com/docs/guides/codex) | Yes | Via `agents/openai.yaml` spec |
| [Antigravity](https://deepmind.google/technologies/antigravity/) | Yes | Loaded automatically from `~/.gemini/config/skills/` |
| Other agents | Partial | Use `SKILL.md` directly as a system-prompt extension |

---

## Skill structure

```
ultraplan-engineering/
+-- SKILL.md                          # Main skill definition (frontmatter + instructions)
+-- agents/
|   +-- openai.yaml                   # OpenAI Codex agent spec
+-- references/
|   +-- grill-me.md                   # Intake questionnaire and assumptions lock
|   +-- operating-model.md            # Full issue -> milestone -> MR/PR workflow
|   +-- subagents-and-automations.md  # Subagent design and automation policy
|   +-- templates.md                  # Plan, issue, worklog, MR/PR, ADR templates
+-- scripts/
    +-- bootstrap_ultraplan.py        # Bootstraps private local scaffolding in a git repo
```

---

## Installation

### One command (recommended)

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/install.sh | bash
```

Both scripts detect which runtimes are present and install to the correct paths. Use `--dry-run` to preview without copying.

### Manual installation

Clone or download this repo, then copy the `ultraplan-engineering/` directory to your runtime's skills directory:

| Runtime | Target path |
|---------|-------------|
| Claude Code | `~/.claude/skills/ultraplan-engineering/` |
| Antigravity | `~/.gemini/config/skills/ultraplan-engineering/` |
| Codex | `~/.codex/skills/ultraplan-engineering/` |

**Windows (Claude Code):**
```powershell
Copy-Item -Recurse .\ultraplan-engineering\ "$env:USERPROFILE\.claude\skills\ultraplan-engineering\"
```

**macOS / Linux (Antigravity):**
```bash
cp -r ./ultraplan-engineering/ ~/.gemini/config/skills/ultraplan-engineering/
```

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

For Git repositories, run the bootstrap script to set up private local scaffolding:

```bash
python scripts/bootstrap_ultraplan.py --repo . --profile both
```

Profiles:

| Profile | What it creates |
|---------|----------------|
| `both` | Claude Code subagents + Codex instruction artifacts |
| `claude` | Claude Code subagents only |
| `codex` | Codex instruction artifacts only |
| `none` | `.ultraplan/` worklogs and plans only |

Private artifacts are registered in `.git/info/exclude` and are never committed.

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
