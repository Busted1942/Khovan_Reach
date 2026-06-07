# KHOVAN REACH — ADMIN CONTROL AND TESTING PLAN
*Merged Scenario Control Panel and testing/regression architecture.*

Version: 2.4 repo-consolidated branch-lifecycle update
Status: Canonical admin/testing specification  
Supersedes: `khovan_reach_scenario_control_panel_architecture.md` and `khovan_reach_testing_regression_architecture.md`

---

# 1. Purpose

**Repo-consolidation note:** This version keeps the story-jump framework and aligns file references and DAMCON threshold language with `docs/00_project/00_source_index.md`.


This document defines the admin/test layer that makes Khovan Reach practical to build, debug, regression-test, and run.

It merges:
- Scenario Control Panel architecture
- story-jump preset definitions
- testing layers
- regression matrices
- pre-session acceptance checks
- golden path tests

The goal is to avoid full 95-105 minute mission replays for every feature change.

---

# 2. Scenario Control Panel

The Scenario Control Panel is a GM/admin-only interface.

It supports:
- story jumps
- checkpoint reload
- scene hold/release
- clip replay
- timer control
- subsystem seeding
- pirate state control
- debrief synthetic states
- test validation
- action logging

It must not be visible to players.

---

# 3. Control panel modes

## 3.1 Test / Authoring Mode

Purpose:
- development
- playtest setup
- feature tests
- regression tests
- synthetic outcomes

Capabilities:
- all story jumps
- forced state changes
- forced outcomes
- arbitrary variable setting if implemented
- spawn/despawn test entities
- clear/reset tools

## 3.2 Live GM Recovery Mode

Purpose:
- protect real sessions
- correct runtime errors
- preserve pacing

Capabilities:
- reload last checkpoint
- hold/release current scene
- replay clips
- delay/trigger DAMCON report
- reset current drill
- expose pirates if jammed
- force next beat if blocked
- add qualification note

Live Mode must hide destructive Test Mode tools.

---

# 4. Control panel sections

## 4.1 Mission overview

Display:

```text
mission_phase
current_scene
current_beat
last_checkpoint
active timers
next expected event
held transition status
active warnings
```

## 4.2 Story jump presets

Display:
- jump ID
- target scene
- mode access
- seed status
- validation status

## 4.3 Scene flow controls

Controls:

```text
hold current scene
release held scene
advance to next beat
force scene exit
replay current briefing
replay last clip
mark current beat complete
```

## 4.4 System controls

Controls:

```text
timer hold/resume
trigger next DAMCON report
delay next DAMCON report
spawn/reset drill drone
reset current drill
mark pirates suspected
mark pirates exposed
trigger pirate docking request
trigger pirate combat state
force cache selection result
trigger repair resolution
```

## 4.5 Qualification notes

Controls:

```text
open station observation view
add GM note
mark observation evidence
flag retest item
preserve notes across reload
export debrief support summary
```

## 4.6 Debug/destructive tools

Test Mode only.

```text
set arbitrary variable
force DAMCON outcome
force pirate outcome
force Halcyon outcome
spawn/despawn test entities
reset all state
skip to debrief with synthetic data
clear timers
clear checkpoint data
```

---

# 5. Story jump contract

A story jump is a full world-state preset.

Required fields:

```text
jump_id
display_name
target_scene
mode_access
mission_phase
required_prior_flags
ship_state
weapons_state
damcon_state
halcyon_state
pirate_state
cache_state
timers
entities
clips
gm_display
expected_next_event
validation_checks
recovery_notes
```

---


# 6. Required story jumps

Story jumps are state presets, not scene-number assignments.

## 6.1 Act I v2.2 jump presets

```text
JUMP-001 mission_start_generator_governor
JUMP-002 post_departure_generator_packet
JUMP-003 tarsis_approach_governor_active
JUMP-004 tarsis_resupply_complete
JUMP-005 shakedown_choice_full
JUMP-006 shakedown_choice_compressed
JUMP-007 direct_scenario_after_resupply
JUMP-008 engineering_shakedown_start
JUMP-009 stationary_drone_disable
JUMP-010 live_fire_target
```

## 6.2 Act II / Act III jump presets

```text
JUMP-011 anderson_orders
JUMP-012 distress_localized
JUMP-013 halcyon_arrival
JUMP-014 away_mission_start
JUMP-015 cascade_decision
JUMP-016 cache_run_extended_timer
JUMP-017 cache_run_compressed_timer
JUMP-018 pirate_arrival_cover_intact
JUMP-019 pirate_suspected
JUMP-020 pirate_exposed
JUMP-021 combat_active
JUMP-022 cache_selection
JUMP-023 repair_resolution_clean
JUMP-024 repair_resolution_hypoxic
JUMP-025 repair_resolution_total_loss
JUMP-026 return_transit
JUMP-027 debrief
```

