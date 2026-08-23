# Slice 07B Verification — Halcyon Drift arrival

Goal: Halcyon Drift exists as a scannable, hailable contact; Engineering and DAMCON deployment state is tracked; arrival checkpoint persists.

## Status

live-proven — reviewer closure directed by the operator on 2026-08-23 after the listed use cases were exercised repeatedly across multiple play-test sessions. The earlier PARTIAL entry remains in the append-only log; the closure entry records the later evidence.

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
- section 6.1 `[LIVE]` — matching `//enable/comms` and `//comms` companions gated on Halcyon's selected role; lifeform-backed replies explicitly `comms_navigate("//comms")` to rebuild that root after their sender overrides finish.
- section 7.4 `[LIVE]` / preference 3 `[UNPROVEN]` in the cookbook — an unknown contact gets no Comms buttons, so both new-contact and reuse paths refresh only Halcyon's side-specific `scan` key and leave the stock `scan_type_list` untouched. This slice's repeated play tests locally promote the applied route to live-measured evidence; they do not change the cookbook-wide tag.
- section 8.2 `[LIVE]` — Halcyon carries only Khovan roles, no stock `station` role, so no stock panel competes for the option list.
- section 5.2 `[LIVE]` — n/a here; no polling observer in this slice.
- section 9.4 `[COMPILE]` plus section 12 uncertainty handling — the installed library exposes `grid_restore_damcons()` but no away-team abstraction. The detachment follows the library's own grid-object deletion shape; repeated authorize/recall/jump use cases now supply live-measured evidence for this slice.

## Files Touched

- `scripts/lib/entity_cleanup_helpers.mast` (new — first file in `scripts/lib/`)
- `scripts/acts/act2_halcyon_arrival.mast` (new)
- `scripts/main.mast` (imports + init)
- `scripts/systems/story_jump_presets.mast` (the former JUMP-013 Halcyon-arrival preset was later retired; JUMP-012 now owns the complete arrival checkpoint)
- `tests/test_act2_halcyon_arrival_static.py` (new)
- `run_tests.py`

## State Variables

`halcyon_arrival_initialized`, `halcyon_spawned`, `halcyon_object_id`, `halcyon_navproxy_id`, `halcyon_spawn_count`, `halcyon_cleanup_count`, `halcyon_cleanup_in_progress`, `halcyon_destruction_source`, `halcyon_scan_observed`, `halcyon_hail_observed`, `halcyon_arrival_status`, `halcyon_contact_fallback_available`, `engineering_deployed`, `engineering_deploy_status`, `engineering_placement`, `damcon_deployed`, `damcon_deploy_status`, `halcyon_deploy_acknowledgement_sent`, the `halcyon_manifest_*` selection/count/summary fields, and the `halcyon_damcon_*` team identity/count/transfer fields, plus the player-facing `*_text` variables.

`engineering_placement` takes exactly `aboard_halcyon` or `returned_to_artemis`, the strings the packet pins, because **Slice 09 reads this to choose the extended (30 min) or compressed (15 min) DAMCON window.**

The packet flags `damcon_deployed` / `damcon_deploy_status` as a collision hazard against Slice 05's `damcon_rest_*`/`damcon_meal_*` and Slice 09's `damcon_timer_*`. The duplicate-shared check in `run_tests.py` passes.

## Runtime Flow

