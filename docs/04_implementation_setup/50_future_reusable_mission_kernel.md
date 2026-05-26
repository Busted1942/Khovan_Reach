# Future Reusable Cosmos/MAST Mission Kernel Planning

Status: planning only
Purpose: Capture what may later become a reusable Cosmos/MAST starter kernel after Khovan Reach proves the extraction threshold.
Authority: implementation setup note, not scenario canon

This document does not create an active runtime template. It does not move, duplicate, or replace Khovan Reach source files.

---

## 1. Status

- Planning only.
- Not active runtime code.
- Not a template yet.
- Not scenario canon.
- Not a replacement for Khovan Reach design or implementation docs.

The Slice 01A through Slice 03 plumbing appears promising as a future reusable mission starter, but it is still embedded in Khovan Reach and still depends on Khovan proving at least one real gameplay path.

---

## 2. Extraction Threshold

Do not extract a reusable kernel until Khovan proves all of the following:

- one real playable mission start beyond bootstrap
- one real gameplay progression path with actual runtime gates, state changes, GM observability, and player-facing behavior
- `python run_tests.py quick` passing
- static/source checks passing
- MAST compile/preflight checks passing where available
- live route-smoke evidence for startup and at least one gameplay transition
- no major unresolved startup, page lifecycle, player-ship, or client-console uncertainty

Until that threshold is met, keep the plumbing in the Khovan implementation and improve it there.

---

## 3. Candidate Reusable Kernel Components

The following pieces may be candidates for later extraction if they remain stable through real gameplay:

- mission package/startup structure
- `script.py` / `story.mast` / `story.json` pattern, if proven beyond bootstrap
- bootstrap state initialization
- live startup trace and route breadcrumbs
- last-success audit versus current-attempt trace distinction
- `run_tests.py` quick/static/preflight harness
- Operator Test Expectation handoff pattern
- Branch Lifecycle check pattern
- Scenario Control Panel foundation
- Story-jump framework plumbing
- verification document pattern

Candidate components must be rewritten as generic plumbing before reuse. They should not retain Khovan scenario assumptions.

---

## 4. Khovan-Specific Material That Must Not Be Extracted

Do not extract these into a generic kernel:

- Khovan Reach scenario guide
- Artemis/Kestrel/Tarsis story assumptions
- Dillon, Anderson, or Hessler content
- pirate story content
- DAMCON story logic
- qualification cards
- Act I / Act II / Act III scene structure
- generator-governor or Tarsis gates
- Khovan-specific story-jump presets
- Khovan-specific mission states that are not generic lifecycle states

If examples are needed later, they must be clearly marked as sample mission content, not Khovan canon.

---

## 5. Required Generic Placeholders

A future kernel would need explicit placeholders such as:

- `MISSION_NAME`
- `PLAYER_SHIP_NAME`
- `INSTRUCTOR_NAME`
- `START_PHASE`
- `START_SCENE`
- `START_BEAT`
- `FIRST_CLIP_OR_MESSAGE`
- `STORY_JUMP_IDS`
- `GM_ADMIN_MODE_NAME`

Additional placeholders may be needed for faction names, map names, side IDs, console labels, player count settings, and GM-facing test text.

---

## 6. Risks

- Extracting too early may freeze unproven workarounds.
- Reference-mission patterns may not generalize to every Cosmos/MAST mission style.
- Khovan-specific assumptions may leak into future missions.
- Quick/static tests may be mistaken for live runtime proof.
- Breadcrumbs may become player-facing clutter if not gated or documented correctly.
- A template may encourage future projects to copy Khovan story structure instead of only using generic plumbing.
- The Scenario Control Panel and story-jump framework may need changes after the first real gameplay progression path.

---

## 7. Future Extraction Plan

When the extraction threshold is met:

1. Create a separate starter repo or a clearly named template branch.
2. Copy only generic plumbing.
3. Replace Khovan names with placeholders.
4. Remove Khovan-specific story, characters, factions, scene gates, and jump IDs.
5. Add sample mission content that is clearly non-canonical.
6. Preserve quick/static/preflight checks, but relabel them for the generic mission.
7. Verify the template by creating a fresh test mission from it.
8. Live-smoke the fresh test mission.
9. Document what remains live-runtime-only and cannot be proven statically.

The extraction should be treated as architecture/productization work, not as part of a Khovan gameplay slice.

---

## 8. Acceptance Criteria For Extraction

A future extracted kernel is acceptable only when:

- a new mission generated from the kernel loads
- the generated mission enters a playable bootstrap
- route breadcrumbs are logged
- the generated mission supports one sample story progression
- quick tests pass
- MAST compile/preflight checks pass where available
- live smoke passes
- no Khovan-specific strings remain except in examples clearly marked as examples
- documentation states which behaviors remain live-runtime-only

Until these criteria are met, the reusable kernel remains a planning idea, not a deliverable.
