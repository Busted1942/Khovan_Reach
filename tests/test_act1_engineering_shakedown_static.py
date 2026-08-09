from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINEERING_PATH = "scripts/acts/act1_engineering_shakedown.mast"
GENERATOR_PATH = "scripts/acts/act1_generator_tarsis_gate.mast"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def label_body(text: str, label: str) -> str:
    match = re.search(
        rf"^=== {re.escape(label)} ===(?P<body>.*?)(?=^=== |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing label: {label}")
    return match.group("body")


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
            '+ "Khovan: Confirm Speed 0 at Full Impulse" khovan_engineering_confirm_no_motion if engineering_no_motion_fallback_available and not engineering_no_motion_confirmed',
            '+ "Khovan: DamCon Team in Crew Quarters and Rested" khovan_engineering_confirm_damcon_rest_cycle if damcon_rest_cycle_fallback_available and not damcon_rest_cycle_confirmed',
            '+ "Khovan: Confirm Controlled Overload Started" khovan_engineering_start_controlled_overload if damcon_rest_cycle_confirmed and not controlled_overload_started',
            '+ "Khovan: Fallback Confirm Controlled Damage" khovan_engineering_confirm_controlled_damage if controlled_overload_damage_fallback_available and not controlled_overload_damage_detected',
            '+ "Khovan: Confirm Repairs Complete" khovan_engineering_confirm_repair_complete if controlled_overload_repair_fallback_available and not controlled_overload_repair_confirmed',
            '+ "Khovan: Fallback Confirm Navigation Priority" khovan_engineering_confirm_navigation_priority if navigation_priority_preset_fallback_available and not navigation_priority_preset_set',
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

        self.assertNotIn("gamemaster", engineering.lower())
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
            "Captain: You are cleared for departure. Bring your ship to at least 2 KM from the station.",
            "Engineering: On Captin command, set Impulse to 0% and Warp to 200% so we can validate your heat sinks.",
            "Helm: Validate that Impuse speed reads 0, then go to warp 1, wait for the speed to stabilze and report ship speed to captian.",
            "Great, everything is checking out so far. Let's test some internal comms systems next.\\nEngineering: Click on one of the crew quarters, click set rally point, and then choose one of your DamCon teams. This will set their idle position. Note that you can read their medical status when you click on DamCon teams.",
            "Confirmed.",
            "Engineering: Note your crew will be able to work most efficiently when they are allowed lesiure time in their quarters, mess, and gym. If injured, they should be ordered to report to sickbay. The are extreamly dedicated, which puts the preassure on you to manage them well. Take care of your crew when the preassure is low and they will take care of you when the preassure is high.",
            "Engineering: Now we are going to perform a controlled overload to test our damage control systems. Set Impulse, Warp, and Manuver to 300%. Monitor the systems heat and your DamCon team's response to the failure.",
            "Engineering: Now we are going to do a controlled overload exercise. Set Impulse, Warp and Maneyver to 300% and wait for them to overload. Bleed off the excess heat after the overload and monitor your DamCon team progress and then reset them to 100%.",
            "Note that you get a bonus to your sleep, eat and workout bonuses when your teams are in the appropriate rooms, quarters, mess, or rec/gym.",
            "We saw the damage and will leave it to you to monitor repairs. Did you see how your rested crew was able to race through the ship to get to the damage quicker than your non-rested crew? Manage your crew well.\\nComms: Confirm when engineering reports repairs are complete.",
            "repair complete",
            "maneuvering to one hundred ninety percent, warp to ten percent, and impulse to one hundred percent",
            "Engineering systems shakedown complete",
            "Controlled contact handling is next",
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
        engineering = read(ENGINEERING_PATH)
        for phrase in [
            "automatic_playerThrottle_cur_speed_position_delta_observer_engineering_slider_keys_unverified",
            "automatic_engine_system_damage_observer_with_comms_fallback",
            "damcon_location_api_unverified_comms_fallback_after_observer_attempt",
            "engineering_captain_comms_confirmation_fallback_until_repair_completion_api_verified",
            "maneuver_190_warp_10_impulse_100_preset_api_unverified_comms_fallback_after_operator_action",
            "DAMCON location",
            "live Cosmos proof before automatic gates can be claimed",
        ]:
            self.assertIn(phrase, engineering)

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

        damcon_confirmation = label_body(engineering, "khovan_engineering_confirm_damcon_rest_cycle")
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
            "khovan_engineering_confirm_damcon_rest_cycle": ["damcon_rest_cycle_confirmed = True"],
            "khovan_engineering_start_controlled_overload": ["controlled_overload_started = True"],
            "khovan_engineering_complete_controlled_damage": [
                "controlled_overload_damage_detected = True",
                "controlled_overload_repair_supervision_started = True",
            ],
            "khovan_engineering_confirm_repair_complete": [
                "controlled_overload_repair_confirmed = True",
                "controlled_overload_repaired = True",
            ],
            "khovan_engineering_confirm_navigation_priority": [
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
