#!/usr/bin/env python3
"""
install.py -- UltraPlan skill installer
Source: https://github.com/Shoko-official/UltraPlan-Skill

Cross-platform, Python 3.8+, stdlib only. No pip, no execution policy.

Usage:
  python install.py                    # auto-detect runtimes, install all found
  python install.py --dry-run          # preview without copying
  python install.py --runtime cursor   # install one runtime
  python install.py --runtime claude-code,antigravity

Supported runtimes: antigravity, claude-code, codex, cursor, windsurf
"""

import argparse, os, shutil, sys, platform, urllib.request, zipfile, io, tempfile

REPO_URL = "https://github.com/Shoko-official/UltraPlan-Skill"
REPO_ZIP  = "https://github.com/Shoko-official/UltraPlan-Skill/archive/refs/heads/main.zip"
HOME = os.path.expanduser("~")

def _paths():
    return {
        "antigravity": {
            "dest":  os.path.join(HOME, ".gemini", "config", "skills", "ultraplan-engineering"),
            "src":   "adapters/antigravity",
            "kind":  "skill-dir",
            "label": "Antigravity (Google DeepMind)",
        },
        "claude-code": {
            "dest":  os.path.join(HOME, ".claude", "skills", "ultraplan-engineering"),
            "src":   "adapters/claude-code",
            "kind":  "skill-dir",
            "label": "Claude Code (Anthropic)",
        },
        "codex": {
            "dest":  os.path.join(HOME, ".codex", "skills", "ultraplan-engineering"),
            "src":   "adapters/codex",
            "kind":  "skill-dir",
            "label": "Codex (OpenAI)",
        },
        "cursor": {
            "dest":  None,
            "src":   "adapters/cursor/ultraplan.mdc",
            "kind":  "single-file",
            "label": "Cursor",
            "note":  "Cursor rules are project-level. The file is saved to your current directory -- copy it to .cursor/rules/ in each project.",
        },
        "windsurf": {
            "dest":  None,
            "src":   "adapters/windsurf/ultraplan.md",
            "kind":  "single-file",
            "label": "Windsurf",
            "note":  "Windsurf rules are project-level. The file is saved to your current directory -- copy it to .windsurf/rules/ in each project.",
        },
    }

DETECTION_HINTS = {
    "antigravity": [os.path.join(HOME, ".gemini")],
    "claude-code":  [os.path.join(HOME, ".claude")],
    "codex":        [os.path.join(HOME, ".codex")],
    "cursor": [
        os.path.join(os.environ.get("APPDATA",""), "Cursor"),
        os.path.join(HOME, "Library","Application Support","Cursor"),
        os.path.join(HOME, ".config","Cursor"),
    ],
    "windsurf": [
        os.path.join(os.environ.get("APPDATA",""), "Windsurf"),
        os.path.join(HOME, ".codeium","windsurf"),
        os.path.join(HOME, "Library","Application Support","Windsurf"),
        os.path.join(HOME, ".config","Windsurf"),
    ],
}

def detect_runtimes():
    return [rt for rt, hints in DETECTION_HINTS.items()
            if any(os.path.isdir(h) for h in hints if h)]

def download_repo():
    print(f"  Downloading from {REPO_URL} ...")
    data = urllib.request.urlopen(REPO_ZIP, timeout=30).read()
    tmp = tempfile.mkdtemp(prefix="ultraplan-")
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(tmp)
    sub = next((d for d in os.listdir(tmp) if os.path.isdir(os.path.join(tmp, d))), None)
    return (os.path.join(tmp, sub) if sub else tmp), tmp

def install_runtime(runtime, cfg, source_root, dry_run):
    src  = os.path.join(source_root, cfg["src"].replace("/", os.sep))
    dest = cfg.get("dest")
    kind = cfg["kind"]
    print(f"\n  [{cfg['label']}]")
    if kind == "single-file":
        print(f"  {cfg.get('note','')}")
        fname  = os.path.basename(src)
        target = os.path.join(os.getcwd(), fname)
        if dry_run:
            print(f"  [DRY RUN] Would save: {target}")
        else:
            shutil.copy2(src, target)
            print(f"  Saved to: {target}")
        return True
    print(f"  Target: {dest}")
    if dry_run:
        print(f"  [DRY RUN] Would install to: {dest}")
        return True
    if os.path.isdir(dest):
        print("  Existing install found -- overwriting.")
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)
    for item in os.listdir(src):
        s, d = os.path.join(src, item), os.path.join(dest, item)
        (shutil.copytree if os.path.isdir(s) else shutil.copy2)(s, d)
    print("  Done.")
    return True

def main():
    p = argparse.ArgumentParser(description="Install UltraPlan for AI runtimes.")
    p.add_argument("--dry-run",  action="store_true")
    p.add_argument("--runtime",  default="", help="comma-separated runtimes or 'all'")
    args = p.parse_args()

    paths = _paths()
    if not args.runtime or args.runtime.lower() == "all":
        selected = detect_runtimes()
        if not selected:
            print("No known AI runtimes detected. Use --runtime <name> to force.")
            print(f"Valid: {', '.join(paths)}")
            sys.exit(0)
        print(f"Detected runtimes: {', '.join(selected)}")
    else:
        selected = [r.strip().lower() for r in args.runtime.split(",")]
        bad = [r for r in selected if r not in paths]
        if bad:
            print(f"Unknown runtime(s): {', '.join(bad)}")
            print(f"Valid: {', '.join(paths)}")
            sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.isdir(os.path.join(script_dir, "adapters")):
        source_root, cleanup = script_dir, None
        print(f"Using local source: {source_root}")
    else:
        print("Adapters not found locally -- downloading from GitHub...")
        source_root, cleanup = download_repo()

    if args.dry_run:
        print("\n[DRY RUN -- no files will be copied]\n")

    installed = []
    for rt in selected:
        cfg  = paths[rt]
        src_check = os.path.join(source_root, cfg["src"].replace("/", os.sep))
        if not os.path.exists(src_check):
            print(f"\n  [{cfg['label']}] SKIP -- adapter not found: {src_check}")
            continue
        if install_runtime(rt, cfg, source_root, args.dry_run):
            installed.append(cfg["label"])

    if cleanup:
        shutil.rmtree(cleanup, ignore_errors=True)

    print()
    if args.dry_run:
        print("Dry run complete. No files were copied.")
    elif installed:
        print(f"UltraPlan installed for: {', '.join(installed)}")
        print("Restart your AI runtime to pick up the new skill.")
        print(f"\nSource & updates: {REPO_URL}")
    else:
        print("Nothing installed.")

if __name__ == "__main__":
    main()
