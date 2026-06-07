# Slice 05 Verification

Branch: slice05-engineering-shakedown
Goal: implement the Full Shakedown Engineering systems sequence immediately after the accepted Slice 04 Tarsis resupply/governor-clear handoff.

## Source Sections Used

- `AGENTS.md`, Runtime Load and GUI Lifecycle Testing, Operator Test Expectation.
- `docs/00_project/00_source_index.md`, active source map and Current Act I Canon.
- `docs/01_design/00_scenario_play_guide.md`, Act I shakedown fork revision and Engineering station qualification role.
- `docs/01_design/10_mast_requirements.md`, Sections 6.2, 6.10, and 8.4.
- `docs/01_design/20_gm_operational_notes.md`, Sections 6.1, 6.4, and 6.8.
- `docs/01_design/40_admin_testing_plan.md`, JUMP-008 and ACT1-012 through ACT1-018.
- `docs/01_design/50_implementation_slice_plan.md`, Slice 05.
- `docs/02_content/40_dillon_clips.md`, Training Control / Tarsis text packet context.
- `docs/04_implementation_setup/10_mast_file_lessons.md`, active-MAST caution against old Engineering/Drill Two drift.
- `tests/SLICE04_VERIFICATION.md`, accepted Tarsis handoff state.
- `tests/ADMIN_JUMP_VERIFICATION.md`, approved Post-Tarsis GM test preset.

## Files Touched

- `scripts/acts/act1_engineering_shakedown.mast`
- `scripts/acts/act1_generator_tarsis_gate.mast`
- `scripts/main.mast`
- `scripts/systems/scenario_control_panel.mast`
- `run_tests.py`
- `tests/test_act1_engineering_shakedown_static.py`
- `tests/SLICE05_VERIFICATION.md`

## State Variables

Slice 05 owns:

- `engineering_shakedown_initialized`
- `engineering_shakedown_available`
- `engineering_shakedown_started`
- `engineering_shakedown_status`
- `engineering_shakedown_detection_mode`
- `engineering_shakedown_last_step`
- `engineering_impulse_zero_warp_200_requested`
- `engineering_no_motion_validation_requested`
- `engineering_no_motion_confirmed`
- `damcon_rest_cycle_confirmed`
- `damcon_meal_cycle_confirmed`
- `controlled_overload_started`
- `controlled_overload_damage_detected`
- `controlled_overload_repair_supervision_started`
- `controlled_overload_repair_confirmed`
- `controlled_overload_repaired`
- `navigation_priority_preset_set`
- `engineering_shakedown_complete`

The implementation also sets `shakedown_mode = "full"` when Slice 05 becomes available.

## Runtime Flow

1. Slice 04 Tarsis resupply or the approved Post-Tarsis GM test preset calls `khovan_act1_engineering_shakedown_prepare_after_tarsis`.
2. The existing Tarsis Comms contact offers `Khovan: Begin Engineering Shakedown` after governor clear.
3. Training Control instructs impulse 0 / warp 200 and asks Captain/Helm to validate no motion.
4. No-motion validation first uses an automatic observer: Helm full throttle, actual speed near zero, and negligible position delta.
5. If the no-motion observer times out because Engineering slider keys cannot be verified, a fallback confirmation appears.
6. DAMCON Control confirmations still use Comms fallback because a reliable grid-location/readiness API is not yet identified.
7. Training Control instructs Helm to set engines to all stop, then controlled 300% impulse/warp overload.
8. Controlled overload damage first uses an automatic engine-system-damage observer.
9. If engine damage is not observed, a fallback controlled-damage confirmation appears.
10. Repair supervision and repair completion use Comms fallback until a repair-completion API is proven.
11. Navigation priority asks Engineering to set maneuvering 190%, warp 10%, and impulse 100%; confirmation remains fallback until preset storage/current-preset keys are proven.
12. `engineering_shakedown_complete = True`.
13. Current Objective advances to Engineering shakedown complete / await next shakedown instruction.
14. GM Test Mode includes `Engineering Shakedown Complete` as a shortcut for testing content immediately after Slice 05.

