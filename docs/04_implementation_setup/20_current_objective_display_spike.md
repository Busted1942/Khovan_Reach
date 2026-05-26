# KHOVAN REACH — CURRENT OBJECTIVE DISPLAY SPIKE

Version: 1.0 reconstructed implementation setup note
Status: Implementation spike / not yet proven
Purpose: Determine whether persistent current-objective text can be implemented reliably in Cosmos/MAST without archive spam or stale-objective leakage.

---

# 1. Authority and scope

This file is an implementation setup note, not scenario canon.

The active design remains governed by:

- `docs/01_design/00_scenario_play_guide.md`
- `docs/01_design/10_mast_requirements.md`
- `docs/01_design/40_admin_testing_plan.md`
- `docs/01_design/50_implementation_slice_plan.md`

Persistent current-objective text is not yet proven. The implementation must treat it as a spike until Cosmos/MAST behavior is verified.

---

# 2. Desired outcome

Preferred outcome:

- a true persistent left/mid-screen current-goal display, if Cosmos/MAST supports it

Fallback outcome:

- timed overlay plus managed heartbeat refresh
- Comms archive echo once per objective change
- no Comms archive spam on heartbeat refresh
- no stale objective after story jumps or reload recovery

---

# 3. Required state

The implementation should support current-objective state equivalent to:

```text
current_objective_id
current_objective_title
current_objective_body
current_objective_step
current_objective_owner
current_objective_mode
current_objective_visible
current_objective_run_id
current_objective_updated_at
current_objective_archive_id
```

`current_objective_run_id` is required because delayed or looping overlay behavior can survive story jumps unless invalidated.

---

# 4. Required behavior

Current-objective display must:

- set objective state from one central helper or message router
- clear objective state intentionally
- refresh only through a managed heartbeat if no true persistent display exists
- echo each objective change to the Comms archive once
- avoid archive spam during heartbeat refresh
- invalidate stale heartbeat work after story jumps
- preserve player-facing clarity without becoming a hidden checklist

Do not scatter raw GUI/info-panel calls across scene files.

---

# 5. Spike tests

Minimum tests:

```text
OBJ-001 objective appears
OBJ-002 objective persists or refreshes
OBJ-003 objective echoes once into Comms archive
OBJ-004 objective replacement works
OBJ-005 story jump invalidates stale objective
OBJ-006 ordinary prompt traffic does not permanently erase current objective
OBJ-007 heartbeat refresh does not spam Comms archive
```

Acceptance:

- current-objective display has a proven implementation path or a documented fallback
- no stale objectives after story jumps
- no Comms archive spam

---

# 6. Status rule

Until live Cosmos/MAST confirms the selected implementation path, references to persistent objective display should use spike language.

Do not promote this to a proven player-facing runtime guarantee until tested.
