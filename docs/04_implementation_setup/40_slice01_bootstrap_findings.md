# Khovan Reach — Slice 01 Bootstrap Implementation Findings

Status: implementation finding log  
Authority: implementation setup / bootstrap evidence  
Scope: Slice 01 mission shell and bootstrap  
Design impact: none unless explicitly promoted by architecture review

This file records implementation findings discovered while turning the stable Khovan Reach architecture into Cosmos/MAST mission code.

Do not treat this file as scenario canon. Use it to protect implementation discipline, runtime packaging, and test coverage.

---

## 1. Runtime-clean mission root

### Finding

Git-ignored does not mean Cosmos-ignored.

Files and folders under the active Cosmos mission directory may still be visible to Cosmos/MAST runtime even if Git ignores them.

The active mission path is:

```text
C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach
```

External clones, archived old-build files, and local reference missions placed inside that tree can influence runtime load behavior if active bootstrap files reference them or if Cosmos/MAST scans broadly.

### Rule

The mission root must be runtime-clean, not merely Git-clean.

Active runtime files must not reference:

- docs_external/_local_clones
- reference_missions/_local_clones
- archive/old_build_reference
- old_mast
- old root MAST modules
- missing .mast files

### Preferred future improvement

Move full external reference clones outside the live mission root by default, for example:

```text
C:\Users\buste\OneDrive\Desktop\Cosmos\data\mission_references\khovan_reach_refs\
```

Keep only manifests, fetch scripts, and curated notes inside the committed Khovan repo.

---

## 2. Tier 2 references are implementation evidence only

Tier 2 references are valuable for package layout, MAST syntax, story.json, script.py, story.mast, task scheduling, and known-good mission patterns.

They are not Khovan design authority.

Reference missions may inform packaging and runtime conventions when multiple known-good examples agree. They must not change Khovan story, pacing, objectives, factions, or player-facing behavior.

---

## 3. __lib__.json packaging metadata

### Finding

Most inspected reference missions include root-level __lib__.json.

Observed simple mission metadata:

```json
{
  "version": "v1.3.0"
}
```

The MAST extension warns when no __lib__.json exists and may classify the folder differently.

### Decision

Khovan uses root-level __lib__.json with:

```json
{
  "version": "v1.3.0"
}
```

This is packaging metadata only. It is not scenario design.

### Acceptance impact

Quick tests should validate:

- __lib__.json exists
- it is valid JSON
- version is v1.3.0

Live Cosmos smoke must still prove that the package loads.

---

## 4. Root story.mast wrapper and scripts/main.mast ownership

### Finding

Known-good reference missions commonly use root-level story.mast.

The Khovan repo structure reserves scripts/ for active runtime code.

### Rule

Khovan should use:

```text
story.mast
```

as the thin root bootstrap wrapper required by Cosmos/MAST, and:

```text
scripts/main.mast
```

as the active Khovan mission entrypoint.

Root story.mast must not become a second copy of mission implementation logic.

### Test implication

Quick tests should verify:

- root story.mast exists
- scripts/main.mast exists
- root story.mast reaches or includes the active Khovan bootstrap path
- old root MAST names are not used as active implementation modules

---

## 5. Runtime load-path dependency validation

### Finding

Static file presence tests passed while live Cosmos failed on a missing old MAST dependency:

```text
Cannot load file:
...\khovan_reach\salvager_arrival.mast
```

This showed that tests were checking repo shape but not the active runtime load path.

### Rule

python run_tests.py quick must include runtime load-path validation for Cosmos/MAST work.

Quick tests should fail if active runtime files reference:

- missing .mast files
- archived old-build files
- external reference clone paths
- forbidden old module names
- files outside the active mission load path

### Forbidden old module examples

```text
salvager_arrival.mast
salvager_arrival
act_1_qualification.mast
act_1_state_helpers.mast
act_2_investigation.mast
act_3_khovan_reach.mast
dev_jump.mast
state_save.mast
```

Old root-level or archived `damcon_timer.mast` references remain forbidden until replaced by the current active implementation. A fresh active module at `scripts/systems/damcon_timer.mast` is allowed when the DAMCON timer slice implements it under the current requirements.

### Architecture note

Current requirements say the active pirate module should be pirate_state_machine.mast, not salvager_arrival.mast.

---

## 6. MAST GUI/task lifecycle requirement

### Finding

Live Cosmos later failed with:

```text
SBS_Utils runtime error
SBS Utils hook level runtime error
EDGE CASE. Did you set END or Yield the last GUI Task?
maststorypage.py line 591 in present
```

This means the mission reached the SBS Utils GUI/storypage scheduler but did not leave a valid active/yielding GUI or StoryPage task alive.

A one-shot bootstrap that initializes state and then falls off the end is not enough.

### Rule

Slice 01 bootstrap must leave a valid yielding/long-running GUI/story task alive, following a reference-backed pattern.

