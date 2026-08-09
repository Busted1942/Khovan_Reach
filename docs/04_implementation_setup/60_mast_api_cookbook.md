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

**Rule for agents: prefer a pattern cited in this file over anything you recall about MAST.** If this file does not cover what you need, use the API-uncertainty format in section 12 — do not invent syntax.

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

### A literal `\n` survives ONLY in a `shared` declaration

**[LIVE]** — found twice by compile preflight on 2026-08-09, both times costing a
failed build.

This works:

```mast
shared engineering_start_text = "Artemis - Captain: Cleared for departure.\nArtemis - Helm: Confirm impulse reads zero."
```

These do **not** — both fail the parser with
`Exception: unterminated string literal (detected at line 1)`:

```mast
    # BROKEN: \n inside an inline comms_receive() argument
    comms_receive("Artemis - Captain: Cleared.\nArtemis - Helm: Confirm.", title="Dillon")

    # BROKEN: \n inside an inline task_schedule() dict
    await task_schedule(khovan_set_current_objective, {"objective_body": "Artemis - Helm: Clear the envelope.\nArtemis - Comms: Confirm."})
```

**Rule: any multi-line player message must live in a `shared` variable and be
passed by name.** The fix for both breakages was mechanical:

```mast
shared kestrel_launch_envelope_objective_text = "Artemis - Helm: Clear the launch envelope, 1 km off Kestrel.\nArtemis - Comms: Confirm when we are out."

    await task_schedule(khovan_set_current_objective, {"objective_body": kestrel_launch_envelope_objective_text})
```

Two related traps when editing these strings:

- **Apostrophes.** A `'` inside the copy has to survive MAST double quotes *and* the single-quoted Python assertions in `tests/` that mirror it. Rewording around the apostrophe is cheaper than escaping in two languages — `"a torpedo's charge"` became `"the charge from a torpedo"` for exactly this reason.
- **Tooling that writes MAST.** A script emitting `"\n"` from a shell heredoc can produce a *real* newline and split the declaration across two lines, which compiles as garbage. Verify with `grep -n ... | cat -A` after any scripted edit.

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

### Two accepted alternatives to a run-ID

Added 2026-08-09, after `tools/review_gate.py` flagged three live observers that
were correct. A run-ID is the default, not the only valid answer. Both of these
close the same hole and both are recognised by the gate:

**1. The bounded polling observer of section 5.2.** It invalidates on shared
state rather than a generation counter — an opening `if <state>: ->END` that a
story jump resets — and bounds itself with a tick ceiling. Note it splits across
two labels: the scheduled entry label holds the delay, and the ceiling lives in
the tick label one `jump` away, so checking only the scheduled label misses it.

**2. A one-shot that re-tests its precondition after the yield**
(`act1_engineering_shakedown.mast`, `khovan_engineering_watch_damcon_rest_cycle`):

```mast
=== khovan_engineering_watch_damcon_rest_cycle ===
    if damcon_rest_cycle_confirmed:
        ->END
    await delay_sim(seconds=8)
    if not damcon_rest_cycle_confirmed:
        damcon_rest_cycle_fallback_available = True
    ->END
```

**The re-check must come after the final delay.** A guard that only runs *before*
the yield proves nothing, because the state it read can change while the task is
suspended. That is not a theoretical concern — it was the real
`khovan_drone_01_reset` bug fixed on 2026-08-09: the label incremented
`drone_contact_sequence_run_id`, yielded, then respawned without ever re-reading
it. **Incrementing a generation counter is not the same as checking one.**

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

**[UNPROVEN — DISCONFIRMED FOR GM ROUTES, corrected 2026-08-08]** Plain (bare) message to the acting console, cited from `scenario_control_panel.mast`:

```mast
    comms_receive(text, title="Khovan Scenario Control", title_color="cyan")
```

This was previously tagged **[LIVE]** in this cookbook, meaning "cited to a working file in this repo" — but "cited to a working file" is not the same evidence class as "confirmed rendering observed live," and this repo's own rule is not to conflate them. Live smoke on 2026-08-08 tested this exact call shape from **every GM-only route in `act1_drone_contact_fire.mast`** (Spawn, Select, Read Target Spike Status, Cleanup) across 3+ sessions: the operator confirmed each handler executes correctly (trace breadcrumbs fire every time, state changes correctly), but **nothing ever rendered visibly on the GM console for any of them.** The Scenario Control Panel uses this identical bare shape and has never been independently confirmed to render either — its own report was never distinguished from "the menu navigates correctly," which is not the same claim.

Contrast: the **same bare shape, called from a player-facing route** (`khovan_drone_contact_fire_hail_spike_target`, Comms hail to a player console) — **is** live-confirmed working (operator report, 2026-08-08). The failure appears specific to GM-only (`COMMS_ORIGIN_ID` gated on `has_roles(..., "gamemaster")`) routes, not to `comms_receive()` in general.

