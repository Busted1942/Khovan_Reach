#!/usr/bin/env python3
"""Self-tests for tools/review_gate.py.

A review gate with a wrong regex is worse than no gate: it either waves
violations through (silent) or cries wolf on good code until reviewers stop
reading it (loud, then silent). Both directions are tested here — every check
gets a violating fixture AND a clean fixture, because a pattern that flags
everything passes a violation-only test suite.

Fixtures are synthetic MAST-shaped text, not the real mission files. Pinning
these tests to live runtime files would make them fail whenever the mission
changes, which is a different check than "does the pattern work".
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE_PATH = ROOT / "tools" / "review_gate.py"


def load_gate():
    spec = importlib.util.spec_from_file_location("review_gate", GATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {GATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gate = load_gate()


def all_lines(text: str) -> set[int]:
    return set(range(1, len(text.splitlines()) + 1))


class ReviewGateFileExists(unittest.TestCase):
    def test_gate_script_present(self):
        self.assertTrue(
            GATE_PATH.is_file(),
            "tools/review_gate.py is referenced by the handoff protocol section 5.4",
        )


class LabelParsing(unittest.TestCase):
    SAMPLE = "\n".join(
        [
            "shared thing = 0",  # 1
            "=== label_one ===",  # 2
            "    do_a()",  # 3
            "=== label_two ===",  # 4
            "    do_b()",  # 5
            "    do_c()",  # 6
        ]
    )

    def test_blocks_span_to_next_label(self):
        blocks = gate.label_blocks(self.SAMPLE)
        self.assertEqual(blocks, [("label_one", 2, 3), ("label_two", 4, 6)])

    def test_line_maps_to_owning_label(self):
        blocks = gate.label_blocks(self.SAMPLE)
        self.assertEqual(gate.block_for_line(blocks, 5)[0], "label_two")

    def test_line_before_first_label_has_no_block(self):
        blocks = gate.label_blocks(self.SAMPLE)
        self.assertIsNone(gate.block_for_line(blocks, 1))


class ToObjectNoneCheck(unittest.TestCase):
    def test_chained_call_is_flagged(self):
        text = "    roles = to_object(station_id).get_roles()\n"
        self.assertEqual(len(gate.analyze_to_object("f.mast", text, all_lines(text))), 1)

    def test_assignment_without_none_check_is_flagged(self):
        text = "\n".join(
            [
                "    beacon = to_object(station_id)",
                "    beacon.pos = Vec3(1, 2, 3)",
            ]
        )
        failures = gate.analyze_to_object("f.mast", text, all_lines(text))
        self.assertEqual(len(failures), 1)
        self.assertIn("beacon", failures[0])

    def test_assignment_with_is_none_check_is_clean(self):
        text = "\n".join(
            [
                "    beacon = to_object(station_id)",
                "    if beacon is None:",
                "        ->END",
            ]
        )
        self.assertEqual(gate.analyze_to_object("f.mast", text, all_lines(text)), [])

    def test_assignment_with_is_not_none_check_is_clean(self):
        text = "\n".join(
            [
                "    artemis_object = to_object(artemis_id)",
                "    if artemis_object is not None:",
                "        artemis_object.pos = Vec3(0, 0, 0)",
            ]
        )
        self.assertEqual(gate.analyze_to_object("f.mast", text, all_lines(text)), [])

    def test_to_object_list_is_not_matched(self):
        """to_object_list() returns a list and has different semantics.

        The two names share a prefix, so a sloppy pattern flags every
        to_object_list() call in the repo.
        """
        text = "    existing = to_object_list(role('tarsis_station'))\n"
        self.assertEqual(gate.analyze_to_object("f.mast", text, all_lines(text)), [])

    def test_unchanged_lines_are_not_scanned(self):
        """Diff scoping is the mechanism that keeps accepted debt from failing."""
        text = "    beacon = to_object(station_id)\n    beacon.pos = 1\n"
        self.assertEqual(gate.analyze_to_object("f.mast", text, set()), [])


class ArtemisIdGuard(unittest.TestCase):
    def test_unguarded_ship_api_call_is_flagged(self):
        text = "\n".join(
            [
                "=== khovan_do_thing ===",
                "    artemis_object = to_object(artemis_id)",
            ]
        )
        failures = gate.analyze_artemis_guards("f.mast", text, all_lines(text))
        self.assertEqual(len(failures), 1)
        self.assertIn("khovan_do_thing", failures[0])

    def test_guard_in_same_label_is_clean(self):
        text = "\n".join(
            [
                "=== khovan_do_thing ===",
                "    if artemis_id == 0:",
                "        ->END",
                "    artemis_object = to_object(artemis_id)",
            ]
        )
        self.assertEqual(gate.analyze_artemis_guards("f.mast", text, all_lines(text)), [])

    def test_compound_guard_is_clean(self):
        text = "\n".join(
            [
                "=== khovan_do_thing ===",
                "    if artemis_id == 0 or drone_01_target_id == 0:",
                "        ->END",
                "    drone_range = sbs.distance_id(artemis_id, drone_01_target_id)",
            ]
        )
        self.assertEqual(gate.analyze_artemis_guards("f.mast", text, all_lines(text)), [])

    def test_guard_in_a_different_label_does_not_protect(self):
        text = "\n".join(
            [
                "=== khovan_guarded ===",
                "    if artemis_id == 0:",
                "        ->END",
                "=== khovan_unguarded ===",
                "    artemis_object = to_object(artemis_id)",
            ]
        )
        failures = gate.analyze_artemis_guards("f.mast", text, all_lines(text))
        self.assertEqual(len(failures), 1)
        self.assertIn("khovan_unguarded", failures[0])

    def test_non_api_mentions_are_not_flagged(self):
        """Assignments and comparisons are not ship API calls.

        act1_generator_tarsis_gate.mast has 33 artemis_id mentions and 4
        guards; flagging every mention would make the check useless.
        """
        text = "\n".join(
            [
                "=== khovan_do_thing ===",
                "    shared artemis_id = 0",
                "    if artemis_id != 0:",
                "        status = 'ready'",
                "    trace = f'id={artemis_id}'",
            ]
        )
        self.assertEqual(gate.analyze_artemis_guards("f.mast", text, all_lines(text)), [])

    def test_one_report_per_label(self):
        text = "\n".join(
            [
                "=== khovan_do_thing ===",
                "    a = to_object(artemis_id)",
                "    b = sbs.distance_id(artemis_id, other_id)",
            ]
        )
        self.assertEqual(len(gate.analyze_artemis_guards("f.mast", text, all_lines(text))), 1)


class RunIdGuard(unittest.TestCase):
    DELAYED_UNGUARDED = "\n".join(
        [
            "=== khovan_delayed ===",
            "    sequence_run_id = sequence_run_id + 1",
            "    await delay_sim(seconds=1)",
            "    await task_schedule(khovan_respawn)",
        ]
    )
    DELAYED_GUARDED = "\n".join(
        [
            "=== khovan_delayed ===",
            "    default hold_run_id = drone_01_stationary_hold_run_id",
            "    if hold_run_id != drone_01_stationary_hold_run_id:",
            "        ->END",
            "    await delay_sim(seconds=1)",
        ]
    )
    IMMEDIATE = "\n".join(
        [
            "=== khovan_immediate ===",
            "    status = 'done'",
        ]
    )

    def test_delayed_target_without_guard_is_flagged(self):
        caller = "    await task_schedule(khovan_delayed)\n"
        index = {"khovan_delayed": self.DELAYED_UNGUARDED}
        failures = gate.analyze_run_id("f.mast", caller, all_lines(caller), index)
        self.assertEqual(len(failures), 1)
        self.assertIn("khovan_delayed", failures[0])

    def test_incrementing_a_run_id_is_not_a_guard(self):
        """Bumping the counter then yielding still resumes unguarded."""
        index = {"khovan_delayed": self.DELAYED_UNGUARDED}
        caller = "    await task_schedule(khovan_delayed)\n"
        failures = gate.analyze_run_id("f.mast", caller, all_lines(caller), index)
        self.assertTrue(failures, "a bare run_id increment must not satisfy the check")

    def test_delayed_target_with_guard_is_clean(self):
        caller = "    task_schedule(khovan_delayed, {'hold_run_id': x})\n"
        index = {"khovan_delayed": self.DELAYED_GUARDED}
        self.assertEqual(gate.analyze_run_id("f.mast", caller, all_lines(caller), index), [])

    def test_immediate_target_needs_no_guard(self):
        """Labels that never yield cannot be invalidated by a story jump."""
        caller = "    await task_schedule(khovan_immediate)\n"
        index = {"khovan_immediate": self.IMMEDIATE}
        self.assertEqual(gate.analyze_run_id("f.mast", caller, all_lines(caller), index), [])

    BOUNDED_OBSERVER = "\n".join(
        [
            "=== khovan_watch_tick ===",
            "    if engineering_no_motion_confirmed:",
            "        ->END",
            "    engineering_no_motion_observer_ticks = engineering_no_motion_observer_ticks + 1",
            "    if engineering_no_motion_observer_ticks >= 20:",
            "        engineering_no_motion_fallback_available = True",
            "        ->END",
            "    await delay_sim(seconds=1)",
            "    jump khovan_watch_tick",
        ]
    )
    UNBOUNDED_OBSERVER = "\n".join(
        [
            "=== khovan_watch_tick ===",
            "    engineering_no_motion_observer_ticks = engineering_no_motion_observer_ticks + 1",
            "    await delay_sim(seconds=1)",
            "    jump khovan_watch_tick",
        ]
    )

    def test_bounded_observer_needs_no_run_id(self):
        """Cookbook 5.2 observers invalidate on state plus a tick ceiling.

        Flagging these was a real false positive against three live observers in
        act1_engineering_shakedown.mast.
        """
        caller = "    task_schedule(khovan_watch_tick)\n"
        index = {"khovan_watch_tick": self.BOUNDED_OBSERVER}
        self.assertEqual(gate.analyze_run_id("f.mast", caller, all_lines(caller), index), [])

    def test_tick_counter_without_a_ceiling_is_still_flagged(self):
        """A counter with no ceiling is an unbounded loop, not the 5.2 pattern."""
        caller = "    task_schedule(khovan_watch_tick)\n"
        index = {"khovan_watch_tick": self.UNBOUNDED_OBSERVER}
        self.assertTrue(gate.analyze_run_id("f.mast", caller, all_lines(caller), index))

    RECHECKS_AFTER = "\n".join(
        [
            "=== khovan_watch_rest ===",
            "    if damcon_rest_cycle_confirmed:",
            "        ->END",
            "    await delay_sim(seconds=8)",
            "    if not damcon_rest_cycle_confirmed:",
            "        damcon_rest_cycle_fallback_available = True",
            "    ->END",
        ]
    )
    GUARDS_ONLY_BEFORE = "\n".join(
        [
            "=== khovan_watch_rest ===",
            "    if damcon_rest_cycle_confirmed:",
            "        ->END",
            "    await delay_sim(seconds=8)",
            "    damcon_rest_cycle_fallback_available = True",
            "    ->END",
        ]
    )

    def test_recheck_after_the_delay_is_accepted(self):
        caller = "    task_schedule(khovan_watch_rest)\n"
        index = {"khovan_watch_rest": self.RECHECKS_AFTER}
        self.assertEqual(gate.analyze_run_id("f.mast", caller, all_lines(caller), index), [])

    def test_guarding_only_before_the_delay_is_still_flagged(self):
        """The khovan_drone_01_reset bug: guards before the yield prove nothing."""
        caller = "    task_schedule(khovan_watch_rest)\n"
        index = {"khovan_watch_rest": self.GUARDS_ONLY_BEFORE}
        self.assertTrue(gate.analyze_run_id("f.mast", caller, all_lines(caller), index))

    def test_unknown_target_is_not_flagged(self):
        caller = "    await task_schedule(khovan_from_another_file)\n"
        self.assertEqual(gate.analyze_run_id("f.mast", caller, all_lines(caller), {}), [])


class SpawnExistenceAndCleanup(unittest.TestCase):
    def test_spawn_without_check_or_cleanup_is_flagged(self):
        text = "    drone = npc_spawn(1, 2, 3, 'D', 'r', 'h', 'b')\n"
        failures = gate.analyze_spawn("f.mast", text, all_lines(text))
        self.assertEqual(len(failures), 2)

    def test_spawn_with_check_and_cleanup_is_clean(self):
        text = "\n".join(
            [
                "    drone_target = npc_spawn(1, 2, 3, 'D', 'r', 'h', 'b')",
                "    if drone_target_id == 0:",
                "        ->END",
                "=== khovan_cleanup ===",
                "    sbs.delete_object(drone_target_id)",
            ]
        )
        self.assertEqual(gate.analyze_spawn("f.mast", text, all_lines(text)), [])

    def test_file_without_spawn_is_ignored(self):
        text = "    status = 'idle'\n"
        self.assertEqual(gate.analyze_spawn("f.mast", text, all_lines(text)), [])


class BootstrapApis(unittest.TestCase):
    def test_forbidden_api_is_flagged(self):
        text = "    sim_create(1)\n"
        self.assertEqual(len(gate.analyze_bootstrap_apis("f.mast", text, all_lines(text))), 1)

    def test_ordinary_line_is_clean(self):
        text = "    npc_spawn(1, 2, 3, 'D', 'r', 'h', 'b')\n"
        self.assertEqual(gate.analyze_bootstrap_apis("f.mast", text, all_lines(text)), [])


class ProtectedDocsAndNames(unittest.TestCase):
    def test_unratified_design_doc_change_is_flagged(self):
        # A path that does not exist on disk reads as empty text, so it carries
        # no ratification marker - the unratified case.
        failures, notes = gate.check_protected_docs(["docs/01_design/99_not_a_real_doc.md"])
        self.assertEqual(len(failures), 1)
        self.assertEqual(notes, [])

    def test_unratified_content_doc_change_is_flagged(self):
        failures, notes = gate.check_protected_docs(["docs/02_content/99_not_a_real_doc.md"])
        self.assertEqual(len(failures), 1)
        self.assertEqual(notes, [])

    def test_ratified_design_doc_change_is_a_note_not_a_failure(self):
        # 10_mast_requirements.md carries a dated operator-ratification note in
        # section 17. A ratified edit must not fail the gate forever.
        failures, notes = gate.check_protected_docs(["docs/01_design/10_mast_requirements.md"])
        self.assertEqual(failures, [])
        self.assertEqual(len(notes), 1)

    def test_ratification_marker_must_be_dated(self):
        self.assertIsNone(gate.RATIFIED_RE.search("this was operator-ratified at some point"))
        self.assertIsNotNone(gate.RATIFIED_RE.search("(operator-ratified 2026-08-08)"))

    def test_implementation_docs_are_allowed(self):
        failures, notes = gate.check_protected_docs(
            ["docs/04_implementation_setup/70_agent_handoff_protocol.md", "scripts/main.mast"]
        )
        self.assertEqual(failures, [])
        self.assertEqual(notes, [])

    def test_parallel_filename_is_flagged(self):
        failures = gate.check_forbidden_filenames(["scripts/acts/act1_drone_final.mast"])
        self.assertEqual(len(failures), 1)

    def test_ordinary_filename_is_clean(self):
        self.assertEqual(
            gate.check_forbidden_filenames(["scripts/acts/act1_drone_contact_fire.mast"]),
            [],
        )


if __name__ == "__main__":
    unittest.main()
