# KHOVAN REACH — SLICE PACKETS 07–16

Version: 1.0
Status: active implementation input contract
Purpose: full slice packets for Slices 07 through 16, written to the 21-field template in `docs/01_design/50_implementation_slice_plan.md` section 2.

## Why this file exists, and what it is not

`docs/01_design/50_implementation_slice_plan.md` is the design authority for *what* each slice is. It is off-limits to edit during implementation work (`AGENTS.md` section 2, `70_agent_handoff_protocol.md` section 5.2). This file is the build-side elaboration of Slices 07–16 into handoff-ready packets. It adds no scenario design and changes no scenario intent.

Where this file and the slice plan disagree about *design*, the slice plan wins and the disagreement is a finding to route to the operator — several are recorded below. Where they differ in *detail*, this file is simply more specific.

Slices 00–06 are not re-packeted here. They are built or in progress, and their verification records already carry their contracts.

---

# 1. Cross-cutting findings

These were found while writing the packets and apply across several slices. Each is a real conflict or gap in the existing plan, not a style preference.

## 1.1 `damcon_*` state prefix is already taken, by a different concept

Slice 05 already owns these names in `scripts/acts/act1_engineering_shakedown.mast`:

```text
damcon_rest_cycle_confirmed          damcon_meal_cycle_confirmed
damcon_rest_cycle_detection_mode     damcon_meal_cycle_detection_mode
damcon_rest_cycle_fallback_available damcon_meal_cycle_fallback_available
damcon_rest_cycle_text               damcon_meal_cycle_text
damcon_mess_instruction_text
```

These are **Act I engineering-shakedown crew-positioning gates** — DAMCON crew sent to quarters and mess as a training drill. They have nothing to do with Slice 09's DAMCON timer, which tracks a team **trapped aboard Halcyon Drift after the cascade**.

Slice 09 must not reuse or extend the `damcon_rest_*` / `damcon_meal_*` groups. It gets `damcon_timer_*`, `damcon_team_*`, `damcon_report_*`, and `damcon_outcome_*`. An agent that greps `damcon_` and assumes one owner will corrupt Slice 05's live-proven gates.

## 1.2 `repair_*` state prefix is already taken, by a different concept

`repair_complete_text` already exists in Slice 05 — it is the **controlled-overload repair** in the Act I engineering shakedown. Slice 13's repair is the **Halcyon Drift hull/systems repair** in Act III. Slice 13 gets `halcyon_repair_*`, never bare `repair_*`.

## 1.3 Acts II/III have no automation gate map

`10_mast_requirements.md` section 8.9 is the only canonical gate/fallback table and it covers **Act I only**. Every packet below therefore specifies its own gate/fallback pairs. These are proposals derived from the ownership matrix in section 7 and the per-system requirements in sections 9–15 — they are **not** operator-approved canon the way section 8.9 is. Treat a gate/fallback pair in this file as a design proposal to confirm at live smoke, not as settled.

## 1.4 Only 3 of 27 JUMP presets exist

`scripts/systems/story_jump_presets.mast` implements JUMP-001, JUMP-004, and one unnumbered preset (see `tests/ADMIN_JUMP_VERIFICATION.md` for the JUMP-008 semantic conflict). Slices 07–16 need JUMP-011 through JUMP-027. Every packet that needs a preset lists it explicitly, because a slice with no jump preset cannot be live-smoked without replaying everything before it — which, at Act III, is a 95–105 minute replay per attempt.

**Preset work is not optional scope inside these slices.** It is the only thing that keeps live-smoke cost bounded.

## 1.5 Clips are text stand-ins

Per the operator decision recorded in `10_mast_file_lessons.md` section 3.8, every clip in these slices ships as a **text stand-in**, structurally equivalent to a future audio trigger, with the clip ID logged. No packet below builds audio playback, and none should grow a general clip router speculatively.

## 1.6 Helper extraction starts here

`scripts/lib/` is empty. Per `70_agent_handoff_protocol.md` section 5.2, Slices 09, 11, and 15 must place shared cleanup/spawn/seed logic in `scripts/lib/` from the start rather than growing act files toward the 969-line precedent set by `act1_generator_tarsis_gate.mast`.

---

# 2. Packets

## SLICE 07 — Act II pivot and Halcyon arrival

**Sizing note.** The slice-plan entry lists 6 build items across 4 scenes (5 Anderson Orders, 6 Transit, 7 Distress Localized, 8 Halcyon Arrival), plus 2 checkpoints and 3 jump presets. Decomposed honestly that is 11 implementation tasks, which exceeds the 8-task rule in `70_agent_handoff_protocol.md` section 3.2. **Split into Phase A and Phase B**, following the Slice 06 precedent. The phase boundary is a live-smoke gate, not a convenience.

### Slice 07 Phase A — Anderson orders and Act II pivot

```text
Slice ID:            07A
Goal:                Mission pivots from Act I training to Act II live operation. Anderson
                     delivers orders, the mission phase advances, and Science can localize
                     the distress signal.

Source docs:         docs/01_design/00_scenario_play_guide.md Scenes 5-7
                     docs/01_design/10_mast_requirements.md section 7 (ownership: Scene 5
                       AUTO, Scene 6 AUTO, Scene 7 AUTO + GM-SUP), section 12 (checkpoints)
                     docs/01_design/40_admin_testing_plan.md sections 6.2, 10
                     docs/02_content/30_anderson_clips.md Clip 1
                     docs/02_content/40_dillon_clips.md Clip 8
                     tests/SLICE06_VERIFICATION.md (entry state this slice inherits)

Files to modify:     scripts/acts/act2_pivot.mast                    (new)
                     scripts/main.mast                               (import + init order)
                     scripts/systems/story_jump_presets.mast         (JUMP-011, JUMP-012)
                     tests/test_act2_pivot_static.py                 (new)
                     run_tests.py                                    (register test file)
                     tests/SLICE07A_VERIFICATION.md                  (new)

Runtime owner model: act2_pivot.mast owns act2_* / anderson_* / distress_* state, the Act II
                     phase transition, and the post_anderson_orders checkpoint write.
                     story_jump_presets.mast owns JUMP-011/012 dispatch only; the seed
                     helpers themselves live in act2_pivot.mast, matching how Slice 04/05
                     seed helpers live in their own act files.
                     No other file writes act2_* state.

State variables needed:
                     act2_pivot_initialized            act2_pivot_status
                     act2_last_progression_summary
                     anderson_orders_delivered         anderson_clip_1_stub_sent
                     anderson_orders_text              anderson_orders_ack_status
                     distress_signal_detected          distress_localized
                     distress_localization_status      distress_science_gate_status
                     distress_localization_fallback_available
                     dillon_clip_8_stub_sent
                     Collision check: no existing shared name begins act2_, anderson_,
                     or distress_ (verified by repo-wide grep at packet-writing time).
                     The duplicate-shared check in run_tests.py enforces this at build time.

Branch type:         implementation
Starting branch:     master, after Slice 06 merges back
Expected return branch: master
Branch lifecycle plan:
                     Open slice07a-act2-pivot from master. Commit per task. Merge back to
                     master only after Phase A live smoke passes or a documented fallback
                     is accepted. Record in branch_ledger.md at open and at merge.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks (ordered, each testable):
                     1. Create act2_pivot.mast, import from main.mast, add init task after
                        Slice 06 init. Add BOOT-style trace marker.
                     2. Anderson Clip 1 text stand-in with duplicate suppression, routed
                        through the existing safe-message wrapper in audio_runtime.mast.
                     3. Act I -> Act II phase transition, gated on
                        engineering_shakedown_complete (or Direct Scenario equivalent).
                     4. Distress signal detection state + Science route exposing
                        localization, with GM/Comms fallback and
                        distress_localization_fallback_available.
                     5. Dillon Clip 8 text stand-in with duplicate suppression.
                     6. post_anderson_orders checkpoint write.
                     7. JUMP-011 anderson_orders + JUMP-012 distress_localized presets with
                        seed helpers and run-ID invalidation of stale Act I timers.
                     8. Static tests + run_tests.py registration.

Tests required:      JUMPTEST-011, JUMPTEST-012   (jump preset validation)
                     SAVE-004                     (post_anderson_orders checkpoint saves)
                     OBJ-001, OBJ-002             (current-objective updates on pivot)
                     All IDs verified present in tests/test_coverage_matrix.md.

Acceptance criteria: Act II phase is reachable from Slice 06 end state without GM
                     intervention; Anderson Clip 1 and Dillon Clip 8 each deliver exactly
                     once; distress localization has a working automatic path AND a working
                     fallback; post_anderson_orders checkpoint persists; JUMP-011/012 seed
                     valid states; quick passes; no design doc modified.

Expected observations:
                     Anderson Clip 1 text appears once in the Comms surface.
                     mission_phase reads act_2 after orders.
                     Science sees a distress-localization action; using it sets
                       distress_localized and updates the current objective.
                     GM Test Mode shows JUMP-011 and JUMP-012; each seeds without error.
                     Trace shows the Act II init and pivot markers in order.

Failure/ambiguous observations:
                     Clip text appears twice, or not at all.
                     Phase advances before Slice 06 completion.
                     Science action present but produces no state change and no error
                       (AMBIGUOUS - record as such, do not pass).
                     Jump preset seeds but leaves a stale Act I advisory timer firing.
                     Objective text does not change after pivot.

What remains unproven after this slice:
                     Halcyon spawn/scan/hail (Phase B).
                     Whether the distress-localization Science route renders in a live
                       crewed session - GM-console-only smoke cannot prove Science UI, as
                       Slice 06 already demonstrated.

Next action by result:
                     PASS -> Phase B.
                     Science route fails or is ambiguous -> fall back to Comms/GM-marked
                       localization, set the fallback flag, record, continue to Phase B.
                     Phase transition fires early -> stop, fix the gate before Phase B.

Known risks:         Anderson is a new speaker with no existing station/contact binding;
                       the Slice 04 lifeform-overlay black-box failure is precedent for
                       message-surface problems. Use the proven safe-message wrapper.
                     Act I timers must be invalidated on Act II entry or a stale Kestrel
                       advisory can fire mid-Act-II (run-ID guard pattern, cookbook 5.1).

Do not implement:    Halcyon spawn, scan, or hail (Phase B).
                     Engineering/DAMCON deployment state (Phase B).
                     Hessler away mission or any Scene 9 content (Slice 08).
                     Cascade trigger (Slice 08).
                     DAMCON timer of any kind (Slice 09).
                     Audio playback (text stand-ins only).
                     Any JUMP preset other than 011 and 012.
                     Any change to Act I files beyond timer invalidation hooks.
```

