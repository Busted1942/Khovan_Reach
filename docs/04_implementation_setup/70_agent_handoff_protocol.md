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
- driving live smoke with the operator and recording the result
- promoting **[UNPROVEN]** to **[LIVE]** in the API cookbook

## 2.2 Implementation agent (Codex)

Owns bounded, well-specified construction:

- writing MAST for a single packet
- writing the matching static tests
- wiring the test file into `run_tests.py`
- drafting the verification record's static sections

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

**Runtime owner model.** Which file owns which route, timer, and state group. Prevents two files racing on the same gate.

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

---

# 4. Verification record — the output contract

One file per slice, `tests/SLICEnn_VERIFICATION.md`.

## 4.1 Required structure

Keep these two parts separate. They have different lifetimes.

**Part 1 — Contract (living).** What the slice claims, now. Rewrite in place as the slice evolves. Target under 150 lines.

```text
## Status
    one of: spike-in-progress | implemented-live-unproven | live-proven | blocked
## Source Sections Used
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

## 4.3 Claim discipline

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

## 5.2 Implementation agent constraints

An implementation agent working from a packet **must not**:

- change any file under `docs/01_design/` or `docs/02_content/` — design conflicts are routed back as findings, never resolved in place
- invent MAST syntax not present in the cookbook — use the section 12 uncertainty format instead
- exceed `Files to modify` without surfacing it
- implement anything in `Do not implement`
- claim live proof, tests run, commits made, or merges performed that did not happen
- create parallel files named `final`, `new`, `copy`, `old`, `merged`, `v2`, or `patched`

## 5.3 Implementation agent → planning agent

Return:

1. The diff.
2. The verification record Part 1, with `Acceptance Not Covered` honestly filled.
3. `python run_tests.py quick` output, verbatim.
4. Any API-uncertainty blocks raised.
5. The completion report from `AGENTS.md` section 4:

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

Before the operator is asked for live smoke, the planning agent checks:

- [ ] Every packet field was addressed, or the gap is stated
- [ ] No new `shared` name collides with an existing one
- [ ] Every automatic gate has a fallback path
- [ ] Every delayed task has a run-ID guard
- [ ] Every spawn has an existence check and a cleanup routine
- [ ] Every `artemis_id` use is guarded against 0
- [ ] Nothing in `Do not implement` was implemented
- [ ] No design doc was modified
- [ ] `python run_tests.py quick` passes, or the failure is documented
- [ ] `git diff --check` is clean

---

# 6. Operator test expectation

Per `AGENTS.md` section 6, any request for operator action must include the full block. Never say only "run this."

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