1. `khovan_act2_initialize_halcyon_arrival` runs from `main.mast` after the Act II pivot init.
2. `khovan_halcyon_spawn` places Halcyon 12 km ahead and 4 km off Artemis, registers object and navproxy ids, refreshes the player-side known-contact key on both new and reused contacts, creates Captain Aurel Hessler as a lifeform hosted aboard Halcyon, and writes `post_halcyon_arrival`.
3. Science uses the stock sensor display and reports Halcyon's identity and condition verbally to the Captain; no automatic Science Comms message is generated.
4. The Captain orders Comms to select Halcyon and hail; the hail handler records `halcyon_scan_observed` and `halcyon_hail_observed`. Hessler answers and asks Artemis to transmit an away-team complement consisting of the required DAMCON team and one or two officers, including Engineering. Dillon then addresses only the Captain with protocol: Comms assembles the manifest, Engineering is required by the repair, one additional officer is discretionary, and DAMCON Team Reyes consists of Reyes, Park, and Achebe. Dillon also states that a Captain joining the away team must designate acting command aboard Artemis. After the lifeform-backed replies, the handler explicitly rebuilds Halcyon's selected root route so the manifest action replaces the completed hail action.
5. Comms selects Engineering and optionally the Captain, Science, Weapons, Helm, or Comms as the second officer. Add/remove controls enforce a maximum of two; transmission is unavailable until Engineering is selected. If the Captain is selected, Comms must designate a remaining Science, Weapons, Helm, or Comms officer as acting command before transmission becomes available. The final control explicitly says `Transmit Manifest & Authorize Departure`, and Dillon's protocol copy warns that transmission immediately sends the declared officers and DAMCON team off Artemis.
6. Transmitting the manifest is the Captain's departure authorization → the runtime selects DC3 when available, removes that real grid team and any old-style rally marker from Artemis, verifies the `damcons` roster fell by exactly one, then sets `engineering_placement = aboard_halcyon` and `damcon_deployed`. Hessler acknowledges the manifest only after the transfer succeeds. A failed reduction blocks the away-mission transition, exposes fallback status, and leaves a `Retry Away-Team Departure` Comms action.
7. Optional recall → `grid_restore_damcons(artemis_id)` recreates the tracked named team, the runtime verifies the roster rose by exactly one, then sets `engineering_placement = returned_to_artemis`. The shared Act II reset path performs the same restoration before JUMP-011/012 cleanup can clear deployment state.

## GM Controls

JUMP-012 Distress Localized is the Test-Mode-gated Halcyon arrival checkpoint. It runs the shared Act II reset and cleanup barrier before rebuilding the contact, and repeated execution must leave exactly one Halcyon at the guarded approach. The redundant former JUMP-013 Halcyon Arrival preset is absent; Slice 08 may reuse the free number for a distinct boundary.

## Player-Facing Behavior

Hessler's hail reply, Hessler's request for the away-team complement, his post-transfer acknowledgement naming the transmitted roster and any acting commander, and fiction-facing Hessler status updates. Science reports verbally to the Captain and does not generate a Comms message. Dillon does not speak for Halcyon or lead the rescue; he states manifest and command-transfer protocol to the Captain, including that transmitting the manifest is the departure authorization. Comms performs the actual one-or-two-officer selection and acting-command designation, and the final action is labeled `Transmit Manifest & Authorize Departure`. If the Captain deploys, the post-transfer objective addresses Artemis Acting Command instead. All written messages follow the addressee convention; `tests/test_mission_text_contract.py` enforces it.

## Tests/Static Checks

`tests/test_act2_halcyon_arrival_static.py` — 48 checks. The load-bearing ones:

- **Helper owns no shared state.** Parses the lib file and asserts zero `shared` declarations. Slice 11 needs this routine for two pirates at once; state would make it a singleton.
- **Cleanup does not clear its own flag.** Asserts `halcyon_cleanup_in_progress = False` is *absent* from the cleanup routine, because the deferred destroy handler owns the clear. This is the exact bug fixed live on 2026-08-08.
- **Selections cleared before deletion**, ordered.
- **JUMP-012 uses the repeat-safe reset and guarded approach**, with the retired Halcyon-arrival construct absent and JUMP-013's number free for a distinct future preset.
- **Comms block opens with a statement**, not an option line — the Kestrel failure shape.
- **Halcyon Comms survives reuse and lifeform replies.** Asserts both spawn branches refresh the known-contact key and hail/status replies navigate back to the selected Halcyon root after sender overrides.
- **DAMCON departure is a grid mutation, not a story-only flag.** Asserts the authorization calls the detach routine before advancing, DC3 is preferred, the library's grid-delete/agent-cleanup pair is used, and exactly-one count verification is present.
- **Manifest transmission performs departure authorization.** Asserts the transmit handler awaits the authorization routine, requires successful deployment before Hessler acknowledges receipt, and no longer posts a second authorization objective.
- **Recall and jumps cannot forget the team.** Asserts recall and the common Act II reset restore the named team before advancing or cleaning up, and block if verification fails.

`python run_tests.py quick`: PASS, 313 checks (12 harness, 301 Python tests), 0 failures, 0 warnings, compile preflight included. `tools/review_gate.py --base master`: MECHANIZED PASS.

## Acceptance Covered

