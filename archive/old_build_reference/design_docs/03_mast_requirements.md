# KHOVAN REACH — MAST SCRIPTING REQUIREMENTS

*Implementation specification for the MAST code. Designed to be handed to ChatGPT (or any coding assistant) as the spec for writing the actual scripts. Pair with the Pass 1 scene-by-scene play guide and the Pass 2 dialogue files.*

---

## ABOUT THIS DOCUMENT

This is not MAST code. It's the specification ChatGPT needs to produce MAST code. The required mechanics, state, triggers, and outputs are enumerated here in terms that should translate cleanly to MAST patterns once the coding assistant has reference missions to pattern-match against.

Key references the coding assistant will need:

- The sbs_utils documentation (provided as URL or saved pages)
- One or more reference missions (SecretMeeting, LegendaryMissions) for pattern-matching
- Pass 1 Rev 1.1 (the scene-by-scene play guide)
- Pass 2 files (dialogue and clip text)

The coding assistant generates MAST; the GM runs it; failures and revisions iterate through ChatGPT and Claude as needed.

---

## 1. OVERALL MISSION STRUCTURE

### Mission entry point

The mission has a single entry point. On scenario load, MAST should:

1. Initialize Artemis state per Pass 1 Section 2 (Ship State at Mission Start)
2. Initialize all state variables defined in this document to their default values
3. Trigger Dillon Clip 1 (opening briefing)
4. Begin Scene 1 (departure from Kestrel Yards)

### Scene flow

Scenes flow sequentially in the standard execution path. Some scenes branch based on captain decisions (Scene 11 fork). The MAST code should structure scenes as labels with explicit transitions.

Recommended file structure (Pass 1 already specified this):

- `main.mast` — entry point, imports act files, routes top-level execution
- `act_1_qualification.mast` — Scenes 1-4
- `act_2_investigation.mast` — Scenes 5-8
- `act_3_khovan_reach.mast` — Scenes 9-15
- `damcon_timer.mast` — Suit O2 timer mechanic
- `salvager_arrival.mast` — Pirate arrival and dialogue state machine
- `state_save.mast` — Checkpoint and reload mechanic
- `lib/` — Shared functions (audio playback, comms helpers, etc.)

---

## 2. STATE VARIABLES

All state variables the mission needs to track. ChatGPT should declare these in MAST and reference them across scenes.

### Mission state

| Variable | Type | Default | Description |
|---|---|---|---|
| `mission_phase` | enum | `initialization` | `initialization`, `act_1`, `act_2`, `act_3`, `debrief`, `complete` |
| `current_scene` | int | 0 | 1-15, matches scene numbers in Pass 1 |
| `last_checkpoint` | enum | `none` | Last checkpoint saved; targets for state-save reload |

### Drill state (Act I)

Keep the existing high-level completion flags, then track Drill Two as a guided step sequence and Drill Three as an unguided observation task.

| Variable | Type | Default | Description |
|---|---|---|---|
| `drill_1_complete` | bool | false | Dock and resupply complete |
| `drill_1_retry_occurred` | bool | false | Drill 1 was paused and retried (Dillon Clip 3 Variant B) |
| `drill_2_complete` | bool | false | Guided contact handling complete: Drone 01 Weapons subsystem disabled and ceasefire verified |
| `drill_3_complete` | bool | false | Unguided evasive live-fire repeat complete: Drone 02 Engine subsystem disabled and ceasefire verified |

#### Drill Two guided state

| Variable | Type | Default | Description |
|---|---|---|---|
| `drill_2_started` | bool | false | Drill Two has begun. |
| `drill_2_drone_id` | entity/ref | null | Runtime handle for Drill Drone 01. |
| `drill_2_current_step` | int | 0 | Current guided step, 0-10. |
| `drill_2_science_check` | bool | false | Step 1 complete: Science classified contact. |
| `drill_2_comms_check` | bool | false | Step 2 complete: Comms hail/response logged. |
| `drill_2_captain_posture_check` | bool | false | Step 3 complete: Captain authorized intercept posture, not fire. |
| `drill_2_helm_geometry_check` | bool | false | Step 4 complete: Helm established safe firing geometry. |
| `drill_2_engineering_boost_check` | bool | false | Step 5 complete: Engineering weapons boost/heat stable. |
| `drill_2_weapons_ready_check` | bool | false | Step 6 complete: Weapons selected/tuned/subtargeted Weapons. |
| `drill_2_fire_authorized_check` | bool | false | Step 7 complete: Captain authorized controlled fire. |
| `drill_2_weapons_subsystem_disabled` | bool | false | Step 8 complete: Drone 01 Weapons subsystem disabled. |
| `drill_2_ceasefire_check` | bool | false | Step 9 complete: ceasefire confirmed. |
| `drill_2_verification_check` | bool | false | Step 10 complete: Science/Comms final verification. |
| `drill_2_fire_before_authorized` | bool | false | Safety/qualification flag. |
| `drill_2_drone_destroyed` | bool | false | Drone destroyed before clean completion. |
| `drill_2_result` | enum | `pending` | `pending`, `complete`, `retry_required`, `failed_overfire`. |

