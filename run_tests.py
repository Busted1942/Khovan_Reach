#!/usr/bin/env python3
"""Minimal Slice 00 repository checks for Khovan Reach."""

from __future__ import annotations

import re
import sys
from pathlib import Path


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
    "main.mast",
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


def print_group(label: str, items: list[str]) -> None:
    for item in items:
        print(f"{label}: {item}")


def run_quick() -> int:
    print("Khovan Reach Slice 00 quick checks")

    required_docs, source_failures = read_source_index()
    failures = []
    warnings = []

    failures.extend(source_failures)
    if required_docs:
        failures.extend(check_required_docs(required_docs))

    failures.extend(check_required_folders())
    failures.extend(check_old_mast_filenames())
    failures.extend(check_conflicting_doc_filenames(required_docs))
    warnings.extend(check_old_mast_archive_warning())

    if failures:
        print_group("FAIL", failures)
    else:
        print("PASS: required active docs, folders, active scripts, and doc names are clean")

    if warnings:
        print_group("WARN", warnings)

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
