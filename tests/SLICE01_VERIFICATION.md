# Slice 01 Verification

## Goal

Build the minimum Khovan Reach mission shell and bootstrap path. Slice 01 does not implement Act I gameplay features.

## Source sections used

- `docs/01_design/10_mast_requirements.md`, Sections 4-6
- `docs/01_design/40_admin_testing_plan.md`, BOOT-001 through BOOT-012
- `docs/01_design/50_implementation_slice_plan.md`, Slice 01
- `docs/02_content/40_dillon_clips.md`, Clip 1
- `docs/04_implementation_setup/10_mast_file_lessons.md`, old implementation evidence only
- `docs_external/00_tier2_reference_inventory.md`
- Local Tier 2 bootstrap references under `docs_external/_local_clones`
- Local Tier 2 reference missions under `reference_missions/_local_clones`
- `docs_external/_local_clones/sbs_utils/sbs_utils/mast/mast.py`, loader behavior evidence only

## Files/folders verified

- `description.txt`
- `__lib__.json`
- `script.py`
- `story.json`
- `story.mast`
- `scripts/main.mast`
- `scripts/systems/bootstrap_state.mast`
- `scripts/systems/audio_runtime.mast`
- `scripts/systems/debug_runtime.mast`
- `tests/test_bootstrap_static.py`

Old MAST files remain archive/reference only under `archive/old_build_reference/old_mast`.

## State variables

Slice 01 initializes:

- `mission_phase = act_1`
- `current_scene = 1`
- `current_beat = scene_1_bootstrap`
- `last_checkpoint = none`
- `transition_held = false`
- `test_mode_enabled = false`
- `live_recovery_mode_enabled = false`
- `generator_governor_active = true`
- `starting_homing_torpedoes = 2`
- `kestrel_generator_packet_sent = false`
- `launch_envelope_cleared = false`
- `shakedown_mode = unset`
- `training_overlay_active = true`
- `comms_archive_enabled = true`
- `dillon_clip_1_status = stubbed`

## Runtime flow

`script.py` bootstraps sbs_utils `StoryPage` using `story.mast`. `story.mast` imports `scripts/main.mast`. `scripts/main.mast` imports the three Slice 01 system files and exposes `@map/khovan_reach`.

The map route runs:

1. bootstrap state initialization
2. debug/admin visibility stub initialization
3. Dillon Clip 1 stub
4. Scene 1 bootstrap completion
5. a direct jump into a no-op runtime idle loop so the StoryPage task remains alive

