# KHOVAN REACH — `scripts/lib/` EXTRACTION PLAN

Status: build-side architecture plan, NOT design authority
Purpose: define the shared-helper boundaries before Slices 09, 11, and 15 land, while the extraction is still cheap.

Pair with:
- `docs/04_implementation_setup/10_mast_file_lessons.md` section 3.4 — names the six modules this plans
- `docs/04_implementation_setup/70_agent_handoff_protocol.md` section 5.2 — the ~400-line extraction rule
- `AGENTS.md` sections 2 and 4 — work boundaries and the non-negotiable MAST patterns

---

# 1. Why now

`scripts/lib/` contains one file: `.gitkeep`.

Meanwhile the act files have grown past the threshold the handoff protocol sets:

| File | Lines | `shared` vars |
|---|---|---|
| `scripts/acts/act1_generator_tarsis_gate.mast` | 983 | 81 |
| `scripts/acts/act1_drone_contact_fire.mast` | 798 | 81 |
| `scripts/acts/act1_engineering_shakedown.mast` | 507 | 52 |

Section 5.2 says extract "when a slice would push a single `.mast` file past roughly 400 lines, or when two slices need the same cleanup/seeding/spawn logic." All three act files are past that, and the second condition is about to bite: Slices 09, 11, 12, and 15 each add a state tree comparable to Slice 04's.

Section 5.2 also says this is "cheapest to enforce before Slices 09 (DAMCON), 11 (pirates), and 15 (checkpoint/reload) land." That window is open now and closes when Slice 07 Phase B starts writing Act II runtime.

**The `shared` namespace is the real driver.** It is global across every MAST file, collisions fail silently, and the repo is at ~290 declarations. Every new act file that redefines its own spawn/cleanup state widens that surface. Extraction is as much a namespace decision as a file-size one.

---

# 2. The rule this plan follows

**Do not refactor proven code without a reason.** `AGENTS.md` section 2 is explicit that `act1_generator_tarsis_gate.mast` is accepted technical debt, not a defect — it carries the deepest live-smoke history in the repo, and a speculative refactor risks regressing the parts of the mission with the most evidence behind them.

So this plan is **additive, not a rewrite**:

- New shared logic goes into `scripts/lib/` from the start.
- Existing act files are left alone unless a slice packet independently requires a change inside them.
- Where an act file already contains logic a new slice needs, the logic is **copied into `lib/` and the act file left untouched**, with the duplication recorded here and retired only when that act file is being modified for another reason.

Duplication is the cheaper error. Regressing `act1_generator_tarsis_gate.mast` costs a crewed session; a duplicated cleanup routine costs a few lines.

---

# 3. Module boundaries

Six modules, from `10_mast_file_lessons.md` section 3.4. Each owns a *category of behaviour*, not a slice.

## 3.1 `scripts/lib/entity_cleanup_helpers.mast`

**ALREADY ASSIGNED — Slice 07B owns creating this file.** Correction, 2026-08-08:
rev 1.0 of this plan sequenced this module "before Slice 11." That was written
without checking `80_slice_packets_07_16.md`, where Slice 07B lists
`scripts/lib/entity_cleanup_helpers.mast (new - see 1.6)` in Files to modify and
task 2 as "Create `scripts/lib/entity_cleanup_helpers.mast` with a generic
'despawn object, drop navproxy, clear all three selections' routine." It arrives
four slices earlier than this plan said.

The packet also already states the ownership rule this document arrives at
independently in section 4: "it owns no state of its own."

**Owns:** deleting spawned objects and their navproxies, clearing selections, and
the destroy-source attribution guard.

**What this plan still contributes.** The Slice 07B interface covers despawn and
deselect. It does **not** mention the destroy-source attribution guard, and that
omission is the expensive one. Slice 06 confirmed live that `sbs.delete_object()`
fires the same `//damage/destroy` hook a genuine Weapons kill fires, that the hook
is **deferred/queued** relative to the calling handler, and that a premature flag
clear defeats the guard. That took four independent cleanup events and multiple
live passes to find and fix.

Slice 11 spawns two pirate vessels; Slice 12 destroys them and must distinguish a
genuine kill from cleanup to set `pirate_outcome` correctly. It will hit this
behaviour identically.

**Recommendation:** Slice 07B's packet should extend task 2 to include the
attribution guard, or Slice 12's packet should name it explicitly as a reuse
dependency. Otherwise the finding gets re-derived live. **Routed to the operator**
as a packet amendment — this document does not amend packets.

**Interface (proposed, extending the 07B definition):**
- cleanup routine taking an object id: delete navproxy, delete object, clear selections, set a cleanup-in-progress flag
- destroy-hook attribution helper distinguishing GM cleanup from a genuine kill
- existence check helper

**State it owns:** none. A generic `*_cleanup_in_progress` convention where consumers pass their own id.

## 3.2 `scripts/lib/drone_spawn_helpers.mast`

**Owns:** idempotent spawn with existence check, navproxy attachment, spawn-failure fallback flagging.

Despite the name, this is the general NPC-spawn helper — Drone 01/02, pirates, and any Act III contact. Rename to `npc_spawn_helpers.mast` if the operator prefers; the lessons doc name is preserved here for traceability.