#### Drill Three unguided state

| Variable | Type | Default | Description |
|---|---|---|---|
| `drill_3_started` | bool | false | Drill Three has begun. |
| `drill_3_drone_id` | entity/ref | null | Runtime handle for Drill Drone 02. |
| `drill_3_evasion_active` | bool | false | Drone evasion behavior is active. |
| `drill_3_contact_reacquired_observed` | bool | false | Observation: Science reacquired/classified target. |
| `drill_3_comms_status_observed` | bool | false | Observation: Comms monitored or relayed drone status. |
| `drill_3_captain_objective_observed` | bool | false | Observation: Captain declared Engine objective and/or fire authorization. |
| `drill_3_helm_geometry_observed` | bool | false | Observation: Helm held arc/range under evasion. |
| `drill_3_engineering_boost_observed` | bool | false | Observation: Engineering supported live fire with power/heat management. |
| `drill_3_weapons_tuning_observed` | bool | false | Observation: Weapons tuned beams/targeted Engines. |
| `drill_3_fire_before_authorized` | bool | false | Observation: Weapons fired before authorization. |
| `drill_3_engine_subsystem_disabled` | bool | false | Hard gate: Drone 02 Engine subsystem disabled. |
| `drill_3_ceasefire_confirmed` | bool | false | Hard gate: ceasefire confirmed after Engine disable. |
| `drill_3_drone_destroyed` | bool | false | Drone destroyed before Engine-disable confirmation. |
| `drill_3_help_prompt_used` | bool | false | Dillon/GM gave safety-level nudge after stall. |
| `drill_3_result` | enum | `pending` | `pending`, `complete`, `retry_required`, `failed_overfire`. |

### Anderson orders (Act II)

| Variable | Type | Default | Description |
|---|---|---|---|
| `anderson_orders_received` | bool | false | Set true when Anderson Clip 1 plays |
| `captain_acknowledged_orders` | bool | false | Captain has acknowledged the diversion order |
| `distress_signal_detected` | bool | false | Science has detected the partial signal |
| `captain_deviated_to_distress` | bool | false | Captain ordered course change to Halcyon Drift |

### Halcyon Drift state (Act III)

| Variable | Type | Default | Description |
|---|---|---|---|
| `engineer_deployed_to_halcyon` | bool | false | Engineering and DAMCON team transferred |
| `damcon_team_count_aboard_artemis` | int | 6 | Standard 6 teams; reduce to 5 when 3 personnel transfer |
| `convergence_revealed` | bool | false | Engineering has identified the cache requirement |
| `cascade_triggered` | bool | false | The atmospheric loss cascade has happened |
| `cascade_time` | timestamp | null | Time when cascade triggered, for timer calculation |

### Captain's decisions

| Variable | Type | Default | Description |
|---|---|---|---|
| `engineer_placement` | enum | `not_decided` | `not_decided`, `aboard_halcyon`, `returned_to_artemis` |
| `torpedoes_converted` | int | 0 | Number of torpedoes converted to energy |
| `artemis_departed_for_cache` | bool | false | Captain ordered the cache run |
| `force_authorized` | bool | false | Captain authorized weapons-free on the pirates |

### DAMCON team state

| Variable | Type | Default | Description |
|---|---|---|---|
| `damcon_team_status` | enum | `pending` | `pending`, `active`, `trapped`, `extended_mitigation`, `compressed_mitigation`, `recovered_clean`, `recovered_hypoxic`, `lost` |
| `damcon_timer_config` | enum | `none` | `none`, `extended` (30 min), `compressed` (15 min) |
| `next_damcon_report_time` | timestamp | null | Schedule the next scheduled report |
| `damcon_reports_delivered` | int | 0 | Count of reports given, for indexing the next one |
| `damcon_outcome` | enum | `pending` | `pending`, `clean_survival`, `hypoxic_survival`, `total_loss` |

