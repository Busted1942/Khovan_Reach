# AGENTS.md — Khovan Reach Implementation Agent Rules

Status: repo-root governing control file for every coding/documentation agent working here — Claude Code, Codex, or any other tool
Purpose: Keep agents aligned with the active repo-consolidated source set, Git/GitHub discipline, test-first delivery, branch lifecycle safety, and operator-facing test expectations, regardless of which AI is driving.

This file is tool-agnostic by design. Tool-specific entry files (`CLAUDE.md`, `CODEX.md`) exist only as short pointers here — see `docs/00_project/00_source_index.md` section 2 for the full list. Do not fork rules into a tool-specific file; if a rule applies, it belongs here so every agent sees the same one.

---

# 1. Source authority

Use `docs/00_project/00_source_index.md` as the source map. Nothing outside that map is authority.

Do not treat old Pass files, old MAST files, patch bundles, archived notes, reference missions, generated files, or local clones as current scenario authority unless explicitly promoted.

Do not create parallel active files with names like `final`, `new`, `copy`, `old`, `merged`, `v2`, or `patched`. Edit stable canonical paths in place and rely on Git history for versioning.

Do not reference `archive/`, `docs_external/_local_clones/`, `reference_missions/_local_clones/`, or `old_mast` from any runtime file. **Git-ignored folders are not runtime-ignored** — Cosmos scans the whole mission directory, not just files reachable from `story.mast`. A stray live `.mast` file sitting in an ignored folder can still collide by filename with an active or future runtime file.

---

# 2. Work boundaries

Implementation agents may change runtime code, tests, documentation, and tooling only within the requested task scope.

If implementation discovers an architecture issue, surface it as a finding, blocker, source-update proposal, or slice-plan change. Do not silently change scenario intent to fit implementation convenience.

## The findings return path

Design flows down; evidence has to flow back up, or the design document stays confidently wrong and the correction survives only as long as someone remembers the conversation. Implementation still never edits `docs/01_design/` or `docs/02_content/` — but "surface a finding" is not a format, and a finding written as loose prose gets lost.

File findings in the slice's verification record, under a `## Findings routed to the operator (<date>)` heading, one entry each, carrying all five fields:

```text
Claim touched:  the design statement this bears on, quoted or cited by file and line
Evidence class: from the section 5 table - asserted / static / preflight / observed / measured
Disposition:    confirmed | amended | overturned | unproven | blocked
Owner:          who makes the resulting edit - never the implementing agent
Dependency:     what has to happen first, or "none"
```

Rules that make the path work:

- **Disposition is a closed vocabulary.** Anything outside those five words is prose, and prose cannot be counted or filtered.
- **Overturned requires attached evidence** at observed or better. An overturned claim without a measurement is just disagreement.
- **Correct the record where it was wrong, do not silently rewrite it.** The superseded claim stays readable, dated, next to the finding that killed it. See cookbook 17.11 — a silent edit erases exactly the evidence that stops the next agent re-deriving the same appealing error.
- **State conclusion posture.** A finding either recommends (and justifies) or lays out a tradeoff and names the decision as the operator's. Mixing the two is how a recommendation gets mistaken for a decision.

Do not change scenario design, player-facing content, qualification criteria, DAMCON timing, Hessler behavior, pirate fiction, or debrief content unless the task explicitly targets those docs. Concretely, this means: **do not edit `docs/01_design/` or `docs/02_content/` during implementation work.** Design conflicts are surfaced as findings and routed to the operator — never resolved in place, never worked around silently.

Do not reintroduce `artemis_ship_name`, `sim_create()`, `player_spawn(`, or `assign_client_to_ship` into the bootstrap path. LegendaryMissions owns the console and player-spawn lifecycle; Khovan only binds state to the ship it creates.

Do not carry docs/governance changes into a runtime implementation branch, or start docs work from a branch with uncommitted runtime changes — see section 7 for the full branch-transition checklist.

---

# 3. Orientation — read order and repo shape

Read in this order before any artifact-changing work:

1. This file — governing.
2. `docs/00_project/00_source_index.md` — which files are canonical.
3. `docs/04_implementation_setup/70_agent_handoff_protocol.md` — the slice-packet-in / verification-record-out contract.
4. `docs/04_implementation_setup/60_mast_api_cookbook.md` — proven MAST syntax. Read before writing any `.mast`.
5. The specific design sections named in the current slice packet — sections, not whole files. Context spent on unrelated design docs is context not spent on the packet.

## Commands

```bash
python run_tests.py quick
```

`quick` is the only supported invocation. There is no full/slow mode.

**Portability note:** this repo is documented with `python`, which is correct on the Windows box this mission is built on. Most Linux/macOS sandboxes (including cloud coding-agent environments) only expose `python3` by default. If `python run_tests.py quick` fails with a not-found error, retry as `python3 run_tests.py quick` before concluding the harness is broken.