**Interface:** spawn-at-offset-from-anchor, returning id and setting a `*_fallback_available` flag on failure per `AGENTS.md` section 4.

## 3.3 `scripts/lib/target_detection_helpers.mast`

**Owns:** range-band checks, stationary-hold observers, bounded polling with tick ceilings.

Slice 06's `khovan_drone_01_watch_stationary_hold` is the reference implementation and already carries the correct run-ID guard shape. Act III needs the same for cache approach, pirate range, and Halcyon station-keeping.

**Interface:** distance-between-ids, in-band check, and a bounded observer template. Every observer ships a fallback flag and a tick ceiling — cookbook 5.2.

## 3.4 `scripts/lib/resupply_helpers.mast`

**Owns:** ordnance and energy restoration, docking-state side effects.

Currently embedded in `act1_generator_tarsis_gate.mast`. **Do not extract now** — that file is the accepted-debt file. Create this module when Act III needs resupply (torpedo conversion, post-combat rearm) and copy rather than move.

## 3.5 `scripts/lib/act1_helpers.mast`

**Owns:** Act I-specific neutral state seeding.

Lowest priority. Its value was separating seed logic from the dev-jump harness, which `story_jump_presets.mast` already does. Create only if Act I work resumes.

## 3.6 `scripts/systems/checkpoint_system.mast`

**Owns:** checkpoint payload write/restore, and the irreversible-state exclusion list.

Note this lives in `systems/`, not `lib/` — it is cross-cutting runtime, not a helper library. It is the highest-risk module in the mission and the one section 5.2 specifically expects to reuse neutral helpers rather than duplicate story-jump seeding.

**Hard invariant, from `00_source_index.md` section 8:** reload must not undo committed consequences. DAMCON deaths, expended ordnance, and pirate outcomes survive restore. The module needs an explicit *exclusion list* of state that is never restored, and that list is design authority — it belongs in the Slice 15 packet, ratified, not invented in code.

---

# 4. Naming and namespace rules

Extraction only helps if it shrinks the global surface. Three rules:

1. **Helpers take parameters; they do not read caller state.** A helper that reads `drone_01_target_id` directly is not reusable. Pass the id.
2. **Helpers declare no `shared` state of their own** unless it is genuinely global (a registry, a counter). Every flag a helper sets is a flag the caller owns and passes.
3. **Prefix every new `shared` name by owner.** `drone_01_*`, `pirate_*`, `damcon_*`, `checkpoint_*`. The collision check in `run_tests.py` catches cross-file duplicates; prefixes prevent them being written.

Rule 2 is the one most likely to be broken under time pressure, and it is the one that matters — a helper with its own `shared` state is a singleton, so two pirates cannot use it at once.

---

# 5. Sequencing

Corrected 2026-08-08 against the actual packets.

| Order | Module | Trigger | Cost if skipped |
|---|---|---|---|
| 1 | `entity_cleanup_helpers` | **Slice 07B, already assigned** | re-deriving the deferred-destroy-hook finding live |
| 2 | `drone_spawn_helpers` | Slice 07B or 11, wherever the second spawner lands | duplicated spawn/fallback logic across act files |
| 3 | `target_detection_helpers` | before Slice 11 range work | duplicated observer/tick-ceiling logic |
| 4 | `checkpoint_system` | Slice 15 Phase A spike | highest — the no-fail premise depends on it |
| 5 | `resupply_helpers` | when Act III needs rearm | low; copy from Act I |
| 6 | `act1_helpers` | only if Act I work resumes | none currently |

Rev 1.0 proposed items 1-3 as a standalone slice-shaped unit before Slice 11.
That is retracted: item 1 is already inside Slice 07B, so carving it out now would
mean amending a written packet to create a dependency that does not need to exist.

The remaining sequencing advice still holds for items 2 and 3 — decide where they
live *before* the slice that needs them opens, rather than discovering the shared
need mid-slice. That is the Slice 06 failure pattern, where architecture and
features churned together across 83 commits.

---

# 6. Verification

Extraction is refactoring, so the bar is *no behaviour change*:

- `python run_tests.py quick` passes before and after, with the same check count or higher.
- The `shared` collision check must not gain entries.
- Because static tests cannot prove runtime equivalence, any extraction touching a live-proven path needs one live smoke confirming the extracted path still fires — evidence class per `AGENTS.md` section 5.
- `python tools/review_gate.py --base master` must stay clean; the spawn/cleanup check exists precisely to catch a helper that drops an existence check or cleanup routine.

---

# 7. Revision

Rev 1.1 (2026-08-08) — corrected against `80_slice_packets_07_16.md`.
`entity_cleanup_helpers.mast` is already a **Slice 07B** deliverable with a
defined interface and the same no-state-of-its-own rule this plan derived
independently — four slices earlier than rev 1.0 claimed. Section 3.1 and the
section 5 sequencing table are corrected, and rev 1.0's proposal to carve items
1-3 into a standalone pre-Slice-11 unit is retracted.

The plan's remaining contribution to that module is narrower but real: the 07B
interface covers despawn and deselect and does **not** mention the destroy-source
attribution guard, which Slice 06 paid several live passes to find. That gap is
routed to the operator as a packet amendment rather than fixed here.

Rev 1.0 (2026-08-08) — initial plan. Written while `scripts/lib/` was still empty and three act files sat at 507-983 lines.
