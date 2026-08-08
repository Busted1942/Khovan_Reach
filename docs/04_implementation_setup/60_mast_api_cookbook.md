# KHOVAN REACH — MAST / SBS UTILS API COOKBOOK

Version: 1.0
Status: implementation reference, non-canonical
Authority: **evidence, not design**. This file records syntax that is already in this repo's active runtime code. It does not define Khovan story, pacing, objectives, factions, or player-facing behavior.

Pair with:
- `docs_external/00_tier2_reference_inventory.md` — where to find upstream docs
- `docs/04_implementation_setup/10_mast_file_lessons.md` — which old-build *patterns* to carry forward
- `docs/04_implementation_setup/40_slice01_bootstrap_findings.md` — bootstrap investigation history

---

# 1. Why this file exists

`docs_external/cosmos/`, `docs_external/mast/`, `docs_external/sbs_utils/`, and `reference_missions/` currently contain no committed reference material. Every coding agent that opens this repo re-derives MAST syntax from memory, and MAST is not a language a model can safely guess at.

Meanwhile this repo contains roughly 1,700 lines of MAST that has been through live Cosmos. That is the best local API evidence available, and it was not written down anywhere an agent would find it.

**Rule for agents: prefer a pattern cited in this file over anything you recall about MAST.** If this file does not cover what you need, use the API-uncertainty format in section 11 — do not invent syntax.

Every entry below cites the active file and line where it is used. Verify the citation before relying on it; line numbers drift.

---

# 2. Evidence tiers used in this file

Each pattern is tagged:

- **[LIVE]** — exercised in live Cosmos and recorded in a slice verification doc.
- **[COMPILE]** — compiles under the installed sbs_utils MastStory preflight (`tests/test_mast_compile_or_preflight.py`), but its runtime behavior is not yet proven.
- **[UNPROVEN]** — written against reference/API reading only. Compiles. May not work. Treat as a hypothesis.

Do not upgrade a tag without a live smoke record.

---

# 3. Mission package and entry chain

**[LIVE]** The proven load path is:

```text
story.json -> script.py -> story.mast -> LegendaryMissions.server_console -> scripts/main.mast @map/khovan_reach -> khovan_reach_slice01_entry
```

Root `story.mast` is a 4-line wrapper and nothing else (`story.mast:4`):

```mast
import scripts/main.mast
```

Active runtime code lives under `scripts/`. Imports are repo-root-relative, one per line, at the top of `scripts/main.mast` (`scripts/main.mast:5-14`):

```mast
import scripts/systems/bootstrap_state.mast
import scripts/acts/act1_generator_tarsis_gate.mast
```

## 3.1 script.py responsibilities

**[LIVE]** Three non-obvious things `script.py` must do (`script.py:30-36`, `script.py:80`, `script.py:83-84`):

```python
from sbs_utils.gui import Gui
from sbs_utils.mast.maststorypage import StoryPage
from sbs_utils.mast.mast import Mast
from sbs_utils.mast.mast_globals import MastGlobals

# Makes `script.<fn>()` callable from inside MAST. Without this, every
# script.write_khovan_startup_trace(...) call in MAST fails.
MastGlobals.globals["script"] = sys.modules.get("script")

Mast.include_code = True

Gui.server_start_page_class(KhovanReachStoryPage)
Gui.client_start_page_class(KhovanReachStoryPage)
```

The `MastGlobals.globals["script"]` injection is the mechanism behind the entire breadcrumb-trace system. It is easy to break and produces a silent, ambiguous failure when broken.

## 3.2 Map route

**[LIVE]** `scripts/main.mast:18-27`:

```mast
@map/khovan_reach "Khovan Reach"
" TSN training mission bootstrap shell.
metadata: ```
Properties:
  Main:
    Player Ships: 'gui_int_slider("$text:int;low: 1.0;high:8.0;", var= "PLAYER_COUNT")'
```
    await task_schedule(khovan_reach_slice01_entry)
    ->END
```

---

# 4. State, labels, and control flow

## 4.1 Shared state

**[LIVE]** Declare at file top level, outside any label:

```mast
shared mission_phase = "initialization"
shared artemis_id = 0
```

To assign a shared from inside a label, repeat the `shared` keyword (`scripts/systems/playable_bootstrap.mast:33`):

