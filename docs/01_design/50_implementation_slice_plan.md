# KHOVAN REACH — IMPLEMENTATION SLICE PLAN
*Coding-project slicing plan based on merged architecture docs.*

Version: 1.5 repo-consolidated branch-lifecycle + operator-test-expectation update
Status: Canonical implementation planning aid  
Pair with: docs/01_design/10_mast_requirements.md, docs/01_design/40_admin_testing_plan.md, docs/01_design/00_scenario_play_guide.md

---

# 1. Purpose

This document divides Khovan Reach implementation into manageable build slices.

Each slice should produce:
- runnable code
- a specific testable capability
- a clear acceptance gate
- limited context requirements for coding assistants

Use this to keep the implementation project focused.

---

# 2. Slice packet template

Each slice packet should include:

```text
Slice ID:
Goal:
Source docs:
Files to modify:
Runtime owner model:
State variables needed:
Branch type:
Starting branch:
Expected return branch:
Branch lifecycle plan:
Runtime/live-smoke allowed from this branch:
Merge-back required:
Implementation tasks:
Tests required:
Acceptance criteria:
Expected observations:
Failure/ambiguous observations:
What remains unproven:
Next action by result:
Known risks:
Do not implement:
```

---

# 3. Build slices

## Slice 00 — Repo setup and old-build lesson transfer

Goal:
- Prepare a clean implementation workspace before mission feature coding.

Inputs:
- docs/04_implementation_setup/00_transfer_from_old_build.md
- docs/04_implementation_setup/10_mast_file_lessons.md
- docs/04_implementation_setup/20_current_objective_display_spike.md
- docs/00_project/10_repo_structure.md
- docs/00_project/20_build_start_checklist.md

Build:
- place active docs in the repo structure
- keep old implementation files out of active source
- verify test harness starts
- capture old-build lessons
- confirm current source authority
- no mission feature coding

Tests:
- repository structure check
- quick test command check if test harness exists
- source-authority checklist

Acceptance:
- repo has one active source copy of each document
- old MAST files are archived externally or treated as history only
- implementation prompt and transfer notes are available
- no feature code has been started


## Slice 01 — Mission shell and load proof

Goal:
- Mission package loads, active Khovan route executes, mission state initializes, and live smoke proves the bootstrap path reaches the Scene 1 validation marker.

Inputs:
- `docs/01_design/10_mast_requirements.md` Sections 4-6
- Dillon Clip 1

Build:
- mission file layout
- `main.mast`
- state initialization
- audio wrapper stub
- GM overlay stub
- runtime load-path and GUI lifecycle guards

Tests:
- BOOT-001 through BOOT-012

Acceptance:
- Quick/static checks pass.
- Active runtime load-path checks pass where implemented.
- Live Cosmos mission load reaches the Khovan Slice 01 validation marker without manual recovery.
- The validation marker is load proof only; it is not a playable Scene 1 start.
- If live Cosmos still fails, the checkpoint must be explicitly labeled as a blocker/investigation checkpoint, not as completed Slice 01.

---

## Slice 01A — Minimum playable bootstrap

Goal:
- Convert Slice 01 load proof into the minimum playable Scene 1 bootstrap before Scenario Control Panel work proceeds.

Inputs:
- `docs/01_design/10_mast_requirements.md`, Mission bootstrap and Minimum playable bootstrap
- `docs/01_design/40_admin_testing_plan.md`, BOOT and PLAYBOOT tests
- `docs/02_content/40_dillon_clips.md`, Clip 1
- local Tier 2 references for player-ship, console, clip, and GUI syntax only

Build:
- reference-backed Artemis/player ship creation or explicit runtime confirmation
- minimum client/server path needed for players to connect to the starting bridge state
- operator-visible Dillon Clip 1 text/audio stub
- Scene 1 status that confirms which bootstrap objects and stubs are active
- preservation of the Slice 01 load marker and lifecycle safety

Tests:
- BOOT-001 through BOOT-012
- PLAYBOOT-001 through PLAYBOOT-010

Acceptance:
- Quick/static checks pass.
- Fresh live Cosmos load reaches playable Scene 1 with no manual recovery.
- A connected client can observe the minimum starting bridge/player-ship state, or an exact API blocker is documented.
- Dillon Clip 1 is queued, played, or represented by an operator-visible text/audio stub.
- BOOT-006 is either implemented with reference-backed syntax or explicitly blocked with the exact player-ship/API uncertainty.
- The validation marker alone is not sufficient acceptance for Slice 01A.

