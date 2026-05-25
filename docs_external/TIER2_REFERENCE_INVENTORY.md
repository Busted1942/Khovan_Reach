# Khovan Reach — Tier 2 Implementation Reference Inventory

Status: implementation-reference inventory  
Authority: non-canonical; syntax/API/reference only  
Purpose: Tell coding agents where to find Cosmos/MAST/sbs_utils documentation, known-good reference missions, and old Khovan implementation-history evidence.

This file does not define Khovan Reach design.

Active design authority remains:

- `docs/00_project/00_source_index.md`
- the active design docs listed by that source index

Tier 2 material may be used only for syntax, API, bootstrap, file layout, and known-good implementation patterns, including:

- mission bootstrap file layout
- `main.mast` / `story.mast` / `story.json` / `script.py` patterns
- MAST include/import syntax
- sbs_utils API syntax
- Comms route/menu syntax
- Science scan syntax
- ship spawning syntax
- GM-only controls
- task scheduling and delayed events
- smoke-test patterns
- known-good reference mission structure

Reference missions must not be used to alter Khovan story, pacing, factions, objectives, or player-facing behavior.

Do not import scenario design, pacing, story structure, or player-facing behavior from reference missions.

---

## Original user-provided source roots

- `https://github.com/artemis-sbs`
- `https://www.armidalesoftware.com/Artemis/CosmosBridgeTools.htm`
- `https://github.com/astrolamb-gaming`
- `https://artemis-sbs.github.io/sbs_utils/`

`artemis-sbs` and `astrolamb-gaming` are organization/root sources. The fetch script uses selected concrete repositories from those roots.

Selected clone targets are not exhaustive. If Slice 01 or later work needs an API not covered by the selected repositories, revisit the root sources and document any newly selected reference repo before using it.

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

## Current local status

- `docs_external/_local_clones`: not yet populated.
- `reference_missions/_local_clones`: not yet populated.
- `docs_external/cosmos`: not yet populated.
- `docs_external/mast`: not yet populated.
- `docs_external/sbs_utils`: not yet populated.
- `reference_missions`: not yet populated beyond local guardrail files.
- `archive/old_build_reference`: populated with archive/reference material only.
- `archive/old_build_reference/old_mast`: populated with old Khovan MAST implementation-history evidence.
- `archive/old_build_reference/test_harness`: populated with old abandoned test-harness evidence only.
- `scripts`: active runtime location only; currently placeholder-only and must not receive old MAST files.

Folders marked "not yet populated" currently contain no implementation reference files beyond placeholder files such as `.gitkeep` or local README guardrails.

---

## Safe local fetch workflow

Use `tools/fetch_tier2_references.ps1` to populate approved local reference clones.

Fetch mode:

```powershell
.\tools\fetch_tier2_references.ps1
```

If local PowerShell execution policy blocks direct script execution, use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\fetch_tier2_references.ps1
```

Dry-run preview mode:

```powershell
.\tools\fetch_tier2_references.ps1 -DryRun
```

The script must not be used to pull references into active `scripts/`. External reference clones are local evidence only and must not be committed.

---

## Tier 2 fetch targets

| Target | Local destination | Upstream | Use for | Current local state |
| --- | --- | --- | --- | --- |
| sbs_utils docs/source | `docs_external/_local_clones/sbs_utils` | `https://github.com/artemis-sbs/sbs_utils.git` | MAST language, sbs_utils API, bootstrap examples, docs source | not yet populated |
| MAST starter | `docs_external/_local_clones/mast_starter` | `https://github.com/artemis-sbs/mast_starter.git` | minimal starter layout and bootstrap conventions | not yet populated |
| Tutorial runner | `docs_external/_local_clones/tutorial_runner` | `https://github.com/artemis-sbs/tutorial_runner.git` | tutorial execution patterns and runnable examples | not yet populated |
| Legendary Missions | `reference_missions/_local_clones/LegendaryMissions` | `https://github.com/artemis-sbs/LegendaryMissions.git` | broad known-good mission structure, GM/comms/science/damage patterns | not yet populated |
| Secret Meeting | `reference_missions/_local_clones/SecretMeeting` | `https://github.com/artemis-sbs/SecretMeeting.git` | compact bootstrap and simple MAST mission layout | not yet populated |
| Walk The Line | `reference_missions/_local_clones/WalkTheLine` | `https://github.com/artemis-sbs/WalkTheLine.git` | compact bootstrap, helper-function patterns, alternate mission structure | not yet populated |

