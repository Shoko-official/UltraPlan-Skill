#!/usr/bin/env bash
# install.sh -- Install the UltraPlan skill to one or more AI runtime skill directories.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/install.sh | bash
#   ./install.sh --dry-run
#   ./install.sh --runtime claude,antigravity
#
# Options:
#   --dry-run           Print target paths without copying any files
#   --runtime LIST      Comma-separated runtimes: claude, antigravity, codex, all (default: all)

set -euo pipefail

SKILL_NAME="ultraplan-engineering"
DRY_RUN=0
RUNTIME="all"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --runtime) RUNTIME="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# Resolve source directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [[ -d "$SCRIPT_DIR/$SKILL_NAME" ]]; then
  SOURCE_DIR="$SCRIPT_DIR/$SKILL_NAME"
else
  # Running via curl | bash -- clone to temp
  TEMP_DIR="$(mktemp -d)"
  echo "Downloading UltraPlan skill to $TEMP_DIR ..."
  git clone --depth 1 https://github.com/Shoko-official/UltraPlan-Skill.git "$TEMP_DIR" 2>/dev/null
  SOURCE_DIR="$TEMP_DIR/$SKILL_NAME"
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "ERROR: Could not find skill source at: $SOURCE_DIR" >&2
  exit 1
fi

# Runtime target paths
declare -A TARGETS=(
  [claude]="$HOME/.claude/skills/$SKILL_NAME"
  [antigravity]="$HOME/.gemini/config/skills/$SKILL_NAME"
  [codex]="$HOME/.codex/skills/$SKILL_NAME"
)

# Determine which runtimes to install
if [[ "$RUNTIME" == "all" ]]; then
  SELECTED=("claude" "antigravity" "codex")
else
  IFS=',' read -ra SELECTED <<< "$RUNTIME"
fi

INSTALLED=()

for rt in "${SELECTED[@]}"; do
  rt="$(echo "$rt" | tr -d ' ')"
  if [[ -z "${TARGETS[$rt]+_}" ]]; then
    echo "WARNING: Unknown runtime '$rt' -- skipping. Valid: claude, antigravity, codex, all"
    continue
  fi
  TARGET="${TARGETS[$rt]}"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY RUN] Would install to: $TARGET"
    continue
  fi

  echo "Installing to $rt -> $TARGET ..."
  if [[ -d "$TARGET" ]]; then
    echo "  Existing install found -- overwriting."
  fi
  mkdir -p "$TARGET"
  cp -r "$SOURCE_DIR/." "$TARGET/"
  INSTALLED+=("$rt")
  echo "  Done."
done

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo ""
  echo "Dry run complete. No files were copied."
elif [[ "${#INSTALLED[@]}" -gt 0 ]]; then
  echo ""
  echo "UltraPlan skill installed to: $(IFS=', '; echo "${INSTALLED[*]}")"
  echo "Restart your AI runtime to pick up the new skill."
else
  echo "Nothing installed."
fi
