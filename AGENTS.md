# AGENTS.md — Khovan Reach Implementation Agent Rules

Status: repo-root implementation-agent control file
Purpose: Keep coding and documentation agents aligned with the active repo-consolidated source set, Git/GitHub discipline, test-first delivery, branch lifecycle safety, and operator-facing test expectations.

---

# 1. Source authority

Use `docs/00_project/00_source_index.md` as the source map.

Do not treat old Pass files, old MAST files, patch bundles, archived notes, reference missions, generated files, or local clones as current scenario authority unless explicitly promoted.

Do not create parallel active files with names like `final`, `new`, `copy`, `old`, `merged`, `v2`, or `patched`.

Edit stable canonical paths in place and rely on Git history for versioning.

---

# 2. Work boundaries

Implementation agents may change runtime code, tests, documentation, and tooling only within the requested task scope.

If implementation discovers an architecture issue, surface it as a finding, blocker, source-update proposal, or slice-plan change. Do not silently change scenario intent to fit implementation convenience.

Do not change scenario design, player-facing content, qualification criteria, DAMCON timing, Hessler behavior, pirate fiction, or debrief content unless the task explicitly targets those docs.

---

# 3. Git and GitHub discipline

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

Do not claim files were edited, tested, committed, pushed, merged, or live-smoked unless that action actually happened.

---

# 4. Branch Lifecycle and Return-to-Work Checks

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

Commit, stash, or intentionally discard local changes before switching. Do not carry unresolved docs/test/governance changes into runtime implementation work.

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

# 5. Runtime Load and GUI Lifecycle Testing

For Cosmos/MAST work, `python run_tests.py quick` must protect the active runtime load path, not just source hygiene.

Quick tests should fail when active runtime files reference:

- missing `.mast` files
- archived old-build files
- external reference clone paths
- forbidden old module names
- files outside the active mission load path

Git-ignored folders are not runtime-ignored. If external reference clones live under the active Cosmos mission root, active runtime files must not reference them.

When available, quick should also run the installed SBS Utils / MAST compile-preflight path. Treat this as a middle evidence class: stronger than text-only static checks because it compiles `story.mast` and imported active MAST files, but weaker than live Cosmos smoke because it does not prove runtime values, GUI/page lifecycle, player assignment, renderer behavior, or server/client playability.

When live Cosmos reports a missing load file, add a targeted regression check so the same class of failure is caught by `quick` before the next live run.

For SBS Utils / MAST bootstrap work, quick tests should also check the lifecycle contract where practical:

- root `story.mast` reaches the active Khovan entry path
- `scripts/main.mast` is reached by the active entry path
- the active bootstrap leaves a yielding or long-running GUI/story task alive
- the task is connected to the actual startup route, not merely present in a file

Static tests cannot fully prove live runtime behavior. Live Cosmos smoke remains required for mission-load acceptance items such as BOOT-001 and BOOT-012.

If live Cosmos fails after quick tests pass, treat the live failure as stronger evidence. Update the verification note, add a regression/static check where feasible, and do not claim the slice complete until the live failure is fixed or documented as a blocker.

When live Cosmos crashes or goes ambiguous with empty `mast.runtime.log` / `mast.compile.log`, use a route-smoke breadcrumb trace before guessing at runtime fixes. Keep the evidence classes separate:

- last-success audit, such as `tests/live_smoke_last_bootstrap.txt`
- append-only crash breadcrumbs, such as `tests/live_startup_trace.txt`

Route-smoke breadcrumbs should bracket the real startup path and risky handoffs: `script.py` entry, sbs_utils import, client/start page setup, `story.mast` handoff, `scripts/main.mast` entry, state defaults, subsystem entry, and the exact API call suspected of crashing. If the trace does not update, the active startup path is earlier or different than assumed. If it stops at a marker, inspect the next line or API call first.

Quick tests may check that route-smoke markers exist and trace files are ignored, but they must not claim live success from marker strings alone.

---

# 6. Operator Test Expectation

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
