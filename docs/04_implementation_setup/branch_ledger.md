# Branch Ledger

Status: lightweight implementation branch ledger
Last updated: 2026-08-08

Purpose: record active/recent Khovan branch roles, evidence, risks, and next actions from observable Git history. Do not treat this file as a substitute for `git log`, `git branch --all`, or source authority in `docs/00_project/00_source_index.md`.

Current observed branch state:

- Current branch: `docs/review-gate-tooling`
- `slice06-drone-contact-fire` tip: `b49f216 fix: shorten Kestrel reserve confirmation`
- `master` remains at `6ff6f68 merge Slice 05 engineering shakedown` as of this entry; Slice 06 work has not merged back yet
- 36 local+remote branch refs exist as of this entry, most of them merged Slice 04 children already marked deletable below. Branch cleanup is still outstanding (see `docs/04_implementation_setup/70_agent_handoff_protocol.md` section 7).

## docs/review-gate-tooling

Role: docs/governance + review-tooling branch

Started from: `slice06-drone-contact-fire` at `b49f216`, with a clean tree (per `AGENTS.md` branch-transition discipline — no uncommitted runtime changes carried in).

Purpose: mechanize the seven pattern/Git checks in `70_agent_handoff_protocol.md` section 5.4 so reviewing a Codex diff does not require reading whole MAST files by hand, and close a blind spot in the shared-name collision check.

Files: `tools/review_gate.py` (new), `tests/test_review_gate_static.py` (new), `run_tests.py`, `docs/04_implementation_setup/70_agent_handoff_protocol.md`, `docs/04_implementation_setup/branch_ledger.md`. No mission runtime `.mast` file changed.

Status: complete. Landed directly on `slice06-drone-contact-fire` as `afce5b0`, NOT via the section 7 merge-back path. Recorded here as a deviation rather than corrected — see "Why this was not unwound" below.

### Why this was not unwound

The commit was authored on `docs/review-gate-tooling`, but the VS Code/Codex
side switched the checkout back to `slice06-drone-contact-fire` mid-task
(visible in reflog as `HEAD@{3}: checkout: moving from docs/review-gate-tooling
to slice06-drone-contact-fire`, a checkout the planning agent did not perform).
The commit therefore landed on the runtime branch, which `AGENTS.md` section 2
forbids for docs/governance work.

The intended correction was to rewind `slice06-drone-contact-fire` by one
commit and re-land via merge-back. Before that could run, Codex committed
seven further runtime commits on top (`ae94379` through `aa215c5`), leaving
`afce5b0` buried mid-history. Removing it now requires rebasing seven commits
of active runtime work on a branch another agent holds checked out — a
materially larger risk than the deviation it would correct.

Decision: leave history intact and record the deviation honestly. Rationale:

- the commit touches zero `.mast` files — docs, tooling, and tests only, so
  the harm the rule guards against (docs work contaminating runtime code) did
  not occur
- `python run_tests.py quick` passes at the current tip, 146 checks
- rewriting another agent's in-flight commits to tidy history trades a
  cosmetic problem for a real one

Process change adopted: the planning agent does not own the checkout in a
shared working directory. Verify `git rev-parse --abbrev-ref HEAD` immediately
before every commit rather than trusting a checkout made earlier in the same
task.

Evidence:

- `python run_tests.py quick`: PASS, 146 checks (12 harness, 134 Python tests), 0 failures, 0 warnings, compile preflight included.
- 31 self-tests in `tests/test_review_gate_static.py` cover both directions per check — violation detected AND clean code not flagged.
- Negative control on the strengthened shared-name check: emptying `ALLOWED_CROSS_FILE_SHARED` reports `artemis_id` in `scripts/main.mast` + `scripts/systems/playable_bootstrap.mast`. The pre-fix `^shared` pattern reported nothing, confirming the indent blind spot was real and is now closed.
- First run against the Slice 06 diff surfaced two findings, both verified genuine, zero false positives across 42 changed files.

Known risks: the gate proves pattern conformance only — evidence class "static tests" per `AGENTS.md` section 5. It cannot prove runtime behavior, and a clean run is explicitly not a complete review; five judgment checks remain with the reviewer.

