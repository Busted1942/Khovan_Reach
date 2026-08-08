# Admin Jump Verification

Branch: slice05-engineering-shakedown
Scope: GM-only Test Mode story jump presets for Slice 04/Slice 05 setup/smoke work.

## What Changed

- The GM Test Mode story jump menu now exposes exactly three active presets:
  - Mission Start
  - Post-Tarsis / Engineering Ready
  - Engineering Shakedown Complete
- Retired future placeholder jumps are not active in the menu.
- Mission Start and Post-Tarsis seed accepted Slice 04 state through `scripts/acts/act1_generator_tarsis_gate.mast`.
- Engineering Shakedown Complete reuses the Post-Tarsis seed, then marks Slice 05 engineering shakedown complete.
- Neither preset creates proof stations or player-console admin controls.

## Preset ID Rename (2026-08-08, plan-hardening)

Preset jump_id values were renamed to align with the JUMP-nnn canonical names in `docs/01_design/40_admin_testing_plan.md` section 6.1/6.3, per operator decision:

| Old jump_id | New jump_id | JUMP-nnn |
|---|---|---|
| `mission_start` | `mission_start_generator_governor` | JUMP-001 |
| `post_tarsis_resupply` | `tarsis_resupply_complete` | JUMP-004 |
| `engineering_shakedown_complete` | `engineering_shakedown_complete` (unchanged) | none — see note below |

**Open finding, not yet resolved:** `engineering_shakedown_complete` has no clean JUMP-nnn match. The admin plan defines JUMP-008 as `engineering_shakedown_start` (`engineering_shakedown_complete = false`), which is the *opposite* state from what this preset seeds. This preset seeds the state *after* all Act I v2.2 engineering-shakedown gates are complete, sitting between JUMP-008 and JUMP-009 in the spec's sequence. It kept its descriptive (non-numbered) jump_id. Resolving this requires an operator decision: add a new JUMP number to the admin plan, or accept this preset stays outside the JUMP-nnn scheme permanently.

All references below to `mission_start` and `post_tarsis_resupply` in this doc's live-smoke history predate the rename and describe the presets as they existed at the time; they are left as historical record, not corrected in place.

## What Quick/Static Checks Prove

- `tests/test_story_jump_presets_static.py` checks that the story jump route is GM-only and Test Mode gated.
- Static checks require the registry to contain only `mission_start_generator_governor`, `tarsis_resupply_complete`, and `engineering_shakedown_complete`.
- Static checks require the Slice 04 presets to call the Slice 04 seed helpers and the Slice 05 preset to call the engineering shakedown complete seed helper.
- Static checks reject the retired future placeholder preset names.
- `tests/test_act1_generator_tarsis_static.py` checks that:
  - Mission Start resets zero energy, zero ordnance, active governor, held Kestrel reserve, and the Kestrel departure objective.
  - Post-Tarsis seeds cleared governor, full energy/armament requests, Tarsis completion flags, docked-state setup, and the Engineering-ready objective.
  - Both helpers invalidate stale Kestrel generator-advisory timers.

## What Only Live Cosmos Smoke Can Prove

- The GM can see Khovan Scenario Control from the GM Comms console.
- Test Mode reveals Story Jumps only to the GM.
- Mission Start visibly returns Artemis to the Kestrel start condition.
- Post-Tarsis visibly gives Artemis full energy and armament and places the scenario at the Engineering shakedown handoff.
- Engineering Shakedown Complete visibly places the scenario after the engineering shakedown, with the current objective pointing to the Slice 06 target spike.
- The current objective text appears in the live text/comms surface after each jump.
- Repeated jumps do not leave stale Kestrel advisory messages firing in the wrong state.

## Live Smoke Procedure

Repo/branch assumption: run from `slice05-engineering-shakedown` after `python run_tests.py quick` passes.

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

6. From the same GM jump menu, select `Post-Tarsis / Engineering Ready`.

Expected observation:
- Artemis is at/near Tarsis and treated as post-resupply.
- Energy is full, expected value 1000.
- Armament is full: Homing 10, Nuke 3, EMP 6, Mine 6.
- Current objective says `Begin Engineering shakedown with Tarsis Training Control.`
- Scenario Control overview reports Act I, scene 2, post-Tarsis/Engineering-ready state.

Failure/ambiguous observation:
- Energy is restored but armament is not.
- Artemis remains at Kestrel or cannot interact with Tarsis normally after the jump.
- Objective text remains on Kestrel or Tarsis docking.
- A delayed Kestrel generator advisory fires after the Post-Tarsis jump.

7. From the same GM jump menu, select `Engineering Shakedown Complete`.

Expected observation:
- Artemis is at/near Tarsis and treated as post-resupply.
- Energy is full, expected value 1000.
- Armament is full: Homing 10, Nuke 3, EMP 6, Mine 6.
- Current objective says `Slice 06 target spike ready. GM Test Mode: run Slice 06 Target Spike.`
- Scenario Control overview reports `engineering_shakedown_complete. True`.

Failure/ambiguous observation:
- Engineering shakedown still offers incomplete fallback gates.
- Current objective remains on no-motion, DAMCON, overload, repair, or navigation priority.
- Scenario Control overview does not report engineering shakedown complete.

## What Remains Unproven

- Static tests do not prove live UI visibility, dock-state behavior, or Cosmos data-set rendering.
- The Post-Tarsis jump is an admin test seed and does not prove the real player sequence from Kestrel through normal Tarsis docking.
- The Engineering Shakedown Complete jump is an admin test seed and does not prove the real engineering gates, DAMCON positioning, overload damage, repair, or navigation preset.

## Commit Gate

Do not commit this branch until:

- `python run_tests.py quick` passes.
- `git diff --check` passes.
- The live smoke procedure above confirms all three jumps once.
- Any failed or ambiguous live result is fixed or documented before closing the branch.