The runtime idle loop now presents the temporary Slice 01 confirmation marker:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
```

This marker is not Act I gameplay and is not the Scenario Control Panel. It exists only to prove during live smoke that the bootstrap reached the initialized Scene 1 state.

## GM controls

No Scenario Control Panel is implemented in Slice 01. BOOT-010 is represented by `gm_debug_overlay_status = stubbed`.

## Player-facing behavior

Dillon Clip 1 is safely stubbed because the local environment cannot verify the Cosmos audio playback API. BOOT-011 is represented by `player_debug_controls_status = stubbed_hidden`.

## Tests or jump presets

No story jump presets are implemented in Slice 01.

`python run_tests.py quick` now runs Slice 00 source-hygiene checks plus Slice 01 static bootstrap checks.

## Acceptance criteria

- BOOT-001: mission package files exist for static verification, including reference-aligned `__lib__.json` packaging metadata.
- BOOT-002: `story.mast` imports active `scripts/main.mast`; active main imports required systems.
- BOOT-003: `story.json` is valid JSON.
- BOOT-004: `script.py` parses and has the verified `StoryPage` bootstrap shape.
- BOOT-005: minimum mission state variables initialize statically.
- BOOT-007: Dillon Clip 1 is stubbed with explicit status.
- BOOT-008: `current_scene = 1`.
- BOOT-009: `mission_phase = act_1`.
- BOOT-010: GM debug/admin overlay remains a documented stub.
- BOOT-011: player-facing debug controls remain a documented stub.
- BOOT-012: first scene bootstrap path exists statically; live runtime smoke is still required.

## Known risks or API uncertainties

Live Cosmos runtime was not executed from this environment.

Unverified until live smoke:

- exact MAST runtime execution of the imported map route
- actual audio playback API for Dillon Clip 1
- GM-only debug/admin overlay rendering
- player-facing debug tab/control hiding
- whether additional `story.json` mastlib dependencies are required for later gameplay slices
- `__lib__.json` was added as reference-aligned packaging metadata because `mast_starter`, `SecretMeeting`, `WalkTheLine`, and `LegendaryMissions` include it, simple observed mission examples use `{"version": "v1.3.0"}`, and the VS Code MAST extension warning indicates folder classification behavior. This is not Khovan design authority or mission feature code. Live Cosmos smoke must still verify mission load.

## Live Cosmos smoke evidence and runtime blockers

Quick tests are necessary but not sufficient for Slice 01 acceptance. BOOT-001 requires live mission package load evidence, and BOOT-012 requires live evidence that the first scene proceeds without manual admin action.

Live-load diagnosis must identify the active entry chain from `story.json`, `script.py`, `story.mast`, and `scripts/main.mast`. Slice 01 is not complete until `python run_tests.py quick` passes and live Cosmos load reaches Scene 1, or the remaining blocker is documented with exact error text and next action.

On May 25, 2026, a live Cosmos/MAST load attempt reported:

```text
Cannot load file __init__.mast from library C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach\docs_external\_local_clones\sbs_utils\bar.mastlib
```

Inspection found that active Khovan runtime files do not reference `docs_external/_local_clones`, `reference_missions/_local_clones`, or `bar.mastlib`. `story.json` references only `artemis-sbs.sbs_utils.v1.3.0.sbslib` and has an empty `mastlib` list. `script.py` uses the same sbs_utils `StoryPage` bootstrap shape observed in `mast_starter`, `SecretMeeting`, and `WalkTheLine`.

The likely cause is runtime contamination from local Tier 2 clone folders physically inside the mission root. The local sbs_utils MAST loader evidence shows add-on discovery walking mission subfolders for `.mastlib` and `.zip` files. The ignored reference clone `docs_external/_local_clones/sbs_utils` contains `bar.mastlib` and test `.zip` files, so those local reference artifacts can be discovered even though they are not tracked by Git and are not active Khovan code.

Slice 01 should keep Tier 2 clones outside the live mission package. Static tests now guard against active runtime references to local clone paths and against `.mastlib`, `.sbslib`, or `.zip` artifacts under mission-root reference clone staging folders.

On May 25, 2026, a second live Cosmos/MAST load attempt reported:

```text
Mast Compile Errors
File load error
Cannot load file:
C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach\salvager_arrival.mast
```

This is classified as a runtime load-path failure and old implementation module leak.

Inspection found no active Slice 01 runtime reference to `salvager_arrival.mast` in `story.json`, `script.py`, `story.mast`, or `scripts/`. The source was archived old-build evidence: `archive/old_build_reference/old_mast/__init__.mast` imported old `main.mast`, and archived old `main.mast` imported `salvager_arrival.mast`. Because sbs_utils auto-discovers `__init__.mast` files under the mission root, this archive entrypoint was load-visible during active mission startup.

The archive entrypoint was renamed to `archive/old_build_reference/old_mast/__init__.mast.archive` so the old MAST evidence remains available but cannot auto-load. Static tests now guard against `__init__.mast` files under archive/reference folders, active Slice 01 references to deferred pirate/salvager modules, and active MAST imports that point at missing files.

On May 25, 2026, a third live Cosmos load reached runtime and reported:

```text
SBS Utils Hook Level Runtime Error
EDGE CASE. Did you set END or Yield the last GUI Task?
raise Exception("EDGE CASE. Did you set END or Yield the last GUI Task?")
function: present
line: 591
File:
C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\__lib__\artemis-sbs.sbs_utils.v1.3.0.sbslib\sbs_utils\mast_sbs\maststorypage.py
```

This is classified as a runtime GUI/story task lifecycle failure.

Inspection found no active Slice 01 Scenario Control Panel, button/menu GUI, comms route, dev-jump, or copied old control-panel code. The active `StoryPage` map route completed bootstrap and then ended, leaving no running story task for the GUI page scheduler. Known-good references either keep the map flow awaiting runtime conditions or schedule long-running monitor tasks before the map route ends.

An initial attempt to schedule `khovan_reach_slice01_runtime_idle` as a separate task did not clear the live error. sbs_utils documentation states that `task_schedule()` creates a separate task, while `jump` keeps execution in the same task. Slice 01 now has `@map/khovan_reach` jump directly into `khovan_reach_slice01_runtime_idle`, a no-op loop that waits five seconds and jumps back to itself. This keeps the active StoryPage task alive without adding gameplay, GM controls, story jumps, or unstable GUI syntax. BOOT-010 remains a documented GM overlay stub/API uncertainty for a later slice.

On May 25, 2026, the GUI lifecycle error still occurred after the first direct-idle attempt. The latest stack path indicated a message/pop route rather than only the scheduler tick path:

```text
handlerhooks.py on_message
gui.pop(event.client_id)
gui.py pop
self.present(event)
page.present(event)
EDGE CASE. Did you set END or Yield the last GUI Task?
```

Further inspection found the active StoryPage entry chain:

1. `story.json` loads `artemis-sbs.sbs_utils.v1.3.0.sbslib`.
2. `script.py` registers `KhovanReachStoryPage`.
3. `KhovanReachStoryPage` loads `story.mast`.
4. `story.mast` imports `scripts/main.mast`.
5. sbs_utils `StoryPage.start_story()` defaults to a `main` label unless the page class supplies explicit entry labels.

Before this correction, `script.py` did not define explicit `main_server` or `main_client` labels. The active `@map/khovan_reach` route existed, but the StoryPage startup/pop path could still land on an empty/default startup task rather than the persistent Slice 01 map route.

The corrected lifecycle pattern is:

- `script.py` sets `main_server = "khovan_reach_slice01_entry"`.
- `script.py` sets `main_client = "khovan_reach_slice01_client_entry"`.
- `@map/khovan_reach` jumps to the same server entry.
- `khovan_reach_slice01_entry` runs bootstrap, then jumps directly to `khovan_reach_slice01_runtime_idle`.
- `khovan_reach_slice01_client_entry` jumps directly to `khovan_reach_slice01_runtime_idle`.
- `khovan_reach_slice01_runtime_idle` waits with `await delay_sim(seconds=5)` and jumps back to itself.

Quick tests now verify that the StoryPage entry labels named by `script.py` are actually defined in `scripts/main.mast`, and that the persistent idle loop is reachable from those active entry labels instead of existing only as an unreferenced label.

Live Cosmos smoke must confirm that the missing-file error and the GUI lifecycle error are gone before Slice 01 is claimed complete.

Current completion status: unresolved live Cosmos blocker until Matt confirms the mission package loads, the GUI lifecycle error is gone, and Scene 1 proceeds without manual recovery. This document records static quick checks, runtime load-path checks, live Cosmos smoke requirements, and unresolved blockers separately.

On May 25, 2026, Matt confirmed the previous SBS Utils GUI lifecycle error no longer appears. Current observed live behavior is that the mission loads to a blank/quiet Mission Select screen. The remaining Slice 01 smoke question is whether the bootstrap actually reached Scene 1.

The required next live smoke is to confirm that the marker `Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.` appears, or that an equivalent log marker proves the same entry path ran.

## Slice 01 findings

The active mission package now has a minimal bootstrap shell. Active `scripts/` contains only new Slice 01 bootstrap code and placeholder `.gitkeep` files. It does not contain old archived MAST files.

External Tier 2 clones remain ignored and untracked.

## Next recommended action

Run a live Cosmos smoke test for BOOT-001 through BOOT-012 before starting Slice 02 or any Act I gameplay feature coding.
