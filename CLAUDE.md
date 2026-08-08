# CLAUDE.md — Khovan Reach

Cosmos / Artemis SBS training mission built in MAST + sbs_utils.

**`AGENTS.md` in this directory is the governing control file.** Read it before any artifact-changing work. This file adds the build-side context it does not cover, and is kept short on purpose.

---

## Read order

1. `AGENTS.md` — branch lifecycle, source authority, evidence rules, operator test expectations. Governing.
2. `docs/00_project/00_source_index.md` — which files are canonical. Nothing outside this map is authority.
3. `docs/04_implementation_setup/70_agent_handoff_protocol.md` — the slice-packet-in / verification-record-out contract.
4. `docs/04_implementation_setup/60_mast_api_cookbook.md` — **proven MAST syntax. Read before writing any `.mast`.**
5. The specific design sections named in the current slice packet. Sections, not whole files.

---

## Commands

Quick checks — source hygiene, static tests, and MAST compile preflight:

```bash
python run_tests.py quick
```

`quick` is the only supported invocation. There is no full/slow mode.

---

## Repo shape

```text
story.json / script.py / story.mast   mission package entry (root, required by Cosmos)
scripts/main.mast                     imports every active runtime file
scripts/systems/                      cross-cutting: bootstrap, objective panel, GM control panel, jumps
scripts/acts/                         act/scene gameplay gates
scripts/lib/                          shared helpers (currently empty)
tests/                                static tests + per-slice verification records
docs/01_design/                       scenario canon - DO NOT EDIT during implementation
docs/04_implementation_setup/         handoff, API, and findings docs
archive/, docs_external/, reference_missions/   reference only, never runtime-referenced
```

Load chain: `story.json → script.py → story.mast → LegendaryMissions.server_console → scripts/main.mast @map/khovan_reach`.

---

## Writing MAST here

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

## Evidence classes

Never conflate these. This is the rule most often broken here.

| Class | Proves | Does not prove |
|---|---|---|
| Static tests | file/text structure | anything at runtime |
| MAST compile preflight | `story.mast` + imports compile | runtime values, GUI lifecycle, playability |
| Live Cosmos smoke | actual behavior | — |

A breadcrumb marker in `tests/live_startup_trace.txt` proves the marker was reached, not that the feature works. If live contradicts static, **live wins** — update the record, add a regression check, do not claim completion.

Report honestly: never claim files were edited, tested, committed, pushed, merged, or live-smoked unless it actually happened.

---

## Do not

- Edit `docs/01_design/` or `docs/02_content/` during implementation work. Design conflicts are surfaced as findings and routed to the operator, never resolved in place.
- Create parallel files named `final`, `new`, `copy`, `old`, `merged`, `v2`, or `patched`. Edit the canonical path; Git carries the history.
- Reference `archive/`, `docs_external/_local_clones/`, `reference_missions/_local_clones/`, or `old_mast` from any runtime file. Git-ignored is not runtime-ignored — Cosmos scans this directory.
- Reintroduce `artemis_ship_name`, `sim_create()`, `player_spawn(`, or `assign_client_to_ship` into the bootstrap path. LegendaryMissions owns the console and player-spawn lifecycle; Khovan only binds state to the ship it creates.
- Carry docs/governance changes into a runtime implementation branch, or start docs work from a branch with uncommitted runtime changes.
- Ask the operator to "just run this." Every operator request needs `Expected observation:` and `Failure/ambiguous observation:` — see `AGENTS.md` section 6.
