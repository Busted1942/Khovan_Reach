[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# These clones are Tier 2 implementation references only. They are ignored by
# Git and must not be copied into active scripts/ or treated as Khovan design.
$targets = @(
    @{
        Name = "sbs_utils"
        Url = "https://github.com/artemis-sbs/sbs_utils.git"
        Destination = "docs_external/_local_clones/sbs_utils"
    },
    @{
        Name = "mast_starter"
        Url = "https://github.com/artemis-sbs/mast_starter.git"
        Destination = "docs_external/_local_clones/mast_starter"
    },
    @{
        Name = "tutorial_runner"
        Url = "https://github.com/artemis-sbs/tutorial_runner.git"
        Destination = "docs_external/_local_clones/tutorial_runner"
    },
    @{
        Name = "LegendaryMissions"
        Url = "https://github.com/artemis-sbs/LegendaryMissions.git"
        Destination = "reference_missions/_local_clones/LegendaryMissions"
    },
    @{
        Name = "SecretMeeting"
        Url = "https://github.com/artemis-sbs/SecretMeeting.git"
        Destination = "reference_missions/_local_clones/SecretMeeting"
    },
    @{
        Name = "WalkTheLine"
        Url = "https://github.com/artemis-sbs/WalkTheLine.git"
        Destination = "reference_missions/_local_clones/WalkTheLine"
    }
)

Write-Host "Tier 2 reference fetch helper"
Write-Host "Repo root: $repoRoot"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git is not available on PATH; cannot fetch Tier 2 references."
    exit 1
}

if ($DryRun) {
    Write-Host "Mode: dry run. No clone commands will be executed."
} else {
    Write-Host "Mode: fetch. Cloning missing references only."
}

foreach ($target in $targets) {
    $destination = Join-Path $repoRoot $target.Destination
    $parent = Split-Path -Parent $destination

    Write-Host ""
    Write-Host "Target: $($target.Name)"
    Write-Host "URL: $($target.Url)"
    Write-Host "Destination: $($target.Destination)"

    if (Test-Path -LiteralPath $destination) {
        Write-Host "Status: already exists; skipping."
        continue
    }

    if ($DryRun) {
        Write-Host "Would run: git clone --depth 1 $($target.Url) `"$destination`""
        continue
    }

    if (-not (Test-Path -LiteralPath $parent)) {
        Write-Host "Creating parent folder: $parent"
        New-Item -ItemType Directory -Path $parent | Out-Null
    }

    Write-Host "Running: git clone --depth 1 $($target.Url) `"$destination`""
    git clone --depth 1 $target.Url $destination
}

Write-Host ""
Write-Host "Reminder: external reference clones are ignored by Git and must not be committed."
