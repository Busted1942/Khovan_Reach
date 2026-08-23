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
- section 7.1 `[LIVE]` — preserve the stock Science display by omitting custom `//science` routes; Science reports verbally and the observable gate is carried by Comms.
- section 6.1 `[LIVE]` — matching `//enable/comms` and `//comms` companions gated on Halcyon's selected role.
- section 7.4 `[LIVE]` / preference 3 `[UNPROVEN]` — an unknown contact gets no Comms buttons, so spawn writes only Halcyon's side-specific `scan` key and leaves the stock `scan_type_list` untouched. The fallback remains armed until this is live-measured.
- section 8.2 `[LIVE]` — Halcyon carries only Khovan roles, no stock `station` role, so no stock panel competes for the option list.
- section 5.2 `[LIVE]` — n/a here; no polling observer in this slice.
- section 9.4 `[COMPILE]` plus section 12 uncertainty handling — the installed library exposes `grid_restore_damcons()` but no away-team abstraction. The detachment therefore follows the library's own grid-object deletion shape and remains live-unproven.

## Files Touched

- `scripts/lib/entity_cleanup_helpers.mast` (new — first file in `scripts/lib/`)
- `scripts/acts/act2_halcyon_arrival.mast` (new)
- `scripts/main.mast` (imports + init)
- `scripts/systems/story_jump_presets.mast` (JUMP-013)
- `tests/test_act2_halcyon_arrival_static.py` (new)
- `run_tests.py`

## State Variables

`halcyon_arrival_initialized`, `halcyon_spawned`, `halcyon_object_id`, `halcyon_navproxy_id`, `halcyon_spawn_count`, `halcyon_cleanup_count`, `halcyon_cleanup_in_progress`, `halcyon_destruction_source`, `halcyon_scan_observed`, `halcyon_hail_observed`, `halcyon_arrival_status`, `halcyon_contact_fallback_available`, `engineering_deployed`, `engineering_deploy_status`, `engineering_placement`, `damcon_deployed`, `damcon_deploy_status`, `halcyon_deploy_acknowledgement_sent`, the `halcyon_manifest_*` selection/count/summary fields, and the `halcyon_damcon_*` team identity/count/transfer fields, plus the player-facing `*_text` variables.

`engineering_placement` takes exactly `aboard_halcyon` or `returned_to_artemis`, the strings the packet pins, because **Slice 09 reads this to choose the extended (30 min) or compressed (15 min) DAMCON window.**

The packet flags `damcon_deployed` / `damcon_deploy_status` as a collision hazard against Slice 05's `damcon_rest_*`/`damcon_meal_*` and Slice 09's `damcon_timer_*`. The duplicate-shared check in `run_tests.py` passes.

## Runtime Flow

1. `khovan_act2_initialize_halcyon_arrival` runs from `main.mast` after the Act II pivot init.
2. `khovan_halcyon_spawn` places Halcyon 12 km ahead and 4 km off Artemis, registers object and navproxy ids, creates Captain Aurel Hessler as a lifeform hosted aboard Halcyon, and writes `post_halcyon_arrival`.
3. Science uses the stock sensor display and reports Halcyon's identity and condition verbally to the Captain; no automatic Science Comms message is generated.
4. The Captain orders Comms to select Halcyon and hail; the hail handler records `halcyon_scan_observed` and `halcyon_hail_observed`. Hessler answers and asks Artemis to transmit an away-team complement consisting of the required DAMCON team and one or two officers, including Engineering. Dillon then addresses only the Captain with protocol: Comms assembles the manifest, Engineering is required by the repair, one additional officer is discretionary, and DAMCON Team Reyes consists of Reyes, Park, and Achebe. Dillon also states that a Captain joining the away team must designate acting command aboard Artemis.
5. Comms selects Engineering and optionally the Captain, Science, Weapons, Helm, or Comms as the second officer. Add/remove controls enforce a maximum of two; transmission is unavailable until Engineering is selected. If the Captain is selected, Comms must designate a remaining Science, Weapons, Helm, or Comms officer as acting command before transmission becomes available. Hessler repeats both the transmitted complement and acting-command assignment, then confirms that Halcyon's transfer lock is standing by. Comms can revise either assignment before deployment.
6. The Captain authorizes → the runtime selects DC3 when available, removes that real grid team and any old-style rally marker from Artemis, verifies the `damcons` roster fell by exactly one, then sets `engineering_placement = aboard_halcyon` and `damcon_deployed`. A failed reduction blocks the away-mission transition and exposes fallback status.
7. Optional recall → `grid_restore_damcons(artemis_id)` recreates the tracked named team, the runtime verifies the roster rose by exactly one, then sets `engineering_placement = returned_to_artemis`. The shared Act II reset path performs the same restoration before JUMP-011/012/013 cleanup can clear deployment state.

