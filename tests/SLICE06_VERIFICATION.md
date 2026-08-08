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

Status: partial live proof (GM-console pass 2026-08-08, plus a second operator pass same date exercising Weapons/Science). Spawn, cleanup, non-attack behavior, Science scan, and Weapons selection/fire/kill are live-proven. Status readback (`Read Target Spike Status`) remains live-ambiguous. Comms hail and stock-menu suppression remain untested. Manual subsystem targeting is now confirmed live-UNAVAILABLE against this contact type — a new finding requiring a Drone 01 design decision before Phase B, not just an open risk. See Live Smoke Log at the end of this file for the full record.

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
- Live (2026-08-08, GM console only): boot chain reaches BOOT 010 live; Artemis start state matches source doc; Kestrel Yards and Tarsis Station spawn and appear as GM contacts; Scenario Control Panel renders correctly; Test Mode toggle correctly gates Story Jumps and Slice 06 Target Spike visibility; Spawn Target Spike works and flips `drone_target_spike_active`; Cleanup Target Spike correctly reverts the menu.
- Live (2026-08-08, operator pass): target non-attack behavior confirmed; Science scan confirmed; Weapons target selection confirmed; Weapons fire/kill confirmed. Station crewing arrangement for this pass (single client vs. simultaneous multi-station) was not recorded — confirm before treating this as proof of a genuinely crewed session.

## Acceptance Not Covered

- Live Cosmos must prove scan/hail route visibility for Comms specifically, and no unwanted stock enemy menus. Not tested this pass — Comms hail was not exercised or reported. This is a significant remaining gap: stock-menu suppression is one of the two things this spike exists to prove (the other being subsystem damage).
- Live Cosmos must prove damage/object and damage/destroy events from genuine combat, distinguishable from GM cleanup. A real Weapons kill was confirmed live (2026-08-08), but the specific A/B trace comparison against a GM Cleanup destroy event (requested to confirm the destroy-hook finding below) was not explicitly performed or reported this pass.
- **Live-confirmed as unavailable, 2026-08-08:** manual subsystem targeting does not appear to be exposed against this contact through normal Weapons console targeting. This is no longer "not tested" — it is a live finding requiring a Phase B design decision (see Known Risks).
- Whether Weapons-console damage readout is visible to a crewed station for this contact type — live-confirmed as NOT visible/known to the operator this pass. Needs investigation.
- `Read Target Spike Status` remains live-ambiguous. It was retried this pass but only after the target had already been destroyed ("target gone"), which does not test the original question — whether the report renders while a station is seated and the target is alive. Still unresolved.
- Full Drone 01 and Drone 02 sequence remains unimplemented until Phase A is accepted or a fallback/blocker is documented.

## Known Risks/API Uncertainties

- Neutral `npc_spawn` may still have stock behaviors not visible in static checks.
- `get_weapons_selection` may not fire consistently.
- **Confirmed live 2026-08-08 (operator pass):** manual subsystem targeting is unavailable against the Slice 06 spike target through normal Weapons console targeting — the operator reported no subsystem-targeting option existed against this contact. This was previously listed as a hypothetical risk (`MANUAL_SYSTEM` / `MANUAL_CRITICAL_HIT` may be absent); it is now a confirmed-live finding, not a hypothetical. **Design implication for Phase B:** Drone 01 requires subsystem-hit detection per the source docs. If this Cosmos build cannot expose subsystem targeting for a custom neutral contact, the documented Comms/captain-confirmation fallback needs to become Drone 01's primary detection path, not a last-resort fallback. This is now a decision point for the operator before Phase B design, not a residual risk to note and move past.
- `system_damage` values may not reflect manual subsystem hits without extra handling — unresolved, and now moot if subsystem targeting itself is unavailable (see above).
- **New finding, live 2026-08-08:** the operator could kill the target via Weapons but did not know where or how to read damage on it from any station UI. May share a root cause with the `Read Target Spike Status` rendering gap below (custom/GM-spawned contacts may not receive the same UI treatment as standard hostiles), or may be a separate Weapons-console gap. Needs investigation before Phase B assumes players can see subsystem/hull damage live during Drone 01/02.
- Destruction events may fire, but object cleanup timing may affect status reading.
- If subsystem detection is unavailable, Drone 01 needs a documented Comms/captain confirmation or GM final fallback rather than fake automatic detection. **This condition is now confirmed true, not hypothetical — see above.**
- **Confirmed live 2026-08-08**: `sbs.delete_object()` inside `khovan_drone_contact_fire_cleanup_target_spike` fires the same `//damage/destroy` hook a genuine Weapons kill would. Trace evidence: `[KHOVAN ACT1 DRONE SPIKE CLEANUP] cleanup_count=1` immediately followed by `[KHOVAN ACT1 DRONE SPIKE DAMAGE] ... weapons_damage=0.0 engines_damage=0.0` and `[KHOVAN ACT1 DRONE SPIKE DESTROY]`. GM cleanup and real combat destruction are currently indistinguishable through `drone_target_spike_destroyed_observed`. Since the recorded Drone 02 source decision is "completes on destruction," Phase B must not treat `destroyed_observed` alone as a valid completion signal — it needs a guard (e.g. only trust destruction when accompanied by nonzero `weapons_damage_value`/`engines_damage_value`, or route GM cleanup through a path that does not touch the shared destroy hook).

