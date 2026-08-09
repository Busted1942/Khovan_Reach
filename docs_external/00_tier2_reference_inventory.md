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
- story.json / script.py / story.mast / scripts/main.mast patterns
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

---

## Original user-provided source roots

- https://github.com/artemis-sbs
- https://www.armidalesoftware.com/Artemis/CosmosBridgeTools.htm
- https://github.com/astrolamb-gaming
- https://artemis-sbs.github.io/sbs_utils/

artemis-sbs and astrolamb-gaming are organization/root sources. The fetch script may use selected concrete repositories from those roots, but selected clone targets are not exhaustive.

If Slice 01 or later work needs an API not covered by the selected repositories, revisit the root sources and document any newly selected reference repo before using it.

---

## Source review, 2026-08-09

Prompted by an operator question about whether a set of URLs would add value.
Outcome: **most were already covered, and the gap was consultation, not
coverage.**

Already cloned locally, so no fetch needed:

| Source | Where it landed |
|---|---|
| `artemis-sbs/SecretMeeting` `story.mast` | `reference_missions/_local_clones/SecretMeeting/` |
| `artemis-sbs.github.io/sbs_utils/api/` | `docs_external/_local_clones/sbs_utils/mkdocs/docs/api/` |
| `artemis-sbs.github.io/sbs_utils/mast/tutorial/` | same clone, `mkdocs/docs/tutorial/` |
| `github.com/artemis-sbs` (root) | already listed above |
| `armidalesoftware.com/.../CosmosBridgeTools.htm` | already listed above |
| `github.com/astrolamb-gaming` (root) | already listed above |

The published `sbs_utils` docs site is generated from `mkdocs/docs` inside the
clone we already hold, so the site and the local copy are the same material.
`LegendaryMissions` and `WalkTheLine` are also cloned.

**Not previously listed, and not fetched:**
`artemiswiki.pbworks.com/w/page/44188987/Station overviews`. The URL bounces
between http and https, so it could not be retrieved for assessment. From the
domain and page name it is the classic-Artemis community wiki, which predates
Cosmos and documents bridge stations from a player's perspective rather than
`sbs_utils` scripting. Likely useful for crew-facing language, not for API
questions. Assess before relying on it, and never treat it as Cosmos API
authority.

**What the review actually produced.** Two live failures on 2026-08-09 (the
`set_behavior` crash and the wrong capital-`Station` claim in cookbook 8.2) were
*not* caused by missing reference material:

- `set_behavior` is documented in the sbs_utils source we already had, and the
  accessor needed to reach it (`sim.get_space_object`) is in `api/spaceobject.rst`
  in the docs clone we already had. Recorded in cookbook 12.1.
- The MAST limitation that a literal `\n` survives only in a `shared` declaration,
  and breaks the parser inline, is documented **nowhere** in any of these
  sources. It was found by compile preflight and is now cookbook-recorded.

Practical rule: before raising an API uncertainty, grep the local clones under
`_khovan_reach_tier2_references/`. The answer to the more expensive of today's
two failures was sitting in them the whole time.

## Where the clones actually live

They are **outside** the mission directory, at
`<Cosmos>/_khovan_reach_tier2_references/`, per the runtime-clean warning below.
The `docs_external/_local_clones/` and `reference_missions/_local_clones/`
folders inside this repo are intentionally empty.

---

## Runtime-clean mission-root warning

Git-ignored does not mean Cosmos-ignored.

If external reference clones, archived old MAST files, or other implementation-history material live under the active Cosmos mission directory, Cosmos/MAST may still scan or resolve them at runtime.

The active mission path is expected to be:

```text
C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach
```

Therefore:

- ignored _local_clones folders are convenient for coding agents but may be runtime-visible to Cosmos/MAST
- active runtime files must never reference _local_clones
- active runtime files must never reference archive/old_build_reference
- active runtime files must never reference old_mast
- local reference clones should be moved outside the live mission root if live smoke tests show Cosmos/MAST scans or loads them unexpectedly