## GM Controls

JUMP-013 Halcyon Arrival, Test-Mode gated. **Runs cleanup before seeding**, so repeat jumps cannot stack contacts.

## Player-Facing Behavior

Hessler's hail reply, Hessler's request for the away-team complement, his acknowledgement naming the transmitted roster and any acting commander, and fiction-facing Hessler status updates. Science reports verbally to the Captain and does not generate a Comms message. Dillon does not speak for Halcyon or lead the rescue; he states manifest and command-transfer protocol to the Captain. Comms performs the actual one-or-two-officer selection and acting-command designation, while the Captain retains deployment authorization. If the Captain deploys, the post-transfer objective addresses Artemis Acting Command instead. All written messages follow the addressee convention; `tests/test_mission_text_contract.py` enforces it.

## Tests/Static Checks

`tests/test_act2_halcyon_arrival_static.py` — 46 checks. The load-bearing ones:

- **Helper owns no shared state.** Parses the lib file and asserts zero `shared` declarations. Slice 11 needs this routine for two pirates at once; state would make it a singleton.
- **Cleanup does not clear its own flag.** Asserts `halcyon_cleanup_in_progress = False` is *absent* from the cleanup routine, because the deferred destroy handler owns the clear. This is the exact bug fixed live on 2026-08-08.
- **Selections cleared before deletion**, ordered.
- **JUMP-013 cleans before spawning**, ordered.
- **Comms block opens with a statement**, not an option line — the Kestrel failure shape.
- **DAMCON departure is a grid mutation, not a story-only flag.** Asserts the authorization calls the detach routine before advancing, DC3 is preferred, the library's grid-delete/agent-cleanup pair is used, and exactly-one count verification is present.
- **Recall and jumps cannot forget the team.** Asserts recall and the common Act II reset restore the named team before advancing or cleaning up, and block if verification fails.

`python run_tests.py quick`: PASS, 292 checks (12 harness, 280 Python tests), 0 failures, 0 warnings, compile preflight included. `tools/review_gate.py --base master`: MECHANIZED PASS.

## Acceptance Covered

Statically: idempotent spawn, cleanup ordering, scan and hail flags, a one-team DAMCON grid reduction before deployment state advances, tracked-team restoration before recall/jump state advances, `engineering_placement` set and readable, checkpoint written, JUMP-013 cleanup-before-seed.

## Acceptance Not Covered

