# Slice 04 Verification - Act I Generator-Governor Start And Tarsis Gate

## What Changed

- Added `scripts/acts/act1_generator_tarsis_gate.mast`.
- Wired Slice 04 initialization after the reference-backed playable bootstrap in `scripts/main.mast`.
- Kept the Slice 01B client lifecycle intact; LegendaryMissions still owns normal console selection, Game Master, and Change Console behavior.
- Added the first real Act I progression state:
  - generator governor starts active.
  - fresh load requests Homing `0`, Nukes `0`, EMPs `0`, and Mines `0`.
  - literal zero ship energy is not applied because the active source specifies generator governor, not a no-energy start.
  - Kestrel can release two homing torpedoes as emergency reserve through `Khovan: Request Emergency Homing Reserve`.
  - Artemis starts mechanically held at Kestrel Yards by a position and throttle clamp loop.
  - Kestrel yard-lock presentation uses an in-fiction guarded text packet and trace breadcrumbs as a fallback visual cue.
  - Kestrel departure clearance is required before launch-envelope confirmation.
  - Kestrel departure clearance releases the startup hold before Helm departure.
  - Kestrel generator advisory is scheduled after launch-envelope confirmation plus 10 seconds.
  - Act I briefing/instruction packets are guarded as one-time sends at their intended trigger points.
  - Startup and scheduled Act I packets use a guarded text-message path with valid sender/player IDs instead of raw startup `comms_receive` or blank lifeform/story-dialog overlays.
  - Tarsis homing priority, generator support, and docking clearance are required before governor clear.
  - Tarsis docking/resupply confirmation clears the governor only after required requests are complete.
- Kestrel Yards and Tarsis Station use reference-backed standard station primitives:
  - `npc_spawn(..., "tsn, station, ...", "starbase_command", "behav_station")`.
  - `set_face(..., random_terran(civilian=True))`.
  - `sim.add_navproxy(..., "starbase_command", "#4A7")`.
  - Tarsis uses the uppercase `Station` role only during the standard docking-helper pass, then removes it to reduce confusing stock station options.
  - Tarsis removes the lowercase `station` compatibility role before `docking_standard_player_station`, then restores it after that one-shot docking helper pass so Khovan station Comms options can render while the custom pre-clearance docking blocker remains active.
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
- Tarsis records explicit station spawn, object ID, Slice 04 Comms availability, Comms option rendering, pre-clearance docking block, premature dock-signal ignore, docking-clearance enable, and docking/resupply uncertainty breadcrumbs.

## Implementation Finding

Earlier live smoke proved that selectable contacts can show an empty Options panel while they are unknown to Science. Current Slice 04 live evidence now shows Tarsis can be selected and its Khovan option block can render, so Tarsis is not treated as a hard Science-scan gate for this branch.

For Slice 04 live smoke, Kestrel Yards and Tarsis Station should be available to Comms without requiring a Science scan. Science scanning may still provide observational context, but it is not the required unlock for the current Kestrel-to-Tarsis generator handoff.

Custom Khovan station/profile/Comms binding is deferred. Custom station presentation polish should wait until the core gate is stable. Standard/reference-backed stations are the accepted Slice 04 path until the core gate is proven; this standard station fallback remains intentional.

The restored `Comms Test Station` is diagnostic only. It exists to compare a known-visible proof route against Kestrel/Tarsis while Slice 04 Comms is being stabilized. It is not part of the Khovan scenario design and should be removed once the real Kestrel/Tarsis route is stable.

The station_comms_docking_kernel spike remains evidence only. Slice 04 ports the proven station pattern into Tarsis through stock station spawn, explicit roles, `set_face`, `sim.add_navproxy`, role-owned Comms routes, handler breadcrumbs, docking setup attempts, and fallback confirmation. It does not add `Kernel Known Station`, `Kernel Scan-Gated Station`, or `Kernel Dock Station` to production Slice 04.

Starting-condition audit: energy and ordnance:

- User-reported issue: Artemis was expected to start with 0 energy and no weapons.
- Source finding update: active Slice 04 still does not authorize a literal zero-energy start. The current runtime design now treats the two homing torpedoes as a Kestrel-held emergency reserve instead of a fresh-load inventory item.
- Classification: literal zero energy remains out of scope, but zero fresh-load ordnance is now source-aligned for this branch's live behavior target.
- Change: Slice 04 now requests Artemis starting ordnance through data-set values: `Homing_NUM = 0`, `Nuke_NUM = 0`, `EMP_NUM = 0`, and `Mine_NUM = 0`. It intentionally does not call `set_data_set_value(artemis_id, "energy", ...)`.
- Breadcrumbs: `[KHOVAN ACT1 START STATE] Artemis starting energy set to Cosmos default with generator governor active; zero-energy start not source-authorized`, `[KHOVAN ACT1 START STATE] Artemis starting ordnance set to Homing=0 Nuke=0 EMP=0 Mine=0`, and `[KHOVAN ACT1 START STATE FINAL] homing=0 nuke=0 emp=0 mine=0 reserve=held_by_kestrel`.
- Fallback/uncertainty: quick/static checks can prove the runtime requests these values, but only live Cosmos smoke can prove whether the Weapons/Engineering UI immediately reflects them. If the UI still shows a default loadout after the final breadcrumb, treat that as a live mechanics/API issue.

Emergency reserve behavior:

