#!/usr/bin/env python3
"""Minimal quick checks for Khovan Reach implementation slices."""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
import importlib.util
from io import StringIO
from pathlib import Path


# Several active docs use non-ASCII characters (e.g. the arrow in "GM Comms ->
# Khovan Scenario Control -> ..."-style navigation notes). If a failure or
# warning message ever quotes doc text containing one, printing it on a
# default Windows console (cp1252) raises UnicodeEncodeError and crashes the
# whole run instead of reporting the failure. Force UTF-8 with a safe
# fallback so a reporting bug never masks a real check failure.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
SOURCE_INDEX = ROOT / "docs" / "00_project" / "00_source_index.md"

REQUIRED_FOLDERS = [
    "docs/00_project",
    "docs/01_design",
    "docs/02_content",
    "docs/03_game_resources/comms",
    "docs/04_implementation_setup",
    "docs/05_governance",
    "scripts/acts",
    "scripts/systems",
    "scripts/lib",
    "tests",
    "tools",
    "audio",
    "archive/old_build_reference",
    "archive/old_build_reference/old_mast",
    "docs_external",
    "reference_missions",
]

OLD_ROOT_MAST_FILENAMES = {
    "dev_jump.mast",
    "act_1_qualification.mast",
    "act_1_state_helpers.mast",
    "act_2_investigation.mast",
    "act_3_khovan_reach.mast",
    "damcon_timer.mast",
    "salvager_arrival.mast",
    "state_save.mast",
    "__init__.mast",
}

CONFLICT_WORDS = {
    "pass",
    "patch",
    "merged",
    "addendum",
    "handoff",
    "old",
    "copy",
    "final",
    "new",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_source_index() -> tuple[set[str], list[str]]:
    if not SOURCE_INDEX.is_file():
        return set(), [f"missing source index: {rel(SOURCE_INDEX)}"]

    text = SOURCE_INDEX.read_text(encoding="utf-8-sig")
    required_docs = {
        match.replace("\\", "/")
        for match in re.findall(r"`([^`]+)`", text)
        if match.replace("\\", "/").startswith("docs/")
    }

    if not required_docs:
        return set(), [f"no required docs found in source index: {rel(SOURCE_INDEX)}"]

    return required_docs, []


def check_required_docs(required_docs: set[str]) -> list[str]:
    missing = []
    for doc in sorted(required_docs):
        if not (ROOT / doc).is_file():
            missing.append(f"missing required active doc: {doc}")
    return missing


def check_required_folders() -> list[str]:
    missing = []
    for folder in REQUIRED_FOLDERS:
        if not (ROOT / folder).is_dir():
            missing.append(f"missing required folder: {folder}")
    return missing


def check_old_mast_filenames() -> list[str]:
    scripts_dir = ROOT / "scripts"
    if not scripts_dir.is_dir():
        return ["missing scripts folder: scripts"]

    failures = []
    for path in scripts_dir.rglob("*"):
        if path.is_file() and path.name in OLD_ROOT_MAST_FILENAMES:
            failures.append(f"old root MAST filename in active scripts: {rel(path)}")
    return failures


def check_no_live_mast_files_outside_runtime() -> list[str]:
    """Cosmos scans the whole mission directory, not just imported files.

    A live .mast file sitting under archive/, docs_external/, or
    reference_missions/ can be picked up by that scan even though nothing
    in the active runtime imports it, and can collide by filename with an
    active or future runtime file (e.g. main.mast, damcon_timer.mast).
    Reference material in these folders must use a defanged extension
    such as .mast.archive so Cosmos never parses it as live MAST.
    """
    scan_roots = ["archive", "docs_external", "reference_missions"]
    failures = []
    for folder in scan_roots:
        folder_path = ROOT / folder
        if not folder_path.is_dir():
            continue
        for path in folder_path.rglob("*.mast"):
            if path.is_file():
                failures.append(f"live .mast file outside runtime scope: {rel(path)}")
    return failures


def check_slice01_bootstrap_files() -> list[str]:
    required = [
        "description.txt",
        "script.py",
        "story.json",
        "story.mast",
        "scripts/main.mast",
        "scripts/systems/bootstrap_state.mast",
        "scripts/systems/playable_bootstrap.mast",
        "scripts/systems/audio_runtime.mast",
        "scripts/systems/debug_runtime.mast",
        "tests/test_bootstrap_static.py",
        "tests/SLICE01_VERIFICATION.md",
    ]
    return [
        f"missing Slice 01 bootstrap file: {path}"
        for path in required
        if not (ROOT / path).is_file()
    ]


def check_clone_contents_not_tracked() -> list[str]:
    if not (ROOT / ".git").exists():
        return []

    result = subprocess.run(
        [
            "git",
            "ls-files",
            "docs_external/_local_clones",
            "reference_missions/_local_clones",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return [f"git clone tracking check failed: {result.stderr.strip()}"]

    tracked = [line for line in result.stdout.splitlines() if line.strip()]
    return [f"external clone content is tracked: {line}" for line in tracked]


def run_static_unittests() -> tuple[list[str], int, list[str]]:
    test_files = [
        ROOT / "tests" / "test_bootstrap_static.py",
        ROOT / "tests" / "test_mast_compile_or_preflight.py",
        ROOT / "tests" / "test_scenario_control_panel_static.py",
        ROOT / "tests" / "test_story_jump_presets_static.py",
        ROOT / "tests" / "test_act1_generator_tarsis_static.py",
        ROOT / "tests" / "test_act1_engineering_shakedown_static.py",
        ROOT / "tests" / "test_act1_drone_contact_fire_static.py",
        ROOT / "tests" / "test_comms_proof_station_static.py",
    ]
    suite = unittest.TestSuite()
    for test_file in test_files:
        spec = importlib.util.spec_from_file_location(test_file.stem, test_file)
        if spec is None or spec.loader is None:
            return [f"could not load static test file: {rel(test_file)}"], 0, []

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))

    result = unittest.TextTestRunner(stream=StringIO(), verbosity=1).run(suite)
    failures = []
    for test_case, traceback_text in result.failures + result.errors:
        last_line = traceback_text.strip().splitlines()[-1]
        failures.append(f"{test_case.id()}: {last_line}")
    skips = [
        f"{test_case.id()}: skipped - {reason}"
        for test_case, reason in result.skipped
    ]
    return failures, result.testsRun, skips


def run_pytest_doc_checks() -> tuple[list[str], int]:
    if importlib.util.find_spec("pytest") is None:
        return [], 0

    test_paths = [
        ROOT / "tests" / "test_branch_lifecycle_docs.py",
        ROOT / "tests" / "test_operator_test_expectation_docs.py",
    ]
    missing = [f"missing pytest doc test: {rel(path)}" for path in test_paths if not path.is_file()]
    if missing:
        return missing, 0

    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_paths[0]), str(test_paths[1])],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        return [], 0

    output = result.stdout.strip() or result.stderr.strip()
    return [f"pytest doc checks failed: {output}"], 0


