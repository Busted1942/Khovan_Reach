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

## BOOT coverage audit

| ID | Requirement | Classification | Evidence / rationale |
| --- | --- | --- | --- |
| BOOT-001 | Mission package loads | implemented and live-smoked | Cosmos loaded Khovan without the previous missing-file or SBS Utils GUI lifecycle errors. The visible Slice 01 marker and `tests/live_smoke_last_bootstrap.txt` prove the active package/startup path ran. |
| BOOT-002 | `main.mast` imports/includes required files or documented equivalent | implemented and live-smoked | `story.mast` imports `scripts/main.mast`; `scripts/main.mast` imports bootstrap, audio, and debug system files. The live visible marker is emitted from `scripts/main.mast` after those system tasks run. |
| BOOT-003 | `story.json` is valid | implemented static-only | Quick tests validate JSON shape and expected sbs_utils dependency. Live load indirectly uses it, but JSON validity remains a static/parser check. |
| BOOT-004 | `script.py` initializes without runtime error | implemented and live-smoked | The marker file is written by `KhovanReachStoryPage.start_story()` after sbs_utils starts the configured StoryPage path. |
| BOOT-005 | Mission state variables initialize | implemented static-only | Quick tests validate the full Slice 01 state set. Live smoke directly proves the `mission_phase=act_1` and `current_scene=1` surface markers; broader defaults remain static-only. |
| BOOT-006 | Artemis starts with correct ship state | missing | Active Slice 01 does not create a sim world, spawn Artemis, assign clients to a ship, or apply live ship state. This is the smallest remaining Slice 01 runtime primitive if BOOT-006 must be satisfied before completion. |
| BOOT-007 | Dillon Clip 1 queues, plays, or stubs | intentionally stubbed | `scripts/systems/audio_runtime.mast` sets `dillon_clip_1_status = "stubbed"`. Real audio playback API remains unverified and is not implemented. |
| BOOT-008 | `current_scene = 1` | implemented and live-smoked | Bootstrap state sets `current_scene = 1`; live marker file records `current_scene=1`; visible marker appeared without admin/recovery action. |
| BOOT-009 | `mission_phase` valid | implemented and live-smoked | Bootstrap state sets `mission_phase = "act_1"`; live marker file records `mission_phase=act_1`. |
| BOOT-010 | GM debug/admin overlay visible to GM | API uncertainty/spike | `gm_debug_overlay_status = "stubbed"` exists, but no GM overlay is rendered. GUI/admin implementation remains unsafe to invent and belongs in a focused later spike or Slice 02 foundation. |
| BOOT-011 | Player-facing debug controls hidden | implemented static-only | No active player debug/admin routes or Scenario Control Panel controls are present. `player_debug_controls_status = "stubbed_hidden"` documents intent. |
| BOOT-012 | First scene proceeds without manual admin action | implemented and live-smoked | Live load reached the Slice 01 status marker and marker file without manual admin/recovery controls. This proves bootstrap Scene 1 proceeds; playable Artemis/console state remains separate under BOOT-006. |

Smallest remaining Slice 01 implementation work:

1. BOOT-006: add a minimal, reference-backed runtime primitive for Artemis/player ship setup if Slice 01 completion requires live ship state. This likely needs `sim_create`, a player ship spawn or `spawn_players`, starting torpedo/state application, and possibly client assignment/console routing. It should be approved as a focused Slice 01 bootstrap patch before implementation.
2. BOOT-010: leave as API uncertainty/spike unless Slice 01 explicitly requires visible GM overlay before Slice 02. Do not build Scenario Control Panel in Slice 01.
3. BOOT-007: current stub is acceptable only as an intentional stub; real audio playback remains a later API verification item.

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

Live Cosmos smoke had to confirm that the missing-file error and the GUI lifecycle error were gone before Slice 01 could be evaluated further.

That blocker was later cleared by live marker evidence. This document records static quick checks, runtime load-path checks, live Cosmos smoke requirements, and remaining coverage gaps separately.

On May 25, 2026, Matt confirmed the previous SBS Utils GUI lifecycle error no longer appears. Current observed live behavior is that the mission loads to a blank/quiet Mission Select screen. The remaining Slice 01 smoke question is whether the bootstrap actually reached Scene 1.

The generic default server welcome screen is not required for Khovan mission load. The absence of the previous SBS Utils runtime error is progress, but it is not sufficient Slice 01 acceptance evidence.

Matt also observed that `mast.runtime.log` and `mast.compile.log` exist but remain empty after live load. Log-only smoke evidence is therefore unreliable in this setup.

Logging triage on May 25, 2026 found that the local `docs_external/_local_clones` and `reference_missions/_local_clones` folders are not present inside the live mission root, which is intentional runtime-root hygiene. Available installed/reference evidence shows:

- sbs_utils creates `mast.compile.log` and `mast.runtime.log` file handlers when a MAST story is compiled.
- `mast.compile.log` may remain empty when there are no compile diagnostics.
- MAST `log(...)` defaults to DEBUG-level logging; without an enabled logger, marker text may not appear even when the file exists.
- Reference mission code uses the MAST `logger(...)` command to enable logging.

Slice 01 now enables the `mast.runtime` logger immediately before the bootstrap log marker with `logger("mast.runtime")`, but this is still secondary diagnostics until live Cosmos proves that this local launch path writes runtime logs. Logging remains a future diagnostics spike if richer runtime traces are needed.