### Slice 07 Phase B — Halcyon arrival and deployment

```text
Slice ID:            07B
Goal:                Halcyon Drift exists as a scannable, hailable contact; Engineering and
                     DAMCON deployment state is tracked; arrival checkpoint persists.

Source docs:         docs/01_design/00_scenario_play_guide.md Scene 8
                     docs/01_design/10_mast_requirements.md section 7 (Scene 8 = AUTO +
                       GM-SUP, "Spawn/scan/hail/deploy state", GM coordinates Hessler handoff)
                     docs/04_implementation_setup/60_mast_api_cookbook.md sections 7, 8
                       (spawn, roles, selection, cleanup)
                     tests/SLICE07A_VERIFICATION.md

Files to modify:     scripts/acts/act2_halcyon_arrival.mast          (new)
                     scripts/lib/entity_cleanup_helpers.mast         (new - see 1.6)
                     scripts/main.mast
                     scripts/systems/story_jump_presets.mast         (JUMP-013)
                     tests/test_act2_halcyon_arrival_static.py       (new)
                     run_tests.py
                     tests/SLICE07B_VERIFICATION.md                  (new)

Runtime owner model: act2_halcyon_arrival.mast owns halcyon_* state, the Halcyon spawn
                     lifecycle, and its Science/Comms routes.
                     entity_cleanup_helpers.mast owns the reusable despawn/deselect routine
                     and is called by story jumps; it owns no state of its own.
                     act2_pivot.mast keeps ownership of act2_/distress_ state; Phase B reads
                     but never writes it.

State variables needed:
                     halcyon_arrival_initialized       halcyon_spawned
                     halcyon_object_id                 halcyon_navproxy_id
                     halcyon_spawn_count               halcyon_cleanup_count
                     halcyon_scan_observed             halcyon_hail_observed
                     halcyon_arrival_status            halcyon_contact_fallback_available
                     engineering_deployed              engineering_deploy_status
                     engineering_placement             damcon_deployed
                     damcon_deploy_status
                     WARNING: damcon_deployed / damcon_deploy_status are new names in the
                     damcon_ space. They are Act II deployment tracking and must not be
                     confused with Slice 05's damcon_rest_*/damcon_meal_* gates (finding 1.1)
                     or Slice 09's damcon_timer_* group. engineering_placement is the input
                     Slice 09 reads to choose extended vs compressed timer config - name it
                     exactly this, because Slice 09's packet depends on it.

Branch type:         implementation
Starting branch:     master, after 07A merges
Expected return branch: master
Branch lifecycle plan: slice07b-halcyon-arrival; same discipline as 07A.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. Create act2_halcyon_arrival.mast + import/init wiring.
                     2. Create scripts/lib/entity_cleanup_helpers.mast with a generic
                        "despawn object, drop navproxy, clear all three selections" routine.
                     3. Halcyon spawn with existence check (do not double-spawn) and
                        registration of object/navproxy IDs.
                     4. Science scan route + halcyon_scan_observed.
                     5. Comms hail route + halcyon_hail_observed, with GM fallback.
                     6. Engineering + DAMCON deployment state, including
                        engineering_placement (aboard_halcyon | returned_to_artemis).
                     7. post_halcyon_arrival checkpoint write.
                     8. JUMP-013 halcyon_arrival preset, seeding through the cleanup helper
                        so repeat jumps do not stack Halcyon copies.

Tests required:      JUMPTEST-013
                     SAVE-005
                     OBJ-003, OBJ-004
                     All verified present in tests/test_coverage_matrix.md.

Acceptance criteria: Halcyon spawns exactly once per jump; repeat JUMP-013 does not stack
                     duplicates; scan and hail both register; engineering_placement is set
                     and readable; checkpoint persists; cleanup helper fully removes the
                     contact; quick passes.

Expected observations:
                     Exactly one Halcyon Drift contact after arrival, and still exactly one
                       after re-running JUMP-013.
                     Science scan sets the observed flag; Comms hail sets its flag.
                     GM overview shows engineering_placement.

Failure/ambiguous observations:
                     Two or more Halcyon contacts after a repeat jump (cleanup failure).
                     Contact selectable but Comms options panel empty - this is the exact
                       Slice 04 Tarsis failure; treat as FAIL, not ambiguous, and consult
                       the Slice 04 record before re-attempting.
                     Scan/hail actions execute with no state change and no error (AMBIGUOUS).
                     Cleanup fires a //damage/destroy handler - see the Slice 06 finding;
                       if any destruction-sensitive state exists by then, guard it.

What remains unproven: Hessler away-mission interaction (Slice 08).
                     Whether engineering_placement survives checkpoint reload (Slice 15).

Next action by result:
                     PASS -> Slice 08.
                     Duplicate spawn -> stop; fix cleanup helper before Slice 08, because
                       Slices 10/11/12 all reuse it.
                     Empty Comms panel -> apply Slice 04 remedy, re-smoke before proceeding.

Known risks:         Spawn/cleanup is the highest-reuse code in the remaining build; a defect
                       here propagates to cache, pirates, and combat.
                     sbs.delete_object() firing //damage/destroy is confirmed live (Slice 06).

Do not implement:    Hessler dialogue or away-mission beats (Slice 08).
                     Cascade (Slice 08). DAMCON timer (Slice 09).
                     Halcyon repair (Slice 13) - arrival only, no repair state.
                     Audio playback.
```

---

## SLICE 08 — Away mission wrapper and cascade

```text
Slice ID:            08
Goal:                The Hessler away-mission scene is bounded by a runtime beat tracker so
                     a GM-driven conversation cannot lose mission structure, and the cascade
                     fires cleanly as the input to Slice 09.

Source docs:         docs/01_design/00_scenario_play_guide.md Scene 9
                     docs/01_design/10_mast_requirements.md section 7 (Scene 9 = GM-DRIVE
                       inside AUTO wrapper: "Beat tracker, comms channel, cascade readiness";
                       GM paces the Hessler conversation), section 12 (post_cascade)
                     docs/02_content/00_hessler_voice_mode.md
                     docs/04_implementation_setup/60_mast_api_cookbook.md sections 5.1,
                       5.2, 17.11, 17.12, and 17.12.1
                     tests/SLICE07B_VERIFICATION.md

Files to modify:     scripts/acts/act2_away_mission.mast             (new)
                     scripts/main.mast
                     scripts/systems/story_jump_presets.mast         (JUMP-013 through JUMP-015)
                     tests/test_act2_away_mission_static.py          (new)
                     tests/test_story_jump_presets_static.py
                     tests/test_coverage_matrix.md
                     run_tests.py
                     tests/SLICE08_VERIFICATION.md                   (new)

Runtime owner model: act2_away_mission.mast owns away_*, hessler_channel_open,
                     hessler_contact_status, cascade_*, convergence_*, bridge_report_*, and
                     the beat tracker. lifeform_helpers.mast retains ownership of
                     hessler_lifeform_*. This is the first GM-DRIVE scene: runtime owns structure
                     and readiness only, never dialogue content. The GM drives pacing; the
                     runtime must never auto-advance a beat the GM has not marked, except
                     the cascade readiness gate.
                     Slice 09 reads cascade_triggered and cascade_time but never writes them.

State variables needed:
                     away_mission_initialized      away_mission_active
                     away_mission_beat             away_mission_beat_count
                     away_mission_status           away_mission_beats_complete
                     hessler_channel_open          hessler_contact_status
                     convergence_flag              convergence_status
                     cascade_ready                 cascade_triggered
                     cascade_time                  cascade_trigger_source
                     bridge_report_status          bridge_report_last
                     cascade_fallback_available
                     Collision check: exact proposed names are available. The hessler_ prefix
                     is already shared: lifeform_helpers.mast owns hessler_lifeform_id and
                     hessler_lifeform_status. Reuse that existing Halcyon-hosted Hessler
                     lifeform and do not shadow, reset, or recreate its lifecycle state here.
                     cascade_triggered / cascade_time are named exactly as
                     10_mast_requirements.md section 9.1 specifies, because Slice 09's
                     activation contract reads them verbatim.

Branch type:         implementation
Starting branch:     master, after Slice 07B merges
Expected return branch: master
Branch lifecycle plan: slice08-away-mission-cascade; standard discipline.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. Create act2_away_mission.mast + wiring.
                     2. Reuse hessler_lifeform_id and the existing Hessler send/fallback path
                        delivered by Slice 07B; do not create a second Hessler lifeform.
                     3. Beat tracker: ordered beat list, GM-advanced, with current beat
                        surfaced to the GM overview. No auto-advance.
                     4. Hessler comms channel state (open/close), GM-controlled.
                     5. Convergence flag - the condition set that makes cascade legitimate.
                     6. Cascade readiness gate + cascade trigger, writing cascade_triggered
                        and cascade_time. Include a GM manual trigger as the documented
                        fallback and set cascade_fallback_available.
                     7. Guard every delayed cascade/readiness task with an away-mission run ID;
                        cleanup and all three story jumps must invalidate earlier tasks.
                     8. Bridge report state so the bridge crew sees away-team status. This is
                        state/surface work only; do not invent Reyes dialogue or a Reyes
                        lifeform in this slice.
                     9. Write last_checkpoint = "post_cascade" after a valid cascade trigger.
                    10. Add three independent presets, each using reset/cleanup helpers rather
                        than chaining one story jump through another:
                        - JUMP-013 away_team_deployed: the distinct Scene 8 -> Scene 9 boundary.
                          Seed a transmitted manifest and exactly one deployed DAMCON team by
                          calling the existing Slice 07B deployment path, not by setting only
                          presentation flags.
                        - JUMP-014 away_mission_start: initialize the Scene 9 wrapper at its
                          first GM-controlled beat.
                        - JUMP-015 cascade_decision: seed the final pre-cascade decision state
                          without firing the cascade automatically.
                        Remove the temporary "JUMP-013 is free" placeholder assertion when
                        JUMP-013's real static coverage is added.

Tests required:      JUMPTEST-013, JUMPTEST-014, JUMPTEST-015
                     SAVE-006: Slice 08 proves the checkpoint write and valid trigger ordering;
                       Slice 15 retains ownership of checkpoint reload/persistence proof.
                     OBJ-005, OBJ-006
                     Reconcile that split ownership explicitly in tests/test_coverage_matrix.md.

Acceptance criteria: Beat tracker never auto-advances; GM can move forward and the runtime
                     records each beat; cascade sets cascade_triggered and a usable
                     cascade_time; a valid cascade writes the post_cascade checkpoint; all
                     three presets seed valid, independent state; JUMP-013 leaves exactly one
                     DAMCON team deployed and cannot inherit a prior jump's state; quick passes.

Expected observations:
                     GM overview shows current away-mission beat and it changes only on GM
                       action.
                     Cascade sets cascade_triggered true and stamps cascade_time.
                     Bridge report surface shows away-team status to non-GM stations.
                     GM Test Mode lists JUMP-013 away_team_deployed, JUMP-014
                       away_mission_start, and JUMP-015 cascade_decision in order.

Failure/ambiguous observations:
                     A beat advances without GM action (structure loss - FAIL).
                     Cascade fires without convergence and without explicit GM override.
                     cascade_time is unset, zero, or None after trigger - this silently
                       breaks every Slice 09 threshold; treat as FAIL, not ambiguous.
                     JUMP-013 fails to reduce Artemis's DAMCON roster by exactly one, or
                       inherits a prior hail/manifest/deployment flag (cleanup/seed failure -
                       FAIL).
                     Bridge report state set but nothing renders (AMBIGUOUS).

What remains unproven: Whether cascade_time and post_cascade survive checkpoint reload
                       (Slice 15).
                     Whether the beat tracker is usable at conversational pace with a real
                       GM - only a crewed session can show this.

Next action by result:
                     PASS -> Slice 09.
                     cascade_time unreliable -> STOP. Slice 09's entire outcome model is
                       elapsed-time arithmetic on this value. Fix before starting Slice 09.

Known risks:         This is the first GM-DRIVE scene; the temptation to auto-advance for
                       convenience directly violates the section 7 ownership model.
                     cascade_time is the single highest-leverage value in Acts II/III.
                     JUMP-013 previously named a redundant Halcyon-arrival preset and was
                       deleted after live cleanup/state leakage. Its number is intentionally
                       reissued here for a distinct boundary; JUMP-014 and JUMP-015 retain
                       their canonical meanings. Do not restore the deleted promote path.
                     Slice 07B is live-proven by operator report across repeated play-test
                       sessions. Preserve that verification record's earlier PARTIAL entry as
                       history; consume its later closure entry as the current prerequisite.

Do not implement:    Any DAMCON timer behavior (Slice 09) - this slice only fires the
                       trigger and records the timestamp.
                     Hessler dialogue text or TTS.
                     A duplicate Hessler lifeform, a Reyes lifeform, or new Reyes dialogue.
                     Cache, pirates, combat, repair.
                     Audio playback.
```

