from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = "scripts/systems/comms_proof_station.mast"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class CommsProofStationStaticTests(unittest.TestCase):
    def test_proof_station_module_exists_and_is_wired_after_act1_init(self) -> None:
        self.assertTrue((ROOT / PROOF_PATH).is_file())
        main = read("scripts/main.mast")
        self.assertIn(f"import {PROOF_PATH}", main)
        self.assertIn("await task_schedule(khovan_comms_proof_station_initialize)", main)

        act1_index = main.index("await task_schedule(khovan_act1_initialize_generator_tarsis_gate)")
        proof_index = main.index("await task_schedule(khovan_comms_proof_station_initialize)")
        debug_index = main.index("await task_schedule(khovan_reach_initialize_debug_runtime)")
        self.assertLess(act1_index, proof_index)
        self.assertLess(proof_index, debug_index)

    def test_proof_station_uses_old_tarsis_style_identity_setup(self) -> None:
        proof = read(PROOF_PATH)
        for phrase in [
            "await task_schedule(khovan_comms_proof_setup_tsn_side)",
            'npc_spawn(9000, 0, 3500, "Comms Test Station", "tsn, friendly, khovan_comms_proof_station, khovan_drill_resupply", "starbase_command", "behav_station")',
            "set_face(khovan_comms_proof_station_id, random_terran(civilian=True))",
            'sim.add_navproxy(khovan_comms_proof_station_id, "Comms Test Station", "starbase_command", "#4A7")',
            'remove_role(khovan_comms_proof_station_id, "Station")',
            'add_role(khovan_comms_proof_station_id, "station")',
            'add_role(khovan_comms_proof_station_id, "khovan_comms_proof_station")',
            'proof_blob.set("torpedo_types_available", "Homing,Nuke,EMP,Mine")',
            'set_data_set_value(khovan_comms_proof_station_id, "Homing_NUM", 32, 0)',
            "proof_side = proof_object.side",
            'science_set_scan_data(player_id, khovan_comms_proof_station_id, "Known TSN diagnostic contact for Slice 04 Comms option proof.")',
            'link(player_id, "extra_scan_source", khovan_comms_proof_station_id)',
            "[KHOVAN COMMS PROOF] Comms Test Station spawned with old Tarsis settings side=",
            "[KHOVAN COMMS PROOF] proof station marked known to player ships for Comms button test",
        ]:
            self.assertIn(phrase, proof)

        for phrase in [
            "=== khovan_comms_proof_setup_tsn_side ===",
            'tsn_side = to_side_id("tsn")',
            'tsn_side = await prefab_spawn(prefab_side_generic, data={"key":"tsn"})',
            'side_set_display_name(tsn_side, "TSN")',
            'side_set_description(tsn_side, "The Terran Stellar Navy")',
            'side_set_icon_color(tsn_side, "#07F")',
        ]:
            self.assertIn(phrase, proof)

    def test_proof_route_uses_simple_khovan_role_condition(self) -> None:
        proof = read(PROOF_PATH)
        for phrase in [
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "khovan_comms_proof_station")',
            "[KHOVAN COMMS PROOF] proof station selected",
            '//comms if has_roles(COMMS_SELECTED_ID, "khovan_comms_proof_station")',
            '+ "Proof Option" khovan_comms_proof_option_selected',
            "=== khovan_comms_proof_option_selected ===",
            "[KHOVAN COMMS PROOF] proof option selected",
            "comms_receive(\"Proof Option selected.",
        ]:
            self.assertIn(phrase, proof)

    def test_proof_station_is_isolated_from_slice04_gate_logic(self) -> None:
        proof = read(PROOF_PATH).lower()
        for forbidden in [
            "kestrel",
            "tarsis_station",
            "generator_governor_active",
            "tarsis_homing_priority_requested",
            "tarsis_generator_support_requested",
            "tarsis_docking_clearance_requested",
            "docking_set_docking_logic",
            "docking_standard_player_station",
            "khovan_act1",
            "drone",
            "damcon",
            "pirate",
            "debrief",
        ]:
            self.assertNotIn(forbidden, proof)


if __name__ == "__main__":
    unittest.main()
