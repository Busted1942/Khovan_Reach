# KHOVAN REACH — MAST FILE LESSONS EXTRACT

Version: 1.0
Status: Setup / implementation-handoff note
Purpose: Extract useful implementation lessons from the prior MAST files without treating the old code as current design authority.

---

# 1. Decision

The old MAST files contain useful implementation patterns.

They should be transferred as implementation lessons, not copied forward as current scenario design.

Current v2.2 architecture remains authoritative.

The old MAST files are most useful for:

- GM-only jump harness pattern
- text prompt routing pattern
- reusable helper separation
- stale-task invalidation with run IDs
- Kestrel/Tarsis baseline setup
- docking/resupply hooks
- drone spawn/cleanup patterns
- automatic gate examples
- target-selection and subsystem-damage experiments
- warning signs about old assumptions

---

# 2. Files Reviewed

The following old implementation files were reviewed:

- main.mast
- dev_jump.mast
- act_1_qualification.mast
- act_1_state_helpers.mast
- act_2_investigation.mast
- act_3_khovan_reach.mast
- damcon_timer.mast
- salvager_arrival.mast
- state_save.mast
- __init__.mast

---

# 3. Transfer These Patterns

## 3.1 GM-only jump route worked well

The old dev_jump.mast uses a GM-only Comms route:

- Khovan Dev Jumps
- restricted by gamemaster role checks
- returns to the same GM jump menu after each jump
- sends a jump summary to Comms
- stores dev_jump_anchor and dev_jump_summary

Transfer this into the v2.2 Scenario Control Panel.

Do not preserve the name "Khovan Dev Jumps" as the production-facing concept. Rename conceptually to:

- Scenario Control Panel
- Test Mode Story Jumps
- Live GM Recovery Mode

Implementation lesson:

- GM-only Comms menus are viable for test controls.
- Each jump should return an immediate confirmation packet.
- Each jump should record anchor, scene, seeded state, and next expected action.

---

## 3.2 Curated jump anchors were the right model

The old dev jump harness did not teleport to arbitrary scene numbers. It used curated anchors:

- normal start
- Scene 1 departure
- Scene 2 Drill One
- Drill Two start
- Drill Two steps 1 through 10
- Scene 4 Drill Three
- Act II / Anderson Orders

Transfer this principle directly.

Fresh implementation rule:

- story jumps are named presets
- each preset seeds world state
- each preset sets expected next action
- each preset logs what was dev-seeded and what was not observed for qualification

Do not implement raw "current_scene = X" jump controls as the primary mechanism.

---

## 3.3 Dev jump summary is valuable

The old dev_jump_summary format carried:

- anchor
- scene
- drone state
- prior checks
- next expected action

Keep this idea.

Fresh implementation should show this in the GM Scenario Control Panel after every jump.

Recommended fields:

- jump_id
- display_name
- target_scene
- seeded_state_summary
- spawned_entities
- expected_next_event
- skipped_observations
- warnings
- validation_result

---

## 3.4 Helper separation was a strong design choice

The old act_1_state_helpers.mast separated neutral state helpers from dev_jump.mast.

This is one of the best old-build lessons.

Fresh build should preserve the separation:

- Scenario Control Panel owns UI controls.
- Helper modules own cleanup, seeding, spawning, resupply, and selections.
- Production checkpoint/reload should reuse neutral helpers.
- Test Mode should not be the only owner of restore logic.

Recommended fresh modules:

- scripts/systems/scenario_control_panel.mast
- scripts/systems/story_jump_presets.mast
- scripts/lib/act1_helpers.mast
- scripts/lib/entity_cleanup_helpers.mast
- scripts/lib/resupply_helpers.mast
- scripts/lib/drone_spawn_helpers.mast
- scripts/lib/target_detection_helpers.mast
- scripts/systems/checkpoint_system.mast

---

## 3.5 Runtime cleanup pattern is worth preserving

The old helper layer cleared:

- Drill Two navproxy
- Drill Three navproxy
- old Drill Two drone objects
- old Drill Three drone objects
- science selection
- comms selection
- weapons selection
- stale run IDs

This should become the standard story-jump cleanup pattern.

Fresh rule:

Before any story jump, run cleanup for the current act and invalidate old delayed tasks.

Do not simply spawn new entities on top of old entities.

