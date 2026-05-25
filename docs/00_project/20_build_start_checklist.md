# KHOVAN REACH — BUILD START CHECKLIST

Revision: repo-consolidated baseline
Status: Setup checklist
Purpose: Confirm the project is ready to begin implementation Slice 0 / Slice 1.

---

# 1. Source Authority

- [ ] `docs/00_project/00_source_index.md` is present.
- [ ] `docs/00_project/10_repo_structure.md` is present.
- [ ] `docs/00_project/20_build_start_checklist.md` is present.
- [ ] `docs/01_design/00_scenario_play_guide.md` is active.
- [ ] `docs/01_design/10_mast_requirements.md` is active.
- [ ] `docs/01_design/20_gm_operational_notes.md` is active.
- [ ] `docs/01_design/30_qualification_cards.md` is active.
- [ ] `docs/01_design/40_admin_testing_plan.md` is active.
- [ ] `docs/01_design/50_implementation_slice_plan.md` is active.
- [ ] `docs/02_content/00_hessler_voice_mode.md` is active.
- [ ] `docs/02_content/10_pirate_dialogue.md` is active.
- [ ] `docs/02_content/20_damcon_reports.md` is active.
- [ ] `docs/02_content/30_anderson_clips.md` is active.
- [ ] `docs/02_content/40_dillon_clips.md` is active.
- [ ] `docs/02_content/50_debrief_script.md` is active.
- [ ] `docs/03_game_resources/comms/00_tsn_cultural_comms_playbook.md` is active.
- [ ] `docs/04_implementation_setup/00_transfer_from_old_build.md` is active.
- [ ] `docs/04_implementation_setup/10_mast_file_lessons.md` is active.
- [ ] `docs/04_implementation_setup/20_current_objective_display_spike.md` is active.
- [ ] `docs/04_implementation_setup/30_implementation_project_start_prompt.md` is active.

---

# 2. Archive Hygiene

- [ ] Old pass covers are not in the active repo tree.
- [ ] Old outlines are not in the active repo tree.
- [ ] Old Pass 1 / Pass 2 / Pass 3 source files are not competing with the stable files.
- [ ] Old MAST requirements and old GM notes are not competing with the stable files.
- [ ] Old merged bundles and patch bundles are not in the active repo tree.
- [ ] Old Act I addenda are not in the active repo tree.
- [ ] Old implementation history has been captured in `docs/04_implementation_setup/` and then excluded or archived outside the active tree.

---

# 3. Governance

- [ ] `docs/05_governance/00_project_instructions_architecture.md` is present.
- [ ] `docs/05_governance/10_proview_decision_support_operating_rules_v2_2.txt` is present.
- [ ] ProView is treated as governance, not scenario canon.
- [ ] `docs/00_project/00_source_index.md` remains the source-of-truth map.

---

# 4. Game Resources

- [ ] `docs/03_game_resources/comms/00_tsn_cultural_comms_playbook.md` is the repo source for the Comms culture sheet.
- [ ] If mirrored to Google Drive, the sync direction is explicitly documented.
- [ ] If a runtime copy is needed, it is generated from `docs/03_game_resources/comms/00_tsn_cultural_comms_playbook.md` rather than edited separately.
- [ ] Runtime/player-facing copies do not expose secret pirate truth.

---

# 5. Old Build Lessons

- [ ] `docs/04_implementation_setup/00_transfer_from_old_build.md` exists.
- [ ] `docs/04_implementation_setup/10_mast_file_lessons.md` exists.
- [ ] `docs/04_implementation_setup/20_current_objective_display_spike.md` exists.
- [ ] Old dev jump harness concept is transferred to the Scenario Control Panel plan.
- [ ] Helper-module separation is captured.
- [ ] Production checkpoint separation is captured.
- [ ] `run_id` / `generation_id` stale-task protection is captured.
- [ ] Weak-frequency relay warning is captured.
- [ ] Drone subsystem-damage spike is captured.
- [ ] Old design authority is explicitly rejected.

---

# 6. Implementation Environment

- [ ] Mission path is the real Cosmos `data/missions/khovan_reach` path.
- [ ] No junction workflow is used unless re-verified.
- [ ] Current `sbs_utils` / MAST docs are available.
- [ ] At least one reference mission is available.
- [ ] Python test dependencies are installed.
- [ ] `python run_tests.py quick` works or failure is documented.
- [ ] `git status` is clean or expected.

---

# 7. Slice 0 Ready

Slice 0 can begin when all must-have setup items above are complete.

Slice 0 objective:

- organize repo
- verify tests
- verify source placement
- confirm old-build lessons are captured
- create initial test matrix shell
- no mission feature coding yet

---

# 8. Slice 1 Ready

Slice 1 can begin after Slice 0 passes.

Slice 1 objective:

- mission loads
- state initializes
- empty Scene 1 starts
- GM/admin overlay shell appears
- Scenario Control Panel shell appears
- story-jump framework shell exists
- message wrapper supports upper-left overlay and Comms archive echo

---

# 9. Do Not Start Full Act I Until

- [ ] Target subsystem-damage spike is complete.
- [ ] Kestrel/Tarsis Comms route stability is confirmed.
- [ ] Overlay + Comms archive echo is confirmed.
- [ ] Current-objective display spike has a proven path or accepted fallback.
- [ ] Story jump stale-task protection works.
- [ ] Player-facing debug controls can be hidden.
