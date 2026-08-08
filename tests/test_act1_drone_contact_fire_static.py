from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRONE_PATH = "scripts/acts/act1_drone_contact_fire.mast"


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


class Act1DroneContactFireStaticTests(unittest.TestCase):
    def test_slice06_spike_module_exists_imports_and_initializes(self) -> None:
        self.assertTrue((ROOT / DRONE_PATH).is_file())
        main = read("scripts/main.mast")
        self.assertIn(f"import {DRONE_PATH}", main)
        self.assertIn("await task_schedule(khovan_act1_initialize_drone_contact_fire)", main)

        jump_index = main.index("await task_schedule(khovan_story_jump_initialize_registry)")
        drone_index = main.index("await task_schedule(khovan_act1_initialize_drone_contact_fire)")
        playable_index = main.index("await task_schedule(khovan_reach_initialize_playable_bootstrap)")
        self.assertLess(jump_index, drone_index)
        self.assertLess(drone_index, playable_index)

    def test_phase_a_spike_state_variables_exist_without_full_drone_flow(self) -> None:
        drone = read(DRONE_PATH)
        for phrase in [
            "shared drone_contact_fire_initialized = False",
            'shared drone_contact_sequence_status = "not_initialized"',
            'shared drone_contact_detection_mode = "phase_a_spike_only_live_cosmos_proof_required"',
            "shared drone_target_spike_available = False",
            "shared drone_target_spike_active = False",
            "shared drone_target_spike_target_id = 0",
            "shared drone_target_spike_scan_observed = False",
            "shared drone_target_spike_hail_observed = False",
            "shared drone_target_spike_weapons_selected = False",
            "shared drone_target_spike_damage_observed = False",
            "shared drone_target_spike_manual_subsystem_hit_observed = False",
            "shared drone_target_spike_destroyed_observed = False",
            'shared drone_target_spike_result = "unproven"',
            "Drone 01 proves Weapons subsystem disable; Drone 02 completes on destruction",
            "=== khovan_act1_drone_contact_fire_prepare_after_engineering ===",
            'drone_contact_sequence_status = "phase_a_spike_ready_after_engineering"',
            '"objective_id": "slice06_target_spike_ready"',
            "GM Test Mode: run Slice 06 Target Spike.",
        ]:
            self.assertIn(phrase, drone)

        for forbidden in [
            "drill_2_",
            "drill_3_",
            "drone_01_spawned = True",
            "drone_02_spawned = True",
            "drone_01_controlled_disable_complete",
            "drone_02_complete",
            "Anderson",
            "Halcyon",
            "pirate",
            "cache_run",
        ]:
            self.assertNotIn(forbidden, drone)

    def test_gm_only_test_mode_spike_controls_exist(self) -> None:
        drone = read(DRONE_PATH)
        panel = read("scripts/systems/scenario_control_panel.mast")
        self.assertIn(
            '//comms/gamemaster/khovan_drone_contact_fire_spike if has_roles(COMMS_ORIGIN_ID, "gamemaster") and test_mode_enabled',
            drone,
        )
        for phrase in [
            '+ "Spawn Target Spike" khovan_drone_contact_fire_spawn_target_spike if not drone_target_spike_active',
            '+ "Select Target Spike" khovan_drone_contact_fire_select_target_spike if drone_target_spike_active',
            '+ "Read Target Spike Status" khovan_drone_contact_fire_report_target_spike',
            '+ "Cleanup Target Spike" khovan_drone_contact_fire_cleanup_target_spike if drone_target_spike_active or drone_target_spike_destroyed_observed',
            '+ "Slice 06 Target Spike" //comms/gamemaster/khovan_drone_contact_fire_spike if test_mode_enabled',
        ]:
            self.assertIn(phrase, drone + panel)

        self.assertNotIn("//comms/khovan_drone_contact_fire_spike", drone)
        self.assertNotIn("@gui", drone)
        self.assertNotIn("//gui", drone)

    def test_spike_spawn_uses_small_neutral_training_target_and_scan_comms_hooks(self) -> None:
        drone = read(DRONE_PATH)
        spawn_body = label_body(drone, "khovan_drone_contact_fire_spawn_target_spike")
        for phrase in [
            'npc_spawn(32000, 0, 12000, "Slice 06 Spike Target"',
            '"khovan_training, neutral, khovan_slice06_spike_target, khovan_drone_spike_target"',
            '"behav_npcship"',
            'sim.add_navproxy(drone_target_spike_target_id, "Slice 06 Spike Target"',
            'link(artemis_id, "extra_scan_source", drone_target_spike_target_id)',
            "set_science_selection(artemis_id, drone_target_spike_target_id)",
            "set_comms_selection(artemis_id, drone_target_spike_target_id)",
            "[KHOVAN ACT1 DRONE SPIKE SPAWN]",
        ]:
            self.assertIn(phrase, spawn_body)

        for phrase in [
            '//enable/science if has_roles(SCIENCE_SELECTED_ID, "khovan_slice06_spike_target")',
            '//science if has_roles(SCIENCE_SELECTED_ID, "khovan_slice06_spike_target")',
            'drone_target_spike_scan_observed = True',
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "khovan_slice06_spike_target")',
            '//comms if has_roles(COMMS_SELECTED_ID, "khovan_slice06_spike_target")',
            '+ "Khovan: Hail Spike Target" khovan_drone_contact_fire_hail_spike_target',
            'drone_target_spike_hail_observed = True',
            "stock enemy taunt, surrender, or hostile menu",
        ]:
            self.assertIn(phrase, drone)

    def test_spike_observers_cover_selection_damage_subsystem_and_destruction(self) -> None:
        drone = read(DRONE_PATH)
        for phrase in [
            '//select/weapons if has_role(WEAPONS_ORIGIN_ID, "__player__")',
            "selected_weapons_target_id = get_weapons_selection(WEAPONS_ORIGIN_ID)",
            "drone_target_spike_weapons_selected = True",
            '//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_slice06_spike_target")',
            'system = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_SYSTEM")',
            'target_id = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_CRITICAL_HIT")',
            'spike_target.data_set.get("system_damage", sbs.SHPSYS.WEAPONS)',
            'spike_target.data_set.get("system_damage", sbs.SHPSYS.ENGINES)',
            "drone_target_spike_manual_subsystem_hit_observed = True",
            '//damage/destroy if has_role(DESTROYED_ID, "khovan_slice06_spike_target")',
            "drone_target_spike_destroyed_observed = True",
            "sbs.delete_object(drone_target_spike_target_id)",
            "[KHOVAN ACT1 DRONE SPIKE DAMAGE]",
            "[KHOVAN ACT1 DRONE SPIKE DESTROY]",
        ]:
            self.assertIn(phrase, drone)

    def test_scenario_control_panel_reports_spike_status(self) -> None:
        panel = read("scripts/systems/scenario_control_panel.mast")
        for phrase in [
            "drone_contact_sequence_status. {drone_contact_sequence_status}",
            "drone_target_spike_status. {drone_target_spike_status}",
            "drone_target_spike_result. {drone_target_spike_result}",
        ]:
            self.assertIn(phrase, panel)

    def test_quick_suite_includes_slice06_static_checks(self) -> None:
        runner = read("run_tests.py")
        self.assertIn('ROOT / "tests" / "test_act1_drone_contact_fire_static.py"', runner)

    def test_slice06_verification_doc_records_phase_a_limits(self) -> None:
        path = ROOT / "tests" / "SLICE06_VERIFICATION.md"
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
            "spike result",
            "tests/static checks",
            "live smoke checklist",
            "expected observations",
            "failure/ambiguous observations",
            "acceptance covered",
            "acceptance not covered",
            "known risks/api uncertainties",
            "next action",
            "phase a",
            "drone 02 completes on destruction",
            "quick/static checks do not prove live cosmos",
        ]:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