- Purpose: make the two Kestrel-held homing torpedoes meaningful before departure/Tarsis transit as an emergency reserve under the generator governor.
- Source intent preserved: generator governor remains active, Artemis starts with 0 homing torpedoes and no nukes/EMPs/mines, Kestrel can release exactly 2 homing torpedoes through Comms, and Tarsis remains required for homing replacement plus generator acceptance.
- Live failure fixed: fresh load showed `Homing 2/10` because the Slice 04 start-state code explicitly set `Homing_NUM = 2`.
- Change: Kestrel Comms now includes `Khovan: Request Emergency Homing Reserve`.
- Response text: `Kestrel Yard Control: emergency homing reserve released. Artemis now carries two homing torpedoes as generator-governor margin. No nukes, EMPs, or mines are released before Tarsis resupply. Tarsis has been notified to prioritize homing replacement and generator acceptance.`
- Runtime behavior: fresh load requests Homing `0`; the Kestrel reserve request sets `Homing_NUM` to `2` once; repeat selection is suppressed and cannot raise the count above 2.
- Breadcrumbs: `[KHOVAN ACT1 RESERVE 001] emergency homing reserve requested`, `[KHOVAN ACT1 RESERVE 002] emergency homing reserve load requested`, `[KHOVAN ACT1 RESERVE 003] emergency homing reserve applied homing=2`, and `[KHOVAN ACT1 RESERVE 004] emergency homing reserve already loaded; homing remains 2` on repeat.
- Guardrail: this is not torpedo-to-energy conversion and does not clear the generator governor or replace the Tarsis handoff.

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
- Change: Slice 04 keeps the mechanical hold and adds an in-fiction `Kestrel Yard Control` guarded text packet: yard-lock is engaged, hold position on the launch ramp until Comms requests departure clearance.
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
- Change: Tarsis pre-clearance docking now uses a small custom clearance-denied handler. It still rejects docking, but the rejection message says `Tarsis Docking Control: docking clearance not granted. Complete required traffic before approach.`
- Breadcrumb: `[KHOVAN ACT1 DOCK BLOCKED] Tarsis docking rejected: clearance not granted`.
- Static proof: quick tests check the custom handler, the clearance-denied text, the blocked breadcrumb, absence of the old incompatible-systems text from the Tarsis handler, and the unchanged post-clearance `docking_dock_with_friendly_station` enable path.
- Live proof still required: only Cosmos can prove the visible rejection text appears when Helm attempts to dock before Tarsis clearance.
- Future/reuse note: the same custom "no clearance to dock" handler may be useful for Kestrel after departure, because Artemis should not be able to dock back with Kestrel during Slice 04.

Tarsis Comms options render bug:

- Bug: live smoke showed Tarsis Station was visible/selectable and logged `[KHOVAN ACT1 COMMS 007]` plus `[KHOVAN ACT1 COMMS 007A]`, but the Comms options panel stayed empty. The crew could not request homing priority, generator support, or docking clearance.
- Best-known cause: the lowercase `station` compatibility role was removed before `docking_standard_player_station` to prevent premature docking, but it was never restored for the station Comms renderer. The enable hook could fire on `tarsis_station`, while the option buttons still failed to render.
- Change: Slice 04 still removes lowercase `station` before `docking_standard_player_station`, then restores lowercase `station` after that helper pass, removes uppercase `Station` to reduce stock-option confusion, and installs the custom pre-clearance docking blocker. This preserves the docking gate while restoring the Khovan option path.
- Breadcrumbs: `[KHOVAN ACT1 COMMS 004D]` records role restoration/stock-role suppression, `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` records option-block evaluation, and the required option handlers log `[KHOVAN ACT1 COMMS TARSIS HAIL]`, `[KHOVAN ACT1 COMMS TARSIS HOMING]`, `[KHOVAN ACT1 COMMS TARSIS GENERATOR]`, `[KHOVAN ACT1 COMMS TARSIS CLEARANCE]`, `[KHOVAN ACT1 COMMS TARSIS RESUPPLY]`, and `[KHOVAN ACT1 COMMS TARSIS STATUS]`.
- Live proof still required: only Cosmos can prove the option buttons are visibly rendered and clickable after Tarsis is known/selectable.

Act I message-ordering bug:

- Bug: Act I briefing/instruction text could fire before the player action that should trigger it, or repeat in a way that made the live flow read incorrectly.
- Current live regression evidence before this repair: Tarsis route/option-render breadcrumbs repeated and pre-clearance docking rejection worked, but Tarsis option clicks did not produce `[KHOVAN ACT1 COMMS TARSIS HOMING]`, `[KHOVAN ACT1 COMMS TARSIS GENERATOR]`, `[KHOVAN ACT1 COMMS TARSIS CLEARANCE]`, or `[KHOVAN ACT1 MSG TARSIS 002/003/004]`. Dillon's opening briefing also was not established as both a visible message and Comms-log entry at mission start.
- Intended sequence:
  1. Mission start: Dillon Clip 1 stub / opening qualification briefing.
  2. Startup hold: Kestrel yard-lock message, if retained.
  3. Kestrel departure clearance request selected: Kestrel grants departure clearance.
  4. Launch-envelope confirmation selected: Kestrel logs Artemis clear of the launch envelope and starts the 10-second advisory timer.
  5. After launch-envelope plus 10 seconds: Kestrel generator advisory.
  6. Immediately after advisory: Training Control speed-power reminder.
  7. Then shakedown profile prompt, if implemented.
  8. Tarsis homing priority request selected: Tarsis homing-priority acknowledgment.
  9. Tarsis generator support request selected: Tarsis generator-support acknowledgment.
  10. Tarsis docking clearance request selected: Tarsis docking-clearance acknowledgment and docking setup enabled.
  11. Tarsis pre-clearance docking rejection appears only when the player attempts to dock before clearance.
  12. Tarsis resupply/governor clear message appears only after required Tarsis requests plus docking/resupply/fallback condition.