Statically: idempotent spawn, cleanup ordering, scan and hail flags, a one-team DAMCON grid reduction before deployment state advances, tracked-team restoration before recall/jump state advances, `engineering_placement` set and readable, checkpoint written, and JUMP-012's guarded repeat-safe arrival path.

Live measured by operator report across repeated play-test sessions: repeat JUMP-012 contact/range/reset behavior; stock Science display; known Halcyon Comms route; Hessler hail and status responses; manifest add/remove/revise, officer-limit, Captain/acting-command, and transmission gating cases; departure authorization; exactly-one DAMCON removal; recall; and full-roster restoration on later jumps.

## Acceptance Not Covered

No in-scope Slice 07B acceptance item remains uncovered.

Evidence provenance limitation: the closure is an operator attestation covering many play-test sessions, not a retained trace, screenshot set, build-version ledger, or reviewer-witnessed single run. That limits later forensic reconstruction but does not leave the repeatedly exercised acceptance cases open.

Intentional boundaries, not missing acceptance: selected bridge officers leave through story state rather than console reassignment, and Captain decisions from Halcyon are narrative relocation rather than a separate downstream runtime branch. The `tsn_warpster` hull remains a cosmetic placeholder tracked under Known Risks.

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

**Resolution, 2026-08-23 — live measured.** The operator reports exercising authorization, recall, subsequent story-jump restoration, and the other listed use cases repeatedly across many play tests. The roster fell by exactly one on departure, restored on recall/reset, and did not accumulate loss across the tested cases. The uncertainty block remains above as the pre-test record; its HIGH-until-measured condition is now satisfied for this slice.

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

### Non-ASCII punctuation corrupted Dillon's manifest protocol

Claim touched: the cookbook known-bad rule at section 11 states that player-facing text must use ASCII and no dash punctuation, guarded by `test_player_facing_text_is_ascii_and_uses_no_dash_punctuation`.
Evidence class: observed
Disposition: confirmed
Owner: operator, for live acceptance of the repaired Dillon message
Dependency: restart Cosmos, hail Halcyon, and inspect the full Dillon protocol line through the DAMCON names

The operator screenshot shows the Comms renderer turning the em dashes around `Reyes, Park, and Achebe` into multiple lines of garbage characters. The existing regression named by the cookbook inspected only the Act I drone file, so it did not protect new copy elsewhere in the mission. Dillon's line now uses two ASCII sentences, and the shared mission-text contract now checks every runtime `*_text` variable for ASCII and forbidden dash punctuation.

### In-place manifest option mutation preceded an engine space-object assertion

Claim touched: this record's Player-Facing Behavior claim that Comms could repeatedly select and remove away-team members safely on Halcyon's target-selected route.
Evidence class: observed
Disposition: amended
Owner: operator, for live-measured acceptance of repeated selection and removal
Dependency: restart Cosmos and complete the add/remove sequence below twice without an assertion or stale menu

The operator screenshot records Artemis' `MissionScript.cpp` line 785 assertion `VALID_SPACE_OBJ(ID)` while Comms was selecting and deselecting crew. The live trace shows repeated evaluation of Halcyon's custom Comms route, no manifest transmission, and no deployment, so the failure occurred during roster editing rather than Hessler messaging or DAMCON transfer. The prior handlers changed which buttons were visible but did not return the Comms promise to a named route. The repair places roster controls in `//comms/khovan_halcyon_manifest`, explicitly refreshes that submenu after every add, remove, and acting-command action, and returns to the Halcyon root after transmission. Per-action trace breadcrumbs now identify the last completed click if the assertion recurs. This is a cookbook-shaped repair, but the exact engine-side invalid ID remains unproven until the same toggle sequence succeeds twice.

### JUMP-013 left Artemis at Tarsis instead of staging the Halcyon arrival

Claim touched: this record's Runtime Flow claim that JUMP-013 seeds a playable Scene 8 Halcyon-arrival checkpoint.
Evidence class: observed
Disposition: amended
Owner: operator, for live-measured acceptance of the repeat-safe approach placement
Dependency: restart Cosmos and execute JUMP-013 twice, checking the Artemis-to-Halcyon range after each execution

The operator screenshot shows Halcyon spawned at the fixed distress point while Artemis remains beside Tarsis, approximately 95 km away. Static inspection confirmed JUMP-013 validated the contact and scene but never changed or checked the player ship's position. The repair uses the same guarded direct `Vec3` position assignment already observed in the Kestrel mechanical hold, clears stale docking state, sets throttle to zero, and places Artemis five kilometres short of Halcyon. The seed now blocks and reports a failed validation if either object is missing or the resulting range is outside 4.5-5.5 km. This recommends a collision-safe approach point rather than overlapping the two ships.

