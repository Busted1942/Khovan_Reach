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

**On the component-selection row — already decided; cite, do not re-open.**

Rev 1.0 of this document presented this as an open design question with three
options. That was written without reading the Slice 10 packet, which had already
resolved it. The packet's Known Risks field states:

> "The requirements specify option semantics but not the presentation mechanism;
> the cookbook has no proven inventory/selection-prompt pattern. Expect to use a
> Comms-route option list (the proven pattern) rather than inventing a UI. Raise
> an API-uncertainty block if tempted to do otherwise."

That is the ruling. The Comms-route option list is the expected mechanism, and the
escalation path for deviating from it is already specified. The `LOW` confidence
rating above stands — there is genuinely no proven list UI — but it is a known
constraint with a chosen workaround, not an open question.

Slice 10 also already owns the semantics (four option classes, `cache_retry_required`
on a wrong first pick, a timer-consequence marker recording the cost) and the
`cache_selection_fallback_available` flag. Nothing here supersedes any of it.

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

# 5. Relationship to the existing slice packets

**Correction, 2026-08-08.** Rev 1.0 of this section listed five rows as "must be
spiked before their packet is written." That framing was wrong and is retracted.
All ten packets in `80_slice_packets_07_16.md` are already written, and they
already flag their own spikes. This document does not lead that work; it
supplements it.

What the packets already establish, verified by reading them:

| Row flagged here | Already covered by | Standing |
|---|---|---|
| Science component selection | Slice 10 Known Risks | **Already decided** — see below |
| Checkpoint payload round-trip | Slice 15, marked **SPIKE REQUIRED** | Already flagged |
| Pirate hostile transition | Slice 12 Phase A, marked **SPIKE REQUIRED** | Already flagged, and the packet already records the cookbook gap |
| Pirate flee/despawn | Slice 12 Phase B tasks 1-2 | Already scoped |
| Cache docking | Slice 10 task 2 | Scoped, reusing the 07B cleanup helper |

Slices 09, 11, 12, and 15 all carry an explicit **SPIKE REQUIRED** header in the
packets. That is the authoritative spike list. This document adds no slices to it.

**What this document does add**, and why it is still worth ratifying: the packets
carry nine `*_fallback_available` flags spread across ten slices, but no
consolidated preferred-detection table. Section 8.9 gives Act I one page showing
every gate, its detection, and its fallback side by side. Sections 3 and 4 above
are that page for Acts II/III, with two columns section 8.9 does not have —
a cookbook citation and a confidence rating. The value is the consolidated view
and the evidence tagging, not the identification of unknowns.

**Reading order when they disagree:** the packet wins. A packet is a build
contract with named files, state, and test IDs. This is a policy overview.
Any disagreement is a finding against this document, not against the packet.

---

# 6. What this document deliberately does not do

- It does not assign slice IDs to gates. `80_slice_packets_07_16.md` owns that.
- It does not decide the Science-selection fiction, the cultural-tell menu shape, or anything else marked "Routed." Those are design calls under `AGENTS.md` section 2.
- It does not claim any `[UNPROVEN]` row will work. Confidence is an estimate of risk, not evidence.

---

# 7. Revision

Rev 1.1 (2026-08-08) — corrected against `80_slice_packets_07_16.md`, which rev 1.0
had not been read against. Three changes:

- Section 5 retracted and rewritten. It had claimed five rows "must be spiked
  before their packet is written." All ten packets already exist, and Slices 09,
  11, 12, and 15 already carry **SPIKE REQUIRED** headers. The packets are the
  authoritative spike list.
- The component-selection discussion retracted. It had posed an open design
  question with three options; Slice 10's Known Risks had already chosen the
  Comms-route option list and specified the escalation path.
- Added the precedence rule: where this document and a packet disagree, the
  packet wins and the difference is a finding against this document.

**Process note.** Rev 1.0 was written from the play guide and the cookbook without
reading the existing packets in full, and was marked ready to ratify. Had it been
ratified as written, it would have imported a retracted framing and a re-opened
design question into design authority. Any future document proposing policy over
Slices 07-16 must be cross-read against `80_slice_packets_07_16.md` before it is
offered for ratification.

Rev 1.0 (2026-08-08) — initial proposal, written against play guide Scenes 5-15 and cookbook tags as of `slice06-drone-contact-fire`.