- **Everything live.** No Cosmos run.
- **Duplicate spawn.** Only disprovable by running JUMP-013 twice and counting contacts. This is the packet's stop condition: duplicates mean fix the helper before Slice 08, because Slices 10/11/12 all reuse it.
- **Whether the Comms panel renders.** The packet calls an empty panel here "the exact Slice 04 Tarsis failure" and says treat it as FAIL, not ambiguous.
- **Whether Hessler's Halcyon-hosted lifeform and badge render.** Dillon and Anderson prove the helper can create addressable lifeforms, but Hessler's deferred creation after the Halcyon spawn and cleanup/recreation cycle remain live-unproven. The Halcyon-object fallback preserves every required message.
- **Whether `tsn_warpster` is an acceptable hull for a Vesperan civilian hauler.** Chosen because it is the only hull proven to spawn in this repo. Cosmetic, but wrong for the fiction — see Known Risks.
- **Whether Halcyon's spawn offset puts it in sensor range.** 12 km ahead, 4 km off, untested.
- **Whether the DAMCON roster visibly drops and restores in this Cosmos build.** Static tests and compile preflight prove the route and call shapes, not live Engineering UI/agent lifecycle behavior.
- **Whether the Comms option list remains usable at every one/two-officer add/remove/revise state.** Static checks prove the conditions and handlers exist, not that the live panel refreshes after each selection.
- **Officer departure is story state, not console reassignment.** Only the DAMCON grid team is mechanically removed. Selected bridge officers must roleplay leaving their stations; the runtime does not disconnect clients or disable consoles.
- **Captain decisions from Halcyon are a narrative relocation, not a new downstream runtime branch.** Slice packets gate later behavior on `engineering_placement`, cascade state, and elapsed time; they do not read Captain location. Future Scene 9/10 presentation must nevertheless respect the acting-command assignment rather than assuming every Captain decision originates on the Artemis bridge.

## Known Risks/API Uncertainties

**1. Hull art is a placeholder.** `tsn_warpster` is a TSN warship hull standing in for a Vesperan civilian cargo hauler. It is the only hull with proven spawn behavior in this repo, so it was chosen for reliability over fiction. **Routed to the operator:** pick a civilian hull from the Cosmos roster, or accept the placeholder. `starbase_civil` and `kralien_cruiser` are the only other hulls this repo has spawned.

**2. Halcyon carries no stock `station` role — deliberate.** Cookbook 8.2: an object holding the stock role gets the stock Comms panel, which owns the right-hand option list. That was the Kestrel failure. Halcyon is a ship, not a station, so this should not arise, but it is why the roles are Khovan-specific.

**3. The destroy handler treats genuine destruction as an error state.** Halcyon being destroyed in Act II is not a designed outcome; it sets `halcyon_arrival_status = "halcyon_destroyed_unexpectedly"` and clears `halcyon_spawned`. No recovery path exists. If a crew can plausibly destroy her, that needs a design ruling.

**4. Single-team away deployment has no cookbook-proven abstraction.**

```text
API uncertainty:
Question:            Can one DAMCON grid team be removed for an away mission and
                     later recreated without disturbing Artemis's other teams?
Sources checked:     cookbook sections 9.4 and 12; installed
                     sbs_utils/procedural/internal_damage.py; the active Slice 05
                     DAMCON roster query.
What appears documented:
                     DAMCON are named DC1..DC3 grid objects with role `damcons`.
                     The installed library's lethal-damage path uses
                     sbs.delete_grid_object(host, id) followed by Agent.destroyed().
                     grid_restore_damcons(host) recreates missing named teams.
What appears inferred:
                     That the same delete pair is safe when initiated by a MAST
                     Comms action, and that restore completes synchronously enough
                     for an immediate role-index count check.
Risk:                HIGH until live measured: a stale role index could reject a
                     successful transfer, and grid_restore_damcons() is broad—it
                     restores every missing named team, not only the tracked one.
Recommended spike or next action:
                     Live-measure authorize, recall, and repeat JUMP-013 twice.
                     Record the Engineering roster and transfer trace before and
                     after each action; do not promote player guidance from static
                     or compile evidence.
```

## Findings routed to the operator (2026-08-23)

### Verbal Science report was duplicated into the Comms feed

Claim touched: this record's Runtime Flow and Player-Facing Behavior claims that the hail handler should send an `Artemis Science: Sensor Report` before Hessler answers.
Evidence class: observed
Disposition: amended
Owner: operator, for live acceptance that the hail now proceeds directly to Hessler
Dependency: restart Cosmos, hail Halcyon, and inspect the message order