### Repeat Act II jump passed a lifeform Agent to the space-object deletion API

Claim touched: this record's Runtime Flow and cleanup claims that JUMP-012/JUMP-013 can remove an existing Hessler lifeform and Halcyon contact repeat-safely.
Evidence class: observed
Disposition: amended
Owner: operator, for live-measured acceptance of repeated JUMP-012/JUMP-013 teardown
Dependency: restart Cosmos, execute JUMP-013 followed by JUMP-012 twice, and retain the lifeform-cleanup and Halcyon-cleanup trace groups

The append-only trace ends after Act I timer invalidation on the failing JUMP-012, before any Hessler or Halcyon cleanup breadcrumb. The previous run had created Hessler with story-Agent id `36028797018964722`; cleanup then called `sbs.delete_object()` with that id. Installed `lifeform_spawn()` constructs a plain Python `Agent`, while `sbs.delete_object()` accepts SBS space-object ids and asserts `VALID_SPACE_OBJ(ID)` otherwise. The repair reverses `lifeform_init()` wiring by removing the badge path and transferring Hessler off Halcyon, then calls `Agent.destroyed()` and never invokes the space-object deletion API. Three breadcrumbs bracket those lifecycle steps. The trace/source pairing strongly identifies the crash cause; repeat live execution remains required to promote the repair to measured.

### Consecutive JUMP-012 then JUMP-013 redundantly rebuilt the same Halcyon state

Claim touched: this record's Runtime Flow claim that adjacent Act II presets can be executed consecutively without crashing or destroying a valid arrival state.
Evidence class: observed
Disposition: amended
Owner: operator, for live-measured acceptance of in-place JUMP-012 to JUMP-013 promotion
Dependency: restart Cosmos and execute JUMP-012 followed by JUMP-013 twice, retaining both JUMP-013 PROMOTE trace groups

The operator reports another server crash after executing JUMP-013 immediately after JUMP-012. The append-only trace shows JUMP-012 had created Hessler and Halcyon successfully. JUMP-013 then unconditionally called the complete JUMP-012 seed again, moved Artemis back through the Act I/Tarsis setup, and stopped after Act I timer invalidation before the Halcyon cleanup barrier could report. JUMP-013 now recognizes a localized, spawned, correctly positioned JUMP-012 state and promotes it in place, preserving that Halcyon/Hessler pair. Direct JUMP-013 still builds JUMP-012 when the prerequisite state is absent. This removes the unnecessary teardown from the observed failing sequence; repeat live execution remains required.

### JUMP-013 retired because JUMP-012 now owns the complete Halcyon arrival checkpoint

Claim touched: this record's Jump Preset and Runtime Flow claims that a separate JUMP-013 Halcyon Arrival preset remains necessary after JUMP-012.
Evidence class: static
Disposition: amended
Owner: operator, for the corresponding canonical admin-plan update
Dependency: none

The operator decided that JUMP-013 is redundant now that JUMP-012 localizes the distress signal, spawns Halcyon, and places Artemis at the guarded five-kilometre approach. Runtime implementation removes JUMP-013 from the GM menu, registry record, dispatcher, relocation state, and Halcyon seed handlers. JUMP-012 is the sole GM arrival checkpoint and the sole fallback named by Halcyon's bounded observers. Historical JUMP-013 findings above remain readable as the evidence trail that led to this decision.

**The specific admin-plan update this finding calls for:** `docs/01_design/40_admin_testing_plan.md` section 6.2 still assigns `JUMP-013 halcyon_arrival` and `JUMP-014 away_mission_start` in its canonical jump list. The operator has separately directed that a new preset claim the number 013 rather than skip to 014, so section 6.2's row for 013 needs a new `jump_id` and 014 should be confirmed to still mean `away_mission_start` (i.e., not renumbered) once the new preset's purpose is decided. A guarded placeholder (`tests/test_story_jump_presets_static.py::test_jump_013_number_is_free_for_reissue`) starts failing the moment any preset registers `JUMP-013` again, so this is enforced rather than a note that can be missed.

### Halcyon Comms route disappeared across a contact/reply lifecycle transition