**Do not use this bare shape for a new GM-only route.** Use the `comms_override` shape below instead — it is the only proven-live pattern that has not also failed for a GM route in this build. See `act1_drone_contact_fire.mast:82-176` for an in-progress experimental fix (wraps every GM-only `comms_receive()` call in `comms_override(COMMS_ORIGIN_ID, COMMS_ORIGIN_ID, from_name=...)`), not yet live re-tested. If it also fails, this needs an API-uncertainty escalation to the operator rather than further guessing — see `tests/SLICE06_VERIFICATION.md` Known Risks for the full record.

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

**[UNPROVEN — experimental, 2026-08-08]** The same shape, applied to a GM-only route by using `COMMS_ORIGIN_ID` as both sender and player id, since a GM console has no separate NPC/player pair the way a docking hook does:

```mast
    with comms_override(COMMS_ORIGIN_ID, COMMS_ORIGIN_ID, from_name="Khovan Slice 06 Spike"):
        comms_receive(text, title="Khovan Slice 06 Spike", title_color="cyan")
```

Not yet live re-tested (see `act1_drone_contact_fire.mast`). If confirmed live, this becomes the required shape for every GM-only `comms_receive()` call and `scenario_control_panel.mast` / `story_jump_presets.mast` should be updated to match — they currently use the disconfirmed bare shape above and have never been independently confirmed to render for the GM either.

### The client renders the header as `from_name: title`

**[LIVE]** — observed on a player console 2026-08-09.

`comms_override(..., from_name=X)` and `comms_receive(..., title=Y)` are **two
different fields**, and the client concatenates them. Passing the same string to
both produces a doubled header: `Dillon: Dillon`, `Kestrel Yard Control: Kestrel
Yard Control`.

Give them different values — speaker, then role:

```mast
    with comms_override(sender_id, player_id, from_name="Dillon"):
        comms_receive(text, title="Instructor", title_color="cyan")
```

That renders `Dillon: Instructor`. The stock LegendaryMissions docking traffic
does the same thing, which is why `Tarsis Station (usfp): Tarsis Docking Control`
reads correctly while a hand-rolled message doubles up.

`scripts/systems/audio_runtime.mast` centralises this: `startup_sender` feeds
`from_name`, and an optional `startup_title` feeds `title`, defaulting to
`startup_sender` so existing call sites are unchanged.

**Body text should not repeat the speaker.** Once the header carries it, a
`"Dillon: ..."` prefix inside the message is duplicated on screen. This repo's
convention is that the body opens with the *addressee* instead —
`"Artemis - Engineering: ..."` — with one line per recipient.

Note the split by channel: `comms_receive()` renders a sender header, so the
body names only the addressee. `comms_broadcast()` below renders **body text
only** with no sender at all, so an objective line has to carry everything it
needs on its own.

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

Note `+ "Label":` with a trailing colon opens an inline block; without a colon it takes a label name.

### The cost of a custom Science route — read this before adding one

**Rule: [LIVE]**, operator-confirmed 2026-08-09. **Mechanism: partly [UNPROVEN]** — see the correction note below before relying on the explanation.

**Adding a Khovan `//enable/science` for a contact costs you that contact's stock Science panel.** You lose the `status`/`intel`/`bio` tabs, the A–E shield-frequency bars, and the `WEAP/ENGN/SENS/SHLD` percentages, and you cannot get them back while the route exists. This part is proven: removing the Khovan route from Drone 01 restored the full panel on a live run.

**Correction, 2026-08-09 — do not repeat the original explanation of *why*.** This entry first claimed the stock panel appears because *no* `//enable/science` passes, leaving the engine to render natively. That is wrong. `legendarymissions/science_scans/science.mast:144` carries

```mast
//enable/science if side_are_enemies(SCIENCE_ORIGIN_ID, SCIENCE_SELECTED_ID)
//science if side_are_enemies(...) and has_any_role(SCIENCE_SELECTED_ID, "ship,cockpit")
    + "scan":  + "status":  + "intel":  + "bio":
```

so an enable passes for **every** enemy contact, sbs_utils owns the panel in both the working and the broken case, and those four tabs are LegendaryMissions' own route — not a native engine render. Adding a second, Khovan route changes the resulting tab set. Exactly how the two routes combine is **not yet pinned down**: the observed panels (Khovan's buttons alone pre-fix, the stock four post-fix) are not fully explained by `show_buttons()` alone, and `has_any_role(SCIENCE_SELECTED_ID, "ship,cockpit")` on the stock route is a live variable no Khovan spawn sets explicitly. Treat the rule as reliable and the mechanism as open.

Mechanism so far, from `sbs_utils/procedural/science.py`:

- `start_science_selected()` collects **every** `//enable/science` label in the compiled mission (`labels_get_type("enable/science")`) and runs them. If none pass it calls `t.end()` and returns. In practice, for an enemy contact, the stock route above always passes.
- Once any enable passes, sbs_utils owns the panel and `ScanPromise.show_buttons()` runs:

