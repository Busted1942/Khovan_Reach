# Slice 03 Verification

Status: static framework complete / live Cosmos smoke required
Purpose: Verify the Story-jump preset framework without expanding into Act I gameplay, destructive controls, checkpoint reload, or player-facing jump UI.

## What Changed

- Added `scripts/systems/story_jump_presets.mast`.
- Added a GM-only Test Mode story-jump submenu under the existing Scenario Control Panel.
- Added Test Mode enable/disable controls while keeping Live GM Recovery Mode separate and disabled by default.
- Added six initial preset IDs:
  - `mission_start`
  - `drill_2_guided_contact`
  - `anderson_orders`
  - `cascade_decision`
  - `pirate_arrival_cover_intact`
  - `debrief`
- Added structured preset metadata fields for each preset.
- Added a common preset executor that updates mission state markers, increments `story_jump_generation_id`, writes GM summary state, appends the Scenario Control action log, and writes `[KHOVAN JUMP ...]` smoke-trace lines.
- Marked future-system presets as framework-only where the supporting gameplay systems are not implemented yet.
- Added Slice 03 static checks to `python run_tests.py quick`.

## What Was Not Added

- No actual Act I gates.
- No Kestrel/Tarsis gameplay.
- No drone or combat mechanics.
- No DAMCON timer.
- No pirate state machine gameplay.
- No cache run.
- No debrief UI.
- No destructive controls.
- No arbitrary variable editor.
- No production checkpoint/reload.
- No normal player-facing story-jump controls.
- No custom Khovan client selector.

## What Quick/Static Checks Prove

- `story_jump_presets.mast` exists, imports, and initializes from the active bootstrap path.
- The six required preset IDs exist.
- Each preset has required metadata fields.
- Story-jump controls are under a GM-only Comms route.
- Story-jump controls are gated by `test_mode_enabled`.
- Test Mode and Live GM Recovery Mode remain separate.
- The common executor increments `story_jump_generation_id`.
- The common executor writes validation summary state and Scenario Control action-log state.
- Framework presets do not spawn drones, pirates, DAMCON, debrief UI, or other future systems.
- Active runtime files do not reintroduce the custom Khovan selector.
- Active runtime files do not directly route to `common_console_select.client_main`.
- Active runtime files do not restore direct client-side `assign_client_to_ship` / `gui_console(console_select)` flow.

## What Only Live Cosmos Smoke Can Prove

- The mission launches with the Slice 03 imports present.
- The normal Cosmos/Legendary selector still appears.
- The Game Master option still appears.
- Helm/player consoles still work and can move Artemis.
- The Scenario Control Panel still appears only to the GM.
- Test Mode controls appear only to the GM.
- The Test Mode story-jump submenu appears only after Test Mode is enabled.
- Preset buttons produce visible GM-side summaries.
- `[KHOVAN JUMP ...]` trace lines appear in `tests/live_startup_trace.txt`.
- Player consoles do not see story-jump controls.
- Change Console works, if explicitly tested.

## Live Smoke Checklist

1. Launch Khovan Reach fresh.
2. Confirm no `PLAYER_COUNT` or `TAB_CONSOLES` runtime error.
3. Confirm server reaches the playable space view.
4. Connect a player client.
5. Confirm normal selector appears.
6. Select Helm and confirm Artemis can move.
7. Open Game Master.
8. Confirm Khovan Scenario Control appears.
9. Confirm Story Jump controls are not shown until Test Mode is enabled.
10. Enable Test Mode.
11. Open Test Mode Story Jumps.
12. Trigger `mission_start`.
13. Confirm the GM receives a story-jump summary.
14. Inspect `tests/live_startup_trace.txt` for a `[KHOVAN JUMP ...] mission_start` line.
15. Trigger each framework-only preset one at a time only if the mission remains stable.
16. Confirm each framework-only preset reports that gameplay systems are not implemented yet.
17. Confirm player consoles do not see story-jump controls.

## Expected Observation

- No runtime error overlay.
- No custom Khovan `Select a bridge console for Artemis` selector.
- Normal selector and Game Master option remain available.
- Helm can move Artemis.
- Test Mode can be enabled and disabled from the GM-only panel.
- Test Mode Story Jumps appears only while Test Mode is enabled.
- `mission_start` reports a valid framework seed for Scene 1.
- Future presets report framework-only warnings instead of pretending to run unsupported gameplay.
- `tests/live_startup_trace.txt` records `[KHOVAN JUMP ...]` entries when presets are triggered.
- Player clients do not see jump controls.

## Failure Or Ambiguous Observation

- Any `PLAYER_COUNT` or `TAB_CONSOLES` runtime error.
- Any runtime error overlay.
- Story-jump controls visible to player consoles.
- Test Mode Story Jumps visible while Test Mode is disabled.
- Preset selection shows no GM confirmation and writes no trace line.
- Future presets silently imply completed gameplay systems that are not implemented.
- Normal console selection, Game Master availability, or Helm movement regresses.

## What Remains Unproven

- Static tests do not prove live Comms rendering or button execution.
- Static tests do not prove every future seeded state is complete.
- Framework-only presets do not prove Act I gates, drones, DAMCON, pirates, cache run, or debrief behavior.
- Change Console remains unproven unless Matt explicitly exercises it during live smoke.
- Weapons torpedo-load behavior remains a known out-of-scope issue.

## Next Action By Result

- If quick/static checks fail, fix source structure before live smoke.
- If live smoke passes, Slice 03 can move to review/merge planning.
- If GM cannot see Test Mode controls, document the exact Scenario Control / Comms route blocker.
- If players can see story-jump controls, stop and fix visibility before proceeding.
- If framework presets imply unsupported gameplay, revise the preset summary/validation wording before committing.
