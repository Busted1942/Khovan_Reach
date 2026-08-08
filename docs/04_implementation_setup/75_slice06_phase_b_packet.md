# KHOVAN REACH — SLICE 06 PHASE B PACKET

Status: approved implementation packet — revised during Phase B build
Purpose: build the production Drone 01 controlled-disable and Drone 02 live-fire sequence only after the accepted Phase A API spike.

This is build-side elaboration of canonical Slice 06. It does not change scenario design. Where it conflicts with a design source, implementation must stop and raise the finding rather than resolve it in code.

```text
Slice ID:            06B

Goal:                Add the actual Act I drill beside the accepted Phase A target spike:
                     Drone 01 is a passive controlled-disable target whose Weapons subsystem
                     completes only after three confirmed manual subsystem hits and a ceasefire;
                     Drone 02 is a low-pressure live-fire target that completes on destruction.
                     Then deliver the cultural Comms packet and set an explicit Act-II-ready
                     marker for Slice 07 to consume. This packet adopts the explicit source decision recorded in
                     tests/SLICE06_VERIFICATION.md: Drone 01 proves Weapons subsystem disable;
                     Drone 02 completes on destruction.

Source docs:         docs/01_design/50_implementation_slice_plan.md, §2 and Slice 06
                     docs/01_design/00_scenario_play_guide.md, Scenes 4A, 5A, and 6A
                     docs/01_design/10_mast_requirements.md, §7 scene ownership matrix and
                     §§8.5-8.7
                     docs/01_design/30_qualification_cards.md, Act I station observations and
                     forked-profile rule at lines 419-421
                     docs/01_design/40_admin_testing_plan.md, ACT1-019 through ACT1-024
                     docs/04_implementation_setup/60_mast_api_cookbook.md, §§5, 6, 8, and 12
                     tests/SLICE06_VERIFICATION.md, Status, Known Risks/API Uncertainties, and
                     Live Smoke Log (Phase A accepted evidence and source decision)

Files to modify:     scripts/acts/act1_drone_contact_fire.mast
                     tests/test_act1_drone_contact_fire_static.py
                     tests/SLICE06_VERIFICATION.md
                     tests/test_coverage_matrix.md
                     run_tests.py only if the existing test-discovery path cannot run the updated
                     static test; otherwise do not modify it.

Runtime owner model: scripts/acts/act1_drone_contact_fire.mast exclusively owns all Slice 06
                     entity IDs, spawn/reset/cleanup, Drone 01 gates, Drone 02 destruction,
                     drill status, and Drill-to-Act-II handoff request. It consumes the existing
                     khovan_set_current_objective() service in
                     scripts/systems/current_objective_panel.mast for all player-facing objective
                     updates; it does not own that service or its shared state. Existing
                     scripts/systems/scenario_control_panel.mast remains GM navigation/overview
                     owner. Existing story-jump code is not changed by this packet.

State variables needed:
                     All names below were checked against every current `shared` declaration in
                     scripts/ and the current test tree; none exists at packet time. Phase A
                     drone_target_spike_* names remain spike-only and are not reused as production
                     state.

                     drone_01_active
                     drone_01_target_id
                     drone_01_navproxy_id
                     drone_01_spawn_count
                     drone_01_reset_count
                     drone_01_reset_reason
                     drone_01_status
                     drone_01_scan_complete
                     drone_01_hail_complete
                     drone_01_shield_frequency_relay_complete
                     drone_01_weapons_lock_active
                     drone_01_range_band_active
                     drone_01_stationary_hold_active
                     drone_01_stationary_hold_run_id
                     drone_01_stationary_hold_seconds
                     drone_01_fire_authorized
                     drone_01_manual_system
                     drone_01_weapons_hit_count
                     drone_01_weapons_disabled
                     drone_01_ceasefire_confirmed
                     drone_01_destroyed_in_error
                     drone_01_cleanup_in_progress
                     drone_01_fallback_available
                     drone_01_fallback_reason

                     drone_02_active
                     drone_02_target_id
                     drone_02_navproxy_id
                     drone_02_status
                     drone_02_destroyed
                     drone_02_cleanup_in_progress
                     drone_02_fallback_available
                     drone_02_fallback_reason

                     drone_contact_cultural_packet_sent
                     drone_contact_act2_handoff_status

Branch type:         implementation

Starting branch:     slice06-drone-contact-fire at d4138e2. `.claude/settings.local.json` is
                     deliberately ignored by .gitignore and is not part of this packet commit.

Expected return branch:
                     slice06-drone-contact-fire

Branch lifecycle plan:
                     1. Review and approve this packet before any runtime edit.
                     2. Confirm `git status --short --branch`, `git log --oneline -5`, and
                        `python run_tests.py quick` before implementation.
                     3. Implement only the listed files, run quick and `git diff --check`, and
                        update the verification record's static sections.
                     4. Commit intentionally on this branch. Do not merge or switch branches
                        during this packet without the branch-transition checks in AGENTS.md §7.
                     5. Request a live Cosmos smoke with the required observations below; append
                        its dated result to the verification record. Do not call Phase B complete
                        on static or compile evidence alone.

Runtime/live-smoke allowed from this branch:
                     yes — after packet review, clean implementation diff, and passing quick
                     checks. Live smoke is required for acceptance but remains operator-run.

Merge-back required: no separate docs/governance branch is planned. The implementation branch
                     remains the return branch; any later merge target requires operator direction.

Implementation tasks:
                     1. Preserve Phase A evidence and its GM test route, but explicitly separate
                        it from production state. Replace the spike's player-visible Science and
                        Comms instrumentation strings before any equivalent text is presented by
                        Drone 01/02. Do not reuse phrases asking players to observe API behavior.
                     2. Add production initialization, state reset, existence checks, navproxy
                        cleanup, and run-ID invalidation for Drone 01 and Drone 02. A cleanup
                        deletion must be marked before delete_object() and consumed by its deferred
                        destroy hook, using the Phase A live-proven guard pattern.
                     3. Spawn Drone 01 as a normal enemy object near the Tarsis Training Beacon,
                        with non-attacking/training-safe behavior. Route its player instructions
                        through khovan_set_current_objective() so the proven objective broadcast,
                        not GM-only comms_receive(), carries player-facing progress.
                     4. Implement the Drone 01 scan, hail, shield-frequency relay, beam-lock,
                        1-2 km range, stationary 15-second, and fire-clearance gates. Every
                        automatic gate exposes a Comms/GM fallback and its *_fallback_available
                        state. The delayed stationary check must carry drone_01_stationary_hold_run_id
                        and stop on reset, destruction, or story-jump invalidation.
                     5. In //damage/object, count a Drone 01 hit only when MANUAL_SYSTEM is
                        present and identifies Weapons. Do not require MANUAL_CRITICAL_HIT: Phase A
                        live evidence proved it can be absent while MANUAL_SYSTEM is valid. Set
                        drone_01_weapons_disabled only at the third confirmed Weapons hit.
                     6. Before authorization, reset Drone 01; if it is destroyed before its
                        Weapons array is disabled, reset it. Each reset cleans the old entity and
                        respawns five kilometres farther from the beacon, increments
                        drone_01_reset_count, clears the required transient gates, and broadcasts
                        the canonical reset notice. A reset/destroy cleanup must never count as a
                        live-fire success.
                     7. After the confirmed disable and captain/Training Control ceasefire,
                        cleanly remove Drone 01 and spawn Drone 02 at ten kilometres. Drone 02 may
                        maneuver but must remain non-lethal/training-safe; its genuine destruction
                     event sets drone_02_destroyed and sets drone_contact_act2_ready for Slice 07.
                     Do not require a
                        subsystem disable or ceasefire for Drone 02.
                     8. Send the canonical cultural Comms packet through the objective broadcast
                        channel and its archive echo, set a status on every success/failure/fallback
                        branch, invoke only an existing Act II transition route, and add static
                        regression coverage plus coverage-matrix status updates.

Tests required:      ACT1-019
                     ACT1-020
                     ACT1-021
                     ACT1-022
                     ACT1-023
                     ACT1-024

Acceptance criteria: - Drone 01 is passive and uses the complete controlled-disable sequence.
                     - Unauthorized damage and premature destruction reset Drone 01 five kilometres
                       farther from the beacon without advancing the drill.
                     - The range band plus a full 15-second stationary hold are required before
                       fire authorization; stale delayed work cannot satisfy the gate after reset.
                     - Three confirmed MANUAL_SYSTEM=WEAPONS hits disable Drone 01's Weapons array;
                       a genuine ceasefire is required before Drone 01 completes.
                     - Drone 02 spawns at ten kilometres and only its genuine destruction sets
                       the Slice-07-owned Act-II-ready marker; it does not change mission_phase.
                     - The canonical cultural packet is visible through the objective-broadcast
                       channel and archives once; no GM-only comms_receive() rendering is required.
                     - Quick/static checks pass, then the listed ACT1 checks receive live evidence.

Expected observations:
                     - ACT1-019: firing before clearance removes Drone 01, then a replacement
                       appears five kilometres farther from Tarsis Training Beacon; objective text
                       gives the canonical unauthorized-hit reset message.
                     - ACT1-020: destroying Drone 01 before its Weapons array is disabled produces
                       the controlled-disable reset message and a five-kilometre-farther target;
                       it does not spawn Drone 02 or advance Act II.
                     - ACT1-021: no clearance appears outside 1-2 km or before 15 stationary
                       seconds; the objective broadcast confirms the window only after both hold.
                     - ACT1-022: exactly three valid manual Weapons-subsystem hits record disable;
                       non-Weapons damage and fewer than three hits do not complete it.
                     - ACT1-023: a genuine Weapons destruction of Drone 02 records destruction,
                       sets the Act-II-ready objective, and does not confuse GM cleanup with a
                       kill.
                     - ACT1-024: the canonical cultural packet is visibly broadcast and appears
                       once in the Comms archive.

Failure/ambiguous observations:
                     - A target attacks, stock enemy menus appear, or instrumentation language is
                       visible: stop and record the target/route and exact output.
                     - A reset happens at the wrong distance, retains a prior gate, or a deleted
                       object advances a success path: FAIL; capture trace lines and status values.
                     - No MANUAL_SYSTEM value arrives on a deliberate Weapons subsystem hit, or
                       the value does not identify Weapons: AMBIGUOUS/FAIL; do not substitute
                       generic system_damage or MANUAL_CRITICAL_HIT.
                     - The objective broadcast/archive message is absent, duplicated, or only a
                       GM comms_receive() result: FAIL/AMBIGUOUS as appropriate.
                     - No visible problem but no trace/status evidence of a gate: AMBIGUOUS, not
                       a pass.

What remains unproven:
                     - No Phase B runtime behavior is proven by this packet or static tests.
                     - The Phase A spike proved MANUAL_SYSTEM exposure, but not the exact
                       production normal-enemy object/role combination, range observer, beam-lock
                       observer, stationary-hold observer, or three-hit production state machine.
                     - Generic system_damage remains unsuitable as per-subsystem proof; no
                       subsystem-keyed data_set lookup is claimed here.
                     - GM-only comms_receive() rendering remains deliberately deprioritized and is
                       not a Phase B acceptance dependency.
                     - Slice 07 owns the actual Act II callable and phase transition; Slice 06
                       only records drone_contact_act2_ready.

Next action by result:
                     - If static checks and a crewed live smoke meet all observations, update
                       SLICE06_VERIFICATION.md with a dated PASS/PARTIAL record and prepare the
                       reviewed implementation commit for operator-directed next work.
                     - If a proven Phase A API behavior differs in the production target, retain
                       the evidence, enable the documented Comms/GM fallback, and record a
                       targeted API uncertainty; do not silently weaken the controlled-disable
                       requirement.
                     - Slice 07 consumes drone_contact_act2_ready and owns the actual phase pivot.

Known risks:          - Source conflict to surface, not resolve: the detailed D3 items in the admin
                       plan describe an Engine-disable/ceasefire Drill Three, while the canonical
                       Slice 06 acceptance IDs and the explicit Phase A source decision specify
                       Drone 02 destruction. This packet follows the explicit decision and names
                       only ACT1-019 through ACT1-024; it does not edit either design document.
                     - Phase A's destroy-hook guard is live-proven only for its spike object. The
                       implementation must reproduce the cleanup-vs-genuine-kill live test for
                       each production target.
                     - Normal enemy object selection and non-attacking behavior were proven only
                       by the spike's custom neutral target. A production enemy object may expose
                       stock behavior; live smoke is mandatory.
                     - Existing GM-only comms_receive() rendering has a documented live failure.
                       Objective broadcast is the required player-facing channel for this packet.
                     - The packet is documentation only. It does not itself resolve any API or
                       live-runtime uncertainty.

Do not implement:    - Any edit under docs/01_design/ or docs/02_content/.
                     - A fix or further experiment for GM-only comms_receive() rendering.
                     - New Scenario Control Panel, story-jump presets, checkpoint/reload work, or
                       changes to bootstrap, Tarsis, or Engineering ownership.
                     - A generic system_damage threshold as a substitute for MANUAL_SYSTEM=WEAPONS.
                     - Drone 02 Engine-subsystem/ceasefire completion, despite the conflicting
                       detailed D3 test prose; its completion is destruction by explicit decision.
                     - Qualification auto-grading, new Dillon/audio content, pirate/DAMCON/Act II
                       gameplay, or changes to qualification/design/player-fiction text.
                     - Removal of Phase A evidence or any assertion that static checks prove live
                       Cosmos behavior.
```
