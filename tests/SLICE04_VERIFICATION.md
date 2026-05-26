# Slice 04 Verification - Act I Generator-Governor Start And Tarsis Gate

## What Changed

- Added `scripts/acts/act1_generator_tarsis_gate.mast`.
- Wired Slice 04 initialization after the reference-backed playable bootstrap in `scripts/main.mast`.
- Kept the Slice 01B client lifecycle intact; LegendaryMissions still owns normal console selection, Game Master, and Change Console behavior.
- Added the first real Act I progression state:
  - generator governor starts active.
  - 2-homing reserve is represented as state/log evidence pending ordnance API proof.
  - Artemis starts mechanically held at Kestrel Yards by a position and throttle clamp loop.
  - Kestrel yard-lock presentation uses an in-fiction startup overlay and trace breadcrumbs as a fallback visual cue.
  - Kestrel departure clearance is required before launch-envelope confirmation.
  - Kestrel departure clearance releases the startup hold before Helm departure.
  - Kestrel generator advisory is scheduled after launch-envelope confirmation plus 10 seconds.
  - Tarsis homing priority, generator support, and docking clearance are required before governor clear.
  - Tarsis docking/resupply confirmation clears the governor only after required requests are complete.
- Kestrel Yards and Tarsis Station use reference-backed standard station primitives:
  - `npc_spawn(..., "tsn, station, ...", "starbase_command", "behav_station")`.
  - `set_face(..., random_terran(civilian=True))`.
  - `sim.add_navproxy(..., "starbase_command", "#4A7")`.
  - Tarsis keeps the uppercase `Station` compatibility role for station Comms.
  - Tarsis removes the lowercase `station` compatibility role before `docking_standard_player_station`, then restores it after that one-shot docking helper pass so station Comms options can render while the custom pre-clearance docking blocker remains active.
  - Kestrel removes the lowercase `station` role before `docking_standard_player_station` so the startup hold does not enter the Legendary docking transition/refit helper.
  - `khovan_tarsis_docking_rejected_before_clearance` is installed for Tarsis before clearance.
  - `docking_dock_with_friendly_station` is installed for Tarsis only after the Tarsis docking-clearance Comms request succeeds.
- Khovan-specific Comms gate options are attached to the station Comms routes.
- Temporary proof station `Comms Test Station` is restored as a live comparison target after cleanup regressed visible Comms routes.
- Kestrel Yards is explicitly marked known to Artemis at startup so departure-control Comms should not require Science scanning.
- Kestrel and Tarsis Khovan menu-owner routes use simple Khovan role conditions, matching the path that previously let station options render after the contact was known.
- Bug fix: fresh mission load now schedules `khovan_act1_hold_artemis_at_kestrel_until_clearance`, skips the Legendary docking transition helper for Kestrel, resets `playerThrottle` to `0`, and repositions Artemis at the Kestrel start point until departure clearance is granted.
- Added Kestrel hold breadcrumbs:
  - `[KHOVAN ACT1 HOLD 001]` hold scheduled.
  - `[KHOVAN ACT1 DOCK 001K]` Kestrel Legendary docking helper skipped.
  - `[KHOVAN ACT1 HOLD 002]` mechanical hold fallback active at Kestrel.
  - `[KHOVAN ACT1 HOLD 003]` hold released after clearance.
- Added Kestrel yard-lock presentation breadcrumbs:
  - `[KHOVAN ACT1 VISUAL 001]` yard-lock visual setup attempted.
  - `[KHOVAN ACT1 VISUAL 002]` mechanical yard-lock visual fallback active.
- The station_comms_docking_kernel spike is used as implementation evidence only. No kernel proof stations are added to production Slice 04.
- Tarsis records explicit station spawn, object ID, scan-gated visibility, Comms-route availability, Comms option rendering, pre-clearance docking block, premature dock-signal ignore, docking-clearance enable, and docking/resupply uncertainty breadcrumbs.

## Implementation Finding

Live smoke proved that selectable contacts can still show an empty Options panel while they are unknown to Science. During diagnosis, the Options panel stayed blank; station Comms options are hidden until Science initial scan makes the contact known. SBS Utils `CommsPromise.set_buttons()` does not send Comms buttons while `science_is_unknown(origin, selected)` is true.

