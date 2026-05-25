# Khovan Reach — Tier 2 Implementation Reference Inventory

Status: implementation-reference inventory  
Authority: non-canonical; syntax/API/reference only  
Purpose: Tell coding agents where to find Cosmos/MAST/sbs_utils documentation, known-good reference missions, and old Khovan implementation-history evidence.

This file does not define Khovan Reach design.

Active scenario/design authority remains:

- docs/00_project/00_source_index.md
- docs/01_design/*
- docs/02_content/*
- docs/03_game_resources/*

Implementation setup and evidence sources:

- docs/04_implementation_setup/*

These setup files guide implementation restart, source transfer, and known-risk handling. They do not override active design docs.

Tier 2 materials may be used only to answer implementation questions such as:

- mission bootstrap file layout
- `story.json` / `script.py` / `story.mast` / `scripts/main.mast` patterns
- MAST include/import syntax
- sbs_utils API syntax
- Comms route/menu syntax
- Science scan syntax
- ship spawning syntax
- GM-only controls
- task scheduling and delayed events
- smoke-test patterns
- known-good reference mission structure

Do not import scenario design, pacing, story structure, factions, objectives, or player-facing behavior from reference missions.

Local clones must not become active runtime dependencies.

---

## Original user-provided source roots

- https://github.com/artemis-sbs
- https://www.armidalesoftware.com/Artemis/CosmosBridgeTools.htm
- https://github.com/astrolamb-gaming
- https://artemis-sbs.github.io/sbs_utils/

`artemis-sbs` and `astrolamb-gaming` are organization/root sources. The fetch script may use selected concrete repositories from those roots, but selected clone targets are not exhaustive.

If Slice 01 or later work needs an API not covered by the selected repositories, revisit the root sources and document any newly selected reference repo before using it.

---

## Runtime-clean mission-root warning

Git-ignored does not mean Cosmos-ignored.

If external reference clones, archived old MAST files, or other implementation-history material live under the active Cosmos mission directory, Cosmos/MAST may still scan or resolve them at runtime.

The active mission path is expected to be:

```text
C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach
```

Reference folders that are ignored by Git can still be runtime-visible to Cosmos if they sit under that active mission root. In particular, `_local_clones` folders may contain `.mastlib`, `.sbslib`, `.zip`, `__init__.mast`, or other files that the MAST loader can discover even though Git ignores them.

Active runtime files must not reference:

- `docs_external/_local_clones`
- `reference_missions/_local_clones`
- `archive/old_build_reference`
- `old_mast`

Tier 2 clones should live outside the active mission package when running live Cosmos smoke tests.

Preferred long-term reference-cache pattern:

```text
C:\Users\buste\OneDrive\Desktop\Cosmos\data\mission_references\khovan_reach_refs\
```

or another sibling/outside folder that is not part of the loadable mission package.

---

## Required local inventory check

Before Slice 01 coding or live-load troubleshooting, run:

```powershell
Get-ChildItem docs_external -Recurse -File | Select-Object FullName
Get-ChildItem reference_missions -Recurse -File | Select-Object FullName
Get-ChildItem archive/old_build_reference -Recurse -File | Select-Object FullName
Get-ChildItem scripts -Recurse -File | Select-Object FullName
Get-ChildItem . -File | Select-Object Name
```

The check is observational only. Do not download, move, copy, or activate reference material automatically.

---

## Local reference locations

Expected committed folders:

```text
docs_external/
docs_external/cosmos/
docs_external/mast/
docs_external/sbs_utils/
reference_missions/
archive/old_build_reference/
archive/old_build_reference/old_mast/
```

Optional local-only folders:

```text
docs_external/_local_clones/
reference_missions/_local_clones/
```

Rules:

- `docs_external/cosmos`, `docs_external/mast`, and `docs_external/sbs_utils` may contain curated notes or snapshots if deliberately committed.
- `_local_clones` folders are local-only reference caches.
- `_local_clones` folders must be ignored by Git.
- `_local_clones` folders must not be referenced from active runtime files.
- `archive/old_build_reference/old_mast` is old Khovan implementation-history evidence only.
- `scripts/` is active runtime code only and must not receive old MAST files.

---

## Online Tier 2 reference sources

### sbs_utils documentation

Category: official/primary documentation  
URL: https://artemis-sbs.github.io/sbs_utils/  
Expected local folder: `docs_external/sbs_utils/` or external reference cache  
Slice 01 relevance: required

Inspect for MAST/Cosmos/sbs_utils API syntax, mission startup, task scheduling, GUI/route helpers, and Comms/Science/spawn examples where documented.

### artemis-sbs/sbs_utils

Category: official/primary source repo  
URL: https://github.com/artemis-sbs/sbs_utils  
Expected local folder: `docs_external/_local_clones/sbs_utils/` or external reference cache  
Slice 01 relevance: required

Inspect for `script.py` patterns, MAST examples, package layout, tests, docs source, and API examples.

### artemis-sbs/mast_starter

Category: official/reference bootstrap repo  
URL: https://github.com/artemis-sbs/mast_starter  
Expected local folder: `docs_external/_local_clones/mast_starter/` or external reference cache  
Slice 01 relevance: required

Inspect for minimal mission bootstrap, `story.json`, `script.py`, `story.mast`, `__lib__.json`, and startup/lifecycle patterns.

### artemis-sbs/tutorial_runner

Category: official/reference mission/tooling repo  
URL: https://github.com/artemis-sbs/tutorial_runner  
Expected local folder: `docs_external/_local_clones/tutorial_runner/` or external reference cache  
Slice 01 relevance: high-value

Inspect for mission startup, tutorial sequencing, UI/message examples, task scheduling, and tests.

### artemis-sbs reference missions

Use these as reference missions only:

- https://github.com/artemis-sbs/LegendaryMissions
- https://github.com/artemis-sbs/SecretMeeting
- https://github.com/artemis-sbs/WalkTheLine

Expected local folder: `reference_missions/_local_clones/` or external reference cache.

Inspect for known-good mission structure, MAST packaging conventions, task lifecycle patterns, and root mission packaging. Do not import scenario design, story flow, gameplay pacing, objectives, factions, or player-facing behavior.

### Cosmos Bridge Tools / Armidale Software

Category: supplemental tooling/documentation  
URL: https://www.armidalesoftware.com/Artemis/CosmosBridgeTools.htm  
Expected local folder: `docs_external/cosmos/` or external reference cache

Inspect for Cosmos tooling, launch/setup notes, and mission setup assumptions. Do not import obsolete launch assumptions unless verified.

### Astrolamb Gaming GitHub organization

Category: secondary candidate reference source  
URL: https://github.com/astrolamb-gaming  
Expected local folder: `reference_missions/_local_clones/astrolamb-gaming/` or external reference cache

Inspect only if needed for known-good mission examples. Do not import design or scenario behavior.

---

## Approved clone targets

The fetch script uses selected concrete repositories from the source roots. These targets are not exhaustive.

| Target | Expected local folder | Upstream |
| --- | --- | --- |
| sbs_utils | `docs_external/_local_clones/sbs_utils` | `https://github.com/artemis-sbs/sbs_utils.git` |
| mast_starter | `docs_external/_local_clones/mast_starter` | `https://github.com/artemis-sbs/mast_starter.git` |
| tutorial_runner | `docs_external/_local_clones/tutorial_runner` | `https://github.com/artemis-sbs/tutorial_runner.git` |
| LegendaryMissions | `reference_missions/_local_clones/LegendaryMissions` | `https://github.com/artemis-sbs/LegendaryMissions.git` |
| SecretMeeting | `reference_missions/_local_clones/SecretMeeting` | `https://github.com/artemis-sbs/SecretMeeting.git` |
| WalkTheLine | `reference_missions/_local_clones/WalkTheLine` | `https://github.com/artemis-sbs/WalkTheLine.git` |

If any expected local folder is empty or missing, mark it as not yet populated and use the next available reference level. Do not commit external clone contents.

---

## Recommended local population strategy

- Keep the committed Khovan repo lightweight.
- Commit this inventory and fetch scripts.
- Use local clones only as implementation evidence.
- Do not commit external repo clones unless explicitly approved.
- If committing snapshots later, commit only curated notes or extracted examples with attribution.
- Prefer external/sibling reference caches outside the live mission root when Cosmos/MAST runtime behavior is uncertain.
- If `_local_clones` remain inside the live mission root, require quick tests that reject runtime references to them.

---

## Slice 01 minimum reference check

Before changing the Slice 01 bootstrap, inspect the active entry chain and compare it to known-good references:

- `story.json`
- `script.py`
- `story.mast`
- `scripts/main.mast`
- `__lib__.json`
- whether the entry chain leaves a yielding or long-running GUI/story task alive

Reference missions may answer syntax, API, bootstrap, file-layout, and known-good implementation-pattern questions. They must not change Khovan story, pacing, factions, objectives, or player-facing behavior.

---

## API uncertainty format

When Cosmos/MAST/sbs_utils behavior is unclear, document:

- the API or runtime behavior in question
- active files inspected
- reference files inspected
- observed live Cosmos error, if any
- static test coverage added or why it is not practical
- live smoke step still required
- next recommended spike or verification action

Static tests can protect source hygiene, load-path shape, and known regression patterns. Static tests cannot claim live mission load by themselves; BOOT-001 and BOOT-012 require live Cosmos smoke evidence or a documented blocker.

---

## Known current gaps

- `docs_external/cosmos` may not be populated.
- `docs_external/mast` may not be populated.
- `docs_external/sbs_utils` may not be populated.
- `reference_missions` may not be populated except ignored local clones.
- Old Khovan archive is populated but archive-only.
- `_local_clones` may be runtime-visible if placed under the live mission root.
- Slice 01 agents must not claim Tier 2 resources are locally available until inventory commands prove it.
- Slice 01 agents must not claim live mission load from static tests alone.
