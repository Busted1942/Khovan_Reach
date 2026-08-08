# Slice 06 Verification

Goal: build Slice 06 Drone 01 controlled disable and Drone 02 live-fire target, starting with the mandatory target subsystem-damage spike before implementing the full drill.

## Status

implemented-live-unproven — Phase A is accepted live evidence. Phase B production code and static regression coverage are present, but no Phase B crewed Cosmos smoke has run.

## Source Sections Used

- `AGENTS.md`, branch lifecycle, source authority, and operator test expectations.
- `docs/00_project/00_source_index.md`, active source map.
- `docs/01_design/00_scenario_play_guide.md`, Scene 4A Drone 01 and Scene 5A Drone 02.
- `docs/01_design/10_mast_requirements.md`, sections 8.5 and 8.6.
- `docs/01_design/40_admin_testing_plan.md`, ACT1-019 through ACT1-024 and D2/D3 checks.
- `docs/01_design/50_implementation_slice_plan.md`, Slice 06 and mandatory target subsystem-damage spike.
- `docs/02_content/40_dillon_clips.md`, Clips 4 through 7.
- `docs/04_implementation_setup/10_mast_file_lessons.md`, target subsystem-damage spike warning.
- `tests/SLICE04_VERIFICATION.md` and `tests/SLICE05_VERIFICATION.md`, accepted prior-slice state and GM jump handoff.

## Files Touched

- `scripts/acts/act1_drone_contact_fire.mast`
- `scripts/main.mast`
- `scripts/systems/scenario_control_panel.mast`
- `run_tests.py`
- `tests/test_act1_drone_contact_fire_static.py`
- `tests/SLICE06_VERIFICATION.md`

## State Variables

Phase A spike state currently owns:

- `drone_contact_fire_initialized`
- `drone_contact_sequence_status`
- `drone_contact_detection_mode`
- `drone_contact_last_step`
- `drone_contact_source_decision`
- `drone_target_spike_available`
- `drone_target_spike_active`
- `drone_target_spike_target_id`
- `drone_target_spike_navproxy_id`
- `drone_target_spike_spawn_count`
- `drone_target_spike_cleanup_count`
- `drone_target_spike_status`
- `drone_target_spike_scan_observed`
- `drone_target_spike_hail_observed`
- `drone_target_spike_weapons_selected`
- `drone_target_spike_damage_observed`
- `drone_target_spike_manual_subsystem_hit_observed`
- `drone_target_spike_manual_subsystem`
- `drone_target_spike_weapons_damage_value`
- `drone_target_spike_engines_damage_value`
- `drone_target_spike_destroyed_observed`
- `drone_target_spike_stock_comms_menu_observation`
- `drone_target_spike_training_safe_observation`
- `drone_target_spike_result`
- `drone_target_spike_blocker`
- `drone_target_spike_fallback`

Phase B production state is isolated from the spike: `drone_contact_sequence_run_id`, `drone_contact_production_available`, `drone_contact_profile_route`, `drone_contact_act2_ready`, `drone_contact_act2_handoff_status`, `drone_contact_cultural_packet_sent`, all `drone_01_*` and `drone_02_*` shared variables declared in `act1_drone_contact_fire.mast`. Drone 01 begins 15 km from Tarsis Training Beacon and every reset adds 5 km. Do not create a duplicate legacy `drill_2_*` or `drill_3_*` state tree.

## Runtime Flow

Phase A remains GM-only evidence. Phase B production flow:

1. Full and Compressed Shakedown make the production drill available; Direct Scenario marks the drills bypassed without failure states.
2. Drone 01 spawns passively 15 km from Tarsis Training Beacon. Science scan, Comms hail, shield relay, Weapons lock, 1-2 km range, and a guarded 15-second stationary hold precede authorization.
3. Only `MANUAL_SYSTEM=WEAPONS` damage increments the three-hit disable count. Every automatic gate has a named Comms/GM fallback flag.
4. Unauthorized damage or premature destruction resets Drone 01 5 km farther from the beacon. Cleanup and reset destruction cannot advance success.
5. Confirmed disable plus ceasefire spawns Drone 02 at 10 km. Its genuine destruction sets `drone_contact_act2_ready`; Slice 07, not Slice 06, owns `mission_phase = "act_2"`.
6. The cultural packet is sent once through `khovan_set_current_objective`; GM-only `comms_receive()` remains out of scope.

Phase A flow:

1. GM enables Test Mode.
2. Engineering shakedown completion, or the Engineering Shakedown Complete story jump, sets the Current Objective to `Slice 06 target spike ready. GM Test Mode: run Slice 06 Target Spike.`
3. GM opens `Slice 06 Target Spike`.
4. GM spawns a single neutral training target.
5. The spike links the target as an extra Science scan source and selects it for Science/Comms.
6. Science scan hooks set `drone_target_spike_scan_observed`.
7. Comms hail hook sets `drone_target_spike_hail_observed` and asks the operator to watch for stock enemy menus.
8. Weapons selection hook records `drone_target_spike_weapons_selected` if the target is selected.
9. Damage hook records generic damage, manual subsystem hit evidence, and current Weapons/Engines damage values.
10. Destruction hook records `drone_target_spike_destroyed_observed` and clears the target.
11. Cleanup removes the target and nav proxy.

## GM Controls

- GM-only route: `//comms/gamemaster/khovan_drone_contact_fire_spike`.
- It is visible only when `test_mode_enabled`.
- Controls are Spawn Target Spike, Select Target Spike, Read Target Spike Status, and Cleanup Target Spike.
- Scenario Control overview reports spike status/result.
- No player-facing debug/admin controls are added.

## Player-Facing Behavior

Phase A is a spike harness; Phase B is the player drill:

- After Slice 05 completion, Current Objective labels the Slice 06 target spike as ready instead of ending on an await-next placeholder.
- Current Objective labels the spike as GM target spike active after the spike spawns.
- Science sees scan text for the spike target.
- Comms sees a Khovan hail option and drill-mode response.
- Production player instructions use the proven current-objective broadcast channel. Spike scan/hail output no longer exposes API-test instrumentation language.

## Spike Result

Status: partial live proof (GM-console pass 2026-08-08, plus a genuinely 4-station operator pass same date exercising Weapons/Science/Comms/Helm, cross-checked directly against `tests/live_startup_trace.txt`). Spawn, cleanup, non-attack behavior, Science scan (while alive), Comms hail (no stock-menu interference), and Weapons selection/fire/kill are all live-proven. The destroy-hook guard's damage-value branch is confirmed workable on live trace data. Manual subsystem targeting was initially reported and recorded as confirmed-unavailable; reading the code against the trace showed that was wrong — it was two code bugs (a `data_set.get()` key/default mixup, and a signal-combination bug that discarded a real live `MANUAL_SYSTEM` event), not an API limitation.