---

## SLICE 09 — DAMCON timer  **(SPIKE REQUIRED)**

**Spike rationale.** `70_agent_handoff_protocol.md` section 3.2 flags this slice for timer persistence, report scheduling under story jump, and the irreversible-loss flag. Two of the three are unproven API behavior, and the third is irreversible by definition — a bug here destroys mission state that reload is explicitly forbidden from undoing (`10_mast_requirements.md` section 12). 23 test IDs. Phase A proves the mechanics; Phase B builds the drill.

### Slice 09 Phase A — timer/persistence spike

```text
Slice ID:            09A
Goal:                Prove, in live Cosmos, that a long-running timer survives story jumps
                     and checkpoint writes, that scheduled reports fire on interval without
                     drift or duplication, and that an irreversible flag stays set.

Source docs:         docs/01_design/10_mast_requirements.md section 9 (all), section 12
                     docs/01_design/40_admin_testing_plan.md section 12
                     docs/04_implementation_setup/60_mast_api_cookbook.md sections 5.1, 5.2
                     tests/SLICE08_VERIFICATION.md (cascade_time contract)

Files to modify:     scripts/systems/damcon_timer.mast               (new)
                     scripts/lib/timer_helpers.mast                  (new - see 1.6)
                     scripts/main.mast
                     scripts/systems/scenario_control_panel.mast     (GM spike controls)
                     tests/test_damcon_timer_spike_static.py         (new)
                     run_tests.py
                     tests/SLICE09_VERIFICATION.md                   (new)

Runtime owner model: damcon_timer.mast owns all damcon_timer_*, damcon_team_*,
                     damcon_report_*, damcon_outcome_* state and the scheduling loop.
                     timer_helpers.mast owns reusable run-ID-guarded interval scheduling and
                     is reused by Slice 11's pirate arrival timer - build it generic.
                     It reads cascade_triggered / cascade_time / engineering_placement and
                     writes none of them.
                     CRITICAL: this file must not touch damcon_rest_* or damcon_meal_*,
                     which belong to Slice 05 (finding 1.1).

State variables needed:
                     damcon_timer_initialized      damcon_timer_active
                     damcon_timer_config           damcon_timer_start_time
                     damcon_timer_elapsed          damcon_timer_run_id
                     damcon_timer_paused           damcon_timer_pause_reason
                     damcon_team_status            damcon_report_interval
                     damcon_report_count           damcon_report_last_time
                     damcon_report_held            damcon_report_hold_started
                     damcon_report_hold_limit      damcon_report_drift
                     damcon_outcome                damcon_outcome_locked
                     damcon_timer_fallback_available
                     damcon_timer_spike_status     damcon_timer_spike_result
                     Collision check: none of these exist. Distinct from Slice 05's
                     damcon_rest_*/damcon_meal_* and Slice 07B's damcon_deploy* groups.

Branch type:         spike/experiment
Starting branch:     master, after Slice 08 merges
Expected return branch: master
Branch lifecycle plan:
                     slice09a-damcon-timer-spike. Merged deliberately if the mechanics hold;
                     discarded with a recorded finding if they do not. Do not merge a spike
                     that only "compiles" - Slice 06 Phase A is the precedent for stopping
                     at partial proof and saying so.
Runtime/live-smoke allowed from this branch: yes - this branch exists to be live-smoked
Merge-back required: only on acceptance

Implementation tasks:
                     1. Create timer_helpers.mast: run-ID-guarded repeating interval task
                        (cookbook 5.1 pattern), generic over interval and callback.
                     2. Create damcon_timer.mast; activate on cascade_triggered; select
                        config from engineering_placement (aboard_halcyon -> extended/180s,
                        returned_to_artemis -> compressed/90s) per requirements 9.1.
                     3. Elapsed-time computation and threshold evaluation only - no player
                        messaging yet.
                     4. Irreversible flag: once damcon_outcome reaches total_loss, set
                        damcon_outcome_locked and make it unwritable by any later path.
                     5. GM Test Mode spike controls: start, force-elapse, read status,
                        stop/reset. Test-Mode-gated exactly like the Slice 06 spike route.
                     6. Trace breadcrumbs on every tick, report, hold, and threshold cross.
                     7. Static tests + registration.

Tests required:      DAMCON-001  cascade trigger starts timer
                     DAMCON-002  Engineer aboard Halcyon selects extended timer
                     DAMCON-003  Engineer returned selects compressed timer
                     DAMCON-005  timer persists across checkpoint
                     DAMCON-006  timer restores after reload
                     DAMCON-010  extended reports schedule every 180 seconds
                     DAMCON-011  compressed reports schedule every 90 seconds
                     All verified present in tests/test_coverage_matrix.md.
                     DAMCON-005/006 may be blocked until Slice 15 - if so, record them as
                     blocked in the matrix rather than claiming them.

Acceptance criteria: Timer starts on cascade; correct config selected from
                     engineering_placement; reports fire on interval without duplication or
                     drift beyond a recorded tolerance; a story jump invalidates the old
                     timer and does not leave a second one running; total_loss lock cannot
                     be cleared.

Expected observations:
                     Trace shows one report per interval, monotonic report_count.
                     Re-running a story jump does not produce interleaved reports from two
                       timers.
                     After forcing elapse past threshold, damcon_outcome reads total_loss and
                       stays there through further jumps.

Failure/ambiguous observations:
                     Two timers running after a jump (run-ID guard failed) - FAIL.
                     Reports drift cumulatively rather than staying on interval.
                     damcon_outcome_locked can be cleared by a jump seed - FAIL, this is the
                       irreversibility contract.
                     Timer appears to run but elapsed never changes (AMBIGUOUS - likely a
                       sim-time vs wall-time confusion; investigate before continuing).
                     Checkpoint written but timer state absent on reload - record as a
                       Slice 15 dependency, not a Phase A failure.

What remains unproven after Phase A:
                     Report content, GM hold/release UX, player-facing delivery, warning
                     sub-bands, and the full outcome narrative - all Phase B.

Next action by result:
                     PASS -> Phase B.
                     Run-ID guard fails -> stop; this pattern is reused by Slice 11's arrival
                       timer, so fix it here.
                     Sim-time ambiguity -> raise as an API-uncertainty finding
                       (cookbook section 12 format) before Phase B.

Known risks:         Elapsed-time semantics in Cosmos are not characterized in the cookbook.
                     A 30-minute extended threshold cannot be smoke-tested in real time -
                       the force-elapse GM control is mandatory, not a convenience.
                     Slice 05 damcon_* collision (finding 1.1).

Do not implement:    Report text/content (Phase B).
                     GM hold/release controls (Phase B).
                     Warning sub-bands (Phase B).
                     Any change to Slice 05 damcon_rest_*/damcon_meal_* state.
                     Repair resolution consequences (Slice 13).
```

