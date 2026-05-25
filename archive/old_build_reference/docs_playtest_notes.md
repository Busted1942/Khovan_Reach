# Playtest Notes

## Session log

Add a section per playtest session. Date, crew composition, 
which path the captain chose, what worked, what failed, 
what to revise.

### 2026-05-17 - Dev jump harness implementation

**Crew:** N/A - static implementation check only.

**Path taken:** Dev infrastructure.

**Outcome:**
- Added GM-only Act I dev jump controls.
- Refined the harness so reusable Act I cleanup/resupply/spawn helpers live outside the dev UI in `scripts/act_1_state_helpers.mast`.
- Refined Drill Two jump setup again so the shared helper layer owns step-state seeding and target selection; `dev_jump.mast` keeps only dev controls/reporting.
- Static compile passed with `.\sbs.bat compile khovan_reach` from the missions directory.
- Manual Cosmos smoke is still required for control visibility, Drone 01/02 cleanup, and Drill Two/Three runtime behavior.

**What worked:**
- MAST compile accepted the new harness and timer/evasion run IDs.

**What didn't:**
- No live Cosmos smoke has been run in this implementation pass.

**Revisions to make:**
- Smoke the required harness anchors in Cosmos before committing as stable.

## Template

### YYYY-MM-DD — Playtest N

**Crew:**
- Captain: 
- Helm: 
- Weapons: 
- Engineering: 
- Science: 
- Comms: 

**Path taken:** A / B / C / D / brick wall / offramp

**Outcome:**
- DAMCON status: 
- Halcyon Drift status: 
- Salvagers: 
- Total session time: 

**What worked:**

**What didn't:**

**Revisions to make:**