The operator screenshot shows the long Science report duplicated into the Comms archive even though the intended interaction has Science report verbally to the Captain. The hail handler still records `halcyon_scan_observed` as its observable gate but no longer sends a Science message; Captain Aurel Hessler is now the first transmitted response to the hail.

### Dillon incorrectly delivered Halcyon's request for assistance

Claim touched: this record's Runtime Flow and Player-Facing Behavior claims that Dillon's deployment prompt was appropriate after Hessler answered the Halcyon hail; `docs/04_implementation_setup/96_next_session_execution_plan.md` states Hessler should be a lifeform hosted on Halcyon.
Evidence class: observed
Disposition: amended
Owner: operator, for live acceptance of Hessler's identity, badge route, message attribution, and repeat-safe cleanup
Dependency: restart Cosmos, run JUMP-013 twice, hail Halcyon, and request a status update in each run

The operator screenshot shows Commander Dillon delivering the damaged vessel's request immediately after Hessler's hail, placing the instructor in command of a civilian rescue request. Static inspection confirmed there was no Hessler lifeform despite the implementation plan and glossary describing him as one. It also found that Act II objectives inherited the panel's default `Commander Dillon` owner, allowing his badge to repeat Captain-owned orders as instructions. The repair creates Captain Aurel Hessler aboard each Halcyon spawn, removes him through the same deferred cleanup barrier as the ship, routes both the hail response and deployment request through him, converts the raw player status route into a fiction-facing Hessler update, and marks all Act II objectives as `Artemis Captain` owned. During those objectives Dillon's badge offers only an observer assessment.

### Custom Halcyon Science behavior replaced the stock panel and left Comms unknown

Claim touched: this record's superseded Cookbook Patterns and Runtime Flow claims that a custom Science scan route followed by a Comms hail formed a working investigation gate.
Evidence class: observed
Disposition: overturned
Owner: operator, for live acceptance of the stock Science display and repaired hail route
Dependency: restart Cosmos, reach Halcyon, inspect Science, then select and hail Halcyon on Comms twice to promote the repair from observed to measured

The operator screenshots show the exact cookbook 7.1 custom-Science failure signature: a lone `Scan` tab with `no data`, rather than the stock Science display. They also show Halcyon as `unknown` with an empty Comms Options panel, matching cookbook 7.4's early return for an unknown contact. The implementation now removes the custom Science route, writes only the side-specific known-contact scan key, and carries the observable gate through matching Comms companion routes. This conclusion recommends the repair; live acceptance remains the operator's decision.

### Captain-facing report text obscured the stock Science telemetry

Claim touched: this record's cookbook 7.4 implementation claim that seeding Halcyon's known-contact `scan` key preserved a usable standard Science display.
Evidence class: observed
Disposition: amended
Owner: operator, for live acceptance of the shortened scan line on the stock Science panel
Dependency: restart Cosmos, select Halcyon on Science, and confirm the stock range, bearing, shield, and tab information remains legible

The stock tabs returned, but the operator screenshot shows the full Captain-facing sensor report written into the `scan` field and overlapping the engine's target telemetry. The known-contact field now contains only `Vesperan civilian cargo hauler. Distress beacon active.` The detailed condition report remains a separate Science-to-Captain message during the hail sequence, and the on-screen objective is shortened so it does not crowd the Science console.

### JUMP-013 could re-adopt a contact pending deferred deletion

Claim touched: this record's static acceptance claim that JUMP-013 cleanup-before-spawn was sufficient for repeat safety.
Evidence class: static
Disposition: amended
Owner: operator, for live acceptance of repeat execution
Dependency: restart Cosmos and execute JUMP-013 twice while retaining both spawn and cleanup trace groups

