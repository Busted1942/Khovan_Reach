[CmdletBinding()]
param(
    [switch]$Execute
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

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

if (-not $Execute) {
    Write-Host "Mode: dry run. No network commands will be executed."
    Write-Host "Re-run with -Execute only after explicit approval."
} else {
    Write-Host "Mode: execute. Cloning missing references only."
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

    if (-not $Execute) {
        Write-Host "Would run: git clone --depth 1 $($target.Url) `"$destination`""
        continue
    }

    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }

    git clone --depth 1 $target.Url $destination
}

Write-Host ""
Write-Host "Reminder: external reference clones are ignored by Git and must not be committed."