### Cache state

| Variable | Type | Default | Description |
|---|---|---|---|
| `cache_arrival` | bool | false | Artemis has reached the Khovan Reach cache |
| `cache_component_selected` | enum | `none` | `none`, `correct`, `incorrect_military`, `incorrect_regulator`, `incorrect_other` |
| `cache_retry_required` | bool | false | First selection was wrong; return trip required |
| `cache_retry_complete` | bool | false | Correct component obtained on second attempt |

### Pirate state machine (Scene 12 — from Pass 1 Rev 1.1)

| Variable | Type | Default | Description |
|---|---|---|---|
| `pirate_cover_status` | enum | `intact` | `intact`, `suspected`, `exposed` |
| `pirates_arrived` | bool | false | Pirates within sensor range |
| `pirate_arrival_time` | timestamp | null | For salvager arrival timer calculation |
| `credentials_requested` | bool | false | Comms asked for credentials |
| `credentials_provided` | enum | `none` | `none`, `partial`, `evasive`, `refused` |
| `legal_posture_challenged` | bool | false | Comms invoked rescue law |
| `cultural_mismatch_observed` | bool | false | Comms identified species protocol mismatch |
| `science_scan_completed` | bool | false | Science scanned the pirates |
| `science_scan_result` | enum | `none` | `none`, `clean`, `suspicious` |
| `docking_requested` | bool | false | Pirates requested docking with Halcyon Drift |
| `docking_denied` | bool | false | Captain or Hessler denied docking |
| `unauthorized_docking_attempt` | bool | false | Pirates breached approach envelope without authorization |
| `combat_active` | bool | false | Pirate combat in progress |
| `pirate_outcome` | enum | `pending` | `pending`, `fleeing`, `fled`, `surrendered`, `destroyed`, `boarded`, `escaped_with_cargo` |

### Halcyon Drift outcome

| Variable | Type | Default | Description |
|---|---|---|---|
| `halcyon_repair_complete` | bool | false | The stabilizer is installed and reactor stable |
| `halcyon_outcome` | enum | `pending` | `pending`, `repaired`, `lost`, `partially_damaged` |
| `hessler_status` | enum | `aboard_halcyon` | `aboard_halcyon`, `aboard_artemis`, `lost` |

---

## 3. ACT I DRILL IMPLEMENTATION

### Design summary

**Drill Two** is a guided tutorial. It advances through a fixed sequence of station checks. Each check is either detected mechanically or marked by a GM-only control.

Hard completion gate:

- All guided steps complete.
- Drone 01 Weapons subsystem disabled.
- Ceasefire and final verification complete.

**Drill Three** is an unprompted transfer task. It should not be step-gated like Drill Two. The crew receives the objective and constraints, then executes independently.

Hard completion gate:

- Drone 02 Engine subsystem disabled.
- Ceasefire confirmed.
- Drone not destroyed before Engine-disable confirmation.

Process behaviors in Drill Three should be tracked for debrief, not silently used as hidden blockers unless the behavior is mechanically necessary to disable Engines.

### Guided Drill Two implementation

#### Start sequence

When Scene 3 starts:

1. Set `current_scene = 3`.
2. Set `drill_2_started = true`.
3. Set `drill_2_current_step = 0`.
4. Play Dillon Clip 4.
5. Spawn Drill Drone 01 at long range.
6. Store reference in `drill_2_drone_id`.
7. Configure it passive: no fire, no evasion.
8. Configure targetable Weapons subsystem if supported.
9. Advance to Step 1.

#### Step advancement model

Implement a function or label equivalent to `advance_drill_2_step` using local project conventions.

Conceptual behavior:

```text
When current step check becomes true:
  send completion line or GM-facing marker
  increment drill_2_current_step
  send next step prompt
```

The exact implementation may be event-driven, timer-polled, or GM-command-driven depending on current MAST patterns.

#### Drill Two step map

