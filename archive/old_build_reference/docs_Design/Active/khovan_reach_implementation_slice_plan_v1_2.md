# KHOVAN REACH — IMPLEMENTATION SLICE PLAN v1.2
*Coding-project slicing plan based on merged architecture docs.*

Status: Canonical implementation planning aid  
Pair with: `03_mast_requirements_v2_2_merged.md`, `khovan_reach_admin_testing_plan_v2_2_merged.md`, `khovan_reach_pass1_v2_2_merged.md`

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
Implementation tasks:
Tests required:
Acceptance criteria:
Known risks:
Do not implement:
```

---

# 3. Build slices

## Slice 01 — Mission shell and bootstrap

Goal:
- Mission loads, initializes state, plays opening clip, reaches Scene 1.

Inputs:
- `03_mast_requirements_v2_2_merged.md` Sections 4-6
- Dillon Clip 1

Build:
- mission file layout
- `main.mast`
- state initialization
- audio wrapper stub
- GM overlay stub

Tests:
- BOOT-001 through BOOT-012

Acceptance:
- Fresh mission load reaches Scene 1 without manual recovery.

---

## Slice 02 — Scenario Control Panel foundation

Goal:
- GM-only panel exists with mission overview, mode separation, and basic controls.

Inputs:
- `khovan_reach_admin_testing_plan_v2_2_merged.md` Sections 2-6

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


## Slice 04 — Act I generator-governor start and Tarsis gate

Inputs:
- `khovan_reach_pass1_v2_1_merged.md`, Act I Scenes 1-2
- `03_mast_requirements_v2_1_merged.md`, Act I implementation
- `05_dillon_clips_v2_1_merged.md`, Clip 1 and text-message triggers
- `khovan_reach_admin_testing_plan_v2_1_merged.md`, ACT1-001 through ACT1-011

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
- `khovan_reach_pass1_v2_1_merged.md`, Scene 3A
- `03_mast_requirements_v2_1_merged.md`, Engineering shakedown gates
- `02_gm_operational_notes_v2_1_merged.md`, DAMCON fallback guidance
- `khovan_reach_admin_testing_plan_v2_1_merged.md`, ACT1-012 through ACT1-018

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

Inputs:
- `khovan_reach_pass1_v2_1_merged.md`, Scenes 4A-6A
- `03_mast_requirements_v2_1_merged.md`, Drone 01/Drone 02 implementation
- `01_qualification_cards_v2_1_merged.md`, Act I scoring rule
- `khovan_reach_admin_testing_plan_v2_1_merged.md`, ACT1-019 through ACT1-024

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

# 5. Recommended first implementation order

Minimum viable playable vertical path:

```text
1. Slice 01 — Mission shell
2. Slice 02 — Control Panel foundation
3. Slice 03 — Story jumps
4. Slice 04 — Drill One
5. Slice 05 — Drill Two
6. Slice 06 — Drill Three
7. Slice 07 — Act II / Halcyon arrival
8. Slice 08 — Away wrapper / cascade
9. Slice 09 — DAMCON timer
10. Slice 10 — Cache run
11. Slice 11 — Pirate state machine
12. Slice 13 — Repair resolution
13. Slice 14 — Debrief
14. Slice 15 — Reload hardening
15. Slice 16 — Regression harness
```

Slice 12 combat can be stubbed if necessary for an early noncombat test, but must be complete before live player run.
