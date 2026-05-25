# Slice 01 Verification

Status: verification record template / Slice 01 evidence log
Purpose: Separate static quick checks, runtime load-path checks, live Cosmos smoke, unresolved blockers, and completion status.

---

# Evidence classes

- Static quick checks: source hygiene, expected files, forbidden references, parser/schema checks where available.
- Runtime load-path checks: active startup/import/include path points only to allowed existing files.
- Live Cosmos smoke: actual Cosmos/MAST mission load and Scene 1 behavior.
- Blocker checkpoint: documented failure that is intentionally preserved for investigation, not claimed complete.

# do not claim live cosmos success unless cosmos was actually run and passed.

## live cosmos smoke evidence and runtime blockers

quick tests are necessary but not sufficient.
Slice 01 static checks are necessary but not sufficient.

`python run_tests.py quick` currently covers source hygiene, package/static checks, and selected runtime-load-path checks. It does not by itself prove that Cosmos can load the mission, that SBS Utils GUI tasks remain alive, or that Scene 1 proceeds without manual recovery.

Live Cosmos smoke remains required for:

- BOOT-001 mission package loads
- BOOT-010 GM debug/admin overlay visible to GM, if implemented in this slice
- BOOT-011 player-facing debug controls hidden, if implemented in this slice
- BOOT-012 first scene proceeds without manual admin action

The live-smoke marker file is `tests/live_smoke_last_bootstrap.txt`.

### Live failure: missing old MAST dependency

Observed error:

```text
Cannot load file:
C:\Users\buste\OneDrive\Desktop\Cosmos\data\missions\khovan_reach\salvager_arrival.mast
```

Classification:

- runtime load-path failure
- old implementation module leaked into active bootstrap path
- not a design change

Resolution requirement:

- active Slice 01 bootstrap must not load old Act II/III or pirate/salvager modules
- active runtime files must not reference `salvager_arrival.mast`
- quick tests must include a regression check for forbidden old module references and missing `.mast` dependencies

### Live failure: SBS Utils GUI task lifecycle

Observed error:

```text
SBS_Utils runtime error
SBS Utils hook level runtime error
EDGE CASE. Did you set END or Yield the last GUI Task?
maststorypage.py line 591 in present
```

Classification:

- runtime GUI/story task lifecycle failure
- mission reaches SBS Utils but the active GUI/story task appears to end without a valid yield/long-running task
- not a Khovan scenario design change

Resolution requirement:

- identify the actual active entry chain from `story.json` / `script.py` / `story.mast` to `scripts/main.mast`
- ensure the active bootstrap reaches a reference-backed yielding or long-running GUI/story task
- quick tests should verify the task is connected to the active entry route where practical
- live Cosmos smoke must confirm the error is gone

### Evidence rule

Do not mark Slice 01 complete until:

- `python run_tests.py quick` passes
- active runtime load-path checks pass
- live Cosmos mission load reaches Scene 1 without manual recovery, or
- an exact blocker is documented with next action and the commit is explicitly marked as a blocker/investigation checkpoint

## Operator-facing live-smoke expectation

When asking the operator to run Slice 01 live smoke, include:

```text
What changed:
What to run or do:
Expected observation:
Failure/ambiguous observation:
What remains unproven:
Next action by result:
```

Expected live-smoke observation should include a Khovan-specific visible or logged marker, for example:

```text
Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized.
mission_phase=act_1
current_scene=1
```

Failure or ambiguous observations include:

```text
blank screen with no marker
empty mast.runtime.log or mast.compile.log when a marker was expected
default server screen appears but no Khovan marker appears
no error but no proof the Khovan startup route ran
```

If the check is a negative control, state which failure is expected and when that expected failure means the control passed.

