from __future__ import annotations

import ast
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_STATE = {
    "mission_phase": "\"act_1\"",
    "current_scene": "1",
    "current_beat": "\"scene_1_bootstrap\"",
    "last_checkpoint": "\"none\"",
    "transition_held": "False",
    "test_mode_enabled": "False",
    "live_recovery_mode_enabled": "False",
    "generator_governor_active": "True",
    "starting_energy": "0",
    "starting_homing_torpedoes": "0",
    "kestrel_generator_packet_sent": "False",
    "launch_envelope_cleared": "False",
    "energy_restored": "False",
    "dillon_clip_1_stub_sent": "False",
    "shakedown_mode": "\"unset\"",
    "training_overlay_active": "True",
    "comms_archive_enabled": "True",
    "artemis_player_ship_status": "\"pending_playable_bootstrap\"",
    "scene_1_runtime_presence": "\"pending_playable_bootstrap\"",
    "player_console_select_status": "\"legendary_reference_lifecycle\"",
}

REQUIRED_LEGENDARY_MASTLIB_STACK = [
    "artemis-sbs.LegendaryMissions.autoplay.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.ai.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.commerce.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.comms.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.consoles.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.damage.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.docking.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.fleets.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.grid_comms.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.hangar.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.internal_comms.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.prefabs.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.operator.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.science_scans.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.upgrades.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.gamemaster.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.gamemaster_comms.v1.3.0.mastlib",
    "artemis-sbs.LegendaryMissions.basic_player_destroy.v1.3.0.mastlib",
]

LEGACY_MAST_NAMES = {
    "dev_jump.mast",
    "act_1_qualification.mast",
    "act_1_state_helpers.mast",
    "act_2_investigation.mast",
    "act_3_khovan_reach.mast",
    "damcon_timer.mast",
    "salvager_arrival.mast",
    "state_save.mast",
    "__init__.mast",
}

FORBIDDEN_RUNTIME_REFERENCES = {
    "docs_external/_local_clones",
    r"docs_external\_local_clones",
    "reference_missions/_local_clones",
    r"reference_missions\_local_clones",
    "bar.mastlib",
}

MISSION_ROOT_LIBRARY_ARTIFACT_SUFFIXES = {".mastlib", ".sbslib", ".zip"}

DEFERRED_BOOTSTRAP_MODULE_REFERENCES = {
    "act_2_investigation.mast",
    "act_3_khovan_reach.mast",
    "damcon_timer.mast",
    "pirate_state_machine.mast",
    "salvager_arrival.mast",
}

