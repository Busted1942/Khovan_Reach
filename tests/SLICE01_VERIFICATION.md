# Slice 01 Verification

## Goal

Build the minimum Khovan Reach mission shell and bootstrap path. Slice 01 does not implement Act I gameplay features.

## Source sections used

- `docs/01_design/10_mast_requirements.md`, Sections 4-6
- `docs/01_design/40_admin_testing_plan.md`, BOOT-001 through BOOT-012
- `docs/01_design/50_implementation_slice_plan.md`, Slice 01
- `docs/02_content/40_dillon_clips.md`, Clip 1
- `docs/04_implementation_setup/10_mast_file_lessons.md`, old implementation evidence only
- `docs_external/TIER2_REFERENCE_INVENTORY.md`
- Local Tier 2 bootstrap references under `docs_external/_local_clones`

## Files/folders verified

- `description.txt`
- `__lib__.json`
- `script.py`
- `story.json`
- `story.mast`
- `scripts/main.mast`
- `scripts/systems/bootstrap_state.mast`
- `scripts/systems/audio_runtime.mast`
- `scripts/systems/debug_runtime.mast`
- `tests/test_bootstrap_static.py`

Old MAST files remain archive/reference only under `archive/old_build_reference/old_mast`.

## State variables

Slice 01 initializes:

- `mission_phase = act_1`
- `current_scene = 1`
- `current_beat = scene_1_bootstrap`
- `last_checkpoint = none`
- `transition_held = false`
- `test_mode_enabled = false`
- `live_recovery_mode_enabled = false`
- `generator_governor_active = true`
- `starting_homing_torpedoes = 2`
- `kestrel_generator_packet_sent = false`
- `launch_envelope_cleared = false`
- `shakedown_mode = unset`
- `training_overlay_active = true`
- `comms_archive_enabled = true`
- `dillon_clip_1_status = stubbed`

## Runtime flow

`script.py` bootstraps sbs_utils `StoryPage` using `story.mast`. `story.mast` imports `scripts/main.mast`. `scripts/main.mast` imports the three Slice 01 system files and exposes `@map/khovan_reach`.

The map route schedules:

1. bootstrap state initialization
2. debug/admin visibility stub initialization
3. Dillon Clip 1 stub
4. Scene 1 bootstrap completion

## GM controls

No Scenario Control Panel is implemented in Slice 01. BOOT-010 is represented by `gm_debug_overlay_status = stubbed`.

## Player-facing behavior

Dillon Clip 1 is safely stubbed because the local environment cannot verify the Cosmos audio playback API. BOOT-011 is represented by `player_debug_controls_status = stubbed_hidden`.

## Tests or jump presets

No story jump presets are implemented in Slice 01.

`python run_tests.py quick` now runs Slice 00 source-hygiene checks plus Slice 01 static bootstrap checks.

## Acceptance criteria

- BOOT-001: mission package files exist for static verification, including reference-aligned `__lib__.json` packaging metadata.
- BOOT-002: `story.mast` imports active `scripts/main.mast`; active main imports required systems.
- BOOT-003: `story.json` is valid JSON.
- BOOT-004: `script.py` parses and has the verified `StoryPage` bootstrap shape.
- BOOT-005: minimum mission state variables initialize statically.
- BOOT-007: Dillon Clip 1 is stubbed with explicit status.
- BOOT-008: `current_scene = 1`.
- BOOT-009: `mission_phase = act_1`.
- BOOT-010: GM debug/admin overlay remains a documented stub.
- BOOT-011: player-facing debug controls remain a documented stub.
- BOOT-012: first scene bootstrap path exists statically; live runtime smoke is still required.

## Known risks or API uncertainties

Live Cosmos runtime was not executed from this environment.

Unverified until live smoke:

- exact MAST runtime execution of the imported map route
- actual audio playback API for Dillon Clip 1
- GM-only debug/admin overlay rendering
- player-facing debug tab/control hiding
- whether additional `story.json` mastlib dependencies are required for later gameplay slices
- `__lib__.json` was added as reference-aligned packaging metadata because `mast_starter`, `SecretMeeting`, `WalkTheLine`, and `LegendaryMissions` include it, simple observed mission examples use `{"version": "v1.3.0"}`, and the VS Code MAST extension warning indicates folder classification behavior. This is not Khovan design authority or mission feature code. Live Cosmos smoke must still verify mission load.

## Slice 01 findings

The active mission package now has a minimal bootstrap shell. Active `scripts/` contains only new Slice 01 bootstrap code and placeholder `.gitkeep` files. It does not contain old archived MAST files.

External Tier 2 clones remain ignored and untracked.

## Next recommended action

Run a live Cosmos smoke test for BOOT-001 through BOOT-012 before starting Slice 02 or any Act I gameplay feature coding.
