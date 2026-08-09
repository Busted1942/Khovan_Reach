#!/usr/bin/env python3
"""Mechanized review gate for implementation-agent diffs.

`docs/04_implementation_setup/70_agent_handoff_protocol.md` section 5.4 lists
ten checks a planning/review agent must run before asking the operator for a
live Cosmos smoke. Seven of them are pure pattern/Git questions. Answering
those by reading a 450-line MAST diff by hand is slow, and it is exactly the
kind of reading where a missing `artemis_id == 0` guard slides past — the
reviewer is looking at what changed, not at what is absent.

This tool answers the mechanizable seven. It deliberately does NOT answer the
three that need judgment (packet-field coverage, gate/fallback pairing, and
`Do not implement` adherence); those are printed as a manual checklist so the
reviewer is reminded that a clean run is not a complete review.

Scoping rule — this is a REVIEW tool, not a repo linter
-------------------------------------------------------
Checks run against the diff, not the whole tree. `scripts/acts/` carries real
accepted technical debt that is live-proven (see `AGENTS.md` section 2 on
`act1_generator_tarsis_gate.mast`). A whole-repo linter would fail on that
debt from day one and be silenced within a week. Scoping to added lines means
the gate only ever polices new work.

Guard lookups still read the FULL current file: if an added line uses
`artemis_id`, the guard protecting it may be pre-existing and unchanged. The
question is whether the guard exists now, not whether it is new.

Usage
-----
    python tools/review_gate.py                 # diff vs master
    python tools/review_gate.py --base <ref>    # diff vs another ref
    python tools/review_gate.py --full          # scan whole changed files

Exit codes: 0 all mechanized checks pass, 1 at least one failed, 2 bad usage.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

# AGENTS.md section 2: design conflicts are surfaced as findings and routed to
# the operator, never resolved in place by an implementation agent.
PROTECTED_DOC_DIRS = ("docs/01_design/", "docs/02_content/")

# AGENTS.md section 1: no parallel active files.
FORBIDDEN_NAME_TOKENS = {
    "final",
    "new",
    "copy",
    "old",
    "merged",
    "v2",
    "patched",
}

# AGENTS.md section 2: LegendaryMissions owns the console and player-spawn
# lifecycle. Reintroducing any of these into the bootstrap path breaks it.
FORBIDDEN_BOOTSTRAP_APIS = (
    "artemis_ship_name",
    "sim_create(",
    "player_spawn(",
    "assign_client_to_ship",
)

# An operator ratification must be dated, so "ratified" cannot be asserted in
# the abstract. Matches e.g. "(operator-ratified 2026-08-08)".
RATIFIED_RE = re.compile(r"operator-ratified\s+\d{4}-\d{2}-\d{2}")

LABEL_RE = re.compile(r"^===\s*([A-Za-z_]\w*)\s*===")

# `to_object(` must not also match `to_object_list(`; the character after the
# name is `(` in one and `_` in the other, so this is safe as written.
TO_OBJECT_ASSIGN_RE = re.compile(r"(\w+)\s*=\s*to_object\(")
TO_OBJECT_CHAINED_RE = re.compile(r"to_object\([^()]*\)\s*\.")
TO_OBJECT_ANY_RE = re.compile(r"\bto_object\(")

# A risky artemis_id use is one that hands the id to an API. Comparisons and
# assignments are not risky and must not be flagged, or the check drowns in
# noise (act1_generator_tarsis_gate.mast alone has 33 mentions, 4 guards).
RISKY_ARTEMIS_RE = re.compile(
    r"to_object\(\s*artemis_id\s*\)|sbs\.\w+\([^)]*\bartemis_id\b"
)

TASK_SCHEDULE_RE = re.compile(r"task_schedule\(\s*(\w+)")

# Cookbook 5.2 bounded observer: a tick counter plus a ceiling that ends the
# loop. Both must be present - a counter with no ceiling is an unbounded loop,
# which is its own bug.
OBSERVER_TICKS_RE = re.compile(r"\w*_ticks\b")
OBSERVER_CEILING_RE = re.compile(r"\w*_ticks\s*>=")
JUMP_RE = re.compile(r"^\s*jump\s+(\w+)", re.MULTILINE)
NPC_SPAWN_RE = re.compile(r"\bnpc_spawn\(")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, result.stdout, result.stderr


def changed_files(base: str) -> tuple[list[str], list[str]]:
    """Return (changed paths, errors).

    Uses three-dot range so the comparison is against the merge base, not the
    tip of `base`. A reviewer on a branch that is simply behind `master`
    should not see unrelated files reported as their own changes.
    Uncommitted working-tree changes are included: an agent that edited but
    did not commit still changed the tree, and the gate must see it.
    """
    code, out, err = git("merge-base", base, "HEAD")
    if code != 0:
        return [], [f"cannot find merge base with '{base}': {err.strip()}"]
    merge_base = out.strip()

    paths: set[str] = set()
    for args in (
        ("diff", "--name-only", f"{merge_base}...HEAD"),
        ("diff", "--name-only", "HEAD"),
        ("ls-files", "--others", "--exclude-standard"),
    ):
        code, out, err = git(*args)
        if code != 0:
            return [], [f"git {' '.join(args)} failed: {err.strip()}"]
        paths.update(line.strip() for line in out.splitlines() if line.strip())

    return sorted(paths), []


def added_lines(base: str, path: str) -> set[int]:
    """Line numbers added/modified in `path`, in the CURRENT file's numbering.

    Parsed from unified-diff hunk headers so the result can be used to index
    into the working-tree file directly.
    """
    code, out, _ = git("merge-base", base, "HEAD")
    merge_base = out.strip() if code == 0 else base

    lines: set[int] = set()
    for diff_args in (
        ("diff", "-U0", f"{merge_base}...HEAD", "--", path),
        ("diff", "-U0", "HEAD", "--", path),
    ):
        code, out, _ = git(*diff_args)
        if code != 0:
            continue
        current = 0
        for line in out.splitlines():
            hunk = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if hunk:
                current = int(hunk.group(1))
                continue
            if line.startswith("+") and not line.startswith("+++"):
                lines.add(current)
                current += 1
    return lines


def label_blocks(text: str) -> list[tuple[str, int, int]]:
    """Return (label name, first line, last line) 1-indexed and inclusive."""
    lines = text.splitlines()
    starts: list[tuple[str, int]] = []
    for index, line in enumerate(lines, start=1):
        match = LABEL_RE.match(line)
        if match:
            starts.append((match.group(1), index))

    blocks = []
    for position, (name, start) in enumerate(starts):
        end = starts[position + 1][1] - 1 if position + 1 < len(starts) else len(lines)
        blocks.append((name, start, end))
    return blocks


def block_for_line(blocks: list[tuple[str, int, int]], line_no: int) -> tuple[str, int, int] | None:
    for block in blocks:
        if block[1] <= line_no <= block[2]:
            return block
    return None


def mast_files(paths: list[str]) -> list[str]:
    return [
        path
        for path in paths
        if path.endswith(".mast") and (ROOT / path).is_file()
    ]


def scope_lines(path: str, base: str, full: bool) -> set[int]:
    text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
    if full:
        return set(range(1, len(text.splitlines()) + 1))
    return added_lines(base, path)


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------


def check_protected_docs(paths: list[str]) -> tuple[list[str], list[str]]:
    """AGENTS.md section 2: design/content docs are not edited during implementation.

    Returns (failures, notes). An edit carrying a dated operator-ratification
    note in the document itself is reported as a note rather than a failure.

    Without that escape hatch, a ratified edit fails this check forever, and a
    check that fails forever on an accepted condition is one reviewers learn to
    skip -- which costs more than the rule protects. The marker is a visible,
    greppable claim inside mission canon that a human can audit, and AGENTS.md
    section 5 already forbids recording an action that did not happen.
    """
    failures: list[str] = []
    notes: list[str] = []
    for path in paths:
        if not path.replace("\\", "/").startswith(PROTECTED_DOC_DIRS):
            continue
        full = ROOT / path
        text = full.read_text(encoding="utf-8", errors="replace") if full.is_file() else ""
        if RATIFIED_RE.search(text):
            notes.append(f"design/content doc modified but operator-ratified in-document: {path}")
        else:
            failures.append(
                f"design/content doc modified (AGENTS.md section 2 - route as a finding instead): {path}"
            )
    return failures, notes


def check_forbidden_filenames(paths: list[str]) -> list[str]:
    failures = []
    for path in paths:
        stem = Path(path).stem.lower()
        tokens = {token for token in re.split(r"[^a-z0-9]+", stem) if token}
        hits = tokens & FORBIDDEN_NAME_TOKENS
        if hits:
            words = ", ".join(sorted(hits))
            failures.append(f"parallel-file name token in changed path: {path} ({words})")
    return failures


def analyze_bootstrap_apis(path: str, text: str, scope: set[int]) -> list[str]:
    lines = text.splitlines()
    failures = []
    for line_no in sorted(scope):
        if line_no > len(lines):
            continue
        line = lines[line_no - 1]
        for api in FORBIDDEN_BOOTSTRAP_APIS:
            if api in line:
                failures.append(
                    f"forbidden bootstrap API reintroduced: {path}:{line_no} ({api})"
                )
    return failures


def analyze_to_object(path: str, text: str, scope: set[int]) -> list[str]:
    """AGENTS.md section 4: none-check every to_object().

    Two shapes are wrong. A chained call (`to_object(x).method()`) can never be
    checked and is always a violation. An assignment is a violation only if no
    `is None` / `is not None` test on that name follows within a few lines.
    """
    lines = text.splitlines()
    failures = []
    for line_no in sorted(scope):
        if line_no > len(lines):
            continue
        line = lines[line_no - 1]
        if not TO_OBJECT_ANY_RE.search(line):
            continue

        if TO_OBJECT_CHAINED_RE.search(line):
            failures.append(
                f"unchecked to_object() with chained call: {path}:{line_no} "
                f"-> {line.strip()}"
            )
            continue

        assign = TO_OBJECT_ASSIGN_RE.search(line)
        if not assign:
            continue

        name = assign.group(1)
        window = lines[line_no : min(line_no + 5, len(lines))]
        guard = re.compile(rf"\b{re.escape(name)}\s+is\s+(not\s+)?None\b")
        if not any(guard.search(candidate) for candidate in window):
            failures.append(
                f"to_object() result not None-checked within 5 lines: "
                f"{path}:{line_no} ({name})"
            )
    return failures


def analyze_artemis_guards(path: str, text: str, scope: set[int]) -> list[str]:
    """AGENTS.md section 4: guard `if artemis_id == 0` before any ship API call.

    Scoped to the label block containing the risky line, because that is the
    unit MAST actually executes. A guard anywhere earlier in the same block
    protects the call; a guard in a different label does not.
    """
    lines = text.splitlines()
    blocks = label_blocks(text)
    failures = []
    reported: set[str] = set()

    for line_no in sorted(scope):
        if line_no > len(lines):
            continue
        if not RISKY_ARTEMIS_RE.search(lines[line_no - 1]):
            continue

        block = block_for_line(blocks, line_no)
        if block is None:
            body = text
            label = "<file scope>"
        else:
            label, start, end = block
            body = "\n".join(lines[start - 1 : end])

        if label in reported:
            continue
        if not re.search(r"artemis_id\s*==\s*0", body):
            reported.add(label)
            failures.append(
                f"ship API call on artemis_id without `artemis_id == 0` guard "
                f"in label: {path}:{line_no} (label {label})"
            )
    return failures


def check_forbidden_bootstrap_apis(paths: list[str], base: str, full: bool) -> list[str]:
    failures = []
    for path in mast_files(paths):
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        failures.extend(analyze_bootstrap_apis(path, text, scope_lines(path, base, full)))
    return failures


def check_to_object_none_checks(paths: list[str], base: str, full: bool) -> list[str]:
    failures = []
    for path in mast_files(paths):
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        failures.extend(analyze_to_object(path, text, scope_lines(path, base, full)))
    return failures


def check_artemis_id_guards(paths: list[str], base: str, full: bool) -> list[str]:
    failures = []
    for path in mast_files(paths):
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        failures.extend(analyze_artemis_guards(path, text, scope_lines(path, base, full)))
    return failures


def build_label_index() -> dict[str, str]:
    """Map every label name in the repo to its body.

    Built repo-wide, not diff-scoped: a `task_schedule` in a changed file can
    target a label defined in an unchanged file.
    """
    index: dict[str, str] = {}
    scripts = ROOT / "scripts"
    if not scripts.is_dir():
        return index
    for path in scripts.rglob("*.mast"):
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        for name, start, end in label_blocks(text):
            index[name] = "\n".join(lines[start - 1 : end])
    return index


def rechecks_after_delay(body: str) -> bool:
    """True if the label re-tests state AFTER its last yield.

    The hazard a run-ID prevents is acting on stale intent once execution
    resumes. A label that re-reads the state it is about to act on, after the
    delay, has already closed that hole - see
    khovan_engineering_watch_damcon_rest_cycle, which guards on
    damcon_rest_cycle_confirmed both before and after its delay.

    Deliberately narrow: the re-check must come after the final delay_sim.
    Guards that only run before the yield prove nothing, which is exactly the
    bug found in khovan_drone_01_reset.
    """
    marker = "delay_sim"
    if marker not in body:
        return False
    tail = body[body.rfind(marker) :]
    return re.search(r"^\s*if\s+.+:", tail, re.MULTILINE) is not None


def is_bounded_observer(body: str, index: dict[str, str], depth: int = 0) -> bool:
    """True if this label is (or hands off to) a cookbook 5.2 bounded observer.

    5.2 splits across two labels: an entry label that seeds state, delays, and
    jumps; and a tick label that carries the counter and the ceiling. The
    scheduled target is the entry label, so checking only its own body misses
    the ceiling and produces a false positive. Follow `jump` one hop.
    """
    if OBSERVER_TICKS_RE.search(body) and OBSERVER_CEILING_RE.search(body):
        return True
    if depth >= 2:
        return False
    for target in JUMP_RE.findall(body):
        nxt = index.get(target)
        if nxt is not None and is_bounded_observer(nxt, index, depth + 1):
            return True
    return False


def analyze_run_id(
    path: str, text: str, scope: set[int], index: dict[str, str]
) -> list[str]:
    """AGENTS.md section 4: every delayed task carries a run-ID guard.

    A `task_schedule` target only needs the guard when it actually yields —
    an immediately-completing label cannot be invalidated by a story jump.
    `delay_sim` in the target body is the discriminator. Cookbook section 5.1
    documents the shape: `default x_run_id = ...` plus an `!=` bail-out.

    Incrementing a run id is not the same as checking one. A label that bumps
    the counter and then yields is still unguarded on resume.
    """
    lines = text.splitlines()
    failures = []
    reported: set[str] = set()

    for line_no in sorted(scope):
        if line_no > len(lines):
            continue
        match = TASK_SCHEDULE_RE.search(lines[line_no - 1])
        if not match:
            continue

        target = match.group(1)
        body = index.get(target)
        if body is None or "delay_sim" not in body:
            continue
        if target in reported:
            continue
        # Cookbook 5.2 bounded polling observers are the other proven shape for
        # delayed work and legitimately carry no run-ID. They invalidate on
        # shared state instead - an opening `if <state>: ->END` that a story
        # jump resets - and bound themselves with a tick ceiling. Requiring a
        # run-ID here flagged act1_engineering_shakedown.mast's three live
        # observers, which is exactly the false-positive class that trains
        # reviewers to ignore a gate.
        if is_bounded_observer(body, index) or rechecks_after_delay(body):
            continue
        if re.search(r"run_id\s*!=", body) is None:
            reported.add(target)
            failures.append(
                f"delayed task scheduled without run-ID guard: {path}:{line_no} "
                f"-> label {target} (cookbook section 5.1)"
            )
    return failures


def analyze_spawn(path: str, text: str, scope: set[int]) -> list[str]:
    """AGENTS.md section 4: every spawn has an existence check and a cleanup routine.

    File-scoped rather than label-scoped: cleanup legitimately lives in a
    different label from the spawn, so requiring both in one block would be
    wrong. Requiring both somewhere in the owning file matches how
    `act1_drone_contact_fire.mast` is actually written.
    """
    lines = text.splitlines()
    touches_spawn = any(
        NPC_SPAWN_RE.search(lines[line_no - 1])
        for line_no in scope
        if line_no <= len(lines)
    )
    if not touches_spawn:
        return []

    failures = []
    if not re.search(r"_id\s*==\s*0", text):
        failures.append(
            f"npc_spawn() without a spawned-id existence check in file: {path} "
            f"(cookbook section 8.1)"
        )
    if "delete_object" not in text:
        failures.append(
            f"npc_spawn() without a cleanup routine in file: {path} "
            f"(cookbook section 8.5)"
        )
    return failures


def check_run_id_guards(paths: list[str], base: str, full: bool) -> list[str]:
    index = build_label_index()
    failures = []
    for path in mast_files(paths):
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        failures.extend(analyze_run_id(path, text, scope_lines(path, base, full), index))
    return failures


def check_spawn_existence_and_cleanup(paths: list[str], base: str, full: bool) -> list[str]:
    failures = []
    for path in mast_files(paths):
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        failures.extend(analyze_spawn(path, text, scope_lines(path, base, full)))
    return failures


def check_git_diff_whitespace() -> list[str]:
    code, out, err = git("diff", "--check")
    if code == 0:
        return []
    detail = out.strip() or err.strip()
    return [f"git diff --check reported whitespace errors:\n{detail}"]


def check_quick_tests() -> list[str]:
    result = subprocess.run(
        [sys.executable, "run_tests.py", "quick"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    failures = []
    if result.returncode != 0:
        tail = "\n".join(output.strip().splitlines()[-15:])
        failures.append(f"run_tests.py quick FAILED:\n{tail}")

    # A skipped compile preflight is an evidence-class gap, not a pass.
    # run_tests.py prints this on its own line for exactly this reason.
    if "EVIDENCE GAP" in output:
        failures.append(
            "run_tests.py quick passed WITHOUT the MAST compile preflight "
            "(sbs_utils not found on this machine). Do not claim "
            "compile-preflight coverage - see AGENTS.md section 5."
        )
    return failures


MANUAL_CHECKS = [
    "Every packet field was addressed, or the gap is stated",
    "Every automatic gate ships with a Comms/GM fallback and a *_fallback_available flag",
    "Nothing in the packet's `Do not implement` list was implemented",
    "New MAST patterns cite a cookbook section + evidence tag, or raise a section 12 uncertainty block",
    "Verification record `Status` and `Acceptance Not Covered` set by the REVIEWER, not the implementation agent",
]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Mechanized half of the section 5.4 review gate."
    )
    parser.add_argument("--base", default="master", help="base ref to diff against")
    parser.add_argument(
        "--full",
        action="store_true",
        help="scan whole changed files instead of only added lines",
    )
    args = parser.parse_args(argv)

    print("Khovan Reach review gate")
    print(f"base: {args.base}   scope: {'whole changed files' if args.full else 'added lines'}")

    paths, errors = changed_files(args.base)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    if not paths:
        print("No changed files against base. Nothing to review.")
        return 0

    print(f"changed files: {len(paths)}")

    failures: list[str] = []
    notes: list[str] = []
    checks_run = 0

    doc_failures, doc_notes = check_protected_docs(paths)
    notes.extend(doc_notes)

    for label, result in (
        ("protected docs", doc_failures),
        ("parallel filenames", check_forbidden_filenames(paths)),
        ("bootstrap APIs", check_forbidden_bootstrap_apis(paths, args.base, args.full)),
        ("to_object none-check", check_to_object_none_checks(paths, args.base, args.full)),
        ("artemis_id guard", check_artemis_id_guards(paths, args.base, args.full)),
        ("run-ID guard", check_run_id_guards(paths, args.base, args.full)),
        ("spawn/cleanup", check_spawn_existence_and_cleanup(paths, args.base, args.full)),
        ("whitespace", check_git_diff_whitespace()),
        ("quick tests", check_quick_tests()),
    ):
        checks_run += 1
        if result:
            failures.extend(result)
        else:
            print(f"  ok: {label}")

    print()
    for note in notes:
        print(f"NOTE: {note}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
    print(
        f"MECHANIZED: {'FAIL' if failures else 'PASS'} "
        f"({len(failures)} failure(s), {checks_run} checks)"
    )

    print()
    print("STILL REQUIRES HUMAN/REVIEWER JUDGMENT - a clean run above is not a complete review:")
    for item in MANUAL_CHECKS:
        print(f"  [ ] {item}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