- Change: Slice 04 now sends Dillon's opening briefing after Kestrel/Artemis sender context exists and before the Kestrel yard-lock packet, stages Tarsis options before/after docking clearance, and has one-time send flags for the Dillon stub, Kestrel yard-lock, Kestrel departure response, launch-envelope response, generator advisory, Training Control speed-power reminder, Tarsis request acknowledgments, and Tarsis governor-clear response. Duplicate paths write `[KHOVAN ACT1 MSG ORDER]` breadcrumbs instead of replaying the packet.
- Story sequence text:
  1. Dillon: `Captain. Crew of Artemis. This is a qualification cruise. Standard pattern: depart Kestrel, dock and resupply at Tarsis, conduct the selected shakedown profile, then return for debrief. I'll be observing. Run the cruise. Do your jobs. Captain, the ship is yours.`
  2. Kestrel yard-lock: `Kestrel Yard Control: Artemis is held in yard-lock pending departure clearance. Comms, request clearance when the captain is ready.`
  3. Kestrel departure: `Kestrel Yard Control: departure clearance granted. Helm may clear the launch envelope.`
  4. Kestrel launch-envelope: `Kestrel Yard Control logs Artemis clear of the launch envelope. Advisory packet will follow after yard telemetry catches up.`
  5. Kestrel advisory: `Kestrel Yard Control: advisory packet follows. Your generator assembly is still under observation. We have placed a temporary governor on generator output. You may see sluggish acceleration and reduced sustained-speed response until Tarsis accepts the generator handoff and clears the governor. Tarsis has been notified to prioritize homing-torpedo production and generator acceptance.`
  6. Training reminder: `Training Control: keep speed and power changes deliberate. Treat the generator advisory as active until Tarsis completes the handoff. Comms should coordinate homing priority, generator support, and docking clearance with Tarsis.`
- Guardrail: launch-envelope confirmation cannot restart the advisory timer after the advisory has already been sent, and resend-advisory only works after the advisory has been delivered.
- Static proof: quick tests check the one-time flags, intended handler ties, staged Tarsis labels, duplicate-suppression breadcrumbs, advisory timer guard, resend-advisory guard, Tarsis dock-attempt rejection path, per-option Tarsis message breadcrumbs, Dillon guarded text stand-in, absence of blank story-dialog overlays in the startup path, and Tarsis governor-clear one-time guard.
- Live proof still required: only Cosmos can prove the guarded text/Comms messages appear in the intended player-facing order and do not repeat unexpectedly.

Startup `comms_receive` crash:

- Crash: fresh mission load crashed in `khovan_act1_show_kestrel_yard_lock_visual_fallback` when it called `comms_receive(kestrel_yard_lock_visual_text, title="Kestrel Yard Control", title_color="green")` outside a valid selected-station sender context. The SBS Utils Comms helper tried to read `from_obj.INV.name` and raised `error: 'name'`.
- Best-known cause: startup and scheduled story packets do not always have a valid `COMMS_SELECTED_ID` / sender object with `INV.name`. Raw `comms_receive` is safe for selected station option handlers, but unsafe for the startup yard-lock path and other scheduled non-Comms packet tasks.
- Change: startup/scheduled packets now route through `khovan_reach_send_safe_startup_message`, which disables the risky lifeform/story-dialog overlay path and uses guarded `comms_override(...): comms_receive(...)` only when valid sender/player IDs are available.
- Breadcrumbs: `[KHOVAN ACT1 UI] black-box overlay source disabled or replaced`, `[KHOVAN ACT1 UI] lifeform overlay deferred`, `[KHOVAN ACT1 UI] safe text message path used`, `[KHOVAN ACT1 MSG SAFE] comms_receive skipped: no valid sender/context`, `[KHOVAN DILLON 001]`, `[KHOVAN DILLON 002]`, `[KHOVAN DILLON 003]` or `[KHOVAN DILLON SAFE]`, `[KHOVAN ACT1 MSG DILLON 001] Dillon opening briefing sent`, and `[KHOVAN ACT1 MSG KESTREL 001] Kestrel yard-lock message sent`.
- Scope note: later Kestrel/Tarsis Comms option handlers keep their selected-station `comms_receive` responses because those run from station Comms context. Startup Comms-log echo is claimed only when the guarded sender/player context is valid; otherwise the trace records the safe skip.
- Static proof: quick tests check the safe helper, Dillon helper call after Kestrel/Artemis context exists, Kestrel yard-lock helper call, advisory/training helper calls, absence of raw `comms_receive` from startup/scheduled packet labels, and absence of `sbs.send_story_dialog` from the startup message helper.
- Live proof still required: only Cosmos can prove fresh load no longer crashes, the Dillon/Kestrel text packets are visible/useful, and no black-box overlay remains.

Dillon text stand-in / black-box UI regression:

- Bug: Dillon Clip 1 was not reliably visible/logged, and prior lifeform-style/story-dialog attempts could leave a persistent black rectangle or blank portrait/info panel on viewer/client screens.
- Best-known cause: blank or incomplete `sbs.send_story_dialog(..., "", ...)` overlay calls are unsafe for this branch, while raw startup `comms_receive` can crash before a valid sender object/context exists.
- Change: Dillon Clip 1 is now a text stand-in sent once through the central guarded startup helper after Kestrel/Artemis IDs exist. The helper does not call `sbs.send_story_dialog`; true lifeform overlay/audio playback is deferred.
- Text stand-in: `Captain. Crew of Artemis. This is a qualification cruise. Standard pattern: depart Kestrel, dock and resupply at Tarsis, conduct the selected shakedown profile, then return for debrief. I'll be observing. Run the cruise. Do your jobs. Captain, the ship is yours.`
- Acceptance status: this is text stand-in plumbing only. It does not implement final Dillon audio/video or prove true lifeform presentation.
- Live proof still required: no persistent black box on main viewer/client screens, Dillon text appears or the trace records the safe fallback, and existing Kestrel/Tarsis gates still work.

Latest live result:

- Kestrel Yards shows usable Comms options without a Science scan.
- `Comms Test Station` shows `Proof Option` without a Science scan.
- Tarsis Station is selectable, and `[KHOVAN ACT1 COMMS 007]`, `[KHOVAN ACT1 COMMS 007A]`, and `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` can repeat as the Comms UI refreshes.
- Tarsis pre-clearance docking rejection works and logs `[KHOVAN ACT1 DOCK BLOCKED]`.
- The repaired behavior must prove option-click breadcrumbs and `[KHOVAN ACT1 MSG TARSIS 001-006]` live.

## What Quick/Static Checks Prove

Quick/static checks prove source structure only:

- Slice 04 module exists and is imported from `scripts/main.mast`.
- Slice 04 initialization runs after playable bootstrap wiring.
- Required Act I state variables and default flags are present.
- `generator_governor_active` starts true.
- `starting_homing_torpedoes` and `artemis_start_homing_torpedoes` are set to 0, while `homing_reserve_count` is set to 2.
- Artemis starting ordnance is requested as Homing=0, Nuke=0, EMP=0, Mine=0.
- Artemis starting energy is not set to 0; Slice 04 uses the generator governor as the source-authorized constraint.
- Final start-state breadcrumb `[KHOVAN ACT1 START STATE FINAL] homing=0 ...` exists so live smoke can verify the last Slice 04 ordnance request.
- Kestrel has a `Khovan: Request Emergency Homing Reserve` option.
- The reserve request sets `Homing_NUM` to 2 exactly once, logs `[KHOVAN ACT1 RESERVE 001/002/003]`, suppresses repeats with `[KHOVAN ACT1 RESERVE 004]`, and does not mutate energy or governor state.
- Kestrel/Tarsis use reference-backed standard station primitives.
- Kestrel/Tarsis Comms routes and gate handlers are present.
- Kestrel departure hold state defaults are present.
- Kestrel departure hold is scheduled after docking setup.
- Kestrel removes lowercase `station` before `docking_standard_player_station`, so the startup hold is not enrolled in `docking_dock_with_friendly_station`.
- Kestrel does not call `docking_set_docking_logic(player_id, kestrel_yards_id, docking_dock_with_friendly_station)`.
- Kestrel yard-lock visual status, fallback mode, startup text, guarded safe text call, and `[KHOVAN ACT1 VISUAL 001/002]` breadcrumbs are present.
- The hold loop clamps Artemis to Kestrel by `playerThrottle` and position reset until `kestrel_departure_clearance_granted`.
- The Kestrel departure-clearance handler calls the release helper.
- The release helper leaves throttle at zero and records the release breadcrumb.
- The temporary proof station is imported, scheduled after Slice 04 setup, and isolated from Kestrel/Tarsis gate state.
- Tarsis station spawn, object ID, Slice 04 Comms availability, Comms-route availability, Comms option rendering, docking block, and docking enable breadcrumbs are present.
- Tarsis removes lowercase `station` before `docking_standard_player_station`, so the normal friendly docking helper is not installed through the automatic standard-station pass before clearance.
- Tarsis restores lowercase `station` after `docking_standard_player_station` runs, and removes uppercase `Station` after that helper pass to reduce confusing stock station options.
- Tarsis pre-clearance docking uses `khovan_tarsis_docking_rejected_before_clearance`.
- Tarsis pre-clearance rejection text says docking clearance is not granted, not that docking systems are incompatible.
- Tarsis pre-clearance rejection includes `[KHOVAN ACT1 DOCK BLOCKED]`.
- Tarsis Comms option block contains the required staged labels: Hail, Homing-Torpedo Priority, Generator Support, Docking Clearance, conditional Confirm Docking/Resupply, and Gate Status.
- Tarsis option handlers set the required flags, send Comms responses, and write the new Tarsis option/message breadcrumbs.
- Dillon's opening briefing sends through the safe guarded text helper after Kestrel/Artemis sender context exists and before Kestrel yard-lock messaging.
- The safe startup helper records `[KHOVAN ACT1 UI]` breadcrumbs and `[KHOVAN ACT1 MSG SAFE]` when Comms-log echo is skipped.
- The startup text helper does not call `sbs.send_story_dialog`, so the risky black-box overlay path is not in the Slice 04 startup packet route.
- Act I message-order flags exist for mission start, Kestrel yard-lock, Kestrel departure, launch-envelope, generator advisory, Training Control speed-power reminder, Tarsis request acknowledgments, and Tarsis governor clear.
- Kestrel departure, launch-envelope, generator advisory, Training Control reminder, Tarsis acknowledgments, and governor-clear messages have duplicate-suppression breadcrumbs.
- Launch-envelope confirmation cannot restart the advisory timer after the advisory has already been sent.
- Resend-advisory is guarded so it does not start a new timer.
- Tarsis pre-clearance docking rejection remains tied to the docking rejection handler, not startup.
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
- Kestrel yard-lock guarded text packet appears.
- Whether true docking lines, docking animation, or docked UI state appear.
- Fresh load does not crash in `docking_dock_with_friendly_station`.
- Helm cannot move Artemis away from Kestrel before Comms requests departure clearance.
- Kestrel departure clearance releases the hold.
- Helm can move/depart after Kestrel departure clearance.
- Kestrel Comms options appear without Science initial scan.
- `Comms Test Station` appears and proves the no-scan comparison route.
- Tarsis Comms options appear without requiring a Science scan for this Slice 04 handoff.
- Tarsis Comms-route availability logs when Tarsis is selected.
- Required Tarsis options render after Tarsis is selectable/known.
- Clicking Hail, homing priority, generator support, docking clearance, status, and docking/resupply produces Tarsis responses in the top-center Comms log and writes the corresponding option/message breadcrumbs.
- Act I messages appear only at their intended trigger points and in the intended sequence.
- Duplicate Kestrel/Tarsis option selections do not replay one-time briefing or acknowledgment packets.
- The Training Control speed-power reminder appears immediately after the Kestrel generator advisory.
- Artemis starting energy/ordnance UI matches the intended fresh-load start: generator governor active, Homing 0/10, Nukes 0/3, EMP 0/6, Mines 0/6.
- Kestrel's emergency homing reserve request option appears and releases the reserve through Comms.
- The reserve request changes Homing from 0/10 to 2/10 once, does not increase above 2 on repeat, does not change energy, and does not clear the governor.
- Khovan-specific Kestrel/Tarsis options appear. If any stock Tarsis station options still appear despite uppercase `Station` suppression, document them as unsuppressed stock options and do not use them as proof of Khovan handler wiring.
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
4. Launch Cosmos from branch `slice04-homing-reserve-load-route`.
5. Load Khovan Reach.
6. Confirm normal player console selection still works.
7. Confirm Helm can control Artemis.
8. Confirm Artemis starts near/at Kestrel.
9. Confirm no runtime crash occurs for at least 30 seconds.
10. Confirm `tests/live_startup_trace.txt` logs `[KHOVAN ACT1 START STATE] Artemis starting energy set to Cosmos default with generator governor active; zero-energy start not source-authorized`.
11. Confirm `tests/live_startup_trace.txt` logs `[KHOVAN ACT1 START STATE] Artemis starting ordnance set to Homing=0 Nuke=0 EMP=0 Mine=0`.
12. Confirm `tests/live_startup_trace.txt` logs `[KHOVAN ACT1 START STATE FINAL] homing=0`.
13. Confirm Weapons/Engineering UI state matches the intended fresh-load start: generator governor active, Homing 0/10, Nukes 0/3, EMP 0/6, Mines 0/6.
14. Confirm the Kestrel Yard Control yard-lock overlay appears.
15. Confirm whether docking lines, docking animation, or docked UI state appear. If they do not, classify the result as fallback-only rather than failure.
16. Before using Kestrel Comms, attempt a gentle Helm move/depart input.
17. Confirm Artemis remains mechanically held at Kestrel and does not depart.
18. Use Comms to select Kestrel Yards without an initial Science scan.
19. Confirm Khovan Kestrel options appear.
20. Select `Khovan: Request Emergency Homing Reserve`.
21. Confirm the message explains the two homing torpedoes as generator-governor margin, says no nukes/EMPs/mines are released before Tarsis, and says Tarsis will prioritize homing replacement and generator acceptance.
22. Confirm trace includes `[KHOVAN ACT1 RESERVE 001]`, `[KHOVAN ACT1 RESERVE 002]`, and `[KHOVAN ACT1 RESERVE 003]`.
23. Confirm Homing changes from 0/10 to 2/10.
24. Select `Khovan: Request Emergency Homing Reserve` again.
25. Confirm Homing remains 2/10 and trace includes `[KHOVAN ACT1 RESERVE 004]`.
26. Select `Khovan: Request Departure Clearance`.
27. After clearance, attempt Helm movement/departure again.
28. Confirm Artemis can move/depart after clearance.
29. Select `Khovan: Confirm Launch-Envelope Exit`.
30. Wait 10 seconds and confirm Kestrel generator advisory appears/logs.
31. If Kestrel remains unknown/blank, stop and inspect the Kestrel scan-known setup.
32. If Kestrel options are blank, select `Comms Test Station`.
33. Confirm `Proof Option` appears for the proof station.
34. If the proof station works but Kestrel does not, compare Kestrel known/scan state and route condition against the proof station.
35. Approach Tarsis.
36. Use Comms to select Tarsis Station without treating Science scan as a required unlock.
37. Confirm Khovan Tarsis options appear and are story-guided.
38. Select `Khovan: Hail Tarsis Station`.
39. Confirm `[KHOVAN ACT1 COMMS TARSIS HAIL]` and `[KHOVAN ACT1 MSG TARSIS 001]`.
40. Before docking clearance, try to dock with Tarsis.
41. Confirm docking is blocked, unavailable, rejected, or does not advance Slice 04 state.
42. Select `Khovan: Request Homing-Torpedo Priority`.
43. Confirm `[KHOVAN ACT1 COMMS TARSIS HOMING]` and `[KHOVAN ACT1 MSG TARSIS 002]`.
44. Select `Khovan: Request Generator Support`.
45. Confirm `[KHOVAN ACT1 COMMS TARSIS GENERATOR]` and `[KHOVAN ACT1 MSG TARSIS 003]`.
46. Select `Khovan: Request Docking Clearance`.
47. Confirm `[KHOVAN ACT1 COMMS TARSIS CLEARANCE]`, `[KHOVAN ACT1 MSG TARSIS 004]`, and `[KHOVAN ACT1 DOCK 004]`.
48. Attempt normal docking if available.
49. If docking remains unavailable, use `Khovan: Confirm Docking/Resupply` as the temporary Slice 04 fallback.
50. Confirm `[KHOVAN ACT1 COMMS TARSIS RESUPPLY]` and `[KHOVAN ACT1 MSG TARSIS 005]` only after required requests plus docking/fallback confirmation.
51. Confirm status option logs `[KHOVAN ACT1 COMMS TARSIS STATUS]` and `[KHOVAN ACT1 MSG TARSIS 006]`.
52. Inspect `tests/live_startup_trace.txt`.