## Next Action

Phase A GM-console mechanics and most station mechanics (spawn, non-attack, Science scan, Weapons selection/fire/kill) are now live-proven (2026-08-08). Remaining before Phase A can be called complete:

1. Test Comms hail specifically, and confirm no stock enemy taunt/surrender/hostile menus interfere — not yet tested.
2. Retry `Read Target Spike Status` while the target is still alive and a station is seated — the only attempt so far was after destruction, which doesn't test the real question.
3. Run the destroy-hook A/B comparison directly: trace-compare a real Weapons kill against a GM Cleanup destroy event to confirm they are distinguishable, or confirm they are not (see Known Risks).
4. Add a destruction-source guard before Phase B uses `destroyed_observed` as the Drone 02 completion signal.
5. **New, higher priority than the above:** route the confirmed subsystem-targeting-unavailable finding to the operator as an explicit Drone 01 design decision. If subsystem detection genuinely cannot be automated against a custom contact in this Cosmos build, Drone 01's design needs to commit to the Comms/captain-confirmation path as primary before Phase B is scoped, not discover this mid-build.

Stop after Phase A if stock-menu behavior cannot be proven or reasonably fallback-confirmed, or if the operator decision in item 5 changes Drone 01's scope.

---

## Live Smoke Log (append-only)

### LIVE SMOKE 2026-08-08 (partial — GM-only pass)

```text
branch: slice06-drone-contact-fire
commit: 33cd0c1
build: locally installed Artemis3-x64-release, server + 1 local client (Game Master console)
result: PARTIAL

scope: GM-console-only functional pass, driven by Claude Code via desktop control.
       Science/Comms/Weapons station behavior NOT exercised this pass — no client
       was seated at those consoles. This is not a substitute for a crewed run.

checks:
- boot chain reached [KHOVAN BOOT 010] playable bootstrap complete: PASS
  (trace shows full sequence: bootstrap state -> SCP init -> jump registry ->
  engineering shakedown init -> drone contact fire init -> playable_bootstrap ->
  generator/Tarsis gate init -> debug runtime -> BOOT 009/010)
- Artemis start state matches source doc Act I canon: PASS
  (Energy 0, Homing 0/10, Nuke 0/3, EMP 0/6, Mine 0/6 observed on server HUD)
- Kestrel Yards and Tarsis Station spawn and appear as GM contacts: PASS
- Scenario Control Panel renders live with correct button set: PASS
- Test Mode toggle correctly gates "Test Mode Story Jumps" and
  "Slice 06 Target Spike" visibility (hidden off, shown on): PASS
- Slice 06 Target Spike route renders with correct conditional buttons
  (Spawn only when inactive; Select/Cleanup appear once active): PASS
- Spawn Target Spike: PASS
  (khovan_training contact group appeared, drone_target_spike_active flipped,
  trace: [KHOVAN ACT1 DRONE SPIKE SPAWN] target_id=4611686018427387917 spawn_count=1)
- Read Target Spike Status: AMBIGUOUS
  (label executes without error and comms_navigate returns to the same menu
  cleanly, but no report text was found rendering anywhere in the Game Master
  console UI after repeated attempts, including after maximizing the window
  and toggling the comms-list panel. Not confirmed working; not confirmed broken.)
- Cleanup Target Spike: PASS with a finding
  (menu correctly reverted to spawn-only state; drone_target_spike_active
  cleared)
- Science scan / Comms hail / Weapons selection / manual subsystem damage:
  NOT TESTED this pass (no station client connected)

trace_marker_last: [KHOVAN ACT1 DRONE SPIKE DESTROY] destroyed_id=4611686018427387917

finding: GM Cleanup fires the //damage/destroy hook.
  sbs.delete_object() inside khovan_drone_contact_fire_cleanup_target_spike
  triggers the same //damage/destroy handler a real combat kill would, so
  Cleanup sets drone_target_spike_destroyed_observed = True with
  manual_target=None, manual_system=None, weapons_damage=0.0, engines_damage=0.0.
  GM cleanup and genuine Weapons-caused destruction are currently
  indistinguishable through this hook. If Phase B uses destruction_observed as
  a completion signal (per the recorded Drone 02 source decision), this needs
  a guard before Phase B build, e.g. only trust destruction as a real kill
  when accompanied by nonzero weapons_damage_value, or gate GM cleanup through
  a separate code path that does not touch the shared destroy hook.

blocker: Read Target Spike Status visibility unresolved. Does not block Phase A
  spawn/cleanup mechanics, but blocks confidently reading spike state from the
  GM console for anyone running this live without a trace-file tail open.

next action: Investigate where GM-context comms_receive() actually renders in
  this Cosmos build (may need a Communication-console pass, or the reply may
  need routing through a different mechanism for GM-comms routes specifically).
  Run the remaining Phase A checklist items (Science scan, Comms hail, Weapons
  selection, subsystem damage) with a full crew before calling Phase A complete.
  Resolve the Cleanup/destroy-hook finding before Phase B.
```

