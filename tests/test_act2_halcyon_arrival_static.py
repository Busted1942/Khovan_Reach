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
LIFEFORM_LIB_PATH = "scripts/lib/lifeform_helpers.mast"


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

    def test_spawn_uses_the_fixed_tarsis_relative_source_position(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        self.assertIn("if tarsis_station_id == 0:", body)
        self.assertIn("if tarsis_object is None:", body)
        self.assertIn("tarsis_object.pos.x + distress_source_tarsis_range_m", body)
        self.assertIn("tarsis_object.pos.z", body)

    def test_localization_automatically_triggers_the_spawn(self) -> None:
        halcyon = read(HALCYON_PATH)
        init = label_body(halcyon, "khovan_act2_initialize_halcyon_arrival")
        restart = label_body(halcyon, "khovan_halcyon_restart_arrival_observer")
        watch = label_body(halcyon, "khovan_halcyon_watch_distress_localization")
        self.assertIn("task_schedule(khovan_halcyon_restart_arrival_observer)", init)
        self.assertIn("task_schedule(khovan_halcyon_watch_distress_localization", restart)
        self.assertIn("if arrival_run_id != halcyon_arrival_run_id:", watch)
        self.assertIn("if distress_localized:", watch)
        self.assertIn("task_schedule(khovan_halcyon_spawn)", watch)
        self.assertIn("halcyon_arrival_observer_ticks >= 3000", watch)
        self.assertIn("jump khovan_halcyon_watch_distress_localization", watch)

    def test_act2_story_jump_reset_cleans_contact_and_rearms_arrival(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_reset_for_act2_jump")
        self.assertIn("task_schedule(khovan_halcyon_restore_damcon_team)", body)
        self.assertIn("task_schedule(khovan_halcyon_cleanup_and_wait_for_respawn)", body)
        self.assertIn("task_schedule(khovan_halcyon_restart_arrival_observer)", body)
        self.assertLess(
            body.index("task_schedule(khovan_halcyon_restore_damcon_team)"),
            body.index("task_schedule(khovan_halcyon_cleanup_and_wait_for_respawn)"),
        )
        self.assertLess(
            body.index("task_schedule(khovan_halcyon_cleanup_and_wait_for_respawn)"),
            body.index("task_schedule(khovan_halcyon_restart_arrival_observer)"),
        )
        self.assertNotIn("halcyon_cleanup_in_progress = False", body)

    def test_cleanup_barrier_waits_for_role_index_before_respawn(self) -> None:
        halcyon = read(HALCYON_PATH)
        barrier = label_body(halcyon, "khovan_halcyon_cleanup_and_wait_for_respawn")
        wait = label_body(halcyon, "khovan_halcyon_wait_for_cleanup_settle")
        self.assertIn("task_schedule(khovan_halcyon_cleanup)", barrier)
        self.assertIn('to_object_list(role("khovan_halcyon_drift"))', wait)
        self.assertIn('halcyon_cleanup_barrier_status = "settled"', wait)
        self.assertIn("halcyon_cleanup_wait_ticks >= 5", wait)
        self.assertIn('halcyon_cleanup_barrier_status = "timed_out_contact_or_hessler_still_indexed"', wait)

    def test_jump_013_promotes_valid_jump_012_without_destructive_reseed(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_act2_story_jump_seed_halcyon_arrival")
        self.assertIn('if distress_localized and halcyon_spawned and halcyon_jump_012_relocation_status == "relocated_to_halcyon_approach":', body)
        self.assertIn("[KHOVAN ACT2 JUMP 013 PROMOTE] reusing valid JUMP-012 Halcyon contact without cleanup", body)
        self.assertIn("else:", body)
        self.assertIn("task_schedule(khovan_act2_story_jump_seed_distress_localized)", body)
        self.assertLess(
            body.index('if distress_localized and halcyon_spawned and halcyon_jump_012_relocation_status == "relocated_to_halcyon_approach":'),
            body.index("task_schedule(khovan_act2_story_jump_seed_distress_localized)"),
        )
        self.assertIn('if act1_story_jump_cleanup_barrier_status != "settled":', body)
        self.assertIn("if not halcyon_spawned:", body)
        self.assertIn("task_schedule(khovan_halcyon_relocate_artemis_for_jump_013)", body)
        self.assertIn('if halcyon_jump_013_relocation_status != "relocated_to_halcyon_approach":', body)
        self.assertIn('current_scene = 8', body)
        self.assertIn('current_beat = "scene_8_halcyon_arrival"', body)

    def test_jump_012_relocates_artemis_to_a_guarded_five_kilometre_approach(self) -> None:
        halcyon = read(HALCYON_PATH)
        body = label_body(halcyon, "khovan_halcyon_relocate_artemis_for_jump_012")
        self.assertIn("shared halcyon_jump_012_approach_range_m = 5000", halcyon)
        self.assertIn("shared halcyon_jump_012_actual_range_m = 0", halcyon)
        self.assertLess(body.index("if artemis_id == 0:"), body.index("to_object(artemis_id)"))
        self.assertIn("if artemis_object is None:", body)
        self.assertIn("if halcyon_object_id == 0:", body)
        self.assertIn("if halcyon_jump_object is None:", body)
        self.assertIn(
            "artemis_object.pos = Vec3(halcyon_jump_object.pos.x - halcyon_jump_012_approach_range_m, halcyon_jump_object.pos.y, halcyon_jump_object.pos.z)",
            body,
        )
        self.assertIn('artemis_object.data_set.set("dock_base_id", 0, 0)', body)
        self.assertIn('artemis_object.data_set.set("dock_state", "undocked", 0)', body)
        self.assertIn('artemis_object.data_set.set("playerThrottle", 0, 0)', body)
        self.assertIn("sbs.distance_id(artemis_id, halcyon_object_id)", body)
        self.assertIn('halcyon_jump_012_relocation_status = "relocated_to_halcyon_approach"', body)

    def test_jump_013_relocates_artemis_to_a_guarded_five_kilometre_approach(self) -> None:
        halcyon = read(HALCYON_PATH)
        body = label_body(halcyon, "khovan_halcyon_relocate_artemis_for_jump_013")
        self.assertIn("shared halcyon_jump_013_approach_range_m = 5000", halcyon)
        self.assertLess(body.index("if artemis_id == 0:"), body.index("to_object(artemis_id)"))
        self.assertIn("if artemis_object is None:", body)
        self.assertIn("if halcyon_object_id == 0:", body)
        self.assertIn("if halcyon_jump_object is None:", body)
        self.assertIn(
            "artemis_object.pos = Vec3(halcyon_jump_object.pos.x - halcyon_jump_013_approach_range_m, halcyon_jump_object.pos.y, halcyon_jump_object.pos.z)",
            body,
        )
        self.assertIn('artemis_object.data_set.set("dock_base_id", 0, 0)', body)
        self.assertIn('artemis_object.data_set.set("dock_state", "undocked", 0)', body)
        self.assertIn('artemis_object.data_set.set("playerThrottle", 0, 0)', body)
        self.assertIn("sbs.distance_id(artemis_id, halcyon_object_id)", body)
        self.assertIn('halcyon_jump_013_relocation_status = "relocated_to_halcyon_approach"', body)

    def test_jump_013_summary_validates_contact_scene_and_approach_placement(self) -> None:
        story_jump = read("scripts/systems/story_jump_presets.mast")
        self.assertIn('halcyon_spawned and halcyon_jump_013_relocation_status == "relocated_to_halcyon_approach" and current_scene == 8:', story_jump)
        self.assertIn("Artemis was not placed at its approach point", story_jump)
        self.assertIn("Artemis placed five kilometres off Halcyon", story_jump)

    def test_spawn_promotes_runtime_to_halcyon_arrival_scene(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        self.assertIn('current_scene = 8', body)
        self.assertIn('current_beat = "scene_8_halcyon_arrival"', body)
        self.assertLess(
            body.index("halcyon_spawned = True"),
            body.index('current_scene = 8'),
        )

    def test_reset_blocks_if_deferred_cleanup_does_not_settle(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_reset_for_act2_jump")
        self.assertIn('if halcyon_cleanup_barrier_status != "settled":', body)
        self.assertIn("halcyon_contact_fallback_available = True", body)
        self.assertLess(
            body.index("task_schedule(khovan_halcyon_cleanup_and_wait_for_respawn)"),
            body.index('if halcyon_cleanup_barrier_status != "settled":'),
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
    def test_stock_science_is_preserved_and_hail_is_duplicate_suppressed(self) -> None:
        halcyon = read(HALCYON_PATH)
        executable = code_only(halcyon)
        self.assertNotIn('//enable/science if has_roles(SCIENCE_SELECTED_ID, "khovan_halcyon_drift")', executable)
        self.assertNotIn('//science if has_roles(SCIENCE_SELECTED_ID, "khovan_halcyon_drift")', executable)
        self.assertNotIn("=== khovan_halcyon_scan ===", executable)
        self.assertIn('//comms if has_roles(COMMS_SELECTED_ID, "khovan_halcyon_drift")', halcyon)
        self.assertIn("if halcyon_hail_observed:", label_body(halcyon, "khovan_halcyon_hail"))

    def test_spawn_marks_halcyon_known_without_overwriting_stock_tab_list(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        executable = code_only(body)
        self.assertIn('halcyon_known_object.data_set.set("scan", halcyon_known_scan_data, artemis_object.side)', body)
        self.assertNotIn('data_set.set("scan", halcyon_scan_report_text', body)
        self.assertNotIn("science_set_scan_data", executable)
        self.assertNotIn("science_update_scan_data", executable)
        self.assertNotIn("scan_type_list", executable)
        self.assertIn("if artemis_id == 0:", body)
        self.assertIn('halcyon_arrival_status = "known_contact_seed_blocked_no_artemis"', body)
        self.assertIn("halcyon_contact_fallback_available = True", body)
        self.assertIn("if artemis_object is not None and halcyon_known_object is not None:", body)

    def test_hail_records_verbal_science_gate_without_a_comms_message(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_hail")
        self.assertIn("halcyon_scan_observed = True", body)
        self.assertNotIn('"startup_sender": "Artemis Science"', body)
        self.assertNotIn("halcyon_scan_report_text", body)
        self.assertNotIn("Science report sent before hail", body)
        self.assertIn('"send_lifeform_id": hessler_lifeform_id', body)
        self.assertIn('"send_sender": "Captain Aurel Hessler"', body)

    def test_halcyon_support_request_is_hesslers_and_dillon_only_states_protocol(self) -> None:
        halcyon = read(HALCYON_PATH)
        body = label_body(halcyon, "khovan_halcyon_hail")
        lifeforms = read(LIFEFORM_LIB_PATH)
        self.assertGreaterEqual(body.count('"send_lifeform_id": hessler_lifeform_id'), 2)
        self.assertGreaterEqual(body.count('"send_fallback_sender_id": halcyon_object_id'), 2)
        self.assertIn('"send_text": halcyon_deploy_prompt_text', body)
        self.assertEqual(1, body.count('"send_lifeform_id": dillon_lifeform_id'))
        self.assertEqual(1, body.count('"send_sender": "Commander Dillon"'))
        self.assertIn('"send_text": dillon_away_manifest_protocol_text', body)
        self.assertIn("transmit the complement of your away team", halcyon)
        self.assertIn("one DAMCON team and one or two officers, including a qualified engineer", halcyon)
        self.assertNotIn("They have asked for an engineering team", halcyon)
        self.assertIn('"Request Current Instruction" khovan_dillon_repeat_instruction if current_objective_owner == "Commander Dillon"', lifeforms)
        self.assertIn('"Request Observer Assessment" khovan_dillon_observer_assessment if current_objective_owner != "Commander Dillon"', lifeforms)
        self.assertIn('"send_title": "Observer"', label_body(lifeforms, "khovan_dillon_observer_assessment"))

    def test_dillon_manifest_protocol_precedes_captain_authorization(self) -> None:
        halcyon = read(HALCYON_PATH)
        hail = label_body(halcyon, "khovan_halcyon_hail")
        self.assertIn("Away-mission protocol requires Comms to assemble and transmit the manifest.", halcyon)
        self.assertIn("Assign Engineering and, at your discretion, one additional officer", halcyon)
        self.assertIn("If you join the away team, designate the officer who will hold command of Artemis in your absence", halcyon)
        self.assertIn("DAMCON Team Reyes consists of Reyes, Park, and Achebe. It is the required damage-control element", halcyon)
        self.assertLess(
            hail.index('"send_text": halcyon_deploy_prompt_text'),
            hail.index('"send_text": dillon_away_manifest_protocol_text'),
        )
        self.assertLess(
            hail.index('"send_text": dillon_away_manifest_protocol_text'),
            hail.index('"objective_id": "halcyon_deploy"'),
        )
        self.assertIn("Order Comms to select Engineering and up to one additional officer", hail)
        self.assertIn('"objective_owner": "Artemis Captain"', hail)

    def test_all_halcyon_objectives_are_captain_owned(self) -> None:
        halcyon = read(HALCYON_PATH)
        for objective_id in ["halcyon_arrival", "halcyon_deploy", "halcyon_deploy_authorized"]:
            objective_line = next(line for line in halcyon.splitlines() if f'"objective_id": "{objective_id}"' in line)
            self.assertIn('"objective_owner": "Artemis Captain"', objective_line)
        deployed = label_body(halcyon, "khovan_halcyon_authorize_deployment")
        self.assertIn('halcyon_deployed_objective_owner = "Artemis Captain"', deployed)
        self.assertIn('halcyon_deployed_objective_owner = "Artemis Acting Command"', deployed)
        self.assertIn('"objective_owner": halcyon_deployed_objective_owner', deployed)

    def test_player_status_route_is_a_hessler_update_not_raw_debug_state(self) -> None:
        halcyon = read(HALCYON_PATH)
        route = label_body(halcyon, "khovan_halcyon_report_status")
        self.assertIn('+ "Request Status Update" khovan_halcyon_report_status', halcyon)
        self.assertIn('"send_lifeform_id": hessler_lifeform_id', route)
        self.assertIn('"send_sender": "Captain Aurel Hessler"', route)
        self.assertIn('"send_fallback_sender_id": halcyon_object_id', route)
        self.assertNotIn("comms_override(COMMS_ORIGIN_ID", route)
        self.assertNotIn("spawned=", route)
        self.assertNotIn("damcon=", route)

    def test_hessler_is_created_aboard_halcyon_and_has_a_badge_route(self) -> None:
        spawn = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        lifeforms = read(LIFEFORM_LIB_PATH)
        self.assertIn('task_schedule(khovan_create_hessler_lifeform, {"hessler_host_id": halcyon_object_id})', spawn)
        self.assertIn('shared hessler_lifeform_id = 0', lifeforms)
        create = label_body(lifeforms, "khovan_create_hessler_lifeform")
        self.assertIn('"lifeform_name": "Captain Aurel Hessler"', create)
        self.assertIn('"lifeform_roles": "khovan_hessler"', create)
        self.assertIn('"lifeform_path": "//comms/khovan_hessler"', create)
        self.assertIn('"lifeform_host_id": hessler_host_id', create)
        self.assertIn("//comms/khovan_hessler", lifeforms)
        self.assertIn('"Repeat Assistance Request" khovan_hessler_repeat_assistance', lifeforms)

    def test_hessler_lifecycle_is_part_of_halcyon_cleanup_barrier(self) -> None:
        halcyon = read(HALCYON_PATH)
        cleanup = label_body(halcyon, "khovan_halcyon_cleanup")
        barrier = label_body(halcyon, "khovan_halcyon_wait_for_cleanup_settle")
        remove = label_body(read(LIFEFORM_LIB_PATH), "khovan_remove_hessler_lifeform")
        self.assertIn("await task_schedule(khovan_remove_hessler_lifeform)", cleanup)
        self.assertIn('to_object_list(role("khovan_hessler"))', barrier)
        self.assertIn("len(remaining_hessler) == 0", barrier)
        self.assertIn("if hessler_lifeform_id == 0:", remove)
        self.assertIn("if hessler_object_for_cleanup is not None:", remove)
        self.assertNotIn("sbs.delete_object(hessler_lifeform_id)", remove)
        self.assertIn("lifeform_set_path(hessler_lifeform_id, None)", remove)
        self.assertIn("lifeform_transfer(hessler_lifeform_id, None)", remove)
        self.assertIn("hessler_object_for_cleanup.destroyed()", remove)
        self.assertLess(
            remove.index("lifeform_set_path(hessler_lifeform_id, None)"),
            remove.index("lifeform_transfer(hessler_lifeform_id, None)"),
        )
        self.assertLess(
            remove.index("lifeform_transfer(hessler_lifeform_id, None)"),
            remove.index("hessler_object_for_cleanup.destroyed()"),
        )
        for breadcrumb in [
            "[KHOVAN LIB LIFEFORM CLEANUP 001]",
            "[KHOVAN LIB LIFEFORM CLEANUP 002]",
            "[KHOVAN LIB LIFEFORM CLEANUP 003]",
        ]:
            self.assertIn(breadcrumb, remove)

    def test_objective_orders_science_report_then_captain_hail(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_spawn")
        self.assertIn("Have Science report on Halcyon, then order Comms to hail", body)
        self.assertNotIn("report her identity and condition", body)

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

    def test_deployment_removes_one_real_damcon_grid_team(self) -> None:
        halcyon = read(HALCYON_PATH)
        authorize = label_body(halcyon, "khovan_halcyon_authorize_deployment")
        detach = label_body(halcyon, "khovan_halcyon_deploy_damcon_team")
        self.assertIn("task_schedule(khovan_halcyon_deploy_damcon_team)", authorize)
        self.assertIn("if not damcon_deployed:", authorize)
        self.assertLess(
            authorize.index("task_schedule(khovan_halcyon_deploy_damcon_team)"),
            authorize.index("engineering_deployed = True"),
        )
        self.assertIn('to_object_list(grid_objects(artemis_id) & role("damcons"))', detach)
        self.assertIn('if halcyon_damcon_candidate.name == "DC3":', detach)
        self.assertIn("sbs.delete_grid_object(artemis_id, halcyon_damcon_team_id)", detach)
        self.assertIn("halcyon_damcon_team_object.destroyed()", detach)
        self.assertIn("halcyon_damcon_count_after != halcyon_damcon_count_before - 1", detach)
        self.assertIn('halcyon_damcon_transfer_status = "team_removed_from_artemis"', detach)
        self.assertNotIn("sbs.delete_object(halcyon_damcon_team_id)", detach)

    def test_hessler_acknowledges_the_transmitted_complement_before_transfer(self) -> None:
        halcyon = read(HALCYON_PATH)
        confirm = label_body(halcyon, "khovan_halcyon_manifest_confirm")
        self.assertIn("Manifest received: {halcyon_manifest_summary}", confirm)
        self.assertIn("standing by at Halcyon's transfer lock to receive the away team", confirm)
        self.assertIn("if not halcyon_deploy_acknowledgement_sent:", confirm)
        self.assertIn('"send_lifeform_id": hessler_lifeform_id', confirm)
        self.assertIn('"send_sender": "Captain Aurel Hessler"', confirm)
        self.assertIn('"send_text": halcyon_deploy_acknowledgement_text', confirm)
        self.assertIn("halcyon_deploy_acknowledgement_sent = True", confirm)

    def test_comms_selects_one_or_two_officers_with_engineering_required(self) -> None:
        halcyon = read(HALCYON_PATH)
        for option in [
            'Select Engineering Officer (Required)',
            'Select Captain',
            'Select Science Officer',
            'Select Weapons Officer',
            'Select Helm Officer',
            'Select Comms Officer',
            'Transmit Away-Team Complement',
            'Revise Away-Team Complement',
            'Designate Science Officer as Acting Command',
            'Designate Weapons Officer as Acting Command',
            'Designate Helm Officer as Acting Command',
            'Designate Comms Officer as Acting Command',
        ]:
            self.assertIn(f'+ "{option}"', halcyon)
        transmit_line = next(line for line in halcyon.splitlines() if '+ "Transmit Away-Team Complement"' in line)
        self.assertIn("halcyon_manifest_engineering_selected", transmit_line)
        self.assertIn("halcyon_manifest_officer_count >= 1", transmit_line)
        self.assertIn("halcyon_manifest_officer_count <= 2", transmit_line)
        self.assertIn("not halcyon_manifest_captain_selected or halcyon_manifest_acting_command_designated", transmit_line)
        for label in [
            "khovan_halcyon_manifest_add_engineering",
            "khovan_halcyon_manifest_add_captain",
            "khovan_halcyon_manifest_add_science",
            "khovan_halcyon_manifest_add_weapons",
            "khovan_halcyon_manifest_add_helm",
            "khovan_halcyon_manifest_add_comms",
        ]:
            body = label_body(halcyon, label)
            self.assertIn("halcyon_manifest_officer_count >= 2", body)
            self.assertIn("task_schedule(khovan_halcyon_manifest_recount)", body)

    def test_manifest_mutation_uses_a_stable_refreshed_comms_submenu(self) -> None:
        halcyon = read(HALCYON_PATH)
        root_route = halcyon.split(
            '//comms if has_roles(COMMS_SELECTED_ID, "khovan_halcyon_drift")', 1
        )[1].split(
            '\n//comms/khovan_halcyon_manifest if has_roles(COMMS_SELECTED_ID, "khovan_halcyon_drift")',
            1,
        )[0]
        self.assertIn(
            '+ "Assemble Away-Team Complement" //comms/khovan_halcyon_manifest',
            root_route,
        )
        self.assertNotIn('+ "Select Engineering Officer', root_route)
        self.assertNotIn('+ "Remove Engineering Officer', root_route)
        self.assertIn(
            '//comms/khovan_halcyon_manifest if has_roles(COMMS_SELECTED_ID, "khovan_halcyon_drift")',
            halcyon,
        )
        self.assertIn('+ "Back to Halcyon Drift" //comms', halcyon)
        mutation_labels = [
            "khovan_halcyon_manifest_add_engineering",
            "khovan_halcyon_manifest_add_captain",
            "khovan_halcyon_manifest_add_science",
            "khovan_halcyon_manifest_add_weapons",
            "khovan_halcyon_manifest_add_helm",
            "khovan_halcyon_manifest_add_comms",
            "khovan_halcyon_manifest_remove_engineering",
            "khovan_halcyon_manifest_remove_captain",
            "khovan_halcyon_manifest_remove_science",
            "khovan_halcyon_manifest_remove_weapons",
            "khovan_halcyon_manifest_remove_helm",
            "khovan_halcyon_manifest_remove_comms",
            "khovan_halcyon_manifest_command_science",
            "khovan_halcyon_manifest_command_weapons",
            "khovan_halcyon_manifest_command_helm",
            "khovan_halcyon_manifest_command_comms",
            "khovan_halcyon_manifest_command_clear",
        ]
        for label in mutation_labels:
            body = label_body(halcyon, label)
            self.assertIn('comms_navigate("//comms/khovan_halcyon_manifest")', body)
            self.assertIn("[KHOVAN ACT2 HALCYON MANIFEST CLICK]", body)
        confirm = label_body(halcyon, "khovan_halcyon_manifest_confirm")
        self.assertIn('comms_navigate("//comms")', confirm)
        self.assertIn("[KHOVAN ACT2 HALCYON MANIFEST CLICK] transmit complement", confirm)

    def test_transmitted_complement_names_required_damcon_team_and_selected_officers(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_manifest_confirm")
        self.assertIn("DAMCON Team Reyes (Reyes, Park, and Achebe); Engineering Officer", body)
        self.assertIn("; Captain; Artemis acting command: {halcyon_manifest_acting_command_role} Officer", body)
        for role in ["Science", "Weapons", "Helm", "Comms"]:
            self.assertIn(f'; {role} Officer', body)
        self.assertIn('halcyon_manifest_status = "complement_transmitted"', body)
        self.assertIn('"objective_id": "halcyon_deploy_authorized"', body)

    def test_captain_selection_requires_an_acting_commander(self) -> None:
        halcyon = read(HALCYON_PATH)
        confirm = label_body(halcyon, "khovan_halcyon_manifest_confirm")
        remove = label_body(halcyon, "khovan_halcyon_manifest_remove_captain")
        self.assertIn("if halcyon_manifest_captain_selected and not halcyon_manifest_acting_command_designated:", confirm)
        self.assertIn('halcyon_manifest_status = "confirmation_blocked_captain_requires_acting_command"', confirm)
        for role in ["science", "weapons", "helm", "comms"]:
            command = label_body(halcyon, f"khovan_halcyon_manifest_command_{role}")
            self.assertIn("if not halcyon_manifest_captain_selected", command)
            self.assertIn("halcyon_manifest_acting_command_designated = True", command)
        self.assertIn("halcyon_manifest_acting_command_designated = False", remove)
        self.assertIn('halcyon_manifest_acting_command_role = "none"', remove)

    def test_captain_away_path_hands_the_bridge_objective_to_acting_command(self) -> None:
        halcyon = read(HALCYON_PATH)
        body = label_body(halcyon, "khovan_halcyon_authorize_deployment")
        status = label_body(halcyon, "khovan_halcyon_report_status")
        self.assertIn("if halcyon_manifest_captain_selected:", body)
        self.assertIn('halcyon_deployed_objective_owner = "Artemis Acting Command"', body)
        self.assertIn("Captain and the declared away team", body)
        self.assertIn("Hold command and maintain the bridge-to-away-team channel", body)
        self.assertIn("if halcyon_manifest_captain_selected:", status)
        self.assertIn("Artemis - Acting Command: Captain and the declared away team", status)

    def test_authorization_is_hidden_and_blocked_until_complement_is_transmitted(self) -> None:
        halcyon = read(HALCYON_PATH)
        authorize_line = next(line for line in halcyon.splitlines() if '+ "Authorize Engineering Deployment"' in line)
        authorize = label_body(halcyon, "khovan_halcyon_authorize_deployment")
        self.assertIn("if halcyon_manifest_confirmed and not engineering_deployed", authorize_line)
        self.assertIn("if not halcyon_manifest_confirmed:", authorize)
        self.assertIn('halcyon_arrival_status = "deployment_blocked_manifest_not_transmitted"', authorize)

    def test_manifest_state_is_cleared_by_initialization_and_story_jump_reset(self) -> None:
        halcyon = read(HALCYON_PATH)
        init = label_body(halcyon, "khovan_act2_initialize_halcyon_arrival")
        reset = label_body(halcyon, "khovan_halcyon_reset_for_act2_jump")
        for body in [init, reset]:
            self.assertIn("halcyon_manifest_confirmed = False", body)
            self.assertIn("halcyon_manifest_officer_count = 0", body)
            for role in ["engineering", "captain", "science", "weapons", "helm", "comms"]:
                self.assertIn(f"halcyon_manifest_{role}_selected = False", body)
            self.assertIn('halcyon_manifest_summary = "not_declared"', body)
            self.assertIn("halcyon_manifest_acting_command_designated = False", body)
            self.assertIn('halcyon_manifest_acting_command_role = "none"', body)

    def test_damcon_detachment_guards_ship_and_team_objects(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_deploy_damcon_team")
        self.assertIn("if artemis_id == 0:", body)
        self.assertIn("if artemis_damcon_host is None:", body)
        self.assertIn("if halcyon_damcon_count_before == 0:", body)
        self.assertIn("if halcyon_damcon_team_object is None:", body)
        self.assertGreaterEqual(body.count("halcyon_damcon_transfer_fallback_available = True"), 4)

    def test_old_style_damcon_rally_marker_is_removed_with_team(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_deploy_damcon_team")
        self.assertIn('get_inventory_value(halcyon_damcon_team_id, "idle_marker", 0)', body)
        self.assertIn("sbs.delete_grid_object(artemis_id, halcyon_damcon_idle_marker_id)", body)
        self.assertIn("if halcyon_damcon_idle_marker_object is not None:", body)
        self.assertIn("halcyon_damcon_idle_marker_object.destroyed()", body)

    def test_recall_restores_the_tracked_team_before_story_state_advances(self) -> None:
        halcyon = read(HALCYON_PATH)
        restore = label_body(halcyon, "khovan_halcyon_restore_damcon_team")
        recall = label_body(halcyon, "khovan_halcyon_recall_engineering")
        self.assertIn("if artemis_id == 0:", restore)
        self.assertIn("if artemis_damcon_restore_host is None:", restore)
        self.assertIn("grid_restore_damcons(artemis_id)", restore)
        self.assertIn("halcyon_damcon_restored_candidate.name == halcyon_damcon_team_name", restore)
        self.assertIn("halcyon_damcon_count_after != halcyon_damcon_count_before + 1", restore)
        self.assertIn("task_schedule(khovan_halcyon_restore_damcon_team)", recall)
        self.assertIn("if damcon_deployed:", recall)
        self.assertLess(
            recall.index("task_schedule(khovan_halcyon_restore_damcon_team)"),
            recall.index('engineering_placement = "returned_to_artemis"'),
        )

    def test_jump_reset_blocks_instead_of_forgetting_a_failed_restore(self) -> None:
        body = label_body(read(HALCYON_PATH), "khovan_halcyon_reset_for_act2_jump")
        self.assertIn("if damcon_deployed:", body)
        self.assertIn('halcyon_arrival_status = "act2_reset_blocked_damcon_restore_failed"', body)
        self.assertLess(
            body.index("if damcon_deployed:"),
            body.index("task_schedule(khovan_halcyon_cleanup_and_wait_for_respawn)"),
        )

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
