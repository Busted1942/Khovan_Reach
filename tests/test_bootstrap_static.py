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
        self.assertIn("class KhovanReachStoryPage(StoryPage):", script)
        self.assertIn('story_file = "story.mast"', script)
        self.assertIn('main_server = "khovan_reach_slice01_entry"', script)
        self.assertIn('main_client = "khovan_reach_slice01_client_entry"', script)
        self.assertIn("SLICE01_SMOKE_MARKER_PATH", script)
        self.assertIn("tests\" / \"live_smoke_last_bootstrap.txt", script)
        self.assertIn("def write_slice01_live_smoke_marker(client_id):", script)
        self.assertIn("def start_story(self, client_id):", script)
        self.assertIn("super().start_story(client_id)", script)
        self.assertIn("write_slice01_live_smoke_marker(client_id)", script)
        self.assertIn("mission_phase=act_1", script)
        self.assertIn("current_scene=1", script)
        self.assertIn("Gui.server_start_page_class(KhovanReachStoryPage)", script)
        self.assertIn("Gui.client_start_page_class(KhovanReachStoryPage)", script)

    def test_live_smoke_marker_file_is_gitignored(self) -> None:
        gitignore = read(".gitignore")
        self.assertIn("tests/live_smoke_last_bootstrap.txt", gitignore)

    def test_story_mast_imports_active_main(self) -> None:
        story = read("story.mast")
        self.assertIn("import scripts/main.mast", story)

    def test_active_main_bootstrap_imports_systems(self) -> None:
        main = read("scripts/main.mast")
        self.assertIn("import scripts/systems/bootstrap_state.mast", main)
        self.assertIn("import scripts/systems/audio_runtime.mast", main)
        self.assertIn("import scripts/systems/debug_runtime.mast", main)
        self.assertIn("@map/khovan_reach", main)
        self.assertIn("=== khovan_reach_slice01_entry ===", main)
        self.assertIn("=== khovan_reach_slice01_client_entry ===", main)
        self.assertIn("khovan_reach_slice01_bootstrap", main)
        self.assertIn("jump khovan_reach_slice01_runtime_idle", main)
        self.assertIn("=== khovan_reach_slice01_runtime_idle ===", main)
        self.assertIn(
            "Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.",
            main,
        )
        self.assertIn("sbs.send_story_dialog(0", main)
        self.assertIn('logger("mast.runtime")', main)
        self.assertIn('"mast.runtime"', main)
        self.assertIn("mission_phase = act_1; current_scene = 1", main)
        self.assertIn("await gui(timeout=delay_sim(10))", main)
        self.assertIn("jump khovan_reach_slice01_runtime_idle", main)

    def test_map_route_continues_directly_into_idle_task(self) -> None:
        main = read("scripts/main.mast")
        match = re.search(
            r"@map/khovan_reach\b(?P<body>.*?)^=== khovan_reach_slice01_entry ===",
            main,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match)
        map_body = match.group("body")
        self.assertIn("jump khovan_reach_slice01_entry", map_body)
        self.assertNotIn("task_schedule(khovan_reach_slice01_runtime_idle)", map_body)
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
        self.assertIn("jump khovan_reach_slice01_runtime_idle", server_body)
        self.assertNotIn("->END", server_body)

        client_match = re.search(
            r"^=== khovan_reach_slice01_client_entry ===(?P<body>.*?)^=== khovan_reach_slice01_bootstrap ===",
            main,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(client_match)
        client_body = client_match.group("body")
        self.assertIn("jump khovan_reach_slice01_runtime_idle", client_body)
        self.assertNotIn("->END", client_body)

    def test_required_bootstrap_system_files_exist(self) -> None:
        for path in [
            "__lib__.json",
            "scripts/main.mast",
            "scripts/systems/bootstrap_state.mast",
            "scripts/systems/audio_runtime.mast",
            "scripts/systems/debug_runtime.mast",
        ]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_bootstrap_state_values_initialize(self) -> None:
        state = read("scripts/systems/bootstrap_state.mast")
        for name, value in REQUIRED_STATE.items():
            pattern = rf"(?m)^\s*{re.escape(name)}\s*=\s*{re.escape(value)}\s*$"
            self.assertRegex(state, pattern, name)

    def test_dillon_clip_1_is_stubbed(self) -> None:
        audio = read("scripts/systems/audio_runtime.mast")
        self.assertIn("=== khovan_reach_stub_dillon_clip_1 ===", audio)
        self.assertIn('dillon_clip_1_status = "stubbed"', audio)

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
        ]:
            self.assertIn(phrase, text)

    def test_agents_doc_requires_runtime_load_and_gui_lifecycle_testing(self) -> None:
        text = read("AGENTS.md").lower()
        self.assertIn("runtime load and gui lifecycle testing", text)
        self.assertIn("runtime load path", text)
        self.assertIn("git-ignored folders are not runtime-ignored", text)
        self.assertIn("live cosmos smoke remains required", text)
        self.assertIn("boot-001", text)
        self.assertIn("boot-012", text)

    def test_slice01_verification_records_live_smoke_requirements(self) -> None:
        text = read("tests/SLICE01_VERIFICATION.md").lower()
        self.assertIn("live cosmos smoke evidence and runtime blockers", text)
        self.assertIn("quick tests are necessary but not sufficient", text)
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
