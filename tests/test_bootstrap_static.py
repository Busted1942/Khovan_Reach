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
        self.assertIn("Gui.server_start_page_class(KhovanReachStoryPage)", script)
        self.assertIn("Gui.client_start_page_class(KhovanReachStoryPage)", script)

    def test_story_mast_imports_active_main(self) -> None:
        story = read("story.mast")
        self.assertIn("import scripts/main.mast", story)

    def test_active_main_bootstrap_imports_systems(self) -> None:
        main = read("scripts/main.mast")
        self.assertIn("import scripts/systems/bootstrap_state.mast", main)
        self.assertIn("import scripts/systems/audio_runtime.mast", main)
        self.assertIn("import scripts/systems/debug_runtime.mast", main)
        self.assertIn("@map/khovan_reach", main)
        self.assertIn("khovan_reach_slice01_bootstrap", main)

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

    def test_slice01_verification_doc_exists(self) -> None:
        self.assertTrue((ROOT / "tests" / "SLICE01_VERIFICATION.md").is_file())


if __name__ == "__main__":
    unittest.main()