### Slice 09 Phase B — reports, holds, outcomes

```text
Slice ID:            09B
Goal:                DAMCON pressure is automatic, pace-adjustable by the GM, and
                     irreversible at threshold.

Source docs:         docs/01_design/10_mast_requirements.md sections 9.2, 9.3
                     docs/02_content/20_damcon_reports.md
                     docs/01_design/40_admin_testing_plan.md section 12
                     tests/SLICE09_VERIFICATION.md (Phase A results)

Files to modify:     scripts/systems/damcon_timer.mast
                     scripts/systems/scenario_control_panel.mast     (GM hold/release)
                     scripts/systems/story_jump_presets.mast         (JUMP-016, JUMP-017)
                     tests/test_damcon_timer_static.py               (new)
                     run_tests.py
                     tests/SLICE09_VERIFICATION.md

Runtime owner model: unchanged from Phase A. GM hold/release is GM-SUP: the runtime queues
                     and auto-releases, the GM may delay within a bounded window, and the
                     timer itself keeps running regardless (requirements 9.2).

State variables needed:
                     (Phase A set, plus)
                     damcon_report_queue           damcon_report_text_last
                     damcon_warning_band           damcon_warning_sent_critical
                     damcon_warning_sent_hypoxic   damcon_hold_count
                     damcon_hold_total_seconds     damcon_combat_hold_active

Branch type:         implementation
Starting branch:     master, after 09A merges
Expected return branch: master
Branch lifecycle plan: slice09b-damcon-reports; standard discipline.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. Report queue + delivery to GM/Comms, sourced from
                        docs/02_content/20_damcon_reports.md.
                     2. Auto-release unless held; GM hold up to 60s normal / 90s in combat
                        (requirements 9.2 items 3-5).
                     3. Hold/release/drift logging.
                     4. Warning sub-bands: extended T+24/T+27, compressed T+9/T+12,
                        duplicate-suppressed.
                     5. Outcome thresholds per 9.3 - clean_survival / hypoxic_survival /
                        total_loss for both configs.
                     6. total_loss sets damcon_team_status = lost, feeding Slice 13.
                     7. JUMP-016 cache_run_extended_timer + JUMP-017 cache_run_compressed_timer.
                     8. Static tests + registration.

Tests required:      DAMCON-004, DAMCON-012, DAMCON-013, DAMCON-014, DAMCON-015,
                     DAMCON-016, DAMCON-017, DAMCON-018, DAMCON-020, DAMCON-021,
                     DAMCON-022, DAMCON-023, DAMCON-024, DAMCON-025, DAMCON-026,
                     DAMCON-027
                     JUMPTEST-016, JUMPTEST-017
                     GOLD-001 (clean qualification success), GOLD-002 (compressed timer loss)
                     All verified present in tests/test_coverage_matrix.md.

Acceptance criteria: Reports deliver on interval with correct content; GM hold works within
                     bounds and auto-releases past them; the timer never stops for a hold;
                     all three outcome bands reachable and correct for both configs; warnings
                     fire once each; total_loss is irreversible.

Expected observations:
                     Reports appear at the configured interval with text from the content doc.
                     GM hold delays delivery; exceeding the bound auto-releases and logs drift.
                     Forcing each band produces the correct damcon_outcome.

Failure/ambiguous observations:
                     Timer pauses during a hold (violates 9.2 - FAIL).
                     A warning fires twice (duplicate suppression failure).
                     Threshold boundary off by one band.
                     Report queued but never rendered (AMBIGUOUS - GM-surface question,
                       same class as the Slice 06 status-readback finding).

What remains unproven: Interaction with Slice 12 combat holds until Slice 12 exists.
                     Reload restoration until Slice 15.

Next action by result:
                     PASS -> Slice 10.
                     Hold pauses the timer -> fix before Slice 10; this is a design-contract
                       violation, not a polish item.

Known risks:         GOLD-002 requires driving a full compressed-timer loss; without the
                       force-elapse control from Phase A this is a 15-minute wait per attempt.
                     Report rendering surface is unproven for GM-context messages
                       (Slice 06 precedent).

Do not implement:    Cache run (Slice 10). Pirates (Slice 11). Combat holds (Slice 12).
                     Halcyon repair or final outcome narrative (Slice 13).
                     Auto-grading of any kind.
```

---

## SLICE 10 — Cache run and component selection

```text
Slice ID:            10
Goal:                Cache arrival, component selection, wrong-part retry, and Science
                     evidence work. A wrong component is recoverable but costly.

Source docs:         docs/01_design/00_scenario_play_guide.md Scene 13
                     docs/01_design/10_mast_requirements.md section 11 (full), section 7
                       (Scene 11 Cache Run and Scene 13 Cache Selection = AUTO + GM-SUP)
                     docs/01_design/40_admin_testing_plan.md section 14
                     tests/SLICE09_VERIFICATION.md (timer pressure this scene runs under)

Files to modify:     scripts/acts/act3_cache_run.mast                (new)
                     scripts/lib/entity_cleanup_helpers.mast         (reuse from 07B)
                     scripts/main.mast
                     scripts/systems/story_jump_presets.mast         (JUMP-022)
                     tests/test_act3_cache_run_static.py             (new)
                     run_tests.py
                     tests/SLICE10_VERIFICATION.md                   (new)

Runtime owner model: act3_cache_run.mast owns cache_* state, the cache contact lifecycle, and
                     the selection routes. It reads damcon_timer_elapsed to stamp the timer
                     consequence of a wrong choice but never writes DAMCON state.
                     Selection presentation is AUTO; interpretation of a wrong choice's
                     narrative cost is GM-SUP.

State variables needed:
                     cache_run_initialized         cache_arrival
                     cache_object_id               cache_navproxy_id
                     cache_spawn_count             cache_cleanup_count
                     cache_options_status          cache_component_selected
                     cache_selection_result        cache_selection_count
                     cache_retry_required          cache_retry_complete
                     cache_timer_consequence_marker
                     cache_science_evidence_status cache_selection_fallback_available
                     Collision check: no existing shared name begins cache_.

Branch type:         implementation
Starting branch:     master, after Slice 09B merges
Expected return branch: master
Branch lifecycle plan: slice10-cache-run; standard discipline.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. Create act3_cache_run.mast + wiring.
                     2. Cache arrival state + contact spawn, reusing the 07B cleanup helper.
                     3. Component options exactly per requirements section 11:
                          Quantum field stabilizer, civilian-grade  -> correct
                          Quantum field stabilizer, military-grade  -> incorrect_military
                          Quantum field regulator, civilian-grade   -> incorrect_regulator
                          Other plausible components                -> incorrect_other
                     4. Selection recording + cache_component_selected.
                     5. Wrong first attempt -> cache_retry_required = true; correct second
                        attempt -> cache_retry_complete = true.
                     6. Timer consequence marker stamping elapsed DAMCON time at wrong choice.
                     7. Science evidence surface so the correct choice is inferable, not
                        guessable, with a GM fallback.
                     8. JUMP-022 cache_selection preset.

Tests required:      CACHE-001, CACHE-002, CACHE-003, CACHE-004, CACHE-005, CACHE-006,
                     CACHE-007, CACHE-008, CACHE-009, CACHE-010, CACHE-011, CACHE-012
                     GOLD-003 (wrong cache recovery)
                     All verified present in tests/test_coverage_matrix.md.
                     GAP: JUMP-022 has no corresponding JUMPTEST ID - see finding 3.6.
                     Validate the preset against the section 10 standard procedure and
                     record it under CACHE-001 until an ID is assigned.

Acceptance criteria: All four option classes selectable and correctly classified; wrong
                     choice sets retry-required and is recoverable; correct second attempt
                     completes; the timer cost of a wrong choice is recorded; Science
                     evidence is available; quick passes.

Expected observations:
                     Four distinct component options render.
                     Selecting civilian-grade stabilizer marks correct on first try.
                     Selecting military-grade marks incorrect_military and sets retry.
                     Timer consequence marker shows elapsed time at the wrong selection.

Failure/ambiguous observations:
                     Options render but selection produces no state change (AMBIGUOUS - the
                       Slice 04 empty-Comms-panel class of failure; check that before
                       assuming a logic bug).
                     Wrong choice is unrecoverable (violates "recoverable but costly").
                     Retry succeeds with no recorded cost (removes the stakes).
                     Cache contact persists after the scene (cleanup failure).

What remains unproven: How a wrong choice reads narratively under real timer pressure -
                     only a crewed run with a live DAMCON timer shows this.

Next action by result:
                     PASS -> Slice 11.
                     Selection inert -> apply Slice 04 remedy and re-smoke.
                     Wrong choice unrecoverable -> stop; this inverts the design intent.

Known risks:         The requirements specify option semantics but not the presentation
                       mechanism; the cookbook has no proven inventory/selection-prompt
                       pattern. Expect to use a Comms-route option list (the proven pattern)
                       rather than inventing a UI. Raise an API-uncertainty block if tempted
                       to do otherwise.

Do not implement:    Pirates (Slice 11) - even though pirates may arrive during the cache run.
                     Repair application (Slice 13) - this slice selects the component only.
                     DAMCON timer changes (Slice 09 owns it).
                     Audio playback.
```

---

## SLICE 11 — Pirate state machine  **(SPIKE REQUIRED)**

**Spike rationale.** Flagged in `70_agent_handoff_protocol.md` section 3.2 for arrival timer, state transitions, and docking backstop. This is also the least mechanically verifiable slice in the mission: 25 test IDs over behavior that is explicitly GM-interpreted (`10_mast_requirements.md` section 10 — "MAST should not attempt full TTS pirate roleplay"). Phase A proves the machine; Phase B adds routing and GM controls.