```python
has_scan = sel_so.data_set.get("scan", origin_so.side)
if has_scan is None:        scan_tabs = "scan"
elif has_scan == "no data": scan_tabs = "scan"
else:                       # only here are //science buttons turned into tabs
sel_so.data_set.set("scan_type_list", scan_tabs, 0)
```

A freshly spawned NPC has `data_set["scan"]` of `None` or the literal `"no data"`, so the panel is **hard-forced to a single `scan` tab** — your custom buttons do not even render. The only escape is putting real text in `data_set["scan"]` via a `<scan>` block or `science_set_scan_data()`, and both of those also overwrite `scan_type_list`.

**So it is strictly either/or:** a Khovan Science route on a contact, **or** that contact's stock scan display. There is no configuration that yields both.

Live evidence (Slice 06, 2026-08-09): Drone 01 with a Khovan `//enable/science` showed one `scan` tab and `no data`. The GM Spike Target — identical `kralien, raider` / `kralien_cruiser` / `behav_npcship`, no Khovan Science route — showed `scan/status/intel/bio` plus the frequency bars with `weak C`. Removing the Khovan route from Drone 01 reproduced the Spike's panel, operator-confirmed.

**Second-order effect — a contact with no scan data is not hailable either.** `comms.py` `set_buttons()` calls `science_is_unknown()` and returns *before* the button loop when it is True, so a never-scanned contact renders as `unknown` with no Comms buttons at all. A `<scan>` block masks this by writing scan text on render; remove the route and the mask goes with it. See section 7.4.

### Custom scan text without losing the panel

**[LIVE]** `act1_generator_tarsis_gate.mast:421-425`. If you only need custom scan *text*, write it directly and skip the route entirely:

```mast
    science_set_scan_data(player_id, tarsis_station_id, "Tarsis Station is the ... contact for Artemis.")
    link(player_id, "extra_scan_source", tarsis_station_id)
```

`link(..., "extra_scan_source", ...)` is **always** paired with `science_set_scan_data`. Using the link alone — as Drone 01 did before 2026-08-09 — is half a pattern and diverts the scan source without supplying a replacement.

### Gating a drill without a Science route

When a drill needs a Science-officer gate on a contact whose stock scan must stay visible, carry the gate on a Comms route and have Science report verbally. `khovan_drone_01_fallback_shield_relay` in `act1_drone_contact_fire.mast` is the worked example.

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

**[UNPROVEN]** `act1_drone_contact_fire.mast:213-248`. This is the highest-risk API in the mission — Slice 06's whole spike exists to test it. Do not build Drone 01 on it until live smoke confirms the fixed version below.

**Bugfix history (2026-08-08):** the original code passed `sbs.SHPSYS.WEAPONS`/`sbs.SHPSYS.ENGINES` as the *default-value* argument of `.get(key, default)` instead of using them as subsystem selectors — `.get()` is a flat key lookup (proven pattern: `artemis_object.data_set.get("playerThrottle", 0)`, section 8), so both fields silently read the same generic `"system_damage"` total. Separately, subsystem-hit detection required `MANUAL_CRITICAL_HIT` to match `DAMAGE_TARGET_ID` **and** `MANUAL_SYSTEM` to be non-`None` in the same event; live smoke on 2026-08-08 showed `MANUAL_SYSTEM` fire once as `SHPSYS.WEAPONS` on an event where `MANUAL_CRITICAL_HIT` was `None`, and the AND discarded that real signal. Full account in `tests/SLICE06_VERIFICATION.md` Known Risks and the Live Smoke Log entry dated 2026-08-08 ("operator pass, weapons exercised") plus its correction.

```mast
//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_slice06_spike_target")
    system = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_SYSTEM")
    target_id = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_CRITICAL_HIT")
    spike_target = to_object(DAMAGE_TARGET_ID)
    if spike_target is not None:
        # No proven per-subsystem data_set key exists yet - both fields read the
        # same generic total until one is proven live. Do not treat them as
        # independently reliable per-subsystem values.
        drone_target_spike_weapons_damage_value = spike_target.data_set.get("system_damage", 0)
        drone_target_spike_engines_damage_value = spike_target.data_set.get("system_damage", 0)
    # Track subsystem-lock (MANUAL_SYSTEM) and critical-hit (MANUAL_CRITICAL_HIT)
    # independently - do not require both in the same event until live evidence
    # justifies it (see bugfix history above).
    if system is not None:
        drone_target_spike_manual_subsystem_hit_observed = True
        drone_target_spike_manual_subsystem = system.name
    if target_id is not None and target_id != 0:
        drone_target_spike_manual_critical_hit_observed = True
    # Consume the manual-hit inventory values unconditionally so they do not leak
    # into the next hit.
    set_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_SYSTEM", None)
    set_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_CRITICAL_HIT", None)
    ->END
```

