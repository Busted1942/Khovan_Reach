from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINEERING_PATH = "scripts/acts/act1_engineering_shakedown.mast"
GENERATOR_PATH = "scripts/acts/act1_generator_tarsis_gate.mast"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def code_only(text: str) -> str:
    """Strip MAST comment lines.

    Handlers here cite the reference files their APIs were read out of, and some of
    those paths contain words the assertions below forbid in code (for example
    legendarymissions/gamemaster_comms/...). Assertions about what the runtime does
    must look at code lines only, or citing a source would trip the guard.
    """
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))


def label_body(text: str, label: str) -> str:
    match = re.search(
        rf"^=== {re.escape(label)} ===(?P<body>.*?)(?=^=== |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing label: {label}")
    return match.group("body")


class Act1EngineeringPowerPresetTests(unittest.TestCase):
    """Design 8.4 step 1 - impulse 0 / warp 200 - detected, not just requested."""

    def test_power_preset_has_an_automatic_observer(self) -> None:
        engineering = read(ENGINEERING_PATH)
        body = label_body(engineering, "khovan_engineering_watch_power_preset")

        # Reads the real console values rather than inferring from ship motion.
        # get_engineering_value is sbs_utils/procedural/space_objects.py:353; the
        # label set is legendarymissions/gamemaster_comms/gamemaster_comms.mast:50.
        self.assertIn('get_engineering_value(artemis_id, "Impulse", -1)', body)
        self.assertIn('get_engineering_value(artemis_id, "Warp", -1)', body)

        # Guards required by AGENTS.md section 4.
        self.assertIn("if artemis_id == 0:", body)
        self.assertIn("if artemis_object is None:", body)
        self.assertIn("if power_preset_run_id != engineering_power_preset_run_id:", body)

        # -1 sentinel separates "label absent on this build" from "slider at zero",
        # so a wrong label set arms the fallback at once instead of waiting out the
        # timeout on a lookup that can never succeed.
        self.assertIn("if impulse_raw < 0 or warp_raw < 0:", body)

        # Scale normalisation: collision.mast treats 1.0 as 100%, so warp 200 is 2.0.
        # Anything above 10 is assumed to be a 0-300 style percent and divided.
        self.assertIn("engineering_impulse_value = engineering_impulse_value / 100", body)
        self.assertIn("engineering_warp_value = engineering_warp_value / 100", body)
        self.assertIn("if engineering_impulse_value <= 0.05 and engineering_warp_value >= 1.95:", body)

        # Raw values traced every tick - the first live run is also the experiment
        # that pins down the scale and confirms the label set.
        self.assertIn("impulse_raw={impulse_raw} warp_raw={warp_raw}", body)

    def test_power_preset_gate_ships_with_a_comms_fallback(self) -> None:
        # AGENTS.md section 4: every automatic gate ships with a Comms/GM fallback
        # and a *_fallback_available flag.
        engineering = read(ENGINEERING_PATH)
        self.assertIn(
            '+ "Confirm Impulse 0 / Warp 200" khovan_engineering_confirm_power_preset if engineering_power_preset_fallback_available and not engineering_power_preset_confirmed',
            engineering,
        )
        watch_body = label_body(engineering, "khovan_engineering_watch_power_preset")
        self.assertIn("engineering_power_preset_fallback_available = True", watch_body)
        # Arming the fallback must widen the options, not close the automatic one.
        # The first version returned on timeout, so automatic detection died ~30s in
        # and Comms confirmation became the only route even if the crew got it right
        # a moment later. The guard condition also duplicate-suppresses the arming.
        self.assertIn(
            "if engineering_power_preset_observer_ticks >= 30 and not engineering_power_preset_fallback_available:",
            watch_body,
        )
        self.assertGreater(
            watch_body.index("jump khovan_engineering_watch_power_preset"),
            watch_body.index("engineering_power_preset_observer_ticks >= 30"),
            "observer must keep looping after arming the fallback",
        )

        # Both routes land in one completion label that records which one fired.
        complete_body = label_body(engineering, "khovan_engineering_complete_power_preset")
        self.assertIn("default power_preset_source", complete_body)
        self.assertIn("if engineering_power_preset_confirmed:", complete_body)
        self.assertIn("engineering_power_preset_source = power_preset_source", complete_body)
        self.assertIn(
            '"power_preset_source": "automatic_engineering_value_observer"',
            watch_body,
        )
        self.assertIn(
            '"power_preset_source": "comms_fallback_confirmation"',
            label_body(engineering, "khovan_engineering_confirm_power_preset"),
        )

    def test_navigation_priority_has_an_automatic_slider_observer(self) -> None:
        # Design 8.4 step 12. Target config is in repair_complete_text: impulse 100%,
        # warp 10%, maneuver 190%. Uses the API confirmed live 2026-08-09.
        engineering = read(ENGINEERING_PATH)
        body = label_body(engineering, "khovan_engineering_watch_navigation_priority")

        for call in [
            'get_engineering_value(artemis_id, "Impulse", -1)',
            'get_engineering_value(artemis_id, "Warp", -1)',
            'get_engineering_value(artemis_id, "Maneuver", -1)',
        ]:
            self.assertIn(call, body)

        # Guards required by AGENTS.md section 4.
        self.assertIn("if artemis_id == 0:", body)
        self.assertIn("if artemis_object is None:", body)
        self.assertIn("if navigation_run_id != navigation_priority_run_id:", body)
        self.assertIn("if nav_impulse_raw < 0 or nav_warp_raw < 0 or nav_maneuver_raw < 0:", body)

        # Wide bands, because values ramp and overshoot - a 200% target settled at
        # 2.005 live, so equality never matches. Width is safe here: no other step in
        # 8.4 combines warp this low with maneuver this high.
        self.assertIn(
            "if navigation_impulse_value >= 0.9 and navigation_impulse_value <= 1.1 and navigation_warp_value <= 0.2 and navigation_maneuver_value >= 1.8:",
            body,
        )
        # Keeps looping - no timeout that abandons automatic detection.
        self.assertIn("jump khovan_engineering_watch_navigation_priority", body)

    def test_navigation_priority_routes_share_one_completion_label(self) -> None:
        engineering = read(ENGINEERING_PATH)
        watch = label_body(engineering, "khovan_engineering_watch_navigation_priority")
        confirm = label_body(engineering, "khovan_engineering_confirm_navigation_priority")
        complete = label_body(engineering, "khovan_engineering_complete_navigation_priority")

        self.assertIn('"nav_priority_source": "automatic_engineering_value_observer"', watch)
        self.assertIn('"nav_priority_source": "comms_fallback_confirmation"', confirm)
        # The Comms route keeps its precondition rather than delegating it.
        self.assertIn("if not controlled_overload_repair_confirmed:", confirm)

        # Duplicate-suppressed: this label completes the shakedown and hands off to
        # Slice 06, so reaching it twice would double-fire that handoff.
        self.assertIn("if navigation_priority_preset_set:", complete)
        self.assertIn("await task_schedule(khovan_act1_drone_contact_fire_prepare_after_engineering)", complete)

        # The parameter must not shadow the shared it writes into.
        self.assertIn("default nav_priority_source", complete)
        self.assertIn("navigation_priority_source = nav_priority_source", complete)

        # Fallback is armed when the step opens, not on a timeout, because the
        # saved-preset half of step 12 is not detectable at all.
        repair_body = label_body(engineering, "khovan_engineering_complete_repair")
        self.assertIn("navigation_priority_preset_fallback_available = True", repair_body)
        self.assertIn("task_schedule(khovan_engineering_watch_navigation_priority", repair_body)

    def test_repair_observer_requires_damage_before_it_can_pass(self) -> None:
        # Design 8.4 step 11. internal_damage.py flips __damaged__/__undamaged__ per
        # grid object (:475-476, :742-743), so "repairs complete" is no grid object
        # still carrying __damaged__.
        engineering = read(ENGINEERING_PATH)
        body = label_body(engineering, "khovan_engineering_watch_repair_completion")

        self.assertIn('grid_objects(artemis_id) & role("__damaged__")', body)

        # The overload takes a moment to damage anything. Without the peak guard a
        # poll starting when the step opens sees zero damaged objects and declares
        # victory before a single hallway blew.
        self.assertIn(
            "if controlled_overload_peak_damaged_grid_count > 0 and controlled_overload_damaged_grid_count == 0:",
            body,
        )

        # Second false-pass, closed separately: grid_objects() on a missing ship
        # returns an empty set, which is indistinguishable from "all repaired" once
        # the peak is above zero.
        self.assertIn("if artemis_object is None:", body)
        self.assertLess(
            body.index("if artemis_object is None:"),
            body.index('grid_objects(artemis_id) & role("__damaged__")'),
            "the missing-object guard must run before the damaged count is read",
        )

    def test_damcon_gate_reads_the_buff_not_the_location(self) -> None:
        # Design 8.4 steps 4 and 6. Team location has no accessor; the earned buff
        # does (grid_ai.py:137-148, reset on expiry at grid_ai.mast:243-248), and it
        # is the better signal - it proves the team parked long enough to benefit.
        engineering = read(ENGINEERING_PATH)
        body = label_body(engineering, "khovan_engineering_watch_damcon_rest_cycle")

        self.assertIn('to_object_list(grid_objects(artemis_id) & role("damcons"))', body)
        self.assertIn('get_inventory_value(damcon_team.id, "rested_speed_coeff", 1.0)', body)
        self.assertIn('get_inventory_value(damcon_team.id, "fed_speed_coeff", 1.0)', body)
        self.assertIn("if damcon_rested_team_count > 0 or damcon_fed_team_count > 0:", body)

        # Arms the Comms fallback on the original 8-second schedule (4 ticks x 2s)
        # and keeps watching rather than returning.
        self.assertIn("if damcon_buff_observer_ticks >= 4 and not damcon_rest_cycle_fallback_available:", body)
        self.assertGreater(
            body.index("jump khovan_engineering_watch_damcon_rest_cycle"),
            body.index("damcon_buff_observer_ticks >= 4"),
        )

    def test_no_motion_gate_cannot_pass_on_a_single_acceleration_sample(self) -> None:
        # Live false pass 2026-08-09 21:20:15. tick 14 read throttle=0; tick 15 read
        # throttle=0.966 speed=0.797 distance_sq=13.7 and CONFIRMED - the first tick
        # of ordinary acceleration, 98 seconds before impulse power was set to zero.
        # A ship spinning up from rest satisfies "slow and barely moved" for exactly
        # one sample on its way up.
        engineering = read(ENGINEERING_PATH)
        body = label_body(engineering, "khovan_engineering_watch_no_motion_validation_tick")

        # 1. Sustained, not single-sample.
        self.assertIn("if engineering_no_motion_hold_ticks >= 5:", body)
        self.assertIn("engineering_no_motion_hold_ticks = engineering_no_motion_hold_ticks + 1", body)
        self.assertIn("engineering_no_motion_hold_ticks = 0", body)

        # 2. Only meaningful once impulse power is actually zero. Design 8.4 orders
        # step 1 before step 3, and the power-preset observer is live-confirmed.
        self.assertIn("engineering_power_preset_confirmed and throttle >= 0.95", body)

        # 3. Rolling anchor. The old code measured from a fixed origin, so once
        # Artemis moved the distance term could never return under threshold and the
        # gate became permanently unreachable - the same trace shows distance_sq
        # pinned at 1.9 million while the ship sat still.
        self.assertIn("engineering_no_motion_start_x = artemis_object.pos.x", body)
        self.assertLess(
            body.index("flat_distance_sq = dx * dx + dz * dz"),
            body.index("engineering_no_motion_start_x = artemis_object.pos.x"),
            "the anchor must be re-set after the delta is computed, not before",
        )

    def test_no_motion_observer_keeps_watching_after_arming_its_fallback(self) -> None:
        # Same fix as the power-preset observer. Live 20:30: ticks 1-13 read
        # throttle=0 while the crew were still setting up, then the observer quit at
        # tick 20 and Comms confirmation was the only route left.
        engineering = read(ENGINEERING_PATH)
        body = label_body(engineering, "khovan_engineering_watch_no_motion_validation_tick")
        self.assertIn(
            "if engineering_no_motion_observer_ticks >= 20 and not engineering_no_motion_fallback_available:",
            body,
        )
        self.assertGreater(
            body.index("jump khovan_engineering_watch_no_motion_validation_tick"),
            body.index("engineering_no_motion_observer_ticks >= 20"),
            "observer must keep looping after arming the fallback",
        )

    def test_engineering_slot_dump_diagnostic_exists(self) -> None:
        # Added after the first live run: get_engineering_value resolved both labels
        # but returned 1.0/1.0 unchanged across 30 ticks while the console was set to
        # impulse 0 / warp 200. The dump distinguishes a wrong label-to-slot mapping
        # from eng_control_value simply not tracking the console.
        engineering = read(ENGINEERING_PATH)
        body = label_body(engineering, "khovan_engineering_dump_engineering_slots")
        self.assertIn("for slot_index in range(30):", body)
        self.assertIn('artemis_object.data_set.get("eng_control_label", slot_index)', body)
        self.assertIn('artemis_object.data_set.get("eng_control_value", slot_index)', body)
        self.assertIn("if artemis_id == 0:", body)
        self.assertIn("if artemis_object is None:", body)
        # No control-flow escape inside the loop - breaking out of a MAST for loop is
        # not a proven pattern, so the body uses an if-guard only.
        loop_start = body.index("for slot_index in range(30):")
        self.assertNotIn("->END", body[loop_start:body.index("[KHOVAN ACT1 ENG SLOT DUMP] end", loop_start)])

        watch_body = label_body(engineering, "khovan_engineering_watch_power_preset")
        self.assertIn('"dump_reason": "power_preset_first_tick"', watch_body)
        self.assertIn('"dump_reason": "power_preset_timeout"', watch_body)

    def test_power_preset_observer_is_started_and_reset_with_the_shakedown(self) -> None:
        engineering = read(ENGINEERING_PATH)
        start_body = label_body(engineering, "khovan_act1_engineering_shakedown_start")
        self.assertIn("engineering_power_preset_run_id = engineering_power_preset_run_id + 1", start_body)
        self.assertIn(
            'task_schedule(khovan_engineering_watch_power_preset, {"power_preset_run_id": engineering_power_preset_run_id})',
            start_body,
        )
        # Run ID must be bumped before the schedule call, or the observer captures a
        # stale generation and suppresses itself immediately.
        self.assertLess(
            start_body.index("engineering_power_preset_run_id = engineering_power_preset_run_id + 1"),
            start_body.index("task_schedule(khovan_engineering_watch_power_preset"),
        )
        for label in [
            "khovan_act1_initialize_engineering_shakedown",
            "khovan_act1_engineering_shakedown_prepare_after_tarsis",
        ]:
            body = label_body(engineering, label)
            self.assertIn("engineering_power_preset_confirmed = False", body)
            self.assertIn("engineering_power_preset_fallback_available = False", body)
            self.assertIn("engineering_power_preset_run_id = engineering_power_preset_run_id + 1", body)