**Fixed and partially re-tested live (2026-08-08).** Both code bugs are corrected in `act1_drone_contact_fire.mast`, a trace breadcrumb was added to the previously-silent `Read Target Spike Status` handler, and the destroy-hook guard (cleanup-in-progress flag, consumed before the damage-value fallback) is implemented. `python run_tests.py quick` passes (111 checks, 99 tests) and the MAST compile preflight passes against the installed sbs_utils library.

A follow-up live pass (2026-08-08) confirmed two of the three fixes directly from `tests/live_startup_trace.txt`, not from the verbal report alone:
- **Manual subsystem detection: LIVE-CONFIRMED WORKING.** Trace shows `manual_system=SHPSYS.WEAPONS` firing on a real hit, no longer discarded by the removed AND-gate.
- **Destroy-hook guard's damage-value fallback branch: LIVE-CONFIRMED WORKING.** Trace shows `destruction_source=genuine_weapons_kill` correctly attributed to a real Weapons kill (climbing damage to 2.75/2.75, then destroy).
- **Destroy-hook guard's `cleanup_in_progress` flag branch: STILL UNTESTED.** No GM Cleanup was run this session (operator confirmed: "did not seem necessary"), so the primary signal of the guard — not just its fallback — has not been exercised.
- **`Read Target Spike Status`: STILL UNRESOLVED, and now a clearer question than before.** The operator's first report of "Pass" on this item turned out to be a mix-up with Science scanning the target (a real, separate, already-working action) — not the GM-only "Read Target Spike Status" button. Zero `[KHOVAN ACT1 DRONE SPIKE STATUS]` trace entries exist anywhere in the file for this session, confirming the actual GM action was never triggered. This remains open pending a session where that specific GM button is clicked.

**Third live pass (2026-08-08), both remaining checks run:**
- **`Read Target Spike Status` button was clicked. Handler confirmed executing** (`[KHOVAN ACT1 DRONE SPIKE STATUS]` traced) **but nothing rendered on any screen the operator watched.** This is a real, narrower finding than before — not "never tested," but "executes and produces no visible output." Needs a comparison against other `comms_receive()` calls from the same route family before attempting a fix (see Known Risks).
- **Destroy-hook guard's `cleanup_in_progress` flag branch was tested and FAILED.** Two GM Cleanup runs on freshly spawned targets both reported `destruction_source=unattributed_zero_damage` instead of `gm_cleanup`. Root cause found and fixed: `sbs.delete_object()`'s destroy hook fires deferred/queued relative to the calling handler (confirmed by trace ordering across 4 independent cleanup events), and the prior fix cleared the guard flag before the deferred handler ever read it. **Fixed; not yet re-tested.**

**Fourth live pass (2026-08-08), after a confirmed server restart:**
- **Destroy-hook guard: RE-TESTED AND CONFIRMED FIXED.** Both branches now live-confirmed. Guard work is done.
- **GM `comms_receive()` rendering: FINDING WIDENED FROM SPIKE-SPECIFIC TO CROSS-CUTTING.** The requested diagnostic — does the short one-line Cleanup confirmation render? — came back negative: "No, I see no text when cleanup happens. The drone just disappeared." Every GM-only `comms_receive()` call in this file has now been tested and confirmed to execute without ever rendering, while the identical shape called from a player-facing route is confirmed working. An operator screenshot showed a `(unknown)` sender-identity label where a proven working message shows a real title (e.g. "Tarsis Docking Control") — consistent with GM routes lacking the bound identity every other working call supplies via `comms_override()`. Applied an experimental fix (wrap every GM-only `comms_receive()` in this file with `comms_override(COMMS_ORIGIN_ID, COMMS_ORIGIN_ID, from_name=...)`) and downgraded the cookbook's `[LIVE]` tag on the bare shape. **Not yet live-tested.**

**Closure (2026-08-08), by operator direction:** further screenshots from this same session showed the current-objective broadcast text (`comms_broadcast()`, a different proven-live channel) rendering correctly on a player console. The operator judged continued live-smoke cycling on the GM-only rendering question a poor use of session time against building the mission out, and closed Phase A as accepted with this one item deprioritized rather than blocking. See Next Action.

See Live Smoke Log at the end of this file for the full record, both corrections, and both fixes.

Quick/static checks prove the spike harness exists, imports, initializes, exposes GM-only controls, spawns a neutral training target, includes Science/Comms hooks, and includes selection/damage/destruction observers.

Quick/static checks do not prove live Cosmos target behavior, stock enemy menu suppression, non-attacking behavior, scan visibility, Weapons selection events, manual subsystem damage inventory values, system damage values, or destruction event reliability.

Source decision: Drone 02 completes on destruction. This resolves the active-source ambiguity by user direction after reviewing the conflict between destruction-oriented scenario/MAST/slice-plan text and Engine-disable Dillon/admin references. Drone 01 remains the subsystem-disable proof drill.

## Tests/Static Checks

`tests/test_act1_drone_contact_fire_static.py` checks:

- Slice 06 file exists, imports, and initializes before playable bootstrap.
- Phase A spike variables exist.
- Full Drone 01/Drone 02 flow variables are not falsely marked complete.
- GM-only Test Mode spike controls exist.
- Spike target spawn uses a small neutral training target.
- Science and Comms hooks exist.
- Weapons selection, damage/object, manual subsystem, and destruction observers exist.
- Scenario Control reports spike status.
- Quick includes the Slice 06 static test file.
- This verification doc records Phase A limits.

## Live Smoke Checklist

Repo/branch assumption: run from `slice06-drone-contact-fire` after `python run_tests.py quick` and `git diff --check` pass.

1. Launch Khovan Reach.
2. Open GM Comms.
3. Open Khovan Scenario Control.
4. Enable Test Mode.
5. Open `Slice 06 Target Spike`.
6. Select `Spawn Target Spike`.
7. Confirm a single `Slice 06 Spike Target` appears.
8. Confirm it does not attack Artemis.
9. Confirm Science can scan it and the spike status records scan observed.
10. Confirm Comms can hail it and no unwanted stock enemy taunt/surrender/hostile menus interfere.
11. Confirm Weapons can select/lock it and the spike status records selection observed.
12. Fire or otherwise damage the target and confirm damage is recorded.
13. If manual subsystem targeting is available, target Weapons or Engines and confirm subsystem hit evidence records the subsystem.
14. Destroy the target and confirm destruction is recorded.
15. Run Cleanup Target Spike if needed.
16. Confirm player consoles do not show GM/debug controls.