```mast
    shared artemis_id = artemis_object.id
```

Convention in this repo: each subsystem file owns its own `shared` block at the top; `bootstrap_state.mast` owns only cross-cutting mission state. Do not add Act-specific gates to `bootstrap_state.mast`.

## 4.2 Labels

**[LIVE]** Labels are `=== name ===`, body indented 4 spaces, terminated `->END`:

```mast
=== khovan_scenario_control_panel_initialize ===
    scenario_control_panel_initialized = True
    log("Khovan Slice 02 Scenario Control Panel initialized.")
    ->END
```

## 4.3 Calling labels

**[LIVE]** Awaited call, runs to completion before continuing:

```mast
    await task_schedule(khovan_act1_apply_source_authorized_start_state)
```

**[LIVE]** Awaited call with parameters (`scripts/systems/current_objective_panel.mast:26`):

```mast
    await task_schedule(khovan_set_current_objective, {"objective_id": "tarsis_requests", "objective_body": "Proceed to Tarsis.", "objective_step": "Tarsis requests"})
```

**[LIVE]** Fire-and-forget background task — **no `await`** (`scripts/acts/act1_generator_tarsis_gate.mast:677`). This is how delayed/timer behavior is started:

```mast
    task_schedule(khovan_act1_deliver_kestrel_generator_advisory_after_delay, {"advisory_run_id": kestrel_generator_advisory_run_id})
```

## 4.4 Receiving parameters

**[LIVE]** `default` lines at the top of the label declare parameters and their fallbacks (`scripts/systems/current_objective_panel.mast:30-36`):

```mast
=== khovan_set_current_objective ===
    default objective_id = "unknown"
    default objective_color = "cyan"
    default objective_breadcrumb = ""
```

A `default` may reference a shared (`act1_generator_tarsis_gate.mast:685`):

```mast
    default advisory_run_id = kestrel_generator_advisory_run_id
```

## 4.5 Yield and jump

**[LIVE]**

```mast
    yield success
    yield fail
    yield fail if DOCKING_NPC_ID == 0
```

```mast
    jump khovan_engineering_watch_no_motion_validation_tick
```

```mast
    await delay_sim(seconds=10)
```

---

# 5. The two patterns that matter most

These two carry nearly every timed or observed behavior in the mission. Slices 09 (DAMCON), 11 (pirate timers), and 12 (combat) will lean on both heavily.

## 5.1 Run-ID guard for delayed work

**[LIVE]** `scripts/acts/act1_generator_tarsis_gate.mast:673-694`.

Any delayed task that can survive a story jump must carry a generation ID and re-check it after the delay. Increment the shared counter **before** scheduling, pass it in, compare after waking:

```mast
    kestrel_generator_advisory_run_id = kestrel_generator_advisory_run_id + 1
    task_schedule(khovan_act1_deliver_kestrel_generator_advisory_after_delay, {"advisory_run_id": kestrel_generator_advisory_run_id})

=== khovan_act1_deliver_kestrel_generator_advisory_after_delay ===
    default advisory_run_id = kestrel_generator_advisory_run_id
    await delay_sim(seconds=10)
    if advisory_run_id != kestrel_generator_advisory_run_id:
        script.write_khovan_startup_trace("[KHOVAN ACT1 MSG ORDER] duplicate suppressed stale Kestrel advisory timer")
        ->END
    if not launch_envelope_cleared:
        ->END
    if kestrel_generator_packet_sent or kestrel_generator_advisory_sent:
        ->END
```

Note there are three guards, not one: stale generation, precondition still true, and not-already-sent. All three are needed.

A story-jump seed invalidates pending timers by bumping the same counter (`act1_generator_tarsis_gate.mast:237`, `:281`).

## 5.2 Bounded polling observer with fallback

**[LIVE]** `scripts/acts/act1_engineering_shakedown.mast:199-250`.

For Act I, the canonical table of preferred detection and fallback methods for every gate is in `docs/01_design/10_mast_requirements.md` section 8.9 "Act I automation gate map". This section documents the MAST pattern; section 8.9 documents which gate uses which pattern.

MAST has no "watch this value" primitive here. Automatic gates are built as a self-jumping tick label with a tick ceiling and a documented fallback:

```mast
=== khovan_engineering_start_no_motion_watch ===
    artemis_object = to_object(artemis_id)
    if artemis_object is None:
        engineering_no_motion_fallback_available = True
        ->END
    engineering_no_motion_start_x = artemis_object.pos.x
    engineering_no_motion_start_z = artemis_object.pos.z
    engineering_no_motion_observer_ticks = 0
    await delay_sim(seconds=1)
    jump khovan_engineering_watch_no_motion_validation_tick
    ->END

=== khovan_engineering_watch_no_motion_validation_tick ===
    if engineering_no_motion_confirmed:
        ->END
    if not engineering_no_motion_validation_requested:
        ->END
    engineering_no_motion_observer_ticks = engineering_no_motion_observer_ticks + 1

    # ... read state, evaluate gate ...
    if throttle >= 0.95 and speed <= 1 and flat_distance_sq <= 25:
        await task_schedule(khovan_engineering_complete_no_motion_validation, {"completion_source": "automatic_throttle_speed_position_observer"})
        ->END

    if engineering_no_motion_observer_ticks >= 20:
        engineering_no_motion_fallback_available = True
        comms_receive("Training Control: no-motion observer cannot verify the Engineering slider state...", title="Training Control", title_color="yellow")
        ->END

    await delay_sim(seconds=1)
    jump khovan_engineering_watch_no_motion_validation_tick
    ->END
```

**Every automatic gate in this mission must ship with its fallback.** The source design principle is: automatic gate first, Comms/captain confirmation second, GM manual mark last. A gate with no fallback is a mission-stopping bug, because the operator cannot recover mid-session.

---

# 6. Comms

## 6.1 Route guards

**[LIVE]** Two different subjects, easy to confuse:

- `COMMS_ORIGIN_ID` — the console/player *sending*. Use for GM-only gating.
- `COMMS_SELECTED_ID` — the object *targeted*. Use for "when talking to Tarsis".

GM-only top-level entry and submenu (`scripts/systems/scenario_control_panel.mast:16-27`):

```mast
//comms if has_roles(COMMS_ORIGIN_ID, "gamemaster")
    + "Khovan Scenario Control" //comms/gamemaster/khovan_scenario_control_panel

//comms/gamemaster/khovan_scenario_control_panel if has_roles(COMMS_ORIGIN_ID, "gamemaster")
    + "Back" //comms
    + "Hold Scene Transition" khovan_scenario_control_panel_hold_transition
    + "Enable Test Mode" khovan_scenario_control_panel_enable_test_mode if not test_mode_enabled
    + "Test Mode Story Jumps" //comms/gamemaster/khovan_story_jump_presets if test_mode_enabled
```

Button forms:
- `+ "Label" //comms/some/route` — navigate to submenu
- `+ "Label" some_label_name` — run a label
- `+ "Label" target if <condition>` — conditional visibility

Target-selected route, with its `//enable/comms` companion (`scripts/acts/act1_generator_tarsis_gate.mast:98-104`):

```mast
//enable/comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")
    script.write_khovan_startup_trace("[KHOVAN ACT1 COMMS 007] Tarsis standard station selected")

//comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")
    tarsis_comms_options_status = "rendered_after_known_state"
```

## 6.2 Sending

**[LIVE]** Plain message to the acting console:

```mast
    comms_receive(text, title="Khovan Scenario Control", title_color="cyan")
```

**[LIVE]** Return the GM to the menu after an action, or the menu closes (`scenario_control_panel.mast:53`):

```mast
    comms_navigate("//comms/gamemaster/khovan_scenario_control_panel")
```

**[LIVE]** Message appearing to come from an NPC — requires both a valid sender id and player id (`scripts/systems/audio_runtime.mast:19-21`):

```mast
    if startup_sender_id != 0 and startup_player_id != 0:
        with comms_override(startup_sender_id, startup_player_id, from_name=startup_sender):
            comms_receive(startup_text, title=startup_sender, title_color=startup_title_color)
```

**[LIVE]** Text-waterfall broadcast — this is how the Current Objective is delivered (`scripts/systems/current_objective_panel.mast:58`):

```mast
    comms_broadcast(artemis_id, current_objective_last_message, objective_color)
```

**[LIVE]** Styled dialog block inside a docking hook (`act1_generator_tarsis_gate.mast:467-469`):