### Slice 11 Phase A — arrival, transitions, backstop spike

```text
Slice ID:            11A
Goal:                Prove the pirate arrival timer fires correctly, that all canonical state
                     transitions are reachable and one-way where required, and that the
                     docking backstop surfaces when Comms probing stalls.

Source docs:         docs/01_design/10_mast_requirements.md section 10 (all subsections)
                     docs/01_design/40_admin_testing_plan.md section 13
                     docs/02_content/10_pirate_dialogue.md (branch references only)
                     docs/04_implementation_setup/60_mast_api_cookbook.md sections 5.1, 5.2
                     tests/SLICE09_VERIFICATION.md (timer_helpers.mast contract)

Files to modify:     scripts/acts/act3_pirates.mast                  (new)
                     scripts/lib/timer_helpers.mast                  (reuse from 09A)
                     scripts/main.mast
                     scripts/systems/scenario_control_panel.mast     (GM spike controls)
                     tests/test_act3_pirates_spike_static.py         (new)
                     run_tests.py
                     tests/SLICE11_VERIFICATION.md                   (new)

Runtime owner model: act3_pirates.mast owns all pirate_* state, the arrival timer, and the
                     transition rules. Per section 10 the runtime owns arrival timing,
                     variables, branch suggestion, transitions, backstop availability,
                     combat transition, and outcome tracking - and the GM owns voice,
                     interpretation, cultural nuance, and tone. The runtime must never
                     decide that a probe was "good enough"; it exposes transition controls
                     and the GM marks them.

State variables needed:
                     pirates_initialized           pirates_arrived
                     pirate_arrival_time           pirate_arrival_run_id
                     pirate_arrival_timer_active   pirate_cover_status
                     pirate_scene_state            pirate_object_id
                     pirate_navproxy_id            pirate_spawn_count
                     pirate_cleanup_count          pirate_suspicion_tells
                     pirate_transition_last        pirate_transition_count
                     pirate_backstop_available     pirate_backstop_surfaced
                     pirate_backstop_hold          pirate_backstop_deadline
                     pirate_docking_requested      pirate_spike_status
                     pirate_spike_result           pirate_arrival_fallback_available
                     Collision check: no existing shared name begins pirate_.

Branch type:         spike/experiment
Starting branch:     master, after Slice 10 merges
Expected return branch: master
Branch lifecycle plan: slice11a-pirate-machine-spike; merged on acceptance, discarded with a
                     finding otherwise.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: only on acceptance

Implementation tasks:
                     1. Create act3_pirates.mast + wiring.
                     2. Arrival timer (~20 min post-cascade per section 10.1) using
                        timer_helpers.mast, with run-ID guard and a story-jump/GM override.
                     3. Arrival sets pirates_arrived, pirate_arrival_time,
                        pirate_cover_status = intact, pirate_scene_state =
                        arrived_cover_intact.
                     4. Transition rules exactly per section 10.2:
                          intact -> suspected  (5 documented triggers)
                          suspected -> exposed (5 documented triggers)
                          intact -> exposed    (2 documented triggers: unauthorized docking,
                                                weapons activation)
                        Exposure must be one-way - once exposed, no path back to intact.
                     5. Backstop per 10.3: after 3-4 min without meaningful probing, surface
                        "request docking?" with trigger / wait-60s / hold options.
                     6. GM Test Mode spike controls: force arrival, force each transition,
                        surface backstop, read state, reset.
                     7. Trace breadcrumbs on arrival, every transition, and backstop events.

Tests required:      PIRATE-001, PIRATE-002, PIRATE-003, PIRATE-004, PIRATE-005, PIRATE-006
                     PIRATE-010, PIRATE-011, PIRATE-012, PIRATE-013, PIRATE-014,
                     PIRATE-015, PIRATE-016
                     PIRATE-020, PIRATE-021, PIRATE-022, PIRATE-023, PIRATE-024, PIRATE-025
                     All verified present in tests/test_coverage_matrix.md. Note the plan's
                     "PIRATE-001 through PIRATE-035" phrasing spans deliberate numbering
                     gaps (007-009, 017-019, 026-029); only the IDs listed here exist.

Acceptance criteria: Arrival fires on timer and via override; all three transition paths
                     reachable; exposure is irreversible; backstop surfaces on schedule and
                     respects hold; a story jump does not leave a second arrival timer armed.

Expected observations:
                     Trace shows a single arrival event with a stamped time.
                     Each forced transition moves pirate_scene_state along a legal edge only.
                     Attempting intact <- exposed is rejected.
                     Backstop appears after the configured idle window and stops appearing
                       when held.

Failure/ambiguous observations:
                     Two arrival timers after a jump (run-ID guard failure) - FAIL, and the
                       same helper is already used by Slice 09.
                     An illegal transition succeeds (e.g. exposed -> intact).
                     Backstop never surfaces, or surfaces immediately.
                     Arrival state set but no contact visible (AMBIGUOUS - spawn vs state
                       mismatch).

What remains unproven after Phase A:
                     Dialogue branch routing, GM control surface, suggested-branch display,
                     and combat handoff - all Phase B or Slice 12.

Next action by result:
                     PASS -> Phase B.
                     Run-ID failure -> stop; fix timer_helpers.mast and re-verify Slice 09,
                       which shares it.
                     Exposure reversible -> stop; this breaks the Slice 12 entry contract.

Known risks:         Reuses timer_helpers.mast from Slice 09 - a change here can regress
                       DAMCON. Re-run Slice 09 tests after any helper edit.
                     A 20-minute arrival timer is untestable in real time; the force-arrival
                       control is mandatory.

Do not implement:    Dialogue text, TTS, or any pirate voice content.
                     Combat (Slice 12).
                     Suggested-branch display (Phase B).
                     Cache changes (Slice 10 owns cache state).
```

### Slice 11 Phase B — dialogue routing and GM controls

```text
Slice ID:            11B
Goal:                Scene 12 is flexible but tracked: the GM gets state, a recommended
                     branch, a source reference, and transition controls.

Source docs:         docs/01_design/10_mast_requirements.md section 10.4
                     docs/02_content/10_pirate_dialogue.md
                     docs/01_design/20_gm_operational_notes.md
                     tests/SLICE11_VERIFICATION.md (Phase A results)

Files to modify:     scripts/acts/act3_pirates.mast
                     scripts/systems/scenario_control_panel.mast
                     scripts/systems/story_jump_presets.mast         (JUMP-018/019/020)
                     tests/test_act3_pirates_static.py               (new)
                     run_tests.py
                     tests/SLICE11_VERIFICATION.md

Runtime owner model: unchanged. The GM display is a decision aid, never an actor.

State variables needed:
                     (Phase A set, plus)
                     pirate_recommended_branch      pirate_branch_source_ref
                     pirate_gm_display              pirate_gm_display_status
                     pirate_transition_options      pirate_probe_quality_note

Branch type:         implementation
Starting branch:     master, after 11A merges
Expected return branch: master
Branch lifecycle plan: slice11b-pirate-routing; standard discipline.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. GM display surfacing, per section 10.4: current state, recommended
                        branch, source section reference, suggested transition options.
                     2. GM controls: hold / mark suspected / expose / docking request /
                        combat handoff.
                     3. Branch recommendation keyed to pirate_scene_state, referencing
                        docs/02_content/10_pirate_dialogue.md by section - never inlining
                        dialogue text into MAST.
                     4. JUMP-018 pirate_arrival_cover_intact, JUMP-019 pirate_suspected,
                        JUMP-020 pirate_exposed.
                     5. Static tests + registration.

Tests required:      PIRATE-030, PIRATE-031, PIRATE-032, PIRATE-033, PIRATE-034, PIRATE-035
                     JUMPTEST-018, JUMPTEST-019, JUMPTEST-020
                     GOLD-004 (pirate backstop)
                     All verified present in tests/test_coverage_matrix.md.

Acceptance criteria: GM sees state, branch, and source reference at every stage; all GM
                     controls work; the three presets seed their exact states; no dialogue
                     text is embedded in MAST; quick passes.

Expected observations:
                     GM display updates on every transition.
                     Recommended branch changes between intact / suspected / exposed.
                     Each preset lands in the matching pirate_scene_state.

Failure/ambiguous observations:
                     GM display stale after a transition.
                     Recommended branch does not change with state.
                     A preset seeds a state the transition rules consider illegal.
                     Display state set but nothing renders (AMBIGUOUS - same GM-surface
                       question as the Slice 06 status readback; check that finding first).

What remains unproven: Whether the display is actually usable at conversational pace -
                     crewed-session-only, like the Slice 08 beat tracker.

Next action by result:
                     PASS -> Slice 12.
                     Display unusable -> this is a real finding worth routing to the operator
                       before Slice 12, since combat inherits this surface.

Known risks:         This is the slice most likely to tempt an agent into embedding dialogue
                       or auto-judging probe quality. Both violate section 10 ownership.

Do not implement:    Combat mechanics or force authorization (Slice 12).
                     TTS or voice.
                     Auto-evaluation of probe quality - the GM interprets, always.
```

---

## SLICE 12 — Combat transition and pirate outcomes  **(SPIKE REQUIRED)**

**Spike rationale.** Flagged for force authorization, hostile transition, and outcome persistence. Combat is the one place the mission can break irrecoverably mid-session, and `pre_pirate_combat` is the checkpoint that has to catch it.

### Slice 12 Phase A — force authorization and hostile transition spike

