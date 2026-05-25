# KHOVAN REACH — CANONICAL SOURCE INDEX v2.2
*Cleanup/source-governance pass after applying the architecture project instructions and ProView review discipline.*

Status: Canonical architecture and implementation handoff index  
Audience: Architecture project owner, implementation/coding project, GM  
Supersedes: `00_khovan_reach_source_index_v2_1.md` and the v2.1 cleanup/remove list

---

# 1. Purpose

This index resolves the remaining source-drift issues found after the v2.1 merge.

The v2.1 bundle was structurally sound, but the cleanup pass found these quality issues:

1. The source index still referenced `tsn_cultural_comms_playbook_v0_2_all_races.md` even though v0.3 is now the active race-motivation sheet.
2. Some implementation-facing docs still pointed to v2.0 filenames such as `03_mast_requirements_v2_merged.md` and `khovan_reach_admin_testing_plan_v2_merged.md`.
3. Pass 1 still contained older DAMCON outcome thresholds in Scene 14 and timing notes.
4. Several docs used "salvager" language in GM/design prose where "pirates under salvage cover" is clearer. Player-facing fiction may still say "salvagers" before exposure.
5. The project instructions needed a more explicit source-status check before artifact generation.

The v2.2 set is not a narrative redesign. It is a quality and governance cleanup.

---

# 2. Load-bearing architecture rule

Khovan Reach remains governed by this rule:

> Runtime drives normal flow. Players drive decisions. GM supervises ambiguity. GM overrides failure.

Implementation rule:

> Prefer automatic gates wherever Cosmos/MAST exposes reliable state. Use Comms/captain confirmation when an action is not mechanically visible. Use GM manual marks only as the last fallback.

---

# 3. Required source-status check

Before revising or emitting any architecture artifact, perform this check:

1. Identify which active v2.2 source governs the requested change.
2. Identify any older retrieved source that conflicts.
3. Treat conflicting older sources as archived unless the user explicitly asks for historical comparison.
4. State the merge target before emitting a new doc.
5. If the change affects canonical play, update the scenario core, MAST requirements, GM notes, qualification/debrief, and testing docs as needed.
6. If the change affects reusable reference material, update this source index.

This rule exists because older Pass files and draft addenda are still easy to retrieve and can otherwise reintroduce superseded assumptions.

---

# 4. Active v2.2 source-of-truth files

| File | Status | Purpose |
|---|---|---|
| `00_khovan_reach_source_index_v2_2.md` | CANONICAL | Source hierarchy, merge map, archive/remove list |
| `khovan_reach_pass1_v2_2_merged.md` | CANONICAL SCENARIO CORE | Full scene-by-scene play guide with Act I shakedown fork and corrected DAMCON thresholds |
| `01_hessler_voice_mode.md` | CANONICAL CONTENT | Hessler voice-mode operating file |
| `02_pirate_dialogue.md` | CANONICAL CONTENT | Pirate dialogue branches and state cues |
| `03_damcon_reports_v2_2.md` | CANONICAL CONTENT | DAMCON report text with corrected v2.2 threshold language |
| `04_anderson_clips.md` | CANONICAL CONTENT | Anderson clip scripts |
| `05_dillon_clips_v2_2_merged.md` | CANONICAL CONTENT + TRIGGER NOTES | Dillon clips plus Act I Training Control/Kestrel text-message triggers |
| `01_qualification_cards_v2_2_merged.md` | CANONICAL QUALIFICATION | GM-only cards with shakedown fork and pirate-cover wording cleanup |
| `02_gm_operational_notes_v2_2_merged.md` | CANONICAL GM OPS | Runtime-first GM notes with corrected references |
| `03_mast_requirements_v2_2_merged.md` | CANONICAL IMPLEMENTATION SPEC | Coding-assistant handoff spec with corrected cross-links |
| `04_debrief_script_v2_2.md` | CANONICAL DEBRIEF | Debrief script patched for v2.2 wording and runtime support |
| `khovan_reach_admin_testing_plan_v2_2_merged.md` | CANONICAL TEST/CONTROL SPEC | Scenario Control Panel, story jumps, Act I tests, regression plan |
| `khovan_reach_implementation_slice_plan_v1_2.md` | CANONICAL HANDOFF SUPPORT | Suggested build slices and acceptance gates with current references |
| `tsn_cultural_comms_playbook_v0_3_race_summaries.md` | CANONICAL REUSABLE COMMS REFERENCE | Cross-mission race/contact motivation sheet |
| `PROJECT_INSTRUCTIONS_KHOVAN_REACH_ARCHITECTURE_v1_1.md` | CANONICAL PROJECT INSTRUCTIONS | Suggested project-level instructions for architecture governance |

---

# 5. Canonical decisions

## 5.1 Act I shakedown fork

Act I supports three paths:

```text
FULL_SHAKEDOWN        Run expanded new-player training.
COMPRESSED_SHAKEDOWN  Run essential gates only.
DIRECT_SCENARIO       Skip drills after expedited resupply and proceed to Act II.
```

## 5.2 Generator-governor start

Artemis departs Kestrel with a temporary generator-output governor. Kestrel issues two homing torpedoes as emergency conversion reserve. After launch-envelope exit plus 10 seconds, Kestrel explains the generator issue.

Tarsis clears the generator governor after the crew requests:

```text
1. homing torpedo production priority
2. generator acceptance/support
3. docking clearance
```

## 5.3 Text-message delivery model