The `docs_external/cosmos`, `docs_external/mast`, and `docs_external/sbs_utils` folders are reserved for local notes or curated documentation snapshots if Matt explicitly asks for them. The approved clone destinations are under `docs_external/_local_clones` and `reference_missions/_local_clones`.

---

## Online docs to inspect before Slice 01 bootstrap

Use these online docs for syntax/API confirmation when local copies are not populated:

- `https://artemis-sbs.github.io/sbs_utils/`
- `https://artemis-sbs.github.io/sbs_utils/mast/tutorial/`
- `https://artemis-sbs.github.io/LegendaryMissions/`

Slice 01 bootstrap agents should verify:

- required mission files: `description.txt`, `script.py`, `story.mast`, `story.json`
- whether this repo should use `main.mast` directly or a `story.mast` bootstrap wrapper
- MAST module folder loading and `__init__.mast` import syntax
- how `story.json` declares sbs_utils and addon dependencies
- how reference missions structure map labels and mission overview labels
- how the top-level `cosmos_event_handler` delegates into sbs_utils/MAST runtime

Do not treat online reference docs as Khovan design authority.

---

## Reference inspection priority for Slice 01

Use this order when answering Cosmos/MAST/sbs_utils implementation questions:

1. Active Khovan source authority for requirements and boundaries.
2. Local active Khovan code, once Slice 01 creates any.
3. Local Tier 2 docs and reference mission clones, if populated.
4. Online sbs_utils/MAST/Legendary Missions docs.
5. Archived old Khovan MAST as implementation-history evidence only.

For Slice 01 bootstrap specifically, inspect these reference files once populated:

- `docs_external/_local_clones/sbs_utils/script.py`
- `docs_external/_local_clones/sbs_utils/script_min.py`
- `docs_external/_local_clones/sbs_utils/mkdocs/docs/mast/tutorial.md`
- `docs_external/_local_clones/mast_starter`
- `docs_external/_local_clones/tutorial_runner`
- `reference_missions/_local_clones/LegendaryMissions/script.py`
- `reference_missions/_local_clones/LegendaryMissions/story.json`
- `reference_missions/_local_clones/LegendaryMissions/story.mast`
- `reference_missions/_local_clones/SecretMeeting/script.py`
- `reference_missions/_local_clones/SecretMeeting/story.json`
- `reference_missions/_local_clones/SecretMeeting/story.mast`
- `reference_missions/_local_clones/WalkTheLine/script.py`
- `reference_missions/_local_clones/WalkTheLine/story.json`
- `reference_missions/_local_clones/WalkTheLine/story.mast`

If any referenced local file or folder is empty or missing, mark it as not yet populated and use the next available reference level.

---

## Archive-only Khovan evidence

Old Khovan implementation files under `archive/old_build_reference/old_mast` are reference evidence only. They may be inspected for known-good syntax and implementation patterns, but must not be copied into active `scripts/` as mission code.

Current archived old MAST files:

- `act_1_qualification.mast`
- `act_1_state_helpers.mast`
- `act_2_investigation.mast`
- `act_3_khovan_reach.mast`
- `damcon_timer.mast`
- `dev_jump.mast`
- `main.mast`
- `__init__.mast`

Old abandoned test work under `archive/old_build_reference/test_harness` is archive/reference only. Do not restore it as the active test harness.

---

## Usage rules for coding agents

- Inspect Tier 2 references only when MAST, Cosmos, or sbs_utils syntax is uncertain.
- Prefer local active code patterns first when active code exists.
- Use old Khovan MAST as implementation evidence, not design authority.
- Use reference missions for syntax, bootstrap, and known-good structure only.
- Do not use reference missions to change Khovan story, pacing, factions, objectives, or player-facing behavior.
- Do not download documentation or reference missions automatically.
- Do not move old MAST files into active `scripts/`.
- Do not implement mission features while updating this inventory.
- Do not commit external reference clones.

---

## Notes from verified public references

The sbs_utils tutorial describes Cosmos missions as multi-file mission folders and identifies `script.py` and `description.txt` as required mission files. For MAST missions, it identifies `description`, `script.py`, `story.mast`, and `story.json` as required files and recommends starting from a known-good MAST mission `script.py`.

The same tutorial recommends known-good examples including Legendary Missions, Secret Meeting, and Walk The Line. These references are syntax and structure examples only.