## 6.3 Act I preset seed requirements

### JUMP-001 mission_start_generator_governor

```text
generator_governor_active = true
starting_energy = 0
starting_homing_torpedoes = 0
homing_reserve_count = 2
energy_restored = false
current_scene = 1
Dillon Clip 1 ready
Artemis at Kestrel
```

Expected next event: Comms requests departure clearance.

### JUMP-002 post_departure_generator_packet

```text
launch_envelope_cleared = true
kestrel_generator_packet_sent = false
advisory_timer = 10 seconds or ready-to-fire
```

Expected next event: Kestrel generator advisory displays and archives.

### JUMP-003 tarsis_approach_governor_active

```text
generator_governor_active = true
starting_energy = 0
starting_homing_torpedoes = 0
homing_reserve_count = 2
Artemis approaching Tarsis
required requests unset
```

Expected next event: Comms requests homing priority, generator support, and docking clearance.

### JUMP-004 tarsis_resupply_complete

```text
tarsis_homing_priority_requested = true
tarsis_generator_support_requested = true
tarsis_docking_clearance_requested = true
tarsis_resupply_complete = true
generator_governor_active = false
generator_governor_cleared = true
```

Expected next event: shakedown profile selection or selected branch proceeds.

### JUMP-008 engineering_shakedown_start

```text
shakedown_mode = full
generator_governor_cleared = true
engineering_shakedown_complete = false
```

Expected next event: impulse zero / warp 200 instruction.

### JUMP-009 stationary_drone_disable

```text
shakedown_mode = full or compressed
drone_01_spawned = true
drone_01_weapons_disabled = false
drone_01_fire_authorized = false
```

Expected next event: scan/hail/frequency/range/lock gates.

### JUMP-010 live_fire_target

```text
shakedown_mode = full
drone_01_weapons_disabled = true
drone_02_spawned = true
drone_02_destroyed = false
```

Expected next event: captain engages and destroys target.

## 6.4 Live-mode restrictions

Live GM Recovery Mode should allow only:

```text
last_checkpoint
current_scene_start
next_scene
mission_start only before players begin
reload checkpoint
replay clip
hold/release transition
```

Test-only jumps include synthetic repair outcomes, pirate mid-states, and arbitrary Act I branch presets.

# 7. Testing layers

Khovan Reach testing uses six layers:

1. Bootstrap smoke tests
2. Story-jump preset validation
3. Subsystem regression tests
4. Golden-path regression tests
5. Pre-session acceptance tests
6. Full playtests

Full playtests remain necessary, but they should not carry the full testing burden.

---

# 7A. Testing evidence classes

Khovan testing uses separate evidence classes. They are cumulative; a stronger class does not erase the need for narrower regression checks, and a narrower class must not be reported as live runtime proof.

## 7A.1 Static/source checks

Static/source checks inspect repository files without running Cosmos. They include:

- required file presence
- JSON/Python parse checks
- forbidden old-module references
- missing active `.mast` imports where statically detectable
- generated artifact ignore checks
- documentation/governance keyword checks

These checks run through:

```text
python run_tests.py quick
```

Static/source checks can prevent obvious regressions, but they do not prove MAST runtime evaluation, GUI lifecycle behavior, player spawn behavior, or bridge/client usability.

## 7A.2 MAST compile/preflight checks

MAST compile/preflight checks are a middle evidence class between text-only static checks and live Cosmos smoke.

When the local installed SBS Utils package exposes a usable preflight API, quick tests should run:

```text
tests/test_mast_compile_or_preflight.py
```

The current Slice 01A preflight loads the installed `artemis-sbs.sbs_utils.v1.3.0.sbslib`, registers SBS/GUI MAST nodes, points the MAST filesystem at the Khovan mission root, and compiles:

```text
story.mast
scripts/main.mast
scripts/systems/*.mast reached by imports
```

MAST compile/preflight can catch MAST syntax/import/compiler failures before live Cosmos. It cannot prove:

- runtime expression values
- bare-variable availability after task scheduling
- renderer/client-page behavior
- player ship assignment success
- GUI/page lifecycle in live Cosmos
- server/client playability

Therefore compile/preflight success is useful but not acceptance proof for BOOT, PLAYBOOT, admin UI, or gameplay criteria that require live runtime behavior.