**[UNPROVEN]** Destruction, with the GM-cleanup-vs-combat-kill guard (`act1_drone_contact_fire.mast:250-284`). The guard's damage-value branch is **confirmed workable on live trace data** (2026-08-08: a GM cleanup produced `weapons_damage=0.0 engines_damage=0.0`; a real Weapons kill produced climbing nonzero values) — the `cleanup_in_progress` flag branch itself still needs a live re-test. Roles are removed and selections cleared, because object cleanup timing is not guaranteed:

```mast
//damage/destroy if has_role(DESTROYED_ID, "khovan_slice06_spike_target")
    drone_target_spike_destroyed_observed = True
    # sbs.delete_object() in cleanup fires this same hook a genuine kill fires.
    # Primary signal: a flag the cleanup handler sets immediately before its
    # delete_object() call, consumed here. Fallback: a real kill leaves nonzero
    # damage; zero damage with no cleanup flag is unattributed, not assumed genuine.
    if drone_target_spike_cleanup_in_progress:
        drone_target_spike_destruction_source = "gm_cleanup"
        drone_target_spike_cleanup_in_progress = False
    elif drone_target_spike_weapons_damage_value > 0 or drone_target_spike_engines_damage_value > 0:
        drone_target_spike_destruction_source = "genuine_weapons_kill"
    else:
        drone_target_spike_destruction_source = "unattributed_zero_damage"
    remove_role(DESTROYED_ID, "khovan_slice06_spike_target")
    ->END
```

The cleanup handler sets the flag immediately before `sbs.delete_object()`, and clears it again after the call as a fallback in case the hook does not fire synchronously in some future Cosmos build:

```mast
=== khovan_drone_contact_fire_cleanup_target_spike ===
    ...
    drone_target_spike_cleanup_in_progress = True
    sbs.delete_object(drone_target_spike_target_id)
    drone_target_spike_cleanup_in_progress = False
    ...
```

Known open questions on this group are listed in `tests/SLICE06_VERIFICATION.md` under Known Risks/API Uncertainties. Read that before touching damage detection.

## 7.4 An unscanned contact has no Comms buttons

**[LIVE]**, confirmed 2026-08-09. A Khovan `//comms` route on a contact renders nothing — the contact shows as `unknown` — until that contact has scan data for the player's side.

From `sbs_utils/procedural/comms.py`, `set_buttons()`:

```python
unk = science_is_unknown(oo, so)
if unk:
    ...send_comms_selection_info(origin_id, "", "white", "unknown")
    return          # returns BEFORE the button loop
```

and `science_is_unknown()` is True while `data_set["scan"]` is `None`, `""`, `"no data"`, or `"Default Scan"` — which is exactly a freshly spawned NPC.

This is easy to miss because a `//science` route with a `<scan>` block masks it: the block writes scan text on panel render, so the contact is silently "known" from the moment it is selected. Delete the Science route (section 7.1) and the Comms route stops rendering too. That is what happened to Drone 01 on 2026-08-09.

Three ways to make a contact known, in order of preference:

1. `science_set_scan_data(player_id, target_id, "...")` at setup — **[LIVE]**, how Tarsis and Kestrel are made hailable (`act1_generator_tarsis_gate.mast:421-425`). Fine for stations. It ends with `target_blob.set("scan_type_list", scan_tabs, 0)` where `scan_tabs` is `""` for a plain string, so do not use it where the stock tab strip matters.
2. `science_update_scan_data(...)` — preserves an existing tab list but writes `scan_type_list` as `"scan"` when it is currently unset. Same hazard, narrower.
3. Write the scan key alone and leave `scan_type_list` untouched — what `khovan_drone_01_mark_scan_known` does:

```mast
    drone_object.data_set.set("scan", drone_01_known_scan_text, artemis_object.side)
```

**[UNPROVEN]** — only `data_set.get()` is proven from MAST (section 9.1); this write is taken from sbs_utils' own internal call. Always pair it with a Comms-side fallback route so the scene survives if it does not take.

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

## 8.2 Stock station role vs custom Comms routes

**[LIVE — corrected 2026-08-09, previous claim DISCONFIRMED]**

This section previously claimed stock station behavior keys off a **capital**
`Station` role, and told you not to clean the pattern up. That was wrong, and it
cost a live session. **Role names are case-insensitive.**

Proof, from `[KHOVAN ACT1 COMMS 003C-ROLES]` on a live 2026-08-09 run: after
`add_role(id, "station")` followed by `add_role(id, "Station")`, the object's
role list contains `'station'` and never `'Station'`. The second call is a no-op.
It follows that `remove_role(id, "Station")` strips lowercase `'station'`.

**What actually matters:** an object holding the stock `station` role gets the
stock station Comms panel, and that panel owns the right-hand option list. A
custom `//comms` block on the same object still evaluates and still writes its
traces, but the player sees the stock panel — a generic `Options` entry under an
`unknown` sender. That is what makes this look like "my routes are not firing"
when they are.