The ordering was present but did not wait for `delete_object()` to leave the role index. A second spawn could therefore re-adopt the doomed id, after which the deferred destroy left zero contacts. The repair adds a bounded role-index cleanup barrier, recovers an untracked pre-existing contact for deletion, blocks respawn if cleanup does not settle, and makes JUMP-013 build on JUMP-012's single repeat-safe spawn path. Recommendation: accept only when two executions each leave exactly one contact with a new second-run id and both summaries report `valid_runtime_seed`.

### Away-mission authorization did not reduce the Engineering roster

Claim touched: this record's Runtime Flow claim that setting `damcon_deployed` represented deployment of a DAMCON team from Artemis.
Evidence class: observed
Disposition: amended
Owner: operator, for live-measured acceptance of the grid-object transfer and restoration lifecycle
Dependency: restart Cosmos; record DAMCON roster counts before authorization, after authorization, after recall, and after two repeated JUMP-013 executions

The operator observed that authorizing the engineering detachment left all DAMCON teams available aboard Artemis. Static inspection confirmed the handler changed only shared story flags. The repair now removes one actual team—DC3 when present—using the installed library's own grid-delete/agent-cleanup shape, removes its old-style rally marker when present, and advances the story only after the `damcons` role count falls by exactly one. Recall and the shared Act II jump reset restore and verify the tracked team before clearing deployment state. This is an implementation recommendation backed by installed source and compile preflight; the Engineering UI result remains live-unproven.

### Away-team complement expanded from fixed Engineering to a Comms-selected roster

Claim touched: `docs/01_design/00_scenario_play_guide.md`, Scene 8, states that the Engineering player deploys with DAMCON Team Reyes and does not define a selectable second officer.
Evidence class: asserted
Disposition: amended
Owner: operator, to reconcile the canonical Scene 8/9 roster and downstream station assumptions after live acceptance
Dependency: live-test the Comms selection flow and decide whether optional-officer absence from Artemis has later qualification or staffing consequences

The operator directed Hessler to request the full away-team complement and required Comms to select one or two officers in addition to DAMCON. Runtime implementation preserves Engineering as mandatory because Scene 9's repair conversation and Slice 09's timer branch require `engineering_placement = aboard_halcyon`; Comms may add the Captain, Science, Weapons, Helm, or Comms. If the Captain goes, transmission is blocked until Comms designates a remaining officer as acting command, and the bridge objective transfers to that command role. Static inspection found no future slice gate that reads Captain location; the downstream mechanical inputs are Engineering placement, cascade state, and elapsed time. This creates a player-facing choice not yet represented in the protected design documents. No design/content file was edited by implementation.

## Next Action

Operator live smoke, in this order:

1. **Run JUMP-013 twice.** Count Halcyon contacts. Two or more = stop; the cleanup helper is wrong and four later slices depend on it.
2. Select Halcyon on Science → does the normal multi-band display remain visible, with no custom one-tab `Scan` / `no data` panel?
3. After Science reports verbally, select Halcyon on Comms → does `Hail Halcyon Drift` render under a known Halcyon sender? `unknown` or an empty panel = FAIL.
4. Hail → does it proceed directly to two messages headed `Captain Aurel Hessler: Halcyon Drift`, with no Science or Dillon message? Does `Request Status Update` also answer as Hessler?
5. On Comms, select Engineering alone and transmit. Hessler must repeat DAMCON Team Reyes plus Engineering and say Halcyon is standing by; authorization must then appear. Revise and test an ordinary second officer; Hessler must name that officer. Revise again, select Captain, and confirm transmission remains hidden until an acting commander is designated. After designation Hessler must name both Captain and acting command. A third away officer must never be selectable, and removing Engineering must hide transmission.
6. Before authorization, record the Engineering roster (normally DC1/DC2/DC3). Authorize → exactly one team, preferably DC3, disappears and the trace reports `before=3 after=2`. Recall → the same named team returns and the trace reports `before=2 after=3`. Run JUMP-013 twice after a deployment; each jump must leave the full starting roster with no cumulative loss or extra teams.

---

# Live smoke log (append-only)

_No live run yet._
