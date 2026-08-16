# KHOVAN REACH — MAST SCRIPTING REQUIREMENTS
*Implementation specification after merging runtime architecture, Scenario Control Panel, testing/regression improvements, and prior-MAST implementation lessons.*

Status: Canonical implementation handoff  
Supersedes: prior v2.0, v2.1, v2.2, and v2.3 MAST requirements documents, archived outside the active repo
Pair with: `docs/01_design/00_scenario_play_guide.md`, Pass 2 content files, `docs/01_design/30_qualification_cards.md`, `docs/02_content/50_debrief_script.md`, `docs/02_content/20_damcon_reports.md`, `docs/03_game_resources/comms/00_tsn_cultural_comms_playbook.md`, and `docs/01_design/40_admin_testing_plan.md`

---

# 1. Purpose

**Repo-consolidation note:** This document preserves the current scenario architecture and incorporates implementation-start lessons extracted from the prior MAST files. It formalizes the old dev-jump harness as a Scenario Control Panel pattern, adds run ID / generation ID requirements for delayed tasks, adds a current-objective display spike, and keeps the active Comms reference in plain Markdown.


This document is the coding-assistant handoff specification for the Khovan Reach MAST implementation.

It translates the scenario design into runtime contracts:
- mission file structure
- ownership model
- state variables
- scene transitions
- timers
- pirate state machine
- checkpoint/reload behavior
- Scenario Control Panel requirements
- testing hooks
- debrief support

This is not final MAST code.

The coding assistant must still verify actual Cosmos/MAST APIs against documentation and reference missions. Do not invent unsupported property names for subsystem damage, Engineering power state, comms responses, or persistence.

---

# 2. Core runtime philosophy

Khovan Reach is a GM-led scenario but should not be a GM-driven script.

Canonical runtime rule:

```text
Runtime drives normal flow.
Players drive decisions.
GM supervises ambiguity.
GM overrides failure.
```

The runtime should not wait for GM confirmation for routine operations unless mechanical detection is unavailable or the beat is interpretive.

---

# 3. Ownership classes

Every runtime behavior must be classified.

## 3.1 AUTO — runtime-driven

Runtime performs the behavior during normal play.

Examples:
- mission initialization
- state variable initialization
- standard clip triggers
- entity spawn/despawn
- scripted timer scheduling
- checkpoint writes
- default scene transitions when hard gates are met
- debug overlay updates

## 3.2 GM-SUP — GM-supervised

Runtime detects or proposes; GM may hold, release, confirm, or override.

Examples:
- pirate suspicion/exposure after Comms probing
- report timing adjustment
- interpretive captain authorization
- ambiguous drill checks when no API hook exists

Default behavior:

```text
Runtime proposes.
GM may intervene.
If GM does nothing and a safe default exists, proceed after configured delay.
```

## 3.3 GM-DRIVE — GM-driven

GM performs or interprets because human judgment/performance is the point.

Examples:
- pirate captain voice performance
- Hessler scene pacing
- final qualification ratings
- station debrief delivery

## 3.4 GM-OVERRIDE — recovery-only

GM can force behavior when normal runtime breaks or the table needs recovery.

Examples:
- reload checkpoint
- force scene advance
- reset drill
- replay clip
- expose pirates if state deadlocks
- force DAMCON report

GM-OVERRIDE controls are not the normal mission path.

---

# 4. Mission file structure

Recommended package:

```text
mission/
  main.mast
  story.json
  script.py

  acts/
    act_1_drills.mast
    act_2_investigation.mast
    act_3_khovan_reach.mast
    debrief.mast

  systems/
    audio_runtime.mast
    checkpoint_system.mast
    damcon_timer.mast
    pirate_state_machine.mast
    qualification_runtime.mast
    scenario_control_panel.mast
    debug_runtime.mast
    gm_controls.mast

  data/
    dialogue/
    clips/
    qualification/
    story_jump_presets/

  tests/
    smoke/
    story_jumps/
    regression/
    golden_paths/
```

Canonical naming change:
- Use `pirate_state_machine.mast`.
- Do not use `salvager_arrival.mast` as the active module name.

Player-facing text may still say “salvagers” before exposure.

---

# 5. Mission bootstrap

Ownership: AUTO

On scenario load:

1. Initialize Artemis per Pass 1 starting state.
2. Initialize all mission state variables.
3. Initialize Scenario Control Panel in correct mode.
4. Initialize debug overlay for GM only.
5. Initialize checkpoint system.
6. Queue or play Dillon Clip 1.
7. Set `mission_phase = act_1` after initialization.
8. Set `current_scene = 1`.
9. Begin Scene 1.

The GM should not need to manually start core subsystems.