Do not implement:
- Scenario Control Panel
- story jumps
- Kestrel departure clearance gate
- Tarsis gates
- generator advisory timers
- shakedown profile selection
- drones
- DAMCON
- pirates/salvagers
- cache run
- debrief
- current-objective display

---

## Slice 02 — Scenario Control Panel foundation

Goal:
- GM-only panel exists with mission overview, mode separation, and basic controls.

Precondition:
- Slice 01A minimum playable bootstrap has passed live smoke, or its remaining runtime-world blocker is explicitly documented and approved before control-panel work proceeds.

Inputs:
- `docs/01_design/40_admin_testing_plan.md` Sections 2-6

Build:
- GM-only panel
- Test Mode / Live Mode flagging
- mission overview display
- hold/release control
- action log

Tests:
- ADMIN-001 through ADMIN-006

Acceptance:
- GM can see state; players cannot see debug/admin controls.

---

## Slice 03 — Story-jump preset framework

Goal:
- Jump presets can seed valid state.

Inputs:
- Admin/testing plan story-jump contract

Build:
- preset registry
- jump executor
- validation display
- initial presets: mission_start, drill_2_guided_contact, anderson_orders, cascade_decision, pirate_arrival_cover_intact, debrief

Tests:
- JUMPTEST for implemented presets

Acceptance:
- Developer can jump to core scenes without playing from start.

---



## Slice 03A — Current objective display spike

Goal:
- Determine whether persistent left/mid-screen current-goal text is feasible.

Inputs:
- docs/04_implementation_setup/20_current_objective_display_spike.md
- docs/01_design/10_mast_requirements.md message routing requirements
- old MAST text prompt lessons from docs/04_implementation_setup/10_mast_file_lessons.md

Build:
- current objective state variables
- objective set / clear / refresh routines
- Comms archive echo once per objective change
- true static display test if Cosmos/MAST supports it
- managed heartbeat fallback if true static display is not supported
- run_id guard for heartbeat refresh

Tests:
- objective appears
- objective persists or refreshes
- objective echoes once into Comms archive
- objective replacement works
- story jump invalidates stale objective
- ordinary prompt traffic does not permanently erase current objective

Acceptance:
- current objective display has a proven implementation path or a documented fallback
- no Comms archive spam
- no stale objectives after story jumps

## Slice 04 — Act I generator-governor start and Tarsis gate

Inputs:
- `docs/01_design/00_scenario_play_guide.md`, Act I Scenes 1-2
- `docs/01_design/10_mast_requirements.md`, Act I implementation
- `docs/02_content/40_dillon_clips.md`, Clip 1 and text-message triggers
- `docs/01_design/40_admin_testing_plan.md`, ACT1-001 through ACT1-011

Build:
- mission start with generator governor active
- 2 homing torpedoes issued
- Kestrel departure clearance gate
- launch-envelope detection
- 10-second generator advisory
- overlay + Comms archive message routing
- shakedown profile selection
- Tarsis homing priority / generator support / docking clearance gates
- generator governor cleared on Tarsis resupply

Acceptance:
- ACT1-001 through ACT1-011 pass
- Direct Scenario path can reach Act II after resupply

---

## Slice 05 — Full Shakedown Engineering systems sequence

Inputs:
- `docs/01_design/00_scenario_play_guide.md`, Scene 3A
- `docs/01_design/10_mast_requirements.md`, Engineering shakedown gates
- `docs/01_design/20_gm_operational_notes.md`, DAMCON fallback guidance
- `docs/01_design/40_admin_testing_plan.md`, ACT1-012 through ACT1-018

Build:
- impulse zero / warp 200 instruction and validation
- full impulse no-motion validation
- DAMCON crew-quarters confirmation through Comms
- DAMCON mess confirmation through Comms
- controlled 300% impulse/warp overload
- damage detection or confirmation fallback
- repair supervision and completion gate
- navigation priority preset gate

Acceptance:
- ACT1-012 and ACT1-015 through ACT1-018 pass
- Compressed and Direct modes skip these gates cleanly

---

## Slice 06 — Drone 01 controlled disable and Drone 02 live fire


Precondition:
- Run the target subsystem-damage spike before building the full Drone 01/02 sequence.
- Do not assume a normal enemy ship solves subsystem targeting.
- Verify Science scan, Comms route stability, Weapons selection, subsystem hit detection, disable detection, destruction/overfire reset, and absence of unwanted surrender/taunt menus.