## GM Controls

- Scenario Control Panel overview reports `engineering_shakedown_status` and `engineering_shakedown_complete`.
- No new GM manual mark controls were added.
- No player-facing debug/admin controls were added.
- GM manual marking remains a last fallback if player Comms confirmation fails live.

## Player-Facing Behavior

Player-facing text is concise and delivered through the existing Comms/current-objective path:

- Engineering systems shakedown begins.
- Engineering sets impulse zero and warp 200.
- Captain/Helm confirms full-impulse no-motion behavior.
- DAMCON Control confirms crew-quarters rest-cycle standby.
- DAMCON Control confirms mess meal-cycle standby.
- Engineering starts controlled 300% overload after Helm sets engines to all stop.
- Controlled damage is logged.
- Engineering supervises repair.
- Engineering sets maneuvering 190%, warp 10%, and impulse 100% for the navigation-priority preset.
- Training Control marks Engineering shakedown complete.

## Tests/Static Checks

`tests/test_act1_engineering_shakedown_static.py` checks:

- Slice 05 file exists, imports, and initializes.
- State variables exist and legacy `drill_1_*`, `drill_2_*`, and `drill_3_*` state trees are absent.
- Start is blocked before Tarsis handoff.
- Normal Slice 04 resupply and the Post-Tarsis GM preset prepare Slice 05.
- The Engineering Shakedown Complete GM preset reuses the Post-Tarsis seed, marks every Slice 05 engineering gate complete, and sets the current objective to the next-instruction handoff.
- Player Comms route is Tarsis/generator-clear gated.
- No GM/admin controls are exposed to players.
- Required instruction, DAMCON, overload, damage, repair, navigation, and completion gates exist.
- No-motion and engine-damage observer paths exist before fallback confirmations.
- API-uncertain DAMCON, repair, and navigation-preset gates are documented as fallback confirmations.
- Scenario Control Panel reports status only.
- `run_tests.py quick` includes the Slice 05 static test file.

Quick/static checks do not prove live Cosmos UI behavior, Engineering data-set values, damage events, DAMCON location, repair completion, or navigation-priority UI state.

## Live Smoke Checklist

Repo/branch assumption: run from `slice05-engineering-shakedown` after `python run_tests.py quick` and `git diff --check` pass.

1. Launch Khovan Reach.
2. Reach Post-Tarsis / Await Next Shakedown Instruction via normal Slice 04 path or approved GM-only test preset.
3. Confirm Artemis is mission-ready after Tarsis handoff.
4. Select Tarsis Station in Comms and start Engineering shakedown.
5. Confirm Current Objective updates to impulse zero / warp 200 task.
6. Engineering sets impulse zero / warp 200, or use documented fallback if mechanical detection is unavailable.
7. Captain/Helm orders full impulse; confirm no-motion auto-advances if Helm throttle is full and speed/position stay near zero, or that fallback appears after timeout.
8. Confirm DAMCON crew-quarters fallback appears after the observer attempt, then confirm it.
9. Confirm DAMCON mess fallback appears after the observer attempt, then confirm it.
10. Confirm controlled overload instruction tells Helm to set engines to all stop before Engineering sets impulse/warp 300.
11. Trigger controlled overload and watch whether engine damage auto-advances; use fallback only if no damage is detected.
12. Confirm repair supervision/repair completion fallback path.
13. Set maneuvering 190%, warp 10%, and impulse 100%, save or select the navigation-priority preset, then use fallback confirmation unless a preset detector is added.
14. Confirm `engineering_shakedown_complete` is set in Scenario Control Panel overview.
15. Confirm Current Objective advances to Engineering shakedown complete / next instruction.
16. Confirm player consoles do not show admin controls.
17. Confirm Slice 04 Kestrel/Tarsis basics did not regress.
18. Optional shortcut check: GM Scenario Control -> Enable Test Mode -> Test Mode Story Jumps -> Engineering Shakedown Complete.

