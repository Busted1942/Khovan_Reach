# Slice 01 Bootstrap Findings

Status: implementation findings  
Authority: Slice 01 bootstrap/test governance only  
Scope: mission shell, package load, bootstrap state, and live-load blockers

Slice 01 implemented no Act I gameplay features. These findings record bootstrap architecture and test lessons only.

## Runtime-clean mission root

The live Cosmos mission root must contain only files that are safe for the MAST loader to discover at runtime. Git-ignored folders are not runtime-ignored.

Tier 2 reference clones, archive evidence, and old implementation material can affect live mission load if they remain under the active mission root. Runtime-clean means active startup files do not reference local clone paths, archived old-build paths, or old MAST module names, and reference folders do not expose loader-visible artifacts such as `.mastlib`, `.sbslib`, `.zip`, or archive `__init__.mast` files.

## Tier 2 references are implementation evidence only

Tier 2 repositories and reference missions are non-canonical syntax/API/reference material. They may be inspected for Cosmos, MAST, sbs_utils, bootstrap, GUI lifecycle, and file-layout patterns. They must not alter Khovan story, pacing, factions, objectives, or player-facing behavior.

## Packaging metadata

`__lib__.json` is packaging metadata, not mission feature code. Slice 01 added the reference-aligned contents:

```json
{
  "version": "v1.3.0"
}
```

This follows observed `mast_starter`, `SecretMeeting`, `WalkTheLine`, and `LegendaryMissions` packaging patterns and addresses the VS Code MAST extension folder-classification warning. Live Cosmos smoke still has to verify mission package load.

## Entry ownership

The active entry chain is:

- `story.json`
- `script.py`
- `story.mast`
- `scripts/main.mast`

`story.mast` is only the root wrapper expected by sbs_utils. Active Slice 01 runtime ownership lives in `scripts/main.mast` and the minimal system files under `scripts/systems/`.

## Runtime load-path dependency validation

Quick tests must validate active runtime dependencies, not just source hygiene. They should fail for missing active `.mast` imports, active references to external clone paths, active references to archive paths, active references to old MAST module names, and loader-visible archive entrypoints.

The observed missing old MAST dependency was:

```text
Cannot load file:
C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach\salvager_arrival.mast
```

This was a runtime load-path failure and old implementation module leak. The source was archive evidence under `archive/old_build_reference/old_mast`, especially an archive `__init__.mast` that could be auto-discovered and lead to old imports such as `salvager_arrival.mast`.

Forbidden old module examples include `salvager_arrival.mast`, `act_1_qualification.mast`, `act_1_state_helpers.mast`, `act_2_investigation.mast`, `act_3_khovan_reach.mast`, `dev_jump.mast`, and `state_save.mast`.

Old root-level or archived `damcon_timer.mast` references remain forbidden until replaced by the current active implementation. A fresh active module at `scripts/systems/damcon_timer.mast` is allowed when the DAMCON timer slice implements it under the current requirements.

## MAST GUI/task lifecycle requirement

The active StoryPage/bootstrap path must leave a yielding or long-running GUI/story task alive where practical. A Slice 01 bootstrap that completes the active map route without a wait, yield, delay, or equivalent live task can reach sbs_utils GUI presentation with no active task to present.

The observed GUI lifecycle failure was:

```text
SBS Utils Hook Level Runtime Error
EDGE CASE. Did you set END or Yield the last GUI Task?
```

This is classified as a runtime GUI/story task lifecycle failure. Static tests can verify that `scripts/main.mast` contains the intended direct wait/jump idle pattern, but live Cosmos smoke is still required to prove the sbs_utils lifecycle is satisfied.

## Static tests vs live Cosmos smoke

Static quick tests can prove file presence, JSON validity, Python parseability, active import shape, forbidden reference absence, and documented regression guards.

Static tests cannot fully prove:

- BOOT-001 live mission package load
- BOOT-012 first scene proceeds without manual admin action
- live sbs_utils StoryPage/GUI lifecycle behavior
- audio playback API behavior
- GM-only overlay visibility

Those items require live Cosmos smoke evidence or a documented blocker.

## Live failure to regression loop

Every live missing-load or runtime lifecycle failure should produce a targeted regression check when feasible. The check should protect the class of failure without hard-coding broad scenario behavior or implementing deferred gameplay.

## Slice 01 current acceptance stance

Slice 01 is not complete on quick tests alone. It requires `python run_tests.py quick` to pass and live Cosmos to load the mission, reach Scene 1, and avoid the known missing-file and GUI lifecycle errors, or it must preserve a precise blocker with next action.