| Step | Set current step | Prompt | Completion flag |
|---|---|---|---|
| 1 | `drill_2_current_step = 1` | Science scan/classify. | `drill_2_science_check` |
| 2 | `drill_2_current_step = 2` | Comms hail/report response. | `drill_2_comms_check` |
| 3 | `drill_2_current_step = 3` | Captain authorize intercept posture. | `drill_2_captain_posture_check` |
| 4 | `drill_2_current_step = 4` | Helm establish safe firing geometry. | `drill_2_helm_geometry_check` |
| 5 | `drill_2_current_step = 5` | Engineering boost weapons power and report stable. | `drill_2_engineering_boost_check` |
| 6 | `drill_2_current_step = 6` | Weapons select/tune/subtarget Weapons, hold fire. | `drill_2_weapons_ready_check` |
| 7 | `drill_2_current_step = 7` | Captain authorize controlled fire. | `drill_2_fire_authorized_check` |
| 8 | `drill_2_current_step = 8` | Weapons disable Weapons subsystem. | `drill_2_weapons_subsystem_disabled` |
| 9 | `drill_2_current_step = 9` | Captain/Weapons ceasefire. | `drill_2_ceasefire_check` |
| 10 | `drill_2_current_step = 10` | Science/Comms verify status. | `drill_2_verification_check` |

#### Mechanical versus GM-observed checks

Use mechanical detection where verified. Use GM-only mark commands where not verified.

Recommended GM-only fallback commands:

```text
mark_d2_science_check
mark_d2_comms_check
mark_d2_captain_posture
mark_d2_helm_geometry
mark_d2_engineering_boost
mark_d2_weapons_ready
mark_d2_fire_authorized
mark_d2_weapons_disabled
mark_d2_ceasefire
mark_d2_verification
reset_drill2_current_step
reset_drill2_full
```

Do not expose these controls on player-facing consoles unless that is already normal Cosmos behavior.

#### Drill Two hard completion guard

Set `drill_2_complete = true` only when:

```text
drill_2_science_check == true
drill_2_comms_check == true
drill_2_captain_posture_check == true
drill_2_helm_geometry_check == true
drill_2_engineering_boost_check == true
drill_2_weapons_ready_check == true
drill_2_fire_authorized_check == true
drill_2_weapons_subsystem_disabled == true
drill_2_ceasefire_check == true
drill_2_verification_check == true
drill_2_drone_destroyed == false
```

On completion:

1. Set `drill_2_result = complete`.
2. Play Dillon Clip 5.
3. Save checkpoint `end_drill_2`.
4. Transition to Scene 4.

#### Drill Two safety flags

If weapons fire occurs before `drill_2_fire_authorized_check == true`, set:

```text
drill_2_fire_before_authorized = true
```

Then pause or reset to Step 6/7 if current implementation supports it. If fire detection is not available, GM handles manually.

If Drone 01 is destroyed before `drill_2_weapons_subsystem_disabled == true`, set:

```text
drill_2_drone_destroyed = true
drill_2_result = failed_overfire
```

Do not auto-complete the drill.

### Unguided Drill Three implementation

#### Start sequence

When Scene 4 starts:

1. Set `current_scene = 4`.
2. Set `drill_3_started = true`.
3. Play Dillon Clip 6.
4. Spawn Drill Drone 02.
5. Store reference in `drill_3_drone_id`.
6. Configure simple evasion.
7. Set `drill_3_evasion_active = true` when evasion begins.
8. Configure targetable Engine subsystem if supported.
9. Do not send step prompts.

#### Evasion requirement

Keep evasion simple and legible:

- Slow turn.
- Periodic heading changes.
- Short throttle pulses.
- Lateral drift.

Any one is sufficient. Do not implement advanced tactics.

#### Observation flags

Observation flags may be set mechanically or by GM-only marks. They are for debrief and qualification, not hard completion blockers.

Recommended GM-only observation marks:

```text
observe_d3_science_reacquired
observe_d3_comms_status
observe_d3_captain_objective
observe_d3_helm_geometry
observe_d3_engineering_boost
observe_d3_weapons_tuning
observe_d3_fire_before_authorized
observe_d3_help_prompt_used
```

Use these to support the debrief. Do not require them for `drill_3_complete` unless local design explicitly chooses stricter behavior after playtest.

#### Drill Three hard completion guard

Set `drill_3_complete = true` only when:

```text
drill_3_engine_subsystem_disabled == true
drill_3_ceasefire_confirmed == true
drill_3_drone_destroyed == false
```

On completion:

1. Set `drill_3_result = complete`.
2. Play Dillon Clip 7.
3. Save checkpoint `end_drill_3`.
4. Transition to Anderson orders / Act II exactly as before.

#### Drill Three overfire behavior

If Drone 02 is destroyed before `drill_3_engine_subsystem_disabled == true`, set:

```text
drill_3_drone_destroyed = true
drill_3_result = failed_overfire
```