### LIVE SMOKE 2026-08-08 (partial — operator pass, weapons exercised)

```text
branch: slice06-drone-contact-fire
commit: (at time of pass; run_tests.py quick was passing)
build: locally installed Artemis3-x64-release
result: PARTIAL

scope: Operator-driven pass. Station crewing arrangement (single client cycling
       stations vs. multiple simultaneous clients) not recorded — confirm before
       trusting this as proof of a genuinely crewed, simultaneous-station session.

checks:
- Spawn Target Spike: PASS (screenshot confirms one "Slice 06 Spike Target"
  contact, khovan_training group, tsn allegiance tag)
- Target does not attack Artemis: PASS
- Science scan: PASS
- Comms hail / stock-menu suppression: NOT TESTED this pass — not reported.
  This is a real gap: the training-safe Comms hail behavior and stock
  enemy-menu suppression are exactly the finding this checklist exists to
  catch, per the Known Risks entry on npc_spawn stock behaviors.
- Weapons target selection/lock: PASS ("I can fire on the target")
- Weapons fire / damage recorded: PASS ("I can kill it") but with a finding —
  operator reported not knowing where/how to read damage on this contact from
  the Weapons console. Damage values may only be confirmable via the trace
  file, not from any in-game station UI, for this contact type.
- Manual subsystem targeting: FAIL / CONFIRMED UNAVAILABLE — operator reports
  no subsystem-targeting option exists against this contact ("not a standard
  target"). This moves the Known Risks entry on MANUAL_SYSTEM /
  MANUAL_CRITICAL_HIT from hypothetical to confirmed-live: subsystem hit
  detection is NOT available through normal Weapons targeting against a
  GM-spawned neutral contact in this Cosmos build.
- Destruction: PASS ("Pass") — but the specific check requested (compare
  trace damage values on this real Weapons kill against a separate GM Cleanup
  destroy event, to confirm they are distinguishable per the destroy-hook
  finding above) was not explicitly reported as done. Not confirmed either
  way.
- Read Target Spike Status: retried AFTER the target was destroyed
  ("Target gone"). This does not resolve the original open question, which
  was whether the status report renders anywhere in the console UI while a
  station is seated and the target is still alive. Still AMBIGUOUS/open.

trace_marker_last: not captured this pass — recommend tailing
  tests/live_startup_trace.txt during the next pass so damage values and
  destroy-hook markers can be read directly rather than inferred from the UI.

finding (NEW, confirmed live): manual subsystem targeting is unavailable
  against the Slice 06 spike target through normal Weapons console targeting.
  Design implication: Drone 01 (per docs/01_design/10_mast_requirements.md
  section 8.5 and the admin plan's ACT1-021/D2 subsystem-hit checks) requires
  subsystem-hit detection. If this Cosmos build genuinely cannot expose
  MANUAL_SYSTEM/MANUAL_CRITICAL_HIT for a custom neutral contact, Drone 01
  needs the documented Comms/captain-confirmation fallback from Known Risks
  as its PRIMARY path, not a fallback of last resort. This is now a design
  decision point for Phase B, not a residual risk.

finding (NEW): Weapons-side damage readout is not visible/known to the
  operator for this contact type. May be the same root cause as the
  Read Target Spike Status GM-rendering gap (custom/GM-spawned contacts not
  getting the same UI treatment as standard hostiles), or may be a separate
  Weapons-console-specific gap. Needs investigation before Phase B assumes
  players can see subsystem/hull damage during Drone 01/02.

blocker: same as prior entry — Read Target Spike Status rendering, still
  unresolved, now compounded by the Weapons damage-readout gap above.
  Destroy-hook guard (see Known Risks) still not built and still not
  confirmed distinguishable in a live A/B comparison.

next action: 1) confirm crewing arrangement for this pass (single client vs.
  simultaneous stations) so the record is accurate; 2) explicitly test Comms
  hail / stock-menu suppression; 3) retry Read Target Spike Status while the
  target is still alive; 4) run the GM-Cleanup-vs-real-kill trace comparison
  directly; 5) route the subsystem-targeting-unavailable finding to the
  operator as a Drone 01 design decision before Phase B.
```
