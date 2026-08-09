# KHOVAN REACH — ACTS II/III AUTOMATION GATE MAP (PROPOSAL)

Status: build-side proposal, NOT design authority
Purpose: give Slices 07-16 the gate/fallback policy that `docs/01_design/10_mast_requirements.md` section 8.9 already gives Act I.

Pair with:
- `docs/01_design/10_mast_requirements.md` section 8.9 — the Act I map this mirrors, and the canonical format
- `docs/01_design/00_scenario_play_guide.md` Scenes 5-15 — the scenes these gates serve
- `docs/04_implementation_setup/60_mast_api_cookbook.md` — every "preferred detection" below cites a section and evidence tag
- `docs/04_implementation_setup/80_slice_packets_07_16.md` — the packets that consume this

---

# 1. Standing of this document

This is **build-side elaboration, not design authority**, on the same footing as `80_slice_packets_07_16.md`. Where this and a design doc differ, the design doc wins and the difference is a finding.

It exists because `10_mast_requirements.md` section 8.9 is, in the handoff protocol's own words, "the only canonical automation gate map — it covers Act I only." Ten packets remain (07A/B, 09A/B, 11A/B, 12A/B, 15A/B), all in Acts II/III, and without a table each will invent gate/fallback pairs independently.

**To promote into canon:** the operator ratifies this into `10_mast_requirements.md` as section 8.10, following the dated `operator-ratified YYYY-MM-DD` convention established in that document's section 17. Until then it is a proposal and no slice packet should cite it as authority — cite it as a starting point and record the gate actually chosen in the packet.

---

# 2. How to read the table

Same three-tier discipline as section 8.9 and `00_source_index.md` section 8:

1. **Automatic** — runtime reads state and decides. Preferred.
2. **Comms/captain confirmation** — a human asserts it happened. Second.
3. **GM manual mark** — final fallback only.

Two columns are added beyond the Act I format, because Acts II/III carry far more API risk than Act I did:

- **Evidence** — the cookbook section backing the preferred detection, with its tag. `[LIVE]` means proven in this repo's runtime. `[UNPROVEN]` means it is a design intent, not a capability claim.
- **Confidence** — whether the preferred detection is expected to work.
  - **HIGH** — same shape as something already `[LIVE]` here.
  - **MED** — plausible from proven primitives, but the exact call is untried.
  - **LOW** — no proven primitive; treat the fallback as the likely primary.

**A LOW-confidence row is a spike candidate, not a build instruction.** The most expensive mistake available in Acts II/III is writing a packet that assumes an automatic gate, discovering live that Cosmos does not expose it, and burning a crewed session. Section 5 lists the rows that must be spiked before their packet is written.

---

# 3. Act II gates (Slice 07)

| Gate | Preferred detection | Evidence | Conf | Fallback |
|---|---|---|---|---|
| Anderson new-orders transmission fires | runtime timer after Act I completion flag | cookbook 5.1 `[LIVE]` | HIGH | GM trigger |
| Captain acknowledges orders | Comms menu/action | cookbook 6.1 `[LIVE]` | HIGH | GM mark |
| Course set toward Khovan Reach | heading/position delta over time | cookbook 9.1 `[LIVE]` | MED | Helm/captain confirmation |
| Sustained warp transit underway | ship speed/throttle read | cookbook 9.1 `[LIVE]` | MED | Helm confirmation |
| Energy depletion visible to Engineering | ship energy value read | cookbook 9.1 `[LIVE]` | HIGH | Engineering confirmation |
| Distress signal detected at sensor range | distance to Halcyon Drift object | cookbook 9.1 `[LIVE]` | HIGH | GM trigger |
| Science triangulates/classifies source | Science scan route on Halcyon Drift | cookbook 7.1 `[LIVE]` | HIGH | Science/captain confirmation |
| Captain commits to deviate | Comms menu/action or heading change | cookbook 6.1 `[LIVE]` | MED | GM mark (decision is verbal) |
| Arrival at Halcyon Drift | distance threshold | cookbook 9.1 `[LIVE]` | HIGH | GM mark |
| Science scans Halcyon Drift damage state | Science scan route | cookbook 7.1 `[LIVE]` | HIGH | Science/captain confirmation |
| Comms opens hail to Hessler | Comms route on Halcyon Drift | cookbook 6.1 `[LIVE]` | HIGH | GM mark |
| Captain authorizes Engineering deployment | Comms menu/action | cookbook 6.1 `[LIVE]` | MED | GM mark |
| Engineering away-team state entered | **none — fictional state** | — | LOW | **GM mark is primary** (see 4.1) |
| DAMCON team Reyes/Park/Achebe detached | shared state set by the deployment gate | cookbook 4.1 `[LIVE]` | HIGH | — (runtime-owned) |

