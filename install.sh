#!/usr/bin/env bash
# install.sh -- UltraPlan skill installer wrapper
# Source: https://github.com/Shoko-official/UltraPlan-Skill
#
# Requires Python 3.8+ (stdlib only, no pip).
# No execution policy issues on any platform.
#
# Usage:
#   ./install.sh                     # auto-detect runtimes
#   ./install.sh --dry-run           # preview only
#   ./install.sh --runtime cursor    # specific runtime

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || pwd)"
INSTALLER="$SCRIPT_DIR/install.py"

if [[ ! -f "$INSTALLER" ]]; then
  echo "ERROR: install.py not found at $INSTALLER"
  echo "Clone the full repo first:"
  echo "  git clone https://github.com/Shoko-official/UltraPlan-Skill.git"
  exit 1
fi

# Find python
if command -v python3 &>/dev/null; then
  PY=python3
elif command -v python &>/dev/null; then
  PY=python
else
  echo "ERROR: Python 3.8+ is required but not found on PATH."
  echo "Install from https://python.org and re-run."
  exit 1
fi

exec "$PY" "$INSTALLER" "$@"