```text
Slice ID:            12A
Goal:                Prove that a neutral pirate contact can be made hostile under an explicit
                     authorization gate, that combat state is tracked, and that the outcome
                     survives the transition.

Source docs:         docs/01_design/10_mast_requirements.md section 10 (outcome portions),
                       section 12 (pre_pirate_combat checkpoint)
                     docs/02_content/10_pirate_dialogue.md exposed/combat branches
                     docs/04_implementation_setup/60_mast_api_cookbook.md sections 7, 8
                     tests/SLICE06_VERIFICATION.md (destroy-hook finding - directly relevant)
                     tests/SLICE11_VERIFICATION.md

Files to modify:     scripts/acts/act3_pirate_combat.mast            (new)
                     scripts/main.mast
                     scripts/systems/scenario_control_panel.mast
                     tests/test_act3_pirate_combat_spike_static.py   (new)
                     run_tests.py
                     tests/SLICE12_VERIFICATION.md                   (new)

Runtime owner model: act3_pirate_combat.mast owns combat_* and pirate_outcome_* state and the
                     hostile transition. It reads pirate_scene_state (must be exposed) and
                     never writes Slice 11 state except through a documented handoff call.

State variables needed:
                     pirate_combat_initialized     force_authorization_requested
                     force_authorization_granted   force_authorization_source
                     combat_active                 combat_start_time
                     pirate_hostile                pirate_outcome
                     pirate_outcome_locked         pirate_destroyed_observed
                     pirate_destruction_damage_value
                     pirate_fled_observed          pirate_surrendered_observed
                     combat_fallback_available     combat_spike_status
                     Collision check: no existing shared name begins combat_,
                     force_authorization_, or pirate_outcome_.

Branch type:         spike/experiment
Starting branch:     master, after Slice 11B merges
Expected return branch: master
Branch lifecycle plan: slice12a-combat-spike; merged on acceptance.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: only on acceptance

Implementation tasks:
                     1. Create act3_pirate_combat.mast + wiring.
                     2. Force authorization gate: combat cannot start without an explicit
                        captain/GM authorization; record the source.
                     3. Hostile transition of the existing pirate contact - reusing the
                        contact from Slice 11, not spawning a second one.
                     4. pre_pirate_combat checkpoint write before hostility engages.
                     5. Destruction observation WITH the Slice 06 guard: only treat
                        destruction as a genuine kill when accompanied by a nonzero damage
                        value. Record pirate_destruction_damage_value explicitly.
                     6. Outcome lock: once pirate_outcome is set, later paths cannot rewrite
                        it.
                     7. GM Test Mode spike controls: authorize, force hostile, force each
                        outcome, read state, reset.

Tests required:      PIRATE-040, PIRATE-041, PIRATE-042, PIRATE-043
                     SAVE-007 (checkpoint before pirate combat if feasible)
                     All verified present in tests/test_coverage_matrix.md.

Acceptance criteria: Combat cannot start without authorization; the existing contact becomes
                     hostile without duplicating; pre_pirate_combat checkpoint persists;
                     destruction is distinguishable from GM cleanup; outcome is locked once set.

Expected observations:
                     Attempting combat without authorization is refused and logged.
                     After authorization, the same contact ID becomes hostile.
                     GM cleanup produces a destroy event with zero damage and does NOT set a
                       genuine-kill outcome.
                     A real kill produces nonzero damage and does set it.

Failure/ambiguous observations:
                     Combat starts without authorization - FAIL.
                     A second pirate contact appears on hostile transition.
                     GM cleanup registers as a genuine kill - this is the Slice 06 finding
                       recurring; the guard is the whole point of this task.
                     Outcome overwritten by a later path.

What remains unproven after Phase A:
                     Flee/surrender/board branches, narrative resolution, and continuation
                     into Slice 13 - all Phase B.

Next action by result:
                     PASS -> Phase B.
                     Destroy-hook guard fails -> stop. Slice 06 already documented this;
                       shipping it twice would be a known-defect repeat.

Known risks:         CONFIRMED LIVE (Slice 06, 2026-08-08): sbs.delete_object() fires the same
                       //damage/destroy hook a real kill fires, with zero damage values. Any
                       destruction-keyed outcome here must carry the damage-value guard.
                     Making an existing neutral contact hostile is unproven in the cookbook -
                       expect an API-uncertainty block rather than a guess.

Do not implement:    Flee / surrender / boarding branches (Phase B).
                     Repair resolution (Slice 13).
                     Debrief consequences (Slice 14).
                     Respawning pirates.
```

### Slice 12 Phase B — outcome branches and continuation

```text
Slice ID:            12B
Goal:                Exposed pirates can flee, surrender, fight, be destroyed, or board if
                     enabled - and the mission continues cleanly to repair resolution.

Source docs:         docs/02_content/10_pirate_dialogue.md exposed/combat branches
                     docs/01_design/00_scenario_play_guide.md Scene 12
                     tests/SLICE12_VERIFICATION.md (Phase A results)

Files to modify:     scripts/acts/act3_pirate_combat.mast
                     scripts/systems/scenario_control_panel.mast
                     scripts/systems/story_jump_presets.mast         (JUMP-021)
                     tests/test_act3_pirate_combat_static.py         (new)
                     run_tests.py
                     tests/SLICE12_VERIFICATION.md

Runtime owner model: unchanged. Outcome selection among branches is GM-SUP; mechanical
                     detection (destroyed, fled beyond range) is AUTO with GM fallback.

State variables needed:
                     (Phase A set, plus)
                     pirate_flee_threshold_met      pirate_surrender_offered
                     pirate_boarding_enabled        pirate_boarding_state
                     combat_resolution_status       combat_end_time
                     mission_continues_after_combat

Branch type:         implementation
Starting branch:     master, after 12A merges
Expected return branch: master
Branch lifecycle plan: slice12b-combat-outcomes; standard discipline.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. Flee branch: detection + cleanup of the departing contact.
                     2. Surrender branch, GM-marked.
                     3. Destroyed branch, using the Phase A damage-value guard.
                     4. Boarding branch behind pirate_boarding_enabled, default off.
                     5. Outcome persistence into mission state for Slice 13/14 consumption.
                     6. JUMP-021 combat_active preset.
                     7. Static tests + registration.

Tests required:      PIRATE-044, PIRATE-045, PIRATE-046
                     JUMPTEST-021
                     GOLD-005 (ship destruction and reload)
                     All verified present in tests/test_coverage_matrix.md.

Acceptance criteria: Every enabled outcome branch reachable and recorded; the mission
                     continues to Slice 13 from each; boarding stays off unless explicitly
                     enabled; quick passes.

Expected observations:
                     Each forced outcome sets pirate_outcome once and continues the mission.
                     Fled contact is fully cleaned up.
                     Boarding options absent when disabled.

Failure/ambiguous observations:
                     An outcome dead-ends the mission (no path to Slice 13) - FAIL.
                     Fled contact lingers as a stale object.
                     Boarding reachable while disabled.
                     GOLD-005 requires deliberate Artemis destruction; if reload is not yet
                       built (Slice 15), record GOLD-005 as blocked rather than passed.

What remains unproven: Reload behavior after combat (Slice 15).

Next action by result:
                     PASS -> Slice 13.
                     Any outcome dead-ends -> stop; Slice 13 assumes all paths converge.

Known risks:         GOLD-005 genuinely depends on Slice 15; do not claim it here.

Do not implement:    Repair resolution (Slice 13). Debrief (Slice 14).
                     Checkpoint/reload machinery (Slice 15).
```

---

## SLICE 13 — Repair resolution

```text
Slice ID:            13
Goal:                Halcyon repair, DAMCON outcome, pirate outcome, and mission outcome all
                     resolve, and every major variant reaches return/debrief.

Source docs:         docs/01_design/00_scenario_play_guide.md Scene 14
                     docs/01_design/10_mast_requirements.md sections 9.3 (outcome
                       thresholds and the "repair after total loss" rule), 12
                     docs/01_design/20_gm_operational_notes.md
                     tests/SLICE09_VERIFICATION.md, tests/SLICE12_VERIFICATION.md

Files to modify:     scripts/acts/act3_repair_resolution.mast        (new)
                     scripts/main.mast
                     scripts/systems/story_jump_presets.mast         (JUMP-023/024/025/026)
                     tests/test_act3_repair_resolution_static.py     (new)
                     run_tests.py
                     tests/SLICE13_VERIFICATION.md                   (new)

Runtime owner model: act3_repair_resolution.mast owns halcyon_repair_* and
                     mission_resolution_* state. It READS damcon_outcome and pirate_outcome
                     and must never write them - both are locked by their owning slices.
                     Outcome calculation is AUTO; narration is GM-SUP.

State variables needed:
                     repair_resolution_initialized   halcyon_repair_started
                     halcyon_repair_complete         halcyon_repair_status
                     halcyon_component_installed     halcyon_outcome
                     halcyon_drift_status            mission_resolution_ready
                     mission_resolution_status       mission_outcome_summary
                     damcon_final_status
                     WARNING: repair_complete_text already exists and belongs to Slice 05's
                     controlled-overload repair in the Act I engineering shakedown
                     (finding 1.2). This slice uses halcyon_repair_* exclusively. Do not
                     extend or reuse the bare repair_ prefix.

Branch type:         implementation
Starting branch:     master, after Slice 12B merges
Expected return branch: master
Branch lifecycle plan: slice13-repair-resolution; standard discipline.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. Create act3_repair_resolution.mast + wiring.
                     2. Repair gated on the correct cache component being installed.
                     3. Halcyon outcome computed from repair success and timing.
                     4. DAMCON final status read from the locked damcon_outcome, including
                        the requirements 9.3 rule that repair after total loss may save
                        Halcyon Drift but not Reyes, Park, and Achebe.
                     5. Pirate outcome folded into the mission summary.
                     6. mission_resolution_ready + mission_resolution checkpoint.
                     7. JUMP-023 repair_resolution_clean, JUMP-024 repair_resolution_hypoxic,
                        JUMP-025 repair_resolution_total_loss, JUMP-026 return_transit.
                     8. Static tests + registration.

Tests required:      JUMPTEST-017, JUMPTEST-018, JUMPTEST-019, JUMPTEST-020
                     SAVE-008 (checkpoint at mission resolution)
                     GOLD-001, GOLD-002, GOLD-006 (Halcyon Drift loss)
                     All verified present in tests/test_coverage_matrix.md.
                     Note: JUMPTEST-017..020 are defined by the range statement at
                     40_admin_testing_plan.md:583, not as literal tokens.
                     GAP: JUMP-023/024/025/026 have no corresponding JUMPTEST IDs - see
                     finding 3.6. Validate those four presets against the section 10
                     standard procedure and record under GOLD-001/002/006 until IDs exist.

Acceptance criteria: All three DAMCON bands produce distinct, correct resolutions; repair
                     after total loss saves the ship but not the crew; every pirate outcome
                     folds in without dead-ending; mission_resolution checkpoint persists;
                     all four presets seed valid states; quick passes.

Expected observations:
                     clean_survival / hypoxic_survival / total_loss each produce a distinct
                       mission_outcome_summary.
                     Repair completing after total_loss still records crew loss.
                     Each preset lands in the matching resolution state.

Failure/ambiguous observations:
                     A DAMCON band produces the wrong resolution.
                     Repair after total loss silently revives the crew - FAIL; this violates
                       the irreversibility contract in requirements 9.3 and section 12.
                     A pirate outcome leaves resolution unreachable.
                     Resolution state set but no summary renders (AMBIGUOUS).

What remains unproven: Debrief presentation (Slice 14). Reload of resolution state (Slice 15).

Next action by result:
                     PASS -> Slice 14.
                     Crew revival on late repair -> stop immediately; this is the single most
                       important irreversibility rule in the mission.

Known risks:         This slice reads two locked outcomes it must not write; an agent
                       "fixing" an outcome here would silently break Slices 09 and 12.
                     repair_ prefix collision (finding 1.2).

Do not implement:    Debrief display or ratings (Slice 14).
                     Auto-grading of qualification.
                     Any write to damcon_outcome or pirate_outcome.
```

