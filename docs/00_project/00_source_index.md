# KHOVAN REACH — SOURCE INDEX

Revision: repo-consolidated baseline + branch-lifecycle + operator-test-expectation process updates + ProView v2.6 governance update
Status: Canonical source map for the implementation repo
Purpose: Identify the single active source files in this repo. Git history, not filename versioning, tracks future changes.

---

# 1. Source Rule

This repo uses stable filenames.

Do not create parallel active files such as:

- `mast_requirements_v2_4.md`
- `mast_requirements_final.md`
- `mast_requirements_new.md`
- `mast_requirements_copy.md`

Instead:

- edit the stable file
- commit the change
- record meaningful design decisions in commit messages or in the relevant document's revision note

The current active source tree is this package.

---

# 2. Project-Level Docs

- `docs/00_project/00_source_index.md`
- `docs/00_project/10_repo_structure.md`
- `docs/00_project/20_build_start_checklist.md`

Repo-root implementation-agent control:

- `AGENTS.md` (single governing control file for every coding/documentation agent — Claude Code, Codex, or any other tool. All rules live here.)
- `CLAUDE.md` (tool-loaded pointer only, for Claude Code's auto-loaded-file convention. No rules of its own — see `AGENTS.md`.)
- `CODEX.md` (tool-loaded pointer only, mirroring `CLAUDE.md` for Codex-style tools. No rules of its own — see `AGENTS.md`.)

Do not add rules to `CLAUDE.md` or `CODEX.md`. If a rule is needed, it goes in `AGENTS.md` so every agent sees the same one — that is the entire reason these pointer files exist instead of tool-specific copies.

---

# 3. Active Design Docs

- `docs/01_design/00_scenario_play_guide.md`
- `docs/01_design/10_mast_requirements.md`
- `docs/01_design/20_gm_operational_notes.md`
- `docs/01_design/30_qualification_cards.md`
- `docs/01_design/40_admin_testing_plan.md`
- `docs/01_design/50_implementation_slice_plan.md`

These are the active architecture and implementation-handoff sources.

---

# 4. Active Content Docs

- `docs/02_content/00_hessler_voice_mode.md`
- `docs/02_content/10_pirate_dialogue.md`
- `docs/02_content/20_damcon_reports.md`
- `docs/02_content/30_anderson_clips.md`
- `docs/02_content/40_dillon_clips.md`
- `docs/02_content/50_debrief_script.md`

These are Khovan-specific content and live-run references.

---

# 5. Reusable Game Resources

- `docs/03_game_resources/comms/00_tsn_cultural_comms_playbook.md`

This is reusable beyond Khovan Reach. It is plain Markdown because it may be shown in-game or copied into a Comms archive.

Do not expose secret pirate truth in player-facing game resources.

---

# 6. Implementation Setup Docs

- `docs/04_implementation_setup/00_transfer_from_old_build.md`
- `docs/04_implementation_setup/10_mast_file_lessons.md`
- `docs/04_implementation_setup/20_current_objective_display_spike.md`
- `docs/04_implementation_setup/30_implementation_project_start_prompt.md`
- `docs/04_implementation_setup/40_slice01_bootstrap_findings.md`
- `docs/04_implementation_setup/50_future_reusable_mission_kernel.md`
- `docs/04_implementation_setup/60_mast_api_cookbook.md`
- `docs/04_implementation_setup/70_agent_handoff_protocol.md`
- `docs/04_implementation_setup/80_slice_packets_07_16.md`
- `docs/04_implementation_setup/90_act23_automation_gate_map.md`
- `docs/04_implementation_setup/95_scripts_lib_extraction_plan.md`
- `docs/04_implementation_setup/96_next_session_execution_plan.md`

`60_mast_api_cookbook.md` records MAST/sbs_utils syntax already proven in this repo's active runtime code. It is implementation evidence, not design authority, and each pattern is tagged live / compile-only / unproven.

`70_agent_handoff_protocol.md` defines the slice-packet-in / verification-record-out contract used when work is split across planning and implementation agents. It governs process only.

`80_slice_packets_07_16.md` holds the completed slice packets for Slices 07-16, written to the 21-field template in `docs/01_design/50_implementation_slice_plan.md` section 2. It is build-side elaboration, not design authority: where it and the slice plan differ on design, the slice plan wins and the difference is a finding.

`90_act23_automation_gate_map.md` proposes the gate/fallback policy for Acts II/III that `docs/01_design/10_mast_requirements.md` section 8.9 already provides for Act I. Same standing as `80_`: build-side proposal, not design authority. It is written to be ratified into `10_mast_requirements.md` as section 8.10; until then no slice packet may cite it as authority.

`95_scripts_lib_extraction_plan.md` defines the `scripts/lib/` helper-module boundaries and the sequence for creating them. Build-side architecture, deliberately additive — it does not authorize refactoring existing act files.

`96_next_session_execution_plan.md` is the ordered execution plan for the next build stretch, written so a cheaper model can pick the work up without re-deriving context. It leads with the live-smoke items that block everything else, and names what not to do.

These are setup and handoff documents for starting or restarting the coding project. They preserve useful prior-build lessons without making old code authoritative.

The active checklist lives in:

- `docs/00_project/20_build_start_checklist.md`

---

# 7. Governance Docs

- `docs/05_governance/00_project_instructions_architecture.md`
- `docs/05_governance/10_proview_decision_support_operating_rules_v2_6.md`
- `docs/05_governance/20_proview_v2_4_test_first_workflow_checkpoint_draft.md` (draft governance reference preserved for comparison; not the active ProView operating-rules version)

Governance docs shape review discipline. They are not mission canon.

---

# 7A. Non-Canonical Implementation References

- `docs_external/00_tier2_reference_inventory.md`

Tier 2 references are syntax/API/reference evidence only. They do not define Khovan story, pacing, objectives, factions, or player-facing behavior.

---

# 8. Active Design Principles

- Runtime drives normal flow.
- Players drive decisions.
- GM supervises ambiguity.
- GM performs interpretive and dramatic moments.
- GM overrides only for recovery, pacing, or impossible-to-script judgment.
- Prefer automatic gates wherever Cosmos/MAST exposes reliable state.
- Use Comms/captain confirmation when an in-game action is not mechanically visible.
- Use GM manual marks only as the last fallback.
- Reload is not tactical rewind.
- Reload must not undo committed consequences.

---

# 9. Current Act I Canon

- Approved Slice 04 implementation finding: Artemis starts with visible ship energy = 0 while the temporary generator-output governor is active.
- Artemis starts with Homing=0, Nuke=0, EMP=0, Mine=0.
- Kestrel holds 2 homing torpedoes as emergency reserve and loads them only after the player requests the reserve through Comms.
- After launch-envelope exit plus 10 seconds, Kestrel explains the generator issue.
- Tarsis clears the generator governor and restores full energy and armament after the crew requests homing-torpedo priority, generator acceptance/support, docking clearance, and completes normal docking/resupply.
- Act I supports Full Shakedown Cruise, Compressed Shakedown Cruise, and Direct Scenario.
- Training text displays through the upper-left lifeform overlay for now and echoes into the Comms archive.
- Persistent current-objective text is an implementation spike, not yet proven.

---

# 10. Superseded Sources

Older outlines, Pass covers, prior merged bundles, patch bundles, Act I draft addenda, and old MAST implementation files should not live beside this active set as competing sources.

Keep them outside the active repo tree or under a clearly excluded archive if you need them for history.

---

# 11. Naming Convention

Use numbered, stable, lower_snake_case filenames.

Numbers are local to each folder:

- `00_` index or highest-priority starting point
- `10_` major active doc
- `20_` next major active doc
- gaps are intentional for future inserts

Do not encode draft versions in active filenames after this consolidation. Use Git history and document headers instead.
