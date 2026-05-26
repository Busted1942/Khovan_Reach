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

## 7A. MAST compile/preflight is a middle evidence class

### Finding

During Slice 01A, the local installed SBS Utils package exposed a usable MAST compile/preflight path. The repo quick suite now includes:

```text
tests/test_mast_compile_or_preflight.py
```

That test extracts the installed `artemis-sbs.sbs_utils.v1.3.0.sbslib`, registers SBS/GUI MAST nodes, points the MAST filesystem at the Khovan mission root, and compiles the active entry chain beginning at:

```text
story.mast
```

This is stronger than text-only static checking because it asks the MAST compiler/preflight path to load the active imports.

### Limit

MAST compile/preflight is still not live Cosmos smoke.

It does not prove:

- runtime variable values after scheduled tasks
- whether a bare identifier is available in a later route
- player ship assignment behavior
- renderer/shader behavior
- GUI/page lifecycle behavior in the live app
- whether a connected client can enter a usable bridge console

The Slice 01A `artemis_id` failure is the example: preflight and quick checks passed, then live Cosmos exposed a runtime variable-scope error when `assign_client_to_ship(..., artemis_id)` evaluated.

### Rule

Future Cosmos/MAST implementation work should preserve three separate statements in verification notes and handoffs:

```text
static/source checks:
MAST compile/preflight checks:
live Cosmos smoke:
```

If compile/preflight is unavailable locally, quick may skip it with an explicit reason. If it is available, quick should run it. In both cases, acceptance criteria that depend on live runtime behavior still require live Cosmos smoke.

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

## Route-smoke breadcrumb trace lesson from Slice 01A

During Slice 01A, `python run_tests.py quick`, MAST compile/preflight checks, and static load-path checks passed, but live Cosmos still crashed during Khovan mission load.

The normal local logs were not enough:

- `mast.compile.log` was empty or did not identify the live failure
- `mast.runtime.log` was empty or did not identify the live failure
- `tests/live_smoke_last_bootstrap.txt` remained the last-success audit and did not update during the crash

The useful evidence came from an append-only route-smoke breadcrumb trace:

```text
tests/live_startup_trace.txt
```

The trace brackets each startup handoff and risky runtime step:

```text
[KHOVAN EARLY 001] script.py entered
[KHOVAN EARLY 002] before sbs_utils import
[KHOVAN EARLY 003] after sbs_utils import
[KHOVAN EARLY 004] before ClientSelectPage setup
[KHOVAN EARLY 005] after ClientSelectPage setup
[KHOVAN EARLY 006] before story.mast load/handoff
[KHOVAN BOOT 001] scripts/main.mast entered
[KHOVAN BOOT 002] before state defaults
[KHOVAN BOOT 003] after state defaults
[KHOVAN BOOT 004] before playable_bootstrap
[KHOVAN BOOT 005] playable_bootstrap entered
[KHOVAN BOOT 006] before Artemis/player ship init or confirmation
```

The trace narrowed the crash to the Artemis/player ship init block. This converted a vague Khovan-only hard crash into a precise startup-route failure.

### Rule

For future Cosmos/MAST startup or route failures, add route-smoke breadcrumbs before guessing at runtime fixes when:

- quick/static/preflight checks pass but live Cosmos crashes
- `mast.compile.log` and `mast.runtime.log` are empty or unhelpful
- the last-success audit marker does not update
- the active entry chain is in doubt
- a risky API boundary is being crossed, such as player spawn, client page setup, GUI lifecycle, map handoff, or StoryPage handoff

Use separate files for separate evidence classes:

- `tests/live_smoke_last_bootstrap.txt` records the last successful bootstrap audit
- `tests/live_startup_trace.txt` records append-only crash breadcrumbs

If the trace does not update at all, the active startup path is earlier or different than assumed. If the trace stops at a marker, the next line or API call after that marker becomes the first suspect.

This is a troubleshooting and test-evidence pattern. It does not change scenario design or mission runtime requirements.

---

## Slice 01A live-smoke finding: minimum playable bootstrap reached, ordnance unsafe

Matt's Slice 01A live smoke confirmed the minimum playable bootstrap:

- mission launches
- server reaches playable/ready state
- two clients can connect
- console selection works
- Helm console can move Artemis
- Dillon Clip 1 text stub is active
- `mission_phase = act_1`
- `current_scene = 1`

This is sufficient for Slice 01A as a minimum playable bootstrap. It is not Act I gameplay acceptance and does not prove Weapons/ordnance readiness.

Observed known issue after the Slice 01A smoke:

```text
Microsoft Visual C++ Runtime Library
Assertion failed!
Program: ...\Cosmos\Artemis3-x64-release.exe
File: D:\PaxDev\Artemis3\Artemis3\imguiArt3.cpp
Line: 1482
Expression: '!list.empty() && "uiDropDownList; list is empty."'
```

Trigger:

- Weapons client attempts to load a torpedo.

Finding:

- Minimum playable bootstrap reached; ordnance UI/loadout is not yet safe.
- Attempting torpedo load on Weapons client triggers Artemis3 `imguiArt3.cpp` line 1482 `uiDropDownList` empty assertion.
- Likely cause is missing or invalid torpedo inventory / player ship ordnance configuration.

Decision:

- Do not treat this as a Slice 01A blocker unless Slice 01A acceptance is expanded to include Weapons/torpedo gameplay.
- Defer to an ordnance/Tarsis/Act I setup spike unless a tiny reference-backed loadout initialization is added.
- Resolve before Act I Weapons/Tarsis/ordnance/drone slices depend on torpedo loading.

This finding does not change scenario design. It records a runtime implementation boundary discovered during Slice 01A smoke.

---

## Slice 01B finding: client lifecycle requires complete reference rebuild

The Slice 01A custom Khovan selector proved enough for minimum playability, but it is not the correct baseline for Slice 02 because it bypasses normal Cosmos/Legendary station selection, Game Master access, and Change Console behavior.

Failed partial Legendary integration:

```text
common_console_select.mast
name 'PLAYER_COUNT' is not defined

common_console_select.mast
name 'TAB_CONSOLES' is not defined
```

Finding:

- `common_console_select.client_main` is not a standalone label to route into directly.
- `PLAYER_COUNT`, `PLAYER_LIST`, `TAB_CONSOLES`, Change Console routing, Game Master registration, and player ship setup are part of a larger LegendaryMissions lifecycle.
- Old Khovan and reference missions use `settings.yaml`, the full mastlib stack, Legendary `server_console` routing, selected `@map` startup, and `spawn_players`.

Slice 01B port:

- use old/reference `script.py` StoryPage registration with no Khovan `main_server` or `main_client` override
- load the complete old/reference mastlib stack in `story.json`
- add `settings.yaml` with the reference settings contract
- let Legendary `server_console` own server/client lifecycle
- schedule `spawn_players` from the selected Khovan `@map`
- bind Khovan Scene 1 state to the reference-created Artemis player ship
- preserve Dillon Clip 1 stub and Slice 01A bootstrap markers

Deliberately not copied:

- old Khovan Act I gates
- Kestrel/Tarsis logic
- drones
- dev/story jumps
- pirate/salvager flow
- DAMCON
- debrief
- torpedo/ordnance behavior
- Scenario Control Panel

Slice 01B live smoke result:

- mission launches cleanly
- no `PLAYER_COUNT` runtime error
- no `TAB_CONSOLES` runtime error
- server reaches playable space view
- normal Cosmos/Legendary console selector appears
- Game Master option appears
- Helm can enter console and move Artemis
- Dillon Clip 1 stub appears
- custom Khovan selector is gone

Static checks reject partial lifecycle wiring, but they did not prove this live behavior on their own. Change Console should remain an explicit follow-up smoke observation before rebuilding Slice 02 if it was not exercised in the same pass.

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

---

## Slice 02 finding: Scenario Control Panel foundation must preserve the reference client lifecycle

Slice 02 starts from the Slice 01B reference client lifecycle baseline.

The Scenario Control Panel foundation is implemented as a GM-only Comms surface instead of a custom client page or console selector. This preserves:

- Legendary server/client lifecycle ownership
- normal Cosmos/Legendary console selection
- Game Master option availability
- Change Console lifecycle ownership
- Khovan Scene 1 playable bootstrap

The Slice 02 foundation adds only:

- a GM-only Khovan Scenario Control route guarded by `has_roles(COMMS_ORIGIN_ID, "gamemaster")`
- safe initialization after bootstrap state defaults
- mission overview state display
- separate Test Mode and Live GM Recovery Mode flags, both default false
- hold/release controls for `transition_held`
- a simple action log

Deliberately not added:

- story jumps
- destructive controls
- arbitrary variable editor
- checkpoint/reload
- Act I gameplay
- Kestrel/Tarsis gates
- drones
- DAMCON
- pirates
- debrief
- current-objective display
- custom Khovan client selector

Static checks cover the source contract and visibility guard shape only. Live Cosmos smoke remains required to prove:

- the GM can see the Khovan Scenario Control route
- player clients cannot see admin/debug controls
- hold/release updates the visible overview
- Slice 01B console selection, Game Master availability, and Helm movement do not regress
