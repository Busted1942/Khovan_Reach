from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SECTIONS = {
    "AGENTS.md": [
        "Operator Test Expectation",
        "Expected observation:",
        "Failure/ambiguous observation:",
        "What remains unproven:",
        "Next action by result:",
    ],
    "docs/04_implementation_setup/30_implementation_project_start_prompt.md": [
        "Operator Test Expectation",
        "Manual or live tests must always include",
        "Negative-control expected observation",
    ],
    "docs/01_design/50_implementation_slice_plan.md": [
        "Expected observations:",
        "Failure/ambiguous observations:",
        "Operator test expectation discipline",
    ],
    "docs/01_design/40_admin_testing_plan.md": [
        "Operator test expectation evidence",
        "OTE-001",
        "OTE-009",
    ],
    "docs/05_governance/20_proview_v2_4_test_first_workflow_checkpoint_draft.md": [
        "7B.4A Operator Test Expectation",
        "Expected observation",
        "Failure/ambiguous observation",
        "No error + no marker/log/UI/file/runtime proof = ambiguous",
    ],
}


def test_operator_test_expectation_docs_present():
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