Until final UI exists, all Act I instruction/advisory text displays in the upper-left lifeform overlay and echoes into the Comms Officer's console archive. The Comms archive is the durable message history.

## 5.4 DAMCON thresholds

Canonical v2.2 thresholds:

```text
Extended:   T+0 to <T+10 clean; T+10 to <T+30 hypoxic; T+30+ total loss.
Compressed: T+0 to <T+5 clean;  T+5 to <T+15 hypoxic; T+15+ total loss.
```

T+25 extended and T+10 compressed are deep critical bands, not automatic death.

## 5.5 Pirate/salvage-cover wording

Use this convention:

```text
Player-facing before exposure: salvagers / salvage operators.
GM/design prose: pirates under salvage cover.
Runtime/module names: pirate_*.
```

Do not use `salvager_arrival.mast` as the active module name. Use `pirate_state_machine.mast`.

## 5.6 Qualification rule for skipped shakedown

Players are not punished for choosing Direct Scenario.

```text
Full Shakedown: all Act I observations available.
Compressed Shakedown: core Act I observations available; skipped steps are N/A or development-only.
Direct Scenario: Act I drill observations are N/A / not observed by captain election, not NEEDS RETEST.
```

---

# 6. Implementation-project minimal bundle

Use this bundle in the implementation/vibe-coding project:

```text
/docs_from_architecture/
  00_khovan_reach_source_index_v2_2.md
  khovan_reach_pass1_v2_2_merged.md
  01_hessler_voice_mode.md
  02_pirate_dialogue.md
  03_damcon_reports_v2_2.md
  04_anderson_clips.md
  05_dillon_clips_v2_2_merged.md
  01_qualification_cards_v2_2_merged.md
  02_gm_operational_notes_v2_2_merged.md
  03_mast_requirements_v2_2_merged.md
  04_debrief_script_v2_2.md
  khovan_reach_admin_testing_plan_v2_2_merged.md
  khovan_reach_implementation_slice_plan_v1_2.md
  tsn_cultural_comms_playbook_v0_3_race_summaries.md
```

Do not load old outlines, covers, architecture addenda, Act I draft files, or v2.0/v2.1 superseded bundles into routine coding sessions.

---

# 7. Conflict-resolution order

If there is a conflict:

1. `00_khovan_reach_source_index_v2_2.md` controls source hierarchy.
2. `03_mast_requirements_v2_2_merged.md` controls implementation behavior.
3. `khovan_reach_pass1_v2_2_merged.md` controls scenario/narrative flow.
4. `02_gm_operational_notes_v2_2_merged.md` controls GM operation.
5. `khovan_reach_admin_testing_plan_v2_2_merged.md` controls testing/admin behavior.
6. Pass 2 content files control dialogue/clip text unless a v2.2 trigger note explicitly changes when they fire.
7. Qualification cards and debrief script control assessment content, with v2.2 runtime support rules.
8. Archived outlines, covers, and draft architecture addenda do not control implementation.

---

# 8. Active-source removal / archive summary

Move these out of active context after adding v2.2:

```text
00_khovan_reach_source_index_v2_1.md
khovan_reach_pass1_v2_1_merged.md
03_mast_requirements_v2_1_merged.md
02_gm_operational_notes_v2_1_merged.md
01_qualification_cards_v2_1_merged.md
05_dillon_clips_v2_1_merged.md
khovan_reach_admin_testing_plan_v2_1_merged.md
khovan_reach_implementation_slice_plan_v1_1.md
03_damcon_reports.md              # active replacement is 03_damcon_reports_v2_2.md
04_debrief_script.md              # active replacement is 04_debrief_script_v2_2.md
tsn_cultural_comms_playbook_v0_2_all_races.md
00_khovan_reach_source_index_v2.md
03_mast_requirements_v2_merged.md
02_gm_operational_notes_v2_merged.md
khovan_reach_admin_testing_plan_v2_merged.md
khovan_reach_implementation_slice_plan_v1.md
khovan_reach_pass1.md
05_dillon_clips.md
01_qualification_cards.md
khovan_reach_act1_shakedown_fork_v0_5.md
khovan_reach_act1_automation_gate_map_v0_2.md
khovan_reach_act1_v0_5_change_note.md
khovan_reach_act1_shakedown_fork_v0_4.md
khovan_reach_act1_automation_gate_map_v0_1.md
khovan_reach_act1_training_revision_v0_3.md
khovan_reach_act1_training_change_review.md
khovan_reach_runtime_architecture.md
khovan_reach_runtime_architecture_v0_2.md
khovan_reach_scenario_control_panel_architecture.md
khovan_reach_testing_regression_architecture.md
khovan_reach_architecture_audit_merge_plan.md
00_pass2_cover.md
00_pass3_cover.md
khovan_reach_outline.md
khovan_reach_merged_architecture_docs_v2.zip
khovan_reach_merged_docs_v2_1.zip
khovan_reach_act1_training_update_bundle.zip
khovan_reach_act1_v0_4_update_bundle.zip
khovan_reach_act1_v0_5_update_bundle.zip
tsn_cultural_comms_playbook_v0_3_bundle.zip
```

Keep `PROVIEW DECISION SUPPORT OPERATING RULES v2.2` as a governance reference, not as a Khovan mission source. It should not be loaded into implementation coding sessions unless governance behavior is being reviewed.

Keep old files in `/archive` or `/design_history`; do not delete unless you are certain you no longer need audit history.