---

# 4. Act III gates (Slices 09, 11, 12, 15)

## 4.1 Away mission and cascade (Slice 09)

| Gate | Preferred detection | Evidence | Conf | Fallback |
|---|---|---|---|---|
| Hessler conversation beats reached | **none — external GPT-4o** | — | LOW | **GM mark is primary, by design** |
| Convergence reveal relayed to bridge | Comms menu/action by Engineering | cookbook 6.1 `[LIVE]` | MED | GM mark |
| Cascade event fires | runtime timer from deployment | cookbook 5.1 `[LIVE]` | HIGH | GM trigger |
| Suit-O2 timer starts | runtime timer, run-ID guarded | cookbook 5.1 `[LIVE]` | HIGH | — (runtime-owned) |
| DAMCON reports at interval | scheduled task, run-ID guarded | cookbook 5.1 `[LIVE]` | HIGH | GM reads report aloud |
| Timer config extended vs compressed | shared state from captain decision | cookbook 4.1 `[LIVE]` | HIGH | GM sets |
| Engineer aboard Halcyon vs Artemis | **none — fictional state** | — | LOW | **Comms confirmation primary** |
| Captain commits engineer placement | Comms menu/action | cookbook 6.1 `[LIVE]` | MED | GM mark |
| Torpedo→energy conversion performed | torpedo count delta + energy delta | cookbook 9.1 `[LIVE]` | MED | Weapons/captain confirmation |
| DAMCON outcome band resolved | elapsed timer vs threshold table | cookbook 5.1 `[LIVE]` | HIGH | — (runtime-owned) |

**On the two LOW rows.** Engineering's physical location is table fiction — the player stands up and moves to a chair. There is no ship-side state to read, and inventing one would be modelling the room, not the mission. GM mark and Comms confirmation are the *correct* answers here, not concessions. Section 8.9 already accepts this shape for the Act I DAMCON rows.

**On the Hessler row.** The GPT-4o conversation is outside Cosmos entirely. Beat completion is a GM judgment by construction. Do not attempt detection.

## 4.2 Cache run (Slice 09/10 boundary)

| Gate | Preferred detection | Evidence | Conf | Fallback |
|---|---|---|---|---|
| Departure for Khovan Reach | distance from Halcyon Drift increasing | cookbook 9.1 `[LIVE]` | HIGH | Helm confirmation |
| Arrival at cache | distance to cache object | cookbook 9.1 `[LIVE]` | HIGH | GM mark |
| Comms hails cache dock control | Comms route on cache object | cookbook 6.1 `[LIVE]` | HIGH | GM mark |
| Docking with cache complete | docking event/state | cookbook 9.2 `[LIVE]` | MED | GM mark |
| Science selects correct component | **no proven list-selection UI** | — | LOW | **GM-presented list + Comms confirmation** |
| Wrong component detected at install | shared state comparison at repair gate | cookbook 4.1 `[LIVE]` | HIGH | — (runtime-owned) |
| Return transit to Halcyon Drift | distance threshold | cookbook 9.1 `[LIVE]` | HIGH | GM mark |

