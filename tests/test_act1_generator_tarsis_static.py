from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACT1_PATH = "scripts/acts/act1_generator_tarsis_gate.mast"
OBJECTIVE_PATH = "scripts/systems/current_objective_panel.mast"


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


class Act1GeneratorTarsisStaticTests(unittest.TestCase):
    def test_slice04_module_exists_and_is_wired_after_playable_bootstrap(self) -> None:
        self.assertTrue((ROOT / ACT1_PATH).is_file())
        self.assertTrue((ROOT / OBJECTIVE_PATH).is_file())
        main = read("scripts/main.mast")
        self.assertIn(f"import {ACT1_PATH}", main)
        self.assertIn(f"import {OBJECTIVE_PATH}", main)
        self.assertIn("await task_schedule(khovan_act1_initialize_generator_tarsis_gate)", main)

        playable_index = main.index("await task_schedule(khovan_reach_initialize_playable_bootstrap)")
        act1_index = main.index("await task_schedule(khovan_act1_initialize_generator_tarsis_gate)")
        self.assertLess(playable_index, act1_index)
        self.assertNotIn("await task_schedule(khovan_reach_stub_dillon_clip_1)", main)

        act1 = read(ACT1_PATH)
        setup_body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        self.assertIn("await task_schedule(khovan_reach_stub_dillon_clip_1)", setup_body)
        self.assertIn("await task_schedule(khovan_current_objective_init)", setup_body)
        self.assertLess(
            setup_body.index("[KHOVAN ACT1 HOLD 002] Artemis mechanical hold fallback active at Kestrel pending departure clearance"),
            setup_body.index("await task_schedule(khovan_current_objective_init)"),
        )
        self.assertLess(
            setup_body.index("await task_schedule(khovan_current_objective_init)"),
            setup_body.index("await task_schedule(khovan_reach_stub_dillon_clip_1)"),
        )
        self.assertLess(
            setup_body.index("await task_schedule(khovan_reach_stub_dillon_clip_1)"),
            setup_body.index("await task_schedule(khovan_act1_show_kestrel_yard_lock_visual_fallback)"),
        )

    def test_act1_required_state_defaults_and_api_uncertainty_markers_exist(self) -> None:
        act1 = read(ACT1_PATH)
        for phrase in [
            "shared act1_generator_tarsis_gate_initialized = False",
            'shared act1_launch_detection_mode = "temporary_comms_confirmation"',
            'shared act1_docking_detection_mode = "temporary_comms_confirmation"',
            'shared act1_text_delivery_mode = "guarded_comms_text_no_lifeform_overlay"',
            'shared act1_comms_archive_status = "trace_and_action_log_stub"',
            "shared kestrel_departure_clearance_granted = False",
            'shared kestrel_yard_lock_visual_mode = "mechanical_yard_lock_overlay_fallback"',
            'shared kestrel_yard_lock_visual_status = "not_initialized"',
            'shared kestrel_comms_options_status = "not_rendered"',
            'shared kestrel_known_contact_status = "not_seeded"',
            "shared kestrel_yard_lock_message_sent = False",
            "shared kestrel_departure_clearance_response_sent = False",
            "shared kestrel_launch_envelope_response_sent = False",
            "shared kestrel_generator_advisory_sent = False",
            "shared kestrel_homing_reserve_prompt_run_id = 0",
            'shared kestrel_homing_reserve_prompt_status = "pending_departure_clearance"',
            "shared kestrel_homing_reserve_prompt_sent = False",
            'shared kestrel_stock_station_role_status = "active_until_launch_envelope_reserve_and_2km"',
            "shared kestrel_stock_station_disable_range_m = 2000",
            "shared kestrel_stock_station_disable_run_id = 0",
            "shared training_speed_power_reminder_sent = False",
            "shared shakedown_prompt_sent = False",
            "shared homing_reserve_count = 2",
            'shared homing_reserve_runtime_apply_status = "stubbed_due_to_ordnance_api_uncertainty"',
            'shared homing_reserve_live_inventory_status = "not_verified"',
            'shared homing_reserve_request_status = "not_requested"',
            'shared homing_reserve_conversion_mode = "kestrel_request_loads_two_homing_once_no_energy_conversion"',
            "shared kestrel_homing_reserve_max_range_m = 600",
            "shared kestrel_launch_envelope_min_range_m = 1000",
            'shared artemis_start_energy_policy = "visible_zero_energy_with_generator_governor_source_authorized"',
            "shared artemis_start_energy = 0",
            "shared artemis_start_homing_torpedoes = 0",
            "shared artemis_start_nukes = 0",
            "shared artemis_start_emps = 0",
            "shared artemis_start_mines = 0",
            'shared artemis_start_ordnance_runtime_apply_status = "not_applied"',
            "shared tarsis_resupply_energy = 1000",
            'shared tarsis_docking_setup_role_status = "not_enabled"',
            "shared tarsis_mechanical_dock_observed = False",
            'shared tarsis_docking_observer_status = "not_started"',
            'shared tarsis_docking_observer_last_snapshot = "not_checked"',
            'shared kestrel_yard_lock_visual_text = "Artemis - Comms: You are in yard-lock until you request departure clearance. Call when the captain is ready."',
            'shared kestrel_homing_reserve_text = "Artemis - Comms: No homing loaded until you request the emergency reserve. Two rounds only; Tarsis restores the rest with the authorization packet."',
            'shared kestrel_homing_reserve_request_text = "Artemis - Weapons: Transfer complete. Two rounds, reserve margin only, not a combat load. Dump one into the engines if the captain wants speed."',
            'shared kestrel_homing_reserve_prompt_text = "',
            'shared tarsis_generator_support_text = "',
            'shared tarsis_hail_text = "',
            'shared tarsis_docking_clearance_text = "Artemis - Helm: Clearance granted. Approach within tolerance and dock."',
            "shared tarsis_resupply_homing_torpedoes = 10",
            "shared tarsis_resupply_nukes = 3",
            "shared tarsis_resupply_emps = 6",
            "shared tarsis_resupply_mines = 6",
            'shared tarsis_resupply_text = "',
            "shared tarsis_generator_support_requested = False",
            "shared tarsis_docking_clearance_requested = False",
            "shared tarsis_generator_support_response_sent = False",
            "shared tarsis_docking_clearance_response_sent = False",
            "shared tarsis_governor_clear_response_sent = False",
            "shared tarsis_required_requests_complete = False",
            'shared tarsis_station_visibility_status = "known_for_slice04_comms_no_hard_science_gate"',
            'shared tarsis_docking_resupply_status = "blocked_until_docking_clearance"',
            'shared tarsis_docking_gate_status = "not_initialized"',
            'shared tarsis_docking_rejection_text = "Artemis - Helm: Clearance not granted. Finish your Comms traffic before you approach."',
            'shared tarsis_comms_options_status = "not_rendered"',
            "shared generator_governor_cleared = False",
        ]:
            self.assertIn(phrase, act1)

    def test_act1_initialize_sets_generator_governor_and_homing_reserve_stub(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_initialize_generator_tarsis_gate")
        for phrase in [
            "mission_phase = \"act_1\"",
            "current_scene = 1",
            "current_beat = \"scene_1_kestrel_departure_gate\"",
            "generator_governor_active = True",
            "generator_governor_cleared = False",
            "starting_homing_torpedoes = 0",
            "homing_reserve_count = 2",
            'homing_reserve_status = "held_by_kestrel_pending_request"',
            'homing_reserve_runtime_apply_status = "pending_kestrel_request"',
            'homing_reserve_live_inventory_status = "fresh_load_zero_requested_live_smoke_required"',
            'homing_reserve_request_status = "not_requested"',
            'homing_reserve_conversion_mode = "kestrel_request_loads_two_homing_once_no_energy_conversion"',
            'artemis_start_energy_policy = "visible_zero_energy_with_generator_governor_source_authorized"',
            "artemis_start_energy = 0",
            'artemis_start_energy_runtime_apply_status = "pending_visible_zero_energy_apply"',
            "artemis_start_homing_torpedoes = 0",
            "artemis_start_nukes = 0",
            "artemis_start_emps = 0",
            "artemis_start_mines = 0",
            'artemis_start_ordnance_runtime_apply_status = "pending_apply"',
            "tarsis_resupply_energy = 1000",
            "tarsis_resupply_homing_torpedoes = 10",
            "tarsis_resupply_nukes = 3",
            "tarsis_resupply_emps = 6",
            "tarsis_resupply_mines = 6",
            "energy_restored = False",
            'tarsis_docking_setup_role_status = "not_enabled"',
            "tarsis_mechanical_dock_observed = False",
            'tarsis_docking_observer_status = "not_started"',
            'tarsis_docking_observer_last_snapshot = "not_checked"',
            "kestrel_yard_lock_message_sent = False",
            "kestrel_departure_clearance_response_sent = False",
            "kestrel_launch_envelope_response_sent = False",
            "kestrel_generator_advisory_sent = False",
            "training_speed_power_reminder_sent = False",
            "shakedown_prompt_sent = False",
            "tarsis_generator_support_response_sent = False",
            "tarsis_docking_clearance_response_sent = False",
            "tarsis_governor_clear_response_sent = False",
            "[KHOVAN ACT1 001] generator governor initialized active",
            "[KHOVAN ACT1 002] homing reserve held at Kestrel pending Comms request count=2",
            "[KHOVAN ACT1 COMMS 001] Kestrel route registered",
            "[KHOVAN ACT1 COMMS 002] Tarsis route registered",
            "await task_schedule(khovan_act1_apply_source_authorized_start_state)",
            "await task_schedule(khovan_act1_setup_kestrel_and_tarsis_contacts)",
        ]:
            self.assertIn(phrase, body)

    def test_act1_applies_source_authorized_visible_zero_energy_start(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_apply_source_authorized_start_state")
        for phrase in [
            "generator_governor_active = True",
            "starting_homing_torpedoes = 0",
            "homing_reserve_count = 2",
            "artemis_start_energy = 0",
            'artemis_start_energy_runtime_apply_status = "pending_visible_zero_energy_apply"',
            'set_data_set_value(artemis_id, "energy", artemis_start_energy, 0)',
            'set_data_set_value(artemis_id, "Homing_NUM", artemis_start_homing_torpedoes, 0)',
            'set_data_set_value(artemis_id, "Nuke_NUM", artemis_start_nukes, 0)',
            'set_data_set_value(artemis_id, "EMP_NUM", artemis_start_emps, 0)',
            'set_data_set_value(artemis_id, "Mine_NUM", artemis_start_mines, 0)',
            'artemis_start_condition_status = "visible_zero_energy_generator_governor_zero_homing_until_kestrel_reserve"',
            'artemis_start_energy_runtime_apply_status = "requested_visible_energy_0"',
            'artemis_start_ordnance_runtime_apply_status = "requested_homing_0_nuke_0_emp_0_mine_0"',
            "[KHOVAN ACT1 START STATE] Artemis starting energy intentionally set to 0 with generator governor active",
            "[KHOVAN ACT1 START STATE] Artemis starting ordnance set to Homing=0 Nuke=0 EMP=0 Mine=0",
            "[KHOVAN ACT1 START STATE FINAL] energy=",
        ]:
            self.assertIn(phrase, body)
        self.assertNotIn("zero-energy start not source-authorized", body)

    def test_story_jump_mission_start_seed_resets_slice04_start_state(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_story_jump_seed_mission_start")
        for phrase in [
            'mission_phase = "act_1"',
            "current_scene = 1",
            'current_beat = "scene_1_kestrel_departure_gate"',
            'last_checkpoint = "mission_start"',
            "transition_held = False",
            "generator_governor_active = True",
            "generator_governor_cleared = False",
            "starting_homing_torpedoes = 0",
            "homing_reserve_count = 2",
            'homing_reserve_status = "held_by_kestrel_pending_request"',
            "artemis_start_energy = 0",
            "artemis_start_homing_torpedoes = 0",
            "artemis_start_nukes = 0",
            "artemis_start_emps = 0",
            "artemis_start_mines = 0",
            "energy_restored = False",
            "kestrel_departure_clearance_granted = False",
            "launch_envelope_cleared = False",
            "kestrel_generator_packet_sent = False",
            "kestrel_generator_advisory_run_id = kestrel_generator_advisory_run_id + 1",
            "kestrel_generator_advisory_sent = False",
            "tarsis_generator_support_requested = False",
            "tarsis_docking_clearance_requested = False",
            "tarsis_required_requests_complete = False",
            "tarsis_resupply_confirmed = False",
            "tarsis_governor_clear_response_sent = False",
            "[KHOVAN JUMP ACT1 START] mission start seed reset Slice 04 generator/Tarsis gate",
            "await task_schedule(khovan_act1_apply_source_authorized_start_state)",
            "await task_schedule(khovan_act1_setup_kestrel_and_tarsis_contacts)",
            "await task_schedule(khovan_set_current_objective",
            '"objective_id": "kestrel_departure_clearance"',
            "Artemis - Comms: Request departure clearance from Kestrel.",
            "await task_schedule(khovan_scenario_control_panel_update_overview)",
        ]:
            self.assertIn(phrase, body)

    def test_story_jump_post_tarsis_seed_sets_resupplied_handoff_state(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_story_jump_seed_post_tarsis_handoff")
        for phrase in [
            'mission_phase = "act_1"',
            "current_scene = 2",
            'current_beat = "await_next_shakedown_instruction"',
            'last_checkpoint = "tarsis_resupply_governor_cleared"',
            "transition_held = False",
            "kestrel_departure_clearance_granted = True",
            "launch_envelope_cleared = True",
            "kestrel_generator_packet_sent = True",
            "kestrel_generator_advisory_run_id = kestrel_generator_advisory_run_id + 1",
            "kestrel_generator_advisory_sent = True",
            "tarsis_generator_support_requested = True",
            "tarsis_docking_clearance_requested = True",
            "tarsis_required_requests_complete = True",
            "tarsis_resupply_confirmed = True",
            "tarsis_governor_clear_response_sent = True",
            'tarsis_gate_status = "resupply_confirmed_governor_cleared"',
            'tarsis_docking_resupply_status = "story_jump_seeded_post_tarsis_handoff"',
            'tarsis_docking_gate_status = "enabled_after_docking_clearance"',
            "generator_governor_active = False",
            "generator_governor_cleared = True",
            "energy_restored = True",
            "[KHOVAN JUMP ACT1 POST TARSIS] post-resupply handoff seed requested",
            "await task_schedule(khovan_act1_setup_kestrel_and_tarsis_contacts)",
            "await task_schedule(khovan_tarsis_enable_docking_after_clearance)",
            "tarsis_mechanical_dock_observed = True",
            'set_data_set_value(artemis_id, "energy", tarsis_resupply_energy, 0)',
            'set_data_set_value(artemis_id, "Homing_NUM", tarsis_resupply_homing_torpedoes, 0)',
            'set_data_set_value(artemis_id, "Nuke_NUM", tarsis_resupply_nukes, 0)',
            'set_data_set_value(artemis_id, "EMP_NUM", tarsis_resupply_emps, 0)',
            'set_data_set_value(artemis_id, "Mine_NUM", tarsis_resupply_mines, 0)',
            "artemis_object.pos = Vec3(18000, 0, 500)",
            'artemis_object.data_set.set("dock_base_id", tarsis_station_id, 0)',
            'artemis_object.data_set.set("dock_state", "docked", 0)',
            '"objective_id": "engineering_shakedown_ready"',
            "Artemis - Engineering: Resupply complete. Stand by for the shakedown.",
            "await task_schedule(khovan_scenario_control_panel_update_overview)",
        ]:
            self.assertIn(phrase, body)

    def test_active_source_docs_authorize_visible_zero_energy_start(self) -> None:
        active_source = "\n".join(
            [
                read("docs/00_project/00_source_index.md"),
                read("docs/01_design/00_scenario_play_guide.md"),
                read("docs/01_design/10_mast_requirements.md"),
                read("docs/01_design/20_gm_operational_notes.md"),
                read("docs/01_design/40_admin_testing_plan.md"),
                read("docs/02_content/40_dillon_clips.md"),
            ]
        )
        for phrase in [
            "visible ship energy = 0",
            "starting_energy = 0",
            "starting_homing_torpedoes = 0",
            "homing_reserve_count = 2",
            "energy_restored = true",
            "Approved Slice 04 implementation finding",
            "Full energy and armament restored",
        ]:
            self.assertIn(phrase, active_source)

        for forbidden in [
            "zero-energy start not source-authorized",
            "Artemis starts with literal zero energy, because that would indicate an unauthorized",
            "Artemis starting energy is not set to 0",
            "This is a better fiction than starting with visibly low energy",
            "The ship is not presented as simply \"low energy\"",
            "Artemis departs with 2 homing torpedoes as emergency conversion reserve",
            "yard-transfer",
            "energy = 250",
        ]:
            self.assertNotIn(forbidden, active_source)

    def test_current_objective_panel_owns_text_waterfall_updates(self) -> None:
        objective = read(OBJECTIVE_PATH)
        for phrase in [
            "shared current_objective_panel_initialized = False",
            'shared current_objective_delivery_mode = "text_waterfall_comms_broadcast"',
            'shared current_objective_api_status = "reference_backed_comms_broadcast_live_smoke_required"',
            'shared current_objective_id = "none"',
            'shared current_objective_title = "Current Objective"',
            'shared current_objective_mode = "text_waterfall"',
            "shared current_objective_visible = False",
            "shared current_objective_run_id = 0",
            'shared current_objective_test_marker = "S06"',
            "=== khovan_current_objective_init ===",
            "=== khovan_set_current_objective ===",
            "=== khovan_clear_current_objective ===",
            "[KHOVAN OBJECTIVE 001] current objective initialized",
            "[KHOVAN OBJECTIVE 002] objective updated: Kestrel departure clearance",
            "current_objective_last_message = objective_body",
            "comms_broadcast(artemis_id, current_objective_last_message, objective_color)",
            "[KHOVAN OBJECTIVE SAFE] text_waterfall update skipped: missing Artemis id",
        ]:
            self.assertIn(phrase, objective)

        for forbidden in [
            "@gui",
            "//gui",
            "button",
            "scenario_control",
            "sbs.send_story_dialog",
            "gui_info_panel_send_message(",
        ]:
            self.assertNotIn(forbidden, objective.lower())

    def test_current_objective_updates_are_wired_to_slice04_triggers(self) -> None:
        act1 = read(ACT1_PATH)
        setup_body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        departure_body = label_body(act1, "khovan_kestrel_request_departure_clearance")
        launch_body = label_body(act1, "khovan_kestrel_report_launch_envelope_clear")
        clearance_body = label_body(act1, "khovan_tarsis_request_docking_clearance")
        resupply_body = label_body(act1, "khovan_tarsis_complete_mechanical_docking_and_resupply")

        expectations = [
            (setup_body, "khovan_current_objective_init", "await task_schedule(khovan_current_objective_init)"),
            (departure_body, "kestrel_launch_envelope_objective_text", "[KHOVAN OBJECTIVE 003] objective updated: launch envelope (1 km minimum)"),
            (launch_body, "Artemis - Comms: Submit the authorization packet to Tarsis, then request docking clearance.", "[KHOVAN OBJECTIVE 005] objective updated: Tarsis requests"),
            (clearance_body, "Artemis - Helm: Bring us alongside and dock. Resupply completes on hard dock.", "[KHOVAN OBJECTIVE 006] objective updated: Tarsis docking/resupply"),
            (resupply_body, "Artemis - Engineering: Resupply complete. Stand by for the shakedown.", "[KHOVAN OBJECTIVE 007] objective updated: Engineering shakedown ready"),
        ]
        for body, text, breadcrumb in expectations:
            self.assertIn(text, body)
            self.assertIn(breadcrumb, body)

    def test_slice04_player_instruction_clarity_copy_is_source_aligned(self) -> None:
        active_copy = "\n".join(
            [
                read(ACT1_PATH),
                read(OBJECTIVE_PATH),
                read("scripts/systems/audio_runtime.mast"),
            ]
        )

        for phrase in [
            "Crew of Artemis, this is a qualification cruise. First task: get the ship out of Kestrel cleanly. Comms, request departure clearance. Helm, hold position until Kestrel releases the yard-lock. Captain, coordinate the sequence.",
            "Artemis - Comms: Request departure clearance from Kestrel.",
            "Artemis - Weapons: Transfer complete. Two rounds, reserve margin only, not a combat load. Dump one into the engines if the captain wants speed.",
            "Kestrel Yard Control: departure clearance granted. Be advised, Artemis is leaving under a temporary generator governor.",
            "kestrel_launch_envelope_objective_text",
            "Kestrel Yard Control logs Artemis clear of the launch envelope. Proceed to Tarsis: submit the authorization packet, then request docking clearance.",
            "Artemis - Captain: Stay on the shakedown plan. The yard commander would like this ship kept in one piece for another ten thousand parsecs.",
            "Artemis - Comms: Submit the authorization packet to Tarsis, then request docking clearance.",
            "Artemis - Comms: We read you. Kestrel signalled your governor. Submit your authorization packet and we will take the generator handoff, then request docking clearance.",
            "Artemis - Comms: Authorization packet accepted, generator handoff logged. We clear the governor and charge your banks once you are docked. Request docking clearance when you are ready.",
            "Artemis - Helm: Clearance granted. Approach within tolerance and dock.",
            "Artemis - Helm: Bring us alongside and dock. Resupply completes on hard dock.",
            "Artemis - Helm: Clearance not granted. Finish your Comms traffic before you approach.",
            "Artemis - Captain: Authorization packet closed out. Governor cleared, banks charged, ordnance restored. You are released to complete your shakedown.",
            "Artemis - Engineering: Resupply complete. Stand by for the shakedown.",
        ]:
            self.assertIn(phrase, active_copy)

        for forbidden in [
            "Our docking systems aren't compatible with yours",
            "Artemis now carries two homing torpedoes as generator-governor margin",
            "We have issued two homing torpedoes as emergency conversion reserve",
            "Other ordnance will load as available after homing complement is restored",
            "Do not assume full acceleration response until transfer complete",
            "Your generator assembly is still under observation",
            "Treat the generator advisory as active until Tarsis completes the handoff",
            "Helm may clear the launch envelope.",
            "Complete required traffic before approach.",
            "Captain. Crew of Artemis. This is a qualification cruise. Standard pattern",
            "Captain, the ship is yours.",
            "yard-transfer",
        ]:
            self.assertNotIn(forbidden, active_copy)

    def test_kestrel_and_tarsis_use_reference_backed_standard_station_primitives(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        for phrase in [
            'npc_spawn(0, 0, 0, "Kestrel Yards", "tsn, station, kestrel_yards, khovan_origin", "starbase_command", "behav_station")',
            'npc_spawn(18000, 0, 0, "Tarsis Station", "tsn, station, tarsis_station, khovan_drill_resupply", "starbase_command", "behav_station")',
            "set_face(kestrel_yards_id, random_terran(civilian=True))",
            'sim.add_navproxy(kestrel_yards_id, "Kestrel Yards", "starbase_command", "#4A7")',
            "set_face(tarsis_station_id, random_terran(civilian=True))",
            'sim.add_navproxy(tarsis_station_id, "Tarsis Station", "starbase_command", "#4A7")',
            'add_role(kestrel_yards_id, "Station")',
            'remove_role(kestrel_yards_id, "station")',
            'add_role(tarsis_station_id, "Station")',
            'remove_role(tarsis_station_id, "station")',
            'add_role(kestrel_yards_id, "kestrel_yards")',
            'add_role(tarsis_station_id, "tarsis_station")',
            "[KHOVAN ACT1 COMMS 004A] Tarsis Station spawn attempted",
            "[KHOVAN ACT1 COMMS 004B] Tarsis Station spawned id=",
            "[KHOVAN ACT1 COMMS 003] Kestrel standard station setup complete roles=",
            "[KHOVAN ACT1 COMMS 004] Tarsis standard station setup complete roles=",
            "[KHOVAN ACT1 SCAN 001] Tarsis contact available for Slice 04 Comms; Science scan remains observational only",
            "[KHOVAN ACT1 DOCK 001] docking setup scheduled",
            "[KHOVAN ACT1 DOCK 001K] Kestrel Legendary docking helper skipped for startup mechanical hold fallback",
            "await task_schedule(docking_standard_player_station)",
            'add_role(kestrel_yards_id, "station")',
            'add_role(kestrel_yards_id, "Station")',
            'add_role(kestrel_yards_id, "kestrel_yards")',
            'kestrel_comms_options_status = "stock_station_role_cleared_kestrel_yards_retained_for_khovan_comms"',
            "[KHOVAN ACT1 COMMS 003B] Kestrel stock station role cleared; kestrel_yards retained for Khovan Comms options",
            'add_role(tarsis_station_id, "station")',
            'remove_role(tarsis_station_id, "Station")',
            'tarsis_comms_options_status = "station_role_restored_after_docking_helper_pass"',
            "[KHOVAN ACT1 COMMS 004D] Tarsis station role restored and stock Station role removed after docking helper pass for Khovan Comms options",
            'science_set_scan_data(artemis_id, kestrel_yards_id, "Kestrel Yards is Artemis\' launch yard and active departure-control contact.")',
            'link(artemis_id, "extra_scan_source", kestrel_yards_id)',
            'kestrel_known_contact_status = "seeded_via_bound_artemis"',
            "[KHOVAN ACT1 COMMS 003K] Kestrel scan data seeded for Artemis id=",
            'science_set_scan_data(player_id, tarsis_station_id, "Tarsis Station is the Kestrel generator handoff and resupply contact for Artemis.")',
            "docking_set_docking_logic(player_id, tarsis_station_id, khovan_tarsis_docking_rejected_before_clearance)",
            'tarsis_docking_gate_status = "blocked_until_docking_clearance"',
            "[KHOVAN ACT1 DOCK 002] docking setup applied or failed/stubbed",
            'tarsis_docking_resupply_status = "preclearance_docking_blocked_resupply_unproven"',
            "[KHOVAN ACT1 DOCK 002A] Tarsis pre-clearance docking blocker installed id=",
            "[KHOVAN ACT1 DOCK 003] Tarsis docking setup held behind docking clearance",
            "[KHOVAN ACT1 DOCK 003A] Premature Tarsis docking uses Khovan clearance-denied handler until clearance; dock-button visibility requires live proof",
            "[KHOVAN ACT1 COMMS 003A] Kestrel marked known to player ships for departure Comms",
            "[KHOVAN ACT1 COMMS 004C] Tarsis Slice 04 Comms contact available without hard Science-scan gate",
            "[KHOVAN ACT1 003C] Kestrel/Tarsis use reference-backed standard station primitives",
            "[KHOVAN ACT1 003D] Khovan station presentation polish deferred until standard Comms/docking path is proven",
        ]:
            self.assertIn(phrase, body)

        for forbidden in [
            '"tsn, friendly, kestrel_yards, khovan_origin"',
            '"tsn, friendly, tarsis_station, khovan_drill_resupply"',
            "khovan_act1_comms_test_option",
            "Khovan Test Option",
            "khovan_reach_keep_tarsis_priority_docking_hidden",
            "Kernel Known Station",
            "Kernel Scan-Gated Station",
            "Kernel Dock Station",
            "station_comms_docking_kernel",
            "khovan_station_comms_docking_kernel_init",
        ]:
            self.assertNotIn(forbidden, body)

    def test_kestrel_start_hold_skips_transition_only_docking_helper(self) -> None:
        act1 = read(ACT1_PATH)
        setup_body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        self.assertIn('remove_role(kestrel_yards_id, "station")', setup_body)
        self.assertIn(
            'kestrel_start_docking_helper_status = "skipped_startup_hold_uses_mechanical_fallback"',
            setup_body,
        )
        self.assertIn(
            "[KHOVAN ACT1 DOCK 001K] Kestrel Legendary docking helper skipped for startup mechanical hold fallback",
            setup_body,
        )
        self.assertNotIn(
            "docking_set_docking_logic(player_id, kestrel_yards_id, docking_dock_with_friendly_station)",
            setup_body,
        )
        self.assertNotIn(
            "docking_set_docking_logic(player_id, tarsis_station_id, docking_dock_with_friendly_station)",
            setup_body,
        )
        self.assertIn(
            "docking_set_docking_logic(player_id, tarsis_station_id, khovan_tarsis_docking_rejected_before_clearance)",
            setup_body,
        )
        self.assertLess(
            setup_body.index('remove_role(kestrel_yards_id, "station")'),
            setup_body.index("await task_schedule(docking_standard_player_station)"),
        )
        self.assertLess(
            setup_body.index("await task_schedule(docking_standard_player_station)"),
            setup_body.index('kestrel_comms_options_status = "stock_station_role_cleared_kestrel_yards_retained_for_khovan_comms"'),
        )

    def test_kestrel_comms_known_state_uses_bound_artemis_and_preserves_routes(self) -> None:
        act1 = read(ACT1_PATH)
        setup_body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        for phrase in [
            "if artemis_id == 0 or kestrel_yards_id == 0:",
            'kestrel_known_contact_status = "failed_missing_artemis_or_kestrel_id"',
            "kestrel_scan_seed_artemis = to_object(artemis_id)",
            "kestrel_scan_seed_object = to_object(kestrel_yards_id)",
            "if kestrel_scan_seed_artemis is None or kestrel_scan_seed_object is None:",
            'kestrel_known_contact_status = "failed_missing_artemis_or_kestrel_object"',
            'science_set_scan_data(artemis_id, kestrel_yards_id, "Kestrel Yards is Artemis\' launch yard and active departure-control contact.")',
            'link(artemis_id, "extra_scan_source", kestrel_yards_id)',
            'kestrel_known_contact_status = "seeded_via_bound_artemis"',
            "[KHOVAN ACT1 COMMS 003K] Kestrel scan data seeded for Artemis id=",
            'remove_role(kestrel_yards_id, "Station")',
            'add_role(kestrel_yards_id, "kestrel_yards")',
        ]:
            self.assertIn(phrase, setup_body)

        self.assertNotIn("khovan_act1_finalize_kestrel_opening_comms", act1)
        self.assertNotIn("science_set_scan_data(player_id, kestrel_yards_id", setup_body)

        for route in [
            '+ "Hail Kestrel Yards" khovan_kestrel_hail',
            '+ "Request Departure Clearance" khovan_kestrel_request_departure_clearance',
            '+ "Request Emergency Homing Reserve" khovan_kestrel_request_emergency_homing_reserve',
            '+ "Confirm Launch-Envelope Exit" khovan_kestrel_report_launch_envelope_clear',
        ]:
            self.assertIn(route, act1)

    def test_tarsis_docking_setup_waits_for_docking_clearance(self) -> None:
        act1 = read(ACT1_PATH)
        setup_body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        clearance_body = label_body(act1, "khovan_tarsis_request_docking_clearance")
        enable_body = label_body(act1, "khovan_tarsis_enable_docking_after_clearance")

        self.assertLess(
            setup_body.index('remove_role(tarsis_station_id, "station")'),
            setup_body.index("await task_schedule(docking_standard_player_station)"),
        )
        self.assertLess(
            setup_body.index("await task_schedule(docking_standard_player_station)"),
            setup_body.index('add_role(tarsis_station_id, "station")'),
        )
        self.assertLess(
            setup_body.index('add_role(tarsis_station_id, "station")'),
            setup_body.index("docking_set_docking_logic(player_id, tarsis_station_id, khovan_tarsis_docking_rejected_before_clearance)"),
        )
        self.assertIn(
            "docking_set_docking_logic(player_id, tarsis_station_id, khovan_tarsis_docking_rejected_before_clearance)",
            setup_body,
        )
        self.assertNotIn(
            "docking_set_docking_logic(player_id, tarsis_station_id, docking_dock_not_allowed)",
            setup_body,
        )
        self.assertNotIn(
            "docking_set_docking_logic(player_id, tarsis_station_id, docking_dock_with_friendly_station)",
            setup_body,
        )
        self.assertIn(
            "if not tarsis_generator_support_requested:",
            clearance_body,
        )
        self.assertIn("await task_schedule(khovan_tarsis_enable_docking_after_clearance)", clearance_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004R] Tarsis requests complete=", clearance_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004D] Tarsis docking clearance granted; enabling docking setup", clearance_body)
        self.assertIn("if not tarsis_docking_clearance_requested:", enable_body)
        self.assertIn("[KHOVAN ACT1 DOCK 003B] Tarsis docking setup enable blocked before clearance", enable_body)
        self.assertIn('add_role(tarsis_station_id, "station")', enable_body)
        self.assertIn('add_role(tarsis_station_id, "Station")', enable_body)
        self.assertIn('tarsis_docking_setup_role_status = "station_and_Station_roles_restored_after_clearance"', enable_body)
        self.assertIn('tarsis_docking_observer_status = "watching_after_clearance"', enable_body)
        self.assertIn('tarsis_docking_observer_last_snapshot = "not_checked"', enable_body)
        self.assertIn("tarsis_roles_after_clearance = to_object(tarsis_station_id).get_roles()", enable_body)
        self.assertIn("tarsis_docking_player = to_object(player_id)", enable_body)
        self.assertIn('tarsis_docking_player.data_set.set("dock_base_id", 0, 0)', enable_body)
        self.assertIn('tarsis_docking_player.data_set.set("dock_state", "undocked", 0)', enable_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004N] normalized Artemis dock_state=undocked dock_base_id=0 before Tarsis docking setup", enable_body)
        self.assertIn(
            "docking_set_docking_logic(player_id, tarsis_station_id, khovan_tarsis_normal_docking_resupply_after_clearance)",
            enable_body,
        )
        self.assertIn("[KHOVAN ACT1 DOCK 004P] Tarsis normal docking/resupply wrapper set player_id=", enable_body)
        self.assertIn('tarsis_docking_gate_status = "enabled_after_docking_clearance"', enable_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004S] Tarsis stock Station role restored after clearance for mechanical docking affordance", enable_body)
        self.assertIn("await task_schedule(docking_standard_player_station)", enable_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004U] standard friendly station docking helper rerun for Tarsis after clearance", enable_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004] Tarsis docking setup enabled after clearance", enable_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004B] Tarsis docking setup awaiting dock signal after clearance", enable_body)
        self.assertIn("task_schedule(khovan_tarsis_watch_mechanical_docking_after_clearance)", enable_body)

        blocked_body = label_body(act1, "khovan_tarsis_docking_rejected_before_clearance")
        self.assertIn("yield fail if DOCKING_NPC_ID == 0", blocked_body)
        self.assertIn("yield fail if tarsis_docking_clearance_requested", blocked_body)
        self.assertIn("yield fail if DOCKING_NPC_ID != tarsis_station_id", blocked_body)
        self.assertIn('tarsis_docking_gate_status = "preclearance_docking_rejected_missing_clearance"', blocked_body)
        self.assertIn("[KHOVAN ACT1 DOCK BLOCKED] Tarsis docking rejected: clearance not granted", blocked_body)
        self.assertIn('with comms_override(DOCKING_NPC_ID, DOCKING_PLAYER_ID, from_name="Tarsis Docking Control"):', blocked_body)
        self.assertIn('"Docking Clearance Required"', blocked_body)
        self.assertIn("% {tarsis_docking_rejection_text}", blocked_body)
        self.assertIn("yield fail", blocked_body)
        self.assertNotIn("Our docking systems aren't compatible with yours", blocked_body)
        self.assertNotIn("docking_dock_not_allowed", blocked_body)
        self.assertEqual(
            1,
            act1.count("[KHOVAN ACT1 DOCK BLOCKED] Tarsis docking rejected: clearance not granted"),
        )

        normal_body = label_body(act1, "khovan_tarsis_normal_docking_resupply_after_clearance")
        self.assertIn("distance: 600", normal_body)
        self.assertIn("yield fail if DOCKING_NPC_ID == 0", normal_body)
        self.assertIn("yield fail if DOCKING_NPC_ID != tarsis_station_id", normal_body)
        self.assertIn("yield fail if not tarsis_required_requests_complete", normal_body)
        self.assertIn("+++ docking", normal_body)
        self.assertIn('set_weapons_selection(DOCKING_PLAYER_ID, 0)', normal_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004X] Tarsis normal docking wrapper accepted docking attempt after clearance", normal_body)
        self.assertIn("yield success", normal_body)
        self.assertIn("+++ docked", normal_body)
        self.assertIn("grid_restore_damcons(DOCKING_PLAYER_ID)", normal_body)
        self.assertIn('start_counter(DOCKING_PLAYER_ID, "refuel")', normal_body)
        self.assertIn('start_counter(DOCKING_PLAYER_ID, "torps")', normal_body)
        self.assertIn('start_counter(DOCKING_PLAYER_ID, "shields")', normal_body)
        self.assertIn('start_counter(DOCKING_PLAYER_ID, "interior")', normal_body)
        self.assertIn('tarsis_docking_observer_status = "normal_docking_wrapper_docked_after_clearance"', normal_body)
        self.assertIn('tarsis_docking_resupply_status = "normal_docking_wrapper_resupply_scheduled"', normal_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004A] Tarsis dock signal observed after clearance; normal station resupply scheduled", normal_body)
        self.assertIn('task_schedule(khovan_tarsis_complete_mechanical_docking_and_resupply, {"ship_id": DOCKING_PLAYER_ID, "completion_source": "normal_docking_wrapper"})', normal_body)
        self.assertIn("+++ refit", normal_body)
        self.assertIn('DOCKING_PLAYER.data_set.set("energy", tarsis_resupply_energy, 0)', normal_body)
        self.assertIn('DOCKING_PLAYER.data_set.set("Homing_NUM", tarsis_resupply_homing_torpedoes, 0)', normal_body)
        self.assertIn('DOCKING_PLAYER.data_set.set("Nuke_NUM", tarsis_resupply_nukes, 0)', normal_body)
        self.assertIn('DOCKING_PLAYER.data_set.set("EMP_NUM", tarsis_resupply_emps, 0)', normal_body)
        self.assertIn('DOCKING_PLAYER.data_set.set("Mine_NUM", tarsis_resupply_mines, 0)', normal_body)
        self.assertIn("+++ throttle", normal_body)
        self.assertIn('DOCKING_PLAYER.data_set.set("playerThrottle", 0, 0)', normal_body)

        self.assertIn(
            '//shared/signal/docked if has_roles(ORIGIN_ID, "__player__") and has_roles(SELECTED_ID, "tarsis_station")',
            act1,
        )
        dock_signal = re.search(
            r'^//shared/signal/docked if has_roles\(ORIGIN_ID, "__player__"\) and has_roles\(SELECTED_ID, "tarsis_station"\)\n(?P<body>.*?)(?=^//|^=== |\Z)',
            act1,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(dock_signal)
        self.assertIn("if not tarsis_docking_clearance_requested:", dock_signal.group("body"))
        self.assertIn('tarsis_docking_gate_status = "premature_dock_signal_ignored_before_clearance"', dock_signal.group("body"))
        self.assertIn("[KHOVAN ACT1 DOCK 003D] Premature Tarsis dock signal ignored before clearance", dock_signal.group("body"))
        self.assertIn("if tarsis_mechanical_dock_observed:", dock_signal.group("body"))
        self.assertIn("[KHOVAN ACT1 DOCK 004C] Duplicate Tarsis mechanical dock observation suppressed", dock_signal.group("body"))
        self.assertIn(
            "[KHOVAN ACT1 DOCK 004A] Tarsis dock signal observed after clearance; normal station resupply scheduled",
            dock_signal.group("body"),
        )
        self.assertIn('await task_schedule(khovan_tarsis_complete_mechanical_docking_and_resupply, {"ship_id": ORIGIN_ID, "completion_source": "docked_signal"})', dock_signal.group("body"))
        self.assertIn("tarsis_mechanical_dock_observed = True", dock_signal.group("body"))
        self.assertIn('tarsis_docking_observer_status = "signal_observed_after_clearance"', dock_signal.group("body"))

        observer_body = label_body(act1, "khovan_tarsis_watch_mechanical_docking_after_clearance")
        self.assertIn("if tarsis_mechanical_dock_observed:", observer_body)
        self.assertIn('for player_id in role("__player__"):', observer_body)
        self.assertIn('observed_dock_state = observed_player.data_set.get("dock_state", 0)', observer_body)
        self.assertNotIn(
            '.data_set.get("dock_state", 0).data_set.get("dock_state", 0)',
            observer_body,
            "dock_state is already a scalar value; do not dereference it as an object",
        )
        self.assertIn('observed_dock_base_id = observed_player.data_set.get("dock_base_id", 0)', observer_body)
        self.assertIn('observer_snapshot = f"player={player_id} state={observed_dock_state} base={observed_dock_base_id} tarsis={tarsis_station_id}"', observer_body)
        self.assertIn("if observer_snapshot != tarsis_docking_observer_last_snapshot:", observer_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004T] Tarsis dock-state observer", observer_body)
        self.assertIn('if observed_dock_base_id == tarsis_station_id and observed_dock_state == "docked":', observer_body)
        self.assertIn('tarsis_docking_observer_status = "dock_state_observed_after_clearance"', observer_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004A] Tarsis dock signal observed after clearance; normal station resupply scheduled", observer_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004C] Tarsis dock-state observer confirmed docked state after clearance", observer_body)
        self.assertIn('await task_schedule(khovan_tarsis_complete_mechanical_docking_and_resupply, {"ship_id": player_id, "completion_source": "dock_state_observer"})', observer_body)
        self.assertIn("await delay_sim(seconds=1)", observer_body)
        self.assertIn("jump khovan_tarsis_watch_mechanical_docking_after_clearance", observer_body)

    def test_kestrel_departure_hold_clamps_artemis_until_comms_clearance(self) -> None:
        act1 = read(ACT1_PATH)
        for phrase in [
            'shared kestrel_departure_hold_status = "not_initialized"',
            'shared kestrel_departure_hold_release_status = "not_released"',
            'shared kestrel_departure_hold_detection_mode = "mechanical_position_throttle_hold_no_legendary_docking"',
            'shared kestrel_start_docking_helper_status = "not_initialized"',
        ]:
            self.assertIn(phrase, act1)

        init_body = label_body(act1, "khovan_act1_initialize_generator_tarsis_gate")
        self.assertIn('kestrel_departure_hold_status = "waiting_for_contact_setup"', init_body)
        self.assertIn('kestrel_departure_hold_release_status = "not_released"', init_body)
        self.assertIn('kestrel_start_docking_helper_status = "not_initialized"', init_body)

        setup_body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        self.assertIn('kestrel_departure_hold_status = "scheduled"', setup_body)
        self.assertIn("[KHOVAN ACT1 HOLD 001] Kestrel departure hold scheduled", setup_body)
        for phrase in [
            "artemis_object = to_object(artemis_id)",
            "artemis_object.pos = Vec3(0, 0, 500)",
            'artemis_object.data_set.set("dock_base_id", 0, 0)',
            'artemis_object.data_set.set("dock_state", "undocked", 0)',
            'artemis_object.data_set.set("playerThrottle", 0, 0)',
            'kestrel_departure_hold_status = "active"',
            'kestrel_departure_hold_release_status = "waiting_for_clearance"',
            "[KHOVAN ACT1 HOLD 002] Artemis mechanical hold fallback active at Kestrel pending departure clearance",
        ]:
            self.assertIn(phrase, setup_body)
        self.assertIn("task_schedule(khovan_act1_hold_artemis_at_kestrel_until_clearance)", setup_body)
        self.assertLess(
            setup_body.index("[KHOVAN ACT1 DOCK 002] docking setup applied or failed/stubbed"),
            setup_body.index("[KHOVAN ACT1 HOLD 001] Kestrel departure hold scheduled"),
        )
        self.assertLess(
            setup_body.index("[KHOVAN ACT1 HOLD 001] Kestrel departure hold scheduled"),
            setup_body.index("[KHOVAN ACT1 HOLD 002] Artemis mechanical hold fallback active at Kestrel pending departure clearance"),
        )
        self.assertLess(
            setup_body.index("[KHOVAN ACT1 HOLD 002] Artemis mechanical hold fallback active at Kestrel pending departure clearance"),
            setup_body.index("task_schedule(khovan_act1_hold_artemis_at_kestrel_until_clearance)"),
        )

        hold_body = label_body(act1, "khovan_act1_hold_artemis_at_kestrel_until_clearance")
        for phrase in [
            "if kestrel_departure_clearance_granted:",
            "await task_schedule(khovan_act1_release_kestrel_departure_hold)",
            "artemis_object.pos = Vec3(0, 0, 500)",
            'artemis_object.data_set.set("dock_base_id", 0, 0)',
            'artemis_object.data_set.set("dock_state", "undocked", 0)',
            'artemis_object.data_set.set("playerThrottle", 0, 0)',
            'kestrel_departure_hold_status = "active"',
            'kestrel_departure_hold_release_status = "waiting_for_clearance"',
            "[KHOVAN ACT1 HOLD 002] Artemis mechanical hold fallback active at Kestrel pending departure clearance",
            "await delay_sim(seconds=1)",
            "jump khovan_act1_hold_artemis_at_kestrel_until_clearance",
        ]:
            self.assertIn(phrase, hold_body)
        self.assertNotIn('artemis_object.data_set.set("dock_base_id", kestrel_yards_id, 0)', hold_body)
        self.assertNotIn('artemis_object.data_set.set("dock_state", "docked", 0)', hold_body)

        release_body = label_body(act1, "khovan_act1_release_kestrel_departure_hold")
        for phrase in [
            'artemis_object.data_set.set("dock_base_id", 0, 0)',
            'artemis_object.data_set.set("dock_state", "undocked", 0)',
            'artemis_object.data_set.set("playerThrottle", 0, 0)',
            "[KHOVAN ACT1 HOLD 003] Kestrel departure hold released after clearance",
            'kestrel_departure_hold_status = "released_after_clearance"',
            'kestrel_departure_hold_release_status = "released"',
        ]:
            self.assertIn(phrase, release_body)

        clearance_body = label_body(act1, "khovan_kestrel_request_departure_clearance")
        self.assertIn("kestrel_departure_clearance_granted = True", clearance_body)
        self.assertIn("await task_schedule(khovan_act1_release_kestrel_departure_hold)", clearance_body)
        self.assertLess(
            clearance_body.index("kestrel_departure_clearance_granted = True"),
            clearance_body.index("await task_schedule(khovan_act1_release_kestrel_departure_hold)"),
        )

    def test_kestrel_yard_lock_visual_fallback_is_overlay_only_and_guarded(self) -> None:
        act1 = read(ACT1_PATH)
        self.assertIn(
            'shared kestrel_yard_lock_visual_text = "Artemis - Comms: You are in yard-lock until you request departure clearance. Call when the captain is ready."',
            act1,
        )
        self.assertIn('shared kestrel_yard_lock_visual_mode = "mechanical_yard_lock_overlay_fallback"', act1)

        init_body = label_body(act1, "khovan_act1_initialize_generator_tarsis_gate")
        self.assertIn('kestrel_yard_lock_visual_status = "pending_contact_setup"', init_body)

        setup_body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        for phrase in [
            'kestrel_yard_lock_visual_status = "attempted_mechanical_fallback"',
            "[KHOVAN ACT1 VISUAL 001] Kestrel yard-lock visual setup attempted",
            "await task_schedule(khovan_act1_show_kestrel_yard_lock_visual_fallback)",
        ]:
            self.assertIn(phrase, setup_body)
        self.assertLess(
            setup_body.index("[KHOVAN ACT1 VISUAL 001] Kestrel yard-lock visual setup attempted"),
            setup_body.index("[KHOVAN ACT1 HOLD 002] Artemis mechanical hold fallback active at Kestrel pending departure clearance"),
        )
        self.assertLess(
            setup_body.index("[KHOVAN ACT1 HOLD 002] Artemis mechanical hold fallback active at Kestrel pending departure clearance"),
            setup_body.index("await task_schedule(khovan_act1_show_kestrel_yard_lock_visual_fallback)"),
        )

        visual_body = label_body(act1, "khovan_act1_show_kestrel_yard_lock_visual_fallback")
        for phrase in [
            "if kestrel_yard_lock_message_sent:",
            "[KHOVAN ACT1 MSG ORDER] duplicate suppressed Kestrel yard-lock startup message",
            "kestrel_yard_lock_message_sent = True",
            'kestrel_yard_lock_visual_status = "fallback_active_mechanical_yard_lock_overlay"',
            "[KHOVAN ACT1 VISUAL 002] Kestrel mechanical yard-lock visual fallback active",
            "await task_schedule(khovan_reach_send_safe_startup_message",
            '"startup_sender": "Kestrel Yard Control"',
            '"startup_text": kestrel_yard_lock_visual_text',
            '"startup_sender_id": kestrel_yards_id',
            "[KHOVAN ACT1 MSG KESTREL 001] Kestrel yard-lock message sent",
        ]:
            self.assertIn(phrase, visual_body)
        self.assertNotIn("comms_receive(", visual_body)

        yard_lock_text = "\n".join(
            [
                setup_body,
                label_body(act1, "khovan_act1_hold_artemis_at_kestrel_until_clearance"),
                label_body(act1, "khovan_act1_release_kestrel_departure_hold"),
                visual_body,
            ]
        )
        for unsafe in [
            "docking_set_docking_logic(player_id, kestrel_yards_id, docking_dock_with_friendly_station)",
            'artemis_object.data_set.set("dock_base_id", kestrel_yards_id, 0)',
            'artemis_object.data_set.set("dock_state", "docked", 0)',
        ]:
            self.assertNotIn(unsafe, yard_lock_text)

    def test_kestrel_routes_gate_departure_and_launch_envelope_confirmation(self) -> None:
        act1 = read(ACT1_PATH)
        for phrase in [
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "kestrel_yards")',
            '[KHOVAN ACT1 COMMS 005] Kestrel standard station selected',
            '//comms if has_roles(COMMS_SELECTED_ID, "kestrel_yards")',
            '+ "Hail Kestrel Yards" khovan_kestrel_hail',
            '+ "Request Departure Clearance" khovan_kestrel_request_departure_clearance',
            '+ "Request Emergency Homing Reserve" khovan_kestrel_request_emergency_homing_reserve',
            '+ "Confirm Launch-Envelope Exit" khovan_kestrel_report_launch_envelope_clear',
            "[KHOVAN ACT1 COMMS 006] Kestrel Hail option selected",
            "[KHOVAN ACT1 COMMS 006A] Kestrel departure-clearance option selected",
            "[KHOVAN ACT1 COMMS 006B] Kestrel launch-envelope option selected",
            "=== khovan_kestrel_request_departure_clearance ===",
            "=== khovan_kestrel_request_emergency_homing_reserve ===",
            "=== khovan_kestrel_report_launch_envelope_clear ===",
        ]:
            self.assertIn(phrase, act1)
        self.assertNotIn("sbs.send_comms_selection_info", act1)
        self.assertNotIn("//comms/khovan/kestrel", act1)
        self.assertNotIn(
            '//comms if side_are_allies(COMMS_ORIGIN_ID, COMMS_SELECTED_ID) and has_roles(COMMS_SELECTED_ID, "Station,kestrel_yards") and not has_role(COMMS_ORIGIN_ID, "gamemaster")',
            act1,
        )
        self.assertNotIn("Kestrel before sentinel option command", act1)
        self.assertNotIn("Kestrel after sentinel option command", act1)

        clearance_body = label_body(act1, "khovan_kestrel_request_departure_clearance")
        self.assertIn("[KHOVAN ACT1 COMMS 006A] Kestrel departure-clearance option selected", clearance_body)
        self.assertIn("if kestrel_departure_clearance_response_sent:", clearance_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Kestrel departure clearance response", clearance_body)
        self.assertIn("kestrel_departure_clearance_granted = True", clearance_body)
        self.assertIn("[KHOVAN ACT1 004] Kestrel departure clearance granted", clearance_body)
        self.assertNotIn("khovan_kestrel_release_yard_transfer_energy", clearance_body)
        self.assertIn('"detail": "departure clearance granted; waiting for launch envelope confirmation; energy remains at source-authorized start value until Tarsis handoff"', clearance_body)
        self.assertIn("kestrel_departure_clearance_response_sent = True", clearance_body)
        self.assertIn("kestrel_homing_reserve_prompt_run_id = kestrel_homing_reserve_prompt_run_id + 1", clearance_body)
        self.assertIn("task_schedule(khovan_act1_deliver_homing_reserve_prompt_after_departure_clearance", clearance_body)
        self.assertIn("Kestrel Yard Control: departure clearance granted. Be advised, Artemis is leaving under a temporary generator governor.", clearance_body)
        self.assertIn("[KHOVAN ACT1 COMMS 006D] Kestrel departure-clearance option response sent", clearance_body)
        self.assertNotIn('set_data_set_value(artemis_id, "energy"', clearance_body)

        reserve_body = label_body(act1, "khovan_kestrel_request_emergency_homing_reserve")
        for phrase in [
            "[KHOVAN ACT1 RESERVE 001] emergency homing reserve requested",
            'if homing_reserve_status == "loaded_by_kestrel_comms":',
            "[KHOVAN ACT1 MSG ORDER] duplicate suppressed Kestrel emergency homing reserve request",
            "[KHOVAN ACT1 RESERVE 004] emergency homing reserve already loaded; homing remains 2",
            'if kestrel_yards_id == 0:',
            'homing_reserve_request_status = "failed_missing_kestrel_id"',
            "homing_reserve_kestrel_range = sbs.distance_id(artemis_id, kestrel_yards_id)",
            "[KHOVAN ACT1 RESERVE RANGE] Artemis range to Kestrel for reserve request=",
            "if homing_reserve_kestrel_range > kestrel_homing_reserve_max_range_m:",
            'homing_reserve_request_status = "blocked_outside_kestrel_reserve_range"',
            "[KHOVAN ACT1 RESERVE BLOCKED] emergency homing reserve not loaded: Artemis",
            "emergency homing reserve requires Artemis within",
            'homing_reserve_request_status = "loaded_by_kestrel_comms"',
            'homing_reserve_status = "loaded_by_kestrel_comms"',
            'set_data_set_value(artemis_id, "Homing_NUM", homing_reserve_count, 0)',
            "[KHOVAN ACT1 RESERVE 002] emergency homing reserve load requested",
            "[KHOVAN ACT1 RESERVE 003] emergency homing reserve applied homing=2",
            "await task_schedule(khovan_act1_remove_kestrel_stock_station_role_after_reserve_and_launch)",
            "comms_receive(kestrel_homing_reserve_request_text, title=\"Kestrel Yard Control\", title_color=\"green\")",
            '"detail": "emergency homing reserve loaded; Homing_NUM set to 2 once"',
        ]:
            self.assertIn(phrase, reserve_body)
        self.assertNotIn('set_data_set_value(artemis_id, "energy"', reserve_body)

        launch_body = label_body(act1, "khovan_kestrel_report_launch_envelope_clear")
        self.assertIn("[KHOVAN ACT1 COMMS 006B] Kestrel launch-envelope option selected", launch_body)
        self.assertIn("if not kestrel_departure_clearance_granted:", launch_body)
        self.assertIn("yield fail", launch_body)
        self.assertIn("[KHOVAN ACT1 COMMS 006E] Kestrel launch-envelope option rejected before clearance", launch_body)
        self.assertIn("if kestrel_launch_envelope_response_sent:", launch_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Kestrel launch-envelope response", launch_body)
        self.assertIn("if artemis_id == 0 or kestrel_yards_id == 0:", launch_body)
        self.assertIn('kestrel_departure_gate_status = "launch_envelope_blocked_missing_range_ids"', launch_body)
        self.assertIn("[KHOVAN ACT1 LAUNCH BLOCKED] launch envelope not cleared: missing Artemis or Kestrel id", launch_body)
        self.assertIn("launch_envelope_kestrel_range = sbs.distance_id(artemis_id, kestrel_yards_id)", launch_body)
        self.assertIn("[KHOVAN ACT1 LAUNCH RANGE] Artemis range to Kestrel for launch-envelope report=", launch_body)
        self.assertIn("if launch_envelope_kestrel_range < kestrel_launch_envelope_min_range_m:", launch_body)
        self.assertIn('kestrel_departure_gate_status = "launch_envelope_blocked_inside_1km"', launch_body)
        self.assertIn("[KHOVAN ACT1 LAUNCH BLOCKED] launch envelope not cleared: Artemis", launch_body)
        self.assertIn("Artemis must be at least", launch_body)
        self.assertIn("launch_envelope_cleared = True", launch_body)
        self.assertIn('kestrel_generator_advisory_status = "removed_by_operator_no_packet_sent"', launch_body)
        self.assertIn("[KHOVAN ACT1 005] launch envelope clear confirmed; Kestrel advisory packet removed by operator", launch_body)
        self.assertIn("kestrel_launch_envelope_response_sent = True", launch_body)
        self.assertIn("[KHOVAN ACT1 COMMS 006E] Kestrel launch-envelope option response sent", launch_body)
        self.assertIn("await task_schedule(khovan_act1_send_training_speed_power_reminder)", launch_body)
        self.assertIn("await task_schedule(khovan_act1_remove_kestrel_stock_station_role_after_reserve_and_launch)", launch_body)
        self.assertNotIn("khovan_act1_deliver_kestrel_generator_advisory_after_delay", act1)
        self.assertNotIn("kestrel_generator_advisory_text", act1)

        stock_role_body = label_body(act1, "khovan_act1_remove_kestrel_stock_station_role_after_reserve_and_launch")
        for phrase in [
            "if not launch_envelope_cleared:",
            'artemis_object = to_object(artemis_id)',
            'kestrel_homing_inventory = artemis_object.data_set.get("Homing_NUM", 0)',
            "if kestrel_homing_inventory < homing_reserve_count:",
            "kestrel_stock_station_range = sbs.distance_id(artemis_id, kestrel_yards_id)",
            "if kestrel_stock_station_range <= kestrel_stock_station_disable_range_m:",
            "task_schedule(khovan_act1_watch_kestrel_stock_station_disable",
            'kestrel_yards_object.set_behavior("behav_playership")',
            'kestrel_stock_station_role_status = "stock_production_still_active_behavior_swap_unproven"',
            "stock production remains active after departure",
        ]:
            self.assertIn(phrase, stock_role_body)
        self.assertNotIn("remove_role(kestrel_yards_id", stock_role_body)

        stock_watch_body = label_body(act1, "khovan_act1_watch_kestrel_stock_station_disable")
        self.assertIn("await delay_sim(seconds=1)", stock_watch_body)
        self.assertIn("if stock_disable_run_id != kestrel_stock_station_disable_run_id:", stock_watch_body)
        self.assertIn("await task_schedule(khovan_act1_remove_kestrel_stock_station_role_after_reserve_and_launch)", stock_watch_body)

    def test_homing_reserve_prompt_waits_ten_seconds_after_departure_and_skips_loaded_reserve(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_deliver_homing_reserve_prompt_after_departure_clearance")
        for phrase in [
            "await delay_sim(seconds=10)",
            "if prompt_run_id != kestrel_homing_reserve_prompt_run_id:",
            "if not kestrel_departure_clearance_granted:",
            'if homing_reserve_status == "loaded_by_kestrel_comms" or kestrel_homing_reserve_prompt_sent:',
            'kestrel_homing_reserve_prompt_status = "not_sent_reserve_already_requested"',
            "kestrel_homing_reserve_prompt_sent = True",
            '"startup_text": kestrel_homing_reserve_prompt_text',
            "[KHOVAN ACT1 RESERVE PROMPT] 10-second departure-clearance reminder sent",
        ]:
            self.assertIn(phrase, body)

        training_body = label_body(act1, "khovan_act1_send_training_speed_power_reminder")
        for phrase in [
            "if training_speed_power_reminder_sent:",
            "[KHOVAN ACT1 MSG ORDER] duplicate suppressed Dillon speed-power reminder",
            "if not launch_envelope_cleared:",
            "training_speed_power_reminder_sent = True",
            "[KHOVAN ACT1 MSG ORDER] Dillon speed-power reminder sent after launch-envelope clearance",
            "await task_schedule(khovan_lifeform_send",
            '"send_sender": "Dillon"',
            '"send_text": training_speed_power_reminder_text',
            '"send_fallback_sender_id": kestrel_yards_id',
            "[KHOVAN ACT1 MSG TRAINING 001] Dillon speed-power reminder sent",
        ]:
            self.assertIn(phrase, training_body)
        self.assertNotIn("comms_receive(", training_body)

        self.assertNotIn("khovan_kestrel_resend_generator_advisory", act1)

        for forbidden in [
            "Training Control has three profiles",
            "FULL_SHAKEDOWN",
            "COMPRESSED_SHAKEDOWN",
            "DIRECT_SCENARIO",
        ]:
            self.assertNotIn(forbidden, act1)

    def test_tarsis_routes_require_generator_support_before_docking_clearance(self) -> None:
        act1 = read(ACT1_PATH)
        for phrase in [
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")',
            '[KHOVAN ACT1 COMMS 007] Tarsis standard station selected',
            '[KHOVAN ACT1 COMMS 007A] Tarsis Comms route available after Science known state',
            '//comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")',
            'tarsis_comms_options_status = "rendered_after_known_state"',
            '[KHOVAN ACT1 COMMS TARSIS OPTIONS] Tarsis options rendered',
            '+ "Hail Tarsis Station" khovan_tarsis_hail',
            '+ "Submit Authorization Packet" khovan_tarsis_request_generator_support if not tarsis_required_requests_complete',
            '+ "Request Docking Clearance" khovan_tarsis_request_docking_clearance if not tarsis_docking_clearance_requested',
            '+ "Report Tarsis Gate Status" khovan_tarsis_report_gate_status',
            "[KHOVAN ACT1 COMMS 008] Tarsis Hail option selected",
            "[KHOVAN ACT1 COMMS TARSIS HAIL] Tarsis hail selected",
            "[KHOVAN ACT1 COMMS 008B] Tarsis generator-acceptance option selected",
            "[KHOVAN ACT1 COMMS 008C] Tarsis docking-clearance option selected",
            "[KHOVAN ACT1 COMMS 008E] Tarsis status-report option selected",
            "[KHOVAN ACT1 COMMS TARSIS STATUS] Tarsis gate status requested",
        ]:
            self.assertIn(phrase, act1)
        self.assertNotIn("//comms/khovan/tarsis", act1)
        self.assertNotIn("Khovan Test Option", act1)
        self.assertNotIn("khovan_act1_comms_test_option", act1)
        self.assertNotIn("Tarsis before sentinel option command", act1)
        self.assertNotIn("Tarsis after sentinel option command", act1)
        tarsis_menu = re.search(
            r'^//comms if has_roles\(COMMS_SELECTED_ID, "tarsis_station"\)\n(?P<body>.*?)(?=^//|^=== |\Z)',
            act1,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(tarsis_menu)
        self.assertIn('+ "Hail Tarsis Station" khovan_tarsis_hail', tarsis_menu.group("body"))
        self.assertIn('+ "Submit Authorization Packet" khovan_tarsis_request_generator_support if not tarsis_required_requests_complete', tarsis_menu.group("body"))
        self.assertIn('+ "Request Docking Clearance" khovan_tarsis_request_docking_clearance if not tarsis_docking_clearance_requested', tarsis_menu.group("body"))
        self.assertIn('+ "Report Tarsis Gate Status" khovan_tarsis_report_gate_status', tarsis_menu.group("body"))
        self.assertNotIn("Confirm Docking/Resupply", tarsis_menu.group("body"))
        self.assertNotIn("Homing-Torpedo Priority", tarsis_menu.group("body"))
        self.assertNotIn("khovan_tarsis_request_homing_priority", act1)
        self.assertNotIn("tarsis_homing_priority", act1)
        self.assertNotIn(
            '//comms if side_are_allies(COMMS_ORIGIN_ID, COMMS_SELECTED_ID) and has_roles(COMMS_SELECTED_ID, "Station,tarsis_station") and not has_role(COMMS_ORIGIN_ID, "gamemaster")',
            act1,
        )

        hail_body = label_body(act1, "khovan_tarsis_hail")
        generator_body = label_body(act1, "khovan_tarsis_request_generator_support")
        docking_body = label_body(act1, "khovan_tarsis_request_docking_clearance")
        status_body = label_body(act1, "khovan_tarsis_report_gate_status")
        fallback_body = label_body(act1, "khovan_tarsis_confirm_docking_and_resupply")
        clear_body = label_body(act1, "khovan_tarsis_complete_mechanical_docking_and_resupply")
        self.assertNotIn("sbs.send_story_dialog", act1)
        self.assertIn("[KHOVAN ACT1 COMMS TARSIS HAIL] Tarsis hail selected", hail_body)
        self.assertNotIn("sbs.send_story_dialog", hail_body)
        self.assertIn("comms_receive(tarsis_hail_text, title=\"Tarsis Station\", title_color=\"green\")", hail_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 001] hail response sent", hail_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008B] Tarsis generator-acceptance option selected", generator_body)
        self.assertIn("if tarsis_generator_support_response_sent:", generator_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Tarsis generator-support response", generator_body)
        self.assertIn("tarsis_generator_support_requested = True", generator_body)
        self.assertIn("[KHOVAN ACT1 COMMS TARSIS GENERATOR] generator support requested", generator_body)
        self.assertIn("tarsis_generator_support_response_sent = True", generator_body)
        self.assertNotIn("sbs.send_story_dialog", generator_body)
        self.assertIn("comms_receive(tarsis_generator_support_text, title=\"Tarsis Generator Acceptance\", title_color=\"green\")", generator_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 003] generator support response sent", generator_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008G] Tarsis generator-acceptance option response sent", generator_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008C] Tarsis docking-clearance option selected", docking_body)
        self.assertIn("if tarsis_docking_clearance_response_sent:", docking_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Tarsis docking-clearance response", docking_body)
        self.assertIn("if not tarsis_generator_support_requested:", docking_body)
        self.assertIn("Complete generator support before requesting docking clearance.", docking_body)
        self.assertIn("yield fail", docking_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008I] Tarsis docking-clearance option rejected before prerequisites", docking_body)
        self.assertIn("tarsis_docking_clearance_requested = True", docking_body)
        self.assertIn("[KHOVAN ACT1 COMMS TARSIS CLEARANCE] docking clearance requested/granted", docking_body)
        self.assertIn("tarsis_docking_clearance_response_sent = True", docking_body)
        self.assertIn("await task_schedule(khovan_tarsis_enable_docking_after_clearance)", docking_body)
        self.assertNotIn("sbs.send_story_dialog", docking_body)
        self.assertIn("comms_receive(tarsis_docking_clearance_text, title=\"Tarsis Docking Control\", title_color=\"green\")", docking_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 004] docking clearance response sent", docking_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008I] Tarsis docking-clearance option response sent", docking_body)
        self.assertIn("[KHOVAN ACT1 COMMS TARSIS STATUS] Tarsis gate status requested", status_body)
        self.assertIn("generator_status_text = \"not received\"", status_body)
        self.assertIn("docking_status_text = \"not granted\"", status_body)
        self.assertIn("Tarsis gate status: all required traffic complete. Docking/resupply handoff may proceed.", status_body)
        self.assertIn("Complete both before docking/resupply handoff.", status_body)
        self.assertIn("comms_receive(tarsis_gate_status_text", status_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 006] gate status response sent", status_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008D] hidden fallback docking/resupply confirmation attempted", fallback_body)
        self.assertIn("use normal Helm docking after clearance", fallback_body)
        self.assertIn("yield fail", fallback_body)
        self.assertIn("[KHOVAN ACT1 COMMS TARSIS RESUPPLY] mechanical docking/resupply completion source=", clear_body)
        self.assertIn("energy_restored = True", clear_body)
        self.assertIn('set_data_set_value(ship_id, "energy", tarsis_resupply_energy, 0)', clear_body)
        self.assertIn('set_data_set_value(ship_id, "Homing_NUM", tarsis_resupply_homing_torpedoes, 0)', clear_body)
        self.assertIn('set_data_set_value(ship_id, "Nuke_NUM", tarsis_resupply_nukes, 0)', clear_body)
        self.assertIn('set_data_set_value(ship_id, "EMP_NUM", tarsis_resupply_emps, 0)', clear_body)
        self.assertIn('set_data_set_value(ship_id, "Mine_NUM", tarsis_resupply_mines, 0)', clear_body)
        self.assertIn("[KHOVAN ACT1 012A] Tarsis resupply restored energy=", clear_body)
        self.assertIn("[KHOVAN ACT1 012B] Tarsis resupply restored ordnance homing=", clear_body)
        for phrase in [
            "tarsis_resupply_homing_torpedoes = 10",
            "tarsis_resupply_nukes = 3",
            "tarsis_resupply_emps = 6",
            "tarsis_resupply_mines = 6",
        ]:
            self.assertIn(phrase, act1)
        self.assertIn("await task_schedule(khovan_reach_send_safe_startup_message", clear_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 005] docking/resupply response sent", clear_body)

        update_body = label_body(act1, "khovan_tarsis_update_gate_status")
        self.assertIn(
            "if tarsis_generator_support_requested and tarsis_docking_clearance_requested:",
            update_body,
        )
        self.assertIn("tarsis_required_requests_complete = True", update_body)

    def test_governor_clear_only_happens_in_mechanical_tarsis_resupply(self) -> None:
        act1 = read(ACT1_PATH)
        clear_labels = []
        for match in re.finditer(r"^=== (?P<label>.*?) ===(?P<body>.*?)(?=^=== |\Z)", act1, flags=re.MULTILINE | re.DOTALL):
            if re.search(r"generator_governor_active\s*=\s*False", match.group("body")):
                clear_labels.append(match.group("label"))
        self.assertEqual(
            [
                "khovan_act1_story_jump_seed_post_tarsis_handoff",
                "khovan_tarsis_complete_mechanical_docking_and_resupply",
            ],
            clear_labels,
        )
        clear_body = label_body(act1, "khovan_tarsis_complete_mechanical_docking_and_resupply")
        self.assertIn("if tarsis_governor_clear_response_sent:", clear_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Tarsis governor-clear response", clear_body)
        self.assertIn("if not tarsis_required_requests_complete:", clear_body)
        self.assertIn("tarsis_resupply_confirmed = True", clear_body)
        self.assertIn("generator_governor_active = False", clear_body)
        self.assertIn("generator_governor_cleared = True", clear_body)
        self.assertIn("energy_restored = True", clear_body)
        self.assertIn('set_data_set_value(ship_id, "energy", tarsis_resupply_energy, 0)', clear_body)
        self.assertIn('set_data_set_value(ship_id, "Homing_NUM", tarsis_resupply_homing_torpedoes, 0)', clear_body)
        self.assertIn('set_data_set_value(ship_id, "Nuke_NUM", tarsis_resupply_nukes, 0)', clear_body)
        self.assertIn('set_data_set_value(ship_id, "EMP_NUM", tarsis_resupply_emps, 0)', clear_body)
        self.assertIn('set_data_set_value(ship_id, "Mine_NUM", tarsis_resupply_mines, 0)', clear_body)
        self.assertIn("last_checkpoint = \"tarsis_resupply_governor_cleared\"", clear_body)
        self.assertIn("tarsis_governor_clear_response_sent = True", clear_body)
        self.assertIn("[KHOVAN ACT1 012] Tarsis resupply confirmed; generator governor cleared", clear_body)
        self.assertIn("[KHOVAN ACT1 012A] Tarsis resupply restored energy=", clear_body)
        self.assertIn("[KHOVAN ACT1 012B] Tarsis resupply restored ordnance homing=", clear_body)
        self.assertIn("restored full energy/armament", clear_body)

    def test_slice04_breadcrumbs_and_action_log_hooks_are_present(self) -> None:
        act1 = read(ACT1_PATH)
        for breadcrumb in [
            "[KHOVAN ACT1 001]",
            "[KHOVAN ACT1 002]",
            "[KHOVAN ACT1 003]",
            "[KHOVAN ACT1 003C]",
            "[KHOVAN ACT1 003D]",
            "[KHOVAN ACT1 COMMS 001]",
            "[KHOVAN ACT1 COMMS 002]",
            "[KHOVAN ACT1 COMMS 003]",
            "[KHOVAN ACT1 COMMS 003A]",
            "[KHOVAN ACT1 COMMS 004]",
            "[KHOVAN ACT1 COMMS 004A]",
            "[KHOVAN ACT1 COMMS 004B]",
            "[KHOVAN ACT1 COMMS 004C]",
            "[KHOVAN ACT1 COMMS 004D]",
            "[KHOVAN ACT1 COMMS 005]",
            "[KHOVAN ACT1 COMMS 006]",
            "[KHOVAN ACT1 COMMS 007]",
            "[KHOVAN ACT1 COMMS 007A]",
            "[KHOVAN ACT1 COMMS TARSIS OPTIONS]",
            "[KHOVAN ACT1 COMMS TARSIS HAIL]",
            "[KHOVAN ACT1 COMMS TARSIS GENERATOR]",
            "[KHOVAN ACT1 COMMS TARSIS CLEARANCE]",
            "[KHOVAN ACT1 COMMS TARSIS RESUPPLY]",
            "[KHOVAN ACT1 COMMS TARSIS STATUS]",
            "[KHOVAN ACT1 START STATE]",
            "[KHOVAN ACT1 START STATE FINAL]",
            "[KHOVAN ACT1 RESERVE 001]",
            "[KHOVAN ACT1 RESERVE 002]",
            "[KHOVAN ACT1 RESERVE 003]",
            "[KHOVAN ACT1 RESERVE 004]",
            "[KHOVAN ACT1 DOCK 004R]",
            "[KHOVAN ACT1 DOCK 004D]",
            "[KHOVAN ACT1 MSG KESTREL 001]",
            "[KHOVAN ACT1 MSG KESTREL 002]",
            "[KHOVAN ACT1 MSG KESTREL 003]",
            "[KHOVAN ACT1 MSG TRAINING 001]",
            "[KHOVAN ACT1 MSG TARSIS 001]",
            "[KHOVAN ACT1 MSG TARSIS 003]",
            "[KHOVAN ACT1 MSG TARSIS 004]",
            "[KHOVAN ACT1 MSG TARSIS 005]",
            "[KHOVAN ACT1 MSG TARSIS 006]",
            "[KHOVAN ACT1 MSG ORDER]",
            "[KHOVAN ACT1 SCAN 001]",
            "[KHOVAN ACT1 DOCK 001]",
            "[KHOVAN ACT1 DOCK 001K]",
            "[KHOVAN ACT1 DOCK 002]",
            "[KHOVAN ACT1 DOCK 002A]",
            "[KHOVAN ACT1 DOCK 003]",
            "[KHOVAN ACT1 DOCK 003A]",
            "[KHOVAN ACT1 DOCK 003B]",
            "[KHOVAN ACT1 DOCK 003C]",
            "[KHOVAN ACT1 DOCK 003D]",
            "[KHOVAN ACT1 DOCK BLOCKED]",
            "[KHOVAN ACT1 DOCK 004]",
            "[KHOVAN ACT1 DOCK 004S]",
            "[KHOVAN ACT1 DOCK 004N]",
            "[KHOVAN ACT1 DOCK 004P]",
            "[KHOVAN ACT1 DOCK 004X]",
            "[KHOVAN ACT1 DOCK 004A]",
            "[KHOVAN ACT1 DOCK 004C]",
            "[KHOVAN ACT1 DOCK 004T]",
            "[KHOVAN ACT1 HOLD 001]",
            "[KHOVAN ACT1 HOLD 002]",
            "[KHOVAN ACT1 HOLD 003]",
            "[KHOVAN ACT1 VISUAL 001]",
            "[KHOVAN ACT1 VISUAL 002]",
            "[KHOVAN ACT1 004]",
            "[KHOVAN ACT1 005]",
            "[KHOVAN ACT1 007]",
            "[KHOVAN ACT1 009]",
            "[KHOVAN ACT1 010]",
            "[KHOVAN ACT1 010A]",
            "[KHOVAN ACT1 011]",
            "[KHOVAN ACT1 011A]",
            "[KHOVAN ACT1 011B]",
            "[KHOVAN ACT1 012]",
            "[KHOVAN JUMP ACT1 START]",
            "[KHOVAN JUMP ACT1 POST TARSIS]",
        ]:
            self.assertIn(breadcrumb, act1)

        record_body = label_body(act1, "khovan_act1_record_progression")
        self.assertIn("scenario_control_panel_last_action = f\"act1:{action}\"", record_body)
        self.assertIn("scenario_control_panel_action_log =", record_body)
        self.assertIn("await task_schedule(khovan_scenario_control_panel_update_overview)", record_body)

    def test_slice04_does_not_expose_player_debug_or_future_story_content(self) -> None:
        active_runtime = "\n".join(
            [
                read("script.py"),
                read("story.mast"),
                read("scripts/main.mast"),
                read("scripts/systems/playable_bootstrap.mast"),
                read(OBJECTIVE_PATH),
                read("scripts/systems/scenario_control_panel.mast"),
                read(ACT1_PATH),
            ]
        ).lower()
        active_runtime_for_story_guard = active_runtime.replace("grid_restore_damcons", "")
        for forbidden in [
            "Select a bridge console for Artemis",
            "khovan_reach_slice01_client_main",
            "khovan_reach_slice01_console_selected",
            "assign_client_to_ship(client_id, artemis_id)",
            "gui_console(console_select)",
            "//comms/khovan_scenario_control_panel",
            "@gui",
            "//gui",
            "arbitrary variable",
            "damcon",
            "pirate",
            "comms test station",
            "khovan_comms_proof",
            "[khovan comms proof]",
            "proof option",
            "comms proof station initialized",
        ]:
            self.assertNotIn(forbidden.lower(), active_runtime_for_story_guard)

    def test_slice04_verification_doc_records_static_vs_live_limits(self) -> None:
        path = ROOT / "tests" / "SLICE04_VERIFICATION.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8").lower()
        for phrase in [
            "what changed",
            "implementation finding",
            "what quick/static checks prove",
            "what only live cosmos smoke can prove",
            "expected observation",
            "failure/ambiguous observation",
            "what remains unproven",
            "player instruction clarity",
            "first-time player",
            "who acts next",
            "current objective text and comms message text agree",
            "objective text and comms text disagree",
            "quick tests do not prove live runtime behavior",
            "temporary comms confirmation",
            "live mechanics/api issue",
            "starting-condition audit",
            "user-approved implementation finding/source update",
            "visible-zero-energy start",
            "ship energy = 0",
            "energy = 1000",
            "[khovan act1 012a]",
            "homing_num = 0",
            "nuke_num = 0",
            "emp_num = 0",
            "mine_num = 0",
            "emergency reserve behavior",
            "request emergency homing reserve",
            "sets `homing_num` to `2` once",
            "options panel stayed empty",
            "10/10 after the reserve request",
            "standard station fallback",
            "reference-backed standard station primitives",
            "uppercase `station` role only during",
            "without requiring science scan as a hard gate",
            "science scanning may still provide observational context",
            "custom khovan station/profile/comms binding is deferred",
            "custom station presentation",
            "init.mast",
            "tests/live_startup_trace.txt",
            "station_comms_docking_kernel spike",
            "implementation evidence only",
            "no kernel proof stations",
            "mechanical resupply detection",
            "tarsis docking-clearance gate bug",
            "clearance-denied handler",
            "docking clearance not granted",
            "incompatible docking systems",
            "same custom",
            "does not claim hidden/blocked docking ui until live smoke proves it",
            "try to dock before docking clearance",
            "confirm docking is blocked, unavailable, or does not advance slice 04 state",
            "tarsis comms options render bug",
            "station-role restoration",
            "stock-role suppression",
            "option buttons",
            "tarsis comms option rendering checklist",
            "confirm tarsis options are visible",
            "act i message-ordering and player instruction clarity bug",
            "intended sequence",
            "crew of artemis, this is a qualification cruise",
            # Historical: SLICE04_VERIFICATION.md quotes the copy that was live at
            # the time of that smoke. The live-smoke log is append-only, so this
            # assertion tracks the record, not the current runtime copy (which was
            # revised on slice06-dillon-voice-and-prompt-polish).
            "emergency homing torpedo trasfer complete",
            "temporary generator governor",
            "remember to follow the shakedown mission plan artemis",  # historical, see note above
            "complete tarsis comms traffic before approach",
            "player instruction clarity checklist",
            "duplicate-suppression",
            "act i message ordering checklist",
            "training control speed-power reminder",
            "dillon text stand-in / black-box ui regression",
            "black-box overlay source disabled or replaced",
            "lifeform overlay deferred",
            "live guarded text/comms ui ordering",
            "current live regression evidence",
            "comms proof station cleanup",
            "temporary comms proof/test station",
            "no temporary comms proof/test station appears",
            "proof-station removal",
            "msg tarsis 001",
            "msg tarsis 006",
        ]:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