Preferred long-term reference-cache pattern:

```text
C:\Users\buste\OneDrive\Desktop\Cosmos\data\mission_references\khovan_reach_refs\
```

or another sibling/outside folder that is not part of the loadable mission package.

If references remain under the live mission root, every Slice 01+ quick test must verify that no active runtime file references them.

---

## Required local inventory check

Before Slice 01 coding, run:

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

- docs_external/cosmos, docs_external/mast, and docs_external/sbs_utils may contain curated notes or snapshots if deliberately committed.
- _local_clones folders are local-only reference caches.
- _local_clones folders must be ignored by Git.
- _local_clones folders must not be referenced from active runtime files.
- archive/old_build_reference/old_mast is old Khovan implementation-history evidence only.
- scripts/ is active runtime code only and must not receive old MAST files.

---

## Online Tier 2 reference sources

### 1. sbs_utils documentation

Category: official/primary documentation  
URL: https://artemis-sbs.github.io/sbs_utils/  
Expected local folder: docs_external/sbs_utils/ or external reference cache  
Slice 01 relevance: required  
Inspect for:

- MAST/Cosmos/sbs_utils API syntax
- mission startup
- task scheduling
- GUI/route helpers
- Comms/Science/spawn examples where documented

Do not import:

- Khovan design behavior
- unsupported assumptions
- sample scenario pacing

### 2. artemis-sbs/sbs_utils

Category: official/primary source repo  
URL: https://github.com/artemis-sbs/sbs_utils  
Expected local folder: docs_external/_local_clones/sbs_utils/ or external reference cache  
Slice 01 relevance: required  
Inspect for:

- script.py patterns
- MAST examples
- package layout
- tests
- docs source
- API examples

Do not import:

- unrelated sample scenario design
- cloned repo paths into active runtime files

### 3. artemis-sbs/mast_starter

Category: official/reference bootstrap repo  
URL: https://github.com/artemis-sbs/mast_starter  
Expected local folder: docs_external/_local_clones/mast_starter/ or external reference cache  
Slice 01 relevance: required  
Inspect for:

- minimal mission bootstrap
- story.json
- script.py
- story.mast
- __lib__.json
- startup and lifecycle pattern

Do not import:

- sample mission story/pacing
- sample map labels unless adapted to Khovan bootstrap

### 4. artemis-sbs/tutorial_runner

Category: official/reference mission/tooling repo  
URL: https://github.com/artemis-sbs/tutorial_runner  
Expected local folder: docs_external/_local_clones/tutorial_runner/ or external reference cache  
Slice 01 relevance: high-value  
Inspect for:

- mission startup
- tutorial sequencing
- UI/message examples
- task scheduling
- tests

Do not import:

- tutorial content as Khovan design

### 5. artemis-sbs/LegendaryMissions

Category: reference missions  
URL: https://github.com/artemis-sbs/LegendaryMissions  
Expected local folder: reference_missions/_local_clones/LegendaryMissions/ or external reference cache  
Slice 01 relevance: useful after bootstrap  
Inspect for:

- known-good mission structure
- MAST packaging conventions
- task lifecycle patterns

Do not import:

- scenario design
- story flow
- gameplay pacing

### 6. artemis-sbs/SecretMeeting

Category: reference mission  
URL: https://github.com/artemis-sbs/SecretMeeting  
Expected local folder: reference_missions/_local_clones/SecretMeeting/ or external reference cache  
Slice 01 relevance: useful after bootstrap  
Inspect for:

- story progression
- Comms/menu/timer examples if present
- root mission packaging

Do not import:

- story design
- player-facing behavior

### 7. artemis-sbs/WalkTheLine

Category: reference mission  
URL: https://github.com/artemis-sbs/WalkTheLine  
Expected local folder: reference_missions/_local_clones/WalkTheLine/ or external reference cache  
Slice 01 relevance: useful after bootstrap  
Inspect for:

- mission package structure
- runtime lifecycle patterns
- story.mast / script.py startup flow