def conflict_tokens(path: Path) -> set[str]:
    return {
        token
        for token in re.split(r"[^a-z0-9]+", path.stem.lower())
        if token in CONFLICT_WORDS
    }


def check_conflicting_doc_filenames(required_docs: set[str]) -> list[str]:
    docs_dir = ROOT / "docs"
    if not docs_dir.is_dir():
        return ["missing docs folder: docs"]

    listed_docs = {doc.lower() for doc in required_docs}
    failures = []
    for path in docs_dir.rglob("*"):
        if not path.is_file():
            continue

        doc_rel = rel(path)
        if doc_rel.lower() in listed_docs:
            continue

        matches = conflict_tokens(path)
        if matches:
            words = ", ".join(sorted(matches))
            failures.append(f"conflicting active doc filename: {doc_rel} ({words})")

    return failures


def check_old_mast_archive_warning() -> list[str]:
    old_mast_dir = ROOT / "archive" / "old_build_reference" / "old_mast"
    if old_mast_dir.is_dir() and not any(old_mast_dir.iterdir()):
        return [f"old MAST archive is empty: {rel(old_mast_dir)}"]
    return []


def check_duplicate_shared_declarations() -> list[str]:
    """Check for shared variable declarations in multiple MAST files."""
    scripts_dir = ROOT / "scripts"
    if not scripts_dir.is_dir():
        return []

    shared_map = {}
    for path in scripts_dir.rglob("*.mast"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"^shared\s+(\w+)\s*=", text, re.MULTILINE):
            name = match.group(1)
            if name not in shared_map:
                shared_map[name] = []
            shared_map[name].append(rel(path))

    failures = []
    for name, files in sorted(shared_map.items()):
        if len(files) > 1:
            files_str = ", ".join(sorted(set(files)))
            failures.append(f"duplicate shared declaration: {name} in {files_str}")

    return failures