**Portability note:** `python run_tests.py quick` includes a MAST compile-preflight check (see section 5) that requires a locally installed `artemis-sbs.sbs_utils.*.sbslib` outside this repo (`../__lib__/` relative to the mission root). That file is part of the Cosmos/Artemis install, not something to add to version control — do not copy it into this repo to "fix" portability; that trades a missing-evidence problem for a binary-in-git and licensing problem. On a machine without Cosmos installed (e.g. a cloud sandbox with no local game install), this check is designed to skip rather than fail the build, and `quick` still reports an overall PASS if nothing else fails. Read the actual warning line, not just the summary — a PASS on a machine without Cosmos installed is missing the strongest evidence class in section 5's table, even though the top-line result looks identical to a PASS with the compile check included. Do not claim compile-preflight coverage from a machine where this dependency is absent.

## Repo shape

```text
story.json / script.py / story.mast   mission package entry (root, required by Cosmos)
scripts/main.mast                     imports every active runtime file
scripts/systems/                      cross-cutting: bootstrap, objective panel, GM control panel, jumps
scripts/acts/                         act/scene gameplay gates
scripts/lib/                          shared helpers
tests/                                static tests + per-slice verification records
docs/01_design/                       scenario canon - DO NOT EDIT during implementation
docs/04_implementation_setup/         handoff, API, and findings docs
archive/, docs_external/, reference_missions/   reference only, never runtime-referenced
```

Load chain: `story.json → script.py → story.mast → LegendaryMissions.server_console → scripts/main.mast @map/khovan_reach`.

---

# 4. Writing MAST

Use `docs/04_implementation_setup/60_mast_api_cookbook.md`. Every pattern in it is cited to a working file in this repo and tagged **[LIVE]** / **[COMPILE]** / **[UNPROVEN]**.

**Do not write MAST from memory.** If the cookbook does not cover it, use the API-uncertainty format in cookbook section 12 rather than guessing. Invented syntax compiles surprisingly often and fails only in live Cosmos, where each round trip costs an operator session.

Non-negotiable patterns, all learned from real failures:

- Guard `if artemis_id == 0: ->END` before any ship API call.
- None-check every `to_object()`.
- Every delayed task carries a run-ID guard so story jumps invalidate it.
- Every automatic gate ships with a Comms/GM fallback and a `*_fallback_available` flag.
- Every spawn has an existence check and a cleanup routine.
- Duplicate-suppress every player-facing message.
- Set a status string on every branch, including failure branches — the GM overview reads them.

---

# 5. Evidence classes

Never conflate these. This is the rule most often broken here.

| Class | Proves | Does not prove |
|---|---|---|
| Asserted | nothing | anything — a claim with no evidence is E0, however reasonable it sounds |
| Static tests | file/text structure | anything at runtime |
| MAST compile preflight | `story.mast` + imports compile | runtime values, GUI lifecycle, player assignment, renderer behavior, playability |
| **Live observed** | it happened once, under one configuration | that it repeats, or holds outside the case tried |
| **Live measured** | actual behavior — instrumented, reproduced, paired against an expected value | — |

**Split "live" into observed and measured.** These used to be one row and the conflation shipped a defect. A single observation tells you the action worked *that time*; it does not tell you the action is repeatable, and a rule written from it will be stated as though it is.

**Guidance and player-facing copy may only be written from live measured.** If you are about to turn a finding into an instruction a crew or another agent will follow, the finding has to have been reproduced. The cheapest promotion from observed to measured is the one nobody runs: **do the working thing twice.**

Worked example, 2026-08-16 — "damage the target, then scan, and the panel is correct" was a correct live *observation*. It was generalized into the coaching line "Scan her again after every hit", which is false: re-scanning an already-scanned band returns the engine's cache. The cache is per band, and the original experiment never scanned twice. See cookbook 7.3 and 17.10.

A breadcrumb marker in `tests/live_startup_trace.txt` proves the marker was reached, not that the feature works. If live Cosmos contradicts static tests, **live wins.** Update the record, add a regression check, and do not claim the slice complete until the live failure is fixed or documented as a blocker.

Report honestly: never claim files were edited, tested, committed, pushed, merged, or live-smoked unless that action actually happened. This applies to every result an agent records, not only final claims — a "Pass" written into a verification record based on a report is not the same evidence class as a "Pass" verified against the trace log, and the two must not be conflated either.

---

# 6. Git and GitHub discipline

Before artifact-changing work, inspect:

```text
git status --short --branch
git remote -v
git log --oneline -5
```

Before commit, inspect:

```text
git status --short --branch
git diff --stat
```

Keep commits coherent and source-referenced. Do not commit secrets, unrelated debris, accidental generated files, local clones, caches, or unreviewed large binaries.

---

# 7. Branch Lifecycle and Return-to-Work Checks

Before artifact-changing work, confirm branch lifecycle state. Do not rely on `git status` alone; identify whether the current branch is appropriate for the task.

## Branch opening

Run:

```text
git status --short --branch
git log --oneline -5
```

Identify:

```text
Starting branch:
Branch type: implementation | docs/governance | architecture feedback | spike/experiment | emergency fix
Task purpose:
Expected files:
Expected return branch:
Runtime/live-smoke allowed from this branch: yes/no
```