Tarsis docking-clearance regression checklist:

1. Clear `tests/live_startup_trace.txt`.
2. Launch Khovan Reach.
3. Request Kestrel departure clearance.
4. Depart Kestrel.
5. Approach Tarsis.
6. Confirm Tarsis Comms route/options become available without requiring Science scan as a hard gate.
7. Try to dock before docking clearance.
8. Confirm docking is blocked, unavailable, or does not advance Slice 04 state.
9. Request homing priority.
10. Request generator support.
11. Request docking clearance.
12. Confirm docking setup is enabled after clearance.
13. Dock with Tarsis.
14. Confirm generator governor/resupply clear only after required requests plus docking/fallback confirmation.
15. Confirm trace contains each breadcrumb.

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
7. Click Hail and confirm `[KHOVAN ACT1 COMMS TARSIS HAIL]` plus `[KHOVAN ACT1 MSG TARSIS 001]`.
8. Click homing priority request and confirm `[KHOVAN ACT1 COMMS TARSIS HOMING]` plus `[KHOVAN ACT1 MSG TARSIS 002]`.
9. Click generator support request and confirm `[KHOVAN ACT1 COMMS TARSIS GENERATOR]` plus `[KHOVAN ACT1 MSG TARSIS 003]`.
10. Try docking before docking clearance and confirm it is still blocked with the clearance-specific message.
11. Click docking clearance request and confirm `[KHOVAN ACT1 COMMS TARSIS CLEARANCE]` plus `[KHOVAN ACT1 MSG TARSIS 004]`.
12. Confirm Tarsis response appears and docking setup is enabled.
13. Attempt docking again.
14. Confirm no regression in Kestrel behavior.
15. Confirm trace includes all Tarsis option breadcrumbs.

Act I message ordering checklist:

1. Clear `tests/live_startup_trace.txt`.
2. Launch Khovan Reach.
3. Confirm no runtime crash for at least 30 seconds.
4. Confirm no persistent black box, blank portrait, empty info panel, or player-facing debug/admin UI appears on main viewer or player clients.
5. Confirm Dillon opening briefing appears through the guarded text path, or logs `[KHOVAN DILLON SAFE]` if startup Comms echo is unavailable.
6. Confirm trace includes `[KHOVAN DILLON 001]`, `[KHOVAN DILLON 002]`, and either `[KHOVAN DILLON 003]` or `[KHOVAN DILLON SAFE]`.
7. Confirm trace includes `[KHOVAN ACT1 UI] black-box overlay source disabled or replaced`, `[KHOVAN ACT1 UI] lifeform overlay deferred`, and `[KHOVAN ACT1 UI] safe text message path used` or the safe unavailable breadcrumb.
8. Confirm Kestrel yard-lock message appears after Dillon.
9. Select Kestrel departure clearance.
10. Confirm departure response appears once.
11. Select launch-envelope confirmation.
12. Wait 10 seconds.
13. Confirm generator advisory appears once.
14. Confirm Training Control speed-power reminder follows.
15. Select Tarsis.
16. Confirm Tarsis options are visible and story-guided.
17. Click Hail; confirm `[KHOVAN ACT1 COMMS TARSIS HAIL]` and `[KHOVAN ACT1 MSG TARSIS 001]`.
18. Click Homing Priority; confirm `[KHOVAN ACT1 COMMS TARSIS HOMING]` and `[KHOVAN ACT1 MSG TARSIS 002]`.
19. Click Generator Support; confirm `[KHOVAN ACT1 COMMS TARSIS GENERATOR]` and `[KHOVAN ACT1 MSG TARSIS 003]`.
20. Try docking before clearance; confirm clearance-denied message and `[KHOVAN ACT1 DOCK BLOCKED]`.
21. Click Docking Clearance; confirm `[KHOVAN ACT1 COMMS TARSIS CLEARANCE]` and `[KHOVAN ACT1 MSG TARSIS 004]`.
22. Dock with Tarsis; confirm docking works.
23. Use Confirm Docking/Resupply if required; confirm `[KHOVAN ACT1 COMMS TARSIS RESUPPLY]` and `[KHOVAN ACT1 MSG TARSIS 005]`.
24. Confirm no unexpected duplicate story messages.

## Expected Observation