Claim touched: this record's Runtime Flow and Player-Facing Behavior claims that selecting a known Halcyon keeps the target-selected Comms route usable through hail, status replies, and contact reuse.
Evidence class: observed
Disposition: amended
Owner: operator, for repeat live verification and any resulting evidence promotion
Dependency: restart Cosmos; reach Halcyon once through a new spawn and once through repeated JUMP-012, then hail and request status twice on each contact

The operator reported losing the Halcyon Comms route. Static inspection found two routes to that symptom: the existing-contact branch returned without refreshing the player-side known-contact key, while the hail and status handlers completed lifeform sender overrides without explicitly rebuilding Halcyon's selected root. The scoped repair applies cookbook 7.4 preference 3 `[UNPROVEN]` to both new and reused contacts and cookbook 6.1 `[LIVE]` `comms_navigate("//comms")` after the lifeform-backed replies. This recommends the smallest repair supported by the evidence; it does not claim the panel is fixed live. Repeat the working sequence twice before promoting it from observed to measured.

## Next Action

Slice 07B is closed. Merge the reconciled Slice 08 packet through the docs/governance branch, return to clean `master`, then open the Slice 08 implementation branch. The next live acceptance work belongs to Slice 08; do not repeat Slice 07B merely to recreate evidence already supplied by the operator.

---

### Status-string convention has a write side and no read side

Claim touched: `AGENTS.md` section 4, "Set a status string on every branch, including failure branches - the GM overview reads them."
Evidence class: static
Disposition: amended
Owner: operator - approved 2026-08-23; implementation to follow in a scoped cleanup
Dependency: none

Static analysis of the compiled mission counts 74 `*_status` shared variables. The GM overview
(`khovan_scenario_control_panel_update_overview`) reads 4 of them. The remaining 70 are written and
read by nobody, in any file, by any expression or route condition.

The second half of the section 4 sentence was never built. 123 labels set a `*_status` variable and
also write a startup trace in the same label, recording the same event twice - once into a shared
variable that is overwritten and never read, and once into the append-only trace, which carries a
timestamp and keeps history. The mission already contains 447 trace calls, so the diagnostic channel
the status variables were standing in for exists and is in active use.

Amended convention, approved: `*_status` means GM-contract state and must appear in the overview.
Everything else records through `script.write_khovan_startup_trace(...)` and holds no shared
variable. This is the root cause of 114 write-only-state findings and most of 100 branch-records-no-
outcome findings; both classes disappear when the convention states what it actually requires.

Superseded claim retained above per cookbook 17.11: the section 4 sentence stands as written in
`AGENTS.md` until the operator edits it, and this finding is the record of why it is wrong.

#### Correction, same day: the count was wrong by a factor of nearly four

**Evidence class: static (re-measured with a corrected instrument).**
**Disposition: amended. The finding above is retained verbatim per cookbook 17.11.**

**What was claimed above.** "The remaining 70 are written and read by nobody, in any
file, by any expression or route condition."

**What is actually true.** Of 70 `*_status` variables declared:

| read by | count |
|---|---|
| the GM overview | 4 |
| some other expression in MAST | 15 |
| the static test suite or docs | 48 |
| `{}` interpolation, including `% {var}` GUI bodies | 10 |
| **seen by at least one of the above** | **51** |
| **genuinely read by nobody** | **19** |

Nineteen, not seventy. The specific phrase "in any file" was the false part, and it
was checkable at the time.

**Why the original was wrong.** It was measured with masttools before that tool
counted two whole classes of reader: the mission's own static tests, and `{}`
interpolation in MAST text - the latter invisible to any AST query because the
compiler emits no node for a GUI body (cookbook 17.13). The number was not a
guess; it was a real measurement taken with an instrument that could not see
half the read surface, and reported as fact without that caveat. The tool has
since been fixed and re-measured.

**Corrected knock-on numbers.** The write-only-state class is 38 findings, not
114; 19 of those 38 are `*_status`. The branch-records-no-outcome class is 103,
and the claim that this convention is "the root cause of most" of it is now
unproven - it was inferred from the inflated figure and has not been separately
established.

**What still stands.** The GM overview does read only 4 of 70, and 122 labels do
set a `*_status` while also writing a trace in the same label, against 436 trace
calls mission-wide. The duplication is real and the amended convention approved
above is unaffected.

