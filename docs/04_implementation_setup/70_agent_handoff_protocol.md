# KHOVAN REACH — AGENT HANDOFF PROTOCOL

Version: 1.0
Status: active implementation process doc
Purpose: Define the contract between planning/review agents and implementation agents so Khovan Reach can be built by a mix of Claude Code and Codex without losing source authority, evidence discipline, or branch safety.

Pair with:
- `AGENTS.md` — branch lifecycle, source authority, operator test expectations (governing)
- `docs/01_design/50_implementation_slice_plan.md` — slice packet template and build slices
- `docs/04_implementation_setup/60_mast_api_cookbook.md` — proven MAST syntax
- `docs/01_design/40_admin_testing_plan.md` — test IDs and acceptance criteria

This file describes *process*. It does not define scenario design.

---

# 1. The problem this solves

Slice 04 shipped as a 970-line MAST file and a 1,326-line test file across roughly 20 commits and 15 branches. Its entry in the slice plan is 24 lines of bullets. Slices 09, 11, and 15 are each comparable in scope and currently have about 15 lines each.

An implementation agent handed "Build: pirate arrival timer / pirate state variables / suggested dialogue branch display" will invent a state tree, invent MAST syntax, and claim completion from static tests. All three failure modes are expensive to unwind.

The fix is a two-artifact contract:

```text
SLICE PACKET  ->  [implementation agent]  ->  VERIFICATION RECORD
```

Nothing enters implementation without a packet. Nothing is called complete without a record.

---

# 2. Agent roles

These are defaults. The operator may reassign any step, but the artifacts stay the same.

## 2.1 Planning / review agent (Claude Code)

Owns work that needs whole-repo context and judgment:

- branch lifecycle: opening, transitions, merge-back, ledger updates
- API-uncertainty resolution and spike design
- writing the slice packet
- reviewing the implementation diff against the packet
- running `python tools/review_gate.py` and resolving what it reports
- setting the verification record's `Status` and `Acceptance Not Covered` (see section 4.3)
- driving live smoke with the operator and recording the result
- promoting **[UNPROVEN]** to **[LIVE]** in the API cookbook

**Review by diff, not by file.** Read `git diff --stat` first, then scoped
`git diff -- <path>`. Opening whole runtime files costs an order of magnitude
more context than the change warrants — `act1_generator_tarsis_gate.mast` is
969 lines and its typical slice diff is a few dozen. Read the whole file only
when the change is structural or the diff genuinely cannot be understood
without surrounding context.

## 2.2 Implementation agent (Codex)

Owns bounded, well-specified construction:

- writing MAST for a single packet
- writing the matching static tests
- wiring the test file into `run_tests.py`
- drafting the verification record's static sections, **except** `Status` and
  `Acceptance Not Covered` — see section 4.3
- citing a cookbook section and evidence tag for every MAST pattern used

## 2.3 Operator (human)

Owns everything the agents cannot observe:

- launching Cosmos and running live smoke
- reporting expected/failure/ambiguous observations
- approving branch merges, deletions, and design changes
- resolving source-authority conflicts

---

# 3. Slice packet — the input contract

The template is `docs/01_design/50_implementation_slice_plan.md` section 2. A packet is complete when every field is filled with a specific answer. "TBD" in any field means the packet is not ready to hand off.

```text
Slice ID:
Goal:
Source docs:                     exact files and section numbers
Files to modify:                 exact paths, including test files and run_tests.py
Runtime owner model:             which file owns which state and route
State variables needed:          exact names; must not collide with existing shared names
Branch type:                     implementation | docs/governance | architecture feedback | spike/experiment | emergency fix
Starting branch:
Expected return branch:
Branch lifecycle plan:
Runtime/live-smoke allowed from this branch:
Merge-back required:
Implementation tasks:            ordered, each one testable
Tests required:                  by test ID from 40_admin_testing_plan.md
Acceptance criteria:
Expected observations:
Failure/ambiguous observations:
What remains unproven:
Next action by result:
Known risks:
Do not implement:                explicit out-of-scope list
```