Do not auto-complete.

If Drone 02 is destroyed after Engine subsystem disable but before ceasefire is confirmed, mark completion according to playtest choice:

- Conservative: require retry or mark PARTIAL.
- Practical: allow completion but record late ceasefire/overfire as PARTIAL for Weapons and Captain.

Recommended for first implementation: allow GM discretion instead of hard-coding a punitive branch.

#### Drill Three help prompt

If the crew stalls and GM/Dillon gives the single allowed nudge, set:

```text
drill_3_help_prompt_used = true
```

This should not block completion, but should be available for qualification/debrief.

### Subsystem detection priority

Codex must verify whether Cosmos/MAST exposes subsystem damage or disable state for NPC/drone entities.

Priority order:

1. Use native subsystem-damage/disabled API if available.
2. Use target tags or scripted damage callbacks if examples show a supported pattern.
3. Use GM-observed manual mark command as fallback.

Do not invent property names such as `drone.weapons_disabled`, `subsystem_health`, or `engine_damage` unless verified in repo examples or docs.

### Engineering boost detection priority

Codex must verify whether current mission code can read Engineering power allocation, beam output, overboost, heat, or coolant state.

Priority order:

1. Use native Engineering/ship power API if examples show it.
2. Use a threshold on weapon power/beam output if documented.
3. Use GM-observed mark command as fallback.

For Drill Two, the boost check is a guided hard gate.

For Drill Three, the boost is an observation flag unless it is mechanically required to achieve Engine disable.

---

## 4. SCRIPTED TIMING MECHANICS

### DAMCON suit O2 timer

**Activation:** When `cascade_triggered = true`, set `cascade_time = current_time` and initialize the timer.

**Configuration:** Based on `engineer_placement`:
- `aboard_halcyon`: `damcon_timer_config = extended`, report interval = 180 seconds (3 minutes)
- `returned_to_artemis`: `damcon_timer_config = compressed`, report interval = 90 seconds

**Report delivery:** At each report interval, fire a scripted comms message from the DAMCON team. Sequential reports use the text in `03_damcon_reports.md` corresponding to the elapsed time.

**Outcome evaluation:** When `halcyon_repair_complete = true`, calculate elapsed time from cascade:
- Extended config: <T+10 min = `clean_survival`, T+10 to T+25 min = `hypoxic_survival`, >T+25 min = `total_loss`
- Compressed config: <T+5 min = `clean_survival`, T+5 to T+10 min = `hypoxic_survival`, >T+10 min = `total_loss`

If timer reaches the loss threshold before repair completes, set `damcon_outcome = total_loss` and `damcon_team_status = lost`. Repair attempts after this point save Halcyon Drift but not the team.

### Salvager arrival timer

**Activation:** When `cascade_triggered = true`, schedule pirate arrival at `cascade_time + 1200 seconds` (20 minutes).

**Trigger:** At scheduled time, set `pirates_arrived = true` and `pirate_arrival_time = current_time`. Fire the initial pirate hail per `02_pirate_dialogue.md` Section 3.

**Subsequent behavior:** Driven by the pirate state machine (Section 5 below).

### Cache transit timing

The cache run is real game time. Helm controls speed.

- Standard cruise: ~25 minutes round trip
- With torpedo conversion: ~15 minutes round trip
- With cache retry (wrong component first time): add ~15 minutes

These are calibration targets. MAST should not enforce arrival times rigidly — let Helm's actual play determine arrival. The timer math works out naturally given the suit O2 timer's pace.

---

## 5. PIRATE STATE MACHINE LOGIC

The state machine drives Scene 12 dialogue branching. ChatGPT should implement this as a series of guarded transitions.

### Transition triggers

**`intact` → `suspected`:** Any one of:
- Comms requests credentials AND pirates respond evasive/refused
- Comms invokes rescue law AND pirates respond evasive
- Comms invokes cultural protocol AND pirates respond inconsistently
- Comms challenges operational conduct AND pirates respond inconsistently
- Science scan returns `suspicious`
- Captain explicitly names the pirates as suspect to the bridge

**`suspected` → `exposed`:** Any one of:
- A second probe trigger from the list above
- `unauthorized_docking_attempt = true`
- Pirates fire on Artemis or Halcyon Drift
- Captain explicitly accuses the pirates and demands surrender

**`intact` → `exposed` (skip suspected):**
- `unauthorized_docking_attempt = true`
- Pirates fire on Artemis or Halcyon Drift

### Dialogue routing