**What changes.** The de facto reader of `*_status` is the static test suite, not
the GM overview - 48 against 4. Anything acting on this finding must treat the
tests as a consumer, or the cleanup breaks them, which is exactly what happened
once already this session.

### Player-facing sends have six entry points and no shared suppression

Claim touched: `AGENTS.md` section 4, "Duplicate-suppress every player-facing message."
Evidence class: static
Disposition: unproven
Owner: operator - decision deferred, not yet approved for implementation
Dependency: a decision on whether to unify the send path before further Act II content

Six labels wrap message delivery (`khovan_lifeform_send`, `khovan_reach_send_safe_startup_message`,
`khovan_engineering_send_message`, `khovan_drone_contact_fire_send_message`, and two beat-specific
senders), and a further 33 labels call `comms_receive` directly without going through any of them.
Because there is no single send path, suppression cannot be centralised, so each beat maintains its
own flag - 24 `*_sent` variables at present.

A single `khovan_send(message_id, ...)` owning suppression by message id would remove those flags and
the 27 unsuppressed-send findings with them. It touches 39 call sites and is a refactor, not a
cleanup, so it is recorded here as a tradeoff rather than a recommendation. The decision is the
operator's.

**Re-verified 2026-08-23 with the corrected tool** (see the correction to the
finding above): 6 send wrappers exactly as stated; direct `comms_receive`
callers 32 rather than 33, unsuppressed-send findings 26 rather than 27, and
`*_sent` flags 22 rather than 24. The drift is from declarations commented out
elsewhere in this same session, not from the measurement fault that inflated the
status-variable finding. The conclusion is unchanged.

### A declaration-pruning pass removed a live GUI-body variable

Claim touched: commit `38602d2` treated the masttools MAST019 "unused record" verdict as sufficient grounds to comment out 32 `shared` declarations across the runtime files.
Evidence class: static
Disposition: confirmed
Owner: operator, for live acceptance that the pre-clearance Tarsis docking rejection renders its message
Dependency: restart Cosmos, approach Tarsis within docking range before requesting clearance, and read the "Docking Clearance Required" body

Thirty-one of the 32 were genuinely unused. `tarsis_docking_rejection_text` was not: `scripts/acts/act1_generator_tarsis_gate.mast` still reads it as `% {tarsis_docking_rejection_text}` inside the `khovan_tarsis_docking_rejected_before_clearance` GUI body. MAST019 counts expression-position references and does not count `% {var}` substitution, so the only use site was invisible to it. Compile preflight does not close this class either, because an undefined name in a GUI body faults at render rather than at parse. The declaration is restored, and `tests/test_mast_compile_or_preflight.py::test_gui_body_interpolation_never_references_an_undeclared_shared` now fails on any `% {name}` with no `shared` declaration behind it; the negative control was re-applying the original comment, which the new test rejects. Cookbook 17.13 records the rule.

### A backward-jump reset could publish a previous jump's barrier result

Claim touched: this record's repeat-safety claims for the Act II jumps, which rest on `halcyon_cleanup_barrier_status` reporting whether the Halcyon cleanup barrier settled for the jump being executed.
Evidence class: static
Disposition: amended
Owner: operator, for live-measured acceptance of a blocked jump reporting a failed validation rather than a false success
Dependency: restart Cosmos, deploy the away team, force a DAMCON restore failure, then execute JUMP-011 or JUMP-012 and confirm the summary reports a blocked jump

`khovan_halcyon_reset_for_act2_jump` restores a deployed DAMCON team before running its cleanup barrier and bails if that restore fails. On that bail path the barrier never ran, so `halcyon_cleanup_barrier_status` retained whatever the previous jump left, including `"settled"`. Both guards in `scripts/acts/act2_pivot.mast` test that exact string, so a jump could proceed on evidence produced by a different jump. The repair resets the flag to `"not_run"` as the first statement of the label, before any path that can bail. `tests/test_mast_compile_or_preflight.py::test_act2_jump_reset_clears_its_barrier_before_it_can_bail` guards both the presence and the ordering; the negative control moved the reset below the first bail and the test rejected it. Cookbook 5.2 now carries the general rule.

### JUMP-013 promotion skipped the reset chain its seed call owned - superseded

Claim touched: commit `38602d2`'s JUMP-013 promote-in-place branch, which reused a valid JUMP-012 state instead of re-running that seed.
Evidence class: static
Disposition: overturned
Owner: operator - already actioned in this session by a parallel thread; recorded for the trail
Dependency: none

