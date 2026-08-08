from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRONE_PATH = "scripts/acts/act1_drone_contact_fire.mast"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def label_body(text: str, label: str) -> str:
    match = re.search(
        rf"^=== {re.escape(label)} ===(?P<body>.*?)(?=^=== |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing label: {label}")
    return match.group("body")


class Act1DroneContactFireStaticTests(unittest.TestCase):
    def test_slice06_spike_module_exists_imports_and_initializes(self) -> None:
        self.assertTrue((ROOT / DRONE_PATH).is_file())
        main = read("scripts/main.mast")
        self.assertIn(f"import {DRONE_PATH}", main)
        self.assertIn("await task_schedule(khovan_act1_initialize_drone_contact_fire)", main)

        jump_index = main.index("await task_schedule(khovan_story_jump_initialize_registry)")
        drone_index = main.index("await task_schedule(khovan_act1_initialize_drone_contact_fire)")
        playable_index = main.index("await task_schedule(khovan_reach_initialize_playable_bootstrap)")
        self.assertLess(jump_index, drone_index)
        self.assertLess(drone_index, playable_index)

    def test_phase_a_spike_and_phase_b_production_state_are_isolated(self) -> None:
        drone = read(DRONE_PATH)
        for phrase in [
            "shared drone_contact_fire_initialized = False",
            'shared drone_contact_sequence_status = "not_initialized"',
            'shared drone_contact_detection_mode = "phase_a_spike_only_live_cosmos_proof_required"',
            "shared drone_target_spike_available = False",
            "shared drone_target_spike_active = False",
            "shared drone_target_spike_target_id = 0",
            "shared drone_target_spike_scan_observed = False",
            "shared drone_target_spike_hail_observed = False",
            "shared drone_target_spike_weapons_selected = False",
            "shared drone_target_spike_damage_observed = False",
            "shared drone_target_spike_manual_subsystem_hit_observed = False",
            "shared drone_target_spike_manual_critical_hit_observed = False",
            "shared drone_target_spike_destroyed_observed = False",
            'shared drone_target_spike_destruction_source = "not_observed"',
            "shared drone_target_spike_cleanup_in_progress = False",
            'shared drone_target_spike_result = "unproven"',
            "Drone 01 proves Weapons subsystem disable; Drone 02 completes on destruction",
            "=== khovan_act1_drone_contact_fire_prepare_after_engineering ===",
            'drone_contact_sequence_status = "drone_01_ready_after_engineering"',
            '"objective_id": "drone_01_ready"',
            "Drone 01 training contact ready.",
        ]:
            self.assertIn(phrase, drone)

        for phrase in [
            "shared drone_contact_sequence_run_id = 0",
            "shared drone_contact_act2_ready = False",
            "shared drone_01_spawn_offset_m = 15000",
            "shared drone_01_weapons_hit_count = 0",
            "shared drone_02_destroyed = False",
            "shared drone_target_spike_available = False",
        ]:
            self.assertIn(phrase, drone)

        self.assertNotIn('mission_phase = "act_2"', drone)
        self.assertNotIn("khovan_act2_", drone)

    def test_gm_only_test_mode_spike_controls_exist(self) -> None:
        drone = read(DRONE_PATH)
        panel = read("scripts/systems/scenario_control_panel.mast")
        self.assertIn(
            '//comms/gamemaster/khovan_drone_contact_fire_spike if has_roles(COMMS_ORIGIN_ID, "gamemaster") and test_mode_enabled',
            drone,
        )
        for phrase in [
            '+ "Spawn Target Spike" khovan_drone_contact_fire_spawn_target_spike if not drone_target_spike_active',
            '+ "Select Target Spike" khovan_drone_contact_fire_select_target_spike if drone_target_spike_active',
            '+ "Read Target Spike Status" khovan_drone_contact_fire_report_target_spike',
            '+ "Cleanup Target Spike" khovan_drone_contact_fire_cleanup_target_spike if drone_target_spike_active or drone_target_spike_destroyed_observed',
            '+ "Slice 06 Target Spike" //comms/gamemaster/khovan_drone_contact_fire_spike if test_mode_enabled',
        ]:
            self.assertIn(phrase, drone + panel)

        self.assertNotIn("//comms/khovan_drone_contact_fire_spike", drone)
        self.assertNotIn("@gui", drone)
        self.assertNotIn("//gui", drone)

    def test_spike_spawn_uses_small_neutral_training_target_and_stock_scan_comms_hooks(self) -> None:
        drone = read(DRONE_PATH)
        spawn_body = label_body(drone, "khovan_drone_contact_fire_spawn_target_spike")
        for phrase in [
            'npc_spawn(32000, 0, 12000, "Slice 06 Spike Target"',
            '"khovan_training, neutral, khovan_slice06_spike_target, khovan_drone_spike_target"',
            '"behav_npcship"',
            'sim.add_navproxy(drone_target_spike_target_id, "Slice 06 Spike Target"',
            'link(artemis_id, "extra_scan_source", drone_target_spike_target_id)',
            "set_science_selection(artemis_id, drone_target_spike_target_id)",
            "set_comms_selection(artemis_id, drone_target_spike_target_id)",
            "[KHOVAN ACT1 DRONE SPIKE SPAWN]",
        ]:
            self.assertIn(phrase, spawn_body)

        for phrase in [
            '//enable/comms if has_roles(COMMS_SELECTED_ID, "khovan_slice06_spike_target")',
            '//comms if has_roles(COMMS_SELECTED_ID, "khovan_slice06_spike_target")',
            '+ "Khovan: Hail Spike Target" khovan_drone_contact_fire_hail_spike_target',
            'drone_target_spike_hail_observed = True',
            "Khovan: Hail Spike Target",
        ]:
            self.assertIn(phrase, drone)

        self.assertNotIn('//enable/science if has_roles(SCIENCE_SELECTED_ID, "khovan_slice06_spike_target")', drone)
        self.assertNotIn('//science if has_roles(SCIENCE_SELECTED_ID, "khovan_slice06_spike_target")', drone)

    def test_gm_comms_receive_calls_use_comms_override_experiment(self) -> None:
        # Experimental fix, 2026-08-08: live smoke confirmed the bare comms_receive()
        # call in every GM-only route in this file never rendered visibly for the GM
        # across 3+ sessions (Spawn, Select, Read Target Spike Status, Cleanup all
        # confirmed executing via trace but producing no visible output). The one
        # untried proven-live shape from the cookbook is comms_override(sender_id,
        # player_id, from_name=...) wrapping comms_receive() - every other confirmed-
        # working comms_receive() call in the codebase uses it. Not yet live re-tested;
        # this test only locks in that the experiment is actually present in the code.
        drone = read(DRONE_PATH)
        gm_handlers = [
            "khovan_drone_contact_fire_spawn_target_spike",
            "khovan_drone_contact_fire_select_target_spike",
            "khovan_drone_contact_fire_report_target_spike",
            "khovan_drone_contact_fire_cleanup_target_spike",
        ]
        for handler in gm_handlers:
            body = label_body(drone, handler)
            self.assertIn(
                'with comms_override(COMMS_ORIGIN_ID, COMMS_ORIGIN_ID, from_name="Khovan Slice 06 Spike"):',
                body,
                f"{handler} should wrap its comms_receive() call(s) in comms_override",
            )

        # The player-facing Comms hail response is deliberately left as bare
        # comms_receive() - it was already live-confirmed working (operator report,
        # "comms passed"), and touching a proven-working call site without cause
        # would be exactly the kind of unforced change this repo's discipline warns
        # against.
        hail_body = label_body(drone, "khovan_drone_contact_fire_hail_spike_target")
        self.assertNotIn("comms_override", hail_body)
        self.assertIn('comms_receive("Training target acknowledges hail.', hail_body)

    def test_spike_observers_cover_selection_damage_subsystem_and_destruction(self) -> None:
        drone = read(DRONE_PATH)
        for phrase in [
            '//select/weapons if has_role(WEAPONS_ORIGIN_ID, "__player__")',
            "selected_weapons_target_id = get_weapons_selection(WEAPONS_ORIGIN_ID)",
            "drone_target_spike_weapons_selected = True",
            '//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_slice06_spike_target")',
            'system = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_SYSTEM")',
            'target_id = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_CRITICAL_HIT")',
            'spike_target.data_set.get("system_damage", 0)',
            "drone_target_spike_manual_subsystem_hit_observed = True",
            "drone_target_spike_manual_critical_hit_observed = True",
            '//damage/destroy if has_role(DESTROYED_ID, "khovan_slice06_spike_target")',
            "drone_target_spike_destroyed_observed = True",
            "sbs.delete_object(drone_target_spike_target_id)",
            "[KHOVAN ACT1 DRONE SPIKE DAMAGE]",
            "[KHOVAN ACT1 DRONE SPIKE DESTROY]",
            "[KHOVAN ACT1 DRONE SPIKE STATUS]",
        ]:
            self.assertIn(phrase, drone)

        for forbidden in [
            'sbs.SHPSYS.WEAPONS)',
            'sbs.SHPSYS.ENGINES)',
        ]:
            self.assertNotIn(forbidden, drone)

    def test_damage_handler_does_not_gate_subsystem_hit_on_critical_hit_match(self) -> None:
        # Bug fixed 2026-08-08: the prior code required MANUAL_CRITICAL_HIT to match
        # DAMAGE_TARGET_ID *and* MANUAL_SYSTEM to be non-None in the same event before
        # recording a subsystem hit. Live smoke showed a real MANUAL_SYSTEM signal
        # discarded by that AND. Assert the two are tracked independently.
        drone = read(DRONE_PATH)
        # //damage/object is a route, not a label; slice the file between its header
        # and the next route/label header instead.
        start = drone.index('//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_slice06_spike_target")')
        end = drone.index("//damage/destroy", start)
        damage_route_body = drone[start:end]

        self.assertIn("if system is not None:", damage_route_body)
        self.assertIn("drone_target_spike_manual_subsystem_hit_observed = True", damage_route_body)
        self.assertIn("if target_id is not None and target_id != 0:", damage_route_body)
        self.assertIn("drone_target_spike_manual_critical_hit_observed = True", damage_route_body)
        self.assertNotIn(
            "if target_id == DAMAGE_TARGET_ID and system is not None:", damage_route_body
        )

    def test_destroy_handler_has_cleanup_vs_combat_guard(self) -> None:
        # Confirmed live 2026-08-08: sbs.delete_object() in cleanup fires the same
        # //damage/destroy hook a genuine Weapons kill fires. The destroy handler must
        # distinguish source rather than treating destroyed_observed alone as a kill.
        drone = read(DRONE_PATH)
        start = drone.index('//damage/destroy if has_role(DESTROYED_ID, "khovan_slice06_spike_target")')
        destroy_route_body = drone[start:]

        for phrase in [
            "if drone_target_spike_cleanup_in_progress:",
            'drone_target_spike_destruction_source = "gm_cleanup"',
            "elif drone_target_spike_weapons_damage_value > 0 or drone_target_spike_engines_damage_value > 0:",
            'drone_target_spike_destruction_source = "genuine_weapons_kill"',
            'drone_target_spike_destruction_source = "unattributed_zero_damage"',
        ]:
            self.assertIn(phrase, destroy_route_body)

    def test_cleanup_handler_sets_cleanup_in_progress_flag_and_does_not_clear_it(self) -> None:
        # Bugfix 2026-08-08 (live-confirmed, reproduced across 4 independent cleanup
        # events): sbs.delete_object()'s //damage/destroy hook is deferred/queued, not
        # synchronous. The cleanup handler's own CLEANUP trace line always logs BEFORE
        # the resulting DAMAGE/DESTROY events fire. An earlier version of this guard
        # cleared cleanup_in_progress immediately after sbs.delete_object() as a
        # same-build "fallback," which cleared the flag before the destroy handler ever
        # got to read it - live trace showed every cleanup reporting
        # destruction_source=unattributed_zero_damage instead of gm_cleanup. The cleanup
        # handler must set the flag and leave it set; only the destroy handler (once the
        # deferred hook actually fires) or the next spawn's reset may clear it.
        drone = read(DRONE_PATH)
        cleanup_body = label_body(drone, "khovan_drone_contact_fire_cleanup_target_spike")
        self.assertIn("drone_target_spike_cleanup_in_progress = True", cleanup_body)
        self.assertNotIn("drone_target_spike_cleanup_in_progress = False", cleanup_body)
        set_index = cleanup_body.index("drone_target_spike_cleanup_in_progress = True")
        delete_index = cleanup_body.index("sbs.delete_object(drone_target_spike_target_id)")
        self.assertLess(
            set_index, delete_index,
            "cleanup_in_progress must be set True before sbs.delete_object() is called",
        )

    def test_reset_flags_clears_cleanup_in_progress_as_a_safety_net(self) -> None:
        # If sbs.delete_object() ever fails to trigger the destroy hook at all, the
        # flag must not leak forward into a future, unrelated kill. The next spawn's
        # reset is the safety net.
        drone = read(DRONE_PATH)
        reset_body = label_body(drone, "khovan_drone_contact_fire_reset_target_spike_flags")
        self.assertIn("drone_target_spike_cleanup_in_progress = False", reset_body)

    def test_drone_01_reset_respawn_carries_a_run_id_guard(self) -> None:
        # The reset path deletes Drone 01, yields, then respawns it. The yield is
        # a window a story jump can land in: the jump seeds bump
        # drone_contact_sequence_run_id, and without a guard the pending reset
        # spawns Drone 01 into the scene the jump landed in. Incrementing the
        # counter is not the same as checking it - the original code did the
        # former and not the latter.
        drone = read(DRONE_PATH)

        reset_body = label_body(drone, "khovan_drone_01_reset")
        self.assertIn(
            "drone_contact_sequence_run_id = drone_contact_sequence_run_id + 1",
            reset_body,
            "reset must bump the generation counter before scheduling the respawn",
        )
        self.assertIn(
            'task_schedule(khovan_drone_01_reset_respawn, {"reset_run_id": drone_contact_sequence_run_id})',
            reset_body,
            "reset must hand the current run id to the delayed respawn",
        )
        self.assertNotIn(
            "delay_sim",
            reset_body,
            "the yield belongs in the guarded respawn label, not the reset label",
        )

        respawn_body = label_body(drone, "khovan_drone_01_reset_respawn")
        self.assertIn("default reset_run_id = drone_contact_sequence_run_id", respawn_body)
        # Cookbook section 5.1 requires three guards, not one.
        self.assertIn("if reset_run_id != drone_contact_sequence_run_id:", respawn_body)
        self.assertIn("if drone_contact_act2_ready:", respawn_body)
        self.assertIn("if drone_01_active:", respawn_body)

        # The stale check must come after the yield; guarding before the delay
        # proves nothing, because the jump happens during it.
        delay_at = respawn_body.index("delay_sim")
        guard_at = respawn_body.index("if reset_run_id != drone_contact_sequence_run_id:")
        self.assertLess(
            delay_at,
            guard_at,
            "run-ID comparison must happen after the delay, not before it",
        )

    def test_scenario_control_panel_reports_spike_status(self) -> None:
        panel = read("scripts/systems/scenario_control_panel.mast")
        for phrase in [
            "drone_contact_sequence_status. {drone_contact_sequence_status}",
            "drone_target_spike_status. {drone_target_spike_status}",
            "drone_target_spike_result. {drone_target_spike_result}",
        ]:
            self.assertIn(phrase, panel)

    def test_quick_suite_includes_slice06_static_checks(self) -> None:
        runner = read("run_tests.py")
        self.assertIn('ROOT / "tests" / "test_act1_drone_contact_fire_static.py"', runner)

    def test_slice06_verification_doc_records_phase_a_limits(self) -> None:
        path = ROOT / "tests" / "SLICE06_VERIFICATION.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8").lower()
        for phrase in [
            "goal",
            "source sections used",
            "files touched",
            "state variables",
            "runtime flow",
            "gm controls",
            "player-facing behavior",
            "spike result",
            "tests/static checks",
            "live smoke checklist",
            "expected observations",
            "failure/ambiguous observations",
            "acceptance covered",
            "acceptance not covered",
            "known risks/api uncertainties",
            "next action",
            "phase a",
            "drone 02 completes on destruction",
            "quick/static checks do not prove live cosmos",
        ]:
            self.assertIn(phrase, text)

    def test_phase_b_production_contract_uses_proven_signals_and_ready_marker(self) -> None:
        drone = read(DRONE_PATH)
        for phrase in [
            'shared drone_01_spawn_offset_m = 15000',
            'drone_01_spawn_offset_m = drone_01_spawn_offset_m + 5000',
            'sbs.distance_id(artemis_id, drone_01_target_id)',
            'if drone_range < 1000 or drone_range > 2000:',
            'if drone_01_stationary_hold_seconds >= 15:',
            'default hold_run_id = drone_01_stationary_hold_run_id',
            'if hold_run_id != drone_01_stationary_hold_run_id or not drone_01_active:',
            'manual_system = get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_SYSTEM")',
            'if drone_01_manual_system != "WEAPONS":',
            'if drone_01_weapons_hit_count >= 3:',
            'drone_01_weapons_disabled = True',
            'drone_contact_act2_ready = True',
            'drone_contact_act2_handoff_status = "ready_for_slice07_pivot"',
            'if drone_contact_cultural_packet_sent:',
            'shakedown_mode == "direct"',
        ]:
            self.assertIn(phrase, drone)

        for flag in [
            "drone_01_scan_fallback_available",
            "drone_01_hail_fallback_available",
            "drone_01_shield_relay_fallback_available",
            "drone_01_weapons_lock_fallback_available",
            "drone_01_range_fallback_available",
            "drone_01_stationary_hold_fallback_available",
            "drone_01_subsystem_hit_fallback_available",
            "drone_01_ceasefire_fallback_available",
        ]:
            self.assertIn(flag, drone)

        self.assertNotIn('get("system_damage"', label_body(drone, "khovan_drone_01_spawn"))
        self.assertNotIn("MANUAL_CRITICAL_HIT", drone[drone.index('//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_drone_01")'):])
        self.assertNotIn("Observe whether", drone)
        self.assertNotIn("existing Act II transition route", drone)

    def test_drone_01_science_scan_uses_the_proven_scan_result_structure(self) -> None:
        drone = read(DRONE_PATH)
        science_start = drone.index('//science if has_roles(SCIENCE_SELECTED_ID, "khovan_drone_01")')
        science_end = drone.index('//enable/comms if has_roles(COMMS_SELECTED_ID, "khovan_drone_01")', science_start)
        science_body = drone[science_start:science_end]
        self.assertEqual(science_body.count("<scan>"), 2)
        self.assertIn(
            "Drone 01 is a neutral training contact. Weak shield-frequency relay data is available for Weapons.",
            science_body,
        )


if __name__ == "__main__":
    unittest.main()