---

## SLICE 14 — Debrief support

```text
Slice ID:            14
Goal:                Debrief clips and runtime evidence support GM assessment, without the
                     runtime ever grading the crew.

Source docs:         docs/01_design/10_mast_requirements.md section 15
                     docs/01_design/30_qualification_cards.md
                     docs/02_content/50_debrief_script.md
                     docs/02_content/40_dillon_clips.md Clips 10-12
                     docs/02_content/30_anderson_clips.md Clip 3 (optional close)
                     tests/SLICE13_VERIFICATION.md

Files to modify:     scripts/systems/debrief_support.mast            (new)
                     scripts/main.mast
                     scripts/systems/story_jump_presets.mast         (JUMP-027)
                     tests/test_debrief_support_static.py            (new)
                     run_tests.py
                     tests/SLICE14_VERIFICATION.md                   (new)

Runtime owner model: debrief_support.mast owns debrief_* state and the support display.
                     Ownership is GM-DRIVE with AUTO support (requirements section 15): the
                     runtime triggers clips and shows evidence; the GM assigns every rating.
                     The runtime must not compute PASS / PARTIAL / NEEDS RETEST.

State variables needed:
                     debrief_initialized            debrief_active
                     debrief_support_status         debrief_station_evidence
                     debrief_gm_notes               debrief_rating_helm
                     debrief_rating_weapons         debrief_rating_science
                     debrief_rating_comms           debrief_rating_engineering
                     debrief_rating_captain         debrief_ratings_complete
                     dillon_clip_10_stub_sent       dillon_clip_11_stub_sent
                     dillon_clip_12_stub_sent       anderson_clip_3_stub_sent
                     qualification_event_log_status
                     Collision check: no existing shared name begins debrief_. Note
                     qualification_event_log is referenced by D3-012 in the admin plan -
                     confirm its owner before adding to it.

Branch type:         implementation
Starting branch:     master, after Slice 13 merges
Expected return branch: master
Branch lifecycle plan: slice14-debrief-support; standard discipline.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. Create debrief_support.mast + wiring.
                     2. Dillon Clip 10 text stand-in on mission resolution complete.
                     3. Station observation evidence display, sourced from the qualification
                        event log.
                     4. GM notes surface by station/item.
                     5. GM rating entry per station - entry only, never computation.
                     6. Dillon Clip 11 text stand-in gated on damcon_outcome = total_loss.
                     7. Dillon Clip 12 close + optional Anderson Clip 3.
                     8. JUMP-027 debrief preset.

Tests required:      DEBRIEF-001, DEBRIEF-002, DEBRIEF-003, DEBRIEF-004, DEBRIEF-005,
                     DEBRIEF-006, DEBRIEF-007, DEBRIEF-008, DEBRIEF-009, DEBRIEF-010,
                     DEBRIEF-011, DEBRIEF-012
                     All verified present in tests/test_coverage_matrix.md.
                     GAP: JUMP-027 has no corresponding JUMPTEST ID - see finding 3.6.
                     Validate the preset against the section 10 standard procedure and
                     record under DEBRIEF-001 until an ID is assigned.

Acceptance criteria: All clips deliver once each and only under their correct conditions;
                     evidence display reflects actual runtime observations; GM can record a
                     rating per station; the runtime produces no overall grade; quick passes.

Expected observations:
                     Clip 10 on resolution; Clip 11 only on total_loss; Clip 12 at close.
                     Evidence display shows real logged observations, not placeholders.
                     Ratings persist as entered.

Failure/ambiguous observations:
                     Clip 11 fires on a non-total-loss run.
                     Any clip fires twice.
                     Evidence display shows nothing after a full run (AMBIGUOUS - is the
                       event log empty, or is the display broken? Distinguish before judging).
                     The runtime emits an overall grade - FAIL, explicit violation of
                       requirements section 15.

What remains unproven: Whether the evidence display is genuinely useful to a GM - crewed-run
                     judgment, not a static property.

Next action by result:
                     PASS -> Slice 15.
                     Auto-grading present -> remove before merge; this is a stated design
                       prohibition, not a preference.

Known risks:         The qualification event log must have been populated by earlier slices;
                       if it is empty, this slice has nothing to display and the gap belongs
                       upstream, not here.

Do not implement:    Automatic PASS/PARTIAL/NEEDS RETEST computation.
                     Audio playback.
                     Checkpoint/reload (Slice 15).
```

---

## SLICE 15 — Checkpoint/reload hardening  **(SPIKE REQUIRED)**

**Spike rationale.** Flagged for checkpoint payload round-trip and irreversible state preservation. This slice depends on state from every prior slice, and it is the one place where getting it wrong turns reload into a tactical undo — explicitly forbidden by `10_mast_requirements.md` section 12.

### Slice 15 Phase A — checkpoint payload round-trip spike

```text
Slice ID:            15A
Goal:                Prove a checkpoint payload can be written and restored faithfully, and
                     that irreversible state survives reload unchanged.

Source docs:         docs/01_design/10_mast_requirements.md section 12 (full)
                     docs/01_design/40_admin_testing_plan.md section 15
                     All prior SLICEnn_VERIFICATION.md records (state inventory)

Files to modify:     scripts/systems/checkpoint_system.mast          (new)
                     scripts/lib/checkpoint_helpers.mast             (new - see 1.6)
                     scripts/main.mast
                     scripts/systems/scenario_control_panel.mast     (GM spike controls)
                     tests/test_checkpoint_spike_static.py           (new)
                     run_tests.py
                     tests/SLICE15_VERIFICATION.md                   (new)

Runtime owner model: checkpoint_system.mast owns checkpoint_* and reload_* state and the
                     save/restore routines. Checkpoint writes are AUTO; reload is
                     GM-OVERRIDE (requirements section 12). Every other slice's state is
                     read and restored by this system but owned elsewhere - this file must
                     never be the definitional owner of another slice's variable.

State variables needed:
                     checkpoint_system_initialized  checkpoint_last_written
                     checkpoint_last_write_time     checkpoint_write_count
                     checkpoint_payload_status      checkpoint_available_list
                     reload_requested               reload_confirmed
                     reload_source_checkpoint       reload_count
                     reload_status                  reload_irreversible_preserved
                     checkpoint_spike_status        checkpoint_spike_result
                     Collision check: no existing shared name begins checkpoint_ or reload_.
                     Note last_checkpoint (no prefix) already exists and is written by the
                     Act I seed helpers - do not repurpose it; treat it as an input.

Branch type:         spike/experiment
Starting branch:     master, after Slice 14 merges
Expected return branch: master
Branch lifecycle plan: slice15a-checkpoint-spike; merged on acceptance.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: only on acceptance

Implementation tasks:
                     1. Create checkpoint_helpers.mast: generic payload capture/restore.
                     2. Create checkpoint_system.mast; implement the 8 canonical checkpoints
                        from requirements section 12 (post_drill_1, post_drill_2,
                        post_drill_3, post_anderson_orders, post_halcyon_arrival,
                        post_cascade, pre_pirate_combat, mission_resolution).
                     3. Payload contents per section 12: phase/scene/beat, ship state, entity
                        states, resources, active timers, pirate state, cache state,
                        qualification event log.
                     4. Irreversibility filter - on restore, explicitly DO NOT undo:
                        DAMCON deaths, committed Halcyon damage/loss, expended or converted
                        torpedoes, qualification observations, visible pirate exposure.
                     5. GM Test Mode spike controls: write checkpoint, list, restore, diff
                        before/after, read status.
                     6. Trace breadcrumbs on every write and restore.

Tests required:      SAVE-001, SAVE-002, SAVE-003, SAVE-004, SAVE-005, SAVE-006,
                     SAVE-007, SAVE-008
                     SAVE-010, SAVE-011, SAVE-012, SAVE-013, SAVE-014, SAVE-015, SAVE-016
                     DAMCON-005, DAMCON-006 (deferred from Slice 09A)
                     All verified present in tests/test_coverage_matrix.md. The SAVE series
                     has deliberate numbering gaps between these blocks; those numbers are
                     unassigned in the admin plan and must not be invented or cited.

Acceptance criteria: Each checkpoint writes and restores; restored state matches pre-save
                     state for reversible fields; every irreversible field is preserved
                     unchanged; the DAMCON timer restores correctly; quick passes.

Expected observations:
                     Diff before/after restore shows reversible fields restored and
                       irreversible fields untouched.
                     DAMCON timer resumes with correct elapsed time.
                     Restoring an earlier checkpoint does not resurrect a lost DAMCON team.

Failure/ambiguous observations:
                     Reload undoes a DAMCON death - FAIL, the central prohibition.
                     Reload restores expended torpedoes - FAIL.
                     Timer restores with zero or reset elapsed - breaks outcome arithmetic.
                     Payload writes but restore silently no-ops (AMBIGUOUS - check whether
                       the payload is empty or the restore path is unreached).

What remains unproven after Phase A:
                     Catastrophic-failure recovery and the deliberate ship-destruction test -
                     Phase B.

Next action by result:
                     PASS -> Phase B.
                     Any irreversibility violation -> stop. This is the slice's entire reason
                       to exist.

Known risks:         Depends on state from all 14 prior slices; an incomplete payload is the
                       likeliest defect and the hardest to notice.
                     Timer restoration interacts with the Slice 09 run-ID guard - restoring a
                       timer must not leave two running.

Do not implement:    Ship-destruction recovery test (Phase B).
                     Any change to another slice's state ownership.
                     Reload as a tactical convenience feature.
```