## Expected Observations

- Players can identify who acts next and why.
- Engineering shakedown proceeds through all required steps.
- No-motion can auto-advance from Helm throttle, actual speed, and position delta.
- Controlled damage can auto-advance from engine subsystem damage if Cosmos exposes it live.
- Fallback confirmations are clear, in-fiction, and appear only after observer/API uncertainty where applicable.
- GM controls remain hidden from players.
- Slice 04 remains stable.
- Quick tests pass.

## Failure/Ambiguous Observations

- Engineering shakedown starts before Tarsis handoff.
- Objective text and player-facing messages disagree.
- A required step advances without player action or confirmation.
- A mechanical gate is claimed automatic but does not auto-advance or expose a fallback.
- DAMCON confirmation is missing.
- Controlled overload/damage/repair cannot be triggered or confirmed.
- GM Engineering Shakedown Complete jump does not set `engineering_shakedown_complete. True` in Scenario Control.
- Player console sees admin controls.
- Slice 04 Kestrel/Tarsis path regresses.
- Static tests pass but live UI is unclear.

## Acceptance Covered

- Static: Slice 05 file/import/init exists.
- Static: state variables and current shakedown names exist.
- Static: start is gated behind Tarsis handoff or approved Post-Tarsis test preset.
- Static: impulse zero / warp 200 instruction exists.
- Static: no-motion automatic observer exists, with fallback only after timeout or missing object data.
- Static: DAMCON crew-quarters and mess Comms confirmations exist.
- Static: controlled overload asks Helm engines all stop before Engineering 300% output.
- Static: engine-damage observer exists, with fallback only after timeout or missing object data.
- Static: repair and navigation priority confirmation fallback gates exist.
- Static: completion flag is set only at the final navigation priority confirmation.
- Static: GM Engineering Shakedown Complete jump exists, remains Test Mode/GM-only through the existing story-jump route, and seeds completed Slice 05 state only by reusing the Post-Tarsis seed first.
- Static: player consoles do not expose GM/admin controls in the Slice 05 file.
- Static: Slice 04 proof station remains absent through the existing quick suite.

## Acceptance Not Covered

- Live Cosmos must prove that the Tarsis Comms option appears after the handoff.
- Live Cosmos must prove current-objective messages are visible and ordered.
- Live Cosmos must prove player consoles do not see admin controls.
- Live Cosmos must prove the GM Engineering Shakedown Complete jump appears, can be selected, and visibly lands after Slice 05.
- Live Cosmos must prove whether Engineering output, DAMCON location/readiness, repair completion, or navigation-priority preset state can be mechanically detected.
- Live Cosmos must prove whether the no-motion and engine-damage observers auto-advance reliably under operator play.
- Live Cosmos must prove Slice 04 Kestrel/Tarsis path remains stable after this import and handoff hook.

## Known Risks/API Uncertainties

- Whether Cosmos exposes Engineering impulse/warp output reliably.
- Whether Engineering impulse/warp slider values can be read directly. Current observer infers the first gate from Helm full throttle, actual speed, and position delta.
- Whether no-motion validation can be detected by position delta without false positives.
- Whether controlled overload damage can be triggered or detected reliably through `system_damage` on `sbs.SHPSYS.ENGINES`.
- Whether repair completion can be detected reliably.
- Whether DAMCON team location is mechanically visible.
- Whether navigation priority preset storage/current-preset state is observable. Current implementation asks for maneuvering 190%, warp 10%, and impulse 100%, then uses fallback confirmation.

Current implementation finding: no-motion and engine-damage gates have observer-first implementation. DAMCON location/readiness, repair completion, and navigation-priority preset remain fallback-confirmed until live Cosmos or reference code proves reliable APIs. No fake automatic gate is claimed.

## Next Action

Run `python run_tests.py quick` and `git diff --check`. Then live-smoke the checklist above. Do not commit until quick passes, diff check passes, and the live result is either accepted as playable or documented as a blocker.