**On the component-selection row.** This is the highest-value LOW in the document. The play guide gives Science a four-option inventory with deliberate foils, and the qualification card depends on the choice being Science's. Nothing in the cookbook proves a selectable list UI. Options, in preference order:

1. **Comms menu as the list.** Each component is a Comms menu entry on the cache object. Uses only proven routes; the choice is real and runtime-readable. Fiction cost: a cache inventory arriving over Comms rather than a Science console readout. **Recommended.**
2. GM presents the list verbally, Science answers, GM marks. Zero API risk, full GM load, choice not runtime-readable.
3. Spike a Science-console list UI. Highest fidelity, unknown feasibility, `@gui` is currently forbidden in active MAST by `test_gm_only_test_mode_spike_controls_exist`.

Option 1 needs a design ruling because it changes the player-facing fiction. Routed, not decided.

## 4.3 Pirate arrival and deception (Slice 11)

| Gate | Preferred detection | Evidence | Conf | Fallback |
|---|---|---|---|---|
| Pirate arrival timer fires | runtime timer from cascade | cookbook 5.1 `[LIVE]` | HIGH | GM trigger |
| Pirate vessels spawn | `npc_spawn` + existence check | cookbook 8.1 `[LIVE]` | HIGH | — (runtime-owned) |
| Science detects contacts | Science scan route | cookbook 7.1 `[LIVE]` | HIGH | Science/captain confirmation |
| Science scan returns suspicious signatures | shared state set by scan route | cookbook 4.1 `[LIVE]` | HIGH | GM mark |
| Comms hails the claimed salvagers | Comms route on pirate objects | cookbook 6.1 `[LIVE]` | HIGH | GM mark |
| Credentials requested | Comms menu/action | cookbook 6.1 `[LIVE]` | HIGH | GM mark |
| Legal posture challenged | Comms menu/action | cookbook 6.1 `[LIVE]` | HIGH | GM mark |
| Cultural mismatch observed | **judgment — player reads a tell** | — | LOW | **GM mark is primary, by design** |
| `pirate_cover_status` advances | shared state transitions from above | cookbook 4.1 `[LIVE]` | HIGH | — (runtime-owned) |
| Docking requested/denied | Comms menu/action | cookbook 6.1 `[LIVE]` | HIGH | GM mark |
| Unauthorized docking attempt | runtime timer after denial | cookbook 5.1 `[LIVE]` | HIGH | GM trigger |

**On the cultural-mismatch row.** The play guide calls this "the deepest tell." Whether a player *noticed* an inconsistency is not machine-readable. What is machine-readable is whether they acted on it — a Comms menu entry such as "Challenge Skaraani credential inconsistency" converts the judgment into a recordable action without scoring the thought. That is a content-design question for Pass 2 dialogue, and belongs in `docs/02_content/10_pirate_dialogue.md`. Routed.

## 4.4 Combat and outcomes (Slice 12)

| Gate | Preferred detection | Evidence | Conf | Fallback |
|---|---|---|---|---|
| Captain authorizes force | Comms menu/action | cookbook 6.1 `[LIVE]` | MED | GM mark |
| Pirates transition to hostile | role/behaviour change on spawn objects | cookbook 8.1/8.2 `[UNPROVEN]` | MED | GM trigger |
| Weapons engages pirates | `//damage/object` hook on pirate role | cookbook 7.3 `[LIVE]` | HIGH | GM mark |
| Subsystem targeting on pirates | `MANUAL_SYSTEM` inventory read | cookbook 7.3 `[LIVE]` | HIGH | Weapons/captain confirmation |
| Pirate destroyed | `//damage/destroy` + source guard | cookbook 7.3 `[LIVE]` | HIGH | GM mark |
| Pirate surrenders | shared state on damage threshold | cookbook 4.1 `[LIVE]` | MED | GM mark |
| Pirate flees | **no proven despawn-on-flee behaviour** | — | LOW | GM mark + cleanup routine |
| Halcyon Drift damaged during combat | damage hook on Halcyon object | cookbook 7.3 `[LIVE]` | MED | GM mark |
| Engineering harmed if aboard | **fictional state** | — | LOW | **GM mark is primary** |