### Slice 15 Phase B — catastrophic recovery

```text
Slice ID:            15B
Goal:                Reload works under catastrophic failure and is demonstrably not a
                     tactical undo.

Source docs:         docs/01_design/10_mast_requirements.md section 12
                     docs/01_design/40_admin_testing_plan.md sections 15, 18 (GOLD-005)
                     tests/SLICE15_VERIFICATION.md (Phase A results)

Files to modify:     scripts/systems/checkpoint_system.mast
                     scripts/systems/scenario_control_panel.mast
                     tests/test_checkpoint_system_static.py          (new)
                     run_tests.py
                     tests/SLICE15_VERIFICATION.md

Runtime owner model: unchanged. Reload confirmation is GM-OVERRIDE and must require an
                     explicit confirm step - never a single mis-clickable control.

State variables needed:
                     (Phase A set, plus)
                     reload_confirmation_pending    reload_confirmation_text
                     ship_destruction_observed      catastrophic_recovery_status

Branch type:         implementation
Starting branch:     master, after 15A merges
Expected return branch: master
Branch lifecycle plan: slice15b-catastrophic-recovery; standard discipline.
Runtime/live-smoke allowed from this branch: yes
Merge-back required: yes

Implementation tasks:
                     1. Reload confirmation flow with an explicit confirm step.
                     2. Ship destruction detection, applying the Slice 06 damage-value guard.
                     3. Catastrophic recovery path from the most recent valid checkpoint.
                     4. Deliberate ship-destruction test procedure, documented for the
                        operator with expected/failure observations.
                     5. Static tests + registration.

Tests required:      SAVE-020, SAVE-021, SAVE-022, SAVE-023, SAVE-024
                     SAVE-030, SAVE-031, SAVE-032, SAVE-033
                     GOLD-005 (ship destruction and reload)
                     All verified present in tests/test_coverage_matrix.md.

Acceptance criteria: Artemis destruction is detected; recovery restores the last valid
                     checkpoint; irreversible consequences survive the recovery; reload
                     requires explicit confirmation; quick passes.

Expected observations:
                     Deliberate destruction triggers the recovery offer, not a silent reset.
                     Confirming restores the correct checkpoint with irreversibles intact.
                     Declining leaves the mission in its failed state.

Failure/ambiguous observations:
                     Recovery fires automatically without confirmation - FAIL.
                     Recovery restores a checkpoint newer than the destruction.
                     Irreversible state lost during catastrophic recovery specifically, even
                       though Phase A proved it for normal reload.

What remains unproven: Nothing structural - this is the last state-machine slice. Remaining
                     unknowns are session-level and belong to Slice 16.

Next action by result:
                     PASS -> Slice 16.
                     Irreversibles lost only on the catastrophic path -> fix before Slice 16;
                       Phase A passing does not cover this path.

Known risks:         GOLD-005 requires deliberately destroying Artemis in live Cosmos; script
                       the operator request carefully with full expected/failure observations
                       per AGENTS.md section 9.

Do not implement:    Regression harness (Slice 16).
                     Any new gameplay state.
```

---

## SLICE 16 — Regression harness and pre-session workflow

```text
Slice ID:            16
Goal:                Testing becomes routine and lightweight: a GM or developer can validate
                     session readiness in minutes rather than replaying the mission.

Source docs:         docs/01_design/40_admin_testing_plan.md sections 19, 20, 21
                     docs/04_implementation_setup/70_agent_handoff_protocol.md
                     tests/test_coverage_matrix.md
                     All SLICEnn_VERIFICATION.md records

Files to modify:     tests/regression_matrix.md                      (new)
                     tests/regression_log_template.md                (new)
                     tests/known_issues.md                           (new)
                     docs/00_project/20_build_start_checklist.md     (pre-session section)
                     run_tests.py                                    (regression grouping)
                     tests/SLICE16_VERIFICATION.md                   (new)

Runtime owner model: No runtime ownership - this slice adds no MAST and no shared state. It
                     is tooling and documentation only. That is why it is last and why it is
                     the lowest-risk slice in the remaining build.

State variables needed:
                     None. This slice introduces no shared MAST variables.

Branch type:         implementation
Starting branch:     master, after Slice 15B merges
Expected return branch: master
Branch lifecycle plan: slice16-regression-harness; standard discipline.
Runtime/live-smoke allowed from this branch: yes, for the pre-session checklist dry run
Merge-back required: yes

Implementation tasks:
                     1. Regression matrix mapping each change type to the minimum test set
                        that must re-run (admin plan section 19).
                     2. Regression log template.
                     3. Known-issues template, seeded with the open findings carried in the
                        verification records - including the Slice 06 destroy-hook finding
                        and the JUMP-008 preset-naming conflict.
                     4. Pre-session checklist per admin plan section 20.
                     5. Optional grouping in run_tests.py so a subsystem's tests can be run
                        without the whole suite.
                     6. Final pass over tests/test_coverage_matrix.md so every ID reflects
                        real end-state coverage.

Tests required:      PRE-001, PRE-002, PRE-003, PRE-004, PRE-005, PRE-006,
                     PRE-007, PRE-008, PRE-009, PRE-010, PRE-011, PRE-012
                     All verified present in tests/test_coverage_matrix.md.

Acceptance criteria: Pre-session checklist completes in minutes; the regression matrix
                     names a real minimum test set per change type; known issues are current;
                     the coverage matrix honestly reflects end state; quick passes.

Expected observations:
                     A dry run of the checklist surfaces any unready condition.
                     Changing one subsystem points at a bounded test set, not the full suite.

Failure/ambiguous observations:
                     The checklist passes on a knowingly broken build - it is not discriminating.
                     The coverage matrix claims live coverage that no verification record
                       supports - this is the exact overclaim the evidence rules forbid, and
                       it is worth auditing deliberately at this point.

What remains unproven: Nothing this slice can prove alone; its value shows up in the next
                     session that uses it.

Next action by result:
                     PASS -> mission is build-complete pending full crewed validation runs.

Known risks:         The temptation at this stage is to mark the coverage matrix green.
                     Most IDs will legitimately still be static-only or blocked, because
                     crewed live smoke is the scarce resource in this project.

Do not implement:    Any new gameplay behavior.
                     Any new shared MAST state.
                     Auto-grading.
```

---

# 3. Open items requiring operator decision

These are surfaced, not resolved, per `70_agent_handoff_protocol.md` section 8.

1. **Where these packets should ultimately live.** They are in `docs/04_implementation_setup/` to respect the design-doc edit boundary. If the operator prefers them merged into `docs/01_design/50_implementation_slice_plan.md` section 3, that is a design-doc change and needs explicit approval.

2. **Slice 07 split.** The slice plan describes Slice 07 as one slice; this packet splits it into 07A/07B on the section 3.2 sizing rule (11 tasks > 8). Confirm the split, or confirm that the sizing rule should bend here.

3. **Gate/fallback pairs for Acts II/III are proposals, not canon.** Section 8.9 covers Act I only. If the operator wants an Acts II/III gate map with the same authority, that is a design-doc addition and belongs in `10_mast_requirements.md`.

4. **JUMP-008 conflict, still open** from the Slice 06/Task 6 work. `engineering_shakedown_complete` has no canonical JUMP number. Slices 09–14 add JUMP-011 through JUMP-027 around it, so the gap becomes more visible as the build proceeds.

5. **`qualification_event_log` ownership.** Referenced by D3-012 in the admin plan and consumed by Slice 14, but no current slice packet claims to create it. It may belong to Slice 05/06 retroactively, or to a small insertion slice. Needs a decision before Slice 14.

6. **Six JUMP presets have no validation test ID.** `40_admin_testing_plan.md` section 10 states "Each story jump must have a validation test," and defines `JUMPTEST-001 through JUMPTEST-021 correspond to JUMP-001 through JUMP-021`. But sections 6.1–6.2 define **27** presets, JUMP-001 through JUMP-027. So **JUMP-022 (cache_selection), JUMP-023/024/025 (repair resolutions), JUMP-026 (return_transit), and JUMP-027 (debrief)** have no corresponding JUMPTEST ID, contradicting the section 10 rule.

   Found while writing these packets: Slices 10, 13, and 14 each need to validate a preset in that range and had nothing valid to cite. The affected packets now name the gap explicitly and fall back to a neighbouring subsystem ID rather than inventing a JUMPTEST number, because inventing one would put an ID in a packet that the coverage-matrix check would then have to be weakened to accept.

   Resolution is a design-doc edit (extend the JUMPTEST range to 027 in `40_admin_testing_plan.md` section 10), so it is routed to the operator rather than made here. Six IDs, mechanical change.
