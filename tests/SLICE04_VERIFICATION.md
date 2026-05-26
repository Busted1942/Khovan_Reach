# Slice 04 Verification - Act I Generator-Governor Start And Tarsis Gate

## What Changed

- Added `scripts/acts/act1_generator_tarsis_gate.mast`.
- Wired Slice 04 initialization after the reference-backed playable bootstrap in `scripts/main.mast`.
- Kept the Slice 01B client lifecycle intact; LegendaryMissions still owns normal console selection, Game Master, and Change Console behavior.
- Added the first real Act I progression state:
  - generator governor starts active.
  - 2-homing reserve is represented as state/log evidence pending ordnance API proof.
  - Kestrel departure clearance is required before launch-envelope confirmation.
  - Kestrel generator advisory is scheduled after launch-envelope confirmation plus 10 seconds.
  - Tarsis homing priority, generator support, and docking clearance are required before governor clear.
  - Tarsis docking/resupply confirmation clears the governor only after required requests are complete.
- Kestrel Yards and Tarsis Station use reference-backed standard station primitives:
  - `npc_spawn(..., "tsn, station, ...", "starbase_command", "behav_station")`.
  - `set_face(..., random_terran(civilian=True))`.
  - `sim.add_navproxy(..., "starbase_command", "#4A7")`.
  - lowercase `station` role for Legendary docking.
  - uppercase `Station` compatibility role for Legendary station Comms routes.
  - `docking_standard_player_station` and `docking_dock_with_friendly_station`.
- Khovan-specific Comms gate options are attached to the station Comms routes.
- Temporary proof station `Comms Test Station` is restored as a live comparison target after cleanup regressed visible Comms routes.
- Kestrel Yards is explicitly marked known to Artemis at startup so departure-control Comms should not require Science scanning.
- Kestrel and Tarsis Khovan menu-owner routes use simple Khovan role conditions, matching the path that previously let station options render after the contact was known.

## Implementation Finding

Live smoke proved that selectable contacts can still show an empty Options panel while they are unknown to Science. During diagnosis, the Options panel stayed blank; station Comms options are hidden until Science initial scan makes the contact known. SBS Utils `CommsPromise.set_buttons()` does not send Comms buttons while `science_is_unknown(origin, selected)` is true.

For Slice 04 live smoke, Kestrel Yards should be available to Comms without a Science scan because it is Artemis' launch yard. Tarsis Station still follows the normal scan-known behavior unless later design work decides otherwise.

Custom Khovan station/profile/Comms binding is deferred. Custom station presentation polish should wait until the core gate is stable. Standard/reference-backed stations are the accepted Slice 04 path until the core gate is proven; this standard station fallback remains intentional.

The restored `Comms Test Station` is diagnostic only. It exists to compare a known-visible proof route against Kestrel/Tarsis while Slice 04 Comms is being stabilized. It is not part of the Khovan scenario design and should be removed once the real Kestrel/Tarsis route is stable.

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
- The temporary proof station is imported, scheduled after Slice 04 setup, and isolated from Kestrel/Tarsis gate state.
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
- Kestrel Comms options appear without Science initial scan.
- `Comms Test Station` appears and proves the no-scan comparison route.
- Science initial scan makes Tarsis known.
- Tarsis Comms options appear after initial scan.
- Khovan-specific Kestrel/Tarsis options appear alongside any standard station options.
- The 10-second advisory timer fires in live runtime.
- The governor does not clear early.
- The governor clears only after required Tarsis confirmations and docking/resupply confirmation.
- Helm docking is available normally, or docking remains documented as API uncertainty with the temporary Comms confirmation path still visible.

## Live Smoke Checklist

1. Run `python .\run_tests.py quick`.
2. Run `git diff --check`.
3. Run `Remove-Item .\tests\live_startup_trace.txt -ErrorAction SilentlyContinue`.
4. Launch Cosmos from branch `slice04-generator-governor-start`.
5. Load Khovan Reach.
6. Confirm normal player console selection still works.
7. Confirm Helm can control Artemis.
8. Use Comms to select Kestrel Yards without an initial Science scan.
9. Confirm Khovan Kestrel options appear.
10. If Kestrel remains unknown/blank, stop and inspect the Kestrel scan-known setup.
11. If Kestrel options are blank, select `Comms Test Station`.
12. Confirm `Proof Option` appears for the proof station.
13. If the proof station works but Kestrel does not, compare Kestrel known/scan state and route condition against the proof station.
14. Select `Khovan: Request Departure Clearance`.
15. Select `Khovan: Confirm Launch-Envelope Exit`.
16. Wait 10 seconds and confirm Kestrel generator advisory appears/logs.
17. Use Science to perform an initial scan on Tarsis Station.
18. Use Comms to select Tarsis Station.
19. Confirm Khovan Tarsis options appear.
20. Select homing priority, generator support, and docking clearance.
21. Attempt normal docking if available.
22. If docking remains unavailable, use `Khovan: Confirm Docking/Resupply` as the temporary Slice 04 fallback.
23. Confirm governor remains active until required requests and resupply confirmation are complete.
24. Confirm governor clears only after the required path.
25. Inspect `tests/live_startup_trace.txt`.

## Expected Observation

- No Missing Shader File crash.
- No SBS Utils / MAST runtime error.
- Playable bootstrap still works.
- Generator governor initializes active.
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