## 7A.3 Runtime load-path checks

Runtime load-path checks verify that active startup files point only to allowed, existing, active runtime files. They should fail on:

- missing `.mast` files
- old archived MAST modules in active load paths
- external clone paths in active runtime files
- stale old-build module names such as `salvager_arrival.mast`

Runtime load-path checks are still static unless they are observed in live Cosmos.

## 7A.4 Route-smoke breadcrumb traces

Route-smoke traces are live troubleshooting evidence. They should be used when quick/static/preflight checks pass but live Cosmos still crashes, stalls, or gives no useful logs.

Use:

```text
tests/live_startup_trace.txt
```

as append-only crash breadcrumbs, and:

```text
tests/live_smoke_last_bootstrap.txt
```

as the last successful bootstrap audit.

If the trace stops at a marker, the next line or API call is the first suspect. If the trace does not update, the active startup path is earlier or different than assumed.

## 7A.5 Live Cosmos smoke

Live Cosmos smoke is the only evidence class that proves Cosmos/MAST runtime behavior. It is required for acceptance criteria involving:

- mission package load
- player ship visibility or assignment
- GUI/page lifecycle stability
- server/client console transition
- operator-visible mission state
- playable bridge/server state

Live failures outrank green quick tests. A green quick run plus a live runtime failure means the failure must be fixed, converted into a targeted regression when feasible, or documented as an exact blocker.

---

# 8. Required test artifacts

Create in the implementation project:

```text
/tests/test_matrix.md
/tests/story_jump_presets.md
/tests/golden_paths.md
/tests/pre_session_checklist.md
/tests/regression_log.md
/tests/known_issues.md
/tests/playtest_report_template.md
```

---

# 9. Bootstrap tests

```text
BOOT-001 mission package loads
BOOT-002 main.mast imports all required files
BOOT-003 story.json is valid
BOOT-004 script.py initializes without runtime error
BOOT-005 all mission state variables initialize
BOOT-006 Artemis starts with correct ship state
BOOT-007 Dillon Clip 1 queues or plays
BOOT-008 current_scene = 1
BOOT-009 mission_phase valid
BOOT-010 GM debug/admin overlay visible to GM
BOOT-011 player-facing debug controls hidden
BOOT-012 first scene proceeds without manual admin action
```

Acceptance:

```text
Fresh mission load reaches playable Scene 1 with no manual recovery.
```

A validation marker proves load path and lifecycle only. It is not, by itself, playable Scene 1.

---



# 9B. Minimum playable bootstrap tests

```text
PLAYBOOT-001 fresh load reaches playable Scene 1 without Resume Mission or manual recovery
PLAYBOOT-002 validation marker is not treated as playable Scene 1
PLAYBOOT-003 Artemis/player ship exists or exact API blocker is documented
PLAYBOOT-004 connected client can observe starting bridge/player state or exact blocker is documented
PLAYBOOT-005 Dillon Clip 1 queues, plays, or displays an operator-visible text/audio stub
PLAYBOOT-006 player-facing bootstrap text does not expose debug/admin controls
PLAYBOOT-007 Scenario Control Panel is not required for Slice 01A
PLAYBOOT-008 no Act I gates, Tarsis, drones, DAMCON, pirates, cache, debrief, or story jumps are active
PLAYBOOT-009 live smoke records server/client observations and marker-file evidence where available
PLAYBOOT-010 unresolved Cosmos/MAST API uncertainty is documented before Slice 02 proceeds
```

Acceptance:

```text
Fresh mission load reaches playable Scene 1 with no manual recovery, or the exact minimum-playable blocker is documented before Scenario Control Panel work proceeds.
```

---

# 9A. Act I v2.2 tests

```text
ACT1-001: mission starts with generator_governor_active = true
ACT1-002: Artemis starts with exactly 2 homing torpedoes
ACT1-003: departure is blocked until Comms requests clearance
ACT1-004: launch-envelope clear starts 10-second advisory timer
ACT1-005: Kestrel generator advisory appears in upper-left overlay
ACT1-006: Kestrel generator advisory echoes to Comms archive
ACT1-007: shakedown profile choice appears after advisory
ACT1-008: Tarsis docking blocked until homing priority requested
ACT1-009: Tarsis docking blocked until generator support requested
ACT1-010: Tarsis docking blocked until docking clearance requested/granted
ACT1-011: Tarsis resupply clears generator_governor_active
ACT1-012: Full Shakedown enters Engineering systems sequence
ACT1-013: Compressed Shakedown skips Engineering practice without failure flags
ACT1-014: Direct Scenario marks skipped Act I observations N/A
ACT1-015: DAMCON crew-quarters confirmation can route through Comms
ACT1-016: DAMCON mess confirmation can route through Comms
ACT1-017: controlled overload damage is detected or confirmable
ACT1-018: repair completion is detected or confirmable
ACT1-019: Drone 01 early fire triggers reset 5 km farther from beacon
ACT1-020: Drone 01 destruction triggers reset 5 km farther from beacon
ACT1-021: Drone 01 requires 1-2 km range band plus 15-second stationary hold
ACT1-022: Drone 01 Weapons array disables after three confirmed hits
ACT1-023: Drone 02 destruction advances to Act II transition
ACT1-024: cultural Comms packet appears and archives
```