Inputs:
- `docs/01_design/00_scenario_play_guide.md`, Scenes 4A-6A
- `docs/01_design/10_mast_requirements.md`, Drone 01/Drone 02 implementation
- `docs/01_design/30_qualification_cards.md`, Act I scoring rule
- `docs/01_design/40_admin_testing_plan.md`, ACT1-019 through ACT1-024

Build:
- Drone 01 non-attacking enemy object
- Science scan gate
- Comms hail gate
- weak shield frequency relay gate
- Weapons beam lock gate
- 1-2 km range band gate
- 15-second stationary hold gate
- fire authorization gate
- three-hit Weapons-array disable gate
- early-fire reset
- destruction reset
- Drone 02 live-fire target spawn at 10 km
- Drone 02 destruction gate
- cultural Comms packet

Acceptance:
- ACT1-019 through ACT1-024 pass
- Full and Compressed shakedown paths both work
- Direct Scenario bypass does not set drill failure states

---

## Slice 07 — Act II pivot and Halcyon arrival

Goal:
- Anderson order, distress localization, Halcyon arrival, and Engineering deployment work.

Inputs:
- Pass 1 Scenes 5-8
- Anderson Clip 1
- Dillon Clip 8
- Hessler file

Build:
- Act II scene transitions
- distress signal state
- Halcyon spawn/scan/hail
- Engineering deployment flag
- DAMCON deployment state
- `post_anderson_orders` and `post_halcyon_arrival` checkpoints

Tests:
- JUMPTEST-005 through JUMPTEST-008
- SAVE-004/005

Acceptance:
- Mission pivots cleanly from drill to live operation.

---

## Slice 08 — Away mission wrapper and cascade

Goal:
- Hessler scene is bounded by runtime beat tracker and cascade trigger.

Inputs:
- Hessler operating file
- Pass 1 Scene 9

Build:
- away mission beat tracker
- convergence flag
- cascade trigger
- bridge report state
- `post_cascade` checkpoint

Tests:
- JUMPTEST-008/009
- SAVE-006

Acceptance:
- GM can run Hessler scene without losing runtime structure.

---

## Slice 09 — DAMCON timer

Goal:
- Timer, reports, holds, outcomes, and persistence work.

Inputs:
- DAMCON reports
- MAST v2 DAMCON section
- Admin/testing DAMCON tests

Build:
- extended/compressed timer
- report scheduler
- hold/release
- outcome calculator
- irreversible loss flag

Tests:
- DAMCON-001 through DAMCON-027
- GOLD-001/GOLD-002

Acceptance:
- DAMCON pressure is automatic, pace-adjustable, and irreversible at threshold.

---

## Slice 10 — Cache run and component selection

Goal:
- Cache arrival, component selection, wrong-part retry, and Science evidence work.

Inputs:
- Pass 1 Scene 13
- MAST v2 cache section

Build:
- cache arrival state
- inventory UI/prompt
- selection result
- retry required state
- timer consequence marker

Tests:
- CACHE-001 through CACHE-012
- GOLD-003

Acceptance:
- Wrong component is recoverable but costly.

---

## Slice 11 — Pirate state machine

Goal:
- Pirate arrival, state tracking, branch suggestions, and backstop path work.

Inputs:
- Pirate dialogue
- MAST v2 pirate section
- Admin/testing pirate tests

Build:
- pirate arrival timer
- pirate state variables
- suggested dialogue branch display
- suspected/exposed transitions
- docking backstop
- GM controls

Tests:
- PIRATE-001 through PIRATE-035
- GOLD-004

Acceptance:
- Scene 12 is flexible but tracked.

---

## Slice 12 — Combat transition and pirate outcomes

Goal:
- Exposed pirates can flee, surrender, fight, be destroyed, or board if enabled.

Inputs:
- Pirate dialogue exposed/combat branches
- MAST v2 pirate outcome section

Build:
- force authorization gate
- hostile state
- combat resolution hooks
- outcome persistence
- `pre_pirate_combat` checkpoint if feasible

Tests:
- PIRATE-040 through PIRATE-046
- GOLD-005

Acceptance:
- Combat starts and resolves without breaking mission continuation.

---

## Slice 13 — Repair resolution

Goal:
- Halcyon repair, DAMCON outcome, pirate outcome, and mission outcome resolve.