For Slice 04 live smoke, Kestrel Yards should be available to Comms without a Science scan because it is Artemis' launch yard. Tarsis Station still follows the normal scan-known behavior unless later design work decides otherwise.

Custom Khovan station/profile/Comms binding is deferred. Custom station presentation polish should wait until the core gate is stable. Standard/reference-backed stations are the accepted Slice 04 path until the core gate is proven; this standard station fallback remains intentional.

The restored `Comms Test Station` is diagnostic only. It exists to compare a known-visible proof route against Kestrel/Tarsis while Slice 04 Comms is being stabilized. It is not part of the Khovan scenario design and should be removed once the real Kestrel/Tarsis route is stable.

The station_comms_docking_kernel spike remains evidence only. Slice 04 ports the proven station pattern into Tarsis through stock station spawn, explicit roles, `set_face`, `sim.add_navproxy`, role-owned Comms routes, handler breadcrumbs, docking setup attempts, and fallback confirmation. It does not add `Kernel Known Station`, `Kernel Scan-Gated Station`, or `Kernel Dock Station` to production Slice 04.

Kestrel startup docking crash:

- Crash: fresh load showed Artemis held at Kestrel, then the shared Legendary docking helper crashed in `docking_dock_with_friendly_station` when `get_counter_elapsed_seconds(DOCKING_PLAYER_ID, "interior")` returned `None` and the helper compared it to `interior_delay`.
- Best-known cause: Kestrel was being forced into a startup dock/hold state while also enrolled in the Legendary docking transition/refit helper. The helper starts the `interior` counter in its normal `+++ docked` transition, but the forced startup state can reach the `+++ refit` path without that counter.
- Change: Kestrel now uses a mechanical hold fallback instead of true Legendary docking at mission start. It removes the lowercase `station` role before `docking_standard_player_station`, does not call `docking_set_docking_logic(..., kestrel_yards_id, docking_dock_with_friendly_station)`, keeps `dock_state` clear as `undocked`, and repeatedly clamps position plus throttle until clearance.
- Tarsis remains on the standard docking helper because this crash is specific to the Kestrel startup hold path.
- Live proof still required: only Cosmos can prove the shared docking library no longer crashes on fresh load.

Fresh-load Kestrel departure hold bug:

- Bug: Artemis could move before Comms requested Kestrel departure clearance.
- Change: Slice 04 now applies a mechanical hold loop after Kestrel/Tarsis contact setup and releases it from the Kestrel departure-clearance handler.
- Static proof: quick tests check the hold loop, release helper, Kestrel docking-helper skip, throttle clamp, position reset, scheduling point, and breadcrumbs.
- Live proof still required: only Cosmos can prove Helm is actually unable to move before clearance and able to depart after clearance.

Kestrel startup visual docking / yard-lock presentation:

- Observed polish issue: the mechanical Kestrel hold works, but normal docking lines, docking animation, and docked effects are not visible at fresh load.
- Investigation result: the reference Legendary docking visual path is tied to `docking_dock_with_friendly_station` transition/refit states. That path is not safe for Kestrel startup hold because it caused the `interior` counter crash above when used from a forced startup state.
- Change: Slice 04 keeps the mechanical hold and adds an in-fiction `Kestrel Yard Control` startup story dialog: yard-lock is engaged, hold position on the launch ramp until Comms requests departure clearance.
- Fallback status: this is mechanical yard-lock without proven Cosmos docking animation. True docking visuals remain unclaimed until live smoke proves a safe startup path.

Future polish: Kestrel startup docking animation / yard-lock visual

- Current behavior: the safe mechanical yard-lock works. Artemis starts near Kestrel, Helm movement is held before departure clearance, and the hold releases after clearance, but true docking lines / docking animation are not shown at startup.
- Desired future behavior: Kestrel startup should present a launch-ramp or docking-line visual similar to normal station docking while preserving the yard-lock fiction.
- Non-blocking status: this is future polish and is not required for Slice 04 acceptance.
- Risk: true docking animation may require a normal approach-to-dock transition. Earlier startup use of the Legendary docking transition helper crashed in `docking.mast` when the helper reached `interior_delay` state without complete docking counter setup.
- Acceptance for future work: no runtime crash, visible docking or yard-lock effect appears at startup, departure clearance still gates movement, and Tarsis docking remains unchanged.

Tarsis docking-clearance gate bug:

- Bug: Artemis could dock with Tarsis before Comms requested and received Tarsis docking clearance.
- Best-known cause: Tarsis had the lowercase `station` role during startup `docking_standard_player_station`, and Slice 04 also installed `docking_dock_with_friendly_station` directly for Tarsis during contact setup.
- Change: Tarsis now removes lowercase `station` before the standard docking helper runs, installs `khovan_tarsis_docking_rejected_before_clearance` as the pre-clearance docking logic, and enables `docking_dock_with_friendly_station` only from the successful Tarsis docking-clearance handler after homing priority and generator support are requested.
- Fallback status: this should mechanically deny pre-clearance docking attempts, but live smoke must prove whether Cosmos hides the dock button, shows it and rejects docking, or exposes a different ambiguous state. Slice 04 does not claim hidden/blocked docking UI until live smoke proves it.
- Guardrail: if a docked signal still fires before Tarsis docking clearance, Slice 04 logs it as ignored. Governor clear still requires homing priority, generator support, docking clearance, and the temporary Comms docking/resupply confirmation.

Tarsis pre-clearance docking rejection message bug:

- Bug: pre-clearance Tarsis docking was correctly blocked, but the generic Legendary deny helper could tell players "Our docking systems aren't compatible with yours," which misstates the Slice 04 fiction.
- Change: Tarsis pre-clearance docking now uses a small custom clearance-denied handler. It still rejects docking, but the rejection message says `Tarsis Control: docking clearance not granted. Complete required traffic before approach.`
- Breadcrumb: `[KHOVAN ACT1 DOCK BLOCKED] Tarsis docking rejected: clearance not granted`.
- Static proof: quick tests check the custom handler, the clearance-denied text, the blocked breadcrumb, absence of the old incompatible-systems text from the Tarsis handler, and the unchanged post-clearance `docking_dock_with_friendly_station` enable path.
- Live proof still required: only Cosmos can prove the visible rejection text appears when Helm attempts to dock before Tarsis clearance.
- Future/reuse note: the same custom "no clearance to dock" handler may be useful for Kestrel after departure, because Artemis should not be able to dock back with Kestrel during Slice 04.

Tarsis Comms options render bug:

- Bug: live smoke showed Tarsis Station was visible/selectable and logged `[KHOVAN ACT1 COMMS 007]` plus `[KHOVAN ACT1 COMMS 007A]`, but the Comms options panel stayed empty. The crew could not request homing priority, generator support, or docking clearance.
- Best-known cause: the lowercase `station` compatibility role was removed before `docking_standard_player_station` to prevent premature docking, but it was never restored for the station Comms renderer. The enable hook could fire on `tarsis_station`, while the option buttons still failed to render.
- Change: Slice 04 still removes lowercase `station` before `docking_standard_player_station`, then restores lowercase `station` after that helper pass and before installing the custom pre-clearance docking blocker. This preserves the docking gate while restoring the station-Comms option path.
- Breadcrumbs: `[KHOVAN ACT1 COMMS 004D]` records station-role restoration, `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` records option-block evaluation, and the required option handlers log `[KHOVAN ACT1 COMMS TARSIS HOMING]`, `[KHOVAN ACT1 COMMS TARSIS GENERATOR]`, and `[KHOVAN ACT1 COMMS TARSIS CLEARANCE]`.
- Live proof still required: only Cosmos can prove the option buttons are visibly rendered and clickable after Tarsis is known/selectable.

Latest live result:

- Kestrel Yards shows usable Comms options without a Science scan.
- `Comms Test Station` shows `Proof Option` without a Science scan.
- Tarsis Station requires a Science scan before usable Comms options appear.
- This is the current accepted Comms visibility model for Slice 04 while the Tarsis gate is exercised.

## What Quick/Static Checks Prove

Quick/static checks prove source structure only:

- Slice 04 module exists and is imported from `scripts/main.mast`.
- Slice 04 initialization runs after playable bootstrap wiring.
- Required Act I state variables and default flags are present.
- `generator_governor_active` starts true.
- `starting_homing_torpedoes` and `homing_reserve_count` are set to 2.
- Homing reserve runtime application is explicitly stubbed because ordnance API behavior remains uncertain.
- Kestrel/Tarsis use reference-backed standard station primitives.
- Kestrel/Tarsis Comms routes and gate handlers are present.
- Kestrel departure hold state defaults are present.
- Kestrel departure hold is scheduled after docking setup.
- Kestrel removes lowercase `station` before `docking_standard_player_station`, so the startup hold is not enrolled in `docking_dock_with_friendly_station`.
- Kestrel does not call `docking_set_docking_logic(player_id, kestrel_yards_id, docking_dock_with_friendly_station)`.
- Kestrel yard-lock visual status, fallback mode, startup text, story-dialog call, and `[KHOVAN ACT1 VISUAL 001/002]` breadcrumbs are present.
- The hold loop clamps Artemis to Kestrel by `playerThrottle` and position reset until `kestrel_departure_clearance_granted`.
- The Kestrel departure-clearance handler calls the release helper.
- The release helper leaves throttle at zero and records the release breadcrumb.
- The temporary proof station is imported, scheduled after Slice 04 setup, and isolated from Kestrel/Tarsis gate state.
- Tarsis station spawn, object ID, scan-gated visibility, Comms-route availability, Comms option rendering, docking block, and docking enable breadcrumbs are present.
- Tarsis removes lowercase `station` before `docking_standard_player_station`, so the normal friendly docking helper is not installed through the automatic standard-station pass before clearance.
- Tarsis restores lowercase `station` after `docking_standard_player_station` runs, so station Comms option rendering can use the compatibility role without enrolling Tarsis in the early friendly docking setup.
- Tarsis pre-clearance docking uses `khovan_tarsis_docking_rejected_before_clearance`.
- Tarsis pre-clearance rejection text says docking clearance is not granted, not that docking systems are incompatible.
- Tarsis pre-clearance rejection includes `[KHOVAN ACT1 DOCK BLOCKED]`.
- Tarsis Comms option block contains the required homing priority, generator support, and docking clearance labels.
- Tarsis option handlers set the required flags, send Comms responses, and write the new Tarsis option breadcrumbs.
- Tarsis docked-signal guard logs and ignores a pre-clearance Tarsis dock signal.
- Tarsis installs `docking_dock_with_friendly_station` only from `khovan_tarsis_enable_docking_after_clearance`.
- The docking-clearance handler calls the Tarsis docking-enable helper only after homing priority and generator support are marked.
- No kernel proof stations are present in production Slice 04.
- Tarsis tracks the three required requests.
- Governor clear is guarded behind all three Tarsis requests plus docking/resupply confirmation.
- Slice 04 breadcrumbs are present.
- No custom Khovan selector or direct client-side assignment has returned.
- No player-facing debug/admin controls are exposed by the Slice 04 runtime file.

Quick tests do not prove live runtime behavior.

## What Only Live Cosmos Smoke Can Prove

Only live Cosmos smoke can prove:

- Mission launch remains runtime-clean.
- Player consoles and Helm control still work.
- Artemis starts mechanically held at Kestrel Yards.
- Kestrel yard-lock startup overlay appears.
- Whether true docking lines, docking animation, or docked UI state appear.
- Fresh load does not crash in `docking_dock_with_friendly_station`.
- Helm cannot move Artemis away from Kestrel before Comms requests departure clearance.
- Kestrel departure clearance releases the hold.
- Helm can move/depart after Kestrel departure clearance.
- Kestrel Comms options appear without Science initial scan.
- `Comms Test Station` appears and proves the no-scan comparison route.
- Science initial scan makes Tarsis known.
- Tarsis Comms options appear after initial scan.
- Tarsis Comms-route availability logs after Science known state.
- Required Tarsis options render after Tarsis is selectable/known.
- Clicking homing priority, generator support, and docking clearance produces Tarsis responses in the top-center Comms log and writes the corresponding option breadcrumbs.
- Khovan-specific Kestrel/Tarsis options appear alongside any standard station options.
- Before Tarsis docking clearance, the dock button is unavailable, or docking is rejected by the pre-clearance deny helper, or the behavior is otherwise documented as a live mechanical blocker.
- If docking is rejected before Tarsis clearance, the visible rejection text says docking clearance is not granted and does not say docking systems are incompatible.
- Tarsis normal docking setup is enabled only after homing priority, generator support, and docking clearance are requested through Comms.
- The 10-second advisory timer fires in live runtime.
- The governor does not clear early.
- The governor clears only after required Tarsis confirmations and docking/resupply confirmation.
- If the dock button cannot be hidden or denied, the runtime still must not clear governor/resupply state before the required Comms path and the result remains fallback-only.
- Mechanical resupply detection is not claimed until live evidence proves it.

