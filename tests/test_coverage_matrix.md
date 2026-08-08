# Test Coverage Matrix

Status: tracking implementation progress against admin testing plan test IDs
Last updated: initial creation during plan hardening phase
Purpose: record which test IDs are covered (static/compile/live) and which remain not-covered, in a machine-checkable format

This matrix tracks all test IDs from `docs/01_design/40_admin_testing_plan.md`. Each row represents one test ID and its current coverage status.

Coverage statuses:

- `not-covered` — not yet tested (initial honest state)
- `covered-static` — covered by static file/text checks in run_tests.py or test_*_static.py
- `covered-compile` — covered by MAST compile preflight checks (file must exist and compile)
- `covered-live` — covered by live Cosmos smoke or crewed pass
- `blocked` — cannot be implemented or tested yet (depends on prior work)

**Important:** The status field reflects implementation progress. Most IDs start as `not-covered` — that is the correct honest state, not a problem to hide.

---

## Coverage by Test ID

| Test ID | Slice | Status | Evidence |
|---------|-------|--------|----------|
| ACT1-001 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-002 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-003 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-004 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-005 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-006 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-007 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-008 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-009 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-010 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-011 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-012 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-013 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-014 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-015 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-016 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-017 | 04 | covered-static | test_act1_generator_tarsis_static.py |
| ACT1-018 | 05 | covered-static | test_act1_engineering_shakedown_static.py |
| ACT1-019 | 06 | covered-static | test_act1_drone_contact_fire_static.py |
| ACT1-020 | 06 | covered-static | test_act1_drone_contact_fire_static.py |
| ACT1-021 | 06 | covered-static | test_act1_drone_contact_fire_static.py |
| ACT1-022 | 06 | covered-static | test_act1_drone_contact_fire_static.py |
| ACT1-023 | 06 | covered-static | test_act1_drone_contact_fire_static.py |
| ACT1-024 | 06 | covered-static | test_act1_drone_contact_fire_static.py |
| BOOT-001 | 01 | covered-compile | story.mast compiles |
| BOOT-002 | 01 | covered-compile | main.mast imports in story.mast |
| BOOT-003 | 01 | covered-compile | story.json loads in MAST compile preflight |
| BOOT-004 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-005 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-006 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-007 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-008 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-009 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-010 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-011 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-012 | 01 | covered-static | test_bootstrap_static.py |
| CACHE | 10 | not-covered | not yet implemented |
| DAMCON-001 | 09 | not-covered | not yet implemented |
| DAMCON-002 | 09 | not-covered | not yet implemented |
| DAMCON-003 | 09 | not-covered | not yet implemented |
| DAMCON-004 | 09 | not-covered | not yet implemented |
| DAMCON-005 | 09 | not-covered | not yet implemented |
| DAMCON-006 | 09 | not-covered | not yet implemented |
| DAMCON-007 | 09 | not-covered | not yet implemented |
| DAMCON-008 | 09 | not-covered | not yet implemented |
| DAMCON-009 | 09 | not-covered | not yet implemented |
| DAMCON-010 | 09 | not-covered | not yet implemented |
| DAMCON-011 | 09 | not-covered | not yet implemented |
| DAMCON-012 | 09 | not-covered | not yet implemented |
| DAMCON-013 | 09 | not-covered | not yet implemented |
| DAMCON-014 | 09 | not-covered | not yet implemented |
| DAMCON-015 | 09 | not-covered | not yet implemented |
| DAMCON-016 | 09 | not-covered | not yet implemented |
| DAMCON-017 | 09 | not-covered | not yet implemented |
| DAMCON-018 | 09 | not-covered | not yet implemented |
| DAMCON-019 | 09 | not-covered | not yet implemented |
| DAMCON-020 | 09 | not-covered | not yet implemented |
| DAMCON-021 | 09 | not-covered | not yet implemented |
| DAMCON-022 | 09 | not-covered | not yet implemented |
| DAMCON-023 | 09 | not-covered | not yet implemented |
| GOLD-001 | all | not-covered | not yet implemented |
| GOLD-002 | all | not-covered | not yet implemented |
| GOLD-003 | all | not-covered | not yet implemented |
| GOLD-004 | all | not-covered | not yet implemented |
| GOLD-005 | all | not-covered | not yet implemented |
| GOLD-006 | all | not-covered | not yet implemented |
| JUMP-001 | 03 | not-covered | not yet tested |
| JUMP-002 | 03 | not-covered | not yet tested |
| JUMP-003 | 03 | not-covered | not yet tested |
| JUMP-004 | 03 | not-covered | not yet tested |
| JUMP-005 | 03 | not-covered | not yet tested |
| JUMP-006 | 03 | not-covered | not yet tested |
| JUMP-007 | 03 | not-covered | not yet tested |
| JUMP-008 | 03 | not-covered | not yet tested |
| JUMP-009 | 03 | not-covered | not yet tested |
| JUMP-010 | 03 | not-covered | not yet tested |
| JUMP-011 | 07 | not-covered | Act II not yet implemented |
| JUMP-012 | 07 | not-covered | Act II not yet implemented |
| JUMP-013 | 08 | not-covered | Act II not yet implemented |
| JUMP-014 | 08 | not-covered | Act II not yet implemented |
| JUMP-015 | 08 | not-covered | Act II not yet implemented |
| JUMP-016 | 10 | not-covered | Cache not yet implemented |
| JUMP-017 | 10 | not-covered | Cache not yet implemented |
| JUMP-018 | 11 | not-covered | Pirates not yet implemented |
| JUMP-019 | 11 | not-covered | Pirates not yet implemented |
| JUMP-020 | 11 | not-covered | Pirates not yet implemented |
| JUMP-021 | 12 | not-covered | Combat not yet implemented |
| JUMP-022 | 10 | not-covered | Cache not yet implemented |
| JUMP-023 | 13 | not-covered | Repair not yet implemented |
| JUMP-024 | 13 | not-covered | Repair not yet implemented |
| JUMP-025 | 13 | not-covered | Repair not yet implemented |
| JUMP-026 | 07 | not-covered | Act II not yet implemented |
| JUMP-027 | 14 | not-covered | Debrief not yet implemented |
| PIRATE-001 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-002 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-003 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-004 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-005 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-006 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-007 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-008 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-009 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-010 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-011 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-012 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-013 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-014 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-015 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-016 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-017 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-018 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-019 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-020 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-021 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-022 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-023 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-024 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-025 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-026 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-027 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-028 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-029 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-030 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-031 | 11 | not-covered | Pirates not yet implemented |
| PIRATE-032 | 11 | not-covered | Pirates not yet implemented |
| SAVE-001 | 15 | not-covered | Reload not yet implemented |
| SAVE-002 | 15 | not-covered | Reload not yet implemented |
| SAVE-003 | 15 | not-covered | Reload not yet implemented |
| SAVE-004 | 15 | not-covered | Reload not yet implemented |
| SAVE-005 | 15 | not-covered | Reload not yet implemented |
| SAVE-006 | 15 | not-covered | Reload not yet implemented |
| SAVE-007 | 15 | not-covered | Reload not yet implemented |
| SAVE-008 | 15 | not-covered | Reload not yet implemented |
| SAVE-009 | 15 | not-covered | Reload not yet implemented |
| SAVE-010 | 15 | not-covered | Reload not yet implemented |
| SAVE-011 | 15 | not-covered | Reload not yet implemented |
| SAVE-012 | 15 | not-covered | Reload not yet implemented |
| SAVE-013 | 15 | not-covered | Reload not yet implemented |
| SAVE-014 | 15 | not-covered | Reload not yet implemented |
| SAVE-015 | 15 | not-covered | Reload not yet implemented |
| SAVE-016 | 15 | not-covered | Reload not yet implemented |
| SAVE-017 | 15 | not-covered | Reload not yet implemented |
| SAVE-018 | 15 | not-covered | Reload not yet implemented |
| SAVE-019 | 15 | not-covered | Reload not yet implemented |
| SAVE-020 | 15 | not-covered | Reload not yet implemented |
| SAVE-021 | 15 | not-covered | Reload not yet implemented |
| SAVE-022 | 15 | not-covered | Reload not yet implemented |
| SAVE-023 | 15 | not-covered | Reload not yet implemented |
| SAVE-024 | 15 | not-covered | Reload not yet implemented |
