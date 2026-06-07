# KHOVAN REACH — BUILD START CHECKLIST

Revision: repo-consolidated baseline + branch-lifecycle + operator-test-expectation process update + ProView v2.6 governance update
Status: Setup checklist
Purpose: Confirm the project is ready to begin implementation Slice 0 / Slice 1.

---

# 1. Source Authority

- [ ] `docs/00_project/00_source_index.md` is present.
- [ ] `docs/00_project/10_repo_structure.md` is present.
- [ ] `docs/00_project/20_build_start_checklist.md` is present.
- [ ] `AGENTS.md` is present when implementation agents are used.
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
- [ ] `docs/04_implementation_setup/40_slice01_bootstrap_findings.md` is active when Slice 01 findings have been accepted into the setup layer.

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
- [ ] `docs/05_governance/10_proview_decision_support_operating_rules_v2_6.md` is present.
- [ ] `docs/05_governance/20_proview_v2_4_test_first_workflow_checkpoint_draft.md` is present when comparing against the v2.4 draft governance reference.
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

# 6A. Branch Lifecycle and Return-to-Work Checks

Purpose:
- prevent implementation, live-smoke, documentation, governance, and architecture-feedback work from being run on the wrong branch
- keep temporary documentation branches from becoming hidden workflow forks
- make branch transitions explicit, testable, and reportable

This is process discipline only. It does not change scenario design, runtime behavior, player-facing content, or mission acceptance rules.

## Branch types

Before starting artifact-changing work, identify the branch purpose as one of:

- implementation
- docs/governance
- architecture feedback
- spike/experiment
- emergency fix

The branch type must match the task before edits begin.

Implementation and live-smoke work should normally run from the active implementation branch. Documentation, governance, and architecture-feedback branches may run static or quick tests, but should not be used for runtime implementation prompts or live Cosmos smoke unless explicitly approved for that purpose.

## Branch opening check

Before starting work, run:

```text
git status --short --branch
git log --oneline -5
```

Then record:

```text
Starting branch:
Branch type:
Task purpose:
Expected files/areas:
Expected return branch:
Runtime/live-smoke allowed from this branch: yes/no
```

Stop before editing if the branch does not match the task.

## Branch transition check

Before switching branches, run:

```text
python run_tests.py quick
git status --short --branch
git diff --stat
```

If `python run_tests.py quick` is unavailable, document that directly.

Before switching branches:

- commit coherent completed work, or
- stash intentionally, or
- discard intentionally after review

Do not leave unresolved documentation, test, or governance edits mixed with runtime implementation work.

## Branch closing check

Before merging a temporary docs/governance or architecture-feedback branch:

- run quick tests, if available
- inspect changed files
- confirm no mission code was modified unintentionally
- confirm no scenario design changed unintentionally
- commit with a docs/governance-specific message

Recommended inspection:

```text
git status --short --branch
git diff --stat
git diff --name-status
```

## Merge-back check

Completed docs/governance and architecture-feedback branches must be merged back into the active implementation branch intentionally.

After merge-back:

```text
python run_tests.py quick
git status --short --branch
```

Only resume implementation work after confirming:

- current branch is the intended implementation branch
- docs/governance updates are present
- quick tests pass or failure is documented
- working tree is clean or only expected changes remain

## Return-to-work check

Before running implementation prompts, live-smoke prompts, or Cosmos tests, confirm:

- current branch is the intended implementation branch
- current branch contains the latest merged docs/test-governance updates
- `python run_tests.py quick` passes or failure is documented
- no docs-only or architecture-feedback branch is active

If currently on a docs-only, governance, or architecture-feedback branch, stop and switch back before runtime testing.

## Branch lifecycle completion report

Every branch lifecycle operation must report:

```text
Starting branch:
Ending branch:
Branch type:
Commits created:
Merge performed: yes/no
Tests run:
Files changed:
Remaining uncommitted changes:
Next safe branch/action:
```

---

# 6B. Operator Test Expectation Checks

Purpose:
- make manual/operator tests actionable before the operator spends time testing
- distinguish success, failure, and ambiguous no-proof results
- prevent static quick tests, smoke markers, or negative-control failures from being overclaimed

Before asking a human operator to run a command, live smoke, UI check, documentation review, branch workflow check, generated-artifact review, or negative-control test, the agent must provide:

```text
What changed:
What to run or do:
Expected observation:
Failure/ambiguous observation:
What remains unproven:
Next action by result:
```

Manual and live tests must include both:

```text
Expected observation:
Failure/ambiguous observation:
```

Checklist:

- [ ] Test instructions identify exact command, UI action, app launch, or manual check.
- [ ] Test instructions state repo path and branch assumptions when relevant.
- [ ] Expected observations include visible/logged/file/Git/test-count/runtime markers where relevant.
- [ ] Failure or ambiguous observations include missing markers, wrong branch, empty logs, wrong screen, or no-error/no-proof outcomes.
- [ ] The handoff states what remains unproven, especially static-vs-live and smoke-vs-full-feature gaps.
- [ ] Next action is defined for success, failure, and ambiguous results.
- [ ] Negative-control tests state when an expected failure means the control passed.

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