---

## 5.1 Minimum playable bootstrap

Slice 01 load proof is not enough for playable mission start.

A validation marker such as:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
Mission shell active. No Act I gameplay systems loaded.
```

proves that the mission package loads and the Khovan route executes. It does not prove that the crew can start play.

Before Scenario Control Panel work proceeds, Slice 01A must either implement or explicitly block the minimum playable bootstrap:

1. Artemis/player ship creation or confirmed existing player ship.
2. Minimum server/client path needed for players to connect to the starting bridge state.
3. Dillon Clip 1 queued, played, or represented by an operator-visible text/audio stub.
4. `mission_phase = act_1`.
5. `current_scene = 1`.
6. No Act I gameplay gates loaded.
7. No player-facing debug/admin controls.

Do not invent Cosmos/MAST player-ship, clip, GUI, or console syntax. If player ship spawn, client console routing, audio playback, or GUI behavior is uncertain, document the exact API uncertainty and preserve the blocker rather than substituting more static marker text.

---

# 6. State variables

## 6.1 Mission state

```text
mission_phase: initialization | act_1 | act_2 | act_3 | debrief | complete
current_scene: 0-15
current_beat: string/int optional
last_checkpoint: none | post_drill_1 | post_drill_2 | post_drill_3 | post_anderson_orders | post_halcyon_arrival | post_cascade | pre_pirate_combat | mission_resolution
transition_held: bool
test_mode_enabled: bool
live_recovery_mode_enabled: bool
```

## 6.2 Act I shakedown state — summary and legacy mapping

Act I no longer uses three fixed drill groups as the canonical runtime model. The current model is the shakedown fork:

```text
Full Shakedown Cruise
Compressed Shakedown Cruise
Direct Scenario
```

Use Section 6.10 for detailed Act I variables. Do not instantiate a second independent `drill_1_*`, `drill_2_*`, or `drill_3_*` state tree.

If older tests, old-build notes, or archived MAST files mention the legacy drill names, map them as follows:

```text
legacy drill_1_complete -> tarsis_resupply_complete and generator_governor_cleared
legacy drill_2_*        -> drone_01_* controlled-disable variables
legacy drill_3_*        -> drone_02_* live-fire target variables
legacy drill_3_help_prompt_used -> qualification_event_log and/or act1_skipped_observations
```

High-level Act I completion state should be represented with the current shakedown variables:

```text
shakedown_mode: unset | full | compressed | direct
kestrel_departure_clearance_granted: bool
kestrel_generator_packet_sent: bool
tarsis_resupply_complete: bool
generator_governor_cleared: bool
engineering_shakedown_complete: bool
drone_01_weapons_disabled: bool
drone_01_destroyed_in_error: bool
drone_02_destroyed: bool
act1_skipped_observations: list
```

The runtime may expose compatibility labels in the Scenario Control Panel for developer convenience, but persisted mission state should use the current shakedown variable names.

## 6.3 Act II state

```text
anderson_orders_received: bool
captain_acknowledged_orders: bool
distress_signal_detected: bool
captain_deviated_to_distress: bool
```

## 6.4 Halcyon Drift / away mission state

```text
engineer_deployed_to_halcyon: bool
damcon_team_count_aboard_artemis: int
convergence_revealed: bool
cascade_triggered: bool
cascade_time: timestamp/null
away_mission_beat: int/string
engineer_placement: not_decided | aboard_halcyon | returned_to_artemis
torpedoes_converted: int
artemis_departed_for_cache: bool
force_authorized: bool
```

## 6.5 DAMCON state

```text
damcon_team_status: pending | active | trapped | extended_mitigation | compressed_mitigation | recovered_clean | recovered_hypoxic | lost
damcon_timer_config: none | extended | compressed
damcon_timer_active: bool
next_damcon_report_time: timestamp/null
damcon_reports_delivered: int
damcon_report_held: bool
damcon_outcome: pending | clean_survival | hypoxic_survival | total_loss
```

## 6.6 Cache state

```text
cache_arrival: bool
cache_component_selected: none | correct | incorrect_military | incorrect_regulator | incorrect_other
cache_retry_required: bool
cache_retry_complete: bool
```

## 6.7 Pirate state

```text
pirates_arrived: bool
pirate_arrival_time: timestamp/null
pirate_cover_status: intact | suspected | exposed
pirate_scene_state: not_arrived | arrived_cover_intact | under_probe | suspected | exposed | docking_pressure | unauthorized_approach | combat_active | fleeing | surrendered | destroyed | escaped | boarded | resolved
credentials_requested: bool
credentials_provided: none | partial | evasive | refused
legal_posture_challenged: bool
cultural_mismatch_observed: bool
science_scan_completed: bool
science_scan_result: none | clean | suspicious
docking_requested: bool
docking_denied: bool
unauthorized_docking_attempt: bool
combat_active: bool
pirate_outcome: pending | fleeing | fled | surrendered | destroyed | boarded | escaped_with_cargo
```

## 6.8 Outcome state

```text
halcyon_repair_complete: bool
halcyon_outcome: pending | repaired | lost | partially_damaged
hessler_status: aboard_halcyon | aboard_artemis | lost
mission_resolution_ready: bool
```

## 6.9 Qualification support state

Runtime logs evidence; GM assigns ratings.

```text
qualification_notes: data structure by station/item
qualification_event_log: timestamped list
station_rating_captain: unset | pass | partial | needs_retest | n/a
station_rating_helm: unset | pass | partial | needs_retest | n/a
station_rating_weapons: unset | pass | partial | needs_retest | n/a
station_rating_engineering: unset | pass | partial | needs_retest | n/a
station_rating_science: unset | pass | partial | needs_retest | n/a
station_rating_comms: unset | pass | partial | needs_retest | n/a
```

---



## 6.10 Act I shakedown state

Add these state variables to support the generator-governor start, shakedown fork, and automated gates:

```text
starting_energy = 0
generator_governor_active = true / false
kestrel_generator_packet_sent = true / false
starting_homing_torpedoes = 0
homing_reserve_count = 2
energy_restored = true / false
launch_envelope_cleared = true / false
launch_envelope_clear_time = timestamp
shakedown_mode = unset / full / compressed / direct
training_overlay_active = true / false
comms_archive_enabled = true / false
comms_archive_message_ids = list
kestrel_departure_clearance_requested = true / false
kestrel_departure_clearance_granted = true / false
tarsis_homing_priority_requested = true / false
tarsis_generator_support_requested = true / false
tarsis_docking_clearance_requested = true / false
tarsis_docking_clearance_granted = true / false
tarsis_resupply_complete = true / false
generator_governor_cleared = true / false
engineering_shakedown_complete = true / false
damcon_rest_cycle_confirmed = true / false
damcon_meal_cycle_confirmed = true / false
controlled_overload_started = true / false
controlled_overload_damage_detected = true / false
controlled_overload_repaired = true / false
navigation_priority_preset_set = true / false
drone_01_spawned = true / false
drone_01_scanned = true / false
drone_01_hailed = true / false
drone_01_frequency_relayed = true / false
drone_01_beam_lock = true / false
drone_01_range_band_active = true / false
drone_01_stationary_hold_seconds = number
drone_01_fire_authorized = true / false
drone_01_weapons_array_hits = 0..3
drone_01_weapons_disabled = true / false
drone_01_destroyed_in_error = true / false
drone_01_reset_count = number
drone_02_spawned = true / false
drone_02_destroyed = true / false
act1_skipped_observations = list
```

# 7. Scene ownership matrix

Act I v2.2 keeps the profile fork introduced in v2.1 and adds cleanup-aligned source references. Use these ownership defaults:

| Scene/Profile | Runtime default | GM role | Ownership |
|---|---|---|---|
| Kestrel hold/departure | Hold until clearance; detect launch envelope; schedule advisory | Observe command rhythm | AUTO with GM-SUP |
| Tarsis priority/docking | Gate docking on Comms requests; clear governor on resupply | Recover if Comms menu/API unavailable | AUTO with GM-SUP |
| Engineering shakedown | Prompt and detect power/damage/repair gates | Confirm DAMCON-location fallbacks | AUTO with GM-SUP |
| Drone 01 disable | Track scan/hail/range/stationary/lock/hits; reset on violations | Adjudicate API gaps | AUTO with GM-SUP |
| Drone 02 live fire | Spawn target; detect destruction | Ensure training-safe pressure | AUTO |
| Direct Scenario | Mark skipped observations N/A; route to Act II | Confirm captain election | AUTO with GM-SUP |


| Scene | Default owner | Runtime responsibility | GM responsibility |
|---|---|---|---|
| 1 Departure | AUTO | Initialize, play Dillon Clip 1 | Observe opening command rhythm |
| 2 Drill One | AUTO + GM-SUP | Trigger clip, station/resupply state, checkpoint | Pause/retry major procedural error |
| 3 Drill Two | AUTO + GM-SUP | Guided step prompts/gates, drone, completion | Mark unavailable checks, pause safety errors |
| 4 Drill Three | AUTO + GM-SUP | Drone, evasion, hard gate completion | Observe process, single nudge if stalled |
| 5 Anderson Orders | AUTO | Clip triggers, state update | Handle playback issue only |
| 6 Transit | AUTO | Sustained phase, energy cues | Atmosphere if desired |
| 7 Distress Localized | AUTO + GM-SUP | Science data, decision wait | Interpret refusal/hesitation |
| 8 Halcyon Arrival | AUTO + GM-SUP | Spawn/scan/hail/deploy state | Coordinate Hessler handoff |
| 9 Away Mission | GM-DRIVE inside AUTO wrapper | Beat tracker, comms channel, cascade readiness | Pace Hessler conversation |
| 10 Captain Decision | GM-SUP | Present decision state, start chosen timer | Ensure implications are clear |
| 11 Cache Run | AUTO + GM-SUP | Timer reports, transit, resources | Pace report delivery |
| 12 Pirates | GM-SUP / GM-DRIVE | State machine, suggested branch, backstop | Voice pirates, interpret probes |
| 13 Cache Selection | AUTO + GM-SUP | Cache options, selection result | Narrate consequence |
| 14 Repair Resolution | AUTO + GM-SUP | Outcome calculation | Narrate final state |
| 15 Return/Debrief Setup | AUTO | Resolution state, debrief trigger | Prepare review |
| Debrief | GM-DRIVE with AUTO support | Support display and clips | Final assessment |

---


# 8. Act I implementation

Act I is now a shakedown fork with three selectable profiles. It must be runtime-driven by default.

```text
full       expanded new-player training
compressed essential gates only
direct     expedited resupply, then Act II
```

## 8.1 Instruction delivery

Every Act I instruction/advisory must be routed through a shared message function:

```text
send_training_message(message_id, title, body, source, archive=true)
```

Required behavior:

- Display in upper-left lifeform overlay.
- Echo into Comms console archive.
- Store message ID and timestamp.
- Allow Comms to review prior messages.
- Hide implementation/debug metadata from players.

Message sources:

```text
DILLON
TRAINING_CONTROL
KESTREL_YARD_CONTROL
TARSIS_CONTROL
DAMCON_CONTROL
```

## 8.2 Scene 1 — Kestrel hold and generator advisory

Initial runtime setup:

```text
starting_energy = 0
generator_governor_active = true
starting_homing_torpedoes = 0
homing_reserve_count = 2
energy_restored = false
kestrel_departure_clearance_requested = false
kestrel_departure_clearance_granted = false
launch_envelope_cleared = false
kestrel_generator_packet_sent = false
shakedown_mode = unset
```

Gate requirements:

1. Play Dillon Clip 1 at mission start.
2. Hold Artemis at Kestrel until Comms requests departure clearance.
3. Grant clearance through Kestrel Yard Control.
4. Allow Helm to clear launch envelope, then require Artemis to be at least 1 km from Kestrel before Comms can confirm launch-envelope exit.
5. Ten seconds after launch-envelope clear, send the generator advisory.
6. Send the speed/power reminder.
7. Prompt captain for shakedown profile.

Automatic detection:

- `launch_envelope_cleared` should be based on position/distance if available. Slice 04 currently requires Artemis to be at least 1 km from Kestrel before the Comms launch-envelope report succeeds.
- Emergency homing reserve release should be range-limited to Artemis within 600 m of Kestrel.
- The ten-second advisory timer should be runtime scheduled, not GM-timed.

## 8.3 Scene 2 — Tarsis production priority, generator acceptance, docking, and resupply

Docking is blocked until these flags are true:

```text
tarsis_homing_priority_requested = true
tarsis_generator_support_requested = true
tarsis_docking_clearance_requested = true
tarsis_docking_clearance_granted = true
```

On docking/resupply completion:

```text
tarsis_resupply_complete = true
generator_governor_active = false
generator_governor_cleared = true
energy_restored = true
torpedo_complement_standard = true
```

Play Dillon Clip 3 after resupply completion. Use Clip 3 trigger notes from `docs/02_content/40_dillon_clips.md`.

## 8.4 Full Shakedown — Engineering systems sequence

The runtime should guide the following steps in order:

1. Engineering sets impulse engines to 0 and warp engines to 200.
2. Captain orders undock and full impulse.
3. Runtime validates no motion if possible.
4. Engineering assigns DAMCON teams to crew quarters / rest-cycle standby.
5. Comms receives DAMCON Control confirmation.
6. Engineering assigns DAMCON teams to mess / meal-cycle standby.
7. Comms receives DAMCON Control confirmation.
8. Engineering sets impulse and warp engines to 300 and allows controlled overload.
9. Runtime detects engine damage/overload if possible.
10. Engineering supervises repairs.
11. Runtime detects repair completion if possible.
12. Engineering sets a navigation priority preset.

Detection priority:

```text
ship motion / engine output / damage / repair: automatic where possible
DAMCON location: Comms confirmation preferred
GM mark: final fallback only
```

## 8.5 Full or Compressed Shakedown — Drone 01 controlled disable

**Revision note (operator-ratified 2026-08-16) — the Weapons-array disable is one confirmed critical hit, not three.** Gate 9 previously read "disabled in three confirmed hits." That number was set before the stock manual-targeting mechanic was read from source, and it does not survive contact with it: `legendarymissions/consoles/manual_weapons.mast:187` rolls `random.randint(1,20) == 20` **once per press of a subsystem button** — not per beam hit — so three confirmed hits is roughly sixty button presses. Worse, lines 169-173 of the same file clear an armed critical whenever the player switches subsystem, so a crew alternating between Weapons and Engines destroys its own progress. Beam rate does not enter the roll at all; it only decides how quickly an armed critical is consumed.

One successful critical teaches what this gate exists to teach — that subsystem damage is worth pursuing and that manual targeting is the way to reach it. The additional two taught patience with a d20. Runtime now reads `drone_01_required_weapons_hits`, so the count is one line to change if live play argues for two.

Related and unchanged in intent: hit confirmation is no longer inferred from the stock console's `MANUAL_SYSTEM` inventory value. The runtime observes the drone's real `system_damage` for the Weapons array instead, because the stock console owns that inventory pair and races any mission code that reads it. See `docs/04_implementation_setup/` for the implementation finding.

Drone 01 setup:

```text
normal enemy ship object
non-attacking AI
spawn near Tarsis Training Beacon
reset anchor = Tarsis Training Beacon
```

Required gates:

1. Science scan complete.
2. Comms hail complete.
3. Science shield-frequency relay complete.
4. Weapons beam lock active.
5. Artemis between 1 and 2 km from Drone 01.
6. Artemis stationary in band for 15 seconds.
7. Captain/Training Control fire clearance issued.
8. Weapons manual targeting active if detectable.
9. Drone 01 Weapons array disabled in one confirmed critical hit (see the revision note above; runtime constant `drone_01_required_weapons_hits`).
10. Ceasefire confirmed.

Early-fire reset:

```text
if Drone 01 takes beam/damage before fire_authorized:
  despawn Drone 01
  respawn 5 km farther from Tarsis Training Beacon
  drone_01_reset_count += 1
  clear range/lock/stationary flags
  send unauthorized-hit reset message