**Rule:** if an object needs custom Khovan Comms options, it must not keep the
stock `station` role.

```mast
    # Clear the stock station role, keep the custom role the //comms block gates on.
    add_role(station_id, "station")
    remove_role(station_id, "Station")   # case-insensitive: this clears 'station'
    add_role(station_id, "kestrel_yards")
```

Both Kestrel and Tarsis use this shape. Tarsis has been live-correct since Slice
04; Kestrel regressed when a fix re-added its stock role and was corrected here.

**Only keep the stock `station` role when the object genuinely needs stock
docking/resupply behavior**, and accept that custom Comms options will not render
for it while it does.

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

### That trailing argument is an INDEX, not a default

**[LIVE] — corrected 2026-08-09. A previous claim in this repo was wrong.**

`sbs_utils/mock/sbs.py:632` declares the getter as:

```python
def get(self, name, index=0):
    values = self.values.get(name, {})
    value = values.get(index, None)
```

So `data_set.get("energy", 0)` means *"read `energy` at index 0"*, not *"read `energy`, defaulting to 0 if missing"*. The setter has always made this obvious — every call above passes a trailing `0` that nobody would read as a default — but the getter was documented backwards.

`act1_drone_contact_fire.mast` carries a comment asserting the opposite, tagged "confirmed live". What was actually confirmed live is that the **fix worked**, and reading index 0 of a scalar returns the same value either way. The live evidence never discriminated between the two readings.

The indexed form is what makes array-valued keys reachable. From `legendarymissions/comms/enemy_surrender.mast:47-52`:

```mast
    blob = to_blob(COMMS_SELECTED_ID)
    ->END if blob is None
    shield_count = blob.get("shield_count", 0)
    ->END if shield_count is None
    s_ratio = 100
    for s in range(shield_count):
        s_max = blob.get("shield_max_val", s )
        s_cur = blob.get("shield_val", s )
        s_ratio = min(s_cur/s_max, s_ratio)
```

`shield_val` is a per-shield array read by index. `shield_count` is scalar, so it takes index 0.

**Consequence for per-subsystem damage.** Slice 06 concluded there is "no proven per-subsystem `data_set` key" after `get("system_damage", sbs.SHPSYS.WEAPONS)` failed. That call may have been closer to correct than the replacement — the enum was in the index slot, which is where a subsystem selector would belong. Slice 06 fixed a *second*, independent bug in the same handler (an `and` that discarded a real `MANUAL_SYSTEM` signal), and that fix alone could explain the recovery. **Still [UNPROVEN]** — nothing here shows `SHPSYS.WEAPONS` is a valid index for `system_damage`. It reopens the question rather than settling it, and it is a cheap thing to test in the Slice 12 combat spike: read `system_damage` at several indices and trace all of them.

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

## 9.3 Engineering console values (power sliders)

**[LIVE]** — confirmed in live Cosmos 2026-08-09 20:44, trace in `tests/live_startup_trace.txt`, record in `tests/SLICE05_VERIFICATION.md`. This is how a gate detects what Engineering actually set, instead of inferring it from ship motion or asking Comms to confirm it.

```mast
    impulse = get_engineering_value(artemis_id, "Impulse", -1)
    warp = get_engineering_value(artemis_id, "Warp", -1)
    set_engineering_value(artemis_id, "front shield", 1.0)
```

`sbs_utils/procedural/space_objects.py:353`. It walks up to 30 `eng_control_label` slots on the ship's data set and returns the matching `eng_control_value`. Matching is case-insensitive (`label.lower() == name.lower()`).

**Label set — use the observed one, not the LegendaryMissions list.** Dumped live from Artemis (`tsn_light_cruiser`) 2026-08-09:

```text
index=0 BEAM    index=1 TORP     index=2 IMPULSE       index=3 WARP
index=4 MANEUVER index=5 SENSORS index=6 FRONT SHIELD  index=7 REAR SHIELD
```

`legendarymissions/gamemaster_comms/gamemaster_comms.mast:50` lists `["Beam", "torpedo", "Impulse", "Warp", "Jump", "Maneuver", "front shield", "rear shield"]`. **That list is wrong for this build in two places** — the real label is `TORP`, not `torpedo`, and there is a `SENSORS` slot with no `Jump`. `get_engineering_value(id, "torpedo")` returns the default here and looks exactly like a slider at rest. Matching is case-insensitive, so `"Impulse"` correctly finds `IMPULSE`.

Slot 3 is rewritten to `"JUMP"` or `"WARP"` per ship depending on drive type (`legendarymissions/ai/grid_ai.mast:37-42`), so a jump-drive hull has no `"Warp"` label at all. Do not assume the set is the same on every hull — dump it with `khovan_engineering_dump_engineering_slots` rather than assuming.

