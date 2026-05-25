# Slice 01 Verification

Status: verification record template / Slice 01 evidence log
Purpose: Separate static quick checks, MAST compile/preflight checks, runtime load-path checks, live Cosmos smoke, unresolved blockers, and completion status.

---

# Evidence classes

- Static quick checks: source hygiene, expected files, forbidden references, parser/schema checks where available.
- MAST compile/preflight checks: installed SBS Utils / MAST compiler evidence where available. This is a middle evidence class: stronger than text-only static checks, but it does not prove runtime variable values, GUI/page lifecycle, renderer behavior, player assignment, client console transition, or playability.
- Runtime load-path checks: active startup/import/include path points only to allowed existing files.
- Live Cosmos smoke: actual Cosmos/MAST mission load and Scene 1 behavior.
- Blocker checkpoint: documented failure that is intentionally preserved for investigation, not claimed complete.

# do not claim live cosmos success unless cosmos was actually run and passed.

## live cosmos smoke evidence and runtime blockers

quick tests are necessary but not sufficient.
Slice 01 static checks are necessary but not sufficient.

`python run_tests.py quick` currently covers source hygiene, package/static checks, selected runtime-load-path checks, and MAST compile/preflight checks when the installed SBS Utils compiler API is available. It does not by itself prove that Cosmos can load the mission, that SBS Utils GUI tasks remain alive, that clients can enter a console, or that Scene 1 proceeds without manual recovery.

Live Cosmos smoke remains required for:

- BOOT-001 mission package loads
- BOOT-010 GM debug/admin overlay visible to GM, if implemented in this slice
- BOOT-011 player-facing debug controls hidden, if implemented in this slice
- BOOT-012 first scene proceeds without manual admin action

The live-smoke marker file is `tests/live_smoke_last_bootstrap.txt`.

`tests/live_smoke_last_bootstrap.txt` is a last-success audit marker. It is written after Slice 01A reaches `[KHOVAN BOOT 010] playable bootstrap complete`. It should not be used as an early crash trace.

`tests/live_startup_trace.txt` is the append-only early startup breadcrumb trace. It is written and flushed before and after risky Python and MAST startup steps. If live Cosmos crashes before the last-success audit updates, inspect this trace first. If the trace does not update at all, the active startup path is earlier or different than assumed.

### VS Code MAST extension `__init__.mast` warning

The VS Code MAST extension may warn:

```text
No '__init__.mast' file found in this folder.
```

This is classified as a tooling/convenience warning for the current Slice 01 runtime, not a live Cosmos blocker. Live Slice 01 startup uses:

```text
story.json -> script.py -> story.mast -> scripts/main.mast -> khovan_reach_slice01_entry
```

Current active runtime files do not import or load `__init__.mast`, and live Cosmos has already displayed the Slice 01 bootstrap marker without a missing-`__init__.mast` runtime error. Do not create an active `__init__.mast` only to silence the editor warning, and do not copy the archived old-build `__init__.mast` into active runtime.

### Live failure: missing old MAST dependency

Observed error:

```text
Cannot load file:
C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach\salvager_arrival.mast
```

Classification:

- runtime load-path failure
- old implementation module leaked into active bootstrap path
- not a design change

Resolution requirement:

- active Slice 01 bootstrap must not load old Act II/III or pirate/salvager modules
- active runtime files must not reference `salvager_arrival.mast`
- quick tests must include a regression check for forbidden old module references and missing `.mast` dependencies

### Live failure: SBS Utils GUI task lifecycle

Observed error:

```text
SBS_Utils runtime error
SBS Utils hook level runtime error
EDGE CASE. Did you set END or Yield the last GUI Task?
maststorypage.py line 591 in present
```

Classification:

- runtime GUI/story task lifecycle failure
- mission reaches SBS Utils but the active GUI/story task appears to end without a valid yield/long-running task
- not a Khovan scenario design change

Resolution requirement:

- identify the actual active entry chain from `story.json` / `script.py` / `story.mast` to `scripts/main.mast`
- ensure the active bootstrap reaches a reference-backed yielding or long-running GUI/story task
- quick tests should verify the task is connected to the active entry route where practical
- live Cosmos smoke must confirm the error is gone

### Evidence rule

Do not mark Slice 01 complete until:

- `python run_tests.py quick` passes
- active runtime load-path checks pass
- live Cosmos mission load reaches Scene 1 without manual recovery, or
- an exact blocker is documented with next action and the commit is explicitly marked as a blocker/investigation checkpoint

## Slice 01A minimum playable bootstrap evidence

Slice 01A minimum playable bootstrap has been live-smoked with constraints.

Matt's current live smoke confirms:

- mission launches without missing-file/package/import/GUI lifecycle errors
- server reaches playable/ready state
- two clients can connect
- Khovan console selection works
- Helm console can move Artemis
- Dillon Clip 1 text stub is active
- `mission_phase = act_1`
- `current_scene = 1`

This is accepted as Slice 01A minimum playable bootstrap evidence. It is not Act I gameplay acceptance and it does not prove Weapons/ordnance readiness.

Implemented static evidence:

- server entry chain remains `story.json -> script.py -> story.mast -> scripts/main.mast -> khovan_reach_slice01_entry`
- `scripts/systems/playable_bootstrap.mast` now uses the local tutorial/reference pattern: `sim_create()`, `player_spawn(...)`, `assign_client_to_ship(...)`
- the spawn step is surrounded by BOOT 006 sub-step trace markers so any repeat crash identifies the exact failing sub-step
- `script.py` routes clients through the Khovan StoryPage, matching local known-good MAST mission startup shape
- `scripts/main.mast` provides a minimal reference-backed client console selection route using `assign_client_to_ship(client_id, artemis_id)` and `gui_console(console_select)`
- `mission_phase = act_1`
- `current_scene = 1`
- Dillon Clip 1 is represented by an operator-visible text stub
- no Scenario Control Panel, story jumps, Act I gates, Tarsis gates, drones, DAMCON, pirates, cache run, debrief, or current-objective display is loaded
- player-facing debug/admin controls are not introduced

Expected Slice 01A marker text:

```text
Khovan Reach Slice 01A playable bootstrap loaded. Scene 1 initialized.
Artemis player ship initialized with reference-backed sim_create/player_spawn pattern.
Dillon Clip 1 text stub active.
Mission shell active. No Act I gameplay systems loaded.
```

Live Cosmos smoke has proved for Slice 01A:

- fresh mission load reaches the Slice 01A marker without missing-file/package/import/GUI lifecycle errors
- the client no longer remains on Mission Select / Options with only diagnostic text
- Artemis/player ship is client-selectable after the reference-backed spawn and client route
- Helm can move Artemis
- Dillon Clip 1 text stub is visible enough for operator acceptance

Remaining unproven after Slice 01A live smoke:

- Weapons torpedo loadout/UI behavior
- full Act I gates, Kestrel/Tarsis flow, drones, Scenario Control Panel, story jumps, DAMCON, pirates, cache run, debrief, and current-objective display

### Slice 01A known issue: Weapons torpedo-load client crash

Observed after the accepted Slice 01A minimum playable smoke:

```text
Microsoft Visual C++ Runtime Library
Assertion failed!
Program: ...\Cosmos\Artemis3-x64-release.exe
File: D:\PaxDev\Artemis3\Artemis3\imguiArt3.cpp
Line: 1482
Expression: '!list.empty() && "uiDropDownList; list is empty."'
```

Trigger:

- Weapons client attempts to load a torpedo.

Classification:

- known issue outside Slice 01A minimum playable bootstrap
- likely missing or invalid torpedo inventory / player ship ordnance configuration
- does not block Slice 01A unless Slice 01A acceptance is expanded to include Weapons/torpedo gameplay

Required future resolution:

- resolve before Act I Weapons/Tarsis/ordnance/drone slices depend on torpedo loading
- use reference-backed loadout/ordnance initialization; do not invent torpedo UI or loadout syntax

### Slice 01A live-smoke finding: stable diagnostic shell is not playable

Observed live behavior after the shader crash fix:

- Khovan no longer hard-crashes.
- The visible marker says Artemis/player ship initialized and Dillon Clip 1 stub active.
- The UI remains on Mission Select / Options with diagnostic text.

Classification:

- stable diagnostic shell
- not yet playable Scene 1
- remaining boundary is client/page/bridge transition after player ship initialization

Current fix attempt:

- remove direct `ClientSelectPage` registration from `script.py`
- register `KhovanReachStoryPage` for both server and client, matching local known-good MAST mission startup
- add `khovan_reach_slice01_client_main` as a minimal bridge-console selector
- add `khovan_reach_slice01_console_selected` to assign the connected client to Artemis and call `gui_console(console_select)`
- replace the server-side diagnostic idle page with `khovan_reach_slice01_server_playable`
- use the local tutorial / Legendary console pattern: `sim_resume()`, `assign_client_to_ship(0, artemis_id)`, `link(artemis_id, "consoles", client_id)`, and `gui_console("mainscreen")`
- move the last-success marker write until after the server route reaches the mainscreen console transition
- add BOOT 007A-D trace markers around the client/page playable transition and player/client assignment confirmation
- add ROUTE 001-003 trace markers around map selection and the server playable transition

Reference missions inspected for this boundary:

- SBS Utils MAST tutorial: map labels are selected from Mission Select, and player ships are handled from the selected map with `await task_schedule(spawn_players)`.
- `../tutorial_runner-main/mast/simple_common.mast`: server startup uses `sim_create()`, `player_spawn(...)`, `assign_client_to_ship(...)`, `sim_resume()`, and client console selection with `gui_console(console_select)`.
- `../secretmeeting/story.mast` and `../walktheline/story.mast`: selected map routes schedule player spawning from the map route.
- `../legendarymissions/consoles/server_console.mast`: server transition uses `sim_resume()`, assigns the server client to a player ship, then calls `gui_console("mainscreen")`.

Mismatch found:

- Khovan had a valid player-ship bootstrap, but the selected map route returned to a diagnostic StoryPage loop instead of entering a playable console route. That explains why the live UI stayed on Mission Select / Options with Khovan text.

Expected next live-smoke observation:

- fresh Khovan mission load produces no missing-file, package/import, GUI lifecycle, or shader crash errors
- the selected Khovan map reaches the server mainscreen console route instead of remaining on Mission Select / Options with only diagnostic text
- a connected client enters the Khovan StoryPage console selector and can select a bridge console for Artemis
- `tests/live_startup_trace.txt` includes `[KHOVAN ROUTE 003] playable bridge transition reached`
- `tests/live_smoke_last_bootstrap.txt` updates only after the server playable transition marker is reached

### Slice 01A live-smoke failure: Artemis id not shared into assignment routes

Observed live progress:

- fresh server load reached the server playable route
- connected client reached the Khovan console selector
- selecting a console failed before entering a usable bridge console

Observed errors:

```text
scripts/main.mast line 43
label khovan_reach_slice01_server_playable
assign_client_to_ship(0, artemis_id)
name 'artemis_id' is not defined

scripts/main.mast line 72
label khovan_reach_slice01_console_selected
assign_client_to_ship(client_id, artemis_id)
name 'artemis_id' is not defined
```

Classification:

- runtime variable-scope failure
- `artemis_id` was created by the playable-bootstrap helper, but the assignment routes in `scripts/main.mast` could not see it
- client reached the console selector, which is progress, but this is not full Slice 01A success

Reference comparison:

| Reference | Reference ship-id pattern | Khovan mismatch | Fix |
| --- | --- | --- | --- |
| `../tutorial_runner-main/mast/simple_common.mast` | `shared artemis = to_id(player_spawn(...))`, then `assign_client_to_ship(client_id, artemis)` and `gui_console(console_select)` | Khovan assigned to `artemis_id` from `main.mast`, but the visible shared declaration lived in `playable_bootstrap.mast` | declare `shared artemis_id = 0` in `scripts/main.mast` and write to `shared artemis_id` from the bootstrap helper |
| `../khovan_reach_old/scripts/main.mast` | top-level `shared artemis_id = 0` in the same active MAST file that later uses the id | new Slice 01A moved the declaration into an imported helper | restore the id declaration to `scripts/main.mast` without copying old gameplay |
| `../legendarymissions/consoles/server_console.mast` | assign client 0 to the first player ship, then use `gui_console("mainscreen")` | server assignment syntax is reference-backed, but the id variable was unavailable | keep server-side assignment and fix storage |

Current fix attempt:

- `scripts/main.mast` now owns `shared artemis_id = 0`
- `scripts/systems/playable_bootstrap.mast` writes to `shared artemis_id` after spawn/bind
- console selection adds:
  - `[KHOVAN ROUTE 004] console selected`
  - `[KHOVAN ROUTE 005] client assigned to Artemis`
- quick tests fail if assignment routes use `artemis_id` without the shared declaration / shared write pattern

Acceptance requirement:

- fresh server load must not produce the server-side `artemis_id` error
- client console selection must enter a usable bridge console without `artemis_id` runtime errors
- quick tests remain static only; live Cosmos must prove the assignment succeeds

### Slice 01A live-smoke failure: undefined player ship name

Observed live Cosmos error:

```text
mast RUNTIME ERROR
line 24 in file scripts/systems/playable_bootstrap.mast
label khovan_reach_initialize_playable_bootstrap
name 'artemis_ship_name' is not defined
```

Classification:

- real Slice 01A runtime failure
- player-ship bootstrap referenced a top-level MAST shared/config variable that was not available when the spawn expression evaluated
- quick tests forbid the known-bad `artemis_ship_name` identifier in active startup MAST

Fix attempt:

- remove the `artemis_ship_name` dependency
- the later shader-crash finding required adding `sim_create()` before the literal `player_spawn(...)` pattern and surrounding the ship path with BOOT 006 sub-step trace markers
- keep the branch in live-smoke-required status until Cosmos confirms both runtime errors are gone

### Slice 01A live-smoke failure: Khovan-only shader crash

Observed live behavior:

- Cosmos/Artemis launches normally outside Khovan.
- The crash occurs only when loading the Khovan mission.
- Visible error: `Missing Shader File data/PaxDefault/shader-2dnormal.vs`.
- Event Viewer reports `Artemis3-x64-release.exe` crashing during or after Khovan mission load.

Trace evidence:

```text
[KHOVAN BOOT 005] playable_bootstrap entered
[KHOVAN BOOT 006] before Artemis/player ship init or confirmation
```

The trace did not reach `[KHOVAN BOOT 007]`, so the crash happened inside the Artemis/player-ship initialization block. This was after `script.py`, `story.mast`, `scripts/main.mast`, and bootstrap state had all entered.

Classification:

- Khovan-specific live runtime crash
- not a global Cosmos launch failure
- quick/preflight could not prove the renderer/client/player-spawn behavior
- static checks can require the reference-backed `sim_create()` / `player_spawn(...)` / `assign_client_to_ship(...)` shape, but live Cosmos remains required

Current fix attempt:

- use the local tutorial/reference startup order: `sim_create()` before `player_spawn(...)`
- bind an existing TSN player ship if one already exists, otherwise create Artemis with the reference-backed player-spawn pattern
- assign the server client to Artemis after role/name assignment
- keep Dillon Clip 1 text stub, `mission_phase = act_1`, and `current_scene = 1`
- keep Slice 01A incomplete until live Cosmos confirms the Khovan-only shader crash is gone

## MAST compile/preflight evidence

Local installed source evidence:

- `../__lib__/artemis-sbs.sbs_utils.v1.3.0.sbslib/sbs_utils/mast_sbs/maststorypage.py` uses `MastStory().from_file(story_file, None)` to collect compiler errors before presentation.
- `../__lib__/artemis-sbs.sbs_utils.v1.3.0.sbslib/sbs_utils/mast/mast.py` exposes `Mast.from_file(...)` and `Mast.compile(...)`.

Quick-suite use:

- `tests/test_mast_compile_or_preflight.py` extracts the installed sbslib to a temporary directory, imports the MastStory preflight API, registers SBS/GUI story nodes, points `sbs_utils.fs.script_dir` at the Khovan mission root, and compiles `story.mast`.
- This preflight covers the active import chain into `scripts/main.mast` and `scripts/systems/playable_bootstrap.mast`.
- The preflight is compile/static evidence only. It does not evaluate runtime expressions or prove Cosmos UI/player-ship behavior.
- The known `artemis_ship_name` failure was a runtime undefined-variable failure, so quick also includes a direct regression check forbidding that known-bad identifier in active startup MAST.

## Slice 01A early startup trace

Trace file:

```text
tests/live_startup_trace.txt
```

Expected Python-side breadcrumbs:

```text
[KHOVAN EARLY 001] script.py entered
[KHOVAN EARLY 002] before sbs_utils import
[KHOVAN EARLY 003] after sbs_utils import
[KHOVAN EARLY 004] before client StoryPage setup
[KHOVAN EARLY 005] after client StoryPage setup
[KHOVAN EARLY 006] before story.mast load/handoff
[KHOVAN EARLY 007] after story.mast load/handoff
```

Expected MAST-side breadcrumbs:

```text
[KHOVAN BOOT 001] scripts/main.mast entered
[KHOVAN BOOT 002] before state defaults
[KHOVAN BOOT 003] after state defaults
[KHOVAN BOOT 004] before playable_bootstrap
[KHOVAN BOOT 005] playable_bootstrap entered
[KHOVAN BOOT 006] before Artemis/player ship init or confirmation
[KHOVAN BOOT 006A] before sim_create
[KHOVAN BOOT 006B] after sim_create
[KHOVAN BOOT 006C] before existing player ship query
[KHOVAN BOOT 006D] after existing player ship query
[KHOVAN BOOT 006E] before ship spawn call
[KHOVAN BOOT 006F] after ship spawn call
[KHOVAN BOOT 006H] before ship role/name assignment
[KHOVAN BOOT 006I] after ship role/name assignment
[KHOVAN BOOT 006J] before client/player assignment
[KHOVAN BOOT 006K] after client/player assignment
[KHOVAN BOOT 007] after Artemis/player ship init or confirmation
[KHOVAN BOOT 008] Dillon Clip 1 stub/queue reached
[KHOVAN BOOT 009] mission_phase=act_1 current_scene=1
[KHOVAN BOOT 010] playable bootstrap complete
```

Failure interpretation:

- no trace update: `script.py` did not enter, the file path is wrong, or Cosmos loaded a different mission copy
- last EARLY marker only: failure happened before MAST bootstrap reached `scripts/main.mast`
- last BOOT marker identifies the last successful MAST startup step before a crash
- last-success audit without complete trace means the trace wiring must be investigated before accepting live smoke

## Operator-facing live-smoke expectation

When asking the operator to run Slice 01 live smoke, include:

```text
What changed:
What to run or do:
Expected observation:
Failure/ambiguous observation:
What remains unproven:
Next action by result:
```

Expected live-smoke observation should include a Khovan-specific visible or logged marker, for example:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
mission_phase=act_1
current_scene=1
```

Failure or ambiguous observations include:

```text
blank screen with no marker
empty mast.runtime.log or mast.compile.log when a marker was expected
default server screen appears but no Khovan marker appears
no error but no proof the Khovan startup route ran
```

If the check is a negative control, state which failure is expected and when that expected failure means the control passed.