Next action: no merge-back required — the work is already in `slice06-drone-contact-fire` history. Operator reviews the two findings in "Findings routed to operator" below. Delete the `docs/review-gate-tooling` branch pointer at the next branch cleanup; it is a marker for authorship, not unmerged work.

Return branch: `slice06-drone-contact-fire`.

## slice06-drone-contact-fire

Role: current Slice 06 implementation branch (Drone 01/Drone 02, Phase A target subsystem-damage spike)

Started from: `master` at `6ff6f68 merge Slice 05 engineering shakedown`.

Purpose: build and prove the mandatory target subsystem-damage spike required by the Slice 06 plan entry before the full Drone 01/Drone 02 drill is implemented.

Files: `scripts/acts/act1_drone_contact_fire.mast`, `tests/test_act1_drone_contact_fire_static.py`, `tests/SLICE06_VERIFICATION.md`, plus small touch-ups to Slice 04/05 files and `run_tests.py` wiring.

Status: active, in progress. Phase A GM-console mechanics (spawn/cleanup/visibility gating) are live-proven as of the 2026-08-08 GM-only smoke pass recorded in `tests/SLICE06_VERIFICATION.md`. Science/Comms/Weapons station behavior and the `Read Target Spike Status` readback remain unproven or ambiguous.

Evidence:

- Commit `ae95519 feat: add Slice 06 target subsystem-damage spike (Phase A, live-unproven)`.
- Commit `9bd4db9 docs: record Slice 06 GM-only live smoke pass (partial)`.
- `python run_tests.py quick`: PASS as of `9bd4db9` (0 failures, 0 warnings, 96 tests).
- Live smoke log in `tests/SLICE06_VERIFICATION.md` records a real finding: GM `Cleanup Target Spike` fires the same `//damage/destroy` hook a genuine Weapons kill would, via `sbs.delete_object()`. Needs a guard before Phase B trusts `destroyed_observed` as the Drone 02 completion signal.

Known risks: Phase B (full Drone 01/Drone 02 drill) must not start until the crewed Science/Comms/Weapons pass runs and the destroy-hook finding is resolved.

Next action: run the crewed live-smoke pass named in `tests/SLICE06_VERIFICATION.md` Next Action; resolve the status-readback ambiguity; add the destruction-source guard; then proceed to Phase B.

Return branch: `master`, once Phase A (or a documented fallback) is accepted.

## docs/plan-hardening

Role: docs/governance branch

Started from: `slice06-drone-contact-fire` at `ae95519`, after the Slice 06 Phase A spike was committed (per `AGENTS.md` branch-transition discipline — no uncommitted runtime changes were carried into the docs branch).

Purpose: add the agent-handoff foundation docs needed to build the remaining slices with a mix of Claude Code and Codex — `CLAUDE.md`, `docs/04_implementation_setup/60_mast_api_cookbook.md`, `docs/04_implementation_setup/70_agent_handoff_protocol.md` — and register them in the source index.

Status: merged back into `slice06-drone-contact-fire` via `33cd0c1 merge docs/plan-hardening: agent handoff foundations`. No runtime code changed.

Evidence:

- Commit `508c2e6 docs: add agent handoff foundations for mixed Claude/Codex build`.
- Merge commit `33cd0c1` on `slice06-drone-contact-fire`.
- `python run_tests.py quick`: PASS before and after merge.

Known risks: branch pointer remains after merge; local-only, not pushed to origin as of this entry.

Next action: no further work needed on this branch. Delete local branch when branch cleanup is approved.

Return branch: `slice06-drone-contact-fire`.

### Findings routed to operator (from the first review-gate run, 2026-08-08)

Both were found by `tools/review_gate.py --base master` against the Slice 06
diff and then verified by hand. Neither is fixed on this branch: one is a
design-doc question that section 8 says route rather than decide, and the
other is runtime MAST, which must not be edited from a docs/governance branch.

**Finding 1 — a design doc was edited during implementation work.**

