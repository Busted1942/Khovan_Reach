# KHOVAN REACH — REPO STRUCTURE

Version: 1.0 repo-consolidated
Status: Canonical repo placement plan
Purpose: Keep the repo clean, avoid duplicate editable sources, and prevent version-control drift.

---

# 1. Main Rule

One editable source lives in one place.

If a file may be shown in-game, do not maintain a second manually edited copy under data or runtime folders. Either:

- load the canonical file directly, or
- generate a runtime copy from the canonical file through a script

Generated runtime copies should be ignored by Git unless there is a strong reason to commit them.

---

# 2. Recommended Repo Tree

- README.md
- AGENTS.md
- .gitignore
- docs/
  - 00_project/
  - 01_design/
  - 02_content/
  - 03_game_resources/
  - 04_implementation_setup/
  - 05_governance/
- docs_external/
- reference_missions/
- archive/
- scripts/
  - acts/
  - systems/
  - lib/
- tests/
- tools/
- audio/

---

# 3. docs/00_project

Purpose:
- repo-level index and structure guidance

Files:
- 00_source_index.md
- 10_repo_structure.md
- 20_build_start_checklist.md

Do not put scenario prose or implementation code here.

---

# 4. docs/01_design

Purpose:
- active Khovan Reach architecture and implementation handoff

Files:
- 00_scenario_play_guide.md
- 10_mast_requirements.md
- 20_gm_operational_notes.md
- 30_qualification_cards.md
- 40_admin_testing_plan.md
- 50_implementation_slice_plan.md

These are authoritative for design and implementation handoff.

Do not keep older Pass docs beside these files.

---

# 5. docs/02_content

Purpose:
- Khovan-specific content, dialogue, clips, NPC files, and debrief material

Files:
- 00_hessler_voice_mode.md
- 10_pirate_dialogue.md
- 20_damcon_reports.md
- 30_anderson_clips.md
- 40_dillon_clips.md
- 50_debrief_script.md

These are not generic game resources. They belong to Khovan Reach.

---

# 6. docs/03_game_resources

Purpose:
- reusable game resources that can be used beyond Khovan Reach

Current file:
- comms/00_tsn_cultural_comms_playbook.md

Rule:
- game-resource docs should be plain Markdown
- avoid tables
- avoid fenced code blocks
- avoid renderer-dependent formatting

---

# 7. docs/04_implementation_setup

Purpose:
- setup and restart guidance for the implementation project

Files:
- 00_transfer_from_old_build.md
- 10_mast_file_lessons.md
- 20_current_objective_display_spike.md
- 30_implementation_project_start_prompt.md
- 40_slice01_bootstrap_findings.md
These files help the coding project start cleanly. They are not a substitute for the active design docs.

The active build-start checklist lives at `docs/00_project/20_build_start_checklist.md`.

---

# 8. docs/05_governance

Purpose:
- decision and review discipline

Files:
- 00_project_instructions_architecture.md
- 10_proview_decision_support_operating_rules_v2_6.md
- 20_proview_v2_4_test_first_workflow_checkpoint_draft.md

Governance docs are not mission canon. They guide how to evaluate changes.

---

# 9. docs_external, reference_missions, and archive

Purpose:
- hold non-canonical implementation references, reference inventories, and old-build evidence

Rules:
- `docs_external/` contains non-canonical implementation references and curated notes
- `reference_missions/` contains reference mission inventories or reference material only
- `_local_clones` folders are local-only and must be Git-ignored
- external clones and old-build references must not be referenced by active runtime files
- `archive/old_build_reference/` is implementation-history evidence only
- none of these folders override active design docs
- active runtime files must not depend on local clones or archived old-build files

---

# 10. scripts

Purpose:
- MAST runtime code only

Suggested structure:
- scripts/main.mast
- scripts/acts/
- scripts/systems/
- scripts/lib/

Do not put design docs here.

---

# 11. scripts/acts

Purpose:
- scene-flow files

Suggested future files:
- act_1_shakedown.mast
- act_2_investigation.mast
- act_3_khovan_reach.mast
- debrief.mast

---

# 12. scripts/systems

Purpose:
- reusable mission systems

Suggested future files:
- scenario_control_panel.mast
- story_jump_presets.mast
- checkpoint_system.mast
- message_overlay.mast
- comms_archive.mast
- current_objective_display.mast
- damcon_timer.mast
- pirate_state_machine.mast
- qualification_runtime.mast
- audio_runtime.mast

---

# 13. scripts/lib

Purpose:
- helper functions and reusable primitives

Suggested future files:
- act1_helpers.mast
- entity_cleanup_helpers.mast
- resupply_helpers.mast
- drone_spawn_helpers.mast
- target_detection_helpers.mast

Rule:
- helpers should be reusable by story jumps, checkpoint recovery, and normal runtime
- the Scenario Control Panel should not own production restore logic

---

# 14. tests

Purpose:
- automated tests

Suggested future files:
- test_bootstrap.py
- test_story_jumps.py
- test_static_structure.py
- test_message_routing.py

---

# 15. tools

Purpose:
- developer tooling

Suggested future files:
- khovan_regression.ps1
- build_runtime_resources.py

If a runtime copy of a doc is needed, generate it with a tool rather than editing two files by hand.

---

# 16. audio

Purpose:
- produced audio assets

Suggested future folders:
- audio/dillon/
- audio/anderson/
- audio/sfx/

Clip scripts remain in docs/02_content. Audio files go here.

---

# 17. What Is Not Included

This package intentionally does not include:

- old Pass covers
- old outlines
- v2.0/v2.1/v2.2 patch bundles
- Act I draft addenda
- old MAST implementation files
- generated runtime copies of docs

Those belong in external history, not in the active repo source tree.

---

# 18. Naming Convention

Use this convention:

- two-digit numeric prefix
- lower_snake_case
- stable filenames
- no version suffix in active filenames

Examples:
- 00_source_index.md
- 10_mast_requirements.md
- 20_gm_operational_notes.md

Numbers are local to a folder, not global across the repo.

Use Git commits, tags, and document headers for version history.