**Scale — confirmed live.** `1.0` means 100%. A console set to impulse 0 / warp 200 read `impulse_raw=0.0 warp_raw=2.005048990249634`.

**Values are live and they ramp.** This is live slider state, not preset storage — it tracked the operator's console in real time across consecutive ticks:

```text
tick=31 impulse_raw=1.0 warp_raw=1.0
tick=32 impulse_raw=0.0 warp_raw=1.0
tick=33 impulse_raw=0.0 warp_raw=1.85654878616333
tick=34 impulse_raw=0.0 warp_raw=2.005048990249634
```

**Always compare with a tolerance band, never equality.** A 200% target settled at `2.005…`, overshooting; `warp == 2.0` would never have matched, and a poll landing on tick 33 would see `1.857`. Use `>= 1.95`-style thresholds.

**A poll must keep watching after arming its fallback.** The confirmation above landed on tick 34, four ticks past the observer's 30-tick timeout. An observer that returns when it arms its Comms fallback throws away the automatic result the crew is seconds away from producing.

**What this cannot see: saved presets.** These are the live sliders. Whether Engineering saved a configuration to a preset slot (the `S`-then-number binding) is not visible here, so "has a preset configured" is not a gateable condition via this key — only "the sliders currently read X".

**Use a negative sentinel as the default**, not `0`. `get_engineering_value` returns the default when the label is not found, and `0` is indistinguishable from a slider genuinely at zero:

```mast
    impulse_raw = get_engineering_value(artemis_id, "Impulse", -1)
    if impulse_raw < 0:
        # label absent on this build - arm the fallback now, do not wait out a timeout
```

Also used in `collisions/collision.mast:39`, `hangar/hangar_comms.mast:19-20,31-32`. The Khovan reference implementation is `khovan_engineering_watch_power_preset` in `act1_engineering_shakedown.mast`; `khovan_engineering_dump_engineering_slots` in the same file dumps every populated slot and is the tool to reach for when a lookup returns its default.

**Not found:** a separate coolant accessor. Treat coolant as unverified.

## 9.4 Buffs and modifiers

**[UNPROVEN]** — not used in this repo yet, listed so gates do not get built on guesses.

`sbs_utils/procedural/modifiers.py` is a full buff/debuff layer over any blob value, with flat/additive/multiplicative stacking and optional durations. Query side:

```python
    modifier_exists(id, source_or_modifier)
    modifiers_get_for_object(obj_or_id, key)
    modifier_get_time_remaining(modifier)
```

Each modifier carries a `source` identifier and only one per source is active at a time, so "is this buff applied" is `modifier_exists(id, "<source>")`. `sbs_utils/procedural/upgrades.py` is a separate, coarser mechanism (`upgrade_add`, `upgrade_remove_all`).

This only sees buffs applied *through those APIs*. Player-driven Engineering console state is section 9.3, not this.

**DAMCON crew state has no clean accessor.** `internal_damage.py` exposes only `grid_restore_damcons()`; team state lives in grid objects and inventory values (`set_inventory_value(SPAWNED_ID, "idle", True)`, `legendarymissions/ai/grid_ai.mast:52`). Readable, but needs real investigation before a gate depends on it.

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

Per `AGENTS.md` section 8: a breadcrumb marker string is **not** proof of live success. Quick tests may check that markers exist; they must not claim the run worked.

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

## 12.1 Open: changing an object's behavior after spawn

