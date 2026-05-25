from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
import logging
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SBS_UTILS_LIB = (
    ROOT.parent
    / "__lib__"
    / "artemis-sbs.sbs_utils.v1.3.0.sbslib"
)


class MastCompileOrPreflightTests(unittest.TestCase):
    def close_mast_loggers(self) -> None:
        loggers = [logging.getLogger()]
        loggers.extend(
            logger
            for logger in logging.Logger.manager.loggerDict.values()
            if isinstance(logger, logging.Logger)
        )
        for logger in loggers:
            for handler in list(logger.handlers):
                handler.close()
                logger.removeHandler(handler)

    def load_mast_story(self):
        if not SBS_UTILS_LIB.is_file():
            self.skipTest(f"installed sbs_utils library not found: {SBS_UTILS_LIB}")

        temp_dir = tempfile.TemporaryDirectory(prefix="khovan_sbs_utils_preflight_")
        self.addCleanup(temp_dir.cleanup)
        self.addCleanup(self.close_mast_loggers)
        extract_dir = Path(temp_dir.name)
        with zipfile.ZipFile(SBS_UTILS_LIB) as archive:
            archive.extractall(extract_dir)

        sys.path.insert(0, str(extract_dir))
        self.addCleanup(lambda: sys.path.remove(str(extract_dir)))
        try:
            import sbs_utils.mast_sbs.story_nodes  # Registers SBS/GUI MAST nodes.
            from sbs_utils.mast.mast import Mast
            from sbs_utils.mast.maststory import MastStory
            import sbs_utils.fs as sbs_fs
        except Exception as exc:  # pragma: no cover - environment-specific skip
            self.skipTest(f"sbs_utils MastStory preflight API not importable: {exc}")

        original_script_dir = sbs_fs.script_dir
        sbs_fs.script_dir = str(ROOT).replace("/", "\\")
        self.addCleanup(lambda: setattr(sbs_fs, "script_dir", original_script_dir))
        return Mast, MastStory

    def test_active_story_mast_compiles_with_installed_maststory(self) -> None:
        Mast, MastStory = self.load_mast_story()
        Mast.include_code = True
        story = MastStory()

        errors = story.from_file("story.mast", None) or []

        self.assertEqual([], errors)
        for label in [
            "khovan_reach_slice01_entry",
            "khovan_reach_slice01_bootstrap",
            "khovan_reach_initialize_playable_bootstrap",
        ]:
            self.assertIn(label, story.labels)

    def test_active_startup_mast_omits_known_bad_artemis_ship_name_identifier(self) -> None:
        startup_files = [
            ROOT / "story.mast",
            ROOT / "scripts" / "main.mast",
            ROOT / "scripts" / "systems" / "playable_bootstrap.mast",
        ]
        hits = [
            path.relative_to(ROOT).as_posix()
            for path in startup_files
            if "artemis_ship_name" in path.read_text(encoding="utf-8")
        ]
        self.assertEqual([], hits)

    def test_slice01a_bootstrap_uses_reference_backed_spawn_pattern(self) -> None:
        playable = (ROOT / "scripts" / "systems" / "playable_bootstrap.mast").read_text(
            encoding="utf-8"
        )
        self.assertIn("sim_create()", playable)
        self.assertIn('player_spawn(0, 0, 0, "Artemis", "tsn", "tsn_battle_cruiser")', playable)
        self.assertIn("assign_client_to_ship(0, artemis_id)", playable)
        self.assertNotIn("artemis_ship_name", playable)


if __name__ == "__main__":
    unittest.main()
