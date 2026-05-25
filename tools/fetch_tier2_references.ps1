[CmdletBinding()]
param(
    [switch]$DryRun,
    [string]$ReferenceRoot
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if ([string]::IsNullOrWhiteSpace($ReferenceRoot)) {
    $cosmosRoot = (Resolve-Path (Join-Path $repoRoot "../../..")).Path
    $ReferenceRoot = Join-Path $cosmosRoot "_khovan_reach_tier2_references"
}

$referenceRootFull = [System.IO.Path]::GetFullPath($ReferenceRoot)
$repoRootPrefix = $repoRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

if (
    $referenceRootFull.Equals($repoRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
    $referenceRootFull.StartsWith($repoRootPrefix, [System.StringComparison]::OrdinalIgnoreCase)
) {
    Write-Error "ReferenceRoot must be outside the live mission package. The MAST loader can scan .mastlib/.zip files under the mission root."
    exit 1
}

# These clones are Tier 2 implementation references only. They must live
# outside the active mission package because the MAST loader can discover
# .mastlib and .zip files under the mission root. Do not copy them into
# active scripts/ or treat them as Khovan design.
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
Write-Host "Reference root: $referenceRootFull"

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
    $destination = Join-Path $referenceRootFull $target.Destination
    $parent = Split-Path -Parent $destination

    Write-Host ""
    Write-Host "Target: $($target.Name)"
    Write-Host "URL: $($target.Url)"
    Write-Host "Destination: $destination"

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
Write-Host "Reminder: external reference clones are reference-only and must not be committed."