Do not assume that a task exists merely because a label or file exists. The active runtime entry chain must reach the task.

### Static quick-test implication

When practical, quick tests should verify:

- the active entry chain is statically discoverable or documented
- root story.mast reaches scripts/main.mast
- scripts/main.mast reaches the runtime idle/story task
- the idle/story task uses a reference-backed await/delay/yielding loop or equivalent
- the task does not immediately terminate

### Live-smoke implication

Static tests cannot fully prove this behavior.

Live Cosmos smoke remains required evidence for:

- BOOT-001 mission package loads
- BOOT-012 first scene proceeds without manual admin action

---

## 7. Static tests and live Cosmos smoke are different evidence classes

### Finding

python run_tests.py quick can prove source hygiene, package structure, JSON validity, Python syntax/import checks, forbidden reference checks, and some bootstrap contract checks.

It does not automatically prove:

- Cosmos mission menu load
- MAST runtime execution
- SBS Utils GUI lifecycle correctness
- audio playback
- GM-only overlay visibility
- player debug hiding
- first-scene progression

### Rule

Every slice verification note must separate:

- static quick checks
- local import/package checks
- runtime/load-path checks
- live Cosmos smoke checks
- unproven or blocked acceptance criteria

Do not claim Slice 01 complete on static tests alone while live runtime behavior is still failing.

---

## 8. Live failure to regression loop

Every live Cosmos failure should produce one of:

1. a targeted quick regression check, if the class of failure can be detected statically or locally
2. a documented live-smoke checklist item, if only Cosmos can prove it
3. an implementation blocker with exact next action, if unresolved

The first salvager_arrival.mast failure should produce a load-path regression check.

The EDGE CASE GUI task failure should produce a GUI/task lifecycle check where practical and remain a live-smoke requirement.

---

## 9. Slice 01 current acceptance stance

Slice 01 is not complete until:

- python run_tests.py quick passes
- active runtime files have no forbidden/missing load dependencies
- live Cosmos mission load reaches Scene 1 without manual recovery
- any untestable GUI/audio/admin behavior is documented as API uncertainty or live-smoke-only
- tests/SLICE01_VERIFICATION.md reflects actual evidence

If live Cosmos still fails, Slice 01 may be committed only as a documented blocker/investigation checkpoint, not as a completed bootstrap.

---

## Slice 01 live-smoke finding: load proof is not playable bootstrap

During Slice 01, the mission reached a stable live-load/bootstrap checkpoint.

Observed checkpoint:

- branch: `slice01-bootstrap`
- mission starts without missing-file errors
- mission starts without GUI lifecycle errors
- live smoke displays:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
Mission shell active. No Act I gameplay systems loaded.
```

Finding:

- "mission loads and displays validation marker" is not the same as "minimum playable mission start"
- the marker proves package load, Khovan route execution, and GUI lifecycle safety
- it does not prove Artemis/player ship exists
- it does not prove a connected client has a playable bridge state
- it does not prove Dillon Clip 1 was queued, played, or meaningfully stubbed beyond the validation surface

Implementation consequence:

- Slice 01 should be treated as mission shell and load proof
- Slice 01A should own the minimum playable bootstrap
- Scenario Control Panel work should not be treated as a substitute for minimum playable startup

This finding does not change scenario design, player-facing story content, or Act I requirements. It only clarifies implementation sequencing and acceptance evidence.

---

## Branch lifecycle lesson from Slice 01

During Slice 01, work moved between an implementation branch and a temporary documentation/architecture-feedback branch. A live-smoke confirmation prompt was run while the repository was still on the documentation branch. No damage occurred, but the event exposed a workflow gap.

Durable lesson:

- branch status checks are necessary but not sufficient
- branch purpose must be confirmed before work begins
- temporary docs/governance branches must be closed and merged back intentionally
- runtime implementation and live-smoke prompts should run from the active implementation branch
- after merge-back, quick tests and branch status must be rechecked before returning to runtime work

This is a workflow/process finding. It does not change scenario design or mission runtime requirements.

---

## Operator test expectation lesson from Slice 01

During Slice 01, several implementation changes were technically reasonable, but manual verification was hard to interpret because the operator did not always know what success, failure, or ambiguity should look like.

Observed ambiguous or confusing cases included:

- no runtime error but a blank screen
- empty `mast.runtime.log` or `mast.compile.log`
- no visible Khovan-specific marker
- negative-control wording that sounded inverted
- quick tests passing while live Cosmos behavior remained unproven

Durable lesson:

- do not merely ask the operator to run a test
- name the expected observation before the test
- name failure or ambiguous observations before the test
- identify what remains unproven after the test
- give the next action for success, failure, and ambiguity
- for negative controls, state clearly when an expected failure means the control passed

This is a workflow/process finding. It does not change scenario design or mission runtime requirements.