## Live Smoke Checklist

1. Run `python .\run_tests.py quick`.
2. Run `git diff --check`.
3. Run `Remove-Item .\tests\live_startup_trace.txt -ErrorAction SilentlyContinue`.
4. Launch Cosmos from branch `slice04-tarsis-docking-clearance-gate`.
5. Load Khovan Reach.
6. Confirm normal player console selection still works.
7. Confirm Helm can control Artemis.
8. Confirm Artemis starts near/at Kestrel.
9. Confirm no runtime crash occurs for at least 30 seconds.
10. Confirm the Kestrel Yard Control yard-lock overlay appears.
11. Confirm whether docking lines, docking animation, or docked UI state appear. If they do not, classify the result as fallback-only rather than failure.
12. Before using Kestrel Comms, attempt a gentle Helm move/depart input.
13. Confirm Artemis remains mechanically held at Kestrel and does not depart.
14. Use Comms to select Kestrel Yards without an initial Science scan.
15. Confirm Khovan Kestrel options appear.
16. Select `Khovan: Request Departure Clearance`.
17. After clearance, attempt Helm movement/departure again.
18. Confirm Artemis can move/depart after clearance.
19. Select `Khovan: Confirm Launch-Envelope Exit`.
20. Wait 10 seconds and confirm Kestrel generator advisory appears/logs.
21. If Kestrel remains unknown/blank, stop and inspect the Kestrel scan-known setup.
22. If Kestrel options are blank, select `Comms Test Station`.
23. Confirm `Proof Option` appears for the proof station.
24. If the proof station works but Kestrel does not, compare Kestrel known/scan state and route condition against the proof station.
25. Approach Tarsis.
26. Before Science scan, check whether Tarsis Comms options are unavailable or appropriately limited.
27. Use Science to perform an initial scan on Tarsis Station.
28. Use Comms to select Tarsis Station.
29. Confirm Khovan Tarsis options appear.
30. Before docking clearance, try to dock with Tarsis.
31. Confirm docking is blocked, unavailable, rejected, or does not advance Slice 04 state.
32. Select `Khovan: Request Homing-Torpedo Priority`.
33. Select `Khovan: Request Generator Support`.
34. Select `Khovan: Request Docking Clearance`.
35. Confirm Tarsis docking setup is enabled after clearance.
36. Attempt normal docking if available.
37. If docking remains unavailable, use `Khovan: Confirm Docking/Resupply` as the temporary Slice 04 fallback.
38. Confirm generator governor/resupply clear only after required requests plus docking/fallback confirmation.
39. Confirm trace contains Tarsis scan/known, Comms route, homing priority, generator support, docking clearance, docking setup enabled, and pre-clearance block breadcrumbs.
40. Inspect `tests/live_startup_trace.txt`.

Tarsis docking-clearance regression checklist:

1. Clear `tests/live_startup_trace.txt`.
2. Launch Khovan Reach.
3. Request Kestrel departure clearance.
4. Depart Kestrel.
5. Approach Tarsis.
6. Before Science scan, check whether Tarsis Comms options are unavailable or appropriately limited.
7. Science scan Tarsis.
8. Confirm Tarsis Comms route/options become available.
9. Try to dock before docking clearance.
10. Confirm docking is blocked, unavailable, or does not advance Slice 04 state.
11. Request homing priority.
12. Request generator support.
13. Request docking clearance.
14. Confirm docking setup is enabled after clearance.
15. Dock with Tarsis.
16. Confirm generator governor/resupply clear only after required requests plus docking/fallback confirmation.
17. Confirm trace contains each breadcrumb.

Tarsis pre-clearance docking rejection message checklist:

1. Clear `tests/live_startup_trace.txt`.
2. Launch Khovan Reach.
3. Request Kestrel departure clearance.
4. Depart Kestrel.
5. Approach Tarsis before requesting Tarsis docking clearance.
6. Attempt docking.
7. Confirm docking is blocked.
8. Confirm the message says missing clearance / docking clearance not granted.
9. Confirm it does not say incompatible docking systems.
10. Request homing priority.
11. Request generator support.
12. Request docking clearance.
13. Confirm docking becomes available or proceeds through the existing post-clearance path.
14. Confirm trace logs the blocked pre-clearance attempt and post-clearance setup.

