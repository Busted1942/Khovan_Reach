from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ScenarioControlPanelStaticTests(unittest.TestCase):
    def test_admin_001_module_exists_and_is_wired_after_state_defaults(self) -> None:
        self.assertTrue((ROOT / "scripts" / "systems" / "scenario_control_panel.mast").is_file())
        main = read("scripts/main.mast")
        self.assertIn("import scripts/systems/scenario_control_panel.mast", main)
        self.assertIn("await task_schedule(khovan_scenario_control_panel_initialize)", main)

        state_index = main.index("await task_schedule(khovan_reach_initialize_bootstrap_state)")
        panel_index = main.index("await task_schedule(khovan_scenario_control_panel_initialize)")
        playable_index = main.index("await task_schedule(khovan_reach_initialize_playable_bootstrap)")
        self.assertLess(state_index, panel_index)
        self.assertLess(panel_index, playable_index)

    def test_admin_002_gm_only_guard_uses_reference_comms_role_pattern(self) -> None:
        panel = read("scripts/systems/scenario_control_panel.mast")
        self.assertIn('//comms if has_roles(COMMS_ORIGIN_ID, "gamemaster")', panel)
        self.assertIn(
            '//comms/gamemaster/khovan_scenario_control_panel if has_roles(COMMS_ORIGIN_ID, "gamemaster")',
            panel,
        )
        self.assertIn('scenario_control_panel_gm_only_guard = \'has_roles(COMMS_ORIGIN_ID, "gamemaster")\'', panel)
        self.assertIn('scenario_control_panel_hidden_from_players = True', panel)
        self.assertIn('scenario_control_panel_visible_to_gm = True', panel)

    def test_admin_003_mode_flags_are_separate_and_default_false(self) -> None:
        state = read("scripts/systems/bootstrap_state.mast")
        for phrase in [
            "shared test_mode_enabled = False",
            "shared live_recovery_mode_enabled = False",
            "test_mode_enabled = False",
            "live_recovery_mode_enabled = False",
        ]:
            self.assertIn(phrase, state)

        panel = read("scripts/systems/scenario_control_panel.mast")
        self.assertIn("test_mode_enabled", panel)
        self.assertIn("live_recovery_mode_enabled", panel)
        self.assertNotIn("test_mode_enabled = True", panel)
        self.assertNotIn("live_recovery_mode_enabled = True", panel)

    def test_admin_004_overview_contains_required_mission_state(self) -> None:
        panel = read("scripts/systems/scenario_control_panel.mast")
        self.assertIn("=== khovan_scenario_control_panel_update_overview ===", panel)
        for phrase in [
            "MISSION OVERVIEW.",
            "mission_phase. {mission_phase}",
            "current_scene. {current_scene}",
            "current_beat. {current_beat}",
            "last_checkpoint. {last_checkpoint}",
            "transition_held. {transition_held}",
            "test_mode_enabled. {test_mode_enabled}",
            "live_recovery_mode_enabled. {live_recovery_mode_enabled}",
            "last GM action. {scenario_control_panel_last_action}",
            "action log. {scenario_control_panel_action_log}",
        ]:
            self.assertIn(phrase, panel)

    def test_admin_005_hold_release_update_state_and_action_log(self) -> None:
        panel = read("scripts/systems/scenario_control_panel.mast")

        hold_match = re.search(
            r"=== khovan_scenario_control_panel_hold_transition ===(?P<body>.*?)^=== ",
            panel,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(hold_match)
        hold_body = hold_match.group("body")
        self.assertIn("transition_held = True", hold_body)
        self.assertIn('scenario_control_panel_last_action = "hold_transition"', hold_body)
        self.assertIn("scenario_control_panel_action_log", hold_body)
        self.assertIn("await task_schedule(khovan_scenario_control_panel_update_overview)", hold_body)

        release_match = re.search(
            r"=== khovan_scenario_control_panel_release_transition ===(?P<body>.*)$",
            panel,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(release_match)
        release_body = release_match.group("body")
        self.assertIn("transition_held = False", release_body)
        self.assertIn('scenario_control_panel_last_action = "release_transition"', release_body)
        self.assertIn("scenario_control_panel_action_log", release_body)
        self.assertIn("await task_schedule(khovan_scenario_control_panel_update_overview)", release_body)

    def test_admin_006_player_facing_selector_and_admin_exposure_are_absent(self) -> None:
        active_runtime = "\n".join(
            [
                read("script.py"),
                read("story.mast"),
                read("scripts/main.mast"),
                read("scripts/systems/playable_bootstrap.mast"),
                read("scripts/systems/scenario_control_panel.mast"),
            ]
        )
        for forbidden in [
            "Select a bridge console for Artemis",
            "khovan_reach_slice01_client_main",
            "khovan_reach_slice01_console_selected",
            "assign_client_to_ship(client_id, artemis_id)",
            "gui_console(console_select)",
            "route_change_console",
            "@console/khovan",
            'main_client = "khovan_reach_slice01_client_entry"',
        ]:
            self.assertNotIn(forbidden, active_runtime)

        panel = read("scripts/systems/scenario_control_panel.mast")
        self.assertNotIn("//comms/khovan_scenario_control_panel", panel)
        self.assertNotIn("@gui", panel)
        self.assertNotIn("//gui", panel)
        self.assertNotIn("gui_", panel)

    def test_slice02_foundation_does_not_include_future_admin_features(self) -> None:
        panel = read("scripts/systems/scenario_control_panel.mast").lower()
        for forbidden in [
            "story jump",
            "jump preset",
            "checkpoint reload",
            "arbitrary variable",
            "current objective",
            "damcon",
            "pirate",
            "debrief",
        ]:
            self.assertNotIn(forbidden, panel)


if __name__ == "__main__":
    unittest.main()
