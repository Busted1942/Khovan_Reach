# Slice 07B Verification — Halcyon Drift arrival

Goal: Halcyon Drift exists as a scannable, hailable contact; Engineering and DAMCON deployment state is tracked; arrival checkpoint persists.

## Status

implemented-live-unproven — all packet tasks built and statically covered. **No live Cosmos run.** Status is reviewer-set per handoff protocol 4.3.

## Source Sections Used

- `docs/01_design/00_scenario_play_guide.md`, Scene 8.
- `docs/01_design/10_mast_requirements.md`, section 7 (Scene 8 = AUTO + GM-SUP).
- `docs/04_implementation_setup/60_mast_api_cookbook.md`, sections 7 and 8.
- `docs/04_implementation_setup/95_scripts_lib_extraction_plan.md`, section 3.1.
- `tests/SLICE06_VERIFICATION.md`, the deferred-destroy finding this encodes.

## Cookbook Patterns Used

- section 8.1 `[LIVE]` — idempotent spawn with existence check and fallback flag.
- section 8.5 `[LIVE]` — cleanup routine.
- section 7.1 `[LIVE]` — Science scan route gated on a role.
- section 6.1 `[LIVE]` — Comms route gated on a selected role.
- section 8.2 `[LIVE]` — Halcyon carries only Khovan roles, no stock `station` role, so no stock panel competes for the option list.
- section 5.2 `[LIVE]` — n/a here; no polling observer in this slice.

## Files Touched

- `scripts/lib/entity_cleanup_helpers.mast` (new — first file in `scripts/lib/`)
- `scripts/acts/act2_halcyon_arrival.mast` (new)
- `scripts/main.mast` (imports + init)
- `scripts/systems/story_jump_presets.mast` (JUMP-013)
- `tests/test_act2_halcyon_arrival_static.py` (new)
- `run_tests.py`

## State Variables

`halcyon_arrival_initialized`, `halcyon_spawned`, `halcyon_object_id`, `halcyon_navproxy_id`, `halcyon_spawn_count`, `halcyon_cleanup_count`, `halcyon_cleanup_in_progress`, `halcyon_destruction_source`, `halcyon_scan_observed`, `halcyon_hail_observed`, `halcyon_arrival_status`, `halcyon_contact_fallback_available`, `engineering_deployed`, `engineering_deploy_status`, `engineering_placement`, `damcon_deployed`, `damcon_deploy_status`, plus three `*_text` copy variables.

`engineering_placement` takes exactly `aboard_halcyon` or `returned_to_artemis`, the strings the packet pins, because **Slice 09 reads this to choose the extended (30 min) or compressed (15 min) DAMCON window.**

The packet flags `damcon_deployed` / `damcon_deploy_status` as a collision hazard against Slice 05's `damcon_rest_*`/`damcon_meal_*` and Slice 09's `damcon_timer_*`. The duplicate-shared check in `run_tests.py` passes.

## Runtime Flow

1. `khovan_act2_initialize_halcyon_arrival` runs from `main.mast` after the Act II pivot init.
2. `khovan_halcyon_spawn` places Halcyon 12 km ahead and 4 km off Artemis, registers object and navproxy ids, writes `post_halcyon_arrival`.
3. Science scan → `halcyon_scan_observed` + sensor report.
4. Comms hail → `halcyon_hail_observed` + Hessler's reply + Dillon's deployment prompt.
5. Captain authorizes → `engineering_placement = aboard_halcyon`, `damcon_deployed`.
6. Optional recall → `engineering_placement = returned_to_artemis`.

## GM Controls

JUMP-013 Halcyon Arrival, Test-Mode gated. **Runs cleanup before seeding**, so repeat jumps cannot stack contacts.

## Player-Facing Behavior

Hessler's hail reply, the Science sensor report, and Dillon's deployment prompt. All follow the addressee convention; `tests/test_mission_text_contract.py` enforces it.

## Tests/Static Checks

`tests/test_act2_halcyon_arrival_static.py` — 19 checks. The load-bearing ones:

- **Helper owns no shared state.** Parses the lib file and asserts zero `shared` declarations. Slice 11 needs this routine for two pirates at once; state would make it a singleton.
- **Cleanup does not clear its own flag.** Asserts `halcyon_cleanup_in_progress = False` is *absent* from the cleanup routine, because the deferred destroy handler owns the clear. This is the exact bug fixed live on 2026-08-08.
- **Selections cleared before deletion**, ordered.
- **JUMP-013 cleans before spawning**, ordered.
- **Comms block opens with a statement**, not an option line — the Kestrel failure shape.

`python run_tests.py quick`: PASS, 236 checks (12 harness, 224 Python tests), 0 failures, 0 warnings, compile preflight included. `tools/review_gate.py --base master`: MECHANIZED PASS.

## Acceptance Covered

Statically: idempotent spawn, cleanup ordering, scan and hail flags, `engineering_placement` set and readable, checkpoint written, JUMP-013 cleanup-before-seed.

## Acceptance Not Covered

- **Everything live.** No Cosmos run.
- **Duplicate spawn.** Only disprovable by running JUMP-013 twice and counting contacts. This is the packet's stop condition: duplicates mean fix the helper before Slice 08, because Slices 10/11/12 all reuse it.
- **Whether the Comms panel renders.** The packet calls an empty panel here "the exact Slice 04 Tarsis failure" and says treat it as FAIL, not ambiguous.
- **Whether `tsn_warpster` is an acceptable hull for a Vesperan civilian hauler.** Chosen because it is the only hull proven to spawn in this repo. Cosmetic, but wrong for the fiction — see Known Risks.
- **Whether Halcyon's spawn offset puts it in sensor range.** 12 km ahead, 4 km off, untested.

## Known Risks/API Uncertainties

**1. Hull art is a placeholder.** `tsn_warpster` is a TSN warship hull standing in for a Vesperan civilian cargo hauler. It is the only hull with proven spawn behavior in this repo, so it was chosen for reliability over fiction. **Routed to the operator:** pick a civilian hull from the Cosmos roster, or accept the placeholder. `starbase_civil` and `kralien_cruiser` are the only other hulls this repo has spawned.

**2. Halcyon carries no stock `station` role — deliberate.** Cookbook 8.2: an object holding the stock role gets the stock Comms panel, which owns the right-hand option list. That was the Kestrel failure. Halcyon is a ship, not a station, so this should not arise, but it is why the roles are Khovan-specific.

**3. The destroy handler treats genuine destruction as an error state.** Halcyon being destroyed in Act II is not a designed outcome; it sets `halcyon_arrival_status = "halcyon_destroyed_unexpectedly"` and clears `halcyon_spawned`. No recovery path exists. If a crew can plausibly destroy her, that needs a design ruling.

## Next Action

Operator live smoke, in this order:

1. **Run JUMP-013 twice.** Count Halcyon contacts. Two or more = stop; the cleanup helper is wrong and four later slices depend on it.
2. Select Halcyon on Science → does the scan option render and set state?
3. Select Halcyon on Comms → does the option list render? Empty panel = FAIL, consult the Slice 04 record.
4. Hail → deployment prompt → authorize → does the GM overview show `engineering_placement`?

---

# Live smoke log (append-only)

_No live run yet._