**Reuse note.** Every `[LIVE]` tag in this subsection traces to Slice 06's drone work. The destroy-source guard in `act1_drone_contact_fire.mast` is directly reusable and *must* be — `sbs.delete_object()` firing the same `//damage/destroy` hook as a real kill is a confirmed live finding, and pirate cleanup will hit it identically. See section 4 of the `scripts/lib/` proposal.

## 4.5 Repair, debrief, checkpoint (Slices 13-15)

| Gate | Preferred detection | Evidence | Conf | Fallback |
|---|---|---|---|---|
| Correct component installed | shared state comparison | cookbook 4.1 `[LIVE]` | HIGH | — (runtime-owned) |
| Halcyon reactor restored | shared state + objective broadcast | cookbook 4.1 `[LIVE]` | HIGH | — (runtime-owned) |
| DAMCON outcome reported | timer band resolution | cookbook 5.1 `[LIVE]` | HIGH | GM reads outcome |
| Return course set | distance/heading | cookbook 9.1 `[LIVE]` | MED | Helm confirmation |
| Debrief clips played | GM-driven | — | LOW | **GM mark is primary, by design** |
| Checkpoint payload written | shared state serialisation | cookbook 4.1 `[UNPROVEN]` | MED | — (spike required) |
| Checkpoint restored after ship loss | story jump + state seed | cookbook 4.5 `[LIVE]` | MED | GM manual re-seed |
| Irreversible state preserved across reload | explicit non-restored flag set | cookbook 4.1 `[LIVE]` | HIGH | — (runtime-owned) |

**On irreversible state.** `00_source_index.md` section 8 is explicit: "Reload is not tactical rewind. Reload must not undo committed consequences." DAMCON deaths, expended torpedoes, and pirate outcomes must survive a checkpoint restore. That is a *design invariant*, not a gate, and Slice 15's packet should carry it as an acceptance criterion rather than a detection rule.

---

# 5. Rows that must be spiked before their packet is written

Ranked by cost of discovering the problem live:

| # | Row | Slice | Why it must be spiked first |
|---|---|---|---|
| 1 | Science component selection | 09/10 | No proven list UI; drives a qualification card. If option 1 above is rejected there is no fallback that keeps the choice runtime-readable. |
| 2 | Checkpoint payload round-trip | 15 | Already flagged in handoff protocol 3.2. If state cannot round-trip, the no-fail design premise fails. |
| 3 | Pirate hostile transition | 12 | `[UNPROVEN]`. If roles/behaviour cannot flip post-spawn, pirates must spawn hostile, which breaks the salvage-cover fiction. |
| 4 | Pirate flee/despawn | 12 | No proven behaviour; affects cleanup and the `pirate_outcome` state model. |
| 5 | Cache docking | 09/10 | Docking wrapper is proven for Tarsis; the cache is a different object class. |

Rows 3 and 4 can share one Slice 12 Phase A spike. Rows 1 and 5 can share one Slice 09/10 spike.

---

# 6. What this document deliberately does not do

- It does not assign slice IDs to gates. `80_slice_packets_07_16.md` owns that.
- It does not decide the Science-selection fiction, the cultural-tell menu shape, or anything else marked "Routed." Those are design calls under `AGENTS.md` section 2.
- It does not claim any `[UNPROVEN]` row will work. Confidence is an estimate of risk, not evidence.

---

# 7. Revision

Rev 1.0 (2026-08-08) — initial proposal, written against play guide Scenes 5-15 and cookbook tags as of `slice06-drone-contact-fire`.