# 10. Story-jump tests

Each story jump must have a validation test.

Standard procedure:

```text
1. Activate jump.
2. Verify current_scene.
3. Verify mission_phase.
4. Verify required variables.
5. Verify required entities exist or are queued.
6. Verify timers initialize correctly.
7. Verify GM overlay shows expected next event.
8. Trigger next expected event.
9. Verify no immediate errors or invalid state warnings.
```

Test IDs:

```text
JUMPTEST-001 through JUMPTEST-021 correspond to JUMP-001 through JUMP-021.
```

---

# 11. Drill tests

## 11.1 Drill Two

```text
D2-001 Dillon Clip 4 plays once
D2-002 Drone 01 spawns at correct range
D2-003 Drone 01 passive
D2-004 through D2-013 steps 1-10 advance correctly
D2-014 manual GM mark works for each step
D2-015 mechanical detection and manual mark do not double-advance
D2-016 fire before authorization sets safety flag
D2-017 Drone destroyed before objective blocks clean completion
D2-018 all hard flags required for clean completion
D2-019 Dillon Clip 5 plays once
D2-020 post_drill_2 checkpoint saves once
```

## 11.2 Drill Three

```text
D3-001 Dillon Clip 6 plays once
D3-002 Drone 02 spawns correctly
D3-003 simple evasion activates
D3-004 no step prompts fire after intro
D3-005 observation flags can be logged
D3-006 observation flags do not hard-block completion
D3-007 Engine subsystem disable required
D3-008 ceasefire confirmation required
D3-009 Engine disable without ceasefire does not complete unless explicitly implemented as late-ceasefire partial
D3-010 ceasefire without Engine disable does not complete
D3-011 overfire before Engine disable blocks clean completion
D3-012 help prompt logs a `qualification_event_log` entry and, if needed, adds a help/nudge marker to `act1_skipped_observations`
D3-013 Dillon Clip 7 plays once
D3-014 post_drill_3 checkpoint saves once
```

---

# 12. DAMCON tests

```text
DAMCON-001 cascade trigger starts timer
DAMCON-002 Engineer aboard Halcyon selects extended timer
DAMCON-003 Engineer returned selects compressed timer
DAMCON-004 timer state appears on GM overlay
DAMCON-005 timer persists across checkpoint
DAMCON-006 timer restores after reload
DAMCON-010 extended reports schedule every 180 seconds
DAMCON-011 compressed reports schedule every 90 seconds
DAMCON-012 first report fires at T+0
DAMCON-013 reports deliver to correct channel
DAMCON-014 reports use correct sequence
DAMCON-015 GM can hold report
DAMCON-016 GM can release held report
DAMCON-017 held report logs timing drift
DAMCON-018 drift does not alter outcome unless elapsed crosses threshold
DAMCON-020 extended clean survival resolves correctly
DAMCON-021 extended hypoxic survival resolves correctly
DAMCON-022 extended total loss resolves correctly
DAMCON-023 compressed clean survival resolves correctly
DAMCON-024 compressed hypoxic survival resolves correctly
DAMCON-025 compressed total loss resolves correctly
DAMCON-026 total loss is irreversible after threshold
DAMCON-027 total loss persists across reload
```

---

# 13. Pirate tests