`docs/01_design/10_mast_requirements.md` section 17 changed in the Slice 06
range: a 16-item build-slice list was deleted and replaced with a pointer to
`docs/01_design/50_implementation_slice_plan.md` section 5.

The edit itself looks correct — the deleted list duplicated the slice plan and
its closing line referenced `khovan_reach_implementation_slice_plan_v1.md`,
a filename that no longer exists in the active tree. The issue is process, not
content: `AGENTS.md` section 2 routes design conflicts to the operator instead
of resolving them in place, precisely so a good-looking edit does not slip
into canon unreviewed.

Options: (a) ratify the edit and note it in the doc's revision history, or
(b) revert it and re-land it as its own docs branch. Recommend (a) — the
change is sound and reverting costs more than it protects.

**Finding 2 — `khovan_drone_01_reset` yields without a run-ID guard.**

`scripts/acts/act1_drone_contact_fire.mast`, label `khovan_drone_01_reset`.
The label increments `drone_contact_sequence_run_id`, then does
`await delay_sim(seconds=1)`, then `await task_schedule(khovan_drone_01_spawn)`.
Incrementing a run id is not the same as checking one: nothing re-reads it
after the yield, so a story jump landing inside that one-second window resumes
the label and spawns Drone 01 into a scene that has already moved on.

Practical risk today is low — the window is one second and story jumps are
GM-driven. It rises sharply at Slice 15 (checkpoint/reload), where story jumps
become routine and this becomes an intermittent phantom-spawn bug that is
expensive to reproduce.

Fix shape is the cookbook section 5.1 pattern already used by
`khovan_drone_01_watch_stationary_hold` in the same file: capture the run id
before the delay, compare after it, bail on mismatch. Belongs in a Slice 06
implementation branch, not here.

## slice04-player-instruction-clarity

Role: implementation child branch / Slice 04 player-facing instruction clarity branch

Started from, if inferable: `slice04-generator-governor-start` at `d3d4e22`, inferred from reflog and merge graph.

Purpose: clarify Slice 04 player instructions; later fast-forwarded to include proof-station removal, zero-energy/docking compatibility, and Kestrel range-gate work.

Expected files: inferred from commits and merge graph; runtime Slice 04 files, active docs, and Slice 04 tests. Exact original expected file set is unknown.

Status: superseded/merged upward. Local and remote branch tips are `1eb2528 fix: gate Slice 04 Kestrel range checks`; that commit is included in `master` through merge `f05a47d`.

Evidence:

- Branch visible locally and remotely.
- Tip: `1eb2528 fix: gate Slice 04 Kestrel range checks`.
- Merge graph shows `f05a47d merge Slice 04 generator-governor start` includes this branch history.

Known risks: branch pointer remains after merge and may confuse future branch selection. Original branch purpose is narrower than current branch tip because it was fast-forwarded through later child work.

Next action: no implementation work required on this branch. Delete local/remote branch when branch cleanup is approved.

Return branch: `slice04-generator-governor-start` during integration; now `master`.

## slice04-remove-proof-station-start-state

Role: implementation child branch / proof-station removal and Slice 04 start-state branch

Started from, if inferable: `slice04-player-instruction-clarity` at `569c53a`, inferred from reflog and merge graph.

Purpose: remove temporary Comms proof station from production startup; later fast-forwarded to include zero-energy/docking compatibility and Kestrel range-gate work.

Expected files: inferred from commits; active Slice 04 runtime files, proof-station/static tests, active docs, and verification notes. Exact original expected file set is unknown.

Status: superseded/merged upward. Local and remote branch tips are `1eb2528 fix: gate Slice 04 Kestrel range checks`; included in `master` through merge `f05a47d`.

Evidence:

- Branch visible locally and remotely.
- Tip: `1eb2528 fix: gate Slice 04 Kestrel range checks`.
- History includes `ba794f3 fix: remove Slice 04 Comms proof station`.
- Merge graph shows this history included in `slice04-player-instruction-clarity`, `slice04-generator-governor-start`, and `master`.

Known risks: branch pointer remains after merge and may look like active Slice 04 work. Original branch purpose is narrower than current branch tip because it absorbed later child work.

Next action: no implementation work required on this branch. Delete local/remote branch when branch cleanup is approved.

