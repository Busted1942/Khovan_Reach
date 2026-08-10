#!/usr/bin/env python3
"""Static checks for Slice 07B - Halcyon Drift arrival, and the shared cleanup helper.

The packet calls spawn/cleanup "the highest-reuse code in the remaining build"
and warns that a defect here propagates to the cache, the pirates, and combat.
These checks concentrate on that: idempotent spawn, complete cleanup, and the
deferred-destroy guard that Slice 06 paid several live sessions to find.

None of it proves live behavior. Duplicate spawn in particular can only be
disproven by running JUMP-013 twice in Cosmos and counting contacts.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HALCYON_PATH = "scripts/acts/act2_halcyon_arrival.mast"
CLEANUP_LIB_PATH = "scripts/lib/entity_cleanup_helpers.mast"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def code_only(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))


def label_body(text: str, label: str) -> str:
    match = re.search(
        rf"^=== {re.escape(label)} ===(?P<body>.*?)(?=^=== |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing label: {label}")
    return match.group("body")


class CleanupHelperLibrary(unittest.TestCase):
    """scripts/lib/ exists at last; this is its first resident."""

    def test_helper_exists_and_is_imported_before_act_files(self) -> None:
        self.assertTrue((ROOT / CLEANUP_LIB_PATH).is_file())
        main = read("scripts/main.mast")
        self.assertIn(f"import {CLEANUP_LIB_PATH}", main)
        # Helpers must be defined before the act files that call them.
        lib_index = main.index(f"import {CLEANUP_LIB_PATH}")
        act_index = main.index("import scripts/acts/")
        self.assertLess(lib_index, act_index, "lib imports must precede act imports")

    def test_helper_owns_no_shared_state(self) -> None:
        """Extraction plan rule 2: a helper with its own state is a singleton.

        Two pirates need this routine at once in Slice 11; state here would make
        that impossible.
        """
        lib = read(CLEANUP_LIB_PATH)
        declared = re.findall(r"^shared (\w+)", lib, re.MULTILINE)
        self.assertEqual([], declared, f"helper must own no shared state, found {declared}")

    def test_helper_takes_everything_by_parameter(self) -> None:
        body = label_body(read(CLEANUP_LIB_PATH), "khovan_entity_cleanup_despawn_contact")
        for param in ["cleanup_object_id", "cleanup_navproxy_id", "cleanup_owner"]:
            self.assertIn(f"default {param}", body)

    def test_helper_clears_all_three_selections_before_deleting(self) -> None:
        """A console still selecting a deleted object is the Slice 04 empty-panel class."""
        body = label_body(read(CLEANUP_LIB_PATH), "khovan_entity_cleanup_despawn_contact")
        for call in [
            "set_science_selection(artemis_id, 0)",
            "set_comms_selection(artemis_id, 0)",
            "set_weapons_selection(artemis_id, 0)",
        ]:
            self.assertIn(call, body)
        self.assertLess(
            body.index("set_weapons_selection(artemis_id, 0)"),
            body.index("sbs.delete_object(cleanup_object_id)"),
            "selections must be cleared before the object is deleted",
        )

    def test_helper_guards_artemis_id_before_selection_calls(self) -> None:
        body = label_body(read(CLEANUP_LIB_PATH), "khovan_entity_cleanup_despawn_contact")
        self.assertIn("if artemis_id != 0:", body)

    def test_helper_drops_navproxy_before_object(self) -> None:
        body = label_body(read(CLEANUP_LIB_PATH), "khovan_entity_cleanup_despawn_contact")
        self.assertLess(
            body.index("sim.delete_navproxy_by_id(cleanup_navproxy_id)"),
            body.index("sbs.delete_object(cleanup_object_id)"),
        )


class HalcyonSpawnIsIdempotent(unittest.TestCase):
    """The packet's headline acceptance criterion: repeat JUMP-013 must not stack."""

    def test_spawn_has_both_a_flag_guard_and_a_role_query(self) -> None:
        """Two guards catch different failures.

        The flag catches a second call in one run. The role query catches a
        contact that outlived a seed the flag knew nothing about.
        """
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        self.assertIn("if halcyon_spawned:", body)
        self.assertIn('to_object_list(role("khovan_halcyon_drift"))', body)
        self.assertIn("if len(existing_halcyon) > 0:", body)

    def test_spawn_checks_the_returned_id(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        self.assertIn("if halcyon_object_id == 0:", body)
        self.assertIn("halcyon_contact_fallback_available = True", body)

    def test_spawn_guards_artemis_before_using_its_position(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        self.assertIn("if artemis_id == 0:", body)
        self.assertIn("if artemis_object is None:", body)

    def test_jump_013_cleans_up_before_seeding(self) -> None:
        """Repeat jumps stacking contacts is the failure this ordering prevents."""
        body = label_body(read(HALCYON_PATH), "khovan_act2_story_jump_seed_halcyon_arrival")
        self.assertIn("task_schedule(khovan_halcyon_cleanup)", body)
        self.assertIn("task_schedule(khovan_halcyon_spawn)", body)
        self.assertLess(
            body.index("task_schedule(khovan_halcyon_cleanup)"),
            body.index("task_schedule(khovan_halcyon_spawn)"),
            "cleanup must run before the seed spawns a new contact",
        )


class DeferredDestroyGuard(unittest.TestCase):
    """Slice 06 confirmed live that delete_object() fires //damage/destroy, deferred."""

    def test_destroy_handler_distinguishes_cleanup_from_a_kill(self) -> None:
        halcyon = read(HALCYON_PATH)
        self.assertIn('//damage/destroy if has_role(DESTROYED_ID, "khovan_halcyon_drift")', halcyon)
        self.assertIn("if halcyon_cleanup_in_progress:", halcyon)
        self.assertIn('halcyon_destruction_source = "cleanup"', halcyon)
        self.assertIn('halcyon_destruction_source = "genuine_destruction"', halcyon)

    def test_cleanup_sets_the_flag_and_does_not_clear_it(self) -> None:
        """Clearing at the call site is the exact bug fixed live on 2026-08-08.

        The destroy hook is deferred, so the flag must survive until the handler
        reads it. The handler owns the clear.
        """
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_cleanup")
        self.assertIn("halcyon_cleanup_in_progress = True", body)
        self.assertNotIn(
            "halcyon_cleanup_in_progress = False",
            body,
            "the destroy handler clears this flag, never the cleanup routine",
        )


class HalcyonRoutesAndDeployment(unittest.TestCase):
    def test_scan_and_hail_routes_exist_and_are_duplicate_suppressed(self) -> None:
        halcyon = read(HALCYON_PATH)
        self.assertIn('//science if has_roles(SCIENCE_SELECTED_ID, "khovan_halcyon_drift")', halcyon)
        self.assertIn('//comms if has_roles(COMMS_SELECTED_ID, "khovan_halcyon_drift")', halcyon)
        self.assertIn("if halcyon_scan_observed:", label_body(halcyon, "khovan_halcyon_scan"))
        self.assertIn("if halcyon_hail_observed:", label_body(halcyon, "khovan_halcyon_hail"))

    def test_comms_route_opens_with_a_statement(self) -> None:
        """Kestrel's option block was statement-less and rendered nothing live.

        Every //comms block confirmed to render in this repo opens with at least
        one statement, so new blocks match that shape.
        """
        halcyon = read(HALCYON_PATH)
        block = halcyon[halcyon.index('//comms if has_roles(COMMS_SELECTED_ID, "khovan_halcyon_drift")'):]
        block = block[: block.index("\n\n")]
        first = [l.strip() for l in block.splitlines()[1:] if l.strip()][0]
        self.assertFalse(first.startswith("+"), "block must not open with an option line")

    def test_deployment_sets_the_placement_slice09_reads(self) -> None:
        """Slice 09 chooses extended vs compressed timer from engineering_placement.

        The packet pins these exact strings, so Slice 09's packet stays valid.
        """
        halcyon = read(HALCYON_PATH)
        deploy = label_body(halcyon, "khovan_halcyon_authorize_deployment")
        self.assertIn('engineering_placement = "aboard_halcyon"', deploy)
        self.assertIn("damcon_deployed = True", deploy)
        recall = label_body(halcyon, "khovan_halcyon_recall_engineering")
        self.assertIn('engineering_placement = "returned_to_artemis"', recall)

    def test_deployment_is_gated_on_the_hail(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_authorize_deployment")
        self.assertIn("if not halcyon_hail_observed:", body)

    def test_checkpoint_is_written_on_arrival(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        self.assertIn('last_checkpoint = "post_halcyon_arrival"', body)


class Slice07BScope(unittest.TestCase):
    def test_later_slice_content_is_absent(self) -> None:
        halcyon = code_only(read(HALCYON_PATH))
        for forbidden in [
            "shared cascade",
            "shared damcon_timer",
            "shared halcyon_repair",
            "suit_o2",
            "=== khovan_hessler_",
        ]:
            self.assertNotIn(forbidden, halcyon, f"{forbidden} belongs to a later slice")

    def test_quick_suite_includes_slice07b_checks(self) -> None:
        runner = read("run_tests.py")
        self.assertIn('ROOT / "tests" / "test_act2_halcyon_arrival_static.py"', runner)


if __name__ == "__main__":
    unittest.main()