```mast
    with comms_override(DOCKING_NPC_ID, DOCKING_PLAYER_ID, from_name="Tarsis Docking Control"):
        <<[yellow,black] "Docking Clearance Required"
            % {tarsis_docking_rejection_text}
```

## 6.3 Message routing rule

Do not scatter raw `comms_receive` for player-facing instruction. Route it through the wrapper in `scripts/systems/audio_runtime.mast` (`khovan_reach_send_safe_startup_message`), which handles the missing-sender fallback and emits breadcrumbs. Objective text goes through `khovan_set_current_objective`.

---

# 7. Science, Weapons, damage

## 7.1 Science scan route

**[LIVE]** `scripts/acts/act1_drone_contact_fire.mast:151-172`:

```mast
//enable/science if has_roles(SCIENCE_SELECTED_ID, "khovan_slice06_spike_target")

//science if has_roles(SCIENCE_SELECTED_ID, "khovan_slice06_spike_target")
    + "Initial Scan":
        drone_target_spike_scan_observed = True
        <scan>
            % Slice 06 target spike scan observed.
    + "scan":
        <scan>
            % ...
```

Note `+ "Label":` with a trailing colon opens an inline block; without a colon it takes a label name.

## 7.2 Weapons selection

**[UNPROVEN]** `act1_drone_contact_fire.mast:188-196`. Written, compiles, awaiting Slice 06 live smoke:

```mast
//select/weapons if has_role(WEAPONS_ORIGIN_ID, "__player__")
    selected_weapons_target_id = get_weapons_selection(WEAPONS_ORIGIN_ID)
    if selected_weapons_target_id == drone_target_spike_target_id:
        drone_target_spike_weapons_selected = True
    ->END
```

## 7.3 Damage and subsystem hits

**[UNPROVEN]** `act1_drone_contact_fire.mast:198-217`. This is the highest-risk API in the mission — Slice 06's whole spike exists to test it. Do not build Drone 01 on it until live smoke confirms.

```mast
//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_slice06_spike_target")
    system = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_SYSTEM")
    target_id = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_CRITICAL_HIT")
    spike_target = to_object(DAMAGE_TARGET_ID)
    if spike_target is not None:
        drone_target_spike_weapons_damage_value = spike_target.data_set.get("system_damage", sbs.SHPSYS.WEAPONS)
    if target_id != 0:
        # Consume the manual-hit inventory values so they do not leak into the next hit.
        set_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_SYSTEM", None)
        set_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_CRITICAL_HIT", None)
        if target_id == DAMAGE_TARGET_ID and system is not None:
            drone_target_spike_manual_subsystem = system.name
    ->END
```

**[UNPROVEN]** Destruction (`act1_drone_contact_fire.mast:219-237`). Note the roles are removed and selections cleared, because object cleanup timing is not guaranteed:

```mast
//damage/destroy if has_role(DESTROYED_ID, "khovan_slice06_spike_target")
    drone_target_spike_destroyed_observed = True
    remove_role(DESTROYED_ID, "khovan_slice06_spike_target")
    ->END
```

Known open questions on this group are listed in `tests/SLICE06_VERIFICATION.md` under Known Risks/API Uncertainties. Read that before touching damage detection.

---

# 8. Spawning, roles, selection

## 8.1 Idempotent spawn

**[LIVE]** Always check for an existing object first, or story jumps stack duplicates (`act1_generator_tarsis_gate.mast:363-374`):

```mast
    existing_kestrel_yards = to_object_list(role("kestrel_yards"))
    if len(existing_kestrel_yards) == 0:
        kestrel_yards = npc_spawn(0, 0, 0, "Kestrel Yards", "tsn, station, kestrel_yards, khovan_origin", "starbase_command", "behav_station")
        kestrel_yards_id = to_id(kestrel_yards)
        sim.add_navproxy(kestrel_yards_id, "Kestrel Yards", "starbase_command", "#4A7")
```

`npc_spawn(x, y, z, name, roles_csv, hull_key, behavior_key)`. Roles are one comma-separated string.

Known-good keys in use: `"starbase_command"` / `"behav_station"` for stations, `"tsn_warpster"` / `"behav_npcship"` for a small ship.

## 8.2 The capitalized-Station role workaround

**[LIVE]** `act1_generator_tarsis_gate.mast:371-374`. Non-obvious and deliberate — stock station behavior keys off capital `Station`:

```mast
    add_role(kestrel_yards_id, "Station")
    remove_role(kestrel_yards_id, "station")
    add_role(kestrel_yards_id, "kestrel_yards")
```

Do not "clean this up."

## 8.3 Object conversion helpers

**[LIVE]**

```mast
    to_id(obj)
    to_object(id)                                  # returns None if gone - always check
    to_object_list(role("__player__") & role("tsn"))
    to_engine_object(id)                           # .cur_speed
    obj.get_roles()
    obj.update_comms_id()                          # after renaming a ship
```

## 8.4 Selection and scan linking

**[LIVE]** for selection, **[UNPROVEN]** for `extra_scan_source` (`act1_drone_contact_fire.mast:93-96`):

```mast
    link(artemis_id, "extra_scan_source", drone_target_spike_target_id)
    set_science_selection(artemis_id, target_id)
    set_comms_selection(artemis_id, target_id)
    set_weapons_selection(artemis_id, target_id)   # 0 clears
```

## 8.5 Cleanup

**[LIVE]** `act1_drone_contact_fire.mast:129-149`. Navproxy first, then selections, then object:

```mast
    sim.delete_navproxy_by_id(navproxy_id)
    set_science_selection(artemis_id, 0)
    set_comms_selection(artemis_id, 0)
    set_weapons_selection(artemis_id, 0)
    sbs.delete_object(target_id)
```

**[LIVE] Gotcha, confirmed 2026-08-08 Slice 06 GM smoke pass:** `sbs.delete_object()` fires the same `//damage/destroy` hook a genuine Weapons kill fires. Trace evidence from a GM `Cleanup Target Spike` click: `[KHOVAN ACT1 DRONE SPIKE CLEANUP] cleanup_count=1` was immediately followed by `[KHOVAN ACT1 DRONE SPIKE DAMAGE] ... weapons_damage=0.0 engines_damage=0.0` and `[KHOVAN ACT1 DRONE SPIKE DESTROY]` — despite no shot ever being fired.

