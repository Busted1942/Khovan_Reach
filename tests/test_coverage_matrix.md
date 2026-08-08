# Test Coverage Matrix

Status: tracking implementation progress against admin testing plan test IDs
Last updated: fixed regex to include digit-prefix IDs like ACT1-*, D2-*, D3-* (2026-08-08)
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
| ACT1-001 | 04-06 | not-covered | not yet tested |
| ACT1-002 | 04-06 | not-covered | not yet tested |
| ACT1-003 | 04-06 | not-covered | not yet tested |
| ACT1-004 | 04-06 | not-covered | not yet tested |
| ACT1-005 | 04-06 | not-covered | not yet tested |
| ACT1-006 | 04-06 | not-covered | not yet tested |
| ACT1-007 | 04-06 | not-covered | not yet tested |
| ACT1-008 | 04-06 | not-covered | not yet tested |
| ACT1-009 | 04-06 | not-covered | not yet tested |
| ACT1-010 | 04-06 | not-covered | not yet tested |
| ACT1-011 | 04-06 | not-covered | not yet tested |
| ACT1-012 | 04-06 | not-covered | not yet tested |
| ACT1-013 | 04-06 | not-covered | not yet tested |
| ACT1-014 | 04-06 | not-covered | not yet tested |
| ACT1-015 | 04-06 | not-covered | not yet tested |
| ACT1-016 | 04-06 | not-covered | not yet tested |
| ACT1-017 | 04-06 | not-covered | not yet tested |
| ACT1-018 | 04-06 | not-covered | not yet tested |
| ACT1-019 | 04-06 | covered-static | Slice 06 Phase B static reset-offset assertions; live unproven |
| ACT1-020 | 04-06 | covered-static | Slice 06 Phase B static premature-destruction reset assertions; live unproven |
| ACT1-021 | 04-06 | covered-static | Slice 06 Phase B static range and guarded 15-second hold assertions; live unproven |
| ACT1-022 | 04-06 | covered-static | Slice 06 Phase B static MANUAL_SYSTEM=WEAPONS three-hit assertions; live unproven |
| ACT1-023 | 04-06 | covered-static | Slice 06 Phase B static Drone 02 genuine-destruction / Act-II-ready assertions; live unproven |
| ACT1-024 | 04-06 | covered-static | Slice 06 Phase B static duplicate-suppressed cultural objective assertions; live unproven |
| ADMIN-001 | 16 | not-covered | not yet implemented |
| ADMIN-002 | 16 | not-covered | not yet implemented |
| ADMIN-003 | 16 | not-covered | not yet implemented |
| ADMIN-004 | 16 | not-covered | not yet implemented |
| ADMIN-005 | 16 | not-covered | not yet implemented |
| ADMIN-006 | 16 | not-covered | not yet implemented |
| ADMIN-007 | 16 | not-covered | not yet implemented |
| ADMIN-008 | 16 | not-covered | not yet implemented |
| ADMIN-009 | 16 | not-covered | not yet implemented |
| ADMIN-010 | 16 | not-covered | not yet implemented |
| ADMIN-011 | 16 | not-covered | not yet implemented |
| ADMIN-012 | 16 | not-covered | not yet implemented |
| ADMIN-013 | 16 | not-covered | not yet implemented |
| ADMIN-014 | 16 | not-covered | not yet implemented |
| ADMIN-015 | 16 | not-covered | not yet implemented |
| ADMIN-016 | 16 | not-covered | not yet implemented |
| ADMIN-017 | 16 | not-covered | not yet implemented |
| BOOT-001 | 01 | covered-compile | story.mast compiles |
| BOOT-002 | 01 | covered-compile | story.mast compiles |
| BOOT-003 | 01 | covered-compile | story.mast compiles |
| BOOT-004 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-005 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-006 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-007 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-008 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-009 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-010 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-011 | 01 | covered-static | test_bootstrap_static.py |
| BOOT-012 | 01 | covered-static | test_bootstrap_static.py |
| BRANCH-001 | 16 | not-covered | not yet implemented |
| BRANCH-002 | 16 | not-covered | not yet implemented |
| BRANCH-003 | 16 | not-covered | not yet implemented |
| BRANCH-004 | 16 | not-covered | not yet implemented |
| BRANCH-005 | 16 | not-covered | not yet implemented |
| BRANCH-006 | 16 | not-covered | not yet implemented |
| BRANCH-007 | 16 | not-covered | not yet implemented |
| CACHE-001 | 10 | not-covered | not yet implemented |
| CACHE-002 | 10 | not-covered | not yet implemented |
| CACHE-003 | 10 | not-covered | not yet implemented |
| CACHE-004 | 10 | not-covered | not yet implemented |
| CACHE-005 | 10 | not-covered | not yet implemented |
| CACHE-006 | 10 | not-covered | not yet implemented |
| CACHE-007 | 10 | not-covered | not yet implemented |
| CACHE-008 | 10 | not-covered | not yet implemented |
| CACHE-009 | 10 | not-covered | not yet implemented |
| CACHE-010 | 10 | not-covered | not yet implemented |
| CACHE-011 | 10 | not-covered | not yet implemented |
| CACHE-012 | 10 | not-covered | not yet implemented |
| D2-001 | 04 | not-covered | not yet tested |
| D2-002 | 04 | not-covered | not yet tested |
| D2-003 | 04 | not-covered | not yet tested |
| D2-004 | 04 | not-covered | not yet tested |
| D2-005 | 04 | not-covered | not yet tested |
| D2-006 | 04 | not-covered | not yet tested |
| D2-007 | 04 | not-covered | not yet tested |
| D2-008 | 04 | not-covered | not yet tested |
| D2-009 | 04 | not-covered | not yet tested |
| D2-010 | 04 | not-covered | not yet tested |
| D2-011 | 04 | not-covered | not yet tested |
| D2-012 | 04 | not-covered | not yet tested |
| D2-013 | 04 | not-covered | not yet tested |
| D2-014 | 04 | not-covered | not yet tested |
| D2-015 | 04 | not-covered | not yet tested |
| D2-016 | 04 | not-covered | not yet tested |
| D2-017 | 04 | not-covered | not yet tested |
| D2-018 | 04 | not-covered | not yet tested |
| D2-019 | 04 | not-covered | not yet tested |
| D2-020 | 04 | not-covered | not yet tested |
| D3-001 | 05 | not-covered | not yet tested |
| D3-002 | 05 | not-covered | not yet tested |
| D3-003 | 05 | not-covered | not yet tested |
| D3-004 | 05 | not-covered | not yet tested |
| D3-005 | 05 | not-covered | not yet tested |
| D3-006 | 05 | not-covered | not yet tested |
| D3-007 | 05 | not-covered | not yet tested |
| D3-008 | 05 | not-covered | not yet tested |
| D3-009 | 05 | not-covered | not yet tested |
| D3-010 | 05 | not-covered | not yet tested |
| D3-011 | 05 | not-covered | not yet tested |
| D3-012 | 05 | not-covered | not yet tested |
| D3-013 | 05 | not-covered | not yet tested |
| D3-014 | 05 | not-covered | not yet tested |
| DAMCON-001 | 09 | not-covered | not yet implemented |
| DAMCON-002 | 09 | not-covered | not yet implemented |
| DAMCON-003 | 09 | not-covered | not yet implemented |
| DAMCON-004 | 09 | not-covered | not yet implemented |
| DAMCON-005 | 09 | not-covered | not yet implemented |
| DAMCON-006 | 09 | not-covered | not yet implemented |
| DAMCON-010 | 09 | not-covered | not yet implemented |
| DAMCON-011 | 09 | not-covered | not yet implemented |
| DAMCON-012 | 09 | not-covered | not yet implemented |
| DAMCON-013 | 09 | not-covered | not yet implemented |
| DAMCON-014 | 09 | not-covered | not yet implemented |
| DAMCON-015 | 09 | not-covered | not yet implemented |
| DAMCON-016 | 09 | not-covered | not yet implemented |
| DAMCON-017 | 09 | not-covered | not yet implemented |
| DAMCON-018 | 09 | not-covered | not yet implemented |
| DAMCON-020 | 09 | not-covered | not yet implemented |
| DAMCON-021 | 09 | not-covered | not yet implemented |
| DAMCON-022 | 09 | not-covered | not yet implemented |
| DAMCON-023 | 09 | not-covered | not yet implemented |
| DAMCON-024 | 09 | not-covered | not yet implemented |
| DAMCON-025 | 09 | not-covered | not yet implemented |
| DAMCON-026 | 09 | not-covered | not yet implemented |
| DAMCON-027 | 09 | not-covered | not yet implemented |
| DEBRIEF-001 | 14 | not-covered | not yet implemented |
| DEBRIEF-002 | 14 | not-covered | not yet implemented |
| DEBRIEF-003 | 14 | not-covered | not yet implemented |
| DEBRIEF-004 | 14 | not-covered | not yet implemented |
| DEBRIEF-005 | 14 | not-covered | not yet implemented |
| DEBRIEF-006 | 14 | not-covered | not yet implemented |
| DEBRIEF-007 | 14 | not-covered | not yet implemented |
| DEBRIEF-008 | 14 | not-covered | not yet implemented |
| DEBRIEF-009 | 14 | not-covered | not yet implemented |
| DEBRIEF-010 | 14 | not-covered | not yet implemented |
| DEBRIEF-011 | 14 | not-covered | not yet implemented |
| DEBRIEF-012 | 14 | not-covered | not yet implemented |
| GOLD-001 | all | not-covered | not yet implemented |
| GOLD-002 | all | not-covered | not yet implemented |
| GOLD-003 | all | not-covered | not yet implemented |
| GOLD-004 | all | not-covered | not yet implemented |
| GOLD-005 | all | not-covered | not yet implemented |
| GOLD-006 | all | not-covered | not yet implemented |
| JUMP-001 | 03-16 | not-covered | not yet tested |
| JUMP-002 | 03-16 | not-covered | not yet tested |
| JUMP-003 | 03-16 | not-covered | not yet tested |
| JUMP-004 | 03-16 | not-covered | not yet tested |
| JUMP-005 | 03-16 | not-covered | not yet tested |
| JUMP-006 | 03-16 | not-covered | not yet tested |
| JUMP-007 | 03-16 | not-covered | not yet tested |
| JUMP-008 | 03-16 | not-covered | not yet tested |
| JUMP-009 | 03-16 | not-covered | not yet tested |
| JUMP-010 | 03-16 | not-covered | not yet tested |
| JUMP-011 | 03-16 | not-covered | not yet tested |
| JUMP-012 | 03-16 | not-covered | not yet tested |
| JUMP-013 | 03-16 | not-covered | not yet tested |
| JUMP-014 | 03-16 | not-covered | not yet tested |
| JUMP-015 | 03-16 | not-covered | not yet tested |
| JUMP-016 | 03-16 | not-covered | not yet tested |
| JUMP-017 | 03-16 | not-covered | not yet tested |
| JUMP-018 | 03-16 | not-covered | not yet tested |
| JUMP-019 | 03-16 | not-covered | not yet tested |
| JUMP-020 | 03-16 | not-covered | not yet tested |
| JUMP-021 | 03-16 | not-covered | not yet tested |
| JUMP-022 | 03-16 | not-covered | not yet tested |
| JUMP-023 | 03-16 | not-covered | not yet tested |
| JUMP-024 | 03-16 | not-covered | not yet tested |
| JUMP-025 | 03-16 | not-covered | not yet tested |
| JUMP-026 | 03-16 | not-covered | not yet tested |
| JUMP-027 | 03-16 | not-covered | not yet tested |
| JUMPTEST-001 | 03 | not-covered | not yet tested |
| JUMPTEST-002 | 03 | not-covered | not yet tested |
| JUMPTEST-003 | 03 | not-covered | not yet tested |
| JUMPTEST-004 | 03 | not-covered | not yet tested |
| JUMPTEST-005 | 03 | not-covered | not yet tested |
| JUMPTEST-006 | 03 | not-covered | not yet tested |
| JUMPTEST-007 | 03 | not-covered | not yet tested |
| JUMPTEST-008 | 03 | not-covered | not yet tested |
| JUMPTEST-009 | 03 | not-covered | not yet tested |
| JUMPTEST-010 | 03 | not-covered | not yet tested |
| JUMPTEST-011 | 03 | not-covered | not yet tested |
| JUMPTEST-012 | 03 | not-covered | not yet tested |
| JUMPTEST-013 | 03 | not-covered | not yet tested |
| JUMPTEST-014 | 03 | not-covered | not yet tested |
| JUMPTEST-015 | 03 | not-covered | not yet tested |
| JUMPTEST-016 | 03 | not-covered | not yet tested |
| JUMPTEST-017 | 03 | not-covered | not yet tested |
| JUMPTEST-018 | 03 | not-covered | not yet tested |
| JUMPTEST-019 | 03 | not-covered | not yet tested |
| JUMPTEST-020 | 03 | not-covered | not yet tested |
| JUMPTEST-021 | 03 | not-covered | not yet tested |
| KT-001 | 04 | not-covered | not yet tested |
| KT-002 | 04 | not-covered | not yet tested |
| KT-003 | 04 | not-covered | not yet tested |
| KT-004 | 04 | not-covered | not yet tested |
| KT-005 | 04 | not-covered | not yet tested |
| KT-006 | 04 | not-covered | not yet tested |
| MSG-001 | 01 | not-covered | not yet tested |
| MSG-002 | 01 | not-covered | not yet tested |
| MSG-003 | 01 | not-covered | not yet tested |
| MSG-004 | 01 | not-covered | not yet tested |
| MSG-005 | 01 | not-covered | not yet tested |
| OBJ-001 | 08 | not-covered | not yet tested |
| OBJ-002 | 08 | not-covered | not yet tested |
| OBJ-003 | 08 | not-covered | not yet tested |
| OBJ-004 | 08 | not-covered | not yet tested |
| OBJ-005 | 08 | not-covered | not yet tested |
| OBJ-006 | 08 | not-covered | not yet tested |
| OBJ-007 | 08 | not-covered | not yet tested |
| OBJ-008 | 08 | not-covered | not yet tested |
| OBJ-009 | 08 | not-covered | not yet tested |
| OBJ-010 | 08 | not-covered | not yet tested |
| OTE-001 | 16 | not-covered | not yet tested |
| OTE-002 | 16 | not-covered | not yet tested |
| OTE-003 | 16 | not-covered | not yet tested |
| OTE-004 | 16 | not-covered | not yet tested |
| OTE-005 | 16 | not-covered | not yet tested |
| OTE-006 | 16 | not-covered | not yet tested |
| OTE-007 | 16 | not-covered | not yet tested |
| OTE-008 | 16 | not-covered | not yet tested |
| OTE-009 | 16 | not-covered | not yet tested |
| PIRATE-001 | 11 | not-covered | not yet implemented |
| PIRATE-002 | 11 | not-covered | not yet implemented |
| PIRATE-003 | 11 | not-covered | not yet implemented |
| PIRATE-004 | 11 | not-covered | not yet implemented |
| PIRATE-005 | 11 | not-covered | not yet implemented |
| PIRATE-006 | 11 | not-covered | not yet implemented |
| PIRATE-010 | 11 | not-covered | not yet implemented |
| PIRATE-011 | 11 | not-covered | not yet implemented |
| PIRATE-012 | 11 | not-covered | not yet implemented |
| PIRATE-013 | 11 | not-covered | not yet implemented |
| PIRATE-014 | 11 | not-covered | not yet implemented |
| PIRATE-015 | 11 | not-covered | not yet implemented |
| PIRATE-016 | 11 | not-covered | not yet implemented |
| PIRATE-020 | 11 | not-covered | not yet implemented |
| PIRATE-021 | 11 | not-covered | not yet implemented |
| PIRATE-022 | 11 | not-covered | not yet implemented |
| PIRATE-023 | 11 | not-covered | not yet implemented |
| PIRATE-024 | 11 | not-covered | not yet implemented |
| PIRATE-025 | 11 | not-covered | not yet implemented |
| PIRATE-030 | 11 | not-covered | not yet implemented |
| PIRATE-031 | 11 | not-covered | not yet implemented |
| PIRATE-032 | 11 | not-covered | not yet implemented |
| PIRATE-033 | 11 | not-covered | not yet implemented |
| PIRATE-034 | 11 | not-covered | not yet implemented |
| PIRATE-035 | 11 | not-covered | not yet implemented |
| PIRATE-040 | 11 | not-covered | not yet implemented |
| PIRATE-041 | 11 | not-covered | not yet implemented |
| PIRATE-042 | 11 | not-covered | not yet implemented |
| PIRATE-043 | 11 | not-covered | not yet implemented |
| PIRATE-044 | 11 | not-covered | not yet implemented |
| PIRATE-045 | 11 | not-covered | not yet implemented |
| PIRATE-046 | 11 | not-covered | not yet implemented |
| PLAYBOOT-001 | 01A | not-covered | not yet tested |
| PLAYBOOT-002 | 01A | not-covered | not yet tested |
| PLAYBOOT-003 | 01A | not-covered | not yet tested |
| PLAYBOOT-004 | 01A | not-covered | not yet tested |
| PLAYBOOT-005 | 01A | not-covered | not yet tested |
| PLAYBOOT-006 | 01A | not-covered | not yet tested |
| PLAYBOOT-007 | 01A | not-covered | not yet tested |
| PLAYBOOT-008 | 01A | not-covered | not yet tested |
| PLAYBOOT-009 | 01A | not-covered | not yet tested |
| PLAYBOOT-010 | 01A | not-covered | not yet tested |
| PRE-001 | 16 | not-covered | not yet tested |
| PRE-002 | 16 | not-covered | not yet tested |
| PRE-003 | 16 | not-covered | not yet tested |
| PRE-004 | 16 | not-covered | not yet tested |
| PRE-005 | 16 | not-covered | not yet tested |
| PRE-006 | 16 | not-covered | not yet tested |
| PRE-007 | 16 | not-covered | not yet tested |
| PRE-008 | 16 | not-covered | not yet tested |
| PRE-009 | 16 | not-covered | not yet tested |
| PRE-010 | 16 | not-covered | not yet tested |
| PRE-011 | 16 | not-covered | not yet tested |
| PRE-012 | 16 | not-covered | not yet tested |
| SAFE-001 | 01 | not-covered | not yet tested |
| SAFE-002 | 01 | not-covered | not yet tested |
| SAFE-003 | 01 | not-covered | not yet tested |
| SAFE-004 | 01 | not-covered | not yet tested |
| SAFE-005 | 01 | not-covered | not yet tested |
| SAFE-006 | 01 | not-covered | not yet tested |
| SAVE-001 | 15 | not-covered | not yet implemented |
| SAVE-002 | 15 | not-covered | not yet implemented |
| SAVE-003 | 15 | not-covered | not yet implemented |
| SAVE-004 | 15 | not-covered | not yet implemented |
| SAVE-005 | 15 | not-covered | not yet implemented |
| SAVE-006 | 15 | not-covered | not yet implemented |
| SAVE-007 | 15 | not-covered | not yet implemented |
| SAVE-008 | 15 | not-covered | not yet implemented |
| SAVE-010 | 15 | not-covered | not yet implemented |
| SAVE-011 | 15 | not-covered | not yet implemented |
| SAVE-012 | 15 | not-covered | not yet implemented |
| SAVE-013 | 15 | not-covered | not yet implemented |
| SAVE-014 | 15 | not-covered | not yet implemented |
| SAVE-015 | 15 | not-covered | not yet implemented |
| SAVE-016 | 15 | not-covered | not yet implemented |
| SAVE-020 | 15 | not-covered | not yet implemented |
| SAVE-021 | 15 | not-covered | not yet implemented |
| SAVE-022 | 15 | not-covered | not yet implemented |
| SAVE-023 | 15 | not-covered | not yet implemented |
| SAVE-024 | 15 | not-covered | not yet implemented |
| SAVE-030 | 15 | not-covered | not yet implemented |
| SAVE-031 | 15 | not-covered | not yet implemented |
| SAVE-032 | 15 | not-covered | not yet implemented |
| SAVE-033 | 15 | not-covered | not yet implemented |
| SPIKE-001 | 06 | not-covered | not yet tested |
| SPIKE-002 | 06 | not-covered | not yet tested |
| SPIKE-003 | 06 | not-covered | not yet tested |
| SPIKE-004 | 06 | not-covered | not yet tested |
| SPIKE-005 | 06 | not-covered | not yet tested |
| SPIKE-006 | 06 | not-covered | not yet tested |
| SPIKE-007 | 06 | not-covered | not yet tested |
| SPIKE-008 | 06 | not-covered | not yet tested |
| SPIKE-009 | 06 | not-covered | not yet tested |
