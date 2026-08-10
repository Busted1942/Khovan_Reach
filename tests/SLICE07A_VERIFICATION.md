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
6. Comms reports the fix → `khovan_act2_complete_distress_localization` records the source and hands off to Phase B.

## GM Controls

JUMP-011 Anderson Orders and JUMP-012 Distress Localized, both Test-Mode gated, both bumping Act I generations so a seed cannot leave a stale Act I timer running.

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
- Localization has a working reported path and records its source.
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

**2. Anderson has no sender object.** He borrows `tarsis_station_id`, exactly as Dillon does. If Tarsis is out of Comms range during the pivot, the guarded wrapper skips the message and writes the safe breadcrumb rather than failing — but the orders would then never appear. Watch for `[KHOVAN ACT2 SAFE]` in the trace.

**3. The Comms route rides Tarsis.** Play guide Scene 5 has Artemis returning toward Tarsis, so this should hold, but a crew that has flown far from Tarsis may lose the route. The GM jump presets are the backstop.

## Next Action

Operator live smoke. The first run only needs to answer three things:

1. Does `[KHOVAN ACT2 001]` appear at startup, and does the handoff observer tick?
2. On Act I completion, does `[KHOVAN ACT2 002] mission_phase=act_2` fire without GM action?
3. Does Anderson's message render, and does the Tarsis Comms route show the Act II options?

If 3 fails but 1 and 2 pass, the pivot works and only the message surface needs work — use JUMP-011 to continue.

---

# Live smoke log (append-only)

_No live run yet._