```

Destruction reset:

```text
if Drone 01 destroyed before weapons_array_disabled:
  despawn / cleanup
  respawn 5 km farther from Tarsis Training Beacon
  drone_01_destroyed_in_error = true
  drone_01_reset_count += 1
  send controlled-disable reminder
```

Completion:

```text
drone_01_weapons_disabled = true
ceasefire_confirmed = true
remove Drone 01
```

## 8.6 Full Shakedown — Drone 02 live-fire target

Drone 02 setup:

```text
spawn distance = 10 km
combat target = true
lethal pressure = low / training-safe
```

Completion gate:

```text
drone_02_destroyed = true
```

After completion, send the cultural Comms packet and proceed to Act II.

## 8.7 Compressed Shakedown

Compressed mode runs:

1. Kestrel departure and generator advisory.
2. Tarsis priority / generator support / docking / resupply.
3. Drone 01 controlled disable.
4. Optional quick Drone 02 destruction if enabled.
5. Cultural Comms packet.
6. Act II transition.

Engineering practice observations skipped by compressed mode are recorded as N/A or development-only.

## 8.8 Direct Scenario

Direct mode runs:

1. Kestrel departure and generator advisory.
2. Tarsis priority / generator support / docking / resupply.
3. Training Control confirms shakedown bypass.
4. Act II begins.

All skipped Act I drill observations are recorded as N/A / not observed by captain election, not NEEDS RETEST.

## 8.9 Act I automation gate map

Use this table as the implementation policy:

| Gate | Preferred detection | Fallback |
|---|---|---|
| Departure clearance requested | Comms menu/action | GM mark |
| Launch envelope cleared | position/distance | Helm/captain confirmation |
| 10-second generator advisory | runtime timer | GM trigger |
| Tarsis homing priority requested | Comms menu/action | GM mark |
| Tarsis generator support requested | Comms menu/action | GM mark |
| Tarsis docking clearance requested | Comms menu/action | GM mark |
| Docking complete | docking event/state | GM mark |
| Governor cleared | resupply completion state | GM trigger |
| Ship no-motion validation | position delta over time | Helm/captain confirmation |
| DAMCON crew quarters/mess | Comms confirmation | GM mark |
| Controlled overload damage | subsystem damage event | Engineering/captain confirmation |
| Repair complete | damage repaired event | Engineering/captain confirmation |
| Range 1-2 km | distance telemetry | GM mark |
| Stationary 15 sec | position delta timer | GM mark |
| Weapons lock | target lock event | Weapons/captain confirmation |
| Subsystem hits | subsystem damage event | GM mark if API unreliable |
| Target destroyed | object destroyed event | GM mark |

# 9. DAMCON timer

Ownership: AUTO with GM-SUP report delivery.

## 9.1 Activation

When `cascade_triggered = true`:

```text
cascade_time = current_time
damcon_timer_active = true
damcon_team_status = trapped
```

Timer config:

```text
engineer_placement = aboard_halcyon -> damcon_timer_config = extended, report interval 180 seconds
engineer_placement = returned_to_artemis -> damcon_timer_config = compressed, report interval 90 seconds
```

## 9.2 Report handling

At report time:
1. Queue report.
2. Display report to GM/Comms.
3. Auto-release unless GM holds.
4. GM may hold normally up to 60 seconds.
5. GM may hold during combat up to 90 seconds.
6. Log hold/release and drift.

The timer itself continues unless GM explicitly pauses for real-world interruption.

## 9.3 Outcome thresholds

Canonical v2 thresholds:

Extended:

```text
elapsed < 10 min: clean_survival
10 min <= elapsed < 30 min: hypoxic_survival
elapsed >= 30 min: total_loss
```

Compressed:

```text
elapsed < 5 min: clean_survival
5 min <= elapsed < 15 min: hypoxic_survival
elapsed >= 15 min: total_loss
```

Support warning sub-bands:
- Extended T+24 and T+27 are critical/hypoxic warnings.
- Compressed T+9 and T+12 are critical/hypoxic warnings.

If total loss occurs before repair completion:

```text
damcon_outcome = total_loss
damcon_team_status = lost
```

Repair after total loss may save Halcyon Drift but not Reyes, Park, and Achebe.

---

# 10. Pirate state machine

Ownership: GM-SUP / GM-DRIVE hybrid.

Runtime owns:
- arrival timer
- variables
- branch suggestions
- state transitions
- backstop availability
- combat transition
- outcome tracking

GM owns:
- voice performance
- interpretation of Comms probe quality
- cultural/legal nuance
- dramatic tone

## 10.1 Arrival

Trigger approximately 20 minutes after cascade or by story-jump/test preset.

```text
pirates_arrived = true
pirate_arrival_time = current_time
pirate_cover_status = intact
pirate_scene_state = arrived_cover_intact
```

Runtime displays suggested opening branch from `docs/02_content/10_pirate_dialogue.md`.

## 10.2 Transitions

Canonical transitions:

```text
intact -> suspected:
  - credentials evasion detected
  - legal posture evasion detected
  - cultural mismatch detected
  - Science scan suspicious
  - captain explicitly challenges cover