FORBIDDEN_ACTIVE_MAST_GUI_PATTERNS = {
    "//gui",
    "@gui",
    "await gui",
    "gui_",
    "send_gui_",
    "button",
    "present",
    "route_change_console",
    "gui_reroute",
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class BootstrapStaticTests(unittest.TestCase):
    def test_story_json_is_valid(self) -> None:
        data = json.loads(read("story.json"))
        self.assertIn("sbslib", data)
        self.assertIn("artemis-sbs.sbs_utils.v1.3.0.sbslib", data["sbslib"])
        self.assertIn("mastlib", data)
        self.assertEqual(REQUIRED_LEGENDARY_MASTLIB_STACK, data["mastlib"])

    def test_settings_yaml_contains_reference_lifecycle_contract(self) -> None:
        settings = read("settings.yaml")
        for phrase in [
            "AUTO_START: false",
            "SHIP_PICK_READ_ONLY: false",
            "CAN_CHANGE_CONSOLE: true",
            "GAMEMASTER:",
            "enable: true",
            "PLAYER_CREATE_DEFAULT: true",
            "PLAYER_COUNT: 1",
            "PLAYER_LIST:",
            'name: "Artemis"',
            'side: "tsn"',
            'ship: "tsn_battle_cruiser"',
            'WORLD_SELECT: "khovan_reach"',
        ]:
            self.assertIn(phrase, settings)

    def test_lib_json_is_reference_aligned_metadata(self) -> None:
        data = json.loads(read("__lib__.json"))
        self.assertEqual({"version": "v1.3.0"}, data)

    def test_script_py_static_bootstrap_shape(self) -> None:
        script = read("script.py")
        ast.parse(script)
        self.assertIn("KHOVAN_STARTUP_TRACE_PATH", script)
        self.assertIn("tests\" / \"live_startup_trace.txt", script)
        self.assertIn("def write_khovan_startup_trace(message):", script)
        self.assertIn("[KHOVAN EARLY 001] script.py entered", script)
        self.assertIn("[KHOVAN EARLY 002] before sbs_utils import", script)
        self.assertIn("[KHOVAN EARLY 003] after sbs_utils import", script)
        self.assertIn("[KHOVAN EARLY 004] before reference StoryPage registration", script)
        self.assertIn("[KHOVAN EARLY 005] after reference StoryPage registration", script)
        self.assertIn("[KHOVAN EARLY 006] before story.mast load/handoff", script)
        self.assertIn("[KHOVAN EARLY 007] after story.mast load/handoff", script)
        self.assertIn("[KHOVAN EARLY EXCEPTION]", script)
        self.assertIn("traceback.format_exc()", script)
        self.assertIn("from sbs_utils.mast.mast_globals import MastGlobals", script)
        self.assertIn('MastGlobals.globals["script"] = sys.modules.get("script")', script)
        self.assertNotIn("ClientSelectPage", script)
        self.assertIn("class KhovanReachStoryPage(StoryPage):", script)
        self.assertIn('story_file = "story.mast"', script)
        self.assertNotIn("main_server", script)
        self.assertNotIn("main_client", script)
        self.assertIn("SLICE01_SMOKE_MARKER_PATH", script)
        self.assertIn("tests\" / \"live_smoke_last_bootstrap.txt", script)
        self.assertIn("def write_slice01_live_smoke_marker(client_id):", script)
        self.assertIn("def start_story(self, client_id):", script)
        self.assertIn("super().start_story(client_id)", script)
        self.assertNotIn("            write_slice01_live_smoke_marker(client_id)", script)
        self.assertIn("mission_phase=act_1", script)
        self.assertIn("current_scene=1", script)
        self.assertIn("dillon_clip_1_status=stubbed", script)
        self.assertIn("artemis_player_ship_status=initialized_by_reference_pattern", script)
        self.assertIn("scene_1_runtime_presence=artemis_player_ship_and_dillon_stub", script)
        self.assertIn("client_start_page=LegendaryMissions.server_console/client_main", script)
        self.assertIn("LegendaryMissions.server_console -> scripts/main.mast @map/khovan_reach", script)
        self.assertIn("Gui.server_start_page_class(KhovanReachStoryPage)", script)
        self.assertIn("Gui.client_start_page_class(KhovanReachStoryPage)", script)

    def test_live_smoke_marker_file_is_gitignored(self) -> None:
        gitignore = read(".gitignore")
        self.assertIn("tests/live_smoke_last_bootstrap.txt", gitignore)
        self.assertIn("tests/live_startup_trace.txt", gitignore)

    def test_story_mast_imports_active_main(self) -> None:
        story = read("story.mast")
        self.assertIn("import scripts/main.mast", story)

    def test_active_main_bootstrap_imports_systems(self) -> None:
        main = read("scripts/main.mast")
        self.assertIn("import scripts/systems/bootstrap_state.mast", main)
        self.assertIn("import scripts/systems/playable_bootstrap.mast", main)
        self.assertIn("import scripts/systems/audio_runtime.mast", main)
        self.assertIn("import scripts/systems/current_objective_panel.mast", main)
        self.assertIn("import scripts/systems/debug_runtime.mast", main)
        self.assertNotIn("import scripts/systems/comms_proof_station.mast", main)
        self.assertRegex(main, r"(?m)^\s*shared\s+artemis_id\s*=\s*0\s*$")
        self.assertIn("@map/khovan_reach", main)
        self.assertIn("=== khovan_reach_slice01_entry ===", main)
        self.assertNotIn("=== khovan_reach_slice01_client_entry ===", main)
        self.assertNotIn("=== khovan_reach_slice01_client_main ===", main)
        self.assertNotIn("=== khovan_reach_slice01_console_selected ===", main)
        self.assertIn("khovan_reach_slice01_bootstrap", main)
        self.assertNotIn("jump khovan_reach_slice01_server_playable", main)
        self.assertNotIn("=== khovan_reach_slice01_server_playable ===", main)
        self.assertNotIn("Select a bridge console for Artemis", main)
        self.assertIn("khovan_reach_initialize_playable_bootstrap", main)
        self.assertNotIn("khovan_comms_proof_station_initialize", main)
        self.assertNotIn("[KHOVAN BOOT 004B] Comms proof station initialized", main)
        self.assertIn("[KHOVAN BOOT 001] scripts/main.mast entered", main)
        self.assertIn("[KHOVAN BOOT 002] before state defaults", main)
        self.assertIn("[KHOVAN BOOT 003] after state defaults", main)
        self.assertIn("[KHOVAN BOOT 004] before playable_bootstrap", main)
        self.assertNotIn("[KHOVAN BOOT 007A] before client/page playable transition", main)
        self.assertNotIn("[KHOVAN BOOT 007B] after client/page playable transition", main)
        self.assertNotIn("[KHOVAN BOOT 007C] before player/client assignment confirmation", main)
        self.assertNotIn("[KHOVAN BOOT 007D] after player/client assignment confirmation", main)
        self.assertIn("[KHOVAN BOOT 009] mission_phase=act_1 current_scene=1", main)
        self.assertIn("[KHOVAN BOOT 010] playable bootstrap complete", main)
        self.assertIn("[KHOVAN ROUTE 001] map selected", main)
        self.assertIn("[KHOVAN ROUTE 002] before spawn_players", main)
        self.assertIn("[KHOVAN ROUTE 003] after spawn_players", main)
        self.assertNotIn("[KHOVAN ROUTE 004] console selected", main)
        self.assertNotIn("[KHOVAN ROUTE 005] client assigned to Artemis", main)
        self.assertIn("script.write_slice01_live_smoke_marker(0)", main)
        self.assertIn('logger("mast.runtime")', main)
        self.assertIn('"mast.runtime"', main)
        self.assertIn("mission_phase = act_1; current_scene = 1", main)
        self.assertIn("dillon_clip_1_status = stubbed", main)
        self.assertIn("artemis_player_ship_status = initialized", main)
        self.assertNotIn("sim_resume()", main)
        self.assertNotIn("assign_client_to_ship(0, artemis_id)", main)
        self.assertNotIn("assign_client_to_ship(client_id, artemis_id)", main)
        self.assertNotIn("gui_console(console_select)", main)
        self.assertIn("await task_schedule(spawn_players)", main)

    def test_map_route_enters_reference_backed_playable_server_route(self) -> None:
        main = read("scripts/main.mast")
        match = re.search(
            r"@map/khovan_reach\b(?P<body>.*?)^=== khovan_reach_slice01_entry ===",
            main,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match)
        map_body = match.group("body")
        self.assertIn("[KHOVAN ROUTE 001] map selected", map_body)
        self.assertIn("await task_schedule(khovan_reach_slice01_entry)", map_body)
        self.assertNotIn("task_schedule(khovan_reach_slice01_server_playable)", map_body)
        self.assertIn("->END", map_body)

    def test_storypage_uses_reference_reroute_lifecycle(self) -> None:
        script = read("script.py")
        main = read("scripts/main.mast")
        self.assertNotIn("main_server", script)
        self.assertNotIn("main_client", script)
        self.assertIn("Gui.server_start_page_class(KhovanReachStoryPage)", script)
        self.assertIn("Gui.client_start_page_class(KhovanReachStoryPage)", script)

        server_match = re.search(
            r"^=== khovan_reach_slice01_entry ===(?P<body>.*?)^=== khovan_reach_slice01_bootstrap ===",
            main,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(server_match)
        server_body = server_match.group("body")
        self.assertIn("await task_schedule(spawn_players)", server_body)
        self.assertIn("await task_schedule(khovan_reach_slice01_bootstrap)", server_body)
        self.assertIn("script.write_slice01_live_smoke_marker(0)", server_body)
        self.assertIn("->END", server_body)

    def test_required_bootstrap_system_files_exist(self) -> None:
        for path in [
            "__lib__.json",
            "scripts/main.mast",
            "scripts/systems/bootstrap_state.mast",
            "scripts/systems/playable_bootstrap.mast",
            "scripts/systems/audio_runtime.mast",
            "scripts/systems/current_objective_panel.mast",
            "scripts/systems/debug_runtime.mast",
        ]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_bootstrap_state_values_initialize(self) -> None:
        state = read("scripts/systems/bootstrap_state.mast")
        for name, value in REQUIRED_STATE.items():
            pattern = rf"(?m)^\s*{re.escape(name)}\s*=\s*{re.escape(value)}\s*$"
            self.assertRegex(state, pattern, name)

    def test_slice01b_playable_bootstrap_binds_reference_spawned_ship(self) -> None:
        playable = read("scripts/systems/playable_bootstrap.mast")
        self.assertIn("=== khovan_reach_initialize_playable_bootstrap ===", playable)
        self.assertIn("[KHOVAN BOOT 005] playable_bootstrap entered", playable)
        self.assertIn("[KHOVAN BOOT 006] before Artemis/player ship init or confirmation", playable)
        self.assertIn("[KHOVAN BOOT 006A] before reference player ship query", playable)
        self.assertIn("[KHOVAN BOOT 006B] after reference player ship query", playable)
        self.assertIn("[KHOVAN BOOT 006C] before Khovan ship binding", playable)
        self.assertIn("[KHOVAN BOOT 006D] after Khovan ship binding", playable)
        self.assertIn("[KHOVAN BOOT 007] after Artemis/player ship init or confirmation", playable)
        self.assertNotIn("artemis_ship_name", playable)
        self.assertNotIn("sim_create()", playable)
        self.assertNotIn("player_spawn(", playable)
        self.assertNotIn("assign_client_to_ship", playable)
        self.assertIn('if player_ship.name == "Artemis":', playable)
        self.assertIn('artemis_object.name = "Artemis"', playable)
        self.assertIn('role("__player__") & role("tsn")', playable)
        self.assertIn('artemis_player_ship_status = "initialized"', playable)
        self.assertIn('scene_1_runtime_presence = "artemis_player_ship_and_dillon_stub"', playable)
        self.assertIn('player_console_select_status = "legendary_reference_lifecycle"', playable)

    def test_artemis_id_is_shared_after_reference_spawn_players(self) -> None:
        main = read("scripts/main.mast")
        playable = read("scripts/systems/playable_bootstrap.mast")
        self.assertRegex(main, r"(?m)^\s*shared\s+artemis_id\s*=\s*0\s*$")
        self.assertIn("shared artemis_id = artemis_object.id", playable)
        self.assertIn("await task_schedule(spawn_players)", main)
        self.assertNotIn("assign_client_to_ship(client_id, artemis_id)", main)
        self.assertNotIn("gui_console(console_select)", main)

    def test_slice01b_rejects_partial_legendary_or_custom_selector(self) -> None:
        data = json.loads(read("story.json"))
        script = read("script.py")
        runtime_text = "\n".join(
            [
                script,
                read("story.mast"),
                read("scripts/main.mast"),
                read("scripts/systems/playable_bootstrap.mast"),
            ]
        )

        self.assertEqual(REQUIRED_LEGENDARY_MASTLIB_STACK, data["mastlib"])
        self.assertNotEqual(
            [
                "artemis-sbs.LegendaryMissions.consoles.v1.3.0.mastlib",
                "artemis-sbs.LegendaryMissions.gamemaster.v1.3.0.mastlib",
            ],
            data["mastlib"],
        )
        for forbidden in [
            "Select a bridge console for Artemis",
            "khovan_reach_slice01_client_main",
            "khovan_reach_slice01_console_selected",
            "assign_client_to_ship(client_id, artemis_id)",
            "gui_console(console_select)",
            'main_client = "client_main"',
            'main_client = "khovan_reach_slice01_client_entry"',
        ]:
            self.assertNotIn(forbidden, runtime_text)

    def test_dillon_clip_1_is_stubbed(self) -> None:
        audio = read("scripts/systems/audio_runtime.mast")
        self.assertIn("shared dillon_clip_1_stub_text", audio)
        self.assertIn("Crew of Artemis, this is a qualification cruise.", audio)
        self.assertIn("First task: get the ship out of Kestrel cleanly.", audio)
        self.assertIn("Comms, request departure clearance.", audio)
        self.assertIn("Helm, hold position until Kestrel releases the yard-lock.", audio)
        self.assertIn("Captain, coordinate the sequence.", audio)
        self.assertNotIn("Captain. Crew of Artemis. This is a qualification cruise.", audio)
        self.assertNotIn("Standard pattern: depart Kestrel", audio)
        self.assertNotIn("Captain, the ship is yours.", audio)
        self.assertIn("=== khovan_reach_stub_dillon_clip_1 ===", audio)
        self.assertIn("if dillon_clip_1_stub_sent:", audio)
        self.assertIn("[KHOVAN ACT1 MSG ORDER] duplicate suppressed Dillon Clip 1 stub", audio)
        self.assertIn("dillon_clip_1_stub_sent = True", audio)
        self.assertIn('dillon_clip_1_status = "stubbed"', audio)
        self.assertIn('shared dillon_clip_1_delivery_mode = "text_standin_safe_comms_no_lifeform_overlay"', audio)
        self.assertIn("=== khovan_reach_send_safe_startup_message ===", audio)
        self.assertIn("with comms_override(startup_sender_id, startup_player_id, from_name=startup_sender):", audio)
        self.assertIn("comms_receive(startup_text, title=startup_title, title_color=startup_title_color)", audio)
        self.assertIn("[KHOVAN ACT1 UI] black-box overlay source disabled or replaced", audio)
        self.assertIn("[KHOVAN ACT1 UI] lifeform overlay deferred", audio)
        self.assertIn("[KHOVAN ACT1 UI] safe text message path used", audio)
        self.assertIn("[KHOVAN DILLON SAFE] Comms echo skipped because sender/context unavailable", audio)
        self.assertIn("await task_schedule(khovan_reach_send_safe_startup_message", audio)
        self.assertIn('"startup_sender": "Commander Dillon"', audio)
        self.assertIn('"startup_text": dillon_clip_1_stub_text', audio)
        self.assertIn('"startup_sender_id": kestrel_yards_id', audio)
        self.assertIn("[KHOVAN DILLON 001] Clip 1 text stand-in requested", audio)
        self.assertIn("[KHOVAN DILLON 002] Clip 1 visible text sent", audio)
        self.assertIn("[KHOVAN DILLON 003] Clip 1 Comms archive echo sent", audio)
        self.assertIn("[KHOVAN ACT1 MSG DILLON 001] Dillon opening briefing sent", audio)
        self.assertNotIn('comms_receive(dillon_clip_1_stub_text', audio)
        self.assertIn("[KHOVAN BOOT 008] Dillon Clip 1 stub/queue reached", audio)
        self.assertNotIn("sbs.send_story_dialog", audio)

    def test_debug_runtime_is_stubbed(self) -> None:
        debug = read("scripts/systems/debug_runtime.mast")
        self.assertIn('gm_debug_overlay_status = "stubbed"', debug)
        self.assertIn('player_debug_controls_status = "stubbed_hidden"', debug)

    def test_slice01_debug_runtime_has_no_active_gui_controls(self) -> None:
        debug = read("scripts/systems/debug_runtime.mast").lower()
        hits = [
            pattern
            for pattern in FORBIDDEN_ACTIVE_MAST_GUI_PATTERNS
            if pattern in debug
        ]
        self.assertEqual([], sorted(hits))

    def test_slice01_active_mast_has_no_control_panel_or_dev_jump_code(self) -> None:
        hits: list[str] = []
        for path in sorted((ROOT / "scripts").rglob("*.mast")):
            if path.relative_to(ROOT).as_posix() in {
                "scripts/systems/scenario_control_panel.mast",
                "scripts/systems/story_jump_presets.mast",
            }:
                continue
            text = path.read_text(encoding="utf-8").lower()
            for pattern in ["dev_jump", "story jump", "scenario control panel"]:
                if pattern == "scenario control panel" and "scenario control panel is slice 02" in text:
                    continue
                if pattern in text:
                    hits.append(f"{path.relative_to(ROOT).as_posix()}: {pattern}")
        self.assertEqual([], hits)

    def test_legacy_old_mast_filenames_are_not_active(self) -> None:
        found = [
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "scripts").rglob("*.mast")
            if path.name in LEGACY_MAST_NAMES
        ]
        self.assertEqual([], found)

    def test_external_clone_contents_are_not_tracked(self) -> None:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "docs_external/_local_clones",
                "reference_missions/_local_clones",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual("", result.stdout.strip())

    def test_runtime_files_do_not_reference_local_tier2_clones(self) -> None:
        runtime_files = [
            ROOT / "__lib__.json",
            ROOT / "script.py",
            ROOT / "story.json",
            ROOT / "story.mast",
            *sorted((ROOT / "scripts").rglob("*.mast")),
        ]
        hits: list[str] = []
        for path in runtime_files:
            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN_RUNTIME_REFERENCES:
                if forbidden in text:
                    hits.append(f"{path.relative_to(ROOT).as_posix()}: {forbidden}")
        self.assertEqual([], hits)

    def test_no_library_archives_inside_mission_root_reference_clones(self) -> None:
        found: list[str] = []
        for base in [
            ROOT / "docs_external" / "_local_clones",
            ROOT / "reference_missions" / "_local_clones",
        ]:
            if not base.exists():
                continue
            found.extend(
                path.relative_to(ROOT).as_posix()
                for path in base.rglob("*")
                if path.is_file()
                and path.suffix.lower() in MISSION_ROOT_LIBRARY_ARTIFACT_SUFFIXES
            )
        self.assertEqual([], sorted(found))

    def test_no_reference_archive_mast_auto_entrypoints(self) -> None:
        found = [
            path.relative_to(ROOT).as_posix()
            for base in [ROOT / "archive", ROOT / "docs_external", ROOT / "reference_missions"]
            if base.exists()
            for path in base.rglob("__init__.mast")
            if path.is_file()
        ]
        self.assertEqual([], sorted(found))

    def test_slice01_runtime_does_not_load_deferred_modules(self) -> None:
        runtime_files = [
            ROOT / "script.py",
            ROOT / "story.json",
            ROOT / "story.mast",
            *sorted((ROOT / "scripts").rglob("*.mast")),
        ]
        hits: list[str] = []
        for path in runtime_files:
            text = path.read_text(encoding="utf-8").lower()
            for name in DEFERRED_BOOTSTRAP_MODULE_REFERENCES:
                if name in text:
                    hits.append(f"{path.relative_to(ROOT).as_posix()}: {name}")
        self.assertEqual([], hits)

    def test_active_mast_imports_reference_existing_files(self) -> None:
        active_mast_files = [ROOT / "story.mast", *sorted((ROOT / "scripts").rglob("*.mast"))]
        missing: list[str] = []
        for path in active_mast_files:
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"(?m)^\s*import\s+([^\s#]+\.mast)\s*$", text):
                import_path = match.group(1).replace("\\", "/")
                if not (ROOT / import_path).is_file():
                    missing.append(f"{path.relative_to(ROOT).as_posix()}: {import_path}")
        self.assertEqual([], missing)

    def test_slice01_verification_doc_exists(self) -> None:
        self.assertTrue((ROOT / "tests" / "SLICE01_VERIFICATION.md").is_file())

    def test_slice01_bootstrap_findings_doc_records_runtime_blockers(self) -> None:
        path = ROOT / "docs" / "04_implementation_setup" / "40_slice01_bootstrap_findings.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8").lower()
        for phrase in [
            "runtime-clean mission root",
            "salvager_arrival.mast",
            "edge case",
            "gui/task lifecycle",
            "mast compile/preflight",
            "middle evidence class",
            "tests/test_mast_compile_or_preflight.py",
            "route-smoke breadcrumb trace",
            "tests/live_startup_trace.txt",
            "last-success audit",
        ]:
            self.assertIn(phrase, text)

    def test_admin_testing_plan_records_testing_evidence_classes(self) -> None:
        text = read("docs/01_design/40_admin_testing_plan.md").lower()
        for phrase in [
            "testing evidence classes",
            "static/source checks",
            "mast compile/preflight checks",
            "runtime load-path checks",
            "route-smoke breadcrumb traces",
            "live cosmos smoke",
            "tests/test_mast_compile_or_preflight.py",
            "live failures outrank green quick tests",
        ]:
            self.assertIn(phrase, text)

    def test_agents_doc_requires_runtime_load_and_gui_lifecycle_testing(self) -> None:
        text = read("AGENTS.md").lower()
        self.assertIn("runtime load and gui lifecycle testing", text)
        self.assertIn("runtime load path", text)
        self.assertIn("compile-preflight", text)
        self.assertIn("middle evidence class", text)
        self.assertIn("git-ignored folders are not runtime-ignored", text)
        self.assertIn("live cosmos smoke remains required", text)
        self.assertIn("route-smoke breadcrumb trace", text)
        self.assertIn("tests/live_startup_trace.txt", text)
        self.assertIn("last-success audit", text)
        self.assertIn("boot-001", text)
        self.assertIn("boot-012", text)

    def test_quick_flags_skipped_compile_preflight_loudly(self) -> None:
        # A skipped MAST compile preflight (no local Cosmos install) is a real
        # evidence-class gap, not an ordinary warning - a PASS with it skipped
        # must not read identically to a PASS with it included. Verified live
        # by temporarily hiding the sbslib and confirming this line printed,
        # then restoring it; this test locks the mechanism in place.
        runner = read("run_tests.py")
        self.assertIn('"sbs_utils library not found" in warning', runner)
        self.assertIn("EVIDENCE GAP", runner)
        self.assertIn("Do not claim compile-preflight coverage", runner)

    def test_slice01_verification_records_live_smoke_requirements(self) -> None:
        text = read("tests/SLICE01_VERIFICATION.md").lower()
        self.assertIn("live cosmos smoke evidence and runtime blockers", text)
        self.assertIn("quick tests are necessary but not sufficient", text)
        self.assertIn("mast compile/preflight", text)
        self.assertIn("middle evidence class", text)
        self.assertIn("boot-001", text)
        self.assertIn("boot-012", text)
        self.assertIn("salvager_arrival.mast", text)
        self.assertIn("edge case", text)
        self.assertIn("mast.runtime.log", text)
        self.assertIn("mast.compile.log", text)
        self.assertIn("tests/live_smoke_last_bootstrap.txt", text)
        self.assertIn("mission_phase=act_1", text)
        self.assertIn("current_scene=1", text)

    def test_negative_control_wording_is_not_inverted(self) -> None:
        searched_files = [
            ROOT / "run_tests.py",
            *sorted((ROOT / "tests").glob("*.py")),
            *sorted((ROOT / "tests").glob("*.md")),
            *sorted((ROOT / "docs").rglob("*.md")),
        ]
        inverted = (
            "negative control failed: quick tests caught "
            "the broken mast import"
        )
        hits = [
            path.relative_to(ROOT).as_posix()
            for path in searched_files
            if path.is_file()
            and path.name != "test_bootstrap_static.py"
            and inverted in path.read_text(encoding="utf-8").lower()
        ]
        self.assertEqual([], hits)


if __name__ == "__main__":
    unittest.main()