Tarsis Comms option rendering checklist:

1. Clear `tests/live_startup_trace.txt`.
2. Launch Khovan Reach.
3. Request Kestrel departure clearance.
4. Depart Kestrel.
5. Select Tarsis in Comms.
6. Confirm Tarsis options are visible.
7. Click homing priority request.
8. Confirm Tarsis response appears in top-center Comms log and trace.
9. Click generator support request.
10. Confirm Tarsis response appears in top-center Comms log and trace.
11. Try docking before docking clearance and confirm it is still blocked with the clearance-specific message.
12. Click docking clearance request.
13. Confirm Tarsis response appears and docking setup is enabled.
14. Attempt docking again.
15. Confirm no regression in Kestrel behavior.
16. Confirm trace includes all Tarsis option breadcrumbs.

## Expected Observation

- No Missing Shader File crash.
- No SBS Utils / MAST runtime error.
- No `'>=' not supported between instances of 'NoneType' and 'int'` crash from `docking_dock_with_friendly_station`.
- Playable bootstrap still works.
- Generator governor initializes active.
- `tests/live_startup_trace.txt` includes `[KHOVAN ACT1 DOCK 001K]`, `[KHOVAN ACT1 VISUAL 001]`, `[KHOVAN ACT1 VISUAL 002]`, `[KHOVAN ACT1 HOLD 001]`, and `[KHOVAN ACT1 HOLD 002]` on fresh load.
- Kestrel Yard Control overlay says yard-lock is engaged and to hold position until Comms requests departure clearance.
- If docking lines / animation / docked UI state are absent, the result is fallback-only, not true docking visuals.
- Before Kestrel departure clearance, Helm input does not let Artemis leave Kestrel.
- Selecting `Khovan: Request Departure Clearance` produces `[KHOVAN ACT1 HOLD 003]` in the trace.
- After clearance, Artemis is no longer mechanically held at Kestrel and Helm can depart.
- Homing reserve initializes as a clear state/log stub with ordnance API uncertainty documented.
- If live inventory still shows 10/10 homing, treat that as engine/default behavior separate from Khovan's 2-homing reserve state/stub.
- Kestrel is known at startup and shows visible Comms options without Science initial scan.
- `Comms Test Station` appears and shows `Proof Option` as a diagnostic comparison route.
- Before initial scan, Tarsis may be selectable while showing blank/unknown Comms options.
- After Science initial scan, Tarsis shows visible Comms options.
- Trace includes `[KHOVAN ACT1 SCAN 001]` for scan-gated Tarsis setup, `[KHOVAN ACT1 COMMS 004D]` for station-role restoration, `[KHOVAN ACT1 COMMS 007A]` when the Tarsis Comms route is available after the known-state gate, and `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` when the Tarsis option block is evaluated.
- Kestrel departure clearance can be marked through a visible option.
- Kestrel launch-envelope confirmation starts the advisory timer.
- Kestrel advisory appears/logs after the intended delay.
- Tarsis homing priority, generator support, and docking clearance can be marked through visible options.
- Tarsis homing priority produces `[KHOVAN ACT1 COMMS TARSIS HOMING]` and a Tarsis Production Control response.
- Tarsis generator support produces `[KHOVAN ACT1 COMMS TARSIS GENERATOR]` and a Tarsis Generator Acceptance response.
- Tarsis docking clearance produces `[KHOVAN ACT1 COMMS TARSIS CLEARANCE]`, a Tarsis Docking Control response, and `[KHOVAN ACT1 DOCK 004]` after prerequisites are complete.
- Before Tarsis docking clearance, a docking attempt is blocked, unavailable, rejected, or leaves Slice 04 state unchanged; trace includes `[KHOVAN ACT1 DOCK 003]` and `[KHOVAN ACT1 DOCK 003A]`. If a rejected docking attempt reaches the custom handler, trace includes `[KHOVAN ACT1 DOCK BLOCKED]`. If a docked signal fires anyway, trace includes `[KHOVAN ACT1 DOCK 003D]`.
- The pre-clearance Tarsis rejection text says `Tarsis Control: docking clearance not granted. Complete required traffic before approach.`
- The pre-clearance Tarsis rejection text does not say `Our docking systems aren't compatible with yours`.
- After Tarsis docking clearance, trace includes `[KHOVAN ACT1 DOCK 004]` and normal Tarsis docking can be attempted. If the docked signal fires after clearance, trace includes `[KHOVAN ACT1 DOCK 004A]`.
- Governor remains active until homing priority, generator support, and docking clearance are all marked.
- Governor clears only after all three requests and docking/resupply confirmation.

