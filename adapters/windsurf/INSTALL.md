# Installing UltraPlan for Windsurf

Source: https://github.com/Shoko-official/UltraPlan-Skill

## Option A - Project rule via .windsurf/rules/ (recommended)

```bash
mkdir -p .windsurf/rules
curl -fsSL https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/adapters/windsurf/ultraplan.md \
  -o .windsurf/rules/ultraplan.md
```

Windows:
```powershell
New-Item -ItemType Directory -Force ".windsurf\rules" | Out-Null
Invoke-WebRequest https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/adapters/windsurf/ultraplan.md `
  -OutFile ".windsurf\rules\ultraplan.md"
```

Commit the file to share it with your team, or add `.windsurf/rules/ultraplan.md` to `.gitignore` to keep it private.

## Option B - Project rule via .windsurfrules (single-file)

```bash
curl -fsSL https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/adapters/windsurf/ultraplan.md \
  >> .windsurfrules
```

This appends UltraPlan to the existing `.windsurfrules` file at the project root.

## Option C - Global rule (applies to all your projects)

1. Open Windsurf → **Settings** → **AI** → **Rules**
2. Paste the full contents of `ultraplan.md`

## Option D - Let Windsurf Cascade self-install

Open a Cascade chat and paste this prompt:

```
Install the UltraPlan rules for this project.
Clone https://github.com/Shoko-official/UltraPlan-Skill to a temp directory,
copy adapters/windsurf/ultraplan.md to .windsurf/rules/ultraplan.md,
and confirm it is in place.
```

## Verify

After installing, say **"ultraplan this project"** or **"run the grill"** in Cascade - UltraPlan will activate.

## Manual install (no git, no curl)

1. Open https://github.com/Shoko-official/UltraPlan-Skill/blob/main/adapters/windsurf/ultraplan.md
2. Click **Raw**, copy the full content
3. Save as `.windsurf/rules/ultraplan.md` in your project