```text
PIRATE-001 pirate arrival triggers
PIRATE-002 Cordial Reach spawns/queues
PIRATE-003 Bright Reckoning spawns/queues
PIRATE-004 pirate_cover_status = intact
PIRATE-005 GM display shows opening branch
PIRATE-006 combat_active = false
PIRATE-010 credentials probe can advance intact -> suspected
PIRATE-011 rescue law challenge can advance intact -> suspected
PIRATE-012 cultural protocol challenge can advance intact -> suspected
PIRATE-013 Science suspicious scan can advance intact -> suspected
PIRATE-014 captain explicit challenge can advance intact -> suspected
PIRATE-015 GM can hold intact despite weak probe
PIRATE-016 GM can advance suspicion after strong insight
PIRATE-020 second strong tell advances suspected -> exposed
PIRATE-021 unauthorized docking advances suspected -> exposed
PIRATE-022 unauthorized docking advances intact -> exposed
PIRATE-023 weapons activation advances exposed
PIRATE-024 refusal of TSN authority can expose
PIRATE-025 exposed state stops salvage-cover dialogue
PIRATE-030 backstop timer surfaces docking request option
PIRATE-031 GM can trigger docking request
PIRATE-032 GM can wait additional interval
PIRATE-033 docking denial sets docking_denied
PIRATE-034 unauthorized docking attempt fires after denial
PIRATE-035 Hessler warning available
PIRATE-040 force authorization starts combat after exposure
PIRATE-041 pirates can flee
PIRATE-042 pirates can surrender
PIRATE-043 pirates can be destroyed
PIRATE-044 pirates can board if enabled
PIRATE-045 combat resolution advances mission
PIRATE-046 pirate outcome persists into debrief
```

---

# 14. Cache tests

```text
CACHE-001 cache arrival sets cache_arrival = true
CACHE-002 cache options display correctly
CACHE-003 correct component sets correct
CACHE-004 military stabilizer sets incorrect_military
CACHE-005 regulator sets incorrect_regulator
CACHE-006 other wrong component sets incorrect_other
CACHE-007 wrong first attempt sets cache_retry_required
CACHE-008 retry path adds time/state consequence
CACHE-009 correct second attempt sets cache_retry_complete
CACHE-010 repair accepts correct component
CACHE-011 repair rejects wrong component
CACHE-012 cache error surfaces in Science debrief evidence
```

---

# 15. Checkpoint/reload tests

```text
SAVE-001 checkpoint after Drill One
SAVE-002 checkpoint after Drill Two
SAVE-003 checkpoint after Drill Three
SAVE-004 checkpoint after Anderson orders
SAVE-005 checkpoint after Halcyon arrival
SAVE-006 checkpoint after cascade
SAVE-007 checkpoint before pirate combat if feasible
SAVE-008 checkpoint at mission resolution
SAVE-010 reload restores mission_phase
SAVE-011 reload restores current_scene
SAVE-012 reload restores Artemis hull/energy/weapons
SAVE-013 reload restores required entities
SAVE-014 reload restores active timers
SAVE-015 reload restores GM overlay
SAVE-016 reload resumes expected next event
SAVE-020 reload does not resurrect DAMCON team
SAVE-021 reload does not undo Halcyon Drift loss
SAVE-022 reload does not restore converted torpedoes
SAVE-023 reload does not erase qualification observations
SAVE-024 reload does not erase visible pirate exposure
SAVE-030 deliberate ship destruction allows reload
SAVE-031 reload confirmation displays consequences
SAVE-032 mission resumes from checkpoint
SAVE-033 irreversible consequences remain
```

---

# 16. Admin tests

```text
ADMIN-001 GM panel visible only to GM
ADMIN-002 player consoles hide debug/admin controls
ADMIN-003 Test Mode exposes all story jumps
ADMIN-004 Live Mode hides destructive controls
ADMIN-005 hold scene transition works
ADMIN-006 release scene transition works
ADMIN-007 replay last clip works
ADMIN-008 trigger next DAMCON report works
ADMIN-009 delay next DAMCON report works
ADMIN-010 expose pirates works
ADMIN-011 force combat works
ADMIN-012 reset Drill Two works
ADMIN-013 reset Drill Three works
ADMIN-014 manual observation note works
ADMIN-015 manual mark does not corrupt automated state
ADMIN-016 destructive action requires confirmation
ADMIN-017 admin action log records action
```

---

# 17. Debrief tests

```text
DEBRIEF-001 mission resolution triggers debrief setup
DEBRIEF-002 Dillon Clip 10 opens debrief
DEBRIEF-003 station observations display by station
DEBRIEF-004 GM notes persist into debrief
DEBRIEF-005 GM can assign PASS/PARTIAL/NEEDS RETEST/N/A
DEBRIEF-006 runtime does not auto-grade final results
DEBRIEF-007 clean success summary works
DEBRIEF-008 DAMCON loss summary works
DEBRIEF-009 Halcyon Drift loss summary works
DEBRIEF-010 DAMCON total_loss triggers Dillon Clip 11 availability
DEBRIEF-011 Dillon Clip 12 closes debrief
DEBRIEF-012 optional Anderson closing clip can be triggered
```