## 3.1 Fields that carry the most weight

**State variables needed.** List exact names before any code is written. State-name collision across MAST files is the most expensive class of bug in this codebase, because `shared` is global and failures are silent. Cross-check against existing names with a repo-wide grep before writing the packet.

**Runtime owner model.** Which file owns which route, timer, and state group. Prevents two files racing on the same gate. For Act I, see `docs/01_design/10_mast_requirements.md` section 7 "Scene ownership matrix" — every scene is already classified as AUTO / GM-SUP / GM-DRIVE with stated runtime and GM responsibilities. For Acts II/III, fill explicitly in the packet since no equivalent matrix exists.

**Do not implement.** Slice 01A's out-of-scope list is the model — it names twelve specific mechanics. Scope creep in this project historically arrives as "while I was in there."

**Tests required.** Name actual IDs (`ACT1-019`, `DAMCON-004`), not ranges in prose. A range is not a checkable claim.

## 3.2 Packet sizing rule

If a packet's `Implementation tasks` exceed roughly 8 items, or `Files to modify` exceed 4 runtime files, split it. Slice 06 is the model: **Phase A spike, then Phase B build**, with the phase boundary being a live-smoke gate.

Slices that should carry an explicit spike phase, based on their API risk:

| Slice | Spike must prove |
|---|---|
| 06 (in progress) | target subsystem damage, Weapons selection, destruction events, stock-menu suppression |
| 09 DAMCON | timer persistence, report scheduling under story jump, irreversible-loss flag |
| 11 pirates | arrival timer, state transitions, docking backstop |
| 12 combat | force authorization, hostile transition, outcome persistence |
| 15 reload | checkpoint payload round-trip, irreversible state preservation |

**Important note on gate maps:** `docs/01_design/10_mast_requirements.md` section 8.9 provides the only canonical automation gate map — it covers Act I only. Acts II/III have no equivalent gate map yet. Slices 07–16 must define their own gate/fallback pairs in their packets since no pre-computed table exists. This is a real design cost but prevents false assumptions about what Cosmos exposes.

---

# 4. Verification record — the output contract

One file per slice, `tests/SLICEnn_VERIFICATION.md`.

## 4.1 Required structure

Keep these two parts separate. They have different lifetimes.

**Part 1 — Contract (living).** What the slice claims, now. Rewrite in place as the slice evolves. Target under 150 lines.

```text
## Status
    one of: spike-in-progress | implemented-live-unproven | live-proven | blocked
    SET BY THE REVIEWER, not the implementation agent - see section 4.3
## Source Sections Used
## Cookbook Patterns Used
    one line per MAST pattern: section number + evidence tag + where used
## Files Touched
## State Variables
## Runtime Flow
## GM Controls
## Player-Facing Behavior
## Tests/Static Checks
## Acceptance Covered
## Acceptance Not Covered
## Known Risks/API Uncertainties
## Next Action
```

**Part 2 — Live smoke log (append-only).** One dated block per live run, newest last. Never edit an earlier block.

`tests/SLICE04_VERIFICATION.md` is 649 lines because these two parts were interleaved. Every agent that opens the repo pays that cost in context. Split on next edit.

## 4.2 Live smoke result block

Live results must be recorded in a fixed, greppable shape so the next agent can read outcomes without reading prose:

```text
### LIVE SMOKE 2026-06-07
branch: slice06-drone-contact-fire
commit: ae95519
build: Cosmos <version>
result: PASS | FAIL | AMBIGUOUS | PARTIAL

checks:
- ACT1-019: PASS   drone 01 spawned non-attacking
- ACT1-020: FAIL   science scan gate did not fire
- ACT1-021: AMBIG  no error, no marker

trace_marker_last: [KHOVAN ACT1 DRONE SPIKE SPAWN]
blocker:
next action:
```

`AMBIGUOUS` is a first-class result. No error plus no marker is not a pass.

## 4.3 Who owns which field

Two fields are set by the reviewer, never by the implementation agent:

- `Status`
- `Acceptance Not Covered`

Everything else in Part 1 may be drafted by the implementation agent.

The reason is narrow and specific. These two fields are where the slice
declares what it has *not* proven, and section 5 of `AGENTS.md` identifies
overstated evidence as the failure mode agents hit most often here. An agent
grading its own coverage is being asked to write down the weakness of work it
just produced. That is not a claim about any particular agent's honesty — it
is that the two fields exist precisely to catch the optimism the author
cannot see in their own work, so the author is the wrong person to write them.

Cost of the rule: two lines per slice, set at review. There is no ongoing
overhead.

## 4.3.1 Cookbook citation format

Every MAST pattern in the diff must trace to `60_mast_api_cookbook.md`. One
line each in `Cookbook Patterns Used`:

```text
- section 5.1 [LIVE] run-ID guard - khovan_drone_01_watch_stationary_hold
- section 8.1 [LIVE] idempotent spawn - khovan_drone_01_spawn
- section 7.3 [COMPILE] subsystem damage read - khovan_drone_01_damage_hook
```

This converts review from a judgment task into a lookup: the reviewer greps
the cited section and confirms it says what the citation claims, instead of
reading MAST and reasoning about whether an API is real. `AGENTS.md` section 4
is blunt about why this matters — invented syntax compiles surprisingly often
and fails only in live Cosmos, where each round trip costs an operator
session.

A pattern that cannot be cited is not a blocker and must not be guessed at.
Raise it as a cookbook section 12 uncertainty block and route it back.

## 4.4 Claim discipline

Restating `AGENTS.md` section 5, because this is the rule implementation agents break most often:

- Static checks prove file/text structure only.
- MAST compile preflight proves `story.mast` and imported files compile. It does **not** prove runtime values, GUI lifecycle, player assignment, renderer behavior, or playability.
- Only live Cosmos proves live behavior.
- A breadcrumb marker string proves the marker was reached, not that the feature works.
- If live Cosmos contradicts static tests, **live wins.** Update the record, add a regression check, and do not claim the slice complete.

---

# 5. Handoff sequence

## 5.1 Planning agent → implementation agent

Before handoff, confirm and state:

```text
git status --short --branch
git log --oneline -5
python run_tests.py quick
```

Hand over exactly:

1. The completed slice packet.
2. `AGENTS.md` (governing).
3. `docs/04_implementation_setup/60_mast_api_cookbook.md` (syntax authority).
4. The specific source-doc sections named in the packet — sections, not whole files.
5. The prior slice's verification record if this slice depends on its state.

Do not hand over the full docs tree. Context spent on unrelated design docs is context not spent on the packet.

## 5.1.1 Player-facing message channel rule

**Operator ruling, 2026-08-08.** Applies to every slice from 07 onward.

For anything the mission needs to say to players — progress, gate status,
instructions, advisories — use the current-objective broadcast channel:

```mast
    await task_schedule(khovan_set_current_objective, {...})
```

which reaches players via `comms_broadcast()` in `current_objective_panel.mast`.
That channel is live-confirmed working and renders correctly on player consoles.

**Do not use a GM-only `comms_receive()` route to carry player-facing content.**
Every GM-only `comms_receive()` call tested in this build executes correctly and
has never rendered visibly, across 3+ live sessions. Cookbook section 6.2 carries
the full evidence and has downgraded the bare shape to
`[UNPROVEN — DISCONFIRMED FOR GM ROUTES]`.

GM status visibility leans on the Scenario Control Panel overview and the trace
log until the rendering question is resolved.

**Known affected, not yet fixed:** `scripts/systems/scenario_control_panel.mast`
(5 calls) and `scripts/systems/story_jump_presets.mast` (3 calls) still use the
disconfirmed bare shape and have never been independently confirmed to render for
the GM. If the `comms_override` experiment in `act1_drone_contact_fire.mast` is
confirmed live, both need the identical fix.

