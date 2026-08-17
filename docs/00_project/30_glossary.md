# KHOVAN REACH — GLOSSARY

Status: Canonical term list for this repo
Purpose: Define the engine, tooling, and process vocabulary this repo uses without explanation elsewhere. Added because the docs are dense with terms that carry precise meanings, several of which were learned by measurement and are easy to get subtly wrong.

Alphabetical. Terms are defined as this repo uses them, which is not always how the wider Artemis community uses them.

---

**ADD (Architectural Design Document)** — A prescriptive document that defines a direction and justifies it. Contrast with a findings-based analysis, which answers a question without necessarily recommending anything. Posture matters: see `AGENTS.md` section 2.

**band** — One of the four Science scan tabs on a contact: `scan`, `status`, `intel`, `bio`. The engine caches scan results **per band**. Re-reading a band already scanned returns the cached figures; scanning a band not yet used re-resolves them. Measured 2026-08-16; this is the basis of the Science coaching in Act I.

**blob** — The per-object key/value store, reached in code as `object.data_set` or via `get_data_set_value()` / `set_data_set_value()`. Keys are indexed by an integer or, for per-side scan text, by the side string. Holds both engine-owned values (`system_damage`, `shield_val`) and mission-owned ones.

**breadcrumb** — A trace line written by `script.write_khovan_startup_trace()` into `tests/live_startup_trace.txt`. Proves the marker was reached. Proves nothing about whether the surrounding feature works — see `AGENTS.md` section 5.

**crit / critical hit** — The stock manual-targeting mechanic that damages a named NPC subsystem. Writes `system_damage` as a geometric series, `max(cur,1) * 1.35`. **Bypasses shields entirely** — a critical lands with shields fully up. An earlier claim that shields must be down was disproven live and must not be reintroduced.

**DAMCON** — Damage control teams. Player-ship only. Several grid helpers that look like they target an NPC actually reach the player's ship; see *grid helpers*.

**evidence class** — The strength of support behind a claim: asserted, static, compile preflight, live observed, live measured. Never conflate them. The observed/measured split is the one that matters most and the one most often skipped. `AGENTS.md` section 5.

**GM** — Game Master. A console and a role. GM-only routes in this repo are gated behind `has_roles(COMMS_ORIGIN_ID, "gamemaster") and test_mode_enabled` so they can never reach a crew.

**grid / grid objects** — A hull's interior node map, from `data/grid_data.json`. Only 40 of 161 hulls have any `grid_objects`; no Kralien warship does. **Testing `hull in grid_data` proves nothing** — all 161 hulls have an entry and most are empty. Count the contents.

**grid helpers** — `grid_rebuild_grid_objects()`, `grid_damage_system()`, and relatives. Treat as **player-ship APIs**: `grid_apply_system_damage()` ends with `explode_player_ship()`, and a call aimed at an NPC was observed making the player's own DAMCON teams respond. Two GM buttons are deliberately left unwired for this reason.

**hullpoints** — A hull's durability from `data/shipData.yaml` (`kralien_cruiser` 2.0, `xim_light_cruiser` 3.0). Also the value the engine uses as `system_max_damage`, which makes it the denominator of the Science subsystem percentage.

**LegendaryMissions** — The Cosmos mission package that owns the console and player-spawn lifecycle. Khovan Reach binds state to the ship LegendaryMissions creates; it must never call `sim_create()`, `player_spawn(`, or `assign_client_to_ship` itself.

**lifeform** — A person as an object, so Dillon, Anderson, Hessler and Reyes can speak as themselves rather than as a station. See `scripts/lib/lifeform_helpers.mast`.

**MAST** — Multi-Agent Story Telling. The Python-like scripting language mission files are written in. Do not write it from memory; use `docs/04_implementation_setup/60_mast_api_cookbook.md`.

**preflight (MAST compile preflight)** — The middle evidence class. Compiles `story.mast` and its imports. Requires an installed `.sbslib` outside this repo, and **skips rather than fails** where Cosmos is not installed — so a PASS on a machine without the game is missing this class entirely. Read the warning line, not just the summary.

**run-ID guard** — A generation counter compared at the top of every delayed task, so a story jump or reset retires stale timers instead of letting them fire into a later act. Required by `AGENTS.md` section 4; the Act II pivot bumps every Act I counter.

**sbs** — The compiled engine module exposed to Python. Its surface is mirrored (not implemented) by `sbs_utils/mock/sbs.py`, a pybind-generated test double used only by sbs_utils' own tests. Useful as a catalogue of what the engine exposes; **not proof**, since a mock can drift from the real binding.

**sbs_utils** — The Python library between mission scripts and the engine. Ships with Cosmos. Owns `ScanPromise`, comms routing, procedural helpers. Note that some of its code is dead — `ScanPromise.start_scan` is a bare `return`.

**SHPSYS** — The subsystem index enum used as the second argument to `system_damage` / `system_max_damage` blob reads. `WEAPONS=0, ENGINES=1, SENSORS=2, SHIELDS=3`.

**slice** — A unit of scoped implementation work, defined by a packet in `docs/04_implementation_setup/` and closed by a verification record in `tests/`. Slices are the delivery rhythm of this project.

**spike** — A throwaway experiment run to answer one question, usually behind GM controls, deleted or documented as a dead end afterwards. Distinct from a slice: a spike ships no player-facing behavior.

**system_damage** — Engine blob key holding accumulated damage for one subsystem, indexed by `SHPSYS`. The engine **repairs it on its own tick** — values were observed decaying `1 → 0.95` and `1 → 0.99` unprompted, which confounds any polling design. Displayed percentage is `100 * (1 - system_damage / system_max_damage)`.

**verification record** — The per-slice `tests/SLICE*_VERIFICATION.md` file. Carries the exit criteria, the live-smoke log (append-only), and findings routed to the operator. It is the artifact that carries evidence from the build back to the design layer.