Do not edit until the branch matches the task.

## Branch transitions

Before switching branches, run:

```text
python run_tests.py quick
git status --short --branch
git diff --stat
```

If the quick test command is unavailable, document that directly.

Commit, stash, or intentionally discard local changes before switching. Do not carry unresolved docs/test/governance changes into runtime implementation work, and do not start docs work from a branch with uncommitted runtime changes.

## Docs/governance branch closing

Before closing or merging a temporary docs/governance branch:

- run quick tests if available
- inspect changed files
- confirm no mission runtime code changed unintentionally
- confirm no scenario design changed unintentionally
- commit with a docs/governance-specific message

## Merge-back and return to implementation

After a docs/governance or architecture-feedback branch is complete, merge it intentionally into the active implementation branch.

After merge:

```text
python run_tests.py quick
git status --short --branch
```

Before running implementation prompts, live-smoke prompts, or Cosmos tests, confirm:

- current branch is the intended implementation branch
- latest docs/governance updates are merged
- quick tests pass or the failure is documented
- no docs-only branch is active

If on a docs-only, governance, or architecture-feedback branch, stop and switch back before runtime testing unless explicitly approved.

## Completion report

Report:

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

Assistants should proactively guide branch opening, closing, merge-back, and return-to-work steps. Do not wait for the user to ask when branch lifecycle state materially affects safety or recoverability.

---

# 8. Runtime Load and GUI Lifecycle Testing

For Cosmos/MAST work, `python run_tests.py quick` must protect the active runtime load path, not just source hygiene.

Quick tests should fail when active runtime files reference:

- missing `.mast` files
- archived old-build files
- external reference clone paths
- forbidden old module names
- files outside the active mission load path

When available, quick should also run the installed SBS Utils / MAST compile-preflight path. This is the middle evidence class from section 5: stronger than text-only static checks because it compiles `story.mast` and imported active MAST files, but weaker than live Cosmos smoke because it does not prove runtime values, GUI/page lifecycle, player assignment, renderer behavior, or server/client playability.

When live Cosmos reports a missing load file, add a targeted regression check so the same class of failure is caught by `quick` before the next live run.

For SBS Utils / MAST bootstrap work, quick tests should also check the lifecycle contract where practical:

- root `story.mast` reaches the active Khovan entry path
- `scripts/main.mast` is reached by the active entry path
- the active bootstrap leaves a yielding or long-running GUI/story task alive
- the task is connected to the actual startup route, not merely present in a file

Static tests cannot fully prove live runtime behavior. Live Cosmos smoke remains required for mission-load acceptance items such as BOOT-001 and BOOT-012.

When live Cosmos crashes or goes ambiguous with empty `mast.runtime.log` / `mast.compile.log`, use a route-smoke breadcrumb trace before guessing at runtime fixes. Keep the evidence classes separate:

- last-success audit, such as `tests/live_smoke_last_bootstrap.txt`
- append-only crash breadcrumbs, such as `tests/live_startup_trace.txt`

Route-smoke breadcrumbs should bracket the real startup path and risky handoffs: `script.py` entry, sbs_utils import, client/start page setup, `story.mast` handoff, `scripts/main.mast` entry, state defaults, subsystem entry, and the exact API call suspected of crashing. If the trace does not update, the active startup path is earlier or different than assumed. If it stops at a marker, inspect the next line or API call first.

Quick tests may check that route-smoke markers exist and trace files are ignored, but they must not claim live success from marker strings alone.

---

# 9. Operator Test Expectation

When asking the human operator to run a test, app launch, live smoke, UI check, generated-artifact review, branch workflow check, documentation review, or negative-control test, include the expected observable result before asking for the test.

Do not only say "run this." Say what success, failure, and ambiguity look like.

Use this format when an operator action is requested:

```text
What changed:
- files changed
- intended behavior changed
- documentation-only/no-op if applicable

What to run or do:
- exact command, UI action, app launch, or manual check
- repo path and branch assumptions

Expected observation:
- terminal output, Git status shape, test count/pass pattern, log line, visible UI marker, created/updated file, or runtime/game behavior expected if it worked

Failure/ambiguous observation:
- error text, missing marker, wrong screen, unexpected branch, changed file that should not change, test failure, empty log, blank screen, or no-error/no-proof result

What remains unproven:
- static tests versus live runtime
- smoke marker versus full feature behavior
- manual check versus automated regression
- API/environment uncertainty

Next action by result:
- if expected result appears, do X
- if failure appears, capture Y and stop
- if ambiguous, run Z diagnostic
```

If asking for a manual or live test, always include:

```text
Expected observation:
Failure/ambiguous observation:
```

A clean terminal exit is not enough when the acceptance criterion depends on a visible UI marker, log line, runtime state, file output, or game behavior.

For negative-control tests, state explicitly when an expected failure means the negative control passed. Example: "The deliberate broken import should make quick tests fail; if quick tests fail for that import, the negative-control phase passed. Restore the file and rerun quick tests; the restored run should pass."
