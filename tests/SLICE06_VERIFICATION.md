# Slice 06 Verification

Goal: build Slice 06 Drone 01 controlled disable and Drone 02 live-fire target, starting with the mandatory target subsystem-damage spike before implementing the full drill.

## Source Sections Used

- `AGENTS.md`, branch lifecycle, source authority, and operator test expectations.
- `docs/00_project/00_source_index.md`, active source map.
- `docs/01_design/00_scenario_play_guide.md`, Scene 4A Drone 01 and Scene 5A Drone 02.
- `docs/01_design/10_mast_requirements.md`, sections 8.5 and 8.6.
- `docs/01_design/40_admin_testing_plan.md`, ACT1-019 through ACT1-024 and D2/D3 checks.
- `docs/01_design/50_implementation_slice_plan.md`, Slice 06 and mandatory target subsystem-damage spike.
- `docs/02_content/40_dillon_clips.md`, Clips 4 through 7.
- `docs/04_implementation_setup/10_mast_file_lessons.md`, target subsystem-damage spike warning.
- `tests/SLICE04_VERIFICATION.md` and `tests/SLICE05_VERIFICATION.md`, accepted prior-slice state and GM jump handoff.

## Files Touched

- `scripts/acts/act1_drone_contact_fire.mast`
- `scripts/main.mast`
- `scripts/systems/scenario_control_panel.mast`
- `run_tests.py`
- `tests/test_act1_drone_contact_fire_static.py`
- `tests/SLICE06_VERIFICATION.md`

## State Variables

Phase A spike state currently owns:

- `drone_contact_fire_initialized`
- `drone_contact_sequence_status`
- `drone_contact_detection_mode`
- `drone_contact_last_step`
- `drone_contact_source_decision`
- `drone_target_spike_available`
- `drone_target_spike_active`
- `drone_target_spike_target_id`
- `drone_target_spike_navproxy_id`
- `drone_target_spike_spawn_count`
- `drone_target_spike_cleanup_count`
- `drone_target_spike_status`
- `drone_target_spike_scan_observed`
- `drone_target_spike_hail_observed`
- `drone_target_spike_weapons_selected`
- `drone_target_spike_damage_observed`
- `drone_target_spike_manual_subsystem_hit_observed`
- `drone_target_spike_manual_subsystem`
- `drone_target_spike_weapons_damage_value`
- `drone_target_spike_engines_damage_value`
- `drone_target_spike_destroyed_observed`
- `drone_target_spike_stock_comms_menu_observation`
- `drone_target_spike_training_safe_observation`
- `drone_target_spike_result`
- `drone_target_spike_blocker`
- `drone_target_spike_fallback`

Full Drone 01/Drone 02 variables are intentionally not active yet. Do not create a duplicate legacy `drill_2_*` or `drill_3_*` state tree.

## Runtime Flow

Phase A only:

1. GM enables Test Mode.
2. Engineering shakedown completion, or the Engineering Shakedown Complete story jump, sets the Current Objective to `Slice 06 target spike ready. GM Test Mode: run Slice 06 Target Spike.`
3. GM opens `Slice 06 Target Spike`.
4. GM spawns a single neutral training target.
5. The spike links the target as an extra Science scan source and selects it for Science/Comms.
6. Science scan hooks set `drone_target_spike_scan_observed`.
7. Comms hail hook sets `drone_target_spike_hail_observed` and asks the operator to watch for stock enemy menus.
8. Weapons selection hook records `drone_target_spike_weapons_selected` if the target is selected.
9. Damage hook records generic damage, manual subsystem hit evidence, and current Weapons/Engines damage values.
10. Destruction hook records `drone_target_spike_destroyed_observed` and clears the target.
11. Cleanup removes the target and nav proxy.

## GM Controls

- GM-only route: `//comms/gamemaster/khovan_drone_contact_fire_spike`.
- It is visible only when `test_mode_enabled`.
- Controls are Spawn Target Spike, Select Target Spike, Read Target Spike Status, and Cleanup Target Spike.
- Scenario Control overview reports spike status/result.
- No player-facing debug/admin controls are added.

## Player-Facing Behavior

This is a spike harness, not the player drill:

- After Slice 05 completion, Current Objective labels the Slice 06 target spike as ready instead of ending on an await-next placeholder.
- Current Objective labels the spike as GM target spike active after the spike spawns.
- Science sees scan text for the spike target.
- Comms sees a Khovan hail option and drill-mode response.
- No Drone 01/Drone 02 player sequence is implemented yet.

## Spike Result

Static result: implemented but live-unproven.

Quick/static checks prove the spike harness exists, imports, initializes, exposes GM-only controls, spawns a neutral training target, includes Science/Comms hooks, and includes selection/damage/destruction observers.