---

# 18. Golden paths

## GOLD-001 clean qualification success

```text
Engineer stays aboard Halcyon.
Correct cache component first try.
Pirates exposed early or neutralized cleanly.
DAMCON survives clean.
Halcyon repaired.
```

Expected:

```text
damcon_outcome = clean_survival
halcyon_outcome = repaired
pirate_outcome resolved
debrief clean success variant available
```

## GOLD-002 compressed timer loss

```text
Engineer returns to Artemis.
Timer compressed.
Cache run consumes too much time.
DAMCON reaches T+15.
Halcyon repaired late.
```

Expected:

```text
damcon_outcome = total_loss
damcon_team_status = lost
Dillon Clip 11 available
reload does not undo deaths
```

## GOLD-003 wrong cache recovery

```text
Science selects wrong component first.
Retry required.
Second selection correct.
Timer worsens.
```

Expected:

```text
cache_retry_required = true
cache_retry_complete = true
Science debrief evidence includes wrong selection
DAMCON outcome reflects delay
```

## GOLD-004 pirate backstop

```text
Comms does not expose pirates.
Pirates request docking.
Docking denied.
Unauthorized docking attempt.
```

Expected:

```text
unauthorized_docking_attempt = true
pirate_cover_status = exposed
combat_active = true or imminent
Hessler warning available
```

## GOLD-005 ship destruction and reload

```text
Pirate combat destroys Artemis.
GM reloads checkpoint.
```

Expected:

```text
reload succeeds
mission resumes
irreversible consequences remain
qualification observations remain
```

## GOLD-006 Halcyon Drift loss

```text
Repair fails or is delayed beyond allowed path.
Halcyon Drift lost.
Survivors handled as designed.
```

Expected:

```text
halcyon_outcome = lost
debrief loss variant available
Anderson status variant available if used
mission still reaches debrief
```

---

# 19. Change-based regression gate

| Change type | Required tests |
|---|---|
| Bootstrap/file layout | BOOT + JUMPTEST-001 |
| State variable change | BOOT + affected JUMPTEST + SAVE smoke |
| Clip/audio trigger | BOOT + affected scene jump + replay test |
| Act I drill | BOOT + D2/D3 + SAVE-001/002/003 |
| DAMCON timer | BOOT + DAMCON + GOLD-001 or GOLD-002 |
| Pirate state | BOOT + PIRATE + GOLD-004 |
| Cache selection | BOOT + CACHE + GOLD-003 |
| Checkpoint/reload | BOOT + SAVE + GOLD-005 |
| GM/admin panel | BOOT + ADMIN + affected subsystem |
| Debrief/qualification | BOOT + DEBRIEF + one seeded outcome |
| Combat behavior | BOOT + PIRATE combat + GOLD-005 |
| Scene transition | BOOT + affected JUMPTEST + adjacent scene test |

---

# 20. Pre-session checklist

V2.1 Act I checks to include before live play:

```text
PRE-ACT1-001: fresh mission load shows generator-governor start state
PRE-ACT1-002: Kestrel departure clearance gate works
PRE-ACT1-003: post-departure generator advisory fires and archives
PRE-ACT1-004: Tarsis request gates block docking until complete
PRE-ACT1-005: direct scenario bypass marks skipped drills N/A
```


```text
PRE-001 fresh mission load reaches Scene 1
PRE-002 player-facing debug controls hidden
PRE-003 GM control panel visible
PRE-004 jump to Drill Two, verify clip/prompt/drone
PRE-005 jump to Anderson Orders, verify clip trigger
PRE-006 jump to cascade_decision, verify DAMCON timer start
PRE-007 jump to pirate_arrival_cover_intact, verify pirate state and GM branch display
PRE-008 jump to repair_resolution_clean, verify debrief opens
PRE-009 reload last checkpoint once
PRE-010 replay last clip once
PRE-011 verify audio assets available
PRE-012 verify Hessler voice-mode file ready
```

Ready to run if all checks pass or every failure has a documented workaround.

---

# 21. Defect severity

## Severity 1 — session blocker

Mission cannot load, Artemis cannot spawn, Scene 1 cannot begin, GM cannot recover, or player consoles unusable.

Must fix before live session.

## Severity 2 — major path blocker

Drill Two cannot complete, DAMCON timer does not start, pirates cannot expose, repair cannot resolve, or debrief cannot open.

Fix before live session unless workaround exists.

