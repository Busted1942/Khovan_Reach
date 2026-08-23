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

    def test_slice01b_bootstrap_uses_reference_owned_spawn_lifecycle(self) -> None:
        main = (ROOT / "scripts" / "main.mast").read_text(encoding="utf-8")
        playable = (ROOT / "scripts" / "systems" / "playable_bootstrap.mast").read_text(
            encoding="utf-8"
        )
        self.assertIn("await task_schedule(spawn_players)", main)
        self.assertIn('role("__player__") & role("tsn")', playable)
        self.assertIn("shared artemis_id = artemis_object.id", playable)
        self.assertNotIn("sim_create()", playable)
        self.assertNotIn("player_spawn(", playable)
        self.assertNotIn("assign_client_to_ship", playable)
        self.assertNotIn("artemis_ship_name", playable)

    def test_gui_body_interpolation_never_references_an_undeclared_shared(self) -> None:
        """Cookbook 17.13: a declaration pruner cannot see `% {var}`.

        masttools MAST019 counts expression-position references and does not
        count substitution inside a `<<[...]` GUI body, so on 2026-08-23 it
        commented out `tarsis_docking_rejection_text` while its only use site
        still read it. Compile preflight does not close this either - an
        undefined name in a GUI body faults at render, not at parse.

        Scoped to `% {name}` deliberately. A bare `{name}` appears inside
        f-strings and format specifiers all over the runtime, and widening
        this to cover those would flag task-local names and produce the
        cry-wolf failure mode 17.6 warns about.
        """
        import re

        mast_files = sorted((ROOT / "scripts").rglob("*.mast"))
        self.assertTrue(mast_files, "no runtime .mast files found")

        declared: set[str] = set()
        for path in mast_files:
            for line in path.read_text(encoding="utf-8").splitlines():
                match = re.match(r"\s*shared\s+([A-Za-z_]\w*)\s*=", line)
                if match:
                    declared.add(match.group(1))

        dangling: list[str] = []
        for path in mast_files:
            rel = path.relative_to(ROOT).as_posix()
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if line.lstrip().startswith("#"):
                    continue
                for name in re.findall(r"%\s*\{\s*([A-Za-z_]\w*)\s*\}", line):
                    if name not in declared:
                        dangling.append(f"{rel}:{number}: % {{{name}}}")

        self.assertEqual(
            [],
            dangling,
            "GUI-body interpolation references a name with no `shared` "
            "declaration; a pruning pass most likely removed it - see "
            "cookbook 17.13",
        )

    def test_act2_jump_reset_clears_its_barrier_before_it_can_bail(self) -> None:
        """Cookbook 5.2: reset the published status flag first, fail closed.

        `khovan_halcyon_reset_for_act2_jump` restores a deployed DAMCON team
        before running its cleanup barrier and bails if that restore fails.
        Two guards in act2_pivot.mast read `halcyon_cleanup_barrier_status` to
        decide whether the reset actually ran, so if the bail path leaves the
        previous jump's "settled" in place, a later jump proceeds on evidence
        produced by a different jump entirely.
        """
        import re

        halcyon = (
            ROOT / "scripts" / "acts" / "act2_halcyon_arrival.mast"
        ).read_text(encoding="utf-8")
        match = re.search(
            r"^=== khovan_halcyon_reset_for_act2_jump ===(?P<body>.*?)(?=^=== |\Z)",
            halcyon,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, "missing khovan_halcyon_reset_for_act2_jump")
        body = match.group("body")

        reset = body.find('halcyon_cleanup_barrier_status = "not_run"')
        self.assertNotEqual(
            -1,
            reset,
            "the reset must clear halcyon_cleanup_barrier_status - cookbook 5.2",
        )
        first_bail = body.find("->END")
        self.assertNotEqual(-1, first_bail, "expected at least one bail path")
        self.assertLess(
            reset,
            first_bail,
            "halcyon_cleanup_barrier_status is reset after a path that can "
            "already have bailed; a stale 'settled' then reads as consent - "
            "cookbook 5.2",
        )

        pivot = (ROOT / "scripts" / "acts" / "act2_pivot.mast").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            'if halcyon_cleanup_barrier_status != "settled":',
            pivot,
            "no downstream guard reads the flag; if the consumer moved, "
            "re-point this regression rather than deleting it",
        )


if __name__ == "__main__":
    unittest.main()
