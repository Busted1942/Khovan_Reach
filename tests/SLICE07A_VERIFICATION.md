# Slice 07A Verification — Act II pivot

Goal: mission pivots from Act I training to Act II live operation. Anderson delivers orders, the mission phase advances, and the distress signal is localized.

## Status

implemented-live-unproven — all packet tasks are built and statically covered. **No live Cosmos run has executed any of it.** Status is reviewer-set per handoff protocol 4.3.

## Source Sections Used

- `docs/01_design/00_scenario_play_guide.md`, Scenes 5, 6, 7.
- `docs/01_design/10_mast_requirements.md`, section 7 scene ownership (Scene 5 AUTO, Scene 6 AUTO, Scene 7 AUTO + GM-SUP).
- `docs/02_content/30_anderson_clips.md`, Clip 1 New Orders.
- `docs/02_content/40_dillon_clips.md`, Clip 8 Pivot Acknowledgment.
- `docs/04_implementation_setup/80_slice_packets_07_16.md`, Slice 07 Phase A packet.
- `tests/SLICE06_VERIFICATION.md`, the `drone_contact_act2_ready` handoff this slice consumes.

## Cookbook Patterns Used

- section 4.1 `[LIVE]` — shared state at file top; multi-line copy in `shared` vars only.
- section 4.3 `[LIVE]` — `await task_schedule(label, {...})` and fire-and-forget scheduling.
- section 4.4 `[LIVE]` — `default` parameter declarations.
- section 5.1 `[LIVE]` — run-ID guard on the handoff observer; generation bump to invalidate Act I timers.
- section 5.2 `[LIVE]` — bounded polling observer with tick ceiling and fallback.
- section 6.1 `[LIVE]` — Comms route gated on a selected station role.
- section 6.2 `[LIVE]` — `startup_sender` / `startup_title` split so the header reads `Speaker: Role`.
- section 6.2 `[LIVE]` — `comms_broadcast` objective channel for player-facing instruction.

## Files Touched

- `scripts/acts/act2_pivot.mast` (new)
- `scripts/main.mast` (import + init order)
- `scripts/systems/story_jump_presets.mast` (JUMP-011, JUMP-012)
- `tests/test_act2_pivot_static.py` (new)
- `tests/test_story_jump_presets_static.py` (placeholder guard, graduated ids)
- `run_tests.py` (register test file)

## State Variables

`act2_pivot_initialized`, `act2_pivot_status`, `act2_last_progression_summary`, `act2_pivot_run_id`, `act2_handoff_observer_ticks`, `act2_handoff_fallback_available`, `anderson_orders_delivered`, `anderson_clip_1_stub_sent`, `anderson_orders_ack_status`, `anderson_orders_prompt_run_id`, `anderson_orders_text`, `distress_signal_detected`, `distress_localized`, `distress_localization_status`, `distress_science_gate_status`, `distress_localization_fallback_available`, `distress_localization_source`, `dillon_clip_8_stub_sent`, plus four `*_text` copy variables.

Collision check: the duplicate-shared check in `run_tests.py` passes, and no name outside this file begins `act2_`, `anderson_`, or `distress_`.

## Runtime Flow

1. `khovan_act2_initialize_pivot` runs from `main.mast` after Slice 06 init and starts the handoff observer.
2. `khovan_act2_watch_act1_handoff` polls `drone_contact_act2_ready` every 5 seconds, run-ID guarded, ceiling 900 ticks (~75 min).
3. On handoff: all Act I run-IDs are bumped, `mission_phase` becomes `act_2`, scene 5.
4. Anderson Clip 1 text goes out through the guarded safe-message wrapper; `last_checkpoint` becomes `post_anderson_orders`.
5. Comms acknowledges via the Tarsis route → Dillon Clip 8 → distress-localization route opens (scene 7).
6. The automatic proximity sweep resolves the signal → Artemis Science reports the fix to the Captain → `khovan_act2_complete_distress_localization` records the source and hands off to Phase B. GM Scenario Control retains recovery; player Comms does not.

## GM Controls

JUMP-011 Anderson Orders and JUMP-012 Distress Localized, both Test-Mode gated, both bumping Act I generations so a seed cannot leave a stale Act I timer running. `GM: Record Science Signal Fix` is the non-player fallback for a failed proximity sweep.

## Player-Facing Behavior

Anderson's orders, Dillon's pivot note, the localization prompt, and the localization result. All follow the addressee convention and are enforced by `tests/test_mission_text_contract.py` rather than pinned here.