## Failure/Ambiguous Observation

- Kestrel remains unknown or blank before any Science scan.
- Artemis starts free, undocked, or able to move away before Kestrel departure clearance.
- The runtime crashes in `docking_dock_with_friendly_station` with the `NoneType`/`int` comparison.
- The Kestrel Yard Control yard-lock overlay does not appear.
- `[KHOVAN ACT1 DOCK 001K]`, `[KHOVAN ACT1 VISUAL 001]`, `[KHOVAN ACT1 VISUAL 002]`, `[KHOVAN ACT1 HOLD 001]`, or `[KHOVAN ACT1 HOLD 002]` is missing from `tests/live_startup_trace.txt` after fresh load.
- Kestrel departure clearance does not produce `[KHOVAN ACT1 HOLD 003]`.
- Artemis remains stuck after Kestrel departure clearance.
- Tarsis remains unknown after Science initial scan.
- Options panel remains blank after Science initial scan.
- Tarsis is selectable and logs `[KHOVAN ACT1 COMMS 007A]`, but `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` is absent.
- Tarsis is selectable and `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` is present, but the option buttons are still not visible.
- No visible way exists to trigger required Comms gates.
- `[KHOVAN ACT1 COMMS 007A]` is absent after Tarsis is selected through Comms post-scan.
- Tarsis can complete docking before `Khovan: Request Docking Clearance`.
- Tarsis docking before clearance advances Slice 04 state, clears resupply, or clears the governor.
- Pre-clearance Tarsis docking rejection says docking systems are incompatible.
- Pre-clearance Tarsis docking rejection does not clearly say docking clearance is missing/not granted.
- `[KHOVAN ACT1 DOCK BLOCKED]` is absent after a visible rejected Tarsis docking attempt.
- `[KHOVAN ACT1 DOCK 004]` appears before Tarsis docking clearance is requested/granted.
- `[KHOVAN ACT1 DOCK 003D]` appears and the governor still clears or resupply advances before the required Comms path.
- The dock button remains visible before clearance and docking succeeds instead of being denied or state-neutral.
- Kestrel advisory fires immediately without documented reason.
- Tarsis gate cannot be exercised.
- Governor clears early.
- Docking remains unavailable and no temporary Comms confirmation exists.
- Homing inventory is claimed correct while the screen shows an incompatible value such as 10/10 homing.
- `init.mast` warning appears and cannot be classified from current source evidence.
- Quick tests pass but live behavior is unproven.
- This verification doc overclaims automatic launch-envelope, docking, Comms archive, or ordnance behavior.

## What Remains Unproven

- Automatic launch-envelope detection.
- Automatic Tarsis docking/resupply detection.
- Whether Cosmos hides the Tarsis dock button before clearance or leaves it visible while the deny helper rejects docking.
- True Kestrel docking lines, docking animation, or docked UI state at startup.
- Actual generator-output performance reduction.
- Actual torpedo inventory application; torpedo/ordnance crash remains out of scope.
- Custom Kestrel/Tarsis station profile/portrait/menu polish.
- Shakedown profile selection.
- Drone 01/02.
- Full Act I drills.
- Current-objective display unless separately proven.
- Act II/III.
- DAMCON.
- Pirates.
- Qualification/debrief.

## Next Action By Result

- If Kestrel options appear without scan, and Tarsis options appear after Science initial scan, continue Slice 04 live smoke through governor clear.
- If the proof station works but Kestrel does not, preserve the proof station and fix Kestrel known-state or route gating before continuing.
- If options remain blank after Science initial scan, stop and investigate scan-known state or Comms promise ownership.
- If pre-clearance Tarsis docking is denied or state-neutral, continue through the Comms clearance path and document exactly what the dock UI did.
- If pre-clearance Tarsis docking succeeds or advances Slice 04 state, stop and fix the clearance gate before further live smoke.
- If post-clearance docking remains unavailable but the temporary Comms confirmation works, document docking API uncertainty and keep the fallback for Slice 04.
- If governor clears early, stop and fix the Tarsis gate guard before further live smoke.
