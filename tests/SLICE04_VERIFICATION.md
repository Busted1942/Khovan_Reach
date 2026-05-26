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
  - Tarsis keeps the lowercase `station` compatibility role for Legendary docking.
  - Kestrel removes the lowercase `station` role before `docking_standard_player_station` so the startup hold does not enter the Legendary docking transition/refit helper.
  - uppercase `Station` compatibility role for Legendary station Comms routes.
  - `docking_standard_player_station` and `docking_dock_with_friendly_station` remain active for Tarsis.
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
- Tarsis records explicit station spawn, object ID, scan-gated visibility, and docking/resupply uncertainty breadcrumbs.

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
- Tarsis station spawn, object ID, scan-gated visibility, and docking setup breadcrumbs are present.
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
- Khovan-specific Kestrel/Tarsis options appear alongside any standard station options.
- The 10-second advisory timer fires in live runtime.
- The governor does not clear early.
- The governor clears only after required Tarsis confirmations and docking/resupply confirmation.
- Helm docking is available normally, or docking remains documented as API uncertainty with the temporary Comms confirmation path still visible.
- Mechanical resupply detection is not claimed until live evidence proves it.

## Live Smoke Checklist

1. Run `python .\run_tests.py quick`.
2. Run `git diff --check`.
3. Run `Remove-Item .\tests\live_startup_trace.txt -ErrorAction SilentlyContinue`.
4. Launch Cosmos from branch `slice04-kestrel-start-docked-debug`.
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
25. Use Science to perform an initial scan on Tarsis Station.
26. Use Comms to select Tarsis Station.
27. Confirm Khovan Tarsis options appear.
28. Select homing priority, generator support, and docking clearance.
29. Attempt normal docking if available.
30. If docking remains unavailable, use `Khovan: Confirm Docking/Resupply` as the temporary Slice 04 fallback.
31. Confirm governor remains active until required requests and resupply confirmation are complete.
32. Confirm governor clears only after the required path.
33. Inspect `tests/live_startup_trace.txt`.

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
- Kestrel departure clearance can be marked through a visible option.
- Kestrel launch-envelope confirmation starts the advisory timer.
- Kestrel advisory appears/logs after the intended delay.
- Tarsis homing priority, generator support, and docking clearance can be marked through visible options.
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
- No visible way exists to trigger required Comms gates.
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
- If docking remains unavailable but the temporary Comms confirmation works, document docking API uncertainty and keep the fallback for Slice 04.
- If governor clears early, stop and fix the Tarsis gate guard before further live smoke.
