from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRONE_PATH = "scripts/acts/act1_drone_contact_fire.mast"
GENERATOR_PATH = "scripts/acts/act1_generator_tarsis_gate.mast"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def code_only(text: str) -> str:
    """Strip MAST comment lines.

    Several handlers in this file carry long root-cause comments that name the very
    sbs_utils APIs the tests forbid in code (science_set_scan_data, scan_type_list,
    <scan>). Assertions about what the runtime does must look at code lines only, or
    documenting a hazard would trip the guard against it.
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
            "await task_schedule(khovan_drone_01_spawn)",
        ]:
            self.assertIn(phrase, drone)

        prepare_body = label_body(drone, "khovan_act1_drone_contact_fire_prepare_after_engineering")
        self.assertIn("await task_schedule(khovan_drone_01_spawn)", prepare_body)
        self.assertNotIn('"objective_id": "drone_01_ready"', prepare_body)
        self.assertNotIn('+ "Deploy Drone 01" khovan_drone_01_spawn', drone)

        for phrase in [
            "shared drone_contact_sequence_run_id = 0",
            "shared drone_contact_act2_ready = False",
            "shared drone_01_spawn_offset_m = 15000",
            "shared drone_01_deploy_prompt_sent = False",
            "shared drone_01_deploy_prompt_text = \"",  # prose covered by tests/test_mission_text_contract.py
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

    def test_spike_spawn_uses_bare_stock_kralien_cruiser_baseline(self) -> None:
        drone = read(DRONE_PATH)
        spawn_body = label_body(drone, "khovan_drone_contact_fire_spawn_target_spike")
        for phrase in [
            'npc_spawn(32000, 0, 12000, "Kralien Cruiser", "kralien, raider", "kralien_cruiser", "behav_npcship")',
            'drone_target_spike_status = "spawned_stock_kralien_cruiser"',
            "[KHOVAN ACT1 DRONE SPIKE SPAWN]",
        ]:
            self.assertIn(phrase, spawn_body)

        for forbidden in [
            "khovan_training",
            "khovan_slice06_spike_target",
            "khovan_drone_spike_target",
            "sim.add_navproxy",
            'link(artemis_id, "extra_scan_source", drone_target_spike_target_id)',
            "set_science_selection(artemis_id, drone_target_spike_target_id)",
            "set_comms_selection(artemis_id, drone_target_spike_target_id)",
        ]:
            self.assertNotIn(forbidden, spawn_body)

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
            'spike_target.data_set.get("system_damage", sbs.SHPSYS.WEAPONS)',
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

        # This guard used to forbid sbs.SHPSYS.* in the data_set.get() call,
        # from the 2026-08-08 conclusion that the second argument was a fallback
        # default and an enum there was nonsense.
        #
        # That conclusion was wrong, and the guard is retired 2026-08-09.
        # sbs_utils/mock/sbs.py:632 declares get(self, name, index=0) - the
        # second argument is an INDEX. The engine writes per-subsystem damage as
        # blob.set('system_damage', cur, x) over range(SBS.SHPSYS.MAX), so
        # SHPSYS.WEAPONS is exactly the right index and the original call was
        # closer to correct than its replacement. See cookbook section 9.1.
        #
        # Keeping the ban would now forbid the correct form - a stale guard
        # actively blocking the fix, which is worse than no guard.
        self.assertIn(
            'spike_target.data_set.get("system_damage", sbs.SHPSYS.WEAPONS)',
            drone,
            "per-subsystem damage must read by SHPSYS index, not index 0",
        )

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

    def test_drone_01_deploy_prompt_is_delayed_guarded_and_duplicate_suppressed(self) -> None:
        drone = read(DRONE_PATH)
        spawn_body = label_body(drone, "khovan_drone_01_spawn")
        self.assertIn(
            'npc_spawn(beacon.pos.x + drone_01_spawn_offset_m, beacon.pos.y, beacon.pos.z, "Drone 01", "kralien, raider, khovan_drone_01", "kralien_cruiser", "behav_npcship")',
            spawn_body,
        )
        self.assertIn(
            'task_schedule(khovan_drone_01_deliver_deploy_prompt_after_delay, {"deploy_prompt_run_id": drone_contact_sequence_run_id})',
            spawn_body,
        )

        prompt_body = label_body(drone, "khovan_drone_01_deliver_deploy_prompt_after_delay")
        for phrase in [
            "await delay_sim(seconds=10)",
            "if deploy_prompt_run_id != drone_contact_sequence_run_id:",
            "if not drone_01_active or drone_01_deploy_prompt_sent:",
            "drone_01_deploy_prompt_sent = True",
            '"send_text": drone_01_deploy_prompt_text',
        ]:
            self.assertIn(phrase, prompt_body)

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

    def test_drone_01_spawn_matches_the_bare_spike_target_baseline(self) -> None:
        # Regression guard for the 2026-08-09 live symptom: Drone 01's Science panel
        # showed Khovan override text instead of the engine's normal Kralien return,
        # while the GM Spike Target - spawned bare - showed the stock return with
        # shield frequencies. Drone 01 must stay configured the same way the Spike
        # Target is: same hull and stock roles, and none of the extra plumbing that
        # diverted the Science return.
        #
        # Drone 01 keeps its Khovan role for drill-state observation, but its stock
        # spawn configuration matches the GM Spike Target: enemy Kralien roles, the
        # same cruiser hull, and live NPC behavior.
        drone = read(DRONE_PATH)
        spike_spawn = label_body(drone, "khovan_drone_contact_fire_spawn_target_spike")
        drone_spawn = label_body(drone, "khovan_drone_01_spawn")

        for stock_config in ['"kralien, raider', '"kralien_cruiser"']:
            self.assertIn(stock_config, spike_spawn)
            self.assertIn(stock_config, drone_spawn)

        self.assertIn('"behav_npcship"', spike_spawn)
        self.assertIn('"behav_npcship"', code_only(drone_spawn))

        for forbidden in [
            "sim.add_navproxy",
            'link(artemis_id, "extra_scan_source"',
            "set_science_selection(artemis_id, drone_01_target_id)",
            "set_comms_selection(artemis_id, drone_01_target_id)",
        ]:
            self.assertNotIn(forbidden, spike_spawn)
            self.assertNotIn(forbidden, drone_spawn)

    def test_unauthorized_damage_reset_is_duplicate_suppressed(self) -> None:
        # Live trace 2026-08-09 13:06:54: one beam volley produced three
        # //damage/object events inside 45 ms, each scheduling its own reset. Every
        # reset despawns and respawns +5 km, so offset_m ran 15000 -> 30000 -> 45000
        # and the contact became unreachable - and it read as a one-hit kill from the
        # bridge, since the ship simply vanished on the first shot.
        drone = read(DRONE_PATH)
        damage_start = drone.index('//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_drone_01")')
        damage_end = drone.index('//damage/destroy if has_role(DESTROYED_ID, "khovan_drone_01")', damage_start)
        damage_body = code_only(drone[damage_start:damage_end])
        destroy_body = code_only(drone[damage_end:])

        for body, where in [(damage_body, "damage handler"), (destroy_body, "destroy handler")]:
            self.assertIn("if drone_01_reset_message_sent:", body, f"{where} needs the reset guard")
            # The flag must be set synchronously, before the yield - task_schedule
            # yields, so the reset label cannot guard itself in time.
            self.assertLess(
                body.index("drone_01_reset_message_sent = True"),
                body.index("await task_schedule(khovan_drone_01_reset"),
                f"{where} must set the guard before scheduling the reset",
            )

        # Cleared on respawn so the next attempt can reset again.
        self.assertIn("drone_01_reset_message_sent = False", label_body(drone, "khovan_drone_01_reset_flags"))

    def test_drone_01_fire_authorization_shortcut_is_gm_test_only(self) -> None:
        # Diagnostic shortcut, not a fallback and not a gameplay path. It must stay
        # behind the gamemaster + test_mode_enabled route and out of the Kestrel
        # player Comms menu.
        drone = read(DRONE_PATH)
        generator = read(GENERATOR_PATH)
        self.assertIn(
            '+ "Authorize Drone 01 Fire (test)" khovan_drone_01_test_authorize_fire if drone_01_active and not drone_01_fire_authorized',
            drone,
        )
        gm_panel_start = drone.index("//comms/gamemaster/khovan_drone_contact_fire_spike if has_roles(COMMS_ORIGIN_ID, \"gamemaster\") and test_mode_enabled")
        self.assertGreater(gm_panel_start, 0)
        kestrel_menu_start = generator.index('//comms if has_roles(COMMS_SELECTED_ID, "kestrel_yards")')
        kestrel_menu = generator[kestrel_menu_start:generator.index('//enable/comms if has_roles(COMMS_SELECTED_ID, "tarsis_station")', kestrel_menu_start)]
        self.assertNotIn("khovan_drone_01_test_authorize_fire", kestrel_menu)

        body = label_body(drone, "khovan_drone_01_test_authorize_fire")
        # Must invalidate the running stationary-hold watcher first, or it clears
        # range/hold flags out from under authorize_fire and the shortcut silently
        # fails.
        self.assertLess(
            body.index("drone_01_stationary_hold_run_id = drone_01_stationary_hold_run_id + 1"),
            body.index("drone_01_range_band_active = True"),
        )
        self.assertIn("await task_schedule(khovan_drone_01_authorize_fire)", body)

    def test_the_production_drones_use_live_hostile_npc_behavior(self) -> None:
        # Drone 01 now mirrors the GM Spike's live Kralien cruiser behavior. Drone 02
        # remains the separate free-fire completion target.
        drone = read(DRONE_PATH)
        drone_01 = code_only(label_body(drone, "khovan_drone_01_spawn"))
        drone_02 = code_only(label_body(drone, "khovan_drone_02_spawn"))

        # Drone 01: same live NPC behavior as the GM Spike Target.
        self.assertIn('"kralien, raider, khovan_drone_01"', drone_01)
        self.assertIn('"kralien_cruiser", "behav_npcship"', drone_01)

        # Drone 02: live AI, hostile side, and destructible - destruction is its
        # completion gate, so kralien_cruiser's 2 hull points are wanted here.
        self.assertIn('"kralien, raider, khovan_drone_02"', drone_02)
        self.assertIn('"kralien_cruiser", "behav_npcship"', drone_02)

        # The old neutral TSN-hulled configuration is not a combat target:
        # side_are_enemies() is false on a neutral side, so it draws neither the
        # stock enemy Science route nor normal hostile Weapons handling.
        self.assertNotIn("neutral", drone_02)
        self.assertNotIn("tsn_warpster", drone_02)

        # The hull hold belongs to Drone 01's drill only. Drone 02 must stay killable.
        self.assertNotIn("hull_hit_counter", drone_02)
        destroy_02 = drone[drone.index('//damage/destroy if has_role(DESTROYED_ID, "khovan_drone_02")'):]
        self.assertNotIn("hull_hit_counter", code_only(destroy_02))

    def test_drone_01_has_no_khovan_science_route_at_all(self) -> None:
        # Root cause locked in from installed sbs_utils v1.3.0 source, 2026-08-09
        # (sbs_utils/procedural/science.py). start_science_selected() bails out and
        # leaves the Science panel to the engine only when NO //enable/science label
        # passes. If one passes, sbs_utils owns the panel and ScanPromise.show_buttons()
        # hard-forces scan_type_list to a single "scan" tab for as long as
        # data_set["scan"] is None or "no data" - which is a freshly spawned NPC.
        # That costs the A-E shield-frequency bars the drill depends on, and the only
        # escape (a <scan> block or science_set_scan_data) overwrites scan_type_list
        # too. So the route cannot come back in any form without losing frequencies.
        #
        # Live 2026-08-09 confirmed both halves: Drone 01 with //enable/science showed
        # one "scan" tab and "no data"; the Spike Target with no route showed
        # scan/status/intel/bio plus the "weak C" bars.
        drone = read(DRONE_PATH)
        for forbidden in [
            '//enable/science if has_roles(SCIENCE_SELECTED_ID, "khovan_drone_01")',
            '//science if has_roles(SCIENCE_SELECTED_ID, "khovan_drone_01")',
            "Drone 01 is a neutral training contact. Weak shield-frequency relay data is available for Weapons.",
        ]:
            self.assertNotIn(forbidden, drone)

        # Code-scoped so the explanatory comment above the removal, which names
        # <scan> in prose, does not trip this.
        self.assertNotIn("<scan>", code_only(drone))

        # The Spike Target is the reference configuration and must stay routeless too.
        self.assertNotIn('//enable/science if has_roles(SCIENCE_SELECTED_ID, "khovan_slice06', drone)

    def test_drone_01_hull_is_held_so_three_subsystem_hits_can_land(self) -> None:
        # Design 10_mast_requirements.md 8.5 gate 9 wants three confirmed Weapons-array
        # hits, but shipData.yaml gives kralien_cruiser "hullpoints": 2 and manual
        # subsystem targeting only reaches systems once shields are down. Live
        # 2026-08-09: destroyed on the first hit. The hull is held at zero accumulated
        # hits while the drill is live.
        drone = read(DRONE_PATH)
        damage_start = drone.index('//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_drone_01")')
        damage_end = drone.index('//damage/destroy if has_role(DESTROYED_ID, "khovan_drone_01")', damage_start)
        body = code_only(drone[damage_start:damage_end])

        self.assertIn("if drone_01_active and not drone_01_weapons_disabled:", body)
        self.assertIn('set_data_set_value(DAMAGE_TARGET_ID, "hull_hit_counter", 0, 0)', body)

        # Shields must NOT be restored - manual subsystem targeting cannot reach the
        # Weapons array through an intact shield.
        self.assertNotIn("shield_val", body)

        # The manual-hit inventory read has to come before anything else in the
        # handler, or a yield could lose the signal the whole drill depends on.
        self.assertLess(
            body.index('get_inventory_value(DAMAGE_SOURCE_ID, "MANUAL_SYSTEM")'),
            body.index('set_data_set_value(DAMAGE_TARGET_ID, "hull_hit_counter", 0, 0)'),
            "MANUAL_SYSTEM must be read before the hull hold",
        )

        # Holding stops at disable so the ceasefire/cleanup phase behaves normally,
        # and the three-hit gate itself is untouched.
        self.assertIn("if drone_01_weapons_hit_count >= 3:", body)
        self.assertIn("drone_01_weapons_disabled = True", body)
        self.assertIn("drone_01_hull_restore_count = 0", label_body(drone, "khovan_drone_01_reset_flags"))

    def test_drone_01_is_hailable_and_answers_the_hail(self) -> None:
        # Second-order effect of removing the //science route, confirmed live and in
        # sbs_utils v1.3.0 source: comms.py set_buttons() returns before the button
        # loop when science_is_unknown() is True, so a never-scanned contact renders
        # as "unknown" with no Khovan Comms route. The removed <scan> block used to
        # mask this by writing scan text on panel render.
        drone = read(DRONE_PATH)
        self.assertIn('shared drone_01_hail_response_text = "Training drone acknowledges. Transponder reads TSN training contact. Stand by for further instructions."', drone)

        known_body = label_body(drone, "khovan_drone_01_mark_scan_known")
        # Guards required by AGENTS.md section 4.
        self.assertIn("if artemis_id == 0 or drone_01_target_id == 0:", known_body)
        self.assertIn("if artemis_object is None or drone_object is None:", known_body)
        # Writes only the scan key. scan_type_list must stay absent or the engine stops
        # rendering its own full panel - see the science-route tests above.
        self.assertIn(
            'drone_object.data_set.set("scan", drone_01_known_scan_text, artemis_object.side)',
            known_body,
        )
        drone_code = code_only(drone)
        self.assertNotIn("scan_type_list", drone_code)
        self.assertNotIn("science_set_scan_data", drone_code)
        self.assertNotIn("science_update_scan_data", drone_code)
        # Seeded at spawn and cleared per spawn, since a reset respawn is a new object.
        self.assertIn("await task_schedule(khovan_drone_01_mark_scan_known)", label_body(drone, "khovan_drone_01_spawn"))
        self.assertIn("drone_01_known_marked = False", label_body(drone, "khovan_drone_01_reset_flags"))

        # The hail must actually answer, on both the direct and the Tarsis route.
        for handler in ["khovan_drone_01_hail", "khovan_drone_01_fallback_hail"]:
            body = label_body(drone, handler)
            self.assertIn(
                'comms_receive(drone_01_hail_response_text, title="Drone 01", title_color="green")',
                body,
                f"{handler} should send the Drone 01 response",
            )
            self.assertIn("drone_01_hail_complete = True", body)
            # Player-facing reply, so bare comms_receive - comms_override is the
            # GM-only-route workaround and is still experimental.
            self.assertNotIn("comms_override", code_only(body))

        direct_hail_body = label_body(drone, "khovan_drone_01_hail")
        for phrase in [
            "drone_01_scan_complete = True",
            "drone_01_shield_frequency_relay_complete = True",
            "drone_01_scan_fallback_available = False",
            "drone_01_shield_relay_fallback_available = False",
            '"objective_id": "drone_01_weapons_lock"',
            "[KHOVAN OBJECTIVE 018] hail scan relay complete",
        ]:
            self.assertIn(phrase, direct_hail_body)
        self.assertNotIn('"objective_id": "drone_01_relay"', direct_hail_body)

    def test_drone_01_hail_button_is_guarded_and_announces_the_next_step(self) -> None:
        # Regression guard for a reported live symptom: the "Hail Drone 01" button
        # had no completion condition, so it stayed visible forever. A re-click
        # after hail completion silently re-ran the whole handler with no visible
        # change - same response text, same objective text - which read as "the
        # hail did not trigger the next step" even though it had already succeeded.
        drone = read(DRONE_PATH)
        self.assertIn(
            '+ "Hail Drone 01" khovan_drone_01_hail if not drone_01_hail_complete',
            drone,
        )

        body = label_body(drone, "khovan_drone_01_hail")
        self.assertIn("if drone_01_hail_complete:", body)
        self.assertLess(
            body.index("if drone_01_hail_complete:"),
            body.index("drone_01_hail_complete = True"),
            "the duplicate-suppress guard must run before the completion flag is set",
        )

        # Comms-channel confirmation of the next step, not just the current-
        # objective (blue text) overlay - reported hard to notice live.
        self.assertIn(
            'await task_schedule(khovan_drone_contact_fire_send_message, {"drone_message_text": drone_01_weapons_lock_next_step_text',
            body,
        )
        self.assertIn(
            'shared drone_01_weapons_lock_next_step_text = "Artemis - Weapons: Lock beams on Drone 01.\\nArtemis - Helm: Bring us between 1 and 2 kilometres and hold stationary for fifteen seconds."',
            drone,
        )

    def test_drone_01_scan_and_relay_fallbacks_survive_science_route_removal(self) -> None:
        # With no //science route, direct Drone 01 hail completes the drill gates.
        # Kestrel retains independently armed scan and relay fallbacks in case the
        # contact cannot be hailed.
        drone = read(DRONE_PATH)
        generator = read(GENERATOR_PATH)
        spawn_body = label_body(drone, "khovan_drone_01_spawn")
        self.assertIn("drone_01_scan_fallback_available = True", spawn_body)
        self.assertIn("drone_01_shield_relay_fallback_available = True", spawn_body)

        for route in [
            '+ "Fallback Scan" khovan_drone_01_fallback_scan if drone_01_scan_fallback_available',
            '+ "Fallback Shield Relay" khovan_drone_01_fallback_shield_relay if drone_01_shield_relay_fallback_available',
        ]:
            self.assertIn(route, generator)

        self.assertNotIn(
            '//comms if has_roles(COMMS_SELECTED_ID, "tarsis_station") and drone_contact_production_available',
            drone,
        )

        relay_body = label_body(drone, "khovan_drone_01_fallback_shield_relay")
        for phrase in [
            "drone_01_scan_complete = True",
            "drone_01_shield_frequency_relay_complete = True",
            "[KHOVAN OBJECTIVE 018] shield relay complete",
        ]:
            self.assertIn(phrase, relay_body)

        self.assertIn("drone_01_scan_complete = True", label_body(drone, "khovan_drone_01_fallback_scan"))

    def test_khovan_drone_contact_fire_send_message_routes_through_lifeform_helper(self) -> None:
        # Every drone-drill Comms acknowledgement funnels through this one label so
        # a future edit cannot reintroduce a silent gate that only updates the
        # current-objective (blue text) overlay. Dillon is the training instructor
        # voice already used by the ten-second deploy prompt.
        drone = read(DRONE_PATH)
        body = label_body(drone, "khovan_drone_contact_fire_send_message")
        self.assertIn('"send_lifeform_id": dillon_lifeform_id', body)
        self.assertIn('"send_sender": "Commander Dillon"', body)
        self.assertIn('"send_fallback_sender_id": kestrel_yards_id', body)
        self.assertIn("await task_schedule(khovan_lifeform_send,", body)

    def test_every_drone_01_gate_confirmation_sends_a_comms_acknowledgement(self) -> None:
        # Regression guard for the reported bug: fallback gates flipped their flag
        # and updated the current-objective text, but never sent anything into the
        # Comms channel, so the crew had no visible confirmation the click worked.
        drone = read(DRONE_PATH)
        for label in [
            "khovan_drone_01_fallback_scan",
            "khovan_drone_01_fallback_shield_relay",
            "khovan_drone_01_fallback_weapons_lock",
            "khovan_drone_01_fallback_range",
            "khovan_drone_01_fallback_stationary_hold",
            "khovan_drone_01_authorize_fire",
            "khovan_drone_01_register_weapons_hit",
            "khovan_drone_01_confirm_ceasefire",
        ]:
            body = label_body(drone, label)
            self.assertIn(
                "await task_schedule(khovan_drone_contact_fire_send_message,",
                body,
                f"{label} must acknowledge in the Comms channel, not just the objective overlay",
            )

        # The automatic weapons-select detector shares the same acknowledgement,
        # duplicate-suppressed so re-confirming an existing lock does not re-fire it.
        select_start = drone.index('//select/weapons if has_role(WEAPONS_ORIGIN_ID, "__player__")')
        select_end = drone.index("->END", select_start)
        select_body = drone[select_start:select_end]
        self.assertIn("and not drone_01_weapons_lock_active:", select_body)
        self.assertIn("await task_schedule(khovan_drone_contact_fire_send_message,", select_body)

        # Drone 02's kill confirmation, ahead of the larger cultural-packet handoff.
        destroy_start = drone.index('//damage/destroy if has_role(DESTROYED_ID, "khovan_drone_02")')
        destroy_body = drone[destroy_start:drone.index("=== khovan_drone_contact_fire_send_cultural_packet ===", destroy_start)]
        self.assertIn("await task_schedule(khovan_drone_contact_fire_send_message,", destroy_body)

    def test_every_gate_completion_rechecks_fire_authorization(self) -> None:
        # Regression guard for a reported live symptom: the crew got "Beam lock
        # confirmed" and later a stationary hold, but fire never authorized and
        # the blue current-objective text stayed frozen on "Drone away, Science
        # scan the contact" - the very first objective, from before any gate
        # closed. Root cause: khovan_drone_01_authorize_fire was only invoked
        # from the stationary-hold watcher (and its Kestrel fallback), so if the
        # crew locked weapons and held position BEFORE Comms hailed the drone,
        # the watcher found the hail gate missing, gave up silently, and nothing
        # ever re-checked once the hail (or any other out-of-order gate)
        # completed afterward. Every gate-completion path must recheck.
        drone = read(DRONE_PATH)
        for label in [
            "khovan_drone_01_hail",
            "khovan_drone_01_fallback_scan",
            "khovan_drone_01_fallback_hail",
            "khovan_drone_01_fallback_shield_relay",
            "khovan_drone_01_fallback_weapons_lock",
            "khovan_drone_01_fallback_range",
            "khovan_drone_01_fallback_stationary_hold",
        ]:
            body = label_body(drone, label)
            self.assertIn(
                "await task_schedule(khovan_drone_01_authorize_fire)",
                body,
                f"{label} completes a gate and must recheck fire authorization "
                "in case it was the last gate outstanding",
            )

    def test_fallback_hail_syncs_the_blue_objective_like_the_direct_hail_route(self) -> None:
        # Regression guard: the Kestrel "Fallback Hail" route set
        # drone_01_hail_complete and replied over Comms, but unlike the direct
        # "Hail Drone 01" button it never sent the next-step confirmation or
        # advanced current_objective_id past "drone_01_scan" - a crew hailed via
        # Kestrel stayed on the deploy-time objective text indefinitely even
        # after Weapons/Helm finished locking and holding.
        drone = read(DRONE_PATH)
        body = label_body(drone, "khovan_drone_01_fallback_hail")
        self.assertIn(
            'await task_schedule(khovan_drone_contact_fire_send_message, {"drone_message_text": drone_01_weapons_lock_next_step_text',
            body,
        )
        self.assertIn('"objective_id": "drone_01_weapons_lock"', body)

    def test_weapons_hit_counting_is_centralized_for_automatic_and_fallback_paths(self) -> None:
        # Both the automatic //damage/object observer and the Kestrel Comms
        # "Fallback Weapons Hit" route must land on the same completion label, so
        # they count identically and both produce the same Comms acknowledgement -
        # previously the fallback route incremented drone_01_weapons_hit_count
        # through its own separate, unacknowledged copy of the logic, and the
        # automatic path never acknowledged in Comms at all.
        drone = read(DRONE_PATH)
        damage_start = drone.index('//damage/object if has_role(DAMAGE_TARGET_ID, "khovan_drone_01")')
        damage_end = drone.index("=== khovan_drone_01_register_weapons_hit ===", damage_start)
        damage_body = drone[damage_start:damage_end]
        self.assertIn(
            'await task_schedule(khovan_drone_01_register_weapons_hit, {"hit_source": "automatic_manual_system_observer"})',
            damage_body,
        )
        self.assertNotIn("drone_01_weapons_hit_count = drone_01_weapons_hit_count + 1", code_only(damage_body))

        register_body = label_body(drone, "khovan_drone_01_register_weapons_hit")
        self.assertIn("drone_01_weapons_hit_count = drone_01_weapons_hit_count + 1", register_body)
        self.assertIn("if drone_01_weapons_hit_count >= 3:", register_body)

        fallback_body = label_body(drone, "khovan_drone_01_fallback_weapons_hit")
        self.assertIn(
            'await task_schedule(khovan_drone_01_register_weapons_hit, {"hit_source": "comms_fallback_confirmation"})',
            fallback_body,
        )
        self.assertNotIn("drone_01_weapons_hit_count = drone_01_weapons_hit_count + 1", code_only(fallback_body))

    def test_fire_authorization_is_duplicate_suppressed(self) -> None:
        # A race between the automatic stationary-hold watcher and the Kestrel
        # Comms fallback (both can complete on the same tick) must not send the
        # fire-authorization acknowledgement or objective update twice.
        drone = read(DRONE_PATH)
        body = label_body(drone, "khovan_drone_01_authorize_fire")
        self.assertIn("if drone_01_fire_authorized:", body)
        self.assertLess(
            body.index("if drone_01_fire_authorized:"),
            body.index("drone_01_fire_authorized = True"),
        )


if __name__ == "__main__":
    unittest.main()
