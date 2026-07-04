# Installing UltraPlan for Cursor

Source: https://github.com/Shoko-official/UltraPlan-Skill

## Option A — Project rule (recommended, version-controlled)

Copy `ultraplan.mdc` to `.cursor/rules/` in your project:

```bash
mkdir -p .cursor/rules
curl -fsSL https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/adapters/cursor/ultraplan.mdc \
  -o .cursor/rules/ultraplan.mdc
```

Or on Windows:
```powershell
New-Item -ItemType Directory -Force ".cursor\rules" | Out-Null
Invoke-WebRequest https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/adapters/cursor/ultraplan.mdc `
  -OutFile ".cursor\rules\ultraplan.mdc"
```

The rule is now active for every Cursor Agent session in this project. Because `alwaysApply: true` is set in the frontmatter, you do not need to reference it manually.

Commit `.cursor/rules/ultraplan.mdc` to share it with your team, or add `.cursor/rules/ultraplan.mdc` to `.gitignore` to keep it private.

## Option B — Global rule (applies to all your projects)

1. Open Cursor → **Settings** (`Ctrl+,` / `Cmd+,`)
2. Go to **General** → **Rules for AI**
3. Paste the full contents of `ultraplan.mdc` (the markdown body, without the YAML frontmatter)

This applies to every Cursor session across all projects.

## Option C — Let Cursor Agent self-install

Open a Cursor Agent chat and paste this prompt:

```
Install the UltraPlan project rule for this project.
Clone https://github.com/Shoko-official/UltraPlan-Skill to a temp directory,
copy adapters/cursor/ultraplan.mdc to .cursor/rules/ultraplan.mdc,
and confirm it is in place.
```

## Verify

After installing, open Agent mode and say: **"ultraplan this project"** or **"run the grill on this feature"** — UltraPlan will activate.

## Updating

Re-run the install command to overwrite. The rule takes effect immediately on the next chat.

## Manual install (no git, no curl)

1. Open https://github.com/Shoko-official/UltraPlan-Skill/blob/main/adapters/cursor/ultraplan.mdc
2. Click **Raw**, copy the full file content
3. Create `.cursor/rules/ultraplan.mdc` in your project and paste
