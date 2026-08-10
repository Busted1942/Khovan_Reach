#!/usr/bin/env python3
"""Static checks for Slice 07A - Act II pivot.

These prove wiring, guards, and packet scope. They cannot prove that Anderson's
message renders, that the Comms route appears, or that the handoff observer
fires - all of that needs live Cosmos, and Slice 06 already demonstrated that a
GM-console-only smoke does not prove a crewed station route.

Player-facing copy is deliberately not pinned here; tests/test_mission_text_contract.py
enforces the conventions and lets the wording change freely.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACT2_PATH = "scripts/acts/act2_pivot.mast"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def code_only(text: str) -> str:
    """Strip MAST comment lines.

    This file's comments cite the packet's own "Do not implement" list by name,
    so a scope assertion that scanned comments would trip on the documentation
    of the very thing it forbids.
    """
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


class Slice07AWiring(unittest.TestCase):
    def test_module_exists_imports_and_initializes_after_slice06(self) -> None:
        self.assertTrue((ROOT / ACT2_PATH).is_file())
        main = read("scripts/main.mast")
        self.assertIn(f"import {ACT2_PATH}", main)
        self.assertIn("await task_schedule(khovan_act2_initialize_pivot)", main)

        # Act II init must follow Slice 06 init - it polls a flag Slice 06 owns.
        drone_index = main.index("await task_schedule(khovan_act1_initialize_drone_contact_fire)")
        act2_index = main.index("await task_schedule(khovan_act2_initialize_pivot)")
        playable_index = main.index("await task_schedule(khovan_reach_initialize_playable_bootstrap)")
        self.assertLess(drone_index, act2_index)
        self.assertLess(act2_index, playable_index)

    def test_packet_state_variables_exist(self) -> None:
        act2 = read(ACT2_PATH)
        for name in [
            "act2_pivot_initialized",
            "act2_pivot_status",
            "act2_last_progression_summary",
            "anderson_orders_delivered",
            "anderson_clip_1_stub_sent",
            "anderson_orders_text",
            "anderson_orders_ack_status",
            "distress_signal_detected",
            "distress_localized",
            "distress_localization_status",
            "distress_science_gate_status",
            "distress_localization_fallback_available",
            "dillon_clip_8_stub_sent",
        ]:
            self.assertIn(f"shared {name}", act2, f"packet names {name}")

    def test_act2_owns_the_phase_transition_alone(self) -> None:
        """Runtime owner model: no other file writes mission_phase = act_2."""
        offenders = []
        for path in sorted((ROOT / "scripts").rglob("*.mast")):
            rel = path.relative_to(ROOT).as_posix()
            if rel == ACT2_PATH:
                continue
            body = code_only(path.read_text(encoding="utf-8"))
            if 'mission_phase = "act_2"' in body:
                offenders.append(rel)
        self.assertEqual([], offenders, "only act2_pivot.mast may enter Act II")


class Slice07AGuards(unittest.TestCase):
    def test_pivot_is_gated_on_the_act1_handoff(self) -> None:
        body = label_body(read(ACT2_PATH), "khovan_act2_begin_pivot")
        self.assertIn("if not drone_contact_act2_ready:", body)
        # Duplicate suppression - the observer and JUMP-011 can both reach here.
        self.assertIn('if mission_phase == "act_2":', body)

    def test_pivot_invalidates_every_act1_run_id(self) -> None:
        """A stale Act I timer firing mid-Act-II is the hazard the packet names.

        Every run-ID counter declared in scripts/acts/act1_*.mast must be bumped,
        so adding an Act I timer without adding it here fails the build.
        """
        act2 = read(ACT2_PATH)
        body = label_body(act2, "khovan_act2_invalidate_act1_timers")
        declared = set()
        for path in sorted((ROOT / "scripts" / "acts").glob("act1_*.mast")):
            declared |= set(
                re.findall(r"^shared (\w*run_id)\b", path.read_text(encoding="utf-8"), re.MULTILINE)
            )
        self.assertTrue(declared, "expected Act I run-ID counters to exist")
        missing = sorted(name for name in declared if f"{name} = {name} + 1" not in body)
        self.assertEqual([], missing, f"Act I run-IDs not invalidated on pivot: {missing}")

    def test_handoff_observer_is_bounded_and_run_id_guarded(self) -> None:
        body = label_body(read(ACT2_PATH), "khovan_act2_watch_act1_handoff")
        self.assertIn("if handoff_run_id != act2_pivot_run_id:", body)
        self.assertIn("act2_handoff_observer_ticks >= 900", body)
        self.assertIn("jump khovan_act2_watch_act1_handoff", body)
        # Arming the fallback must not end the observer - same lesson as the
        # Slice 05 power-preset observer.
        self.assertGreater(
            body.index("jump khovan_act2_watch_act1_handoff"),
            body.index("act2_handoff_observer_ticks >= 900"),
        )

    def test_clips_are_duplicate_suppressed(self) -> None:
        act2 = read(ACT2_PATH)
        anderson = label_body(act2, "khovan_act2_deliver_anderson_orders")
        self.assertIn("if anderson_clip_1_stub_sent:", anderson)
        dillon = label_body(act2, "khovan_act2_deliver_dillon_pivot_note")
        self.assertIn("if dillon_clip_8_stub_sent:", dillon)

    def test_checkpoint_is_written_at_anderson_orders(self) -> None:
        body = label_body(read(ACT2_PATH), "khovan_act2_deliver_anderson_orders")
        self.assertIn('last_checkpoint = "post_anderson_orders"', body)

    def test_localization_routes_share_one_completion_label(self) -> None:
        """Both routes record which one fired - the Slice 05 observer/fallback shape."""
        act2 = read(ACT2_PATH)
        complete = label_body(act2, "khovan_act2_complete_distress_localization")
        self.assertIn("default localization_source", complete)
        self.assertIn("distress_localization_source = localization_source", complete)
        self.assertIn("if distress_localized:", complete)
        confirm = label_body(act2, "khovan_act2_confirm_distress_localization")
        self.assertIn('"localization_source": "comms_report_confirmation"', confirm)

    def test_messages_use_the_guarded_safe_wrapper(self) -> None:
        """Anderson is a new speaker; the packet names the Slice 04 black-box
        failure as precedent for message-surface problems."""
        act2 = code_only(read(ACT2_PATH))
        self.assertIn("khovan_reach_send_safe_startup_message", act2)
        self.assertIn('"startup_safe_breadcrumb"', act2)


class DistressProximitySweep(unittest.TestCase):
    """Operator intent: fly into the region and your sensors pick the signal up.

    Replaces the first version's Comms-reported fix. That was built because no
    contact object exists in Phase A - which is still true - but a seeded
    coordinate plus a distance check gives Science a real gate without Phase A
    owning a spawn it should not have.
    """

    def test_sweep_measures_distance_to_a_seeded_source(self) -> None:
        body = label_body(read(ACT2_PATH), "khovan_act2_watch_distress_proximity")
        self.assertIn("sweep_dx = artemis_object.pos.x - distress_source_x", body)
        self.assertIn("sweep_dz = artemis_object.pos.z - distress_source_z", body)

    def test_sweep_uses_squared_distance_not_sqrt(self) -> None:
        """math.* is unproven in MAST here; the squared form needs no module.

        act1_drone_contact_fire.mast's stationary-hold observer already uses
        this exact shape live.
        """
        act2 = code_only(read(ACT2_PATH))
        self.assertNotIn("math.", act2)
        body = label_body(act2, "khovan_act2_watch_distress_proximity")
        self.assertIn("distress_range_sq = sweep_dx * sweep_dx + sweep_dz * sweep_dz", body)
        self.assertIn("if distress_range_sq <= distress_detection_range_sq:", body)

    def test_sweep_is_bounded_and_run_id_guarded(self) -> None:
        body = label_body(read(ACT2_PATH), "khovan_act2_watch_distress_proximity")
        self.assertIn("if sweep_run_id != distress_sweep_run_id:", body)
        self.assertIn("distress_sweep_observer_ticks >= 600", body)
        self.assertIn("jump khovan_act2_watch_distress_proximity", body)

    def test_sweep_guards_artemis_before_reading_position(self) -> None:
        body = label_body(read(ACT2_PATH), "khovan_act2_watch_distress_proximity")
        self.assertIn("if artemis_id == 0:", body)
        self.assertIn("if artemis_object is None:", body)

    def test_comms_report_remains_as_the_fallback(self) -> None:
        """The automatic gate ships with its fallback - AGENTS.md section 4."""
        act2 = read(ACT2_PATH)
        self.assertIn("distress_localization_fallback_available = True", act2)
        self.assertIn('"localization_source": "comms_report_confirmation"', act2)
        self.assertIn('"localization_source": "automatic_proximity_sweep"', act2)


class LifeformRouting(unittest.TestCase):
    def test_dillon_and_anderson_speak_through_the_lifeform_helper(self) -> None:
        act2 = code_only(read(ACT2_PATH))
        self.assertIn("khovan_lifeform_send", act2)
        self.assertIn("dillon_lifeform_id", act2)

    def test_every_lifeform_send_carries_a_fallback_sender(self) -> None:
        """A character who cannot speak is mission-stopping; wrong sender id is cosmetic."""
        act2 = code_only(read(ACT2_PATH))
        sends = act2.count("task_schedule(khovan_lifeform_send")
        fallbacks = act2.count("send_fallback_sender_id")
        self.assertEqual(sends, fallbacks, "every lifeform send needs a fallback sender id")


class Slice07AScope(unittest.TestCase):
    """The packet's Do-Not-Implement list, asserted."""

    def test_phase_b_and_later_content_is_absent(self) -> None:
        """Assert the absence of IMPLEMENTATION, not of the words.

        A first version of this test forbade the substring "halcyon" and tripped
        on a status string that names Halcyon precisely to say Phase B owns it.
        Naming what is out of scope is how scope gets documented; the check has
        to distinguish that from building it.
        """
        act2 = code_only(read(ACT2_PATH))
        for forbidden in [
            "shared halcyon",
            "shared hessler",
            "shared cascade",
            "shared damcon_timer",
            "npc_spawn(",
            "shared engineering_deployed",
            "=== khovan_act2_halcyon",
            "sim.add_navproxy",
        ]:
            self.assertNotIn(forbidden, act2, f"{forbidden} is Phase B or later")

    def test_no_gui_or_player_facing_admin_routes(self) -> None:
        act2 = read(ACT2_PATH)
        self.assertNotIn("@gui", act2)
        self.assertNotIn("//gui", act2)

    def test_act1_files_were_not_modified_for_the_handoff(self) -> None:
        """The packet forbids Act I changes beyond timer invalidation hooks.

        The handoff is a poll from Act II precisely so Act I stays untouched.
        """
        for path in sorted((ROOT / "scripts" / "acts").glob("act1_*.mast")):
            body = code_only(path.read_text(encoding="utf-8"))
            self.assertNotIn(
                "khovan_act2_",
                body,
                f"{path.name} must not call into Act II",
            )