Do not import:

- story design
- scenario objectives

### 8. Cosmos Bridge Tools / Armidale Software

Category: supplemental tooling/documentation  
URL: https://www.armidalesoftware.com/Artemis/CosmosBridgeTools.htm  
Expected local folder: docs_external/cosmos/ or external reference cache  
Slice 01 relevance: supplemental  
Inspect for:

- Cosmos tooling
- launch/setup notes
- mission setup assumptions

Do not import:

- obsolete launch assumptions unless verified

### 9. Astrolamb Gaming GitHub organization

Category: secondary candidate reference source  
URL: https://github.com/astrolamb-gaming  
Expected local folder: reference_missions/_local_clones/astrolamb-gaming/ or external reference cache  
Slice 01 relevance: optional  
Inspect for:

- known-good mission examples only if needed

Do not import:

- design
- scenario behavior

---

## Approved clone targets

The fetch script may use these targets as selected concrete references:

```text
docs_external/_local_clones/sbs_utils:
https://github.com/artemis-sbs/sbs_utils.git

docs_external/_local_clones/mast_starter:
https://github.com/artemis-sbs/mast_starter.git

docs_external/_local_clones/tutorial_runner:
https://github.com/artemis-sbs/tutorial_runner.git

reference_missions/_local_clones/LegendaryMissions:
https://github.com/artemis-sbs/LegendaryMissions.git

reference_missions/_local_clones/SecretMeeting:
https://github.com/artemis-sbs/SecretMeeting.git

reference_missions/_local_clones/WalkTheLine:
https://github.com/artemis-sbs/WalkTheLine.git
```

These targets are not exhaustive.

---

## Recommended local population strategy

- Keep the committed Khovan repo lightweight.
- Commit this inventory and fetch scripts.
- Use local clones only as implementation evidence.
- Do not commit external repo clones unless explicitly approved.
- If committing snapshots later, commit only curated notes or extracted examples with attribution.
- Prefer external/sibling reference caches outside the live mission root when Cosmos/MAST runtime behavior is uncertain.
- If _local_clones remain inside the live mission root, require quick tests that reject runtime references to them.

---

## Slice 01 minimum reference check

Before implementing or repairing Slice 01, inspect:

- docs_external/TIER2_REFERENCE_INVENTORY.md
- sbs_utils docs home/API index, if locally available or web-accessible
- sbs_utils repo root, if cloned
- mast_starter root, if cloned
- tutorial_runner root, if cloned
- any story.json, script.py, story.mast, main.mast, or __lib__.json examples found locally
- archive/old_build_reference/old_mast/main.mast only as old implementation evidence

Answer these Slice 01 bootstrap questions:

1. What files are required for a Cosmos/MAST mission package?
2. Where should Khovan's root story.mast live?
3. Does Cosmos expect story.json at repo root?
4. Does Cosmos expect script.py at repo root?
5. How should root story.mast reach scripts/main.mast?
6. How should script.py initialize, if needed?
7. How should a minimal mission initialize state?
8. How can Dillon Clip 1 be queued, played, or safely stubbed?
9. How can the mission leave a valid yielding/long-running GUI/story task alive?
10. What can be checked statically versus only inside live Cosmos?

---

## API uncertainty rule

If local Tier 2 material does not clearly answer a required API or file-layout question, document the uncertainty instead of inventing syntax.

Use this format:

```text
API uncertainty:
Question:
Sources checked:
What appears documented:
What appears inferred:
Risk:
Recommended spike or next action:
```

---

## Known current gaps

- docs_external/cosmos may not be populated.
- docs_external/mast may not be populated.
- docs_external/sbs_utils may not be populated.
- reference_missions may not be populated except ignored local clones.
- Old Khovan archive is populated but archive-only.
- _local_clones may be runtime-visible if placed under the live mission root.
- Slice 01 agent must not claim Tier 2 resources are locally available until inventory commands prove it.
- Slice 01 agent must not claim live mission load from static tests alone.