Inputs:
- Pass 1 Scene 14
- DAMCON outcome rules

Build:
- repair completion
- Halcyon outcome
- DAMCON final status
- mission_resolution_ready
- `mission_resolution` checkpoint

Tests:
- JUMPTEST-017/018/019/020
- GOLD-001/002/006

Acceptance:
- All major outcome variants reach return/debrief.

---

## Slice 14 — Debrief support

Goal:
- Debrief clips and runtime evidence display support GM assessment.

Inputs:
- Qualification cards
- Debrief script
- Dillon Clips 10-12
- Anderson optional closing

Build:
- debrief support view
- observation evidence by station
- GM rating entry
- clip triggers
- outcome summary display

Tests:
- DEBRIEF-001 through DEBRIEF-012

Acceptance:
- GM can deliver debrief without runtime auto-grading.

---

## Slice 15 — Checkpoint/reload hardening

Goal:
- Reload works under catastrophic failure and preserves irreversible consequences.

Inputs:
- MAST v2 checkpoint section
- Admin/testing SAVE tests

Build:
- checkpoint save payloads
- reload confirmation
- irreversible state preservation
- deliberate ship destruction test

Tests:
- SAVE-001 through SAVE-033
- GOLD-005

Acceptance:
- Reload is reliable and not a tactical undo.

---

## Slice 16 — Regression harness and pre-session workflow

Goal:
- Testing becomes routine and lightweight.

Inputs:
- Admin/testing plan

Build:
- test matrix files
- regression log template
- known issues template
- pre-session checklist file
- automated or semi-automated smoke scripts where feasible

Tests:
- PRE-001 through PRE-012

Acceptance:
- GM/developer can validate session readiness in minutes.

---

# 4. Slice discipline

For each slice:

- Do not implement future mechanics unless required by the slice.
- Add placeholders/stubs only when clearly labeled.
- Run slice acceptance tests before proceeding.
- Log bugs and implementation decisions.
- If implementation reveals design conflict, route it back to architecture rather than silently mutating design.

---


## Branch lifecycle discipline

Each implementation slice must declare its branch type and expected return branch.

Use these branch types:

- implementation
- docs/governance
- architecture feedback
- spike/experiment
- emergency fix

Before starting a slice, confirm:

```text
git status --short --branch
git log --oneline -5
```

Before switching branches or closing the slice branch, run:

```text
python run_tests.py quick
git status --short --branch
git diff --stat
```

If a docs/governance or architecture-feedback branch is created during a slice, merge it intentionally back into the active implementation branch before runtime work resumes.

Before live-smoke prompts or Cosmos tests, confirm the current branch is the intended implementation branch and contains the latest merged docs/governance updates.

Completion or checkpoint reporting must include:

```text
Starting branch:
Ending branch:
Branch type:
Commits created:
Merge performed:
Tests run:
Files changed:
Remaining uncommitted changes:
Next safe branch/action:
```

---

## Operator test expectation discipline

Each implementation slice must make its acceptance gate operator-readable.

When a slice asks the human operator to run quick tests, live Cosmos smoke, a UI check, a generated-artifact review, a branch workflow check, a documentation review, or a negative-control test, the slice packet or handoff must include:

```text
What changed:
What to run or do:
Expected observation:
Failure/ambiguous observation:
What remains unproven:
Next action by result:
```

Manual or live tests must always include `Expected observation` and `Failure/ambiguous observation`.

Static quick checks should not be described as proving live Cosmos behavior. A smoke marker should not be described as proving full feature behavior. Negative-control tests must state when an expected failure means the control passed.

---

# 5. Recommended first implementation order

Minimum viable playable vertical path:

```text
1. Slice 01 - Mission shell and load proof
2. Slice 01A - Minimum playable bootstrap
3. Slice 02 - Control Panel foundation
4. Slice 03 - Story jumps
5. Slice 04 - Drill One
6. Slice 05 - Drill Two
7. Slice 06 - Drill Three
8. Slice 07 - Act II / Halcyon arrival
9. Slice 08 - Away wrapper / cascade
10. Slice 09 - DAMCON timer
11. Slice 10 - Cache run
12. Slice 11 - Pirate state machine
13. Slice 13 - Repair resolution
14. Slice 14 - Debrief
15. Slice 15 - Reload hardening
16. Slice 16 - Regression harness
```

Slice 12 combat can be stubbed if necessary for an early noncombat test, but must be complete before live player run.