## Expected Observations

- GM-only spike controls are visible only in Test Mode.
- A neutral training target spawns and is scannable/hailable.
- The target does not attack.
- No stock enemy surrender/taunt/hostile menus break the training fiction.
- Weapons target selection is recorded if Cosmos exposes it.
- Damage/destruction events are recorded if Cosmos exposes them.
- Manual subsystem evidence is recorded if Cosmos exposes `MANUAL_SYSTEM` / `MANUAL_CRITICAL_HIT`.

## Failure/Ambiguous Observations

- Target attacks Artemis.
- Stock enemy menus interfere with the custom Khovan hail.
- Science cannot scan the target.
- Comms cannot hail the target.
- Weapons selection does not trigger.
- Damage/object does not trigger.
- Manual subsystem target data is absent.
- Destruction does not trigger.
- Player consoles see GM controls.
- Static tests pass but live behavior cannot prove the sequence.

## Acceptance Covered

- Static: Phase A spike file/import/init exists.
- Static: GM-only Test Mode controls exist.
- Static: target spawn, scan, hail, selection, damage, subsystem, destruction, and cleanup hooks exist.
- Static: source ambiguity is documented and Drone 02 destruction decision is recorded.
- Static: no full Drone 01/Drone 02 flow is falsely claimed.
- Live (2026-08-08, GM console only): boot chain reaches BOOT 010 live; Artemis start state matches source doc; Kestrel Yards and Tarsis Station spawn and appear as GM contacts; Scenario Control Panel renders correctly; Test Mode toggle correctly gates Story Jumps and Slice 06 Target Spike visibility; Spawn Target Spike works and flips `drone_target_spike_active`; Cleanup Target Spike correctly reverts the menu.
- Live (2026-08-08, 4-station operator pass, trace-verified): target non-attack behavior confirmed; Science scan while alive confirmed; Comms hail confirmed with no stock-menu interference; Weapons target selection confirmed; Weapons fire/kill confirmed with a real, trace-verified damage progression; destroy-hook guard design (GM cleanup vs. real kill, distinguished by damage value) confirmed workable on live data — this pass predates the guard's implementation, it validated the design, not the code.
- Live (2026-08-08, fix-verification follow-up pass, trace-verified): both bugfixes from commit f33d9aa confirmed working live, not just compile-clean — manual subsystem targeting sets correctly (`manual_system=SHPSYS.WEAPONS` observed, no longer discarded), and the destroy-hook guard's damage-value fallback branch correctly attributed a real kill (`destruction_source=genuine_weapons_kill`).
- Live (2026-08-08, second follow-up pass, trace-verified): destroy-hook guard's `cleanup_in_progress` flag branch — found broken, root-caused, fixed, and re-tested in the same pass. Two post-fix cleanups both correctly logged `destruction_source=gm_cleanup`. **The destroy-hook guard is fully live-confirmed on both branches.**

## Acceptance Not Covered

