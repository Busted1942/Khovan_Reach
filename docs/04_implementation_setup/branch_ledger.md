# Branch Ledger

Status: lightweight implementation branch ledger
Last updated: 2026-06-07

Purpose: record active/recent Khovan branch roles, evidence, risks, and next actions from observable Git history. Do not treat this file as a substitute for `git log`, `git branch --all`, or source authority in `docs/00_project/00_source_index.md`.

Current observed branch state:

- Current branch: `master`
- Current `master` tip: `f05a47d merge Slice 04 generator-governor start`
- `git status --short --branch`: clean at `master...origin/master`
- Current visible Slice 04 integration branch: `slice04-generator-governor-start`

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