## Severity 3 — recoverable runtime issue

Clip replay needed, unexpected manual mark needed, display wrong but state valid, noncritical branch unavailable.

Can run with workaround.

## Severity 4 — polish / clarity

Wording, labels, optional clip routing, nonessential timing polish.

Fix when convenient.

---

# 22. Acceptance criteria

The admin/testing layer is acceptable when:

1. Developer can jump to any major story point without replaying prior scenes.
2. Each jump seeds a valid world state.
3. Live Mode hides destructive Test Mode tools.
4. Player consoles never show hidden admin/debug controls.
5. GM can recover common deadlocks in under one minute.
6. Admin actions are logged.
7. Regression tests can isolate major systems.
8. Pre-session readiness can be verified quickly.


---

# 19. v2.3 prior-MAST lesson tests

These tests convert old implementation lessons into explicit acceptance checks.

## 19.1 Message router tests

MSG-001: Training message routes through central message router.

MSG-002: Training message appears in upper-left lifeform overlay or closest supported display.

MSG-003: Training message echoes once into Comms archive.

MSG-004: Character/instructor messages and current-objective messages do not overwrite each other's state.

MSG-005: Story jump invalidates stale delayed message sequences.

## 19.2 Current objective display tests

OBJ-001: Set current objective and verify it appears to relevant player GUIs.

OBJ-002: Current objective echoes once into Comms archive.

OBJ-003: Current objective remains visible for at least 60 seconds or until replaced.

OBJ-004: Replacing objective suppresses or supersedes the old objective.

OBJ-005: Heartbeat fallback does not spam Comms archive.

OBJ-006: Story jump invalidates old objective run ID and prevents stale objective from reappearing.

OBJ-007: Ordinary Dillon/Anderson/training prompt does not permanently erase current objective.

OBJ-008: GM panel shows objective debug state; player consoles do not.

OBJ-009: Clear objective removes or suppresses the display.

OBJ-010: If true static display is not supported, fallback mode is documented.

## 19.3 Story-jump safety tests

JUMP-SAFE-001: Every story jump runs cleanup before seeding new state.

JUMP-SAFE-002: Old Drill Two/Three drone objects are removed or invalidated before new targets spawn.

JUMP-SAFE-003: Old nav proxies are removed or invalidated.

JUMP-SAFE-004: Old delayed messages do not fire after jump.

JUMP-SAFE-005: Old evasion loops do not continue after jump.

JUMP-SAFE-006: Jump summary displays jump_id, target scene, seeded state, and next expected action.

## 19.4 Kestrel/Tarsis route stability tests

KT-001: Kestrel departure Comms route appears at mission start.

KT-002: Departure clearance sets the correct state and releases the ship.

KT-003: Kestrel generator packet fires after launch-envelope exit plus 10 seconds.

KT-004: Tarsis Comms route appears after transit.

KT-005: Tarsis docking requires homing priority request, generator support request, and docking clearance.

KT-006: Adding drone target logic does not remove or corrupt Kestrel/Tarsis Comms routes.

## 19.5 Drone target spike tests

DRONE-SPIKE-001: Candidate target spawns reliably.

DRONE-SPIKE-002: Science scan works without debug clutter.

DRONE-SPIKE-003: Comms route remains stable.

DRONE-SPIKE-004: Weapons can select the target.

DRONE-SPIKE-005: Manual subsystem targeting can be set.

DRONE-SPIKE-006: Subsystem damage/disable is detectable or can be simulated reliably.

DRONE-SPIKE-007: Destruction/overfire is detectable.

DRONE-SPIKE-008: No unwanted surrender/taunt menu appears during training.

DRONE-SPIKE-009: Weak-frequency relay is observational only until baseline subsystem damage is reliable.

## 19.6 Build-start gate

Do not begin the full Act I stationary-drone drill until:

- MSG tests pass or fallback is documented
- OBJ spike reaches true-static or heartbeat fallback decision
- JUMP-SAFE tests pass
- KT route stability tests pass
- DRONE-SPIKE tests pass or a documented fallback gate is approved


---

# 23. Branch lifecycle evidence

Branch lifecycle checks are workflow evidence, not mission runtime tests.

For implementation and live-smoke work, the verification record should include:

```text
starting branch:
ending branch:
branch type:
tests run:
merge-back performed:
runtime/live-smoke branch confirmed:
remaining uncommitted changes:
next safe action:
```

A live-smoke result is not accepted as final runtime evidence when it was accidentally run from a docs-only, governance, or architecture-feedback branch unless the branch state and merge state are explicitly reviewed and accepted.