---

## 3.6 Run ID / generation ID pattern is essential

The old code used run IDs for:

- Dillon opening briefing sequence
- Drill Two authorization hold
- Drill Three evasion loop

This is a high-value implementation pattern.

Fresh build should use run IDs or generation IDs for every delayed or looping behavior that can survive a story jump.

Use run IDs for:

- Kestrel generator packet after launch-envelope exit plus 10 seconds
- training message sequences
- current-objective display heartbeat
- Drill Two 15-second ready hold
- Drill Three evasion loop
- DAMCON report schedule
- pirate arrival timer
- pirate docking backstop timer
- clip playback stand-ins
- delayed scene transitions

Acceptance rule:

If a story jump occurs, no stale delayed message, old objective, old timer, or old drone behavior should fire afterward.

---

## 3.7 Text prompt wrappers worked and should be generalized

The old main.mast had centralized wrappers:

- khovan_reach_dillon_text
- khovan_reach_anderson_text
- khovan_reach_objective_text

They all used gui_info_panel_send_message to send text to GUI info panels.

This is a good pattern.

Fresh build should generalize it into a message router:

- one call for character/instructor overlay
- one call for objective display
- one call for Comms archive echo
- one call for GM log/debug if needed

Current v2.2 requirement:

- training text displays through the temporary upper-left lifeform overlay
- training text echoes into the Comms archive

Fresh implementation should not scatter direct gui_info_panel_send_message calls across scene files. Route all player-facing instruction through a central message system.

---

## 3.8 Text sequencing pattern is useful

The old Act II file sequences Anderson and Dillon text using:

- task_schedule
- delay_sim
- short text chunks
- repeated overlay calls

This is a useful stand-in for later recorded clip playback.

Fresh build should keep this pattern for early development.

Do not block implementation on final audio.

Implementation rule:

- text stand-ins should be structurally equivalent to final clip triggers
- text stand-ins should be replaceable by audio/video playback later
- clip IDs should still be logged

**Active build decision (2026-08-08, plan-hardening):** confirmed by the operator — text stand-ins ship for the first playable run across all 15 specified clips (12 Dillon, 3 Anderson; see `docs/02_content/40_dillon_clips.md` and `docs/02_content/30_anderson_clips.md`). Recorded audio integration is explicitly deferred; the operator will wire it in later. Only Dillon Clip 1 has a runtime stand-in today (`scripts/systems/audio_runtime.mast`); the remaining 14 have zero runtime representation and no owning slice yet. Do not build out a general clip-playback router speculatively — extend `audio_runtime.mast` only when a slice packet actually calls for a specific clip, one at a time, following this section's stand-in pattern. When recorded-audio wiring is eventually picked up, it needs its own slice packet (playback API spike, clip file naming/placement convention, stand-in-to-audio swap mechanism) rather than retrofitting it piecemeal.

---

## 3.9 Kestrel hold loop is a useful starting pattern

The old main.mast kept Artemis at Kestrel until departure clearance by:

- setting dock_base_id
- setting dock_state
- setting throttle to zero
- resetting Artemis position
- looping until clearance flag

This aligns with the current Act I architecture, though the start state has changed.

Fresh build should adapt the hold pattern to v2.2:

- generator_governor_active is true
- starting homing torpedoes are 2
- departure requires Comms clearance
- after launch-envelope exit plus 10 seconds, Kestrel sends generator advisory
- do not reuse old 70 percent energy / 0 torpedo start as canon

---

## 3.10 Custom docking logic is valuable

The old khovan_dock_with_stock_station_release logic did several useful things:

- used normal docking/refit behavior
- restored DAMCON
- refueled
- loaded torpedoes
- triggered Drill One completion when docked after clearance
- prevented clean completion if docking occurred before clearance
- triggered next drill on undock from Tarsis under specific state conditions

Transfer the pattern, but update the gates to v2.2:

Tarsis docking should require:

- homing torpedo production priority requested
- generator support/acceptance requested
- docking clearance requested
- docking event detected

Tarsis completion should clear:

- generator_governor_active
- resupply incomplete flags
- Act I gate into selected shakedown profile

---

## 3.11 Debug tab hiding should remain baseline

The old main.mast removed debug/brain/mast tabs for normal play.

Keep this as a baseline requirement.

