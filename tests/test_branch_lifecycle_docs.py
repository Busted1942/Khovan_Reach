from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SECTIONS = {
    "AGENTS.md": [
        "Branch Lifecycle and Return-to-Work Checks",
        "Runtime Load and GUI Lifecycle Testing",
        "Starting branch:",
        "Next safe branch/action:",
    ],
    "docs/00_project/20_build_start_checklist.md": [
        "Branch Lifecycle and Return-to-Work Checks",
        "Branch opening check",
        "Merge-back check",
        "Return-to-work check",
    ],
    "docs/04_implementation_setup/30_implementation_project_start_prompt.md": [
        "Branch lifecycle gate",
        "runtime/live-smoke allowed from this branch",
        "Completion report",
    ],
    "docs/01_design/50_implementation_slice_plan.md": [
        "Branch lifecycle discipline",
        "Branch type:",
        "Expected return branch:",
        "Runtime/live-smoke allowed from this branch:",
    ],
}


def test_branch_lifecycle_docs_present():
    missing = []
    for rel, phrases in REQUIRED_SECTIONS.items():
        path = ROOT / rel
        if not path.exists():
            missing.append(f"missing file: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for phrase in phrases:
            if phrase not in text:
                missing.append(f"{rel} missing phrase: {phrase}")
    assert not missing, "\n".join(missing)