```text
API uncertainty:
Question:            How do you change an already-spawned object's behavior
                     module (e.g. stop a station's stock production loop)
                     without despawning and respawning it?

Sources checked:     sbs_utils/proxies/space_object.py:55, sbs_utils/mock/sbs.py:926,
                     this cookbook sections 8.1-8.5, live crash 2026-08-09.

What appears documented:
                     set_behavior(name) exists on space_object, and its docstring
                     lists the valid names as: nebula, npcship, asteroid,
                     playership, station. No behav_ prefix.

What appears inferred:
                     That the same call is reachable from a MAST label on an NPC.
                     It is NOT. to_object() returns an Npc proxy for NPC objects,
                     and Npc has no set_behavior attribute.

Risk:                HIGH, and already realised. The call
                     kestrel_yards_object.set_behavior("behav_playership") crashed
                     the server ('Npc' object has no attribute 'set_behavior') the
                     first time a player confirmed launch-envelope exit. It had
                     two independent faults - wrong receiver AND a behav_ prefix
                     that is not in the documented name set - and static tests plus
                     compile preflight both passed with it in place. This is the
                     section 5 evidence table in one line: compile proves compile.

Recommended spike or next action:
                     Do not reintroduce a behavior swap without proving the call
                     shape on a throwaway spawned object under GM Test Mode first.
                     Prove, in order: (a) how to get a space_object rather than an
                     Npc proxy from an id inside MAST, (b) that set_behavior
                     accepts a bare name like "playership", (c) that the swap
                     actually stops stock production and does not break selection,
                     Comms addressability, or cleanup.
                     Until then Kestrel keeps its stock production loop after
                     departure. That is cosmetic; the crash was not.

Update 2026-08-09 - candidate answer to (a), from Tier 2 review:
                     sbs_utils mkdocs `api/spaceobject.rst` shows the accessor
                     this uncertainty was missing:

                         shipID = sim.make_new_active("behav_station", hull_type)
                         ship = sim.get_space_object(shipID)

                     Confirmed in source: `sbs_utils/mock/sbs.py:795` declares
                     `get_space_object(self, arg0: int) -> space_object`, and
                     `space_object` is the class that defines `set_behavior`
                     (`proxies/space_object.py:55`). So the shape to try is
                     `sim.get_space_object(id).set_behavior("playership")`, not
                     `to_object(id).set_behavior(...)`.

                     Still **[UNPROVEN]**. This is documentation plus a source
                     signature, not a live result, and it does not answer (b) or
                     (c). Do not ship it without the spike.

Naming trap worth keeping separate:
                     Spawn-time and runtime use DIFFERENT behavior-name
                     conventions.
                       - `npc_spawn(..., "behav_station")` - prefixed. Confirmed
                         in the SecretMeeting reference mission
                         (`story.mast:79`) and used throughout this repo.
                       - `set_behavior("station")` - bare. Per its own docstring:
                         "nebula, npcship, asteroid, playership, station".
                     The crashing line used the spawn-time spelling against the
                     runtime API, so it was wrong on both the receiver and the
                     argument.
```

---

# 13. Maintaining this file

Add an entry when you prove a new API in live smoke. Promote a tag from **[UNPROVEN]** to **[LIVE]** only when a slice verification doc records the live observation. Keep citations pointing at active `scripts/` files, never at `archive/`.

---

# 14. Patterns from LegendaryMissions and SecretMeeting

Extracted 2026-08-09 from the Tier 2 clones at
`<Cosmos>/_khovan_reach_tier2_references/reference_missions/_local_clones/`.
LegendaryMissions is 112 MAST files across 27 topic folders and is the richest
API evidence available outside this repo.

**Evidence standing.** These are **[REFERENCE]**: real shipping code from the
official org, so the call shapes are almost certainly valid, but nothing here
has run inside Khovan. Treat a pattern as **[UNPROVEN]** on first use in this
repo and promote it only from a live smoke record. Also remember `AGENTS.md`
section 1 — reference missions supply *syntax*, never scenario design.

Everything below answers a question this repo had actually asked.

## 14.1 Despawning a ship without faking a kill

**[REFERENCE]** `comms/enemy_surrender.mast:130-148`.

Slice 06 learned the hard way that `sbs.delete_object()` fires the same
`//damage/destroy` hook a genuine Weapons kill fires, so cleanup and combat are
indistinguishable at the hook. LegendaryMissions never fights that. It flies
surrendered ships home and deletes them only once they are far away:

```mast
======== take_surrendered_home  =========
    await delay_sim(5)
    surrendered = role("surrendered")
    for ship in surrendered:
        ship_obj = to_object(ship)
        continue if ship_obj is None
        spawn_pos = Vec3(ship_obj.spawn_pos)
        _pos = ship_obj.pos
        target_pos(ship, spawn_pos.x, spawn_pos.y, spawn_pos.z, throttle=1.5, target_id=0)
        diff = _pos - spawn_pos
        continue if diff.length() > 500
        sbs.delete_object(ship)
    jump take_surrendered_home
```

Four things worth stealing:

- **`ship_obj.spawn_pos`** — objects remember where they spawned. No bookkeeping needed to send one home.
- **`target_pos(id, x, y, z, throttle=, target_id=)`** — how to order an NPC to fly somewhere.
- **A role as a work queue.** `role("surrendered")` is the whole list; adding the role enqueues a ship.
- **One self-jumping sweeper** for every ship in that state, rather than a timer per ship.

For Slice 12's `pirate_outcome = fled`, this is the shape to copy: flag the ship, let one sweeper walk it off the map, and delete it far from the player where the destroy hook cannot be confused with a kill.

## 14.2 Surrender

**[REFERENCE]** `comms/enemy_surrender.mast:117-129`. Slice 12 needs
`pirate_surrendered_observed`; this is a complete worked example.

```mast
======== comms_do_surrender ========
    player = to_object(COMMS_ORIGIN_ID)
    ->END if player is None
    comms_receive(f"""OK we give up, {player.name}.""", title_color=surrender_color)
    add_role(COMMS_SELECTED_ID, "surrendered")
    remove_role(COMMS_SELECTED_ID, "raider")
    set_data_set_value(COMMS_SELECTED_ID, "surrender_flag", 1)
    fleet_remove_ship(COMMS_SELECTED_ID)
    yield SUCCESS
```