## Tests/Static Checks

`tests/test_act2_pivot_static.py` — 17 checks across wiring, guards, packet scope, and jump presets. Two are structural rather than string pins:

- **Act I run-ID completeness.** Reads every `shared *run_id` declared in `scripts/acts/act1_*.mast` and asserts each is bumped in `khovan_act2_invalidate_act1_timers`. Adding an Act I timer without invalidating it fails the build.
- **Phase-transition ownership.** Scans every MAST file and asserts only `act2_pivot.mast` writes `mission_phase = "act_2"`.

`python run_tests.py quick`: PASS, 217 checks (12 harness, 205 Python tests), 0 failures, 0 warnings, compile preflight included. `tools/review_gate.py --base master`: MECHANIZED PASS.

## Acceptance Covered

- Act II is reachable from the Slice 06 end state without GM intervention (observer path) — **statically**.
- Anderson Clip 1 and Dillon Clip 8 are each duplicate-suppressed.
- Localization has an automatic sensor path plus a GM-only recovery, records its source, and updates the Captain's objective without sending a localization Comms message.
- `post_anderson_orders` checkpoint is written.
- JUMP-011/012 seed valid states and invalidate Act I timers.
- No design or content doc modified.

## Acceptance Not Covered

- **Everything live.** No Cosmos run has executed this slice.
- **Whether the Act II Comms route renders.** It gates on `tarsis_station` plus `mission_phase == "act_2"`. The Tarsis route is live-proven, but this compound condition is not, and Slice 06 showed a route can evaluate while the player sees a different panel.
- **Whether the handoff observer fires.** Its 900-tick ceiling has never been exercised, and neither has the 5-second period over a full Act I.
- **Whether Anderson renders as a speaker.** He is a new sender with no station binding of his own; the message borrows `tarsis_station_id` as sender id, the same workaround Dillon uses. See Known Risks.
- **Whether the distress localization design is right.** See Known Risks.

## Known Risks/API Uncertainties

**1. Distress localization is a reported route, not a Science scan — a design question for the operator.**

The packet says "Science can localize the distress signal", but the packet also puts Halcyon's spawn in Phase B, and the Acts II/III gate map rates the Science-scan row *against the Halcyon object*. There is no object to scan in Phase A. Play guide Scene 7 puts the source at the edge of sensor range with no visual, and `10_mast_requirements.md` section 7 classifies Scene 7 as AUTO + GM-SUP.

Built as a Comms-reported fix on the Tarsis route, with `distress_science_gate_status` recording that no contact object exists until Phase B. **If the intent was a Science console action, this needs a design ruling and a Phase B rework** — routed, not decided.

**Superseded 2026-08-23 by explicit operator direction.** The coordinate-based proximity sweep remains the automatic detector because no Phase A contact exists to scan, but the report and ownership are now Science-facing. The player Comms completion route was removed; only a GM recovery remains. Live rendering of the shipboard Science sender is still unproven.

**Superseded again 2026-08-23 by the operator's live screenshot and direction to drop the message.** Localization now changes runtime state and the Captain's objective silently. Science's player-facing report occurs during the Halcyon investigation/hail sequence, not as an automatic Comms-style message at localization.

**2. Anderson has no sender object.** He borrows `tarsis_station_id`, exactly as Dillon does. If Tarsis is out of Comms range during the pivot, the guarded wrapper skips the message and writes the safe breadcrumb rather than failing — but the orders would then never appear. Watch for `[KHOVAN ACT2 SAFE]` in the trace.

**3. The Comms route rides Tarsis.** Play guide Scene 5 has Artemis returning toward Tarsis, so this should hold, but a crew that has flown far from Tarsis may lose the route. The GM jump presets are the backstop.

## Findings routed to the operator (2026-08-23)

### Automatic localization report appeared as an unwanted Comms message

Claim touched: this record's superseded claim that the automatic sweep and GM recovery should render an `Artemis Science: Sensor Report` localization message.
Evidence class: observed
Disposition: amended
Owner: operator, for live acceptance that localization is silent while the Captain's objective still advances
Dependency: restart Cosmos, cross the localization threshold once organically and once through the GM recovery

The operator screenshot shows the automatic Science report occupying the Comms message feed after localization and explicitly directs that it be dropped. The completion path now records localization and updates the Captain-directed objective without sending that message. The later Halcyon investigation still gives Science the report and preserves the Captain-ordered hail path.

### JUMP-011 suppressed the event it was meant to expose