Return branch: `slice04-player-instruction-clarity` during integration; now `master`.

## slice04-zero-energy-docking-compat-spike

Role: spike/experiment branch

Started from, if inferable: `slice04-remove-proof-station-start-state` at `ba794f3`, inferred from reflog and merge graph.

Purpose: prove/fix zero-energy startup compatibility with Kestrel/Tarsis flow and normal Tarsis docking/resupply after required Comms gates.

Expected files: inferred from commit `384405a`; active Slice 04 runtime, active docs, and Slice 04 static/verification tests. Exact original expected file set is unknown.

Status: superseded/merged upward. Local and remote branch tips remain at `384405a fix: complete Slice 04 zero-energy docking compatibility`; the commit is included in `master` through later branch integration.

Evidence:

- Branch visible locally and remotely.
- Tip: `384405a fix: complete Slice 04 zero-energy docking compatibility`.
- Commit is ancestor of `1eb2528`, which is included in `master` through merge `f05a47d`.

Known risks: branch tip is behind current Slice 04 integration (`1eb2528`) and does not contain the Kestrel 600 m reserve gate, 1 km launch-envelope gate, or objective marker work.

Next action: no implementation work required on this branch. Delete local/remote branch when branch cleanup is approved.

Return branch: `slice04-remove-proof-station-start-state` during integration; now `master`.

## spike-station-comms-docking-kernel

Role: historical spike evidence branch

Started from, if inferable: unknown from currently visible branches; branch was based after `309aed3 merge future reusable mission kernel plan` according to prior inspection before deletion. Current branch pointer is no longer visible in `git branch --all`.

Purpose: investigate station Comms/docking proof patterns with temporary kernel proof stations. Infer from branch name and prior read-only inspection.

Expected files: from prior inspection of commit `ce22aea`; `run_tests.py`, `scripts/main.mast`, `scripts/systems/station_comms_docking_kernel.mast`, `tests/STATION_COMMS_DOCKING_KERNEL_VERIFICATION.md`, and `tests/test_station_comms_docking_kernel_static.py`.

Status: deleted locally and remotely after being classified as superseded historical spike evidence. Not visible in current `git branch --all`.

Evidence:

- Prior read-only inspection identified tip `ce22aea Spike: prove station Comms docking kernel`.
- Prior inspection showed it added proof station startup wiring and station kernel tests/docs.
- Current `git branch --all` does not list the local branch or `origin/spike-station-comms-docking-kernel`.

Known risks: wholesale reuse would reintroduce temporary proof stations into active startup and contradict current Slice 04 cleanup. It did not prove mechanical docking/resupply.

Next action: do not restore or merge. Use only as historical evidence if recoverable from reflog or remote history; useful lessons already ported manually into Slice 04.

Return branch: unknown; now `master`.

## slice04-generator-governor-start

Role: current Slice 04 integration branch

Started from, if inferable: forked from mainline before current `master`; exact opening command unknown. Merge base with `master` before final integration was previously observed as `643f45d docs: note future reusable mission kernel`.

Purpose: consolidate Slice 04 generator-governor start, Kestrel departure/hold/reserve flow, Tarsis Comms gates, normal Tarsis docking/resupply, objective text, proof-station removal, and related docs/tests.

Expected files: active Slice 04 runtime, active docs, tests, and verification notes. Exact original expected file set is unknown.

Status: merged to `master` and pushed. Local and remote branch tips are `1eb2528 fix: gate Slice 04 Kestrel range checks`; `master` includes it through merge `f05a47d merge Slice 04 generator-governor start`.

Evidence:

- Branch visible locally and remotely.
- Tip: `1eb2528 fix: gate Slice 04 Kestrel range checks`.
- `master` tip: `f05a47d merge Slice 04 generator-governor start`.
- `git status --short --branch` clean on `master`.

Known risks: branch pointer remains after merge and may confuse future branch selection. Current branch name remains useful as integration evidence but should not receive new runtime work now that it is merged to `master`.

Next action: test on `master`; delete local/remote integration branch when branch cleanup is approved.

Return branch: `master`.