Each pirate dialogue line from `02_pirate_dialogue.md` is keyed to state. When a pirate is hailed or responds, MAST should:

1. Check current state of relevant variables
2. Look up appropriate dialogue line per the Pass 2 document
3. Deliver via Comms console (TTS or pre-recorded; pre-recorded is harder to vary)
4. Update state variables based on the player's response

For MAST simplicity, the dialogue is delivered as comms messages that the GM voices live. The MAST script triggers the *type* of response needed (e.g., "fire evasive credentials response"); the GM reads the corresponding text.

This is a deliberate simplification — fully scripted branching dialogue with TTS would require dozens of pre-recorded variants. GM-voiced dialogue keeps the implementation lightweight while preserving the state-machine logic.

### Combat transition

When `pirate_cover_status = exposed` AND any of (`unauthorized_docking_attempt`, captain authorizes force, pirates fire):

1. Set `combat_active = true`
2. Spawn pirate vessels as combatant entities in Cosmos
3. Configure their weapons profiles (light-to-moderate; designed to threaten Halcyon Drift, not overwhelm Artemis)
4. Begin combat-active behavior (pirates engage Artemis if it's at scene; pirates board Halcyon Drift if Artemis is distant)
5. Subsequent combat is standard SBS engagement

### Combat resolution

Pirates can flee, surrender, or be destroyed based on combat state:

- `pirate_outcome = fled`: One or both pirates retreat past sensor range while still functional
- `pirate_outcome = surrendered`: Pirates power down weapons and announce surrender; captain accepts
- `pirate_outcome = destroyed`: One or both pirates destroyed in combat
- `pirate_outcome = boarded`: Pirates successfully docked with Halcyon Drift and are in active boarding action; this is a worst-case state requiring captain intervention to clear

Mix-and-match is allowed: one pirate might be destroyed while the other flees, etc.

---

## 6. STATE SAVE AND RELOAD MECHANIC

### Checkpoint locations

The mission should save state at these points (set `last_checkpoint`):

1. End of Drill 1 (after `drill_1_complete = true`)
2. End of Drill 2 (after `drill_2_complete = true`)
3. End of Drill 3 (after `drill_3_complete = true`)
4. After Anderson orders received and captain acknowledged
5. After Halcyon Drift arrival (Scene 8 complete)
6. After cascade trigger (Scene 9 complete, going into Scene 10)

### Save contents

When a checkpoint fires, save:
- All state variables enumerated in Section 2
- Artemis ship state: energy, torpedo complement, hull integrity, DAMCON count, coolant
- Current mission position and orientation in space
- Any active mission objects (Halcyon Drift position, pirate positions if relevant)

### Reload trigger

GM-triggered. The reload is invoked via a GM command (specific MAST command depends on what sbs_cli supports — likely a slash command in the console or a debug menu).

When invoked:
1. Restore all saved state variables
2. Restore Artemis ship state
3. Restore mission position and active objects
4. Resume scene flow from the next scene after the checkpoint
5. Play a brief Dillon line: "Captain. Mission state has been restored to the last checkpoint. Continue operations."

### Reload boundaries

The reload cannot:
- Bring back dead DAMCON team members (the cascade is part of the timeline)
- Undo damage to Halcyon Drift caused by pirate action
- Restore expended torpedoes that were converted to energy (the conversion is committed)

The reload is intended for catastrophic failures (ship destruction, mission-impossible states) — not for "I wish I'd made a different decision." Players should not be told the reload exists; the GM uses it when needed without explanation.

---

## 7. AUDIO/VIDEO CLIP PLAYBACK

### Anderson clips

Three clips per Pass 2 file `04_anderson_clips.md`:

1. New Orders (Clip 1) — full video on main screen
2. Status Acknowledgment (Clip 2) — low-bandwidth packet (still image + audio)
3. Closing Acknowledgment (Clip 3, optional) — low-bandwidth packet

Triggers:
- Clip 1: Anderson orders transmitted; trigger at end of Drill 3
- Clip 2: Mission resolution; trigger after `halcyon_outcome` resolves (with appropriate variant based on outcome and DAMCON status)
- Clip 3: Mission close; trigger at end of debrief (optional, GM call)

### Dillon clips

Twelve clips per Pass 2 file `05_dillon_clips.md`:

1. Opening Briefing — mission start
2. Drill One Intro — Helm approaches Tarsis
3. Drill One Complete — resupply complete
4. Drill Two Intro — Guided Contact Handling, Artemis enters training area
5. Drill Two Complete — Drone 01 Weapons subsystem disabled, ceasefire and verification complete
6. Drill Three Intro — Now You Do It, second drone deployed
7. Drill Three Complete — Drone 02 Engine subsystem disabled and ceasefire confirmed
8. Pivot Acknowledgment — after Anderson orders
9. Distress Signal Observation — after captain deviates (optional)
10. Debrief Opening — start of debrief
11. DAMCON Replenishment — only if DAMCON loss occurred
12. Debrief Closing — end of debrief

Triggers: each clip is fired at the scene transition described in Pass 1 Section 4. MAST plays the audio file and waits for completion before continuing scene flow.

### Audio playback technical notes

Standard Cosmos mission scripting handles audio clip playback. The specific MAST commands depend on the sbs_utils version; ChatGPT should reference the documentation. Typical pattern is to play a sound file and either wait for it or continue scene flow during playback.

For video (Anderson Clip 1), the implementation may differ. Cosmos supports image-with-audio playback on the main screen; check the documentation for specifics.

---

## 8. COMMS MESSAGE SCRIPTING

Several scenes use scripted comms messages — text that appears on the Comms console for the Comms officer to read and respond to. These are:

- DAMCON team status reports (scheduled per Section 3)
- Hessler's communications (relayed through Comms; Hessler is on voice mode separately)
- Pirate dialogue (state-machine driven; GM voices live based on state)
- Anderson communications (the clips are audio/video, but text may also display)

### DAMCON reports as comms messages

Schedule comms messages at each report interval. Use the text from `03_damcon_reports.md` corresponding to the elapsed time and configuration.

Format: appear on the Comms console with sender "DAMCON Team / Reyes (or Park / Achebe)" and the message body. Comms officer reads aloud to bridge.

### Hessler comms relay

Hessler's voice-mode conversation happens off-bridge (with Engineering). Significant moments from that conversation may be relayed by Engineering through Comms to the bridge. These are improvised by the Engineering player and the GM (voicing Hessler); MAST doesn't script them directly.

What MAST does need to support: when Engineering arrives at Halcyon Drift, the Comms officer should have a clear channel to Engineering for relay purposes. The MAST script may want to surface this as a labeled comms channel ("Away Team Channel" or similar) that the Comms officer can monitor.

### Pirate dialogue routing

When pirates speak, the line is delivered through Comms console as if a hail from the pirate vessel. The GM voices the line live. MAST's job is to identify *which* line is appropriate based on the state machine.

A simple implementation: the GM has the dialogue document open and the state machine variables visible (debug display); they read the right line based on what they see. MAST doesn't need to script the dialogue text itself; it scripts the state transitions and the GM follows.

---

## 9. DEBRIEF SCRIPTING

The debrief is primarily GM-voiced with embedded Dillon clips. MAST's role:

1. Trigger Dillon Clip 10 (Debrief Opening) when mission resolution is complete
2. Provide the GM with a debrief support display showing all qualification card observations and outcomes
3. Trigger Dillon Clip 11 (DAMCON Replenishment) if `damcon_outcome = total_loss`
4. Trigger Dillon Clip 12 (Debrief Closing) at end of debrief
5. Optionally trigger Anderson Clip 3 (Closing Acknowledgment) after Dillon Clip 12

The qualification card observations are GM-tracked manually during play; MAST surfaces them at debrief if the GM has been entering them, but does not auto-evaluate them. This is intentional — the qualification framework is interpretive, not algorithmic.

---

## 10. EXPECTED MAST IMPLEMENTATION COMPLEXITY

Approximate scope of MAST work:

- **State variable declarations and initialization:** Small (~50 lines across files)
- **Act I scenes (1-4):** Medium to Large (~300-450 lines total, because Drill Two uses guided gates and Drill Three uses observation flags)
- **Act II scenes (5-8):** Medium (~150-200 lines)
- **Act III scenes (9-15):** Large (~400-600 lines)
- **DAMCON timer mechanic:** Medium (~100-150 lines)
- **Pirate state machine:** Medium (~200-300 lines)
- **State save/reload:** Small to Medium (~50-100 lines)
- **Lib functions (audio, comms, helpers):** Medium (~100-200 lines)

Total estimate: 1,300-2,000 lines of MAST across all files. Comparable to the LegendaryMissions example missions.

This is a real coding project, not a trivial script. Plan for multiple iterations with the coding assistant. Expect to playtest and revise — first version likely has bugs that surface during play.

---

## 11. HANDOFF TO CHATGPT

When you hand this document to ChatGPT (along with the other Pass documents) and ask it to begin MAST coding, recommend this sequence:

1. **First session:** Set up `main.mast` and the file structure. Declare all state variables. Verify the empty mission loads in Cosmos without errors.

2. **Second session:** Implement Scene 1 and Drill 1 (Scenes 1-2). Run in Cosmos. Verify Dillon clips fire and basic drill flow works.

3. **Third session:** Add Drills 2 and 3 (Scenes 3-4). Test the full Act I flow, including Drill Two guided gates and Drill Three unguided Engine-disable exit criteria.

4. **Fourth session:** Implement Act II (Scenes 5-8). Test the pivot and the Halcyon Drift arrival.

5. **Fifth session:** Implement Scene 9 (the away mission). This is mostly GM-driven via the Hessler voice-mode chat; MAST's role is supporting comms and triggering the cascade.

6. **Sixth-seventh sessions:** Implement the DAMCON timer and the pirate state machine. These are the most complex pieces; expect iteration.

7. **Eighth session:** Implement the cache run (Scene 13) including the recoverable failure mechanic.

8. **Ninth session:** Implement Scenes 14-15 (resolution and debrief). Integrate with the qualification framework.

9. **Tenth session:** Implement the state save/reload mechanic. Test it by deliberately destroying the ship and verifying reload works.

10. **Eleventh+ sessions:** Playtest, identify bugs, iterate with ChatGPT and Claude.

Each session is 1-3 hours of focused work. The full implementation will take 20-40 hours of development time across all sessions, plus playtest time.

---

## 12. ACT I SMOKE TESTS

### Smoke A — Drill Two guided step flow

1. Load mission.
2. Advance to Scene 3.
3. Verify Dillon Clip 4 fires.
4. Verify Drone 01 spawns passive and stationary.
5. Verify Step 1 prompt appears or can be delivered by GM.
6. Mark Step 1 complete; verify Step 2 prompt appears.
7. Repeat through Step 10.
8. Verify `drill_2_complete` remains false until all steps are complete.
9. Verify `drill_2_complete` remains false until Weapons subsystem disabled and ceasefire/verification complete.
10. Verify Dillon Clip 5 fires and checkpoint `end_drill_2` saves.

Expected result: Drill Two is a working guided checklist with visible/GM-observed step progression.

### Smoke B — Drill Two guardrails

1. Fire before authorization if safe to test, or use a simulated fire-before-authorization event.
2. Verify `drill_2_fire_before_authorized` is set or GM can mark it.
3. Destroy Drone 01 before Weapons subsystem disable if safe to test.
4. Verify `drill_2_complete` does not become true.

Expected result: Unauthorized fire and overfire do not falsely complete Drill Two.

### Smoke C — Drill Three no-step behavior

1. Advance to Scene 4.
2. Verify Dillon Clip 6 fires.
3. Verify Drone 02 spawns and evades simply.
4. Verify no step prompts are sent after intro.
5. Set observation flags manually or mechanically during play.
6. Verify observation flags do not block completion.
7. Disable Engine subsystem and confirm ceasefire.
8. Verify Dillon Clip 7 fires and checkpoint `end_drill_3` saves.

Expected result: Drill Three is an unguided task, not a hidden checklist.

### Smoke D — Drill Three exit gate

1. Try to complete Drill Three before Engine subsystem disabled.
2. Verify `drill_3_complete` remains false.
3. Disable Engines but do not confirm ceasefire.
4. Verify completion behavior matches chosen implementation.
5. Confirm ceasefire.
6. Verify completion.

Expected result: Engine disabled plus ceasefire is the hard completion condition.

---

## 13. SYNTAX UNCERTAINTY TO VERIFY

Codex must verify, not invent:

- MAST import/include syntax.
- Entity spawn syntax.
- NPC/drone faction and hostility flags.
- AI movement/evasion syntax.
- Station-specific prompts or comms message syntax.
- GM-only command/debug syntax.
- Weapons fire or damage event callbacks.
- Subsystem damage/disable API.
- Engineering power/beam/coolant/heat API.
- Audio/video clip playback syntax.
- Checkpoint save/restore syntax.
- Scene transition conventions in the current repo.

If a capability cannot be verified, use the smallest GM-observed fallback and state the limitation in commit notes.

---

## END OF MAST SCRIPTING REQUIREMENTS
