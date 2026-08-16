#!/usr/bin/env python3
"""Read player-facing copy out of the runtime so tests stop duplicating it.

Why this exists
---------------
Copy assertions used to pin the exact string in two places: the `shared` MAST
declaration and a literal in a test. Every wording change then broke a pile of
tests that were not actually testing the wording - they were testing that a
variable existed, or that a label used it. On 2026-08-09 a single copy pass
required hand-patching roughly a dozen of them, in four rounds, and one of
those patches silently corrupted a test file's quoting.

The rule this module encodes: **a test should assert wiring and conventions,
never a duplicate of the prose.**

- Wiring: does the label exist, does it pass this variable, in this order.
- Convention: does the copy follow the house style (section 4.1 and 6.2 of the
  cookbook).
- Prose: nobody's test. Change it freely.

The one exception is deliberate historical pinning - `SLICE04_VERIFICATION.md`
quotes copy that was live during its smoke, and that log is append-only. Those
assertions stay literal and carry a comment saying so.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# `shared <name>_text = "<value>"` at column 0. Multi-line copy keeps a literal
# \n inside the quotes - see cookbook 4.1 for why it cannot live anywhere else.
SHARED_TEXT_RE = re.compile(r'^shared (\w+_text) = "([^"]*)"', re.MULTILINE)

# House style from cookbook 6.2: the body opens with who is being addressed.
ADDRESSEE_RE = re.compile(r"^Artemis - [A-Z][A-Za-z]*:")

# A body must not open by naming its own sender - comms_receive already renders
# a header, so "Tarsis Control: ..." inside the body prints the name twice.
SELF_NAMING_RE = re.compile(
    r"^(Tarsis|Kestrel|Commander Dillon|Dillon|Training|Drone|Artemis)\b[^:\n]*:(?! )"
    r"|^(Tarsis Control|Tarsis Station|Tarsis Docking Control|Kestrel Yard Control|Commander Dillon|Dillon|Training Control):"
)


def mast_files() -> list[Path]:
    return sorted((ROOT / "scripts").rglob("*.mast"))


def all_player_copy() -> dict[str, tuple[str, str]]:
    """Return {var_name: (repo_relative_file, value)} for every *_text shared."""
    found: dict[str, tuple[str, str]] = {}
    for path in mast_files():
        rel = path.relative_to(ROOT).as_posix()
        for match in SHARED_TEXT_RE.finditer(path.read_text(encoding="utf-8")):
            found[match.group(1)] = (rel, match.group(2))
    return found


def copy_value(name: str) -> str:
    """The live value of one copy variable.

    Use this instead of retyping the string. A test that reads the value and
    compares it to itself asserts nothing, so pair this with a convention check
    or a wiring assertion - never with an equality check against a literal.
    """
    found = all_player_copy()
    if name not in found:
        raise AssertionError(f"no shared copy variable named {name!r} in scripts/")
    return found[name][1]


def copy_lines(name: str) -> list[str]:
    """Copy split on its literal \\n, one entry per addressed recipient."""
    return copy_value(name).split("\\n")


def uses_copy(body: str, name: str) -> bool:
    """True if a label body passes this variable by name rather than inline text."""
    return re.search(rf"\b{re.escape(name)}\b", body) is not None


# ---------------------------------------------------------------------------
# Exemptions
# ---------------------------------------------------------------------------
# Each entry is a design decision, not a silenced failure. Keep the reason.

# Copy that is not a message from Khovan to the Artemis crew, so the
# "Artemis - <Station>:" addressee convention does not apply.
NOT_ADDRESSED_TO_CREW = {
    "drone_01_hail_response_text": "the drone replying to a hail; the drone is the speaker",
    "drone_01_known_scan_text": "Science scan readout, not a Comms message",
    "dillon_clip_1_stub_text": "opening briefing addressed to the whole crew at once",
    "scenario_control_panel_overview_text": "GM-facing panel text, never shown to players",
}

# Copy whose sender genuinely is an external station, where naming the station
# is the point rather than duplication. Empty today; kept so a future entry has
# to justify itself.
SENDER_NAME_ALLOWED: dict[str, str] = {}