Quick/static checks do not prove live Cosmos target behavior, stock enemy menu suppression, non-attacking behavior, scan visibility, Weapons selection events, manual subsystem damage inventory values, system damage values, or destruction event reliability.

Source decision: Drone 02 completes on destruction. This resolves the active-source ambiguity by user direction after reviewing the conflict between destruction-oriented scenario/MAST/slice-plan text and Engine-disable Dillon/admin references. Drone 01 remains the subsystem-disable proof drill.

## Tests/Static Checks

`tests/test_act1_drone_contact_fire_static.py` checks:

- Slice 06 file exists, imports, and initializes before playable bootstrap.
- Phase A spike variables exist.
- Full Drone 01/Drone 02 flow variables are not falsely marked complete.
- GM-only Test Mode spike controls exist.
- Spike target spawn uses a small neutral training target.
- Science and Comms hooks exist.
- Weapons selection, damage/object, manual subsystem, and destruction observers exist.
- Scenario Control reports spike status.
- Quick includes the Slice 06 static test file.
- This verification doc records Phase A limits.

## Live Smoke Checklist

Repo/branch assumption: run from `slice06-drone-contact-fire` after `python run_tests.py quick` and `git diff --check` pass.

1. Launch Khovan Reach.
2. Open GM Comms.
3. Open Khovan Scenario Control.
4. Enable Test Mode.
5. Open `Slice 06 Target Spike`.
6. Select `Spawn Target Spike`.
7. Confirm a single `Slice 06 Spike Target` appears.
8. Confirm it does not attack Artemis.
9. Confirm Science can scan it and the spike status records scan observed.
10. Confirm Comms can hail it and no unwanted stock enemy taunt/surrender/hostile menus interfere.
11. Confirm Weapons can select/lock it and the spike status records selection observed.
12. Fire or otherwise damage the target and confirm damage is recorded.
13. If manual subsystem targeting is available, target Weapons or Engines and confirm subsystem hit evidence records the subsystem.
14. Destroy the target and confirm destruction is recorded.
15. Run Cleanup Target Spike if needed.
16. Confirm player consoles do not show GM/debug controls.

## Expected Observations

- GM-only spike controls are visible only in Test Mode.
- A neutral training target spawns and is scannable/hailable.
- The target does not attack.
- No stock enemy surrender/taunt/hostile menus break the training fiction.
- Weapons target selection is recorded if Cosmos exposes it.
- Damage/destruction events are recorded if Cosmos exposes them.
- Manual subsystem evidence is recorded if Cosmos exposes `MANUAL_SYSTEM` / `MANUAL_CRITICAL_HIT`.

## Failure/Ambiguous Observations

- Target attacks Artemis.
- Stock enemy menus interfere with the custom Khovan hail.
- Science cannot scan the target.
- Comms cannot hail the target.
- Weapons selection does not trigger.
- Damage/object does not trigger.
- Manual subsystem target data is absent.
- Destruction does not trigger.
- Player consoles see GM controls.
- Static tests pass but live behavior cannot prove the sequence.

## Acceptance Covered

- Static: Phase A spike file/import/init exists.
- Static: GM-only Test Mode controls exist.
- Static: target spawn, scan, hail, selection, damage, subsystem, destruction, and cleanup hooks exist.
- Static: source ambiguity is documented and Drone 02 destruction decision is recorded.
- Static: no full Drone 01/Drone 02 flow is falsely claimed.

## Acceptance Not Covered

- Live Cosmos must prove target non-attack behavior.
- Live Cosmos must prove scan/hail route visibility.
- Live Cosmos must prove no unwanted stock enemy menus.
- Live Cosmos must prove Weapons target selection.
- Live Cosmos must prove damage/object and damage/destroy events.
- Live Cosmos must prove manual subsystem targeting data if it is expected for Drone 01.
- Full Drone 01 and Drone 02 sequence remains unimplemented until Phase A is accepted or a fallback/blocker is documented.

## Known Risks/API Uncertainties

- Neutral `npc_spawn` may still have stock behaviors not visible in static checks.
- `get_weapons_selection` may not fire consistently.
- `MANUAL_SYSTEM` / `MANUAL_CRITICAL_HIT` may be absent or not reliable.
- `system_damage` values may not reflect manual subsystem hits without extra handling.
- Destruction events may fire, but object cleanup timing may affect status reading.
- If subsystem detection is unavailable, Drone 01 needs a documented Comms/captain confirmation or GM final fallback rather than fake automatic detection.

## Next Action

Run quick checks and diff check. Then live-smoke Phase A. Stop after Phase A if target selection, subsystem damage, training-safe behavior, or stock-menu behavior cannot be proven or reasonably fallback-confirmed.
