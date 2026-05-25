# KHOVAN REACH — IMPLEMENTATION PROJECT START PROMPT

Revision: repo-consolidated baseline
Status: Prompt for separate implementation/vibe-coding project
Purpose: Keep the implementation project focused on building from the stable repo-consolidated architecture without redesigning the scenario accidentally.

---

You are assisting with the Khovan Reach Implementation project.

This project consumes the Khovan Reach Architecture project's active stable handoff docs and turns them into Cosmos/MAST mission code.

Do not redesign the scenario casually. If implementation reveals a design problem, create an implementation finding and propose an architecture change rather than silently changing mission intent.

# Active source authority

Use these as the current source of truth:

- docs/00_project/00_source_index.md
- docs/01_design/00_scenario_play_guide.md
- docs/01_design/10_mast_requirements.md
- docs/01_design/20_gm_operational_notes.md
- docs/01_design/30_qualification_cards.md
- docs/01_design/40_admin_testing_plan.md
- docs/01_design/50_implementation_slice_plan.md
- docs/02_content/00_hessler_voice_mode.md
- docs/02_content/10_pirate_dialogue.md
- docs/02_content/20_damcon_reports.md
- docs/02_content/30_anderson_clips.md
- docs/02_content/40_dillon_clips.md
- docs/02_content/50_debrief_script.md
- docs/03_game_resources/comms/00_tsn_cultural_comms_playbook.md
- docs/04_implementation_setup/00_transfer_from_old_build.md
- docs/04_implementation_setup/10_mast_file_lessons.md
- docs/04_implementation_setup/20_current_objective_display_spike.md

Treat older outlines, Pass covers, v2.0/v2.1/v2.2/v2.3 patch files, old Act I addenda, and old implementation handoffs as archived unless the user explicitly asks for historical comparison.

# Core runtime rule

Runtime drives normal flow.
Players drive decisions.
GM supervises ambiguity.
GM overrides failure.

# Build discipline

- Build in small slices.
- Do not start with the full Act I drill.
- Start with repo setup, mission skeleton, state initialization, Scenario Control Panel shell, story-jump framework, and message routing wrapper.
- Prefer automatic gates where Cosmos exposes reliable state.
- Use Comms/captain confirmation for non-observable in-fiction actions.
- Use GM manual marks only as fallback.
- Keep Test Mode and Live GM Recovery Mode separate.
- Hide debug/admin controls from player consoles.
- Add tests or acceptance checks for every slice.
- Do not claim a slice complete until tests or smoke checks are run.

# Prior build lessons

Read `docs/04_implementation_setup/00_transfer_from_old_build.md` before coding.

Preserve useful lessons:
- real Cosmos mission path
- baseline Kestrel/Tarsis primitives
- dev jump harness concept as Scenario Control Panel
- neutral helper modules
- checkpoint separation
- run_id / generation_id stale-task protection
- regression workflow

Do not preserve:
- old design authority
- tangled Drill Two experiment branch
- weak-frequency relay as hard gate
- regular-hostile target substitution without proof
- GM-confirmed checks as default when runtime gates are available

# For every implementation slice, produce

1. Goal
2. Source sections used
3. Files to touch
4. State variables
5. Runtime flow
6. GM controls
7. Player-facing behavior
8. Test/jump presets
9. Acceptance criteria
10. Known risks or API uncertainties

If a Cosmos/MAST API capability is uncertain, create a spike before building the feature around it.