`khovan_act2_story_jump_seed_distress_localized` was the only path to `khovan_act2_story_jump_reset_act2_base` and from there to `khovan_halcyon_reset_for_act2_jump`, so skipping the seed skipped a reset two calls deep. JUMP-013 after a played JUMP-012 retained hail, manifest, and deployment state and left Artemis one DAMCON team short, while the GM panel reported `valid_runtime_seed` on a `halcyon_cleanup_barrier_status` written by the earlier jump. The branch also gated on a flag only the skipped path cleared, so no later JUMP-013 could take the rebuild path again. This was first patched by re-applying the resets inline; that patch was then superseded by deleting JUMP-013 outright, since JUMP-012 already spawns Halcyon and stages the same five-kilometre approach. `scripts/` now holds no `jump_013` reference. No regression test is proposed: the defective construct no longer exists, and a general "promotion must re-apply the skipped chain" check would be a cry-wolf pattern of the kind cookbook 17.6 warns against. The rule is recorded as cookbook 17.12/17.12.1 instead.


# Live smoke log (append-only)

### LIVE SMOKE 2026-08-23
branch: codex/captain-directed-anderson-copy
commit: uncommitted (tree at 38602d2 plus local session changes)
build: Cosmos <version not reported>
result: PARTIAL

Reported by the operator in chat during this session, not transcribed from a saved trace file or screenshot. This is weaker provenance than a reviewer-witnessed run — record it as such, do not requote it later as trace-verified. `trace_marker_last` is unknown for the same reason: no trace file was shared alongside the report.

checks:
- NEXT-ACTION-1: NOT RUN   JUMP-012 executed twice, JUMP-013 absent from GM tree, Halcyon contact count, Artemis-to-Halcyon range — operator did not report this item
- NEXT-ACTION-2: PASS      Halcyon on Science shows the normal multi-band display, no custom one-tab Scan/no data panel
- NEXT-ACTION-3: PASS      Halcyon on Comms renders "Hail Halcyon Drift" under a known sender
- NEXT-ACTION-4: PASS      Hail proceeds directly to Hessler; Request Status Update also answers as Hessler
- NEXT-ACTION-5: PASS      Manifest add/remove/revise/acting-command flow, reported generally as "works fine" - operator did not confirm each of the sub-cases listed in item 5 individually (repeat cycle twice, third-officer rejection, revise-after-Captain-designation)
- NEXT-ACTION-6: PASS      DAMCON before/after counts on authorize and recall

trace_marker_last: unknown - not reported
blocker: NEXT-ACTION-1 not yet run; this is the item that exercises both this session's fixes (the 5.2 barrier-reset fail-closed change and the JUMP-013 removal) under live Cosmos
next action: run NEXT-ACTION-1; if it passes, Part 1 `Status` and `Acceptance Not Covered` are reviewer fields per handoff protocol 4.3 and still need reviewer sign-off before this slice is fully closed, independent of this log

### LIVE SMOKE 2026-08-23 — closure
branch: multiple operator play-test sessions; final Slice 07 runtime merged to master
commit: final merged runtime at 6e3b56b (individual play-test commits not reported)
build: Cosmos <versions not retained in this record>
result: PASS

Reported by the operator after the earlier PARTIAL block: all listed use cases were run over many play tests. This is repeat evidence and therefore measured for acceptance, while its provenance remains operator-attested rather than trace- or screenshot-verified.

checks:
- NEXT-ACTION-1: PASS      repeated JUMP-012 leaves JUMP-013 absent, exactly one Halcyon at the guarded approach, and restores the full DAMCON roster after deployment
- NEXT-ACTION-2: PASS      stock multi-band Science display remains usable
- NEXT-ACTION-3: PASS      known Halcyon sender and hail route remain available
- NEXT-ACTION-4: PASS      Hessler hail and status routes remain available across the exercised contact lifecycles
- NEXT-ACTION-5: PASS      repeated manifest selection, removal, revision, officer limit, Captain/acting-command, and transmission-gating cases
- NEXT-ACTION-6: PASS      authorization removes exactly one tracked DAMCON team; recall and later jumps restore it without cumulative loss

trace_marker_last: unknown — no single retained trace represents the many play-test sessions
blocker: none
next action: Slice 08 implementation from clean master after the reconciled packet merges
