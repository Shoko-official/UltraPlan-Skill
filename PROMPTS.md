# UltraPlan - Self-Install Prompts

Copy the prompt for your AI runtime and paste it into a chat.
The AI will install UltraPlan itself, no manual steps needed.

Source: https://github.com/Shoko-official/UltraPlan-Skill

---

## Antigravity (Google DeepMind)

```
Install the UltraPlan skill for Antigravity.

Steps:
1. Clone https://github.com/Shoko-official/UltraPlan-Skill into a temp directory.
2. Copy the adapters/antigravity/ directory to ~/.gemini/config/skills/ultraplan-engineering/
   (create the directory if it does not exist).
3. Confirm the install by listing ~/.gemini/config/skills/ultraplan-engineering/ and
   showing that SKILL.md is present.
4. Delete the temp clone.

Do not install any other adapter. Do not touch .claude/, .codex/, or any path
that is not ~/.gemini/config/skills/.
```

---

## Claude Code (Anthropic)

```
Install the UltraPlan skill for Claude Code.

Steps:
1. Clone https://github.com/Shoko-official/UltraPlan-Skill into a temp directory.
2. Copy the adapters/claude-code/ directory to ~/.claude/skills/ultraplan-engineering/
   (create the directory if it does not exist).
3. Confirm the install by listing ~/.claude/skills/ultraplan-engineering/ and
   showing that SKILL.md is present.
4. Delete the temp clone.

Do not install any other adapter. Do not touch .codex/, .gemini/, or any path
that is not ~/.claude/skills/.
```

---

## Codex (OpenAI)

```
Install the UltraPlan skill for Codex.

Steps:
1. Clone https://github.com/Shoko-official/UltraPlan-Skill into a temp directory.
2. Copy the adapters/codex/ directory to ~/.codex/skills/ultraplan-engineering/
   (create the directory if it does not exist).
3. Confirm the install by listing ~/.codex/skills/ultraplan-engineering/ and
   showing that SKILL.md is present.
4. Delete the temp clone.

Do not install any other adapter. Do not touch .claude/, .gemini/, or any path
that is not ~/.codex/skills/.
```

---

## Cursor

```
Install the UltraPlan rule for this Cursor project.

Steps:
1. Clone https://github.com/Shoko-official/UltraPlan-Skill into a temp directory.
2. Create .cursor/rules/ in the current project root if it does not exist.
3. Copy adapters/cursor/ultraplan.mdc to .cursor/rules/ultraplan.mdc.
4. Confirm the file is present and show the first 5 lines.
5. Delete the temp clone.

Do not create any files outside the current project. Do not touch .claude/,
.codex/, or .gemini/ paths.
```

---

## Windsurf

```
Install the UltraPlan rule for this Windsurf project.

Steps:
1. Clone https://github.com/Shoko-official/UltraPlan-Skill into a temp directory.
2. Create .windsurf/rules/ in the current project root if it does not exist.
3. Copy adapters/windsurf/ultraplan.md to .windsurf/rules/ultraplan.md.
4. Confirm the file is present and show the first 5 lines.
5. Delete the temp clone.

Do not create any files outside the current project. Do not touch .claude/,
.codex/, or .gemini/ paths.
```

---

## Universal (any AI, any runtime)

Use this when you are not sure which of the above applies, or when your AI
can detect runtimes automatically.

```
Install the UltraPlan skill from https://github.com/Shoko-official/UltraPlan-Skill.

Steps:
1. Clone the repo to a temp directory.
2. Run: python install.py --dry-run
   This will detect which AI runtimes are installed on this machine and show
   the target paths without copying anything.
3. If the output looks correct, run: python install.py
4. Confirm which runtimes were installed and delete the temp clone.

If Python is not available, check the adapters/ directory and manually copy
the folder for your runtime to the correct path:
 - Antigravity:  adapters/antigravity/ -> ~/.gemini/config/skills/ultraplan-engineering/
 - Claude Code:  adapters/claude-code/ -> ~/.claude/skills/ultraplan-engineering/
 - Codex:        adapters/codex/       -> ~/.codex/skills/ultraplan-engineering/
 - Cursor:       adapters/cursor/ultraplan.mdc -> .cursor/rules/ultraplan.mdc (in project)
 - Windsurf:     adapters/windsurf/ultraplan.md -> .windsurf/rules/ultraplan.md (in project)
```

---

## Notes

- Each prompt installs **only** the adapter for its own runtime.
- The `source:` field in every adapter points back to this repo, so anyone who
  receives a copy of the skill can find updates.
- To update: re-run the same prompt, or `git pull` the repo and re-run `install.py`.
