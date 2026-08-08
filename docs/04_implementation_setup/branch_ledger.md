# Branch Ledger

Status: lightweight implementation branch ledger
Last updated: 2026-08-08

Purpose: record active/recent Khovan branch roles, evidence, risks, and next actions from observable Git history. Do not treat this file as a substitute for `git log`, `git branch --all`, or source authority in `docs/00_project/00_source_index.md`.

Current observed branch state:

- Current branch: `slice06-drone-contact-fire`
- Current tip: `9bd4db9 docs: record Slice 06 GM-only live smoke pass (partial)`
- `git status --short --branch`: clean at `## slice06-drone-contact-fire` (not yet pushed to origin as of this entry)
- `master` remains at `6ff6f68 merge Slice 05 engineering shakedown` as of this entry; Slice 06 work has not merged back yet
- 36 local+remote branch refs exist as of this entry, most of them merged Slice 04 children already marked deletable below. Branch cleanup is still outstanding (see `docs/04_implementation_setup/70_agent_handoff_protocol.md` section 7).

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