**Implication:** any `*_destroyed_observed`-style flag set inside a `//damage/destroy` handler cannot by itself distinguish a GM despawn from a real combat kill. If a slice uses destruction as a completion signal (Slice 06's Drone 02 does, by recorded source decision), guard it — e.g. only trust destruction when it arrives with nonzero damage values, or route GM cleanup through a path that clears roles/state *before* calling `sbs.delete_object()` so the shared hook has nothing left to match. This applies to every future slice with a GM despawn control over a scorable/gated entity — Slices 09, 11, and 12 are the most likely to hit it again.

---

# 9. Ship data and docking

## 9.1 Reading and writing ship values

**[LIVE]** `act1_generator_tarsis_gate.mast:346-350`, `:312-322`:

```mast
    set_data_set_value(artemis_id, "energy", artemis_start_energy, 0)
    set_data_set_value(artemis_id, "Homing_NUM", value, 0)
    set_data_set_value(artemis_id, "Nuke_NUM", value, 0)
    set_data_set_value(artemis_id, "EMP_NUM", value, 0)
    set_data_set_value(artemis_id, "Mine_NUM", value, 0)

    artemis_object.data_set.set("dock_base_id", tarsis_station_id, 0)
    artemis_object.data_set.set("dock_state", "docked", 0)
    artemis_object.data_set.set("playerThrottle", 0, 0)
```

**[LIVE]** Reading (`act1_engineering_shakedown.mast:227-234`):

```mast
    throttle = artemis_object.data_set.get("playerThrottle", 0)
    dx = artemis_object.pos.x - start_x
    dz = artemis_object.pos.z - start_z
    speed = abs(to_engine_object(artemis_id).cur_speed)
```

**[LIVE]** Range between two objects (`act1_generator_tarsis_gate.mast:605`):

```mast
    range = sbs.distance_id(artemis_id, kestrel_yards_id)
```

## 9.2 Docking wrapper

**[LIVE]** `act1_generator_tarsis_gate.mast:455-489`. A docking handler is a label with yaml metadata and `+++` sections:

```mast
=== khovan_tarsis_normal_docking_resupply_after_clearance ===
metadata: ``` yaml
distance: 600
```
+++ enable
    yield fail if DOCKING_NPC_ID == 0
    yield fail if DOCKING_NPC_ID != tarsis_station_id
    yield fail if not tarsis_required_requests_complete

+++ docking
    set_weapons_selection(DOCKING_PLAYER_ID, 0)
    yield success

+++ docked
    grid_restore_damcons(DOCKING_PLAYER_ID)
    start_counter(DOCKING_PLAYER_ID, "refuel")
```

`+++ enable` decides whether the wrapper applies at all; a `yield fail` there hands off to the next matching wrapper. This is how "reject docking before clearance" and "accept docking after clearance" coexist as two labels.

**[LIVE]** Separate global docking signal (`act1_generator_tarsis_gate.mast:111-125`):

```mast
//shared/signal/docked if has_roles(ORIGIN_ID, "__player__") and has_roles(SELECTED_ID, "tarsis_station")
```

Guard it for premature and duplicate signals — both were observed in Slice 04.

---

# 10. Logging and breadcrumbs

**[LIVE]** Three separate channels, not interchangeable:

```mast
    log("message")                       # mast log
    logger("mast.runtime")               # select logger, then:
    log("message", "mast.runtime")
    script.write_khovan_startup_trace("[KHOVAN ACT1 006] advisory delivered")
```

Breadcrumb convention: `[KHOVAN <AREA> <NUMBER>] <message>`. Breadcrumbs are appended to `tests/live_startup_trace.txt` with an fsync per write, so they survive a hard crash. That is their entire purpose — they bracket risky handoffs so a crash can be located.

`tests/live_startup_trace.txt` (append-only crash breadcrumbs) and `tests/live_smoke_last_bootstrap.txt` (last-success audit) are separate evidence classes. Both are gitignored. Do not merge them.

Per `AGENTS.md` section 5: a breadcrumb marker string is **not** proof of live success. Quick tests may check that markers exist; they must not claim the run worked.

---

# 11. Defensive rules learned the hard way

Every one of these came from a real Slice 01–05 failure.

1. **Guard `artemis_id == 0` before any ship API.** Every single call site. `current_objective_panel.mast:50` and `act1_generator_tarsis_gate.mast:341` both do this and set an explanatory status string instead of failing silently.
2. **None-check every `to_object()`.** Objects disappear.
3. **Duplicate-suppress every message.** Pattern: `if x_sent: ->END` then `x_sent = True` (`audio_runtime.mast:36-40`).
4. **Every automatic gate needs a fallback path and a `*_fallback_available` flag.**
5. **Every delayed task needs a run-ID guard.** See 5.1.
6. **Every spawn needs an existence check and a cleanup routine.** See 8.1, 8.5.
7. **Set a status string on every branch, including the failure branch.** These strings are what the GM Scenario Control overview reads. A silent path is an undiagnosable path.

## Known-bad — do not reintroduce

Guarded by `tests/test_mast_compile_or_preflight.py`:

- `artemis_ship_name` as an identifier in startup files — known bad.
- `sim_create()`, `player_spawn(`, `assign_client_to_ship` in `playable_bootstrap.mast` — LegendaryMissions owns the server/client console and player-spawn lifecycle. Khovan only binds state to the reference-created Artemis (`playable_bootstrap.mast:13-36`).
- Lifeform / upper-left overlay as a text destination — produced a black box. Text currently routes through guarded Comms instead (`audio_runtime.mast:17-18`).
- Temporary Comms proof stations in production startup — removed in Slice 04, `ba794f3`.
- Any runtime reference to `_local_clones`, `archive/old_build_reference`, or `old_mast`. Git-ignored is not runtime-ignored.

---

# 12. API uncertainty format

When this file and local Tier 2 material do not answer a required question, **document the uncertainty; do not invent syntax.** Copy this block into the slice packet and the verification doc:

```text
API uncertainty:
Question:
Sources checked:
What appears documented:
What appears inferred:
Risk:
Recommended spike or next action:
```

If the uncertainty blocks a gameplay gate, the correct response is a spike phase — the pattern Slice 06 used — not a guess wrapped in a fallback.

---

# 13. Maintaining this file

Add an entry when you prove a new API in live smoke. Promote a tag from **[UNPROVEN]** to **[LIVE]** only when a slice verification doc records the live observation. Keep citations pointing at active `scripts/` files, never at `archive/`.
