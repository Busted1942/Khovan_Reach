# Slice 02 Verification

Status: static foundation complete / live Cosmos smoke required
Purpose: Verify the Scenario Control Panel foundation without expanding into future admin or gameplay systems.

## What Changed

- Added `scripts/systems/scenario_control_panel.mast`.
- Added a GM-only Comms route guarded by `has_roles(COMMS_ORIGIN_ID, "gamemaster")`.
- Added safe Scenario Control Panel initialization after bootstrap state defaults.
- Added a mission overview with mission phase, scene, beat, checkpoint, held status, mode flags, and action log.
- Added separate Test Mode and Live GM Recovery Mode state display. Both remain disabled by default.
- Added hold/release controls that update `transition_held` and write action-log entries.
- Added static tests for ADMIN-001 through ADMIN-006 structure.

## What Was Not Added

- No story jumps.
- No destructive controls.
- No arbitrary variable editor.
- No checkpoint/reload.
- No Act I gameplay.
- No Kestrel/Tarsis gates.
- No drones, DAMCON, pirates, debrief, or current-objective display.
- No custom Khovan client selector.

## Evidence Boundary

Quick/static checks prove:

- expected Slice 02 source files exist
- the Scenario Control Panel module is imported and initialized after bootstrap state defaults
- Test Mode and Live GM Recovery Mode are separate flags and default false
- overview source includes mission phase, scene, beat, checkpoint, held status, mode flags, and action log
- Hold, Release, and Refresh buttons are wired to named handlers
- hold/release handlers update `transition_held`, update action-log state, and write smoke-trace lines
- active runtime files do not reintroduce the custom Khovan client selector
- active runtime files do not route directly into partial Legendary client lifecycle code
- static GM-only guard shape uses the reference-backed `has_roles(COMMS_ORIGIN_ID, "gamemaster")` pattern

Only live Cosmos smoke can prove:

- the mission actually launches in Cosmos with the current package
- the normal Cosmos/Legendary selector appears to clients
- the Game Master option appears in the live selector
- the GM can open the Khovan Scenario Control route
- Hold, Release, and Refresh produce visible GM-side behavior in the live UI
- player clients cannot see or access admin/debug controls through the live UI
- Helm can still enter console and move Artemis after Slice 02 wiring
- Change Console works, if it is explicitly exercised

## Accepted Live-Smoke Result Already Observed

Matt has already observed the Slice 01B/Slice 02 baseline through live Cosmos smoke:

- no `PLAYER_COUNT` runtime error
- no `TAB_CONSOLES` runtime error
- mission launches
- normal Cosmos/Legendary selector appears
- Game Master option appears
- Helm moves Artemis
- Dillon Clip 1 stub appears
- custom Khovan `Select a bridge console for Artemis` selector is gone

## What To Run Or Do

Static/local:

```text
python run_tests.py quick
git diff --check
```

Live Cosmos smoke:

1. Launch Khovan Reach.
2. Confirm the server reaches the playable space view.
3. Connect a client and confirm the normal Cosmos/Legendary console selector still appears.
4. Confirm the Game Master option appears.
5. Select Game Master.
6. Open Comms and look for the Khovan Scenario Control route.
7. Open the route and refresh the overview.
8. Use Hold Scene Transition, then Release Scene Transition.
9. Inspect `tests/live_startup_trace.txt`.
10. Connect or inspect a normal player console.

## Expected Observation

- No `PLAYER_COUNT` runtime error.
- No `TAB_CONSOLES` runtime error.
- No SBS Utils Page Level Runtime Error overlay.
- Normal player console selection still works.
- Helm can still move Artemis.
- Game Master can see the Khovan Scenario Control route.
- The overview includes `mission_phase`, `current_scene`, `current_beat`, `last_checkpoint`, and `transition_held`.
- Test Mode is shown as disabled unless explicitly changed by future code.
- Live GM Recovery Mode is shown as disabled unless explicitly changed by future code.
- Hold sets `transition_held` true and updates the action log.
- Release sets `transition_held` false and updates the action log.
- `tests/live_startup_trace.txt` records `[KHOVAN SCP 002]` after Hold, `[KHOVAN SCP 003]` after Release, and `[KHOVAN SCP 004]` after Refresh.
- Player consoles do not show Khovan Scenario Control or debug/admin controls.

## Failure Or Ambiguous Observation

- Any `PLAYER_COUNT` or `TAB_CONSOLES` runtime error.
- Any runtime error overlay.
- Custom `Select a bridge console for Artemis` selector appears.
- Player clients see Khovan Scenario Control or admin/debug controls.
- Game Master cannot see the Khovan Scenario Control route.
- Hold/release does not update the visible overview after refresh.
- Hold/release/refresh does not append the expected `[KHOVAN SCP ...]` trace lines.
- Normal console selection, Game Master availability, or Helm movement regresses.

## What Remains Unproven

- Static tests prove source structure only. They do not prove live Comms route visibility, GM role behavior, or live hold/release rendering.
- Static tests do not prove player clients are unable to reach the route through every possible Cosmos UI path.
- Static tests do not prove future story-transition systems will honor `transition_held`; those systems do not exist in Slice 02.
- Change Console remains unproven unless Matt explicitly exercises it during live smoke.
- Weapons torpedo-load behavior remains a known out-of-scope issue.

## Next Action By Result

- If static checks fail, fix the failing source contract before live smoke.
- If live smoke passes, commit Slice 02 foundation and proceed to review/merge planning.
- If GM cannot see the route but player clients cannot either, document the exact GM Comms route/API blocker.
- If players can see admin controls, stop and fix visibility before any Scenario Control Panel work proceeds.
- If client lifecycle regresses, revert the Slice 02 wiring and re-check Slice 01B baseline before continuing.
