from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACT1_PATH = "scripts/acts/act1_generator_tarsis_gate.mast"


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
        main = read("scripts/main.mast")
        self.assertIn(f"import {ACT1_PATH}", main)
        self.assertIn("await task_schedule(khovan_act1_initialize_generator_tarsis_gate)", main)

        playable_index = main.index("await task_schedule(khovan_reach_initialize_playable_bootstrap)")
        act1_index = main.index("await task_schedule(khovan_act1_initialize_generator_tarsis_gate)")
        self.assertLess(playable_index, act1_index)
        self.assertNotIn("await task_schedule(khovan_reach_stub_dillon_clip_1)", main)

        act1 = read(ACT1_PATH)
        setup_body = label_body(act1, "khovan_act1_setup_kestrel_and_tarsis_contacts")
        self.assertIn("await task_schedule(khovan_reach_stub_dillon_clip_1)", setup_body)
        self.assertLess(
            setup_body.index("[KHOVAN ACT1 HOLD 002] Artemis mechanical hold fallback active at Kestrel pending departure clearance"),
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
            "shared kestrel_yard_lock_message_sent = False",
            "shared kestrel_departure_clearance_response_sent = False",
            "shared kestrel_launch_envelope_response_sent = False",
            "shared kestrel_generator_advisory_sent = False",
            "shared training_speed_power_reminder_sent = False",
            "shared shakedown_prompt_sent = False",
            "shared homing_reserve_count = 2",
            'shared homing_reserve_runtime_apply_status = "stubbed_due_to_ordnance_api_uncertainty"',
            'shared homing_reserve_live_inventory_status = "not_verified"',
            'shared homing_reserve_request_status = "not_requested"',
            'shared homing_reserve_conversion_mode = "kestrel_request_loads_two_homing_once_no_energy_conversion"',
            'shared artemis_start_energy_policy = "cosmos_default_energy_with_generator_governor_not_zero_energy"',
            "shared artemis_start_homing_torpedoes = 0",
            "shared artemis_start_nukes = 0",
            "shared artemis_start_emps = 0",
            "shared artemis_start_mines = 0",
            'shared artemis_start_ordnance_runtime_apply_status = "not_applied"',
            'shared kestrel_homing_reserve_request_text = "Kestrel Yard Control: emergency homing reserve released. Artemis now carries two homing torpedoes as generator-governor margin. No nukes, EMPs, or mines are released before Tarsis resupply. Tarsis has been notified to prioritize homing replacement and generator acceptance."',
            'shared training_speed_power_reminder_text = "Training Control: keep speed and power changes deliberate. Treat the generator advisory as active until Tarsis completes the handoff. Comms should coordinate homing priority, generator support, and docking clearance with Tarsis."',
            'shared tarsis_hail_text = "Tarsis Station: Artemis, we read you. Production Control and Generator Acceptance are standing by for the Kestrel handoff."',
            'shared tarsis_docking_clearance_text = "Tarsis Docking Control: docking clearance granted. Approach within tolerance and initiate docking."',
            'shared tarsis_resupply_text = "Tarsis Station confirms resupply and generator handoff. Kestrel governor is cleared."',
            "shared tarsis_homing_priority_requested = False",
            "shared tarsis_generator_support_requested = False",
            "shared tarsis_docking_clearance_requested = False",
            "shared tarsis_homing_priority_response_sent = False",
            "shared tarsis_generator_support_response_sent = False",
            "shared tarsis_docking_clearance_response_sent = False",
            "shared tarsis_governor_clear_response_sent = False",
            "shared tarsis_required_requests_complete = False",
            'shared tarsis_station_visibility_status = "known_for_slice04_comms_no_hard_science_gate"',
            'shared tarsis_docking_resupply_status = "blocked_until_docking_clearance"',
            'shared tarsis_docking_gate_status = "not_initialized"',
            'shared tarsis_docking_rejection_text = "Tarsis Docking Control: docking clearance not granted. Complete required traffic before approach."',
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
            'artemis_start_energy_runtime_apply_status = "not_overridden_zero_energy_not_source_authorized"',
            "artemis_start_homing_torpedoes = 0",
            "artemis_start_nukes = 0",
            "artemis_start_emps = 0",
            "artemis_start_mines = 0",
            'artemis_start_ordnance_runtime_apply_status = "pending_apply"',
            "kestrel_yard_lock_message_sent = False",
            "kestrel_departure_clearance_response_sent = False",
            "kestrel_launch_envelope_response_sent = False",
            "kestrel_generator_advisory_sent = False",
            "training_speed_power_reminder_sent = False",
            "shakedown_prompt_sent = False",
            "tarsis_homing_priority_response_sent = False",
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

    def test_act1_applies_source_authorized_starting_condition_without_zero_energy(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_apply_source_authorized_start_state")
        for phrase in [
            "generator_governor_active = True",
            "starting_homing_torpedoes = 0",
            "homing_reserve_count = 2",
            'artemis_start_energy_runtime_apply_status = "not_overridden_zero_energy_not_source_authorized"',
            'set_data_set_value(artemis_id, "Homing_NUM", artemis_start_homing_torpedoes, 0)',
            'set_data_set_value(artemis_id, "Nuke_NUM", artemis_start_nukes, 0)',
            'set_data_set_value(artemis_id, "EMP_NUM", artemis_start_emps, 0)',
            'set_data_set_value(artemis_id, "Mine_NUM", artemis_start_mines, 0)',
            'artemis_start_condition_status = "generator_governor_zero_homing_until_kestrel_reserve_no_other_ordnance"',
            'artemis_start_ordnance_runtime_apply_status = "requested_homing_0_nuke_0_emp_0_mine_0"',
            "[KHOVAN ACT1 START STATE] Artemis starting energy set to Cosmos default with generator governor active; zero-energy start not source-authorized",
            "[KHOVAN ACT1 START STATE] Artemis starting ordnance set to Homing=0 Nuke=0 EMP=0 Mine=0",
            "[KHOVAN ACT1 START STATE FINAL] homing=",
        ]:
            self.assertIn(phrase, body)
        self.assertNotIn('set_data_set_value(artemis_id, "energy"', body)

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
            'add_role(tarsis_station_id, "station")',
            'remove_role(tarsis_station_id, "Station")',
            'tarsis_comms_options_status = "station_role_restored_after_docking_helper_pass"',
            "[KHOVAN ACT1 COMMS 004D] Tarsis station role restored and stock Station role removed after docking helper pass for Khovan Comms options",
            'science_set_scan_data(player_id, kestrel_yards_id, "Kestrel Yards is Artemis\' launch yard and active departure-control contact.")',
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
            'remove_role(kestrel_yards_id, "Station")',
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
            "if not tarsis_homing_priority_requested or not tarsis_generator_support_requested:",
            clearance_body,
        )
        self.assertIn("await task_schedule(khovan_tarsis_enable_docking_after_clearance)", clearance_body)
        self.assertIn("if not tarsis_docking_clearance_requested:", enable_body)
        self.assertIn("[KHOVAN ACT1 DOCK 003B] Tarsis docking setup enable blocked before clearance", enable_body)
        self.assertIn('add_role(tarsis_station_id, "station")', enable_body)
        self.assertIn(
            "docking_set_docking_logic(player_id, tarsis_station_id, docking_dock_with_friendly_station)",
            enable_body,
        )
        self.assertIn('tarsis_docking_gate_status = "enabled_after_docking_clearance"', enable_body)
        self.assertIn("[KHOVAN ACT1 DOCK 004] Tarsis docking setup enabled after clearance", enable_body)

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
        self.assertIn(
            "[KHOVAN ACT1 DOCK 004A] Tarsis dock signal observed after clearance; resupply still requires Comms confirmation",
            dock_signal.group("body"),
        )

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
            'shared kestrel_yard_lock_visual_text = "Kestrel Yard Control: Artemis is held in yard-lock pending departure clearance. Comms, request clearance when the captain is ready."',
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

        for unsafe in [
            "docking_set_docking_logic(player_id, kestrel_yards_id, docking_dock_with_friendly_station)",
            'artemis_object.data_set.set("dock_base_id", kestrel_yards_id, 0)',
            'artemis_object.data_set.set("dock_state", "docked", 0)',
            'add_role(kestrel_yards_id, "station")',
        ]:
            self.assertNotIn(unsafe, act1)

    def test_kestrel_routes_gate_departure_and_launch_envelope_confirmation(self) -> None:
        act1 = read(ACT1_PATH)
        for phrase in [
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "kestrel_yards")',
            '[KHOVAN ACT1 COMMS 005] Kestrel standard station selected',
            '//comms if has_roles(COMMS_SELECTED_ID, "kestrel_yards")',
            '+ "Khovan: Hail Kestrel Yards" khovan_kestrel_hail',
            '+ "Khovan: Request Departure Clearance" khovan_kestrel_request_departure_clearance',
            '+ "Khovan: Request Emergency Homing Reserve" khovan_kestrel_request_emergency_homing_reserve',
            '+ "Khovan: Confirm Launch-Envelope Exit" khovan_kestrel_report_launch_envelope_clear',
            '+ "Khovan: Resend Generator Advisory" khovan_kestrel_resend_generator_advisory',
            "[KHOVAN ACT1 COMMS 006] Kestrel Hail option selected",
            "[KHOVAN ACT1 COMMS 006A] Kestrel departure-clearance option selected",
            "[KHOVAN ACT1 COMMS 006B] Kestrel launch-envelope option selected",
            "[KHOVAN ACT1 COMMS 006C] Kestrel resend-advisory option selected",
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
        self.assertIn("kestrel_departure_clearance_response_sent = True", clearance_body)
        self.assertIn("[KHOVAN ACT1 COMMS 006D] Kestrel departure-clearance option response sent", clearance_body)

        reserve_body = label_body(act1, "khovan_kestrel_request_emergency_homing_reserve")
        for phrase in [
            "[KHOVAN ACT1 RESERVE 001] emergency homing reserve requested",
            'if homing_reserve_status == "loaded_by_kestrel_comms":',
            "[KHOVAN ACT1 MSG ORDER] duplicate suppressed Kestrel emergency homing reserve request",
            "[KHOVAN ACT1 RESERVE 004] emergency homing reserve already loaded; homing remains 2",
            'homing_reserve_request_status = "loaded_by_kestrel_comms"',
            'homing_reserve_status = "loaded_by_kestrel_comms"',
            'set_data_set_value(artemis_id, "Homing_NUM", homing_reserve_count, 0)',
            "[KHOVAN ACT1 RESERVE 002] emergency homing reserve load requested",
            "[KHOVAN ACT1 RESERVE 003] emergency homing reserve applied homing=2",
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
        self.assertIn("[KHOVAN ACT1 MSG ORDER] advisory timer ignored because already sent after duplicate launch-envelope confirmation", launch_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Kestrel launch-envelope response", launch_body)
        self.assertIn("launch_envelope_cleared = True", launch_body)
        self.assertIn("kestrel_generator_advisory_run_id = kestrel_generator_advisory_run_id + 1", launch_body)
        self.assertIn("[KHOVAN ACT1 005] launch envelope clear confirmed; Kestrel advisory timer started", launch_body)
        self.assertIn("kestrel_launch_envelope_response_sent = True", launch_body)
        self.assertIn("[KHOVAN ACT1 COMMS 006E] Kestrel launch-envelope option response sent", launch_body)
        self.assertIn("task_schedule(khovan_act1_deliver_kestrel_generator_advisory_after_delay", launch_body)

    def test_kestrel_advisory_waits_ten_seconds_sends_training_reminder_and_does_not_add_profile_selection(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_deliver_kestrel_generator_advisory_after_delay")
        for phrase in [
            "await delay_sim(seconds=10)",
            "if advisory_run_id != kestrel_generator_advisory_run_id:",
            "[KHOVAN ACT1 MSG ORDER] duplicate suppressed stale Kestrel advisory timer",
            "if not launch_envelope_cleared:",
            "if kestrel_generator_packet_sent or kestrel_generator_advisory_sent:",
            "[KHOVAN ACT1 MSG ORDER] advisory timer ignored because already sent",
            "kestrel_generator_packet_sent = True",
            "kestrel_generator_advisory_sent = True",
            "[KHOVAN ACT1 006] Kestrel advisory delivered after 10-second timer",
            "await task_schedule(khovan_reach_send_safe_startup_message",
            '"startup_sender": "Kestrel Yard Control"',
            '"startup_text": kestrel_generator_advisory_text',
            '"startup_sender_id": kestrel_yards_id',
            "[KHOVAN ACT1 MSG KESTREL 004] generator advisory packet sent",
            "delivered by guarded text packet; archive represented by Comms response/trace/action log",
            "await task_schedule(khovan_act1_send_training_speed_power_reminder)",
        ]:
            self.assertIn(phrase, body)
        self.assertNotIn("comms_receive(kestrel_generator_advisory_text", body)

        training_body = label_body(act1, "khovan_act1_send_training_speed_power_reminder")
        for phrase in [
            "if training_speed_power_reminder_sent:",
            "[KHOVAN ACT1 MSG ORDER] duplicate suppressed Training Control speed-power reminder",
            "if not kestrel_generator_advisory_sent:",
            "training_speed_power_reminder_sent = True",
            "[KHOVAN ACT1 MSG ORDER] Training Control speed-power reminder sent after advisory",
            "await task_schedule(khovan_reach_send_safe_startup_message",
            '"startup_sender": "Training Control"',
            '"startup_text": training_speed_power_reminder_text',
            '"startup_sender_id": kestrel_yards_id',
            "[KHOVAN ACT1 MSG TRAINING 001] Training speed-power reminder sent",
        ]:
            self.assertIn(phrase, training_body)
        self.assertNotIn("comms_receive(", training_body)

        resend_body = label_body(act1, "khovan_kestrel_resend_generator_advisory")
        self.assertIn("if not kestrel_generator_packet_sent or not kestrel_generator_advisory_sent:", resend_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] Kestrel advisory resend did not restart timer", resend_body)
        self.assertNotIn("kestrel_generator_advisory_run_id = kestrel_generator_advisory_run_id + 1", resend_body)

        for forbidden in [
            "Training Control has three profiles",
            "FULL_SHAKEDOWN",
            "COMPRESSED_SHAKEDOWN",
            "DIRECT_SCENARIO",
        ]:
            self.assertNotIn(forbidden, act1)

    def test_tarsis_routes_track_three_required_requests_before_clear(self) -> None:
        act1 = read(ACT1_PATH)
        for phrase in [
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")',
            '[KHOVAN ACT1 COMMS 007] Tarsis standard station selected',
            '[KHOVAN ACT1 COMMS 007A] Tarsis Comms route available after Science known state',
            '//comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")',
            'tarsis_comms_options_status = "rendered_after_known_state"',
            '[KHOVAN ACT1 COMMS TARSIS OPTIONS] Tarsis options rendered',
            '+ "Khovan: Hail Tarsis Station" khovan_tarsis_hail',
            '+ "Khovan: Request Homing-Torpedo Priority" khovan_tarsis_request_homing_priority if not tarsis_required_requests_complete',
            '+ "Khovan: Request Generator Support" khovan_tarsis_request_generator_support if not tarsis_required_requests_complete',
            '+ "Khovan: Request Docking Clearance" khovan_tarsis_request_docking_clearance if not tarsis_docking_clearance_requested',
            '+ "Khovan: Confirm Docking/Resupply" khovan_tarsis_confirm_docking_and_resupply if tarsis_docking_clearance_requested',
            '+ "Khovan: Report Tarsis Gate Status" khovan_tarsis_report_gate_status',
            "[KHOVAN ACT1 COMMS 008] Tarsis Hail option selected",
            "[KHOVAN ACT1 COMMS TARSIS HAIL] Tarsis hail selected",
            "[KHOVAN ACT1 COMMS 008A] Tarsis homing-priority option selected",
            "[KHOVAN ACT1 COMMS 008B] Tarsis generator-acceptance option selected",
            "[KHOVAN ACT1 COMMS 008C] Tarsis docking-clearance option selected",
            "[KHOVAN ACT1 COMMS 008D] Tarsis docking/resupply confirmation option selected",
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
        self.assertIn('+ "Khovan: Hail Tarsis Station" khovan_tarsis_hail', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Request Homing-Torpedo Priority" khovan_tarsis_request_homing_priority if not tarsis_required_requests_complete', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Request Generator Support" khovan_tarsis_request_generator_support if not tarsis_required_requests_complete', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Request Docking Clearance" khovan_tarsis_request_docking_clearance if not tarsis_docking_clearance_requested', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Confirm Docking/Resupply" khovan_tarsis_confirm_docking_and_resupply if tarsis_docking_clearance_requested', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Report Tarsis Gate Status" khovan_tarsis_report_gate_status', tarsis_menu.group("body"))
        self.assertNotIn(
            '//comms if side_are_allies(COMMS_ORIGIN_ID, COMMS_SELECTED_ID) and has_roles(COMMS_SELECTED_ID, "Station,tarsis_station") and not has_role(COMMS_ORIGIN_ID, "gamemaster")',
            act1,
        )

        hail_body = label_body(act1, "khovan_tarsis_hail")
        homing_body = label_body(act1, "khovan_tarsis_request_homing_priority")
        generator_body = label_body(act1, "khovan_tarsis_request_generator_support")
        docking_body = label_body(act1, "khovan_tarsis_request_docking_clearance")
        status_body = label_body(act1, "khovan_tarsis_report_gate_status")
        clear_body = label_body(act1, "khovan_tarsis_confirm_docking_and_resupply")
        self.assertNotIn("sbs.send_story_dialog", act1)
        self.assertIn("[KHOVAN ACT1 COMMS TARSIS HAIL] Tarsis hail selected", hail_body)
        self.assertNotIn("sbs.send_story_dialog", hail_body)
        self.assertIn("comms_receive(tarsis_hail_text, title=\"Tarsis Station\", title_color=\"green\")", hail_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 001] hail response sent", hail_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008A] Tarsis homing-priority option selected", homing_body)
        self.assertIn("if tarsis_homing_priority_response_sent:", homing_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Tarsis homing-priority response", homing_body)
        self.assertIn("tarsis_homing_priority_requested = True", homing_body)
        self.assertIn("[KHOVAN ACT1 COMMS TARSIS HOMING] homing priority requested", homing_body)
        self.assertIn("tarsis_homing_priority_response_sent = True", homing_body)
        self.assertNotIn("sbs.send_story_dialog", homing_body)
        self.assertIn("comms_receive(tarsis_homing_priority_text, title=\"Tarsis Production Control\", title_color=\"green\")", homing_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 002] homing priority response sent", homing_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008F] Tarsis homing-priority option response sent", homing_body)
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
        self.assertIn("if not tarsis_homing_priority_requested or not tarsis_generator_support_requested:", docking_body)
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
        self.assertIn("homing_status_text = \"not set\"", status_body)
        self.assertIn("generator_status_text = \"not received\"", status_body)
        self.assertIn("docking_status_text = \"not granted\"", status_body)
        self.assertIn("Tarsis gate status: all required traffic complete. Docking/resupply handoff may proceed.", status_body)
        self.assertIn("Complete all three before docking/resupply handoff.", status_body)
        self.assertIn("comms_receive(tarsis_gate_status_text", status_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 006] gate status response sent", status_body)
        self.assertIn("[KHOVAN ACT1 COMMS TARSIS RESUPPLY] docking/resupply confirmed", clear_body)
        self.assertIn("comms_receive(tarsis_resupply_text, title=\"Tarsis Station\", title_color=\"green\")", clear_body)
        self.assertIn("[KHOVAN ACT1 MSG TARSIS 005] docking/resupply response sent", clear_body)

        update_body = label_body(act1, "khovan_tarsis_update_gate_status")
        self.assertIn(
            "if tarsis_homing_priority_requested and tarsis_generator_support_requested and tarsis_docking_clearance_requested:",
            update_body,
        )
        self.assertIn("tarsis_required_requests_complete = True", update_body)

    def test_governor_clear_only_happens_in_tarsis_resupply_confirmation(self) -> None:
        act1 = read(ACT1_PATH)
        clear_hits = [
            match.start()
            for match in re.finditer(r"generator_governor_active\s*=\s*False", act1)
        ]
        self.assertEqual(1, len(clear_hits))
        clear_body = label_body(act1, "khovan_tarsis_confirm_docking_and_resupply")
        self.assertIn("if tarsis_governor_clear_response_sent:", clear_body)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Tarsis governor-clear response", clear_body)
        self.assertIn("if not tarsis_required_requests_complete:", clear_body)
        self.assertIn("yield fail", clear_body)
        self.assertIn("tarsis_resupply_confirmed = True", clear_body)
        self.assertIn("generator_governor_active = False", clear_body)
        self.assertIn("generator_governor_cleared = True", clear_body)
        self.assertIn("last_checkpoint = \"tarsis_resupply_governor_cleared\"", clear_body)
        self.assertIn("tarsis_governor_clear_response_sent = True", clear_body)
        self.assertIn("[KHOVAN ACT1 012] Tarsis resupply confirmed; generator governor cleared", clear_body)

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
            "[KHOVAN ACT1 COMMS 008]",
            "[KHOVAN ACT1 COMMS TARSIS OPTIONS]",
            "[KHOVAN ACT1 COMMS TARSIS HAIL]",
            "[KHOVAN ACT1 COMMS TARSIS HOMING]",
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
            "[KHOVAN ACT1 MSG KESTREL 001]",
            "[KHOVAN ACT1 MSG KESTREL 002]",
            "[KHOVAN ACT1 MSG KESTREL 003]",
            "[KHOVAN ACT1 MSG KESTREL 004]",
            "[KHOVAN ACT1 MSG TRAINING 001]",
            "[KHOVAN ACT1 MSG TARSIS 001]",
            "[KHOVAN ACT1 MSG TARSIS 002]",
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
            "[KHOVAN ACT1 DOCK 004A]",
            "[KHOVAN ACT1 HOLD 001]",
            "[KHOVAN ACT1 HOLD 002]",
            "[KHOVAN ACT1 HOLD 003]",
            "[KHOVAN ACT1 VISUAL 001]",
            "[KHOVAN ACT1 VISUAL 002]",
            "[KHOVAN ACT1 004]",
            "[KHOVAN ACT1 005]",
            "[KHOVAN ACT1 006]",
            "[KHOVAN ACT1 007]",
            "[KHOVAN ACT1 008]",
            "[KHOVAN ACT1 009]",
            "[KHOVAN ACT1 010]",
            "[KHOVAN ACT1 010A]",
            "[KHOVAN ACT1 011]",
            "[KHOVAN ACT1 011A]",
            "[KHOVAN ACT1 011B]",
            "[KHOVAN ACT1 012]",
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
                read("scripts/systems/scenario_control_panel.mast"),
                read(ACT1_PATH),
            ]
        ).lower()
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
            "current objective",
            "drone",
            "damcon",
            "pirate",
        ]:
            self.assertNotIn(forbidden.lower(), active_runtime)

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
            "quick tests do not prove live runtime behavior",
            "temporary comms confirmation",
            "live mechanics/api issue",
            "starting-condition audit",
            "literal zero-energy",
            "generator governor remains active, artemis starts with 0 homing torpedoes",
            "homing_num = 0",
            "nuke_num = 0",
            "emp_num = 0",
            "mine_num = 0",
            "does not call `set_data_set_value(artemis_id, \"energy\", ...)`",
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
            "act i message-ordering bug",
            "intended sequence",
            "duplicate-suppression",
            "act i message ordering checklist",
            "training control speed-power reminder",
            "dillon text stand-in / black-box ui regression",
            "black-box overlay source disabled or replaced",
            "lifeform overlay deferred",
            "live guarded text/comms ui ordering",
            "current live regression evidence",
            "msg tarsis 001",
            "msg tarsis 006",
        ]:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