Note the state change is **four coordinated writes**: add the new role, remove
the combat role, set an engine-visible flag, and pull the ship out of its fleet.
Dropping any one leaves the ship half-surrendered — still targeted by fleet AI,
or still offered a surrender button.

The offering route also shows how to make a Comms option *conditional on ship
state* rather than on mission flags — it reads shield ratio, crew species, and a
per-ship `surrender_count` to decide whether surrender is even plausible. Slice
11's `pirate_cover_status` can gate options the same way.

## 14.3 Guard clauses: the inline form

**[REFERENCE]** used throughout LegendaryMissions.

This repo writes every guard as two lines. The reference code uses a
one-line form, and inside loops a `continue` variant:

```mast
    ->END if blob is None
    ->END if shield_count is None
    continue if ship_obj is None
```

Same semantics as the two-line `if x is None:` / `->END`. Worth adopting for
simple None-checks — `AGENTS.md` section 4 requires the guard, not a particular
spelling, and the terser form makes a long label readable. Keep the block form
when the failure branch has to set a status or a fallback flag.

## 14.4 Hostility and relationship checks

**[REFERENCE]** `ai/npc_brains.mast:30`, `comms/enemy_stations.mast:3`,
`science_scans/science.mast:16`.

```mast
    side_are_enemies(COMMS_ORIGIN_ID, COMMS_SELECTED_ID)
    side_are_allies(SCIENCE_ORIGIN_ID, SCIENCE_SELECTED_ID)
    is_space_object_id(COMMS_SELECTED_ID)
    has_any_role(COMMS_SELECTED_ID, "Station,ship")
```

`side_are_enemies` is the relationship test the whole reference codebase gates
on. Slice 12 needs exactly this to know when pirates have turned hostile, and
`has_any_role(id, "a,b")` is the comma-separated any-of form — distinct from
`has_roles(id, "a, b")`, which is all-of.

## 14.5 Why stock routes win, and the rule that follows

**[LIVE]** in this repo (the Kestrel Comms failure, 2026-08-09), corroborated by
`comms/enemy_stations.mast:3-5` and `comms/enemy_taunt.mast:27`.

Stock Comms and Science routes gate on the generic roles:

```mast
//comms if has_any_role(COMMS_ORIGIN_ID, "__player__,admiral") and side_are_enemies(...) and has_roles(COMMS_SELECTED_ID, 'Station')
//science if side_are_allies(SCIENCE_ORIGIN_ID, SCIENCE_SELECTED_ID) and has_roles(SCIENCE_SELECTED_ID, "Station")
```

So any object carrying a station role is *also* claimed by LegendaryMissions'
own routes, and the stock panel owns the right-hand option list. That is
precisely the Kestrel failure: Khovan's block evaluated and traced every click
while the player saw the stock panel. See section 8.2 for the rule.

The corollary for Act III: a cache, a derelict, or a pirate given a stock role
inherits stock behavior you did not write. Give objects Khovan-specific roles
and add stock roles only when stock behavior is genuinely wanted.

## 14.6 Spawn-time vs runtime behavior names

**[REFERENCE]** `SecretMeeting/story.mast:79`, `LegendaryMissions` throughout.

```mast
    station_object = npc_spawn(0,0,0, "Starbase Phoenix", "tsn, station", "starbase_civil", "behav_station")
    amb_id = npc_spawn(100, 0, -2000, "Praetor of Peace", "Ambassador", "tsn_warpster", "behav_npcship")
    asteroid = terrain_spawn(v2.x, v2.y, v2.z, None, "#,asteroid", a_type, "behav_asteroid")
```

Spawn takes the **prefixed** name (`behav_station`). The runtime `set_behavior()`
API takes the **bare** name (`station`) per its own docstring. See section 12.1 —
mixing the two is what crashed the server on 2026-08-09.

**`set_behavior` appears in none of the 112 LegendaryMissions files.** There is
no precedent to copy, which is itself evidence: changing behavior after spawn is
not a routine operation in this engine. Section 12.1 stays open.

## 14.7 Where to look next

Folders not yet mined, mapped to the slices that will want them:

| Folder | Likely relevant to |
|---|---|
| `docking/` | Slice 10 cache docking — `docking_dock_with_friendly_station`, `docking_dock_with_resupply_ship` |
| `science_scans/` | Slices 07/11 scan gating by role |
| `fleets/` | Slices 11/12 pirate group behavior |
| `damage/`, `collisions/` | Slice 12 combat outcomes |
| `gamemaster/`, `gamemaster_comms/` | GM controls, and the unresolved GM `comms_receive()` rendering question |
| `data_panels/`, `consoles/` | Slice 10 component selection UI |
| `grid_comms/`, `ai/` | Slice 09 DAMCON |

**Method that worked:** grep the clones for the specific API or behavior in
question *before* raising an API uncertainty. Both expensive failures on
2026-08-09 had answers sitting in material this repo already held.
