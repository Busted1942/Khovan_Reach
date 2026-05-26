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
        self.assertNotRegex(panel, r"(?m)^\s*shared\s+test_mode_enabled\s*=\s*True\s*$")
        self.assertNotRegex(panel, r"(?m)^\s*shared\s+live_recovery_mode_enabled\s*=\s*True\s*$")
        self.assertIn("live_recovery_mode_enabled = False", panel)

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

    def test_admin_005_buttons_wire_to_handlers_that_update_state_and_action_log(self) -> None:
        panel = read("scripts/systems/scenario_control_panel.mast")
        for phrase in [
            '+ "Hold Scene Transition" khovan_scenario_control_panel_hold_transition',
            '+ "Release Scene Transition" khovan_scenario_control_panel_release_transition',
            '+ "Refresh Overview" khovan_scenario_control_panel_refresh_overview',
            '+ "Enable Test Mode" khovan_scenario_control_panel_enable_test_mode if not test_mode_enabled',
            '+ "Disable Test Mode" khovan_scenario_control_panel_disable_test_mode if test_mode_enabled',
            '+ "Test Mode Story Jumps" //comms/gamemaster/khovan_story_jump_presets if test_mode_enabled',
            "=== khovan_scenario_control_panel_hold_transition ===",
            "=== khovan_scenario_control_panel_release_transition ===",
            "=== khovan_scenario_control_panel_refresh_overview ===",
        ]:
            self.assertIn(phrase, panel)

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
        self.assertIn("script.write_khovan_startup_trace", hold_body)
        self.assertIn("comms_receive(scenario_control_panel_overview_text", hold_body)
        self.assertIn('comms_navigate("//comms/gamemaster/khovan_scenario_control_panel")', hold_body)

        release_match = re.search(
            r"=== khovan_scenario_control_panel_release_transition ===(?P<body>.*?)^=== ",
            panel,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(release_match)
        release_body = release_match.group("body")
        self.assertIn("transition_held = False", release_body)
        self.assertIn('scenario_control_panel_last_action = "release_transition"', release_body)
        self.assertIn("scenario_control_panel_action_log", release_body)
        self.assertIn("await task_schedule(khovan_scenario_control_panel_update_overview)", release_body)
        self.assertIn("script.write_khovan_startup_trace", release_body)
        self.assertIn("comms_receive(scenario_control_panel_overview_text", release_body)
        self.assertIn('comms_navigate("//comms/gamemaster/khovan_scenario_control_panel")', release_body)

        refresh_match = re.search(
            r"=== khovan_scenario_control_panel_refresh_overview ===(?P<body>.*)$",
            panel,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(refresh_match)
        refresh_body = refresh_match.group("body")
        self.assertIn('scenario_control_panel_last_action = "refresh_overview"', refresh_body)
        self.assertIn("scenario_control_panel_action_log", refresh_body)
        self.assertIn("script.write_khovan_startup_trace", refresh_body)
        self.assertIn("await task_schedule(khovan_scenario_control_panel_update_overview)", refresh_body)
        self.assertIn("comms_receive(scenario_control_panel_overview_text", refresh_body)
        self.assertIn('comms_navigate("//comms/gamemaster/khovan_scenario_control_panel")', refresh_body)

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
