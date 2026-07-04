#Requires -Version 5.0
<#
.SYNOPSIS
    Installs the UltraPlan skill to AI runtime directories.

.DESCRIPTION
    Wrapper around install.py. Requires Python 3.8+ (no pip needed).
    No execution policy issues -- Python is invoked directly.

    Prefer running install.py directly when Python is on PATH:
        python install.py

.PARAMETER DryRun
    Preview target paths without copying any files.

.PARAMETER Runtime
    Comma-separated runtimes to install to.
    Valid: antigravity, claude-code, codex, cursor, windsurf, all (default)

.EXAMPLE
    # One-shot (requires git + python):
    git clone https://github.com/Shoko-official/UltraPlan-Skill.git ultraplan-skill
    cd ultraplan-skill
    python install.py

.EXAMPLE
    .\install.ps1 -DryRun
    .\install.ps1 -Runtime claude-code,cursor
#>
param(
    [switch]$DryRun,
    [string]$Runtime = "all"
)

$ErrorActionPreference = "Stop"

# Find install.py next to this script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$installer  = Join-Path $scriptDir "install.py"

if (-not (Test-Path $installer)) {
    Write-Error "install.py not found at $installer. Clone the full repo first:`n  git clone https://github.com/Shoko-official/UltraPlan-Skill.git"
    exit 1
}

# Check Python is available
try { $null = python --version 2>&1 } catch {
    Write-Error "Python 3.8+ is required but was not found on PATH.`nInstall from https://python.org and re-run."
    exit 1
}

$pyArgs = @()
if ($DryRun)            { $pyArgs += "--dry-run" }
if ($Runtime -ne "all") { $pyArgs += "--runtime"; $pyArgs += $Runtime }

python $installer @pyArgs
