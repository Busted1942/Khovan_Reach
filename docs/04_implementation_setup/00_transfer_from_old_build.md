# KHOVAN REACH — TRANSFER FROM OLD BUILD

Version: 1.1
Status: Implementation-history transfer note
Purpose: Preserve useful lessons from the previous vibe-coding attempt and reviewed MAST files without treating old code or old docs as current architecture authority.

---

# 1. Decision

Start implementation over from the current v2.2 architecture bundle.

Do not start over ignorant.

Carry forward proven implementation patterns, test workflow lessons, and known failure warnings from:

- current_ai_handoff.md
- playtest_notes.md
- Recovery Notes.txt
- TESTING.md
- old MAST files

Do not carry forward superseded design authority, tangled Drill Two experiments, or old assumptions that conflict with v2.2.

---

# 2. Preserve These Concepts

## 2.1 Real Cosmos mission path

The previous implementation confirmed that the mission should live directly in the real Cosmos mission directory:

- C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach

Do not return to the old junction workflow unless the VS Code / MAST extension behavior has been proven fixed.

---

## 2.2 Known-good baseline primitives

Before rebuilding complex Act I logic, reproduce the baseline primitives that previously worked:

- Artemis spawns.
- Kestrel Yards exists as departure/origin context.
- Tarsis Station appears.
- Tarsis can be hailed.
- Tarsis grants docking clearance.
- Drill One can complete from Tarsis docking clearance plus successful docking.
- Science scan path worked.
- Comms hail path worked.
- Weapons target-selection detection had a known-good pattern.
- Drill Three could transition to Anderson Orders.

---

## 2.3 Scenario Control Panel from old dev jump harness

The old dev_jump.mast had a strong GM-only jump pattern.

Preserve:

- GM-only Comms route
- curated anchors
- jump summary message
- return to jump menu after action
- seeded state notes
- next expected action display

Rename/evolve into:

- Scenario Control Panel
- Test Mode Story Jumps
- Live GM Recovery Mode

Do not copy the old dev UI as the production control panel unchanged.

---

## 2.4 Neutral helper modules

The old act_1_state_helpers.mast is the correct architectural pattern.

Preserve:

- cleanup helpers
- resupply helpers
- drone spawn helpers
- step state seeding
- target selection setup
- helper reuse by dev jumps and future checkpoint restore

Do not let dev/admin UI own production restore logic.

---

## 2.5 Production checkpoint separation

The old state_save.mast correctly remained separate from dev jumps.

Fresh distinction:

- Test Mode story jumps: free jump and seed state for development.
- Live GM Recovery: safe recovery tools only.
- Production checkpoint/reload: no tactical rewind and no undoing committed consequences.

---

## 2.6 Run ID / generation ID stale-task protection

Carry forward the run ID idea.

Any scheduled or delayed task that can survive a story jump needs a run_id or generation_id guard.

Use this for:

- Kestrel generator packet after launch-envelope exit plus 10 seconds
- training message sequences
- current-objective display heartbeat
- Drill Two 15-second ready hold
- Drill Three evasion loop
- DAMCON report queue
- pirate arrival timer
- pirate docking backstop timer
- delayed scene transitions

---

## 2.7 Text prompting pattern

The old MAST files had working text wrappers using GUI info-panel messages.

Preserve the concept, but refactor it.

Fresh rule:

- all training text should pass through a central message router
- training text should appear in the upper-left lifeform overlay or closest current supported UI
- training text should echo to the Comms archive
- current objective should be a separate persistent display system or heartbeat fallback
- direct scene files should not scatter raw gui_info_panel_send_message calls everywhere

---

## 2.8 Current-objective display is unfinished work

The old text prompting worked for timed messages.

The unfinished piece was static current drill goal text on the left/mid-screen.

Fresh implementation should treat this as a named spike:

- Current Objective Display Spike

Do not let it block Slice 1 skeleton.

Do complete it before full Act I drill implementation if possible.

Fallback if true static display is not supported:

- timed overlay plus Comms archive
- managed heartbeat refresh of current objective
- no repeated Comms archive spam

---

## 2.9 Automatic gate patterns

Carry forward automatic gate examples from the old files:

- Helm transit monitor using distance, vector, throttle, and speed.
- Ready posture using distance band and Weapons lock.
- 15-second hold using delayed task and run ID.
- damage/object event hooks.
- damage/destroy reset hooks.
- get_weapons_selection checks.
- Science/Comms/Weapons selection seeding.

These patterns support the current v2.2 rule:

- automatic gates first
- Comms/captain confirmation second
- GM marks last

---

# 3. Do Not Preserve These

## 3.1 Old design authority order

Do not use the old authority order.

Current authority is v2.2 architecture and handoff docs.

Old code is implementation evidence only.

---

## 3.2 Old launch assumptions

Do not preserve old start values such as:

- 70 percent energy start
- 0 homing torpedoes as current canon
- old fixed qualification-cruise-only opening

Current v2.2 start:

- generator-output governor active
- 2 homing torpedoes issued
- Kestrel generator issue packet after launch-envelope exit plus 10 seconds
- Full Shakedown / Compressed Shakedown / Direct Scenario fork

---

## 3.3 GM-confirmed checks as default

Do not preserve old GM-confirmed checks as the default where runtime detection is available.

Use:

- automatic detection where possible
- Comms/captain confirmation when mechanically invisible
- GM manual marks only as fallback

---

## 3.4 Tangled Drill Two branch

Do not carry forward the failed target/weak-frequency branch.

Known problems:

- Kestrel/Tarsis Comms options disappeared.
- Regular-hostile target behavior introduced confusing side/name/skin behavior.
- Surrender/taunt options appeared unexpectedly.
- Subsystem damage was not predictable enough.
- Weak-frequency relay gating stalled damage.
- Science UI became crowded.
- Dev-jump objectives could go stale.

---

## 3.5 Weak-frequency relay as hard gate

Science relaying weak shield frequencies is useful training.

It should not become a hard gate until subsystem damage behavior is proven reliable.

Treat as:

- training evidence
- Comms archive message
- optional coaching cue

Not as:

- required damage gate
- blocker before subsystem disable

---

## 3.6 Regular enemy target substitution without proof

Do not assume a normal enemy ship solves the training target problem.

Run a target spike first.

---

# 4. Required Pre-Implementation Spikes

DRONE-SPIKE-001:
- verify target candidate supports subsystem damage events
- verify destruction/overfire detection
- verify no unwanted surrender/taunt menu

UI-SPIKE-001:
- verify player-facing debug controls can be hidden

MSG-SPIKE-001:
- verify upper-left lifeform overlay and Comms archive echo

OBJ-SPIKE-001:
- verify persistent current-objective display or heartbeat fallback

JUMP-SPIKE-001:
- verify story-jump cleanup cancels stale scheduled messages

COMMS-SPIKE-001:
- verify Kestrel/Tarsis Comms route remains stable after target logic

---

# 5. Final Rule

Transfer implementation knowledge.

Do not transfer old design authority.
