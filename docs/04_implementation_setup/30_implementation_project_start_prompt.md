# KHOVAN REACH — IMPLEMENTATION PROJECT START PROMPT

Version: 1.2 branch-lifecycle + operator-test-expectation update
Status: Implementation-project startup prompt
Purpose: Start or resume coding work from the active repo-consolidated source set without source drift, branch drift, false completion claims, or ambiguous operator test handoffs.

---

# 1. Role

You are implementing Khovan Reach in the Cosmos/MAST implementation repo.

Do not redesign the scenario. Do not treat old Pass files, old MAST files, patch bundles, archived notes, or reference missions as current scenario authority.

Use the active repo docs as the source of truth.

---

# 2. Active source authority

Start by identifying the active sources for the task:

- `docs/00_project/00_source_index.md`
- `docs/00_project/10_repo_structure.md`
- `docs/00_project/20_build_start_checklist.md`
- `docs/01_design/00_scenario_play_guide.md`
- `docs/01_design/10_mast_requirements.md`
- `docs/01_design/40_admin_testing_plan.md`
- `docs/01_design/50_implementation_slice_plan.md`
- relevant `docs/02_content/*` files
- relevant `docs/04_implementation_setup/*` files
- `AGENTS.md` for implementation-agent workflow rules

If sources conflict, stop and report the conflict before implementing.

---

# 3. Branch lifecycle gate

Before running implementation prompts, live-smoke prompts, or Cosmos tests, perform the branch lifecycle check.

Opening check:

```text
git status --short --branch
git log --oneline -5
```

Identify:

```text
current branch:
branch type: implementation | docs/governance | architecture feedback | spike/experiment | emergency fix
task purpose:
expected return branch:
runtime/live-smoke allowed from this branch:
```

Runtime implementation and live-smoke prompts should run from the active implementation branch, not from temporary docs/governance or architecture-feedback branches.

If on a docs-only, governance, or architecture-feedback branch, stop and switch back before runtime testing unless the user explicitly approves that branch for runtime work.

---

# 4. Branch transition and return-to-work routine

Before switching branches:

```text
python run_tests.py quick
git status --short --branch
git diff --stat
```

If `python run_tests.py quick` is unavailable, document that directly.

Before switching branches, commit, stash, or intentionally discard local changes after review. Do not leave unresolved docs/test/governance changes mixed with runtime implementation work.

After completing a docs/governance or architecture-feedback branch:

1. close the temporary branch intentionally
2. merge it into the active implementation branch
3. rerun `python run_tests.py quick` if available
4. confirm `git status --short --branch`
5. only then resume runtime implementation work

---

# 5. Test-first slice discipline

Before implementation, define:

```text
slice/task goal:
source docs:
files expected to change:
acceptance criteria:
existing tests to preserve:
new checks to add:
what each check proves:
what each check does not prove:
live Cosmos smoke required:
stop condition:
```

Do not claim live runtime success from static tests.

If live Cosmos fails after quick tests pass, treat the live failure as stronger evidence. Add a regression/static check where feasible or document why not.

---

# 6. Operator Test Expectation

Before asking the human operator to run a command, manual check, live smoke, UI/runtime check, generated-artifact review, branch workflow check, documentation review, or negative-control test, provide the expected observation.

Required blocks for operator action requests:

```text
What changed:
What to run or do:
Expected observation:
Failure/ambiguous observation:
What remains unproven:
Next action by result:
```

Manual or live tests must always include:

```text
Expected observation:
Failure/ambiguous observation:
```

Do not treat "no error" as proof when the acceptance criterion requires a visible marker, UI state, log line, file output, runtime variable, or game behavior. If the expected marker is absent, classify the result as failure or ambiguous and give the next diagnostic step.

For negative-control tests, state clearly when the expected failure means the negative control passed.

Examples:

```text
Quick tests expected observation:
- python run_tests.py quick exits 0
- summary says PASS or equivalent
- prior test count does not unexpectedly drop
- no external clone contents appear as tracked files

Live game smoke expected observation:
- no SBS Utils error
- visible marker or log marker appears: Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
- mission_phase=act_1
- current_scene=1

Negative-control expected observation:
- deliberate broken import causes quick tests to fail
- restoring the file makes quick tests pass again
- if the broken import is caught, the negative-control phase passed
```

---

# 7. Completion report

Every implementation or branch lifecycle operation must report:

```text
Starting branch:
Ending branch:
Branch type:
Commits created:
Merge performed: yes/no
Tests run:
Files changed:
Remaining uncommitted changes:
Live Cosmos smoke run: yes/no
Next safe branch/action:
```

Do not claim a file was edited, tested, committed, pushed, merged, or live-smoked unless that action actually occurred.
