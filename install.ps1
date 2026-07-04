#Requires -Version 5.0
<#
.SYNOPSIS
    Installs the UltraPlan skill to one or more AI runtime skill directories.

.PARAMETER DryRun
    Print target paths without copying any files.

.PARAMETER Runtime
    Comma-separated list of runtimes to install to.
    Valid values: claude, antigravity, codex, all
    Default: all

.EXAMPLE
    irm https://raw.githubusercontent.com/Shoko-official/UltraPlan-Skill/main/install.ps1 | iex

.EXAMPLE
    .\install.ps1 --DryRun
    .\install.ps1 --Runtime claude,antigravity
#>
param(
    [switch]$DryRun,
    [string]$Runtime = "all"
)

$ErrorActionPreference = "Stop"
$skillName = "ultraplan-engineering"
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# If running via iex (no script path), clone or download to temp
if (-not $repoRoot -or -not (Test-Path (Join-Path $repoRoot $skillName))) {
    $tempDir = Join-Path $env:TEMP "ultraplan-install-$(Get-Random)"
    Write-Host "Downloading UltraPlan skill to $tempDir ..."
    git clone --depth 1 https://github.com/Shoko-official/UltraPlan-Skill.git $tempDir 2>&1 | Out-Null
    $sourceDir = Join-Path $tempDir $skillName
} else {
    $sourceDir = Join-Path $repoRoot $skillName
}

if (-not (Test-Path $sourceDir)) {
    Write-Error "Could not find skill source at: $sourceDir"
    exit 1
}

# Define runtime target paths
$runtimes = @{
    claude      = Join-Path $env:USERPROFILE ".claude\skills\$skillName"
    antigravity = Join-Path $env:USERPROFILE ".gemini\config\skills\$skillName"
    codex       = Join-Path $env:USERPROFILE ".codex\skills\$skillName"
}

# Select runtimes to install to
$selected = if ($Runtime -eq "all") {
    $runtimes.Keys
} else {
    $Runtime -split "," | ForEach-Object { $_.Trim().ToLower() }
}

$installed = @()
$skipped = @()

foreach ($rt in $selected) {
    if (-not $runtimes.ContainsKey($rt)) {
        Write-Warning "Unknown runtime '$rt' -- skipping. Valid: claude, antigravity, codex, all"
        continue
    }
    $targetDir = $runtimes[$rt]

    if ($DryRun) {
        Write-Host "[DRY RUN] Would install to: $targetDir"
        continue
    }

    Write-Host "Installing to $rt -> $targetDir ..."
    if (Test-Path $targetDir) {
        Write-Host "  Existing install found -- overwriting."
    }
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    Copy-Item -Recurse -Force "$sourceDir\*" $targetDir
    $installed += $rt
    Write-Host "  Done."
}

if ($DryRun) {
    Write-Host ""
    Write-Host "Dry run complete. No files were copied."
} elseif ($installed.Count -gt 0) {
    Write-Host ""
    Write-Host "UltraPlan skill installed to: $($installed -join ', ')"
    Write-Host "Restart your AI runtime to pick up the new skill."
} else {
    Write-Host "Nothing installed."
}