- No Missing Shader File crash.
- No SBS Utils / MAST runtime error.
- No `'>=' not supported between instances of 'NoneType' and 'int'` crash from `docking_dock_with_friendly_station`.
- Playable bootstrap still works.
- Generator governor initializes active.
- Dillon opening briefing appears through the guarded text/Comms path before Kestrel yard-lock messaging, or trace logs `[KHOVAN DILLON SAFE]` plus `[KHOVAN ACT1 MSG DILLON 001] Dillon opening briefing sent` as the safe startup fallback.
- Startup/scheduled packets do not crash in `comms_receive`; startup Comms-log echo is claimed only when the guarded sender/player context is valid.
- No persistent black box, blank portrait, empty info panel, or player-facing debug/admin UI remains from Dillon/Kestrel startup messaging.
- `tests/live_startup_trace.txt` includes `[KHOVAN ACT1 DOCK 001K]`, `[KHOVAN ACT1 VISUAL 001]`, `[KHOVAN ACT1 VISUAL 002]`, `[KHOVAN ACT1 HOLD 001]`, and `[KHOVAN ACT1 HOLD 002]` on fresh load.
- Kestrel Yard Control guarded text packet says Artemis is held in yard-lock pending departure clearance.
- If docking lines / animation / docked UI state are absent, the result is fallback-only, not true docking visuals.
- Before Kestrel departure clearance, Helm input does not let Artemis leave Kestrel.
- Selecting `Khovan: Request Departure Clearance` produces `[KHOVAN ACT1 HOLD 003]` in the trace.
- After clearance, Artemis is no longer mechanically held at Kestrel and Helm can depart.
- Fresh load shows Homing 0/10 and logs `[KHOVAN ACT1 START STATE FINAL] homing=0`.
- Kestrel reserve request changes Homing to 2/10 and repeat selection leaves it at 2/10.
- Kestrel is known at startup and shows visible Comms options without Science initial scan.
- `Comms Test Station` appears and shows `Proof Option` as a diagnostic comparison route.
- Tarsis shows visible Khovan Comms options without requiring Science scan as a hard gate.
- Trace includes `[KHOVAN ACT1 SCAN 001]` for Tarsis Slice 04 Comms availability, `[KHOVAN ACT1 COMMS 004D]` for station-role restoration and stock-role suppression, `[KHOVAN ACT1 COMMS 007A]` when the Tarsis Comms route is available, and `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` when the Tarsis option block is evaluated.
- Kestrel departure clearance can be marked through a visible option.
- Kestrel launch-envelope confirmation starts the advisory timer.
- Kestrel advisory appears/logs after the intended delay.
- Training Control speed-power reminder appears after the Kestrel advisory, not before it.
- Repeating Kestrel departure clearance, launch-envelope confirmation, Tarsis request acknowledgments, or Tarsis governor-clear confirmation does not replay one-time packets.
- `Khovan: Resend Generator Advisory` can reference the delivered advisory without restarting the timer.
- Tarsis homing priority, generator support, and docking clearance can be marked through visible options.
- Tarsis Hail produces `[KHOVAN ACT1 COMMS TARSIS HAIL]` and `[KHOVAN ACT1 MSG TARSIS 001]`.
- Tarsis homing priority produces `[KHOVAN ACT1 COMMS TARSIS HOMING]`, `[KHOVAN ACT1 MSG TARSIS 002]`, and a Tarsis Production Control response.
- Tarsis generator support produces `[KHOVAN ACT1 COMMS TARSIS GENERATOR]`, `[KHOVAN ACT1 MSG TARSIS 003]`, and a Tarsis Generator Acceptance response.
- Tarsis docking clearance produces `[KHOVAN ACT1 COMMS TARSIS CLEARANCE]`, `[KHOVAN ACT1 MSG TARSIS 004]`, a Tarsis Docking Control response, and `[KHOVAN ACT1 DOCK 004]` after prerequisites are complete.
- Tarsis docking/resupply confirmation produces `[KHOVAN ACT1 COMMS TARSIS RESUPPLY]` and `[KHOVAN ACT1 MSG TARSIS 005]`.
- Tarsis status produces `[KHOVAN ACT1 COMMS TARSIS STATUS]` and `[KHOVAN ACT1 MSG TARSIS 006]`.
- Before Tarsis docking clearance, a docking attempt is blocked, unavailable, rejected, or leaves Slice 04 state unchanged; trace includes `[KHOVAN ACT1 DOCK 003]` and `[KHOVAN ACT1 DOCK 003A]`. If a rejected docking attempt reaches the custom handler, trace includes `[KHOVAN ACT1 DOCK BLOCKED]`. If a docked signal fires anyway, trace includes `[KHOVAN ACT1 DOCK 003D]`.
- The pre-clearance Tarsis rejection text says `Tarsis Docking Control: docking clearance not granted. Complete required traffic before approach.`
- The pre-clearance Tarsis rejection text does not say `Our docking systems aren't compatible with yours`.
- After Tarsis docking clearance, trace includes `[KHOVAN ACT1 DOCK 004]` and normal Tarsis docking can be attempted. If the docked signal fires after clearance, trace includes `[KHOVAN ACT1 DOCK 004A]`.
- Governor remains active until homing priority, generator support, and docking clearance are all marked.
- Governor clears only after all three requests and docking/resupply confirmation.

## Failure/Ambiguous Observation

