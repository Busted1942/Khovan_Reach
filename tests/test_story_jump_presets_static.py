from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PRESET_IDS = [
    "mission_start",
    "drill_2_guided_contact",
    "anderson_orders",
    "cascade_decision",
    "pirate_arrival_cover_intact",
    "debrief",
]

REQUIRED_METADATA_FIELDS = [
    "jump_id",
    "display_name",
    "target_scene",
    "mode_access",
    "mission_phase",
    "required_prior_flags",
    "seeded_state_summary",
    "entities",
    "timers",
    "clips",
    "gm_display",
    "expected_next_event",
    "validation_checks",
    "recovery_notes",
    "skipped_observations",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class StoryJumpPresetStaticTests(unittest.TestCase):
    def test_story_jump_module_exists_imports_and_initializes(self) -> None:
        self.assertTrue((ROOT / "scripts" / "systems" / "story_jump_presets.mast").is_file())
        main = read("scripts/main.mast")
        self.assertIn("import scripts/systems/story_jump_presets.mast", main)
        self.assertIn("await task_schedule(khovan_story_jump_initialize_registry)", main)

        scp_index = main.index("await task_schedule(khovan_scenario_control_panel_initialize)")
        jump_index = main.index("await task_schedule(khovan_story_jump_initialize_registry)")
        playable_index = main.index("await task_schedule(khovan_reach_initialize_playable_bootstrap)")
        self.assertLess(scp_index, jump_index)
        self.assertLess(jump_index, playable_index)

    def test_registry_state_and_required_fields_exist(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        for phrase in [
            "shared story_jump_registry_initialized = False",
            "shared story_jump_registry_ids =",
            "shared story_jump_preset_count = 6",
            "shared story_jump_metadata_required_fields =",
            "shared story_jump_generation_id = 0",
            "shared story_jump_mode_access = \"test_mode_only\"",
            "=== khovan_story_jump_initialize_registry ===",
            "story_jump_registry_initialized = True",
        ]:
            self.assertIn(phrase, story_jump)

        for field in REQUIRED_METADATA_FIELDS:
            self.assertIn(field, story_jump)

    def test_all_initial_preset_ids_and_metadata_fields_exist(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        for preset_id in PRESET_IDS:
            self.assertIn(preset_id, story_jump)
            metadata_name = f"story_jump_preset_{preset_id}_metadata"
            match = re.search(
                rf'shared {re.escape(metadata_name)} = "(?P<metadata>[^"]+)"',
                story_jump,
            )
            self.assertIsNotNone(match, preset_id)
            metadata = match.group("metadata")
            for field in REQUIRED_METADATA_FIELDS:
                self.assertIn(f"{field}=", metadata, f"{preset_id}:{field}")

    def test_story_jumps_are_gm_only_and_test_mode_gated(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        panel = read("scripts/systems/scenario_control_panel.mast")

        self.assertIn(
            '//comms/gamemaster/khovan_story_jump_presets if has_roles(COMMS_ORIGIN_ID, "gamemaster") and test_mode_enabled',
            story_jump,
        )
        self.assertIn(
            '+ "Test Mode Story Jumps" //comms/gamemaster/khovan_story_jump_presets if test_mode_enabled',
            panel,
        )
        self.assertIn(
            '+ "Enable Test Mode" khovan_scenario_control_panel_enable_test_mode if not test_mode_enabled',
            panel,
        )
        self.assertIn(
            '+ "Disable Test Mode" khovan_scenario_control_panel_disable_test_mode if test_mode_enabled',
            panel,
        )
        self.assertIn("live_recovery_mode_enabled = False", panel)
        self.assertNotIn("//comms/khovan_story_jump_presets", story_jump)
        self.assertNotIn("@console/khovan_story_jump", story_jump)
        self.assertNotIn("@gui", story_jump)
        self.assertNotIn("//gui", story_jump)

    def test_each_button_routes_to_named_handler_and_common_executor(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        expected_labels = {
            "mission_start": "Mission Start",
            "drill_2_guided_contact": "Drill 2 Guided Contact",
            "anderson_orders": "Anderson Orders",
            "cascade_decision": "Cascade Decision",
            "pirate_arrival_cover_intact": "Pirate Arrival Cover Intact",
            "debrief": "Debrief",
        }

        for preset_id, display in expected_labels.items():
            handler = f"khovan_story_jump_preset_{preset_id}"
            self.assertIn(f'+ "{display}" {handler}', story_jump)
            self.assertIn(f"=== {handler} ===", story_jump)
            self.assertIn(
                f'await task_schedule(khovan_story_jump_execute_preset, {{"jump_id": "{preset_id}"}})',
                story_jump,
            )

        self.assertIn("=== khovan_story_jump_execute_preset ===", story_jump)
        self.assertIn('default jump_id = "mission_start"', story_jump)

    def test_executor_has_generation_id_summary_validation_and_action_log(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        executor_match = re.search(
            r"=== khovan_story_jump_execute_preset ===(?P<body>.*)$",
            story_jump,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(executor_match)
        body = executor_match.group("body")

        for phrase in [
            "story_jump_generation_id = story_jump_generation_id + 1",
            "transition_held = False",
            "story_jump_last_validation_result",
            "story_jump_last_summary = f\"STORY JUMP SUMMARY",
            "expected_next_event. {story_jump_expected_next_event}",
            "warning. {story_jump_framework_warning}",
            "skipped_observations. {story_jump_skipped_observations}",
            "scenario_control_panel_last_action = f\"story_jump:{story_jump_last_id}\"",
            "scenario_control_panel_action_log =",
            "script.write_khovan_startup_trace(f\"[KHOVAN JUMP {story_jump_generation_id}]",
            "await task_schedule(khovan_scenario_control_panel_update_overview)",
        ]:
            self.assertIn(phrase, body)

    def test_framework_presets_do_not_spawn_future_gameplay_systems(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        for forbidden in [
            "npc_spawn(",
            "player_spawn(",
            "sim_create(",
            "assign_client_to_ship",
            "gui_console(",
            "route_change_console",
            "drone_spawn",
            "pirate_state_machine",
            "damcon_timer",
            "checkpoint reload",
        ]:
            self.assertNotIn(forbidden, story_jump)

        for preset_id in [
            "drill_2_guided_contact",
            "anderson_orders",
            "cascade_decision",
            "pirate_arrival_cover_intact",
            "debrief",
        ]:
            self.assertIn(preset_id, story_jump)
            self.assertIn("framework preset only; gameplay systems not implemented yet.", story_jump)

    def test_story_jump_seed_targets_are_intentional_framework_markers(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        expected_targets = {
            "mission_start": ('mission_phase = "act_1"', "current_scene = 1"),
            "drill_2_guided_contact": ('mission_phase = "act_1"', "current_scene = 3"),
            "anderson_orders": ('mission_phase = "act_2"', "current_scene = 5"),
            "cascade_decision": ('mission_phase = "act_3"', "current_scene = 9"),
            "pirate_arrival_cover_intact": ('mission_phase = "act_3"', "current_scene = 12"),
            "debrief": ('mission_phase = "debrief"', "current_scene = 14"),
        }
        for preset_id, phrases in expected_targets.items():
            self.assertIn(f'jump_id == "{preset_id}"', story_jump)
            for phrase in phrases:
                self.assertIn(phrase, story_jump)

    def test_active_runtime_keeps_player_lifecycle_and_admin_hidden_guards(self) -> None:
        active_runtime = "\n".join(
            [
                read("script.py"),
                read("story.mast"),
                read("scripts/main.mast"),
                read("scripts/systems/scenario_control_panel.mast"),
                read("scripts/systems/story_jump_presets.mast"),
                read("scripts/systems/playable_bootstrap.mast"),
            ]
        )
        for forbidden in [
            "Select a bridge console for Artemis",
            "khovan_reach_slice01_client_main",
            "khovan_reach_slice01_console_selected",
            "assign_client_to_ship(client_id, artemis_id)",
            "gui_console(console_select)",
            'main_client = "khovan_reach_slice01_client_entry"',
            'main_client = "client_main"',
        ]:
            self.assertNotIn(forbidden, active_runtime)

        self.assertNotIn("common_console_select.client_main", active_runtime)
        self.assertIn("Gui.client_start_page_class(KhovanReachStoryPage)", active_runtime)

    def test_quick_suite_includes_slice03_static_checks(self) -> None:
        runner = read("run_tests.py")
        self.assertIn('ROOT / "tests" / "test_story_jump_presets_static.py"', runner)


if __name__ == "__main__":
    unittest.main()
