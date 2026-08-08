from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOF_PATH = "scripts/systems/comms_proof_station.mast"
ACTIVE_RUNTIME_PATHS = [
    "script.py",
    "story.mast",
    "scripts/main.mast",
    "scripts/systems/bootstrap_state.mast",
    "scripts/systems/playable_bootstrap.mast",
    "scripts/systems/audio_runtime.mast",
    "scripts/systems/current_objective_panel.mast",
    "scripts/systems/debug_runtime.mast",
    "scripts/systems/scenario_control_panel.mast",
    "scripts/systems/story_jump_presets.mast",
    "scripts/acts/act1_generator_tarsis_gate.mast",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class CommsProofStationStaticTests(unittest.TestCase):
    def test_proof_station_module_is_removed_from_production_source(self) -> None:
        self.assertFalse((ROOT / PROOF_PATH).exists())

    def test_proof_station_is_not_imported_or_scheduled(self) -> None:
        main = read("scripts/main.mast")
        for forbidden in [
            f"import {PROOF_PATH}",
            "await task_schedule(khovan_comms_proof_station_initialize)",
            "[KHOVAN BOOT 004B] Comms proof station initialized",
        ]:
            self.assertNotIn(forbidden, main)

        self.assertIn("await task_schedule(khovan_act1_initialize_generator_tarsis_gate)", main)
        self.assertIn("await task_schedule(khovan_reach_initialize_debug_runtime)", main)
        self.assertLess(
            main.index("await task_schedule(khovan_act1_initialize_generator_tarsis_gate)"),
            main.index("await task_schedule(khovan_reach_initialize_debug_runtime)"),
        )

    def test_active_runtime_has_no_comms_proof_station_strings(self) -> None:
        active_runtime = "\n".join(read(path) for path in ACTIVE_RUNTIME_PATHS).lower()
        for forbidden in [
            "comms test station",
            "khovan_comms_proof",
            "[khovan comms proof]",
            "proof option",
            "comms proof station initialized",
            "known tsn diagnostic contact",
        ]:
            self.assertNotIn(forbidden, active_runtime)

    def test_kestrel_and_tarsis_runtime_routes_remain_active(self) -> None:
        act1 = read("scripts/acts/act1_generator_tarsis_gate.mast")
        for phrase in [
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "kestrel_yards")',
            '//comms if has_roles(COMMS_SELECTED_ID, "kestrel_yards")',
            '+ "Khovan: Request Emergency Homing Reserve" khovan_kestrel_request_emergency_homing_reserve',
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")',
            '//comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")',
            '+ "Khovan: Hail Tarsis Station" khovan_tarsis_hail',
            '+ "Khovan: Submit Authorization Packet" khovan_tarsis_request_generator_support if not tarsis_required_requests_complete',
            '+ "Khovan: Request Docking Clearance" khovan_tarsis_request_docking_clearance if not tarsis_docking_clearance_requested',
            "[KHOVAN ACT1 COMMS 004C] Tarsis Slice 04 Comms contact available without hard Science-scan gate",
        ]:
            self.assertIn(phrase, act1)
        self.assertNotIn("Homing-Torpedo Priority", act1)
        self.assertNotIn("khovan_tarsis_request_homing_priority", act1)


if __name__ == "__main__":
    unittest.main()