**This is deprioritized, not open.** The operator judged further live-smoke cycles
on GM rendering a poor use of session time relative to building the mission out.
Do not spend a live-smoke session on it unprompted; diagnose from the trace log if
it is picked up again. If the `comms_override` experiment also fails, there is no
third proven shape in the cookbook — escalate as an API uncertainty rather than
guessing further.

## 5.2 Implementation agent constraints

An implementation agent working from a packet **must not**:

- change any file under `docs/01_design/` or `docs/02_content/` — design conflicts are routed back as findings, never resolved in place
- invent MAST syntax not present in the cookbook — use the section 12 uncertainty format instead
- exceed `Files to modify` without surfacing it
- implement anything in `Do not implement`
- claim live proof, tests run, commits made, or merges performed that did not happen
- create parallel files named `final`, `new`, `copy`, `old`, `merged`, `v2`, or `patched`
- set `Status` or `Acceptance Not Covered` in the verification record (section 4.3)
- use a MAST pattern without citing its cookbook section and evidence tag (section 4.3.1)

**Helper extraction rule.** `docs/04_implementation_setup/10_mast_file_lessons.md` section 3.4 names six helper modules (`act1_helpers`, `entity_cleanup_helpers`, `resupply_helpers`, `drone_spawn_helpers`, `target_detection_helpers`, `checkpoint_system`) as one of the best old-build lessons, but `scripts/lib/` is currently empty and all logic lives in act/system files. When a slice would push a single `.mast` file past roughly 400 lines, or when two slices need the same cleanup/seeding/spawn logic, extract the shared logic to `scripts/lib/` rather than growing the act file further. This is cheapest to enforce before Slices 09 (DAMCON), 11 (pirates), and 15 (checkpoint/reload) land — each adds a state tree comparable to Slice 04's, and the lessons doc specifically expects checkpoint/reload to reuse neutral helpers rather than duplicate story-jump seeding logic. Their packets (section 3 of this doc, once written) should name `scripts/lib/` targets explicitly for entity cleanup, spawn, and checkpoint-seed helpers.

`scripts/acts/act1_generator_tarsis_gate.mast` is already at 969 lines / 78 `shared` variables. This is accepted technical debt, not a defect: the file carries the deepest live-smoke history in the repo (multiple confirmed live findings and fixes — see `tests/SLICE04_VERIFICATION.md`, which still lists items in "What Remains Unproven"), and a speculative refactor risks regressing the parts of the mission with the most live evidence behind them. Do not "fix" it unprompted — only touch it if a specific slice packet requires a change inside it.

## 5.3 Implementation agent → planning agent

Return:

1. The diff.
2. The verification record Part 1, with `Acceptance Not Covered` honestly filled.
3. `python run_tests.py quick` output, verbatim.
4. Any API-uncertainty blocks raised.
5. The completion report from `AGENTS.md` section 7:

```text
Starting branch:
Ending branch:
Branch type:
Commits created:
Merge performed:
Tests run:
Files changed:
Remaining uncommitted changes:
Next safe branch/action:
```

## 5.4 Review gate

Before the operator is asked for live smoke, the planning agent runs:

```bash
python tools/review_gate.py --base master
```

That tool answers the mechanizable half of this gate and exits non-zero on any
failure:

- [x] No design or content doc was modified, or the edit carries a dated
      in-document operator ratification (reported as `NOTE`, not `FAIL`)
- [x] No parallel `final`/`new`/`copy`/`old`/`merged`/`v2`/`patched` filename
- [x] No forbidden bootstrap API reintroduced
- [x] Every `to_object()` is None-checked
- [x] Every ship API call on `artemis_id` is guarded against 0 in its label
- [x] Every delayed task has a run-ID guard
- [x] Every spawn has an existence check and a cleanup routine
- [x] `python run_tests.py quick` passes, and the compile preflight actually ran
- [x] `git diff --check` is clean

Shared-name collisions are covered separately and continuously by
`check_duplicate_shared_declarations()` in `run_tests.py`, so a collision
fails `quick` for everyone rather than only at review.

The remaining checks need judgment and stay with the reviewer. **A clean tool
run is not a complete review:**