class Act1EngineeringShakedownStaticTests(unittest.TestCase):
    def test_slice05_module_exists_imports_and_initializes(self) -> None:
        self.assertTrue((ROOT / ENGINEERING_PATH).is_file())
        main = read("scripts/main.mast")
        self.assertIn(f"import {ENGINEERING_PATH}", main)
        self.assertIn("await task_schedule(khovan_act1_initialize_engineering_shakedown)", main)

        jump_index = main.index("await task_schedule(khovan_story_jump_initialize_registry)")
        engineering_index = main.index("await task_schedule(khovan_act1_initialize_engineering_shakedown)")
        playable_index = main.index("await task_schedule(khovan_reach_initialize_playable_bootstrap)")
        self.assertLess(jump_index, engineering_index)
        self.assertLess(engineering_index, playable_index)

    def test_slice05_state_variables_exist_without_legacy_drill_tree(self) -> None:
        engineering = read(ENGINEERING_PATH)
        for phrase in [
            "shared engineering_shakedown_initialized = False",
            "shared engineering_shakedown_available = False",
            "shared engineering_shakedown_started = False",
            'shared engineering_shakedown_status = "not_initialized"',
            "shared engineering_shakedown_undock_watch_run_id = 0",
            'shared engineering_shakedown_undock_observer_status = "not_started"',
            "shared engineering_impulse_zero_warp_200_requested = False",
            "shared engineering_no_motion_validation_requested = False",
            "shared engineering_no_motion_confirmed = False",
            "shared damcon_rest_cycle_confirmed = False",
            "shared damcon_meal_cycle_confirmed = False",
            "shared controlled_overload_prompt_run_id = 0",
            "shared controlled_overload_prompt_sent = False",
            "shared controlled_overload_started = False",
            "shared controlled_overload_damage_detected = False",
            "shared controlled_overload_repair_confirmed = False",
            "shared controlled_overload_repaired = False",
            "shared navigation_priority_preset_set = False",
            "shared engineering_shakedown_complete = False",
            "shared engineering_shakedown_detection_mode =",
            "shared engineering_shakedown_last_step =",
            "shared engineering_no_motion_fallback_available = False",
            "shared controlled_overload_damage_fallback_available = False",
            "shared navigation_priority_preset_fallback_available = False",
        ]:
            self.assertIn(phrase, engineering)

        for forbidden in [
            "drill_1_",
            "drill_2_",
            "drill_3_",
            "drone_01_spawn",
            "pirate_state_machine",
            "damcon_timer_active = True",
        ]:
            self.assertNotIn(forbidden, engineering)

    def test_slice05_starts_only_after_tarsis_handoff_or_post_tarsis_seed(self) -> None:
        engineering = read(ENGINEERING_PATH)
        generator = read(GENERATOR_PATH)
        start_body = label_body(engineering, "khovan_act1_engineering_shakedown_start")
        prepare_body = label_body(engineering, "khovan_act1_engineering_shakedown_prepare_after_tarsis")
        complete_seed_body = label_body(engineering, "khovan_act1_story_jump_seed_engineering_shakedown_complete")
        normal_resupply_body = label_body(generator, "khovan_tarsis_complete_mechanical_docking_and_resupply")
        post_tarsis_seed_body = label_body(generator, "khovan_act1_story_jump_seed_post_tarsis_handoff")

        self.assertIn("if not generator_governor_cleared or not energy_restored:", start_body)
        self.assertIn("blocked_before_tarsis_handoff", start_body)
        self.assertIn('shakedown_mode = "full"', prepare_body)
        self.assertIn("engineering_shakedown_available = True", prepare_body)
        self.assertIn("engineering_shakedown_complete = False", prepare_body)
        self.assertIn("await task_schedule(khovan_act1_engineering_shakedown_prepare_after_tarsis)", normal_resupply_body)
        self.assertIn("await task_schedule(khovan_act1_engineering_shakedown_prepare_after_tarsis)", post_tarsis_seed_body)
        self.assertIn("await task_schedule(khovan_act1_story_jump_seed_post_tarsis_handoff)", complete_seed_body)
        self.assertIn("engineering_shakedown_complete = True", complete_seed_body)
        self.assertIn('current_beat = "engineering_shakedown_complete"', complete_seed_body)
        self.assertIn('last_checkpoint = "engineering_shakedown_complete"', complete_seed_body)
        self.assertIn("await task_schedule(khovan_act1_drone_contact_fire_prepare_after_engineering)", complete_seed_body)

    def test_player_comms_fallback_route_is_tarsis_gated_and_start_is_undock_triggered(self) -> None:
        engineering = read(ENGINEERING_PATH)
        generator = read(GENERATOR_PATH)
        self.assertIn(
            '//comms if has_roles(COMMS_SELECTED_ID, "tarsis_station") and generator_governor_cleared and not engineering_shakedown_complete',
            engineering,
        )
        for phrase in [
            '+ "Confirm Speed 0 at Full Impulse" khovan_engineering_confirm_no_motion if engineering_no_motion_fallback_available and not engineering_no_motion_confirmed',
            '+ "DamCon Team in Crew Quarters and Rested" khovan_engineering_confirm_damcon_rest_cycle if damcon_rest_cycle_fallback_available and not damcon_rest_cycle_confirmed',
            '+ "Confirm Controlled Overload Started" khovan_engineering_start_controlled_overload if damcon_rest_cycle_confirmed and not controlled_overload_started',
            '+ "Fallback Confirm Controlled Damage" khovan_engineering_confirm_controlled_damage if controlled_overload_damage_fallback_available and not controlled_overload_damage_detected',
            '+ "Confirm Repairs Complete" khovan_engineering_confirm_repair_complete if controlled_overload_repair_fallback_available and not controlled_overload_repair_confirmed',
            '+ "Confirm Combat Posture" khovan_engineering_confirm_navigation_priority if navigation_priority_preset_fallback_available and not navigation_priority_preset_set',
        ]:
            self.assertIn(phrase, engineering)
        self.assertNotIn('"Khovan: Begin Engineering Shakedown"', engineering)
        self.assertNotIn('"Khovan: Fallback DAMCON Mess Standby"', engineering)
        self.assertNotIn("khovan_engineering_confirm_damcon_meal_cycle", engineering)
        prepare_body = label_body(engineering, "khovan_act1_engineering_shakedown_prepare_after_tarsis")
        watch_body = label_body(engineering, "khovan_engineering_watch_tarsis_undock_for_shakedown")
        self.assertIn("engineering_shakedown_undock_watch_run_id = engineering_shakedown_undock_watch_run_id + 1", prepare_body)
        self.assertIn("task_schedule(khovan_engineering_watch_tarsis_undock_for_shakedown", prepare_body)
        self.assertIn("if watch_run_id != engineering_shakedown_undock_watch_run_id:", watch_body)
        self.assertIn('artemis_object.data_set.get("dock_state", "unknown")', watch_body)
        self.assertIn("undock_dock_base_id == tarsis_station_id", watch_body)
        self.assertIn("await delay_sim(seconds=1)", watch_body)
        self.assertIn("await task_schedule(khovan_act1_engineering_shakedown_start)", watch_body)
        self.assertIn("await task_schedule(khovan_act1_engineering_shakedown_prepare_after_tarsis)", label_body(generator, "khovan_tarsis_complete_mechanical_docking_and_resupply"))

        self.assertNotIn("gamemaster", code_only(engineering).lower())
        self.assertNotIn("@gui", engineering)
        self.assertNotIn("//gui", engineering)
        self.assertNotIn("proof_station", engineering.lower())
        self.assertNotIn("proof station", engineering.lower())

    def test_engineering_messages_use_the_guarded_sender_context_wrapper(self) -> None:
        engineering = read(ENGINEERING_PATH)
        message_body = label_body(engineering, "khovan_engineering_send_message")
        self.assertIn("khovan_reach_send_safe_startup_message", message_body)
        self.assertIn('"startup_sender_id": tarsis_station_id', message_body)
        self.assertIn('"startup_player_id": artemis_id', message_body)
        self.assertNotIn("comms_receive(", engineering)

    def test_engineering_sequence_text_and_objectives_exist_in_order(self) -> None:
        engineering = read(ENGINEERING_PATH)
        ordered_labels = [
            "khovan_act1_engineering_shakedown_start",
            "khovan_engineering_confirm_no_motion",
            "khovan_engineering_confirm_damcon_rest_cycle",
            "khovan_engineering_start_controlled_overload",
            "khovan_engineering_confirm_controlled_damage",
            "khovan_engineering_confirm_repair_complete",
            "khovan_engineering_confirm_navigation_priority",
        ]
        label_positions = [engineering.index(f"=== {label} ===") for label in ordered_labels]
        self.assertEqual(label_positions, sorted(label_positions))

        for phrase in [
            "Artemis - Captain: Cleared for departure. Take her 2 km off the station.",
            "Artemis - Engineering: On the captain's order, Impulse 0%, Warp 200%. We are validating heat sinks.",
            "Artemis - Helm: Confirm impulse reads zero, then warp 1. Report speed.",
            "Artemis - Engineering: Good. Set a rally point in a crew quarters and assign a DAMCON team to it. That is where they wait between jobs. Selecting a team also shows its medical status.",
            "Artemis - Engineering: Confirmed.",
            "Artemis - Engineering: Crews work fastest with real time in quarters, mess, and gym. Injured teams go to sickbay. They will run themselves into the ground, so managing them is on you. Look after them when the pressure is low and they will carry you when it is high.",
            "Artemis - Engineering: Controlled overload next. Impulse, Warp, and Maneuver to 300%. Watch your heat and how DAMCON responds.",
            "Artemis - Engineering: Impulse, Warp, and Maneuver to 300% and let them blow. Bleed the heat, track the repair, then return to 100%. Rested, fed, and exercised teams move faster - quarters, mess, and gym each pay separately.",
            "Artemis - Engineering: Damage logged. Repairs are yours. Watch how much faster a rested team crosses the ship.\\nArtemis - Comms: Confirm when repairs are complete.",
            "Artemis - Engineering: Impulse 100%, Warp 10%, Maneuver 190%. Press S at the bottom left, then 2, to save it as your close-quarters preset. Build one for a fight, a transit, and a tow.",
            "Artemis - Comms: Shakedown complete. Confirm when the captain is ready and we will put a training drone in the water.",
            "khovan_act1_drone_contact_fire_prepare_after_engineering",
            '"objective_id": "engineering_impulse_zero_warp_200"',
            '"objective_id": "damcon_crew_quarters_standby"',
            '"objective_id": "controlled_overload_start"',
            '"objective_id": "controlled_overload_damage"',
            '"objective_id": "engineering_repair_supervision"',
            '"objective_id": "navigation_priority_preset"',
            "drone_contact_fire_prepare_after_engineering",
        ]:
            self.assertIn(phrase, engineering)

    def test_observers_and_fallbacks_are_explicit_for_mechanical_gates(self) -> None:
        # Each mechanical gate must declare how it is detected and what it falls back
        # to, so the evidence class of a "pass" is readable off the file.
        engineering = read(ENGINEERING_PATH)
        for phrase in [
            "automatic_playerThrottle_cur_speed_position_delta_observer",
            "automatic_engine_system_damage_observer_with_comms_fallback",
            "automatic_rested_speed_coeff_buff_observer_with_comms_fallback",
            "automatic_fed_speed_coeff_buff_observer_with_comms_fallback",
            "automatic_undamaged_grid_object_observer_with_comms_fallback",
            "automatic_maneuver_190_warp_10_impulse_100_slider_observer_with_comms_fallback",
            # The limit must stay stated: the sliders are readable, saving them to a
            # preset slot is not, so step 12 is only ever half-detected.
            "saving to a preset SLOT is not readable and stays operator-confirmed",
            # Location is still genuinely unreadable - the buff earned is the proxy.
            "DAMCON team LOCATION",
        ]:
            self.assertIn(phrase, engineering)

    def test_engineering_slider_api_is_recorded_as_live_not_unverified(self) -> None:
        # Confirmed live 2026-08-09 20:44: eng_control_value tracks the console in
        # real time (impulse_raw 1.0 -> 0.0, warp_raw 1.0 -> 1.857 -> 2.005 across
        # consecutive ticks) and the gate self-confirmed. The uncertainty note must
        # not keep claiming otherwise - a stale "unverified" marker is what sends the
        # next agent to rebuild a detector that already works.
        engineering = read(ENGINEERING_PATH)
        self.assertNotIn("engineering_slider_keys_unverified", engineering)
        self.assertNotIn("comms_fallback_for_unverified_engineering_slider", engineering)
        uncertainty = engineering[engineering.index("shared engineering_shakedown_api_uncertainty ="):]
        uncertainty = uncertainty[:uncertainty.index("\n")]
        self.assertIn("CONFIRMED LIVE", uncertainty)
        # The observed label set, which differs from the LegendaryMissions list in
        # two places (TORP not torpedo; SENSORS present, no Jump).
        self.assertIn("BEAM/TORP/IMPULSE/WARP/MANEUVER/SENSORS/FRONT SHIELD/REAR SHIELD", uncertainty)
        # Still genuinely open, and must stay recorded as such.
        for still_open in ["DAMCON", "repair completion", "SAVED preset"]:
            self.assertIn(still_open, uncertainty)

        no_motion_watch = label_body(engineering, "khovan_engineering_watch_no_motion_validation_tick")
        for phrase in [
            'throttle = artemis_object.data_set.get("playerThrottle", 0)',
            "speed = abs(artemis_engine_object.cur_speed)",
            "flat_distance_sq <= 25",
            "throttle >= 0.95",
            "speed <= 1",
            "automatic_throttle_speed_position_observer",
            "engineering_no_motion_fallback_available = True",
        ]:
            self.assertIn(phrase, no_motion_watch)

        damage_watch = label_body(engineering, "khovan_engineering_watch_controlled_overload_damage_tick")
        for phrase in [
            'current_engine_damage = artemis_object.data_set.get("system_damage", sbs.SHPSYS.ENGINES)',
            "current_engine_damage > controlled_overload_initial_engine_damage",
            "automatic_engine_system_damage_observer",
            "controlled_overload_damage_fallback_available = True",
        ]:
            self.assertIn(phrase, damage_watch)

        delayed_prompt = label_body(engineering, "khovan_engineering_deliver_controlled_overload_prompt_after_delay")
        for phrase in [
            "await delay_sim(seconds=10)",
            "if prompt_run_id != controlled_overload_prompt_run_id:",
            "if controlled_overload_prompt_sent:",
            "controlled_overload_prompt_sent = True",
            "engineering_message_text\": controlled_overload_prompt_text",
        ]:
            self.assertIn(phrase, delayed_prompt)

        damcon_confirmation = label_body(engineering, "khovan_engineering_complete_damcon_rest_cycle")
        self.assertIn(
            'task_schedule(khovan_engineering_deliver_controlled_overload_prompt_after_delay, {"prompt_run_id": controlled_overload_prompt_run_id})',
            damcon_confirmation,
        )

        for label, required in {
            "khovan_act1_story_jump_seed_engineering_shakedown_complete": [
                "engineering_no_motion_confirmed = True",
                "damcon_rest_cycle_confirmed = True",
                "damcon_meal_cycle_confirmed = True",
                "controlled_overload_started = True",
                "controlled_overload_damage_detected = True",
                "controlled_overload_repaired = True",
                "navigation_priority_preset_set = True",
                "engineering_shakedown_complete = True",
            ],
            "khovan_engineering_complete_no_motion_validation": ["engineering_no_motion_confirmed = True"],
            "khovan_engineering_confirm_damcon_rest_cycle": ["khovan_engineering_complete_damcon_rest_cycle"],
            "khovan_engineering_complete_damcon_rest_cycle": ["damcon_rest_cycle_confirmed = True"],
            "khovan_engineering_start_controlled_overload": ["controlled_overload_started = True"],
            "khovan_engineering_complete_controlled_damage": [
                "controlled_overload_damage_detected = True",
                "controlled_overload_repair_supervision_started = True",
            ],
            "khovan_engineering_confirm_repair_complete": ["khovan_engineering_complete_repair"],
            "khovan_engineering_complete_repair": [
                "controlled_overload_repair_confirmed = True",
                "controlled_overload_repaired = True",
            ],
            # The Comms route now delegates; the flags live in the shared completion
            # label the automatic observer also reaches.
            "khovan_engineering_confirm_navigation_priority": [
                "khovan_engineering_complete_navigation_priority",
            ],
            "khovan_engineering_complete_navigation_priority": [
                "navigation_priority_preset_set = True",
                "engineering_shakedown_complete = True",
            ],
        }.items():
            body = label_body(engineering, label)
            for phrase in required:
                self.assertIn(phrase, body)

    def test_scenario_control_panel_reports_slice05_status_without_new_controls(self) -> None:
        panel = read("scripts/systems/scenario_control_panel.mast")
        self.assertIn("engineering_shakedown_status. {engineering_shakedown_status}", panel)
        self.assertIn("engineering_shakedown_complete. {engineering_shakedown_complete}", panel)
        self.assertNotIn("Force Engineering Shakedown", panel)
        self.assertNotIn("GM Mark Engineering", panel)

    def test_quick_suite_includes_slice05_static_checks(self) -> None:
        runner = read("run_tests.py")
        self.assertIn('ROOT / "tests" / "test_act1_engineering_shakedown_static.py"', runner)

    def test_current_objective_marker_is_slice05_and_leads_blue_text(self) -> None:
        panel = read("scripts/systems/current_objective_panel.mast")
        self.assertIn('shared current_objective_test_marker = "S06"', panel)
        self.assertIn("current_objective_last_message = objective_body", panel)
        self.assertNotIn("current_objective_test_marker}.{current_objective_run_id}", panel)

    def test_slice05_verification_doc_records_static_vs_live_limits(self) -> None:
        path = ROOT / "tests" / "SLICE05_VERIFICATION.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8").lower()
        for phrase in [
            "goal",
            "source sections used",
            "files touched",
            "state variables",
            "runtime flow",
            "gm controls",
            "player-facing behavior",
            "tests/static checks",
            "live smoke checklist",
            "expected observations",
            "failure/ambiguous observations",
            "acceptance covered",
            "acceptance not covered",
            "known risks/api uncertainties",
            "next action",
            "post-tarsis",
            "impulse zero",
            "warp 200",
            "damcon crew-quarters",
            "damcon mess",
            "controlled overload",
            "repair completion",
            "navigation priority",
            "quick/static checks do not prove live cosmos",
        ]:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
