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
        dillon_index = main.index("await task_schedule(khovan_reach_stub_dillon_clip_1)")
        self.assertLess(playable_index, act1_index)
        self.assertLess(act1_index, dillon_index)

    def test_act1_required_state_defaults_and_api_uncertainty_markers_exist(self) -> None:
        act1 = read(ACT1_PATH)
        for phrase in [
            "shared act1_generator_tarsis_gate_initialized = False",
            'shared act1_launch_detection_mode = "temporary_comms_confirmation"',
            'shared act1_docking_detection_mode = "temporary_comms_confirmation"',
            'shared act1_comms_archive_status = "trace_and_action_log_stub"',
            "shared kestrel_departure_clearance_granted = False",
            'shared kestrel_yard_lock_visual_mode = "mechanical_yard_lock_overlay_fallback"',
            'shared kestrel_yard_lock_visual_status = "not_initialized"',
            "shared homing_reserve_count = 2",
            'shared homing_reserve_runtime_apply_status = "stubbed_due_to_ordnance_api_uncertainty"',
            'shared homing_reserve_live_inventory_status = "not_verified"',
            "shared tarsis_homing_priority_requested = False",
            "shared tarsis_generator_support_requested = False",
            "shared tarsis_docking_clearance_requested = False",
            "shared tarsis_required_requests_complete = False",
            'shared tarsis_station_visibility_status = "scan_gated_until_science_initial_scan"',
            'shared tarsis_docking_resupply_status = "docking_setup_attempted_resupply_unproven"',
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
            "starting_homing_torpedoes = 2",
            "homing_reserve_count = 2",
            'homing_reserve_status = "initialized_as_state_only"',
            'homing_reserve_runtime_apply_status = "stubbed_due_to_ordnance_api_uncertainty"',
            'homing_reserve_live_inventory_status = "live smoke reported 10/10 homing; not claimed correct until ordnance API is proven"',
            "[KHOVAN ACT1 001] generator governor initialized active",
            "[KHOVAN ACT1 002] homing reserve initialized as state/log stub count=2",
            "[KHOVAN ACT1 COMMS 001] Kestrel route registered",
            "[KHOVAN ACT1 COMMS 002] Tarsis route registered",
            "await task_schedule(khovan_act1_setup_kestrel_and_tarsis_contacts)",
        ]:
            self.assertIn(phrase, body)

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
            'add_role(tarsis_station_id, "station")',
            'add_role(kestrel_yards_id, "kestrel_yards")',
            'add_role(tarsis_station_id, "tarsis_station")',
            "[KHOVAN ACT1 COMMS 004A] Tarsis Station spawn attempted",
            "[KHOVAN ACT1 COMMS 004B] Tarsis Station spawned id=",
            "[KHOVAN ACT1 COMMS 003] Kestrel standard station setup complete roles=",
            "[KHOVAN ACT1 COMMS 004] Tarsis standard station setup complete roles=",
            "[KHOVAN ACT1 DOCK 001] docking setup scheduled",
            "[KHOVAN ACT1 DOCK 001K] Kestrel Legendary docking helper skipped for startup mechanical hold fallback",
            "await task_schedule(docking_standard_player_station)",
            'science_set_scan_data(player_id, kestrel_yards_id, "Kestrel Yards is Artemis\' launch yard and active departure-control contact.")',
            "docking_set_docking_logic(player_id, tarsis_station_id, docking_dock_with_friendly_station)",
            "[KHOVAN ACT1 DOCK 002] docking setup applied or failed/stubbed",
            'tarsis_docking_resupply_status = "docking_setup_attempted_resupply_unproven"',
            "[KHOVAN ACT1 DOCK 002A] Tarsis docking setup attempted id=",
            "[KHOVAN ACT1 COMMS 003A] Kestrel marked known to player ships for departure Comms",
            "[KHOVAN ACT1 COMMS 004C] Tarsis scan-gated visibility retained; do not claim before/after scan unless live observed",
            "[KHOVAN ACT1 003C] Kestrel/Tarsis use reference-backed standard station primitives",
            "[KHOVAN ACT1 003D] Khovan station presentation polish deferred until standard Comms/docking path is proven",
        ]:
            self.assertIn(phrase, body)

        for forbidden in [
            '"tsn, friendly, kestrel_yards, khovan_origin"',
            '"tsn, friendly, tarsis_station, khovan_drill_resupply"',
            'remove_role(kestrel_yards_id, "Station")',
            'remove_role(tarsis_station_id, "Station")',
            "khovan_act1_comms_test_option",
            "Khovan Test Option",
            "khovan_reach_keep_tarsis_priority_docking_hidden",
            "docking_dock_not_allowed",
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
        self.assertIn(
            "docking_set_docking_logic(player_id, tarsis_station_id, docking_dock_with_friendly_station)",
            setup_body,
        )
        self.assertLess(
            setup_body.index('remove_role(kestrel_yards_id, "station")'),
            setup_body.index("await task_schedule(docking_standard_player_station)"),
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
            'shared kestrel_yard_lock_visual_text = "Artemis, Kestrel Yard Control. Yard-lock is engaged. Hold position on the launch ramp until Comms requests departure clearance."',
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
            'kestrel_yard_lock_visual_status = "fallback_active_mechanical_yard_lock_overlay"',
            "[KHOVAN ACT1 VISUAL 002] Kestrel mechanical yard-lock visual fallback active",
            'sbs.send_story_dialog(0, "Kestrel Yard Control", kestrel_yard_lock_visual_text',
        ]:
            self.assertIn(phrase, visual_body)

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
            '+ "Khovan: Confirm Launch-Envelope Exit" khovan_kestrel_report_launch_envelope_clear',
            '+ "Khovan: Resend Generator Advisory" khovan_kestrel_resend_generator_advisory',
            "[KHOVAN ACT1 COMMS 006] Kestrel Hail option selected",
            "[KHOVAN ACT1 COMMS 006A] Kestrel departure-clearance option selected",
            "[KHOVAN ACT1 COMMS 006B] Kestrel launch-envelope option selected",
            "[KHOVAN ACT1 COMMS 006C] Kestrel resend-advisory option selected",
            "=== khovan_kestrel_request_departure_clearance ===",
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
        self.assertIn("kestrel_departure_clearance_granted = True", clearance_body)
        self.assertIn("[KHOVAN ACT1 004] Kestrel departure clearance granted", clearance_body)
        self.assertIn("[KHOVAN ACT1 COMMS 006D] Kestrel departure-clearance option response sent", clearance_body)

        launch_body = label_body(act1, "khovan_kestrel_report_launch_envelope_clear")
        self.assertIn("[KHOVAN ACT1 COMMS 006B] Kestrel launch-envelope option selected", launch_body)
        self.assertIn("if not kestrel_departure_clearance_granted:", launch_body)
        self.assertIn("yield fail", launch_body)
        self.assertIn("[KHOVAN ACT1 COMMS 006E] Kestrel launch-envelope option rejected before clearance", launch_body)
        self.assertIn("launch_envelope_cleared = True", launch_body)
        self.assertIn("kestrel_generator_advisory_run_id = kestrel_generator_advisory_run_id + 1", launch_body)
        self.assertIn("[KHOVAN ACT1 005] launch envelope clear confirmed; Kestrel advisory timer started", launch_body)
        self.assertIn("[KHOVAN ACT1 COMMS 006E] Kestrel launch-envelope option response sent", launch_body)
        self.assertIn("task_schedule(khovan_act1_deliver_kestrel_generator_advisory_after_delay", launch_body)

    def test_kestrel_advisory_waits_ten_seconds_and_does_not_add_profile_selection(self) -> None:
        act1 = read(ACT1_PATH)
        body = label_body(act1, "khovan_act1_deliver_kestrel_generator_advisory_after_delay")
        for phrase in [
            "await delay_sim(seconds=10)",
            "if advisory_run_id != kestrel_generator_advisory_run_id:",
            "if not launch_envelope_cleared:",
            "if kestrel_generator_packet_sent:",
            "kestrel_generator_packet_sent = True",
            "[KHOVAN ACT1 006] Kestrel advisory delivered after 10-second timer",
            "sbs.send_story_dialog(0, \"Kestrel Yard Control\", kestrel_generator_advisory_text",
            "archive represented by trace/action log stub",
        ]:
            self.assertIn(phrase, body)

        for forbidden in [
            "Training Control has three profiles",
            "FULL_SHAKEDOWN",
            "COMPRESSED_SHAKEDOWN",
            "DIRECT_SCENARIO",
            "shakedown profile",
        ]:
            self.assertNotIn(forbidden, act1)

    def test_tarsis_routes_track_three_required_requests_before_clear(self) -> None:
        act1 = read(ACT1_PATH)
        for phrase in [
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")',
            '[KHOVAN ACT1 COMMS 007] Tarsis standard station selected',
            '//comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")',
            '+ "Khovan: Hail Tarsis Station" khovan_tarsis_hail',
            '+ "Khovan: Request Homing-Torpedo Priority" khovan_tarsis_request_homing_priority',
            '+ "Khovan: Request Generator Support" khovan_tarsis_request_generator_support',
            '+ "Khovan: Request Docking Clearance" khovan_tarsis_request_docking_clearance',
            '+ "Khovan: Confirm Docking/Resupply" khovan_tarsis_confirm_docking_and_resupply',
            '+ "Khovan: Report Tarsis Gate Status" khovan_tarsis_report_gate_status',
            "[KHOVAN ACT1 COMMS 008] Tarsis Hail option selected",
            "[KHOVAN ACT1 COMMS 008A] Tarsis homing-priority option selected",
            "[KHOVAN ACT1 COMMS 008B] Tarsis generator-acceptance option selected",
            "[KHOVAN ACT1 COMMS 008C] Tarsis docking-clearance option selected",
            "[KHOVAN ACT1 COMMS 008D] Tarsis docking/resupply confirmation option selected",
            "[KHOVAN ACT1 COMMS 008E] Tarsis status-report option selected",
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
        self.assertIn('+ "Khovan: Request Homing-Torpedo Priority" khovan_tarsis_request_homing_priority', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Request Generator Support" khovan_tarsis_request_generator_support', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Request Docking Clearance" khovan_tarsis_request_docking_clearance', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Confirm Docking/Resupply" khovan_tarsis_confirm_docking_and_resupply', tarsis_menu.group("body"))
        self.assertIn('+ "Khovan: Report Tarsis Gate Status" khovan_tarsis_report_gate_status', tarsis_menu.group("body"))
        self.assertNotIn(
            '//comms if side_are_allies(COMMS_ORIGIN_ID, COMMS_SELECTED_ID) and has_roles(COMMS_SELECTED_ID, "Station,tarsis_station") and not has_role(COMMS_ORIGIN_ID, "gamemaster")',
            act1,
        )

        homing_body = label_body(act1, "khovan_tarsis_request_homing_priority")
        generator_body = label_body(act1, "khovan_tarsis_request_generator_support")
        docking_body = label_body(act1, "khovan_tarsis_request_docking_clearance")
        self.assertIn("[KHOVAN ACT1 COMMS 008A] Tarsis homing-priority option selected", homing_body)
        self.assertIn("tarsis_homing_priority_requested = True", homing_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008F] Tarsis homing-priority option response sent", homing_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008B] Tarsis generator-acceptance option selected", generator_body)
        self.assertIn("tarsis_generator_support_requested = True", generator_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008G] Tarsis generator-acceptance option response sent", generator_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008C] Tarsis docking-clearance option selected", docking_body)
        self.assertIn("if not tarsis_homing_priority_requested or not tarsis_generator_support_requested:", docking_body)
        self.assertIn("yield fail", docking_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008I] Tarsis docking-clearance option rejected before prerequisites", docking_body)
        self.assertIn("tarsis_docking_clearance_requested = True", docking_body)
        self.assertIn("[KHOVAN ACT1 COMMS 008I] Tarsis docking-clearance option response sent", docking_body)

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
        self.assertIn("if not tarsis_required_requests_complete:", clear_body)
        self.assertIn("yield fail", clear_body)
        self.assertIn("tarsis_resupply_confirmed = True", clear_body)
        self.assertIn("generator_governor_active = False", clear_body)
        self.assertIn("generator_governor_cleared = True", clear_body)
        self.assertIn("last_checkpoint = \"tarsis_resupply_governor_cleared\"", clear_body)
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
            "[KHOVAN ACT1 COMMS 005]",
            "[KHOVAN ACT1 COMMS 006]",
            "[KHOVAN ACT1 COMMS 007]",
            "[KHOVAN ACT1 COMMS 008]",
            "[KHOVAN ACT1 DOCK 001]",
            "[KHOVAN ACT1 DOCK 001K]",
            "[KHOVAN ACT1 DOCK 002]",
            "[KHOVAN ACT1 DOCK 002A]",
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
            "debrief",
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
            "ordnance api uncertainty",
            "options panel stayed blank",
            "10/10 homing",
            "standard station fallback",
            "reference-backed standard station primitives",
            "uppercase `station` compatibility role",
            "science initial scan",
            "station comms options are hidden until science initial scan",
            "custom khovan station/profile/comms binding is deferred",
            "custom station presentation",
            "init.mast",
            "tests/live_startup_trace.txt",
            "station_comms_docking_kernel spike",
            "implementation evidence only",
            "no kernel proof stations",
            "mechanical resupply detection",
        ]:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