- [ ] Every packet field was addressed, or the gap is stated
- [ ] Every automatic gate ships with a Comms/GM fallback and a `*_fallback_available` flag
- [ ] Nothing in `Do not implement` was implemented
- [ ] Every MAST pattern cites a cookbook section and evidence tag (section 4.3.1)
- [ ] `Status` and `Acceptance Not Covered` set by the reviewer (section 4.3)

**Design-doc ratification.** An implementation agent must never edit
`docs/01_design/` or `docs/02_content/`; that rule is unchanged. When an edit
has already happened and the operator decides to keep it rather than revert,
record the decision as a dated note in the affected document itself:

```text
**Revision note (operator-ratified YYYY-MM-DD).** <what changed and why kept>
```

The gate then reports that file as `NOTE` instead of `FAIL`. Without this, a
ratified edit fails the gate on every future run, and a check that fails
forever on an accepted condition is one reviewers learn to skip. The marker is
a visible claim inside mission canon that a human can audit — it is not a way
to pre-authorize an edit, and `AGENTS.md` section 5 already forbids recording
an approval that did not happen.

**Every gate rule is bound to the prose that governs it.**
`tools/review_gate.py` carries a `RULE_CITATIONS` table mapping each check to
the `AGENTS.md` or cookbook section it enforces, and
`tests/test_review_gate_static.py` fails the build if a check runs without a
citation, if a citation names a heading that no longer exists, or if a citation
is left behind by a removed check.

This exists because the two drifted once. On 2026-08-08 the run-ID check was
widened to accept two further patterns while cookbook 5.1 still described only
one, so the tool was passing shapes the documentation did not describe — a
reviewer following the cookbook would have flagged code the gate had already
approved. Neither file was wrong alone; nothing was watching the seam.

Practical effect: **adding a gate rule now requires documenting it.** Write the
prose first, cite it in `RULE_CITATIONS`, then implement the check.

**Scoping.** The tool reads added lines, not whole files. `scripts/acts/`
carries accepted live-proven debt (see `AGENTS.md` section 2 on
`act1_generator_tarsis_gate.mast`); a whole-repo linter would fail on that
debt from day one and be silenced within a week. Guard lookups still read the
full current file, since the guard protecting a new line is often pre-existing.
Use `--full` deliberately when auditing a whole file, and expect known debt to
surface.

---

# 6. Operator test expectation

Per `AGENTS.md` section 9, any request for operator action must include the full block. Never say only "run this."

```text
What changed:
What to run or do:
Expected observation:
Failure/ambiguous observation:
What remains unproven:
Next action by result:
```

`Expected observation` and `Failure/ambiguous observation` are mandatory for every manual or live test.

For negative-control tests, state explicitly that an expected failure means the control passed, and include the restore step.

---

# 7. Branch discipline in a two-agent workflow

One agent per branch at a time. Concurrent agents on one branch produce interleaved commits that cannot be attributed or reverted cleanly.

- Implementation work → `slice<nn>-<topic>`
- Spike work → `slice<nn>-<topic>-spike`, merged or discarded deliberately
- Process/docs work → `docs/<topic>`, merged back before runtime work resumes

Do not carry docs/governance changes into a runtime implementation branch, and do not start docs work from a branch with uncommitted runtime changes. Commit or stash first.

Record every branch in `docs/04_implementation_setup/branch_ledger.md` with role, status, evidence, risks, and next action. Prune merged branches once the ledger records them — the current 20-branch spread makes branch selection a guessing game for a fresh agent.

---

# 8. Escalation

Route back to the operator, do not decide alone, when:

- two active source docs conflict (Slice 06 hit this on Drone 02 destroy-vs-disable)
- a packet requires an API the cookbook does not cover and Tier 2 material does not answer
- live smoke fails in a way that implies a design change
- the packet cannot be implemented without touching `Do not implement`
- a slice turns out to be more than roughly 8 tasks once opened

Surface it as a finding with options and a recommendation. Do not silently change scenario intent to fit implementation convenience.