Claim touched: `tests/TEST_PLAN_2026-08-10.md` section 4.1 and this record's Next Action claim that JUMP-011 can continue past an Anderson message-surface failure.
Evidence class: observed
Disposition: amended
Owner: operator, for live acceptance of the repaired jump
Dependency: restart Cosmos on the repaired branch and execute JUMP-011 twice

The operator observed that the JUMP-011 button appeared to do nothing. Static inspection found that its seed set `anderson_clip_1_stub_sent = True` and `anderson_orders_ack_status = "acknowledged"`, suppressing both the normal Anderson delivery and the Tarsis acknowledgment option. The repair now performs a clean Act II reset, invokes the normal Anderson-delivery label, and leaves acknowledgment pending. Recommendation: accept only after two executions visibly deliver Anderson's packet and expose `Acknowledge Anderson Orders`; this remains observed, not measured, until that rerun.

### JUMP-012 reported localization before producing a complete arrival state

Claim touched: this record's claim that JUMP-012 seeds a valid localized state and `scripts/systems/story_jump_presets.mast`'s former target of Scene 7.
Evidence class: static
Disposition: amended
Owner: operator, for live acceptance of the repaired jump
Dependency: restart Cosmos and execute JUMP-012 twice

The seed set `distress_localized = True` but left contact creation to a background observer, so the button could appear inert and its summary could report Scene 7 while automatic flow was entering Scene 8. The repair now waits for deferred cleanup, spawns Halcyon explicitly through the common path, promotes the runtime to Scene 8, and validates both `distress_localized` and `halcyon_spawned` before reporting success. Recommendation: accept only when both runs leave exactly one selectable Halcyon contact and a Captain-directed scan/hail objective.

### JUMP-011 did not establish a complete post-Act I success state

Claim touched: this record's GM Controls claim that JUMP-011 seeds a valid Act II entry state.
Evidence class: static
Disposition: amended
Owner: operator, for live acceptance of the cleanup barrier and seeded postconditions
Dependency: execute JUMP-011 once with Drone 01 active, once with Drone 02 and its fleet active, and once while a Kestrel/Tarsis hold is active

The earlier repair invalidated Act I timers and reset Act II state, but it did not remove every Act I object or positively record every prior gate as successful. The amended shared seed now records the generator/Tarsis and Engineering success postconditions without advancing into another drill, deletes Drone 01, Drone 02, Drone 02's separate behavior-tree fleet, the GM target spike, and the subsystem-control target, then waits up to five simulation seconds for those exact captured object ids to leave the engine. Only after that barrier settles does it mark both drone drills complete, disable further Act I production, release the mechanical hold, and invalidate the newly seeded Act I observers. JUMP-011, JUMP-012, and JUMP-013 all use this base and all three now include the settled Act I cleanup in their runtime-success contract; JUMP-013 additionally requires its Halcyon cleanup barrier to settle. Recommendation: accept when each preset leaves no old drone/fleet contact, Artemis undocked and controllable, and only the contact/message state appropriate to that preset.

### Player Comms incorrectly owned the distress localization report

Claim touched: this record's Runtime Flow step 6 and Known Risk 1, which described the Tarsis Comms report as the implemented localization completion path.
Evidence class: static
Disposition: amended
Owner: operator, for live acceptance of the Science report and Tarsis trigger explanation
Dependency: acknowledge Anderson organically, cross the proximity threshold, and observe the message headers and available Tarsis options

The operator directed that Science, not Comms or Dillon, report the located signal and that the Captain be told to investigate it. The `Report Distress Localization` player option and its completion source were removed. Tarsis Command Relay now uses the acknowledgment response to explain fictionally that entering the long-range sensor envelope lets Science resolve the source; the automatic sweep then sends `Artemis Science: Sensor Report` to the Captain and directs investigation. A GM-only `GM: Record Science Signal Fix` action preserves the required fallback without giving player Comms ownership. Recommendation: accept only if Tarsis shows no localization option, its acknowledgment explains the trigger, and the automatic and GM-recovery paths both render the same Science-owned report.

## Next Action

Operator live smoke. The first run only needs to answer three things:

1. Does `[KHOVAN ACT2 001]` appear at startup, and does the handoff observer tick?
2. On Act I completion, does `[KHOVAN ACT2 002] mission_phase=act_2` fire without GM action?
3. Does Anderson's message render, and does the Tarsis Comms route show the Act II options?

If 3 fails but 1 and 2 pass, the pivot works and only the message surface needs work — use JUMP-011 to continue.

---

# Live smoke log (append-only)

_No live run yet._
