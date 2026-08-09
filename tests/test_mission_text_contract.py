#!/usr/bin/env python3
"""Enforce the player-copy conventions instead of pinning the prose.

These tests replace a class of assertion that duplicated the exact wording in a
test file. Duplicated wording tests nothing except that two files agree, and it
turns every copy edit into a test-patching exercise.

What is asserted here is the house style itself, which no previous test checked
at all:

- the body opens with the addressee (cookbook 6.2)
- the body does not re-name its own sender, which the header already renders
- design/dev vocabulary does not reach a player console
- multi-recipient copy is one addressed line per recipient
- known past typos do not come back

Prose is deliberately not asserted. Reword freely; these tests only care that
the result still follows the conventions.
"""

from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


def _load_copy_contract():
    """Load the helper by path.

    run_tests.py loads each test file with importlib against an absolute path,
    so `tests/` is never on sys.path and a bare `import copy_contract` fails
    there while succeeding when the file is run directly from `tests/`. Same
    approach test_review_gate_static.py uses for the gate module.
    """
    helper = Path(__file__).resolve().parent / "mission_text.py"
    spec = importlib.util.spec_from_file_location("mission_text", helper)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {helper}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cc = _load_copy_contract()


class AddresseeConvention(unittest.TestCase):
    def test_player_copy_opens_with_an_addressee(self):
        """Cookbook 6.2: "Artemis - <Station>: ..." """
        offenders = []
        for name, (path, value) in sorted(cc.all_player_copy().items()):
            if name in cc.NOT_ADDRESSED_TO_CREW:
                continue
            if not value.strip():
                continue
            if not cc.ADDRESSEE_RE.match(value):
                offenders.append(f"{path}: {name} -> {value[:70]!r}")
        self.assertEqual(
            [],
            offenders,
            "player copy must open with 'Artemis - <Station>:' "
            "(or be listed in copy_contract.NOT_ADDRESSED_TO_CREW with a reason):\n"
            + "\n".join(offenders),
        )

    def test_player_copy_does_not_repeat_its_own_sender(self):
        """comms_receive renders the sender; naming it again prints it twice.

        This is the same duplication that produced "Dillon: Dillon" headers.
        """
        offenders = []
        for name, (path, value) in sorted(cc.all_player_copy().items()):
            if name in cc.SENDER_NAME_ALLOWED:
                continue
            if name in cc.NOT_ADDRESSED_TO_CREW:
                continue
            head = value.split(":", 1)[0]
            if head.startswith("Artemis - "):
                continue
            if ":" in value and re.match(
                r"^(Tarsis|Kestrel|Dillon|Training)\b", head
            ):
                offenders.append(f"{path}: {name} -> {head!r}")
        self.assertEqual(
            [],
            offenders,
            "copy must not open by naming its own sender - the message header "
            "already shows it:\n" + "\n".join(offenders),
        )

    def test_every_addressed_line_names_a_recipient(self):
        """Multi-recipient copy is one addressed line each, not a run-on."""
        offenders = []
        for name, (path, value) in sorted(cc.all_player_copy().items()):
            if name in cc.NOT_ADDRESSED_TO_CREW or "\\n" not in value:
                continue
            for line in value.split("\\n"):
                if not cc.ADDRESSEE_RE.match(line.strip()):
                    offenders.append(f"{path}: {name} -> {line[:60]!r}")
        self.assertEqual([], offenders, "\n".join(offenders))


class NoDesignLanguageOnPlayerConsoles(unittest.TestCase):
    """Dev vocabulary reaching a player console was a real, repeated defect."""

    FORBIDDEN = [
        "fallback confirmation",
        "no failure state",
        "damage observer",
        "live_smoke",
        "unproven",
        "GM mark",
        "detection mode",
        "refresh their comms panel",
        "objective_id",
    ]

    def test_no_design_vocabulary_in_player_copy(self):
        offenders = []
        for name, (path, value) in sorted(cc.all_player_copy().items()):
            if name == "scenario_control_panel_overview_text":
                continue  # GM-facing
            low = value.lower()
            for phrase in self.FORBIDDEN:
                if phrase.lower() in low:
                    offenders.append(f"{path}: {name} contains {phrase!r}")
        self.assertEqual([], offenders, "\n".join(offenders))


class NoRegressionOfFixedTypos(unittest.TestCase):
    """Sixteen of these were shipping to player consoles before 2026-08-09."""

    TYPOS = [
        "Captin", "Impuse", "stabilze", "captian", "lesiure", "extreamly",
        "preassure", "Manuver", "Maneyver", "shaekdown", "trasfer", "Reqquest",
        "clearnece", "recieved", "parsets", "severly", "Conform Combat",
    ]

    def test_known_typos_do_not_return(self):
        offenders = []
        for path in cc.mast_files():
            text = path.read_text(encoding="utf-8")
            for typo in self.TYPOS:
                if typo in text:
                    rel = path.relative_to(cc.ROOT).as_posix()
                    offenders.append(f"{rel}: {typo!r}")
        self.assertEqual([], offenders, "\n".join(offenders))


class HelperBehaviour(unittest.TestCase):
    """The helper has to be trustworthy or the tests above mean nothing."""

    def test_copy_value_reads_the_live_runtime_value(self):
        value = cc.copy_value("damcon_rest_cycle_text")
        self.assertTrue(value.startswith("Artemis - "))

    def test_missing_variable_fails_loudly(self):
        with self.assertRaises(AssertionError):
            cc.copy_value("no_such_copy_variable_text")

    def test_copy_lines_splits_on_the_literal_escape(self):
        lines = cc.copy_lines("controlled_damage_logged_text")
        self.assertEqual(2, len(lines))
        self.assertTrue(all(line.startswith("Artemis - ") for line in lines))


if __name__ == "__main__":
    unittest.main()