The visible story-dialog marker remains useful if Cosmos displays it after the bootstrap state, debug stub, and Dillon Clip 1 stub have run:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
```

The visible marker is emitted from the active Slice 01 bootstrap path with the reference-backed `sbs.send_story_dialog(...)` pattern used by known-good missions. On the May 25 live smoke, this marker was not observable, so it is not sufficient as the only evidence.

Primary next live-smoke proof is the Python-side marker file written after the active sbs_utils `StoryPage.start_story()` startup tick returns for the server page:

```text
tests/live_smoke_last_bootstrap.txt
```

Expected marker-file content includes:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
mission_phase=act_1
current_scene=1
```

This marker is the accepted Slice 01 live-smoke proof. It is temporary Slice 01 smoke scaffolding, not mission gameplay, not player debug control, and not Scenario Control Panel behavior. The file is Git-ignored and must not be committed.

Secondary log marker, if Cosmos begins writing runtime logs:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized. mission_phase = act_1; current_scene = 1.
```

The active bootstrap still emits this marker with `logger("mast.runtime")` followed by `log(..., "mast.runtime")`, but the empty-log observation means `mast.runtime.log` and `mast.compile.log` are secondary evidence only. Quick tests must not require either log file to contain output unless logging is separately proven reliable in this Cosmos launch path.

For the next live smoke, Matt should check `tests/live_smoke_last_bootstrap.txt` after launch/reload. Failure or ambiguous observations are: blank screen with no visible marker, marker file absent, marker file timestamp unchanged after relaunch, marker file missing the exact state lines, logs still empty with no alternate marker, or any runtime error.

## Runtime/server-load observation after bootstrap marker

Matt confirmed the live-smoke marker file is written with:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
mission_phase=act_1
current_scene=1
entry_chain=story.json -> script.py -> story.mast -> scripts/main.mast -> khovan_reach_slice01_entry
```

This proves the active Khovan StoryPage startup path runs far enough for Slice 01 bootstrap smoke evidence. It does not prove the server/client playable state.

Reference inspection found that known-good playable examples use additional runtime primitives that Slice 01 has not yet implemented:

- `SecretMeeting` and `WalkTheLine` use `@map` metadata, LegendaryMissions mastlib dependencies, map start flow, `spawn_players`, docking/setup helpers, and actual world objects.
- `tutorial_runner-main/mast/simple_common.mast` uses `sim_create()`, `player_spawn(...)`, `assign_client_to_ship(...)`, `gui_reroute_server(...)`, `gui_reroute_clients(...)`, `route_change_console(...)`, a server GUI label, and client console selection before player consoles are useful.
- Archived old Khovan MAST also treated Artemis setup as a separate runtime step using `spawn_players`, start-state setters, and Kestrel/Tarsis objects. That old code remains implementation-history evidence only.

Current active Slice 01 code deliberately does not create a simulation world, spawn Artemis, assign a client to a ship, route clients to Helm/Science/Comms/etc., or create the server mission-control surface. Therefore a blank/quiet server screen with the marker file present is currently classified as:

```text
bootstrap route passed; server/client playable state unresolved
```

It is not a missing-file failure and not the previous SBS Utils GUI lifecycle failure.

The next operator test should distinguish these observations:

- Server only: may remain blank/quiet in the current bootstrap shell. Do not treat the generic default server welcome screen as required after Khovan registers its own StoryPage.
- Client connected: useful for diagnosis, but current Slice 01 does not spawn Artemis or assign consoles, so no usable ship/consoles should be assumed yet.
- Marker file: remains the accepted proof that the active bootstrap path ran.

The likely missing runtime primitive is a minimal Slice 01 server/client setup, probably including some combination of `sim_create`, Artemis/player-ship spawn or `spawn_players`, client ship assignment/console routing, and a small server status page. Because this is the first real runtime primitive and BOOT-006 requires Artemis to start with correct ship state, it should be implemented only as an explicitly approved Slice 01 bootstrap patch or spike. It must not silently import Act I gameplay, Kestrel/Tarsis/drone flow, story jumps, or Scenario Control Panel behavior.

Current completion stance:

```text
Mission bootstrap marker: passed.
Server/client playable state: not yet passed.
BOOT-006 Artemis starts with correct ship state: not yet implemented.
BOOT-012 first scene proceeds without manual admin action: passed for bootstrap status marker.
```

## MAST import warning triage

VS Code MAST language-server warnings on import lines such as `import scripts/systems/bootstrap_state.mast`, `import scripts/systems/audio_runtime.mast`, and `import scripts/systems/debug_runtime.mast` are classified as non-blocking editor false positives unless live Cosmos reports a matching compile/load failure.

References inspected:

- `docs_external/_local_clones/mast_starter/story.mast`, via the external Tier 2 cache
- `reference_missions/_local_clones/SecretMeeting/story.mast`, via the external Tier 2 cache
- `reference_missions/_local_clones/WalkTheLine/story.mast`, via the external Tier 2 cache
- `archive/old_build_reference/old_mast/main.mast`
- `sbs_utils/sbs_utils/mast/core_nodes/import_cmd.py`, via the external Tier 2 cache
- `sbs_utils/tests/test_mast.py`, via the external Tier 2 cache

The checked Story mission examples mostly use same-folder imports. The archived old Khovan `main.mast` also uses same-folder imports. However, the sbs_utils import parser explicitly accepts `/` and `\` in import names, and the sbs_utils test suite includes successful compile examples for both `import tests/mast/imp.mast` and `import tests\mast\imp.mast`.

Conclusion: slash-style imports are valid MAST runtime syntax. The active import lines remain unchanged.

## Slice 01 findings

The active mission package now has a minimal bootstrap shell. Active `scripts/` contains only new Slice 01 bootstrap code and placeholder `.gitkeep` files. It does not contain old archived MAST files.

External Tier 2 clones remain ignored and untracked.

## Next recommended action

Run a live Cosmos smoke test for BOOT-001 through BOOT-012 before starting Slice 02 or any Act I gameplay feature coding.
