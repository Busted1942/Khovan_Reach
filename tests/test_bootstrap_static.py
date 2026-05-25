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
    "starting_homing_torpedoes": "2",
    "kestrel_generator_packet_sent": "False",
    "launch_envelope_cleared": "False",
    "shakedown_mode": "\"unset\"",
    "training_overlay_active": "True",
    "comms_archive_enabled": "True",
    "artemis_player_ship_status": "\"pending_playable_bootstrap\"",
    "scene_1_runtime_presence": "\"pending_playable_bootstrap\"",
    "player_console_select_status": "\"client_select_page_enabled\"",
}

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
        self.assertIn("[KHOVAN EARLY 004] before client StoryPage setup", script)
        self.assertIn("[KHOVAN EARLY 005] after client StoryPage setup", script)
        self.assertIn("[KHOVAN EARLY 006] before story.mast load/handoff", script)
        self.assertIn("[KHOVAN EARLY 007] after story.mast load/handoff", script)
        self.assertIn("[KHOVAN EARLY EXCEPTION]", script)
        self.assertIn("traceback.format_exc()", script)
        self.assertIn("from sbs_utils.mast.mast_globals import MastGlobals", script)
        self.assertIn('MastGlobals.globals["script"] = sys.modules.get("script")', script)
        self.assertNotIn("ClientSelectPage", script)
        self.assertIn("class KhovanReachStoryPage(StoryPage):", script)
        self.assertIn('story_file = "story.mast"', script)
        self.assertIn('main_server = "khovan_reach_slice01_entry"', script)
        self.assertIn('main_client = "khovan_reach_slice01_client_entry"', script)
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
        self.assertIn("client_start_page=KhovanReachStoryPage", script)
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
        self.assertIn("import scripts/systems/debug_runtime.mast", main)
        self.assertRegex(main, r"(?m)^\s*shared\s+artemis_id\s*=\s*0\s*$")
        self.assertIn("@map/khovan_reach", main)
        self.assertIn("=== khovan_reach_slice01_entry ===", main)
        self.assertIn("=== khovan_reach_slice01_client_entry ===", main)
        self.assertIn("=== khovan_reach_slice01_client_main ===", main)
        self.assertIn("=== khovan_reach_slice01_console_selected ===", main)
        self.assertIn("khovan_reach_slice01_bootstrap", main)
        self.assertIn("jump khovan_reach_slice01_server_playable", main)
        self.assertIn("=== khovan_reach_slice01_server_playable ===", main)
        self.assertIn(
            "Khovan Reach Slice 01A playable bootstrap loaded. Scene 1 initialized.",
            main,
        )
        self.assertIn("khovan_reach_initialize_playable_bootstrap", main)
        self.assertIn("[KHOVAN BOOT 001] scripts/main.mast entered", main)
        self.assertIn("[KHOVAN BOOT 002] before state defaults", main)
        self.assertIn("[KHOVAN BOOT 003] after state defaults", main)
        self.assertIn("[KHOVAN BOOT 004] before playable_bootstrap", main)
        self.assertIn("[KHOVAN BOOT 007A] before client/page playable transition", main)
        self.assertIn("[KHOVAN BOOT 007B] after client/page playable transition", main)
        self.assertIn("[KHOVAN BOOT 007C] before player/client assignment confirmation", main)
        self.assertIn("[KHOVAN BOOT 007D] after player/client assignment confirmation", main)
        self.assertIn("[KHOVAN BOOT 009] mission_phase=act_1 current_scene=1", main)
        self.assertIn("[KHOVAN BOOT 010] playable bootstrap complete", main)
        self.assertIn("[KHOVAN ROUTE 001] map selected", main)
        self.assertIn("[KHOVAN ROUTE 002] player ship initialized", main)
        self.assertIn("[KHOVAN ROUTE 003] playable bridge transition reached", main)
        self.assertIn("[KHOVAN ROUTE 004] console selected", main)
        self.assertIn("[KHOVAN ROUTE 005] client assigned to Artemis", main)
        self.assertIn("script.write_slice01_live_smoke_marker(0)", main)
        self.assertIn('logger("mast.runtime")', main)
        self.assertIn('"mast.runtime"', main)
        self.assertIn("mission_phase = act_1; current_scene = 1", main)
        self.assertIn("dillon_clip_1_status = stubbed", main)
        self.assertIn("artemis_player_ship_status = initialized", main)
        self.assertIn("sim_resume()", main)
        self.assertIn("assign_client_to_ship(0, artemis_id)", main)
        self.assertIn('link(artemis_id, "consoles", client_id)', main)
        self.assertIn('add_role(client_id, "console, mainscreen")', main)
        self.assertIn('gui_console("mainscreen")', main)
        self.assertIn("assign_client_to_ship(client_id, artemis_id)", main)
        self.assertIn("gui_console(console_select)", main)

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
        self.assertIn("jump khovan_reach_slice01_entry", map_body)
        self.assertNotIn("task_schedule(khovan_reach_slice01_server_playable)", map_body)
        self.assertNotIn("->END", map_body)

    def test_storypage_entry_labels_are_defined_and_persistent(self) -> None:
        script = read("script.py")
        main = read("scripts/main.mast")
        self.assertIn('main_server = "khovan_reach_slice01_entry"', script)
        self.assertIn('main_client = "khovan_reach_slice01_client_entry"', script)

        server_match = re.search(
            r"^=== khovan_reach_slice01_entry ===(?P<body>.*?)^=== khovan_reach_slice01_client_entry ===",
            main,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(server_match)
        server_body = server_match.group("body")
        self.assertIn("await task_schedule(khovan_reach_slice01_bootstrap)", server_body)
        self.assertIn("jump khovan_reach_slice01_server_playable", server_body)
        self.assertNotIn("->END", server_body)

        client_match = re.search(
            r"^=== khovan_reach_slice01_client_entry ===(?P<body>.*?)^=== khovan_reach_slice01_bootstrap ===",
            main,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(client_match)
        client_body = client_match.group("body")
        self.assertIn("jump khovan_reach_slice01_client_main", client_body)
        self.assertNotIn("->END", client_body)

    def test_required_bootstrap_system_files_exist(self) -> None:
        for path in [
            "__lib__.json",
            "scripts/main.mast",
            "scripts/systems/bootstrap_state.mast",
            "scripts/systems/playable_bootstrap.mast",
            "scripts/systems/audio_runtime.mast",
            "scripts/systems/debug_runtime.mast",
        ]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_bootstrap_state_values_initialize(self) -> None:
        state = read("scripts/systems/bootstrap_state.mast")
        for name, value in REQUIRED_STATE.items():
            pattern = rf"(?m)^\s*{re.escape(name)}\s*=\s*{re.escape(value)}\s*$"
            self.assertRegex(state, pattern, name)

    def test_slice01a_playable_bootstrap_uses_reference_spawn_pattern(self) -> None:
        playable = read("scripts/systems/playable_bootstrap.mast")
        self.assertIn("=== khovan_reach_initialize_playable_bootstrap ===", playable)
        self.assertIn("[KHOVAN BOOT 005] playable_bootstrap entered", playable)
        self.assertIn("[KHOVAN BOOT 006] before Artemis/player ship init or confirmation", playable)
        self.assertIn("[KHOVAN BOOT 006A] before sim_create", playable)
        self.assertIn("[KHOVAN BOOT 006B] after sim_create", playable)
        self.assertIn("[KHOVAN BOOT 006E] before ship spawn call", playable)
        self.assertIn("[KHOVAN BOOT 006F] after ship spawn call", playable)
        self.assertIn("[KHOVAN BOOT 006J] before client/player assignment", playable)
        self.assertIn("[KHOVAN BOOT 006K] after client/player assignment", playable)
        self.assertIn("[KHOVAN BOOT 007] after Artemis/player ship init or confirmation", playable)
        self.assertNotIn("artemis_ship_name", playable)
        self.assertIn("sim_create()", playable)
        self.assertIn("shared artemis_id = to_id(player_spawn(0, 0, 0, \"Artemis\", \"tsn\", \"tsn_battle_cruiser\"))", playable)
        self.assertIn("assign_client_to_ship(0, artemis_id)", playable)
        self.assertIn('if player_ship.name == "Artemis":', playable)
        self.assertIn('artemis_object.name = "Artemis"', playable)
        self.assertIn('role("__player__") & role("tsn")', playable)
        self.assertIn('add_role(artemis_id, "default_player_ship")', playable)
        self.assertIn('artemis_player_ship_status = "initialized"', playable)
        self.assertIn('scene_1_runtime_presence = "artemis_player_ship_and_dillon_stub"', playable)
        self.assertIn('player_console_select_status = "client_select_page_enabled"', playable)

    def test_artemis_id_is_shared_before_assignment_routes_use_it(self) -> None:
        main = read("scripts/main.mast")
        playable = read("scripts/systems/playable_bootstrap.mast")
        self.assertRegex(main, r"(?m)^\s*shared\s+artemis_id\s*=\s*0\s*$")
        self.assertIn("shared artemis_id = to_id(player_spawn", playable)
        self.assertIn("shared artemis_id = artemis_object.id", playable)
        self.assertIn("assign_client_to_ship(0, artemis_id)", main)
        self.assertIn("assign_client_to_ship(client_id, artemis_id)", main)

    def test_dillon_clip_1_is_stubbed(self) -> None:
        audio = read("scripts/systems/audio_runtime.mast")
        self.assertIn("shared dillon_clip_1_stub_text", audio)
        self.assertIn("=== khovan_reach_stub_dillon_clip_1 ===", audio)
        self.assertIn('dillon_clip_1_status = "stubbed"', audio)
        self.assertIn("Dillon Clip 1 text stub active", audio)
        self.assertIn("[KHOVAN BOOT 008] Dillon Clip 1 stub/queue reached", audio)
        self.assertIn("sbs.send_story_dialog(0", audio)

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
