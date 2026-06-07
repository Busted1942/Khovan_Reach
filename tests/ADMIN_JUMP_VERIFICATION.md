# Admin Jump Verification

Branch: slice04-admin-jump-missionstart-posttarsis
Scope: GM-only Test Mode story jump presets for Slice 04 setup/smoke work.

## What Changed

- The GM Test Mode story jump menu now exposes exactly two active presets:
  - Mission Start
  - Post-Tarsis / Await Shakedown
- Retired future placeholder jumps are not active in the menu.
- Both presets seed accepted Slice 04 state through `scripts/acts/act1_generator_tarsis_gate.mast`.
- Neither preset creates proof stations or player-console admin controls.

## What Quick/Static Checks Prove

- `tests/test_story_jump_presets_static.py` checks that the story jump route is GM-only and Test Mode gated.
- Static checks require the registry to contain only `mission_start` and `post_tarsis_resupply`.
- Static checks require both presets to call the Slice 04 seed helpers.
- Static checks reject the retired future placeholder preset names.
- `tests/test_act1_generator_tarsis_static.py` checks that:
  - Mission Start resets zero energy, zero ordnance, active governor, held Kestrel reserve, and the Kestrel departure objective.
  - Post-Tarsis seeds cleared governor, full energy/armament requests, Tarsis completion flags, docked-state setup, and the await-shakedown objective.
  - Both helpers invalidate stale Kestrel generator-advisory timers.

## What Only Live Cosmos Smoke Can Prove

- The GM can see Khovan Scenario Control from the GM Comms console.
- Test Mode reveals Story Jumps only to the GM.
- Mission Start visibly returns Artemis to the Kestrel start condition.
- Post-Tarsis visibly gives Artemis full energy and armament and places the scenario at the await-shakedown handoff.
- The current objective text appears in the live text/comms surface after each jump.
- Repeated jumps do not leave stale Kestrel advisory messages firing in the wrong state.

## Live Smoke Procedure

Repo/branch assumption: run from `slice04-admin-jump-missionstart-posttarsis` after `python run_tests.py quick` passes.

1. Start Cosmos and load Khovan Reach.
2. On the GM Comms console, open `Khovan Scenario Control`.
3. Enable Test Mode.
4. Open `Test Mode Story Jumps`.
5. Select `Mission Start`.

Expected observation:
- Artemis is at/near Kestrel start.
- Energy is 0.
- Homing/Nuke/EMP/Mine are 0.
- Current objective says to request Kestrel departure clearance.
- Kestrel and Tarsis are present, with no proof/test station.

Failure/ambiguous observation:
- Player consoles can see admin controls.
- Energy or ordnance remains full at Mission Start.
- A retired jump such as Drill 2, Anderson, Cascade, Pirate Arrival, or Debrief appears.
- Current objective does not update, or stale Tarsis/Kestrel messages appear in the wrong state.

6. From the same GM jump menu, select `Post-Tarsis / Await Shakedown`.

Expected observation:
- Artemis is at/near Tarsis and treated as post-resupply.
- Energy is full, expected value 1000.
- Armament is full: Homing 10, Nuke 3, EMP 6, Mine 6.
- Current objective says `Await next shakedown instruction.`
- Scenario Control overview reports Act I, scene 2, post-Tarsis/await-shakedown state.

Failure/ambiguous observation:
- Energy is restored but armament is not.
- Artemis remains at Kestrel or cannot interact with Tarsis normally after the jump.
- Objective text remains on Kestrel or Tarsis docking.
- A delayed Kestrel generator advisory fires after the Post-Tarsis jump.

## What Remains Unproven

- Static tests do not prove live UI visibility, dock-state behavior, or Cosmos data-set rendering.
- The Post-Tarsis jump is an admin test seed and does not prove the real player sequence from Kestrel through normal Tarsis docking.
- Slice 05 remains intentionally unstarted.

## Commit Gate

Do not commit this branch until:

- `python run_tests.py quick` passes.
- `git diff --check` passes.
- The live smoke procedure above confirms both jumps once.
- Any failed or ambiguous live result is fixed or documented before closing the branch.