Fresh rule:

- Test Mode controls are GM-only.
- Live GM Recovery controls are GM-only.
- Player-facing debug tabs are hidden.
- Test-only controls are not visible in production mode.

---

## 3.12 Drone spawn and scan setup is useful

The old files used:

- npc_spawn for training drones
- sim.add_navproxy for nav/map representation
- link(player, extra_scan_source, drone)
- science scan routes
- comms routes
- weapons selection detection

This is useful and should be re-verified early.

Fresh spike:

- spawn candidate training drone
- verify Science can scan it
- verify Comms can hail or classify it
- verify Weapons can select it
- verify subsystem targeting/damage can be detected
- verify destruction/overfire can be detected

Do not build the whole drill until this target spike passes.

---

## 3.13 Auto gates already existed in the old code

The old code already had good examples of automatic gates:

- Helm transit monitor checked distance, heading vector, throttle, and speed.
- Ready posture checked range and Weapons lock.
- 15-second hold checked that range/lock remained valid.
- damage/object hooks detected hits and subsystem targets.
- damage/destroy hooks detected overfire/destruction.

This supports the current v2.2 philosophy:

- automatic gates first
- Comms/captain confirmation second
- GM manual marks last

Transfer these automatic-gate patterns.

Do not revert to GM-confirmed checks where runtime signals are reliable.

---

# 4. Do Not Transfer These Old Assumptions

## 4.1 Old source comments

main.mast still references older design sources such as old AGENTS.md and design_docs/docs/01_design/10_mast_requirements.md.

Do not preserve those comments as authority.

Fresh comments should reference v2.2 files.

---

## 4.2 Old start state

Old code used:

- artemis_start_energy_percent = 70
- artemis_start_homing_torpedoes = 0

This conflicts with current v2.2 Act I.

Fresh code should use:

- generator_governor_active = true
- starting_homing_torpedoes = 2
- generator issue explained after departure plus 10 seconds
- Tarsis clears the governor after required Comms requests and docking

---

## 4.3 Old module name salvager_arrival

Old code has salvager_arrival.mast.

Fresh code should use pirate_state_machine.mast or pirate_salvage_cover.mast.

Player-facing fiction can still say salvagers before exposure.

Runtime/module names should use pirate_* so implementation is not confused.

---

## 4.4 Old Drill Two sequence is not current canon

The old Act I file contains a large Engineering and Drill Two sequence that only partly matches current v2.2.

Use it for implementation patterns, not for exact content.

The current v2.2 narrative and MAST requirements govern:

- Full Shakedown
- Compressed Shakedown
- Direct Scenario
- generator-governor start
- automatic gates where possible
- Comms/captain confirmation for non-observable actions
- GM marks only as fallback

---

## 4.5 Text prompting worked but was transient

The old text prompting used GUI info-panel messages with a time value.

This worked for timed messages.

It did not yet solve the desired static current-goal display on the left mid-screen.

Fresh implementation should treat persistent current objective display as a separate spike, not as a side effect of the old prompt wrapper.

---

# 5. Recommended Fresh Build Order from MAST Lessons

**Note:** This section uses old planning slice numbers from before `docs/01_design/50_implementation_slice_plan.md` was finalized. These are NOT the current slice IDs. Use the finalized slice plan for current work. This section is retained as historical context on the old MAST lessons.

Slice 0:
- repo cleanup and source placement
- capture these old MAST lessons
- verify tests

Slice 1:
- mission shell
- state initialization
- Kestrel/Tarsis baseline setup
- message router shell
- debug tab hiding

Slice 2:
- Scenario Control Panel shell
- GM-only route
- action log
- mode flagging

Slice 3:
- story jump preset framework
- cleanup helpers
- run ID invalidation
- dev summary display

Slice 4:
- current-objective display spike
- overlay + Comms archive echo
- static or heartbeat current-goal display

Slice 5:
- Kestrel generator-governor start and Tarsis gate

Technical spike before full drone drill:
- target subsystem damage
- Weapons target selection
- overfire/destruction reset
- player-facing debug hidden
- stale-task invalidation under story jump

---

# 6. Final Transfer Rule

Copy patterns.

Do not copy authority.

The old MAST files are evidence of working implementation techniques, not a replacement for the v2.2 architecture.