# 24. Branch lifecycle acceptance checks

```text
BRANCH-001 Branch opening report includes current branch, branch type, task purpose, expected return branch, and runtime/live-smoke allowance.
BRANCH-002 Branch transition report includes quick-test result, git status, and diff stat before switching.
BRANCH-003 Docs/governance branch closing confirms no mission code changed unintentionally.
BRANCH-004 Docs/governance branch merge-back is performed intentionally into the active implementation branch.
BRANCH-005 Quick tests are rerun after merge-back before implementation resumes.
BRANCH-006 Return-to-work check blocks live-smoke or Cosmos testing from docs/governance or architecture-feedback branches.
BRANCH-007 Completion report includes starting branch, ending branch, commits, merge status, tests, changed files, uncommitted changes, and next safe action.
```

---

# 25. Operator test expectation evidence

Operator test expectation checks are workflow evidence, not mission runtime tests.

When implementation, live-smoke, UI/manual, generated-artifact, branch, documentation-review, or negative-control work requires the human operator to verify something, the handoff must include:

```text
What changed:
What to run or do:
Expected observation:
Failure/ambiguous observation:
What remains unproven:
Next action by result:
```

Manual or live tests must always include `Expected observation` and `Failure/ambiguous observation`.

For Khovan live game smoke, expected observations should name the visible or logged Khovan-specific marker and any runtime state that proves the intended route ran. Example:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
mission_phase=act_1
current_scene=1
```

Failure or ambiguous observations include:

```text
blank screen with no marker
empty mast.runtime.log or mast.compile.log when a marker was expected
default server screen appears but no Khovan marker appears
no error appears but there is also no proof the Khovan route ran
quick tests pass but live Cosmos acceptance is still required
```

Negative-control tests must identify which failure is expected. If a deliberate broken import is supposed to make quick tests fail, then the quick-test failure is the expected observation for that phase. The restored phase should return the quick suite to passing.

# 25A. Route-smoke breadcrumb trace pattern

Route-smoke breadcrumb traces are live-smoke troubleshooting evidence, not gameplay tests and not a substitute for acceptance.

Use an append-only route trace when quick/static/preflight checks pass but live Cosmos crashes or provides no useful log output. This is especially important when `mast.runtime.log`, `mast.compile.log`, or the last-success marker file are empty, stale, or ambiguous.

Recommended evidence split:

```text
tests/live_smoke_last_bootstrap.txt = last successful bootstrap audit
tests/live_startup_trace.txt = append-only crash breadcrumb trace
```

Route-smoke traces should bracket the active entry chain and risky runtime boundaries, for example:

```text
[KHOVAN EARLY 001] script.py entered
[KHOVAN EARLY 002] before sbs_utils import
[KHOVAN EARLY 003] after sbs_utils import
[KHOVAN EARLY 006] before story.mast load/handoff
[KHOVAN BOOT 001] scripts/main.mast entered
[KHOVAN BOOT 002] before state defaults
[KHOVAN BOOT 003] after state defaults
[KHOVAN BOOT 004] before a risky subsystem
[KHOVAN BOOT 005] risky subsystem entered
[KHOVAN BOOT 006] before a risky API call
```

Acceptance interpretation:

```text
trace absent = active startup path is earlier/different than assumed, or trace write path failed
trace stops at marker = next startup line/API call is the first suspect
last-success audit stale = previous success only; not proof for the current live run
quick green + live crash = live crash outranks quick green
```

Quick tests may verify that route-smoke marker strings exist in active startup files and that trace artifacts are ignored. Quick tests must not claim the route-smoke trace proves live Cosmos behavior unless the live run actually produced the trace.

# 26. Operator test expectation acceptance checks

```text
OTE-001 Manual/live test requests include an Expected observation block.
OTE-002 Manual/live test requests include a Failure/ambiguous observation block.
OTE-003 Artifact-changing responses identify what changed and whether the change is documentation-only/no-op/runtime-affecting.
OTE-004 Test instructions include exact command, UI action, app launch, or manual check plus branch/location assumptions.
OTE-005 The response states what remains unproven, especially static-vs-live and smoke-vs-full-feature gaps.
OTE-006 The response gives next action by result: success, failure, ambiguous.
OTE-007 Negative-control tests clearly state when an expected failure means the control passed.
OTE-008 Completion reports do not claim live/runtime success from static tests.
OTE-009 If a result has no error but also no marker/log/UI/file/runtime evidence, the assistant classifies it as ambiguous rather than success.
```