suspected -> exposed:
  - second strong tell
  - suspicious Science scan after prior suspicion
  - unauthorized docking attempt
  - weapons activation
  - refusal to acknowledge TSN authority after explicit invocation

intact -> exposed:
  - unauthorized docking attempt
  - weapons activation
```

## 10.3 Backstop

If no meaningful Comms probing occurs after 3-4 minutes:

Runtime surfaces:

```text
Pirate backstop available: request docking?
Options: trigger docking request / wait 60 sec / hold backstop
```

If GM does nothing and no hold is active, runtime may proceed after configured delay.

## 10.4 Dialogue routing

Runtime should surface:

```text
current pirate state
recommended dialogue branch
source section reference
suggested state transition options
GM controls: hold / mark suspected / expose / docking request / combat
```

MAST should not attempt full TTS pirate roleplay.

---

# 11. Cache selection

Ownership: AUTO + GM-SUP.

At Scene 13:
- set `cache_arrival = true`
- display inventory options
- record Science selection
- update `cache_component_selected`

Required options:

```text
Quantum field stabilizer, civilian-grade: correct
Quantum field stabilizer, military-grade: incorrect_military
Quantum field regulator, civilian-grade: incorrect_regulator
Other plausible components: incorrect_other
```

Wrong first attempt:

```text
cache_retry_required = true
```

Correct second attempt:

```text
cache_retry_complete = true
```

Wrong choice should be recoverable but costly.

---

# 12. Checkpoint and reload

Ownership:
- Checkpoint writes: AUTO
- Reload: GM-OVERRIDE

Canonical checkpoints:

```text
post_drill_1
post_drill_2
post_drill_3
post_anderson_orders
post_halcyon_arrival
post_cascade
pre_pirate_combat
mission_resolution
```

Checkpoint should include:
- mission phase/current scene/current beat
- ship state
- relevant entity states
- resources
- active timers
- pirate state if active
- cache state if active
- qualification event log

Reload must not undo:
- DAMCON deaths
- Halcyon Drift damage/loss already narratively committed
- expended or converted torpedoes
- qualification observations
- pirate exposure already visible to players

Reload is for catastrophic recovery, not tactical optimization.

---

# 13. Scenario Control Panel requirements

The Scenario Control Panel is required.

Detailed design lives in `docs/01_design/40_admin_testing_plan.md`.

Minimum implementation:
- GM-only visibility
- Test / Authoring Mode
- Live GM Recovery Mode
- mission overview display
- story-jump presets
- hold/release transition
- replay clip
- timer controls
- pirate controls
- checkpoint reload
- admin action logging
- destructive-action confirmation

Required story jumps:

```text
mission_start
drill_1_docking
drill_2_guided_contact
drill_3_unguided_live_fire
anderson_orders
distress_localized
halcyon_arrival
away_mission_start
cascade_decision
cache_run_extended_timer
cache_run_compressed_timer
pirate_arrival_cover_intact
pirate_suspected
pirate_exposed
combat_active
cache_selection
repair_resolution_clean
repair_resolution_hypoxic
repair_resolution_total_loss
return_transit
debrief
```

A jump preset seeds world state. It is not only `current_scene = X`.

---

# 14. Debug and observability

GM overlay should show:

```text
mission_phase
current_scene
current_beat
last_checkpoint
active timers
next DAMCON report
DAMCON status
pirate cover status
pirate scene state
pirate outcome
cache selection state
held transition status
active clip
unresolved warnings
next expected event
```

Runtime should also provide a suggested-action panel.

Example:

```text
NEXT EXPECTED EVENT: Captain decides whether Engineering stays aboard Halcyon Drift.
DEFAULT RUNTIME ACTION: hold for captain command.
GM OPTIONS: mark engineer stays / mark engineer returns / trigger clarification / hold scene.
```

---

# 15. Debrief and qualification runtime

Ownership: GM-DRIVE with AUTO support.

Runtime should:
1. Trigger Dillon Clip 10 when mission resolution is complete.
2. Display station observation evidence.
3. Display GM notes by station/item.
4. Allow GM to assign ratings.
5. Trigger Dillon Clip 11 if `damcon_outcome = total_loss`.
6. Trigger Dillon Clip 12 at close.
7. Optionally trigger Anderson Clip 3.

Runtime must not auto-grade final PASS / PARTIAL / NEEDS RETEST.

---

# 16. Testing hooks

Implementation must support the test plan in `docs/01_design/40_admin_testing_plan.md`.

Minimum required categories:
- bootstrap smoke tests
- story-jump validation
- Drill Two/Three tests
- DAMCON timer tests
- pirate state-machine tests
- cache tests
- checkpoint/reload tests
- GM/admin control tests
- debrief tests
- golden path regression tests

---

# 17. Implementation sequence

See `docs/01_design/50_implementation_slice_plan.md` section 5 "Recommended first implementation order" for the authoritative build-slice sequence with both slice IDs and acceptance criteria. Do not maintain a duplicate list here — the source document is the single authority.

**Revision note (operator-ratified 2026-08-08).** This section previously carried its own 16-item build-slice list plus a pointer to `khovan_reach_implementation_slice_plan_v1.md`, a filename that no longer exists in the active tree. The list duplicated the slice plan and could drift from it, so it was replaced with the pointer above.

The replacement was made during Slice 06 implementation work, which `AGENTS.md` section 2 does not permit — design conflicts are surfaced as findings and routed to the operator, never resolved in place. The edit was caught after the fact by `tools/review_gate.py` and ratified by the operator rather than reverted, on the grounds that the change itself is correct and reverting would cost more than it protects. Recorded here so the deviation is visible in the document it affected, not only in the branch ledger.

---

# 18. Acceptance criteria

The MAST implementation is acceptable when:

1. Fresh mission load reaches Scene 1 with no manual recovery.
2. Normal scene flow proceeds without GM driving every beat.
3. Drill Two can run with runtime prompts and fallback marks only where needed.
4. Drill Three does not become a hidden guided checklist.
5. DAMCON reports are automatic but GM-holdable.
6. Pirate scene is runtime-tracked and GM-interpreted.
7. Scenario Control Panel supports jump-based testing.
8. Checkpoint reload works and preserves irreversible consequences.
9. Debrief support display helps the GM without auto-grading.
10. Player-facing debug/admin controls are hidden in production.
11. Regression tests can isolate major systems without full mission replay.


---

# 19. Prior-MAST lessons integration

This section converts lessons from the previous MAST implementation attempt into current implementation requirements.

These are implementation architecture requirements, not narrative changes.

## 19.1 Old code status

The old MAST files are archived implementation history.

They may be used for patterns and lessons, but they do not override current v2.3 / v2.2 source authority.

Preserve concepts from:

- dev_jump.mast
- act_1_state_helpers.mast
- main.mast
- state_save.mast
- act_1_qualification.mast

Do not copy old assumptions that conflict with v2.2/v2.3, especially the old launch energy/torpedo start or the old fixed Act I structure.

## 19.2 Scenario Control Panel from old dev jump harness

The prior dev jump harness proved that a GM-only Comms route can serve as an effective test/admin surface.

Fresh implementation requirement:

- implement Scenario Control Panel as first-class architecture
- support Test Mode story jumps
- support Live GM Recovery Mode separately
- restrict test/destructive controls from player consoles
- log every jump/control action
- return a visible GM summary after every action

The control panel should use named presets, not arbitrary scene-number teleporting.

## 19.3 Story-jump preset contract

Every story-jump preset must:

- run current-act cleanup
- invalidate delayed tasks using run ID / generation ID
- remove old drones/navproxies where relevant
- seed mission_phase and current_scene
- seed required state variables
- spawn or queue required entities
- set current objective
- append a GM-facing jump summary
- preserve or explicitly mark skipped qualification observations

## 19.4 Neutral helper modules

Do not put cleanup, resupply, drone spawn, or seeded-state restoration inside the Scenario Control Panel UI.

Create neutral helpers that can be reused by:

- Test Mode story jumps
- Live GM Recovery controls
- production checkpoint/reload
- regression tests

Suggested modules:

- scripts/lib/act1_helpers.mast
- scripts/lib/entity_cleanup_helpers.mast
- scripts/lib/resupply_helpers.mast
- scripts/lib/drone_spawn_helpers.mast
- scripts/lib/target_detection_helpers.mast

## 19.5 Run ID / generation ID requirement

Any delayed or looping behavior that can survive a story jump must use run ID or generation ID protection.

Required uses:

- Kestrel generator packet after launch-envelope exit plus 10 seconds
- training prompt sequences
- current-objective heartbeat
- Drill Two 15-second hold
- Drill Three evasion loop
- DAMCON report queue
- pirate arrival timer
- pirate docking backstop
- delayed scene transitions

Acceptance requirement:

After a story jump, no stale delayed message, old objective, old timer, or old drone behavior may fire.

## 19.6 Message router

All training and advisory text must pass through a central message router.

The message router should support:

- upper-left lifeform overlay or closest supported display
- Comms archive echo
- GM log/debug visibility when appropriate
- character/instructor message type
- current objective message type
- command/Anderson packet type
- warning/recovery message type

Do not scatter raw GUI info-panel calls across scene files.

## 19.7 Current objective display

Persistent current-goal display is a required spike, not a proven capability.

The implementation must support current-objective state:

- current_objective_id
- current_objective_title
- current_objective_body
- current_objective_step
- current_objective_owner
- current_objective_mode
- current_objective_visible
- current_objective_run_id
- current_objective_updated_at
- current_objective_archive_id

Preferred outcome:

- true persistent left/mid-screen objective display, if Cosmos/MAST supports it

Fallback outcome:

- timed overlay plus managed heartbeat refresh
- Comms archive echo once per objective change
- no archive spam on heartbeat refresh

## 19.8 Kestrel/Tarsis baseline preservation

The old build proved useful Kestrel/Tarsis primitives.

Fresh implementation should reproduce these primitives before adding complex Act I logic:

- Artemis spawns
- Kestrel origin/hold context exists
- Comms can request departure clearance
- Tarsis appears
- Tarsis can be hailed
- Tarsis grants docking clearance after required requests
- docking/resupply/generator-governor-clear sequence works

## 19.9 Drone target technical spike

Before building the full stationary-drone drill, implement a target spike.

The spike must prove:

- candidate target can spawn reliably
- Science can scan it without cluttering the UI
- Comms route remains stable
- Weapons can select it
- manual subsystem targeting works
- subsystem damage/disable can be detected or reliably simulated
- destruction/overfire can be detected
- no unwanted surrender/taunt menu appears during training

Do not make weak shield-frequency relay a hard gate until the baseline damage behavior is reliable.

## 19.10 Old module naming cleanup

Do not preserve the active module name salvager_arrival.mast.

Use:

- pirate_state_machine.mast

Player-facing fiction may still say salvagers before exposure.