- **GM `comms_receive()` rendering — cross-cutting, not spike-specific. DEPRIORITIZED, not blocking (operator direction, 2026-08-08).** Every GM-only route in this file (Spawn, Select, Read Status, Cleanup) is confirmed to execute correctly and has never rendered visibly for the GM, across 3+ sessions. An experimental fix (`comms_override` wrap) is applied but not yet live-tested. Do not spend another live-smoke session on this unprompted; diagnose from the trace log if picked up again. If confirmed working, `scenario_control_panel.mast` and `story_jump_presets.mast` need the same fix.
- Weapons-console damage readout visibility to a crewed station — likely blocked on the same data_set.get() bug rather than a separate UI gap, but not yet re-confirmed after the fix. Low priority — see design guidance in Next Action (prefer the objective-broadcast channel).
- Test-instrumentation text is confirmed present in player-facing Comms/Science output (deliberately deferred per operator direction, not a Phase A blocker — must land before Drone 01/02 build reuses this spike's text patterns).

## Known Risks/API Uncertainties

- Neutral `npc_spawn` may still have stock behaviors not visible in static checks.
- `get_weapons_selection` may not fire consistently.
- **SUPERSEDED, then FIXED (not yet live re-tested) — see the trace-verified pass below.** An earlier entry in this section claimed manual subsystem targeting was confirmed live-unavailable and raised it as a Drone 01 design decision. Reading `scripts/acts/act1_drone_contact_fire.mast` against `tests/live_startup_trace.txt` from the same pass showed that was wrong: the trace shows `manual_system=SHPSYS.WEAPONS` fired once (19:12:58), proof Cosmos does expose subsystem-lock info to this hook. The failure was two code bugs, not an API absence, and both are now fixed in the file (still needs live re-test before being trusted):
  1. Lines 206-207 (pre-fix) read `spike_target.data_set.get("system_damage", sbs.SHPSYS.WEAPONS)` and `.get("system_damage", sbs.SHPSYS.ENGINES)` — both calls keyed on the same `"system_damage"` string; the `SHPSYS` enums sat in `.get()`'s unused default-value slot instead of being used as subsystem selectors. **Fixed:** both calls now use a sane default (`0`), and a code comment records that there is still no proven per-subsystem `data_set` key — both fields intentionally read the same generic total until one is proven live.
  2. Lines 208-215 (pre-fix) required `MANUAL_CRITICAL_HIT` to match `DAMAGE_TARGET_ID` **and** `MANUAL_SYSTEM` to be non-`None` in the same event before recording a hit. The one time `MANUAL_SYSTEM` fired live, `MANUAL_CRITICAL_HIT` was `None` on that event, so the AND failed and the signal was silently discarded. **Fixed:** the two signals are now tracked independently (`drone_target_spike_manual_subsystem_hit_observed` on `MANUAL_SYSTEM` alone; a new `drone_target_spike_manual_critical_hit_observed` flag on `MANUAL_CRITICAL_HIT` alone).

  **Status: FIXED AND LIVE-CONFIRMED (2026-08-08 follow-up pass).** Trace shows `manual_system=SHPSYS.WEAPONS` firing on a real hit and no longer being discarded. `manual_subsystem_hit_observed` sets correctly.
- `system_damage` values may not reflect manual subsystem hits without extra handling — root-caused above; the fix makes the default-value bug harmless, but per-subsystem differentiation is still unproven and both fields still read one generic value by design until a per-subsystem key is found.
- **Confirmed live 2026-08-08, root-caused, not yet re-verified after fix:** the operator could kill the target via Weapons but did not know where to read damage on it from any station UI. Likely the same root cause as above. Re-evaluate before assuming a separate UI-visibility problem exists.
- Destruction events fire reliably; the GM-cleanup-vs-real-kill distinction is implemented as a two-layer guard in `//damage/destroy`. **Both branches now live-confirmed working (2026-08-08).** Fallback branch (nonzero damage): `destruction_source=genuine_weapons_kill` correctly attributed a real kill. Primary flag branch: found broken by a live test (`unattributed_zero_damage` instead of `gm_cleanup` on two cleanups), root-caused (the destroy hook is deferred/queued relative to the calling handler — confirmed by `CLEANUP` always tracing before the resulting `DAMAGE`/`DESTROY` events across all 4 cleanup events observed, 2 pre-fix and 2 post-fix), fixed (removed a premature flag-clear that was defeating the guard), and re-tested: two cleanups after the fix both correctly logged `destruction_source=gm_cleanup`. **Destroy-hook guard is done.**
- If subsystem detection proves unreliable in further testing, Drone 01 needs the documented Comms/captain-confirmation fallback as its primary path. Not needed based on evidence so far — the live-confirmed fix above works.
- **`Read Target Spike Status` and ALL GM comms_receive() calls in this file — CROSS-CUTTING FINDING (widened 2026-08-08).** Confirmed the handler executes every time (7 handler runs in one session, each correctly reflecting real state transitions), and confirmed — per the diagnostic comparison this section previously called for — that the short one-line Cleanup confirmation ALSO never renders ("The drone just disappeared," no text). This is not specific to the long status report. Every `comms_receive()` call from every GM-only route in this file has now been tested and confirmed to execute without ever rendering visibly. Distinguishing data point: the same bare `comms_receive()` shape called from the player-facing Comms hail route IS live-confirmed working. The failure is specific to GM-only routes (`COMMS_ORIGIN_ID` gated on `has_roles(..., "gamemaster")`), not to `comms_receive()` broadly. A screenshot of the GM console showed a `(unknown)` label rendering where a message sender's identity/title would normally appear — consistent with GM routes lacking the bound sender identity that every other proven-working `comms_receive()` call supplies via `comms_override()`. **Action taken (experimental, not yet live-tested):** wrapped every GM-only `comms_receive()` call in this file in `comms_override(COMMS_ORIGIN_ID, COMMS_ORIGIN_ID, from_name="Khovan Slice 06 Spike")` — the one proven-live shape not yet tried for a GM route. Cookbook section 6.2's `[LIVE]` tag on the bare shape has been downgraded to `[UNPROVEN — DISCONFIRMED FOR GM ROUTES]`. If the experiment works, `scenario_control_panel.mast` and `story_jump_presets.mast` need the identical fix — they use the same disconfirmed bare shape and have never been independently confirmed to render for the GM either. If the experiment also fails, there is no third proven `comms_receive()` shape in the cookbook to try next; escalate as an API-uncertainty finding rather than guessing further.
- **Confirmed, deliberately deferred (operator direction, 2026-08-08):** test-instrumentation text is exposed directly to player-facing consoles — the Comms hail response (line 185) and two Science scan/intel result blocks (lines 167, 172) contain dev-facing phrasing like "Observe whether any stock enemy taunt... appears" and "Check whether this is sufficient for the future Drone 01 Science gate." Not fixed now per explicit operator call ("OK for now, clean up later"). Must be cleaned before this spike's text patterns are reused as a template for Drone 01/Drone 02 player-facing content.
- **Confirmed live 2026-08-08**: `sbs.delete_object()` inside `khovan_drone_contact_fire_cleanup_target_spike` fires the same `//damage/destroy` hook a genuine Weapons kill would. Trace evidence: `[KHOVAN ACT1 DRONE SPIKE CLEANUP] cleanup_count=1` immediately followed by `[KHOVAN ACT1 DRONE SPIKE DAMAGE] ... weapons_damage=0.0 engines_damage=0.0` and `[KHOVAN ACT1 DRONE SPIKE DESTROY]`. GM cleanup and real combat destruction are currently indistinguishable through `drone_target_spike_destroyed_observed`. Since the recorded Drone 02 source decision is "completes on destruction," Phase B must not treat `destroyed_observed` alone as a valid completion signal — it needs a guard (e.g. only trust destruction when accompanied by nonzero `weapons_damage_value`/`engines_damage_value`, or route GM cleanup through a path that does not touch the shared destroy hook).

## Next Action

**Phase A: ACCEPTED (2026-08-08), by operator direction.** Every mechanic Phase A exists to prove is live-confirmed: spawn, cleanup, non-attack behavior, Science scan, Comms hail with no stock-menu interference, Weapons selection/fire/kill, manual subsystem detection, and the destroy-hook guard (both branches). Proceed to Phase B.

**Deprioritized, not blocking (operator direction, 2026-08-08):** GM-only `comms_receive()` rendering remains unresolved — every GM-only route in this file executes correctly but has never rendered visibly for the GM, and the `comms_override` experiment (see Known Risks) is unverified. The operator judged further live-smoke cycles on this one display issue a poor use of session time relative to building the mission out, and is willing to have future diagnosis done by trace-log reading rather than repeated live round-trips. Do not spend another live-smoke session chasing this unprompted.

**Design guidance for Phase B, arising from this investigation:** the current-objective broadcast channel (`comms_broadcast()` via `khovan_set_current_objective`, `current_objective_panel.mast`) is confirmed live-working and already reaching players — objective text renders correctly in blue on a player console without diagnostic prefixes. For anything Drone 01/02 needs to communicate to players — progress, gate status, instructions — **prefer this proven channel over GM-only `comms_receive()`.** The GM's own status visibility can lean on the Scenario Control Panel overview and, until the rendering question is resolved, the trace log.

Test-instrumentation text visible to players (Comms hail response, two Science scan/intel blocks) is a confirmed, deliberately deferred cleanup item — must land before this spike's patterns are reused for Drone 01/02 player-facing content, not before Phase B starts.

Stop after Phase A only if item 1's re-test shows the comms_override experiment also fails to render.

---

## Live Smoke Log (append-only)

### LIVE SMOKE 2026-08-08 (partial — GM-only pass)

```text
branch: slice06-drone-contact-fire
commit: 33cd0c1
build: locally installed Artemis3-x64-release, server + 1 local client (Game Master console)
result: PARTIAL

scope: GM-console-only functional pass, driven by Claude Code via desktop control.
       Science/Comms/Weapons station behavior NOT exercised this pass — no client
       was seated at those consoles. This is not a substitute for a crewed run.

checks:
- boot chain reached [KHOVAN BOOT 010] playable bootstrap complete: PASS
  (trace shows full sequence: bootstrap state -> SCP init -> jump registry ->
  engineering shakedown init -> drone contact fire init -> playable_bootstrap ->
  generator/Tarsis gate init -> debug runtime -> BOOT 009/010)
- Artemis start state matches source doc Act I canon: PASS
  (Energy 0, Homing 0/10, Nuke 0/3, EMP 0/6, Mine 0/6 observed on server HUD)
- Kestrel Yards and Tarsis Station spawn and appear as GM contacts: PASS
- Scenario Control Panel renders live with correct button set: PASS
- Test Mode toggle correctly gates "Test Mode Story Jumps" and
  "Slice 06 Target Spike" visibility (hidden off, shown on): PASS
- Slice 06 Target Spike route renders with correct conditional buttons
  (Spawn only when inactive; Select/Cleanup appear once active): PASS
- Spawn Target Spike: PASS
  (khovan_training contact group appeared, drone_target_spike_active flipped,
  trace: [KHOVAN ACT1 DRONE SPIKE SPAWN] target_id=4611686018427387917 spawn_count=1)
- Read Target Spike Status: AMBIGUOUS
  (label executes without error and comms_navigate returns to the same menu
  cleanly, but no report text was found rendering anywhere in the Game Master
  console UI after repeated attempts, including after maximizing the window
  and toggling the comms-list panel. Not confirmed working; not confirmed broken.)
- Cleanup Target Spike: PASS with a finding
  (menu correctly reverted to spawn-only state; drone_target_spike_active
  cleared)
- Science scan / Comms hail / Weapons selection / manual subsystem damage:
  NOT TESTED this pass (no station client connected)

trace_marker_last: [KHOVAN ACT1 DRONE SPIKE DESTROY] destroyed_id=4611686018427387917

finding: GM Cleanup fires the //damage/destroy hook.
  sbs.delete_object() inside khovan_drone_contact_fire_cleanup_target_spike
  triggers the same //damage/destroy handler a real combat kill would, so
  Cleanup sets drone_target_spike_destroyed_observed = True with
  manual_target=None, manual_system=None, weapons_damage=0.0, engines_damage=0.0.
  GM cleanup and genuine Weapons-caused destruction are currently
  indistinguishable through this hook. If Phase B uses destruction_observed as
  a completion signal (per the recorded Drone 02 source decision), this needs
  a guard before Phase B build, e.g. only trust destruction as a real kill
  when accompanied by nonzero weapons_damage_value, or gate GM cleanup through
  a separate code path that does not touch the shared destroy hook.

blocker: Read Target Spike Status visibility unresolved. Does not block Phase A
  spawn/cleanup mechanics, but blocks confidently reading spike state from the
  GM console for anyone running this live without a trace-file tail open.

next action: Investigate where GM-context comms_receive() actually renders in
  this Cosmos build (may need a Communication-console pass, or the reply may
  need routing through a different mechanism for GM-comms routes specifically).
  Run the remaining Phase A checklist items (Science scan, Comms hail, Weapons
  selection, subsystem damage) with a full crew before calling Phase A complete.
  Resolve the Cleanup/destroy-hook finding before Phase B.
```

### LIVE SMOKE 2026-08-08 (partial — operator pass, weapons exercised)

```text
branch: slice06-drone-contact-fire
commit: (at time of pass; run_tests.py quick was passing)
build: locally installed Artemis3-x64-release
result: PARTIAL

scope: Operator-driven pass. Station crewing arrangement (single client cycling
       stations vs. multiple simultaneous clients) not recorded — confirm before
       trusting this as proof of a genuinely crewed, simultaneous-station session.

checks:
- Spawn Target Spike: PASS (screenshot confirms one "Slice 06 Spike Target"
  contact, khovan_training group, tsn allegiance tag)
- Target does not attack Artemis: PASS
- Science scan: PASS
- Comms hail / stock-menu suppression: NOT TESTED this pass — not reported.
  This is a real gap: the training-safe Comms hail behavior and stock
  enemy-menu suppression are exactly the finding this checklist exists to
  catch, per the Known Risks entry on npc_spawn stock behaviors.
- Weapons target selection/lock: PASS ("I can fire on the target")
- Weapons fire / damage recorded: PASS ("I can kill it") but with a finding —
  operator reported not knowing where/how to read damage on this contact from
  the Weapons console. Damage values may only be confirmable via the trace
  file, not from any in-game station UI, for this contact type.
- Manual subsystem targeting: FAIL / CONFIRMED UNAVAILABLE — operator reports
  no subsystem-targeting option exists against this contact ("not a standard
  target"). This moves the Known Risks entry on MANUAL_SYSTEM /
  MANUAL_CRITICAL_HIT from hypothetical to confirmed-live: subsystem hit
  detection is NOT available through normal Weapons targeting against a
  GM-spawned neutral contact in this Cosmos build.
- Destruction: PASS ("Pass") — but the specific check requested (compare
  trace damage values on this real Weapons kill against a separate GM Cleanup
  destroy event, to confirm they are distinguishable per the destroy-hook
  finding above) was not explicitly reported as done. Not confirmed either
  way.
- Read Target Spike Status: retried AFTER the target was destroyed
  ("Target gone"). This does not resolve the original open question, which
  was whether the status report renders anywhere in the console UI while a
  station is seated and the target is still alive. Still AMBIGUOUS/open.

trace_marker_last: not captured this pass — recommend tailing
  tests/live_startup_trace.txt during the next pass so damage values and
  destroy-hook markers can be read directly rather than inferred from the UI.

finding (NEW, confirmed live): manual subsystem targeting is unavailable
  against the Slice 06 spike target through normal Weapons console targeting.
  Design implication: Drone 01 (per docs/01_design/10_mast_requirements.md
  section 8.5 and the admin plan's ACT1-021/D2 subsystem-hit checks) requires
  subsystem-hit detection. If this Cosmos build genuinely cannot expose
  MANUAL_SYSTEM/MANUAL_CRITICAL_HIT for a custom neutral contact, Drone 01
  needs the documented Comms/captain-confirmation fallback from Known Risks
  as its PRIMARY path, not a fallback of last resort. This is now a design
  decision point for Phase B, not a residual risk.

finding (NEW): Weapons-side damage readout is not visible/known to the
  operator for this contact type. May be the same root cause as the
  Read Target Spike Status GM-rendering gap (custom/GM-spawned contacts not
  getting the same UI treatment as standard hostiles), or may be a separate
  Weapons-console-specific gap. Needs investigation before Phase B assumes
  players can see subsystem/hull damage during Drone 01/02.

blocker: same as prior entry — Read Target Spike Status rendering, still
  unresolved, now compounded by the Weapons damage-readout gap above.
  Destroy-hook guard (see Known Risks) still not built and still not
  confirmed distinguishable in a live A/B comparison.

next action: 1) confirm crewing arrangement for this pass (single client vs.
  simultaneous stations) so the record is accurate; 2) explicitly test Comms
  hail / stock-menu suppression; 3) retry Read Target Spike Status while the
  target is still alive; 4) run the GM-Cleanup-vs-real-kill trace comparison
  directly; 5) route the subsystem-targeting-unavailable finding to the
  operator as a Drone 01 design decision before Phase B.
```

### LIVE SMOKE 2026-08-08 (operator pass, 4-station crew, trace-verified)

```text
branch: slice06-drone-contact-fire
build: locally installed Artemis3-x64-release, 4 simultaneous station
       clients (Weapons, Science, Comms, Helm) operated by one person
result: PARTIAL, with a correction to the prior entry

scope: Genuinely 4 simultaneous station clients, confirmed by the operator
       and cross-checked against tests/live_startup_trace.txt directly
       rather than taken on the verbal report alone. This is a materially
       stronger crewing arrangement than the prior GM-console-only pass,
       though still one operator across 4 clients rather than 4
       independent people.

checks, verified against trace lines (target_id=...919, spawn_count=3,
spawned 2026-08-08T19:08:23):
- Comms hail: PASS (operator-confirmed; custom Khovan hail route fires,
  no stock enemy menu reported).
- Science scan while target alive: PASS — trace shows SCAN and INTEL
  events on ...919 well before its DESTROY event at 19:16:29.
- Weapons select: PASS — [KHOVAN ACT1 DRONE SPIKE WEAPONS SELECT] fires
  twice (19:11:54, 19:16:22).
- Weapons fire / kill: PASS — trace shows a real weapons-caused kill,
  climbing weapons_damage/engines_damage values (0.0 -> 1.0 -> 1.89 ->
  1.88 -> 1.87 -> 2.86 -> 2.85) immediately followed by
  [KHOVAN ACT1 DRONE SPIKE DESTROY] at 19:16:29.640161.
- Destroy-hook guard (requested A/B comparison): CONFIRMED WORKABLE ON
  LIVE DATA. Found directly in the trace rather than needing a separate
  operator-run comparison. Target ...918 (spawn_count=2) went straight
  from SPAWN to CLEANUP to DAMAGE with weapons_damage=0.0
  engines_damage=0.0 to DESTROY - the GM-cleanup signature. Target ...919
  (this kill) shows climbing nonzero values ending at 2.85/2.85 before
  DESTROY. The two are cleanly distinguishable on damage value alone.
  The guard proposed in the prior Known Risks entry (trust destruction
  only when accompanied by nonzero weapons_damage_value/
  engines_damage_value) is validated, not just proposed.

CORRECTION to the prior entry's framing:
  The prior entry treated "manual subsystem targeting unavailable" as a
  confirmed live API limitation requiring an operator design decision for
  Drone 01. Reading scripts/acts/act1_drone_contact_fire.mast against this
  trace shows that framing was wrong. Two specific code bugs, not a
  platform limitation:

  1. Lines 206-207:
       drone_target_spike_weapons_damage_value =
         spike_target.data_set.get("system_damage", sbs.SHPSYS.WEAPONS)
       drone_target_spike_engines_damage_value =
         spike_target.data_set.get("system_damage", sbs.SHPSYS.ENGINES)
     Both calls read the same "system_damage" key. The SHPSYS.WEAPONS /
     SHPSYS.ENGINES enum values sit in .get()'s default-value argument
     position, not used as subsystem selectors. Since "system_damage" is
     always present, the defaults never apply and both fields always
     receive the same generic value. This is confirmed by the trace:
     weapons_damage and engines_damage track near-identically through the
     entire kill sequence on ...919 rather than diverging by subsystem.

  2. Lines 208-215: manual-subsystem-hit detection requires
     get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_CRITICAL_HIT") to equal
     DAMAGE_TARGET_ID AND get_inventory_value(DAMAGE_SOURCE_ID,
     "MANUAL_SYSTEM") to be non-None in the same damage event. The trace
     shows MANUAL_SYSTEM WAS populated once, as SHPSYS.WEAPONS, at
     19:12:58.526309 - direct evidence Cosmos does expose subsystem-lock
     info to this hook. But MANUAL_CRITICAL_HIT (manual_target in the
     trace) was None on that same event, so the AND condition failed and
     drone_target_spike_manual_subsystem_hit_observed was never set True.
     A real signal was received and discarded by the combination logic.

  Neither of these is a Cosmos API absence. Both are fixable in this file.
  The Known Risks entry claiming subsystem targeting is confirmed
  unavailable, and the Next Action item routing this to the operator as a
  Drone 01 design decision, are both walked back below.

Read Target Spike Status: still genuinely unresolved. New information:
  khovan_drone_contact_fire_report_target_spike (line 123-127) is the
  ONLY handler in this file with no script.write_khovan_startup_trace()
  call. Every other handler logs a breadcrumb; this one does not. There
  is no way to confirm from the trace file whether this route rendered,
  regardless of what happened on screen. This is itself a small, concrete
  fix (add a trace line) that should land before the next attempt to
  resolve this, so the next attempt has evidence either way.

test-instrumentation text confirmed exposed to players (operator-flagged,
  code-located, deliberately deferred per operator direction "OK for now,
  clean up later"):
  - line 185, Comms hail response, sent to whatever Comms station
    triggered the hail (not GM-gated): "Automated training target:
    drill-mode response acknowledged. Observe whether any stock enemy
    taunt, surrender, or hostile menu appears alongside this custom
    route."
  - line 167 and 172, Science <scan>/<intel> result text: "Check whether
    this is sufficient for the future Drone 01 Science gate." and
    "Observe whether subsystem targeting and damage events are
    reliable."
  Not fixed this pass per explicit operator direction. Tracked here so it
  is not lost before the pre-production cleanup pass.

trace_marker_last: [KHOVAN ACT1 DRONE SPIKE DESTROY] destroyed_id=4611686018427387919

blocker: Read Target Spike Status rendering, still unresolved, now with a
  concrete first fix (add the missing trace breadcrumb) rather than no
  path forward.

next action: 1) add a trace breadcrumb to
  khovan_drone_contact_fire_report_target_spike so status-read attempts
  are evidenced either way; 2) fix the two damage-value/subsystem-hit
  bugs above (subsystem-keyed data_set lookup, and the MANUAL_SYSTEM /
  MANUAL_CRITICAL_HIT combination logic); 3) retry Read Target Spike
  Status while the target is alive, now with logging in place; 4) build
  the destroy-hook guard using the confirmed-workable nonzero-damage
  check; 5) THEN reconsider whether Drone 01 needs anything beyond the
  fixed automatic detection - the operator-design-decision framing from
  the prior entry is deferred pending these fixes, not needed now.
```

### LIVE SMOKE 2026-08-08 (fix verification pass, single-station)

```text
branch: slice06-drone-contact-fire
commit: f33d9aa (bugfix commit, verified as the running build - see below)
build: locally installed Artemis3-x64-release
result: PARTIAL

scope: Follow-up pass specifically to verify the three fixes from f33d9aa.
       Not a full re-run of the crewed checklist. Verified from
       tests/live_startup_trace.txt directly rather than the verbal
       report alone, per this file's evidence discipline.

checks:
- Build sanity check: PASS. The trace contains a
  destruction_source=genuine_weapons_kill entry, a field that only exists
  in the post-fix code, confirming the running build had the fix loaded
  (not a stale/cached build producing a false negative on item 1 below).
- Manual subsystem targeting: PASS, LIVE-CONFIRMED.
  20:04:03.534702 [KHOVAN ACT1 DRONE SPIKE DAMAGE] ... manual_system=SHPSYS.WEAPONS
  weapons_damage=0.0 engines_damage=0.0. MANUAL_SYSTEM fired and, with the
  AND-gate removed, is no longer discarded. This is direct trace evidence
  the bug 2 fix works, not just operator-reported "Pass".
- Destroy-hook guard, damage-value fallback branch: PASS, LIVE-CONFIRMED.
  20:05:04.947414 [KHOVAN ACT1 DRONE SPIKE DESTROY] destroyed_id=...
  destruction_source=genuine_weapons_kill. Correctly attributed a real
  Weapons kill (climbing damage 0.0 -> 1.0 -> 1.76 -> 2.75) as genuine.
- Destroy-hook guard, cleanup_in_progress flag branch: NOT TESTED.
  Operator confirmed no GM Cleanup was run this session ("did not seem
  necessary"). This is the guard's PRIMARY signal, not its fallback - the
  fallback passing does not prove the flag branch works. Needs its own
  test: spawn, GM Cleanup with zero damage on the target, confirm
  destruction_source=gm_cleanup in the trace.
- Read Target Spike Status: STILL UNRESOLVED, clarified rather than
  resolved. Operator's initial "Pass" on this item was a mix-up with
  Science scanning the target (a real, separate, already-working action)
  - not the GM-only "Read Target Spike Status" button reached via GM
  Comms -> Khovan Scenario Control -> Slice 06 Target Spike -> Read
  Target Spike Status. grep -c "DRONE SPIKE STATUS"
  tests/live_startup_trace.txt returns 0 across the entire file,
  confirming that specific GM action was never triggered this session.
  Given the build sanity check above rules out a stale build, this is a
  genuine "not yet tested" rather than a renewed "tested and broken"
  finding.

trace_marker_last: [KHOVAN ACT1 DRONE SPIKE DESTROY] destroyed_id=4611686018427387917 destruction_source=genuine_weapons_kill

blocker: Read Target Spike Status remains unverified - not because the
  fix failed, but because the specific GM action has still never been
  triggered with the logging in place across three live-smoke sessions.

next action: 1) navigate to the exact GM path (Khovan Scenario Control ->
  Slice 06 Target Spike -> Read Target Spike Status) and click it while
  a target is alive, then check for [KHOVAN ACT1 DRONE SPIKE STATUS] in
  the trace; 2) spawn a fresh target, GM Cleanup it with zero damage
  applied, confirm destruction_source=gm_cleanup in the trace to close
  out the guard's primary-signal branch.
```

### LIVE SMOKE 2026-08-08 (both remaining checks run - one bug found, one still open)

```text
branch: slice06-drone-contact-fire
commit: c19aabc (docs pass, running build predates the cleanup-guard bugfix below)
build: locally installed Artemis3-x64-release
result: PARTIAL - real bug found and fixed

scope: Operator ran both items from the prior "next action": clicked
       Read Target Spike Status, and ran a full spawn -> GM Cleanup
       cycle (twice) instead of a real kill.

checks:
- Read Target Spike Status handler execution: PASS.
  20:12:03.825920 [KHOVAN ACT1 DRONE SPIKE STATUS] status_read requested
  target_id=4611686018427387920 active=True result=manual_subsystem_hit_
  observed_live_unverified_until_operator_confirms
  The handler unambiguously ran this time - the new trace line proves it.
- Read Target Spike Status VISIBLE RENDERING: STILL UNRESOLVED, now a
  narrower and more specific mystery. Operator confirmed the handler
  fired (trace proves it) but reported nothing appeared on any screen
  they were watching. This is no longer "was it ever triggered" - it
  demonstrably was. It is now specifically "why does comms_receive() from
  this GM Test-Mode route not render," which needs comparison against
  other comms_receive() calls from the same route family before guessing
  a fix (see Known Risks).
- Destroy-hook guard, cleanup_in_progress flag branch: FAIL, ROOT-CAUSED,
  FIXED. Operator ran cleanup twice on freshly spawned targets (no damage
  applied first):
    20:13:44.410546 [DRONE SPIKE CLEANUP] cleanup_count=1
    20:13:44.416568 [DRONE SPIKE DESTROY] ... destruction_source=unattributed_zero_damage
    20:13:54.858829 [DRONE SPIKE CLEANUP] cleanup_count=2
    20:13:54.866781 [DRONE SPIKE DESTROY] ... destruction_source=unattributed_zero_damage
  Both should have reported destruction_source=gm_cleanup and did not.
  Root cause: the destroy hook from sbs.delete_object() is deferred/
  queued, not synchronous - confirmed by CLEANUP always tracing BEFORE
  DAMAGE/DESTROY in every one of 4 independent cleanup events across
  this file (2 pre-fix, 2 post-fix). The prior fix cleared
  cleanup_in_progress immediately after the delete_object() call as a
  same-build "fallback," which cleared the flag before the deferred
  destroy handler ever got to read it - guaranteeing the guard's primary
  signal never worked. FIXED: removed the premature clear. The flag now
  stays True until the destroy handler consumes it, or the next spawn's
  reset clears it as a safety net if the hook never fires at all.

trace_marker_last: [KHOVAN ACT1 DRONE SPIKE DESTROY] destroyed_id=4611686018427387921 destruction_source=unattributed_zero_damage

blocker: Read Target Spike Status rendering, unresolved and now more
  precisely scoped (handler runs, output not visible - see Known Risks
  for the comparison needed before attempting another fix).

next action: 1) re-run the same GM Cleanup test with the flag-clearing
  bugfix in place, confirm destruction_source=gm_cleanup this time;
  2) before attempting a Read-Status rendering fix, check whether the
  Scenario Control Panel's own overview report (same comms_receive
  pattern, same GM Test-Mode route family) or the short one-line Spawn/
  Cleanup confirmation messages render visibly - this will show whether
  the problem is systemic to GM comms_receive(), specific to long
  multi-line reports, or specific to this one handler.
```

### LIVE SMOKE 2026-08-08 (destroy-hook guard confirmed working; GM comms_receive() finding widens)

```text
branch: slice06-drone-contact-fire
build: locally installed Artemis3-x64-release, restarted per this file's guidance
result: PARTIAL - one item confirmed fixed, one finding widened from
        spike-specific to cross-cutting

scope: Operator restarted the server (confirmed via a fresh
       [KHOVAN EARLY 001] script.py entered trace line) and re-ran the
       destroy-hook guard test and the Read Target Spike Status test.

checks:
- Destroy-hook guard, cleanup_in_progress flag branch: PASS, CONFIRMED
  FIXED. Two cleanups this session both correctly logged
  destruction_source=gm_cleanup:
    20:24:15.240281 [DRONE SPIKE DESTROY] destroyed_id=4611686018427387917 destruction_source=gm_cleanup
    20:25:25.548308 [DRONE SPIKE DESTROY] destroyed_id=4611686018427387918 destruction_source=gm_cleanup
  The b68513c fix (do not clear cleanup_in_progress before the deferred
  destroy hook fires) works. Both branches of the destroy-hook guard are
  now live-confirmed.
- Read Target Spike Status: handler fired reliably 7 times this session,
  correctly reflecting real state transitions each time (unproven ->
  manual_subsystem_hit_observed_... -> destruction_observed_gm_cleanup_
  not_a_kill). Operator saw nothing on screen every single time. This
  rules out "didn't notice" - the display genuinely does not render.
- Diagnostic requested last entry: does the short one-line Cleanup
  confirmation ("Slice 06 target spike cleaned up.") render? Operator
  confirmed: no, nothing appears - "The drone just disappeared."
  FINDING WIDENS: this is not specific to the long, multi-line status
  report. Every comms_receive() call from every GM-only route in this
  file - Spawn, Select, Read Status, Cleanup - has now been confirmed to
  execute (trace-proven) and never render visibly. The Scenario Control
  Panel uses the identical bare comms_receive() shape and has never been
  independently confirmed to render either.
- Distinguishing data point: the Comms hail response
  (khovan_drone_contact_fire_hail_spike_target), a PLAYER-facing route
  using the exact same bare comms_receive() shape, IS live-confirmed
  working (operator report, prior session: "comms passed"). The failure
  is specific to GM-only (COMMS_ORIGIN_ID gated on
  has_roles(..., "gamemaster")) routes, not to comms_receive() in
  general.
- Visual clue from an operator screenshot of the GM console: a
  "(unknown)" label renders in the position where a message sender's
  title/identity would normally appear (compare the proven Tarsis
  Docking Control dialog, which shows "Tarsis Docking Control" via
  comms_override's from_name parameter). This is consistent with GM
  routes lacking a bound sender identity, which every OTHER proven-live
  comms_receive() call in the codebase supplies via comms_override().

action taken: applied an EXPERIMENTAL fix, not yet live-tested. Wrapped
  every GM-only comms_receive() call in act1_drone_contact_fire.mast
  (Spawn, Select, Read Status, Cleanup) in
  comms_override(COMMS_ORIGIN_ID, COMMS_ORIGIN_ID, from_name="Khovan
  Slice 06 Spike"). This reuses the ONLY proven-live comms_receive()
  shape not yet tried for a GM route - every other confirmed-working
  comms_receive() call in the codebase (Dillon Clip 1, Tarsis docking
  rejection) uses comms_override(); the bare shape has now failed for
  every GM route tested and succeeded for the one player route tested.
  Deliberately left the Comms hail response (player-facing, already
  confirmed working) untouched. Did NOT touch scenario_control_panel.mast
  or story_jump_presets.mast, which use the same disconfirmed bare shape -
  scoped this experiment to Slice 06's own file first; if it works, those
  two files need the same fix as a follow-up, cross-cutting change.
  Downgraded the cookbook's [LIVE] tag on the bare comms_receive() shape
  to [UNPROVEN - DISCONFIRMED FOR GM ROUTES] with the full evidence
  trail, since "cited to a working file" and "confirmed rendering
  observed live" are different evidence classes and this repo's own
  rule is not to conflate them.

trace_marker_last: [KHOVAN ACT1 DRONE SPIKE DESTROY] destroyed_id=4611686018427387918 destruction_source=gm_cleanup

blocker: comms_override experiment not yet live-tested. If it also
  fails to render, this needs an API-uncertainty escalation rather than
  further blind attempts - there is no third proven comms_receive()
  shape left in the cookbook to try.

next action: 1) restart, spawn a target, try Read Target Spike Status
  and Cleanup again with the comms_override experiment in place; 2) if
  either now renders, apply the same fix to scenario_control_panel.mast
  and story_jump_presets.mast as a follow-up change and re-promote the
  cookbook tag to [LIVE]; 3) if neither renders, stop guessing and
  escalate as an API-uncertainty finding - the operator may need to
  consult Cosmos/Artemis reference material outside this repo, or the
  GM console may display messages in a UI surface not yet identified
  from a screenshot.
```