def extract_admin_test_ids(text: str) -> set[str]:
    """Collect every test ID the admin testing plan defines.

    Two forms appear in the plan and both are authoritative:

    1. Literal tokens, e.g. ``DAMCON-001 cascade trigger starts timer``.
    2. Range statements, e.g. ``JUMPTEST-001 through JUMPTEST-021 correspond
       to JUMP-001 through JUMP-021`` and ``D2-004 through D2-013 steps 1-10
       advance correctly``. These define every ID in the span, but only the
       two endpoints appear as literal tokens.

    Literal-only extraction silently drops the interior of a range. That is
    how JUMPTEST-002..020 and D2-005..012 went missing from the coverage
    matrix: both the plan side and the matrix side were scanned the same way,
    so the two agreed by shared blindness rather than by matching.

    Numbering gaps that are NOT spanned by a range statement (DAMCON 007-009,
    PIRATE 007-009, SAVE-009, etc.) are deliberate decade-grouping in the
    plan and must stay absent.
    """
    ids = set(re.findall(r"\b([A-Z]+\d*\-\d+)\b", text))
    for match in re.finditer(
        r"\b([A-Z]+\d*)\-(\d+)\s+through\s+\1\-(\d+)\b", text
    ):
        prefix = match.group(1)
        start_token, end_token = match.group(2), match.group(3)
        width = len(start_token)
        for number in range(int(start_token), int(end_token) + 1):
            ids.add(f"{prefix}-{number:0{width}d}")
    return ids


def check_test_coverage_matrix() -> list[str]:
    """Verify test coverage matrix exists and is consistent with admin testing plan."""
    matrix_file = ROOT / "tests" / "test_coverage_matrix.md"
    if not matrix_file.is_file():
        return ["missing test coverage matrix: tests/test_coverage_matrix.md"]

    admin_plan = ROOT / "docs" / "01_design" / "40_admin_testing_plan.md"
    if not admin_plan.is_file():
        return ["missing admin testing plan: docs/01_design/40_admin_testing_plan.md"]

    admin_text = admin_plan.read_text(encoding="utf-8")
    admin_ids = extract_admin_test_ids(admin_text)

    matrix_text = matrix_file.read_text(encoding="utf-8")
    matrix_ids = set(re.findall(r"^\|\s*([A-Z]+\d*\-\d+)\s*\|", matrix_text, re.MULTILINE))

    failures = []

    missing_in_matrix = admin_ids - matrix_ids
    if missing_in_matrix:
        for test_id in sorted(missing_in_matrix):
            failures.append(f"test ID in admin plan but not in coverage matrix: {test_id}")

    extra_in_matrix = matrix_ids - admin_ids
    if extra_in_matrix:
        for test_id in sorted(extra_in_matrix):
            failures.append(f"test ID in coverage matrix but not in admin plan: {test_id}")

    return failures


def print_group(label: str, items: list[str]) -> None:
    for item in items:
        print(f"{label}: {item}")


def run_quick() -> int:
    print("Khovan Reach quick checks")

    harness_checks_run = 0
    required_docs, source_failures = read_source_index()
    harness_checks_run += 1
    failures = []
    warnings = []

    failures.extend(source_failures)
    if required_docs:
        harness_checks_run += 1
        failures.extend(check_required_docs(required_docs))

    harness_checks_run += 1
    failures.extend(check_required_folders())
    harness_checks_run += 1
    failures.extend(check_old_mast_filenames())
    harness_checks_run += 1
    failures.extend(check_no_live_mast_files_outside_runtime())
    harness_checks_run += 1
    failures.extend(check_conflicting_doc_filenames(required_docs))
    harness_checks_run += 1
    failures.extend(check_slice01_bootstrap_files())
    harness_checks_run += 1
    failures.extend(check_clone_contents_not_tracked())
    static_failures, static_tests_run, static_warnings = run_static_unittests()
    failures.extend(static_failures)
    warnings.extend(static_warnings)
    harness_checks_run += 1

    pytest_failures, _ = run_pytest_doc_checks()
    failures.extend(pytest_failures)
    harness_checks_run += 1

    harness_checks_run += 1
    failures.extend(check_duplicate_shared_declarations())

    harness_checks_run += 1
    failures.extend(check_test_coverage_matrix())

    warnings.extend(check_old_mast_archive_warning())
    total_checks_run = harness_checks_run + static_tests_run

    if failures:
        print_group("FAIL", failures)
    else:
        print("PASS: source hygiene and Slice 01 bootstrap static checks are clean")

    if warnings:
        print_group("WARN", warnings)

    print(f"Ran {static_tests_run} Python tests")
    print(
        f"CHECKS: {total_checks_run} Khovan quick checks "
        f"({harness_checks_run} harness checks, {static_tests_run} Python tests)"
    )
    print(
        f"SUMMARY: {'FAIL' if failures else 'PASS'} "
        f"({len(failures)} failure(s), {len(warnings)} warning(s))"
    )
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if argv != ["quick"]:
        print("Usage: python run_tests.py quick")
        return 2

    return run_quick()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