class Slice07AJumpPresets(unittest.TestCase):
    def test_jump_011_and_012_are_registered_and_dispatched(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        for jump_id, display in [
            ("anderson_orders", "JUMP-011 Anderson Orders"),
            ("distress_localized", "JUMP-012 Distress Localized"),
        ]:
            handler = f"khovan_story_jump_preset_{jump_id}"
            self.assertIn(f'+ "{display}" {handler}', story_jump)
            self.assertIn(f"=== {handler} ===", story_jump)
            self.assertIn(f'jump_id == "{jump_id}"', story_jump)
            self.assertIn(jump_id, story_jump)

    def test_seeds_invalidate_act1_timers(self) -> None:
        """A seeded jump must not leave a stale Act I timer running."""
        body = label_body(read(ACT2_PATH), "khovan_act2_story_jump_seed_anderson_orders")
        self.assertIn("task_schedule(khovan_act2_invalidate_act1_timers)", body)

    def test_localized_seed_builds_on_the_orders_seed(self) -> None:
        body = label_body(read(ACT2_PATH), "khovan_act2_story_jump_seed_distress_localized")
        self.assertIn("task_schedule(khovan_act2_story_jump_seed_anderson_orders)", body)
        self.assertIn("distress_localized = True", body)

    def test_quick_suite_includes_slice07a_checks(self) -> None:
        runner = read("run_tests.py")
        self.assertIn('ROOT / "tests" / "test_act2_pivot_static.py"', runner)


if __name__ == "__main__":
    unittest.main()