- Kestrel remains unknown or blank before any Science scan.
- Dillon opening briefing is absent, has neither guarded visible text output nor `[KHOVAN DILLON SAFE]` fallback breadcrumbs, or appears after Kestrel yard-lock messaging.
- A persistent black box, blank portrait, empty info panel, or player-facing debug/admin UI appears after startup messaging.
- Fresh load crashes in `comms_receive` with `error: 'name'` from a startup or scheduled packet.
- Artemis starts free, undocked, or able to move away before Kestrel departure clearance.
- The runtime crashes in `docking_dock_with_friendly_station` with the `NoneType`/`int` comparison.
- The Kestrel Yard Control yard-lock overlay does not appear.
- `[KHOVAN ACT1 DOCK 001K]`, `[KHOVAN ACT1 VISUAL 001]`, `[KHOVAN ACT1 VISUAL 002]`, `[KHOVAN ACT1 HOLD 001]`, or `[KHOVAN ACT1 HOLD 002]` is missing from `tests/live_startup_trace.txt` after fresh load.
- `[KHOVAN ACT1 START STATE]` energy or ordnance breadcrumbs are missing from `tests/live_startup_trace.txt` after fresh load.
- Artemis starts with literal zero energy, because that would indicate an unauthorized low-energy/no-weapons design change rather than the current generator-governor design.
- Artemis starts with nukes, EMPs, or mines available before Tarsis resupply.
- Artemis starts with Homing 2/10 before the Kestrel reserve request.
- `[KHOVAN ACT1 START STATE FINAL] homing=0` is missing after fresh load.
- `Khovan: Request Emergency Homing Reserve` is missing from Kestrel Comms.
- The reserve request does not explain why the two homing torpedoes exist, why other ordnance is unavailable, or why Tarsis matters.
- Reserve request changes energy or governor state, fails to set Homing to 2/10, or repeat selection increases Homing above 2/10.
- `[KHOVAN ACT1 RESERVE 001]`, `[KHOVAN ACT1 RESERVE 002]`, or `[KHOVAN ACT1 RESERVE 003]` is missing after the first reserve request.
- `[KHOVAN ACT1 RESERVE 004]` is missing after a repeat reserve request.
- Kestrel departure clearance does not produce `[KHOVAN ACT1 HOLD 003]`.
- Artemis remains stuck after Kestrel departure clearance.
- Tarsis remains unavailable to Comms during the Slice 04 handoff.
- Options panel remains blank when Tarsis is selected.
- Tarsis is selectable and logs `[KHOVAN ACT1 COMMS 007A]`, but `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` is absent.
- Tarsis is selectable and `[KHOVAN ACT1 COMMS TARSIS OPTIONS]` is present, but the option buttons are still not visible.
- No visible way exists to trigger required Comms gates.
- `[KHOVAN ACT1 COMMS 007A]` is absent after Tarsis is selected through Comms.
- Clicking Tarsis Hail, homing priority, generator support, docking clearance, status, or resupply does not produce its paired `[KHOVAN ACT1 COMMS TARSIS ...]` and `[KHOVAN ACT1 MSG TARSIS ...]` breadcrumbs.
- Tarsis can complete docking before `Khovan: Request Docking Clearance`.
- Tarsis docking before clearance advances Slice 04 state, clears resupply, or clears the governor.
- Pre-clearance Tarsis docking rejection says docking systems are incompatible.
- Pre-clearance Tarsis docking rejection does not clearly say docking clearance is missing/not granted.
- `[KHOVAN ACT1 DOCK BLOCKED]` is absent after a visible rejected Tarsis docking attempt.
- `[KHOVAN ACT1 DOCK 004]` appears before Tarsis docking clearance is requested/granted.
- `[KHOVAN ACT1 DOCK 003D]` appears and the governor still clears or resupply advances before the required Comms path.
- The dock button remains visible before clearance and docking succeeds instead of being denied or state-neutral.
- Kestrel advisory fires immediately without documented reason.
- Kestrel launch-envelope confirmation restarts the advisory timer after the advisory has already fired.
- Training Control speed-power reminder appears before the Kestrel generator advisory.
- Tarsis homing, generator-support, docking-clearance, or governor-clear acknowledgments repeat unexpectedly after duplicate option selections.
- Tarsis clearance-denied docking message appears at startup or from a non-docking trigger.
- Tarsis gate cannot be exercised.
- Governor clears early.
- Docking remains unavailable and no temporary Comms confirmation exists.
- Homing inventory is claimed correct while the screen shows an incompatible value such as 2/10 at fresh load or 10/10 after the reserve request.
- `init.mast` warning appears and cannot be classified from current source evidence.
- Quick tests pass but live behavior is unproven.
- This verification doc overclaims automatic launch-envelope, docking, Comms archive, or ordnance behavior.

## What Remains Unproven

- Automatic launch-envelope detection.
- Automatic Tarsis docking/resupply detection.
- Whether Cosmos hides the Tarsis dock button before clearance or leaves it visible while the deny helper rejects docking.
- Live guarded text/Comms UI ordering for Act I text packets; static tests only prove source guards and trigger wiring.
- True lifeform-style Dillon overlay without a black box; this remains deferred polish until live smoke proves a safe API/path.
- True Kestrel docking lines, docking animation, or docked UI state at startup.
- Actual generator-output performance reduction.
- Actual torpedo inventory application; torpedo/ordnance crash remains out of scope.
- Mechanical homing-reserve conversion to energy; current behavior only loads the Kestrel-held reserve as two homing torpedoes.
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

- If Kestrel options and Tarsis Khovan options appear without requiring Science scan as a hard gate, continue Slice 04 live smoke through governor clear.
- If the proof station works but Kestrel does not, preserve the proof station and fix Kestrel known-state or route gating before continuing.
- If Tarsis options remain blank, stop and investigate known-state, role ownership, or Comms promise ownership.
- If pre-clearance Tarsis docking is denied or state-neutral, continue through the Comms clearance path and document exactly what the dock UI did.
- If pre-clearance Tarsis docking succeeds or advances Slice 04 state, stop and fix the clearance gate before further live smoke.
- If post-clearance docking remains unavailable but the temporary Comms confirmation works, document docking API uncertainty and keep the fallback for Slice 04.
- If governor clears early, stop and fix the Tarsis gate guard before further live smoke.
