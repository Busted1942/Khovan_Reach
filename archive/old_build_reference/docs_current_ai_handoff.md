# Khovan Reach AI Handoff

## Current Working State

Repo path:

`C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach`

The mission launches from the real Cosmos `data\missions` location. The old junction approach was abandoned because the VS Code MAST extension did not handle the junction/realpath correctly.

Working baseline to preserve:
- Artemis spawns.
- Kestrel Yards exists as departure/origin context only.
- Tarsis Station appears, can be hailed, grants normal docking clearance, and is the Drill One dock/resupply target.
- Drill One completes from Tarsis docking clearance plus successful docking.
- Drill Two keeps the known-good scan, hail, and Weapons target-selection path.
- Drill Three can transition to the existing Scene 5 Anderson orders entrypoint; later Act II/III remain scaffolded.

Latest implementation state:
- Active feature branch: `feature/khovan-dev-jump-harness`.
- Dev-only GM comms jump harness added in `scripts/dev_jump.mast`.
- Reusable Act I runtime helpers live in `scripts/act_1_state_helpers.mast` so future production checkpoint restore can reuse cleanup/resupply/spawn primitives without depending on the dev jump UI.
- `scripts/state_save.mast` remains the production checkpoint/reload scaffold and was not repurposed for dev jumps.
- Local MAST compile passes with `.\sbs.bat compile khovan_reach` from `C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions`.

## Current Design Authority

Use this source order:
1. Matt's current instruction.
2. `design_docs/khovan_reach_outline.md`
3. `design_docs/khovan_reach_pass1.md`
4. `design_docs/03_mast_requirements.md`
5. Current working MAST code.
6. Local reference missions / sbs_utils docs.
7. General reasoning.

Core guardrails:
- Khovan starts as a qualification cruise.
- Artemis later pivots to investigate a fragmentary distress signal.
- Anderson does not send Artemis to fetch a known part.
- Hessler is not a MAST NPC.
- Pirates initially present as salvagers.
- Qualification is observed through play, not visible player checklists.
- Do not implement Act II or Act III during Act I drill work.

## Act I Drill State

Drill Two is now the guided contact-handling tutorial:
- Drone 01 spawns as the scannable Drill Two contact.
- Science uses normal `scan`, `intel`, and `bio` tabs.
- Comms hail remains gated behind Science classification.
- Weapons target selection is detected with the existing select/weapons pattern.
- Captain posture, Helm geometry, Engineering boost, Weapons tuning/subtarget readiness, controlled-fire authorization, ceasefire, and final verification are GM-confirmed checks.
- Drill Two completion requires Science classification, Comms hail, GM-confirmed readiness/fire/ceasefire/final verification, and Drone 01 Weapons subsystem disabled.
- Drone 01 destruction before Weapons-disable confirmation sets an overfire/failure state and does not complete the drill.

Drill Three is now the unguided transfer drill:
- Drone 02 spawns after Drill Two completes.
- Drone 02 runs simple target-position evasion.
- Science/Comms/Helm/Engineering/Weapons process items are tracked as observations where practical.
- Hard runtime completion is Drone 02 Engine subsystem disabled plus ceasefire confirmed.
- Process misses in Drill Three should inform debrief/qualification but should not silently block completion if the Engine objective and ceasefire are achieved.
- Drill Three schedules the existing Scene 5 Anderson orders text after completion.

## Dev Jump Harness

GM-only comms controls are exposed through `Khovan Dev Jumps`.

Anchors currently available:
- Start Fresh / Normal Mission Start
- Scene 1 Departure
- Scene 2 Drill One
- Scene 3 Drill Two Start
- Drill Two Steps 1-10
- Scene 4 Drill Three Start
- Act II / Anderson Orders

The harness is deliberately curated, not a universal script jump system.

Dev jump behavior:
- Cleans existing Drill Two/Three drone objects and known nav proxies.
- Invalidates old Drill Two authorization-hold timers and Drill Three evasion loops using run IDs.
- Seeds `dev_jump_active`, `dev_jump_anchor`, `dev_seeded_prior_steps`, and `dev_seeded_qualification_context`.
- Seeds skipped drill context only as dev/test context. Skipped observations are not clean qualification passes.
- Spawns Drone 01 or Drone 02 using the same verified local `npc_spawn` / navproxy patterns as Act I.
- Uses GM comms summary text for the selected anchor, prior seeded context, drone state, and next expected action.

Helper ownership:
- `scripts/dev_jump.mast`: GM-only menu controls and dev-seeded context reporting.
- `scripts/act_1_state_helpers.mast`: neutral Act I runtime helpers for cleanup, Artemis resupply/undock state, Drill Two step entry, Drill Two drone placement, and console target selection.
- `scripts/state_save.mast`: production checkpoint save/restore scaffold; currently only documents that future restore should reuse the neutral helpers once serialization/restoration syntax is verified.

Current limitation:
- Existing info-panel text already scheduled before a jump is not canceled; no verified task-cancel pattern has been added yet.
- Drill Two conceptual step anchors are mapped onto the current playable Engineering-prelude implementation. For Captain/Helm anchors, the Engineering prelude may be dev-seeded so the existing ready-posture button remains testable.

## API / Runtime Uncertainty

Verified patterns used:
- MAST labels, shared state, imports, scheduled tasks, delays, logs.
- `npc_spawn`, `sim.add_navproxy`, `target_pos`, roles, extra scan source links.
- Science and Comms station tabs.
- Weapons target-selection detection via `get_weapons_selection`.
- Manual subsystem damage inventory pattern from local LegendaryMissions references.
- GM-only comms controls via `has_roles(COMMS_ORIGIN_ID, "gamemaster")`.

Still needs Cosmos smoke validation:
- Whether manual subsystem hits reliably populate `MANUAL_SYSTEM` / `MANUAL_CRITICAL_HIT` in this mission's normal weapons UI.
- Whether Drone 01/02 subsystem disable is reliably detected by damage events. GM controls exist as fallback.
- Whether `gui_tab_remove_top("debug,brain,mast")` hides the player-facing debug tabs in the actual client layout.
- Actual Dillon audio playback remains TODO; current implementation logs clip placeholders.

## Workflow Rules

Use ChatGPT project chat for:
- deciding next slice
- writing Codex-ready prompts
- interpreting errors
- branch/merge/test guidance
- ProView-style decision support

Use Codex in VS Code for:
- local code inspection
- patches
- running read-only diagnostics
- local compile/smoke checks

Use Codex Chat mode for diagnosis/discovery.
Use Codex Agent mode only when files allowed to edit are clearly listed.

Always check:
- `git status --short`
- `git diff`

Commit only after Cosmos smoke test passes unless Matt explicitly requests a checkpoint/implementation commit before smoke.

Runtime logs should remain ignored:
- `mast.compile.log`
- `mast.runtime.log`
- `debug.log`
- `__pycache__/`

Do not commit runtime logs.
