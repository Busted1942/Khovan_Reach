# KHOVAN REACH

*Standalone TSN training scenario for Cosmos Starship Bridge Simulator. Canonical scene guide. Revision 2.2 merged.*

---

## SOURCE NOTE

This is the canonical v2.2 scene guide. It merges the original Pass 1 operational core with the later runtime architecture and the Act I shakedown-fork revision.

Supersedes, for active use:
- `docs/01_design/00_scenario_play_guide.md`
- `khovan_reach_act1_shakedown_fork_v0_5.md`
- `khovan_reach_act1_automation_gate_map_v0_2.md` as standalone Act I behavior sources

The original Pass 1, Act I v0.5, and automation gate map should be archived as design history.

---

## REVISION HISTORY

**Rev 2.3 Slice 04 implementation finding (current)** - Artemis visibly starts with ship energy at 0, generator governor active, and no loaded ordnance. Kestrel holds the two-homing emergency reserve until Comms requests it. Tarsis normal docking/resupply restores full energy and armament and clears the governor.

**Rev 2.2 (current)** — Cleanup pass. Changes:
- Corrected DAMCON outcome thresholds in Scene 14 and timing notes to match the current source index and GM notes: extended T+30 total-loss threshold, compressed T+15 total-loss threshold.
- Updated design-facing salvage-cover language to clarify pirates under salvage cover while preserving player-facing "salvager" fiction before exposure.
- Updated source references from v2.1 to v2.2.

**Rev 2.1** — Act I shakedown fork merged. Changes:
- Added Full Shakedown / Compressed Shakedown / Direct Scenario fork.
- Earlier model replaced visible low-energy start with generator-output governor and delayed Kestrel advisory; Slice 04 now intentionally combines visible ship energy = 0 with the generator governor.
- Earlier model loaded 2 homing torpedoes at departure; Slice 04 now starts at 0 homing and lets Kestrel load exactly 2 only after the emergency reserve request.
- Added upper-left lifeform overlay plus Comms archive echo for training/instruction text.
- Added Tarsis production-priority and generator-acceptance gates before docking.
- Added expanded Engineering systems shakedown and automation-gate preferences.
- Clarified that skipped shakedown observations are N/A, not failures.

**Rev 1.2** — Act I drill block baked in. Changes:
- Reworked Drill Two into a guided, step-by-step contact-handling tutorial ending in controlled Weapons subsystem disable
- Reworked Drill Three into the unguided evasive live-fire repeat ending in Engine subsystem disable
- Updated Act I timing from ~25 minutes to ~28-30 minutes

**Rev 1.1** — Updated against revised outline. Changes:
- Added "Reactive, not procedural" and "Weapons must have a real live-fire role" as labeled design principles in Section 1
- Added negative-space guardrail in Captain's Briefing materials clarifying what Anderson must NOT mention in his diversion orders
- Replaced prose description of pirate captains in Scene 12 with bulleted design requirements
- Added enumerated pirate state variables to inform Pass 2 dialogue scripting and Pass 3 MAST scripting
- Adjusted Scene 11 timing from "~8 min" to "~8-10 min" to match outline
- Promoted "pirate cover intact / suspected / exposed" as primary state model for the deception detection logic

**Rev 1.0** — Initial Pass 1 from original outline.

---

## 1. MISSION OVERVIEW

### Concept

Khovan Reach is a TSN cruiser mission with an embedded qualification framework for a new crew. The fiction is foreground; qualification observation runs underneath. Players experience a real operational mission with real stakes; the instructor surfaces what was being measured at the debrief.

Artemis is dispatched to investigate a fragmentary distress signal in a quiet region near Khovan Reach. They find a damaged civilian cargo hauler, a crew in genuine distress, and — eventually — opportunistic pirates exploiting the situation under the pretense of being salvagers.

The mission tests six bridge stations through coordinated play rather than discrete drill checks. Helm dockings and transits; Weapons subsystem targeting and torpedo management; Engineering power balance, away mission diagnosis, and the personal-stakes decision; Science long-range sensors, threat classification, and component identification; Comms station hailing, multi-relay coordination, cultural-fluency negotiation, and deception detection; Captain investigation authorization, resource allocation, force authorization, and command judgment under pressure.

The tone is lighter than Sigma Protocol — no moral triangle, no hidden conspiracy, no doctrine confession — but the dramatic weight is real. Engineering may be in personal danger. The DAMCON team may die. The pirates are a genuine combat threat. Failures cost lives. The captain's choices have measurable consequences.

### Design Philosophy

**Console play is the default.** Six players, six stations, mission run through the SBS consoles. The only departure from console play is the brief Engineering away mission to Halcyon Drift, where the Engineering player physically leaves their console but stays at the table for an observed GPT-4o conversation with Hessler.

**Voice-mode AI is limited.** One GPT-4o NPC — Hessler. Lightweight, cooperative, no tier gating. Used to expose the team to voice-mode roleplay before they encounter the harder version in Sigma Protocol. All other NPC dialogue (Anderson, Dillon, pirates under salvage cover, DAMCON team) is delivered through recorded clips or GM voice over Comms console exchanges.

**Qualification is observation, not testing.** Players see no qualification cards during play. Dillon surfaces them at debrief. The mission is played as a real operation; competence is measured by what players actually do, not by checking items off a visible rubric.

**No-fail with real costs.** Catastrophic failures (ship destruction) trigger a MAST state-save reload to the last drill checkpoint with prior qualifications preserved. Non-catastrophic failures (DAMCON casualties, Halcyon Drift loss, weapons depletion) are absorbed into qualification cards and acknowledged at debrief. The team always finishes the mission.

**Reactive, not procedural.** Anderson's orders dispatch Artemis to investigate, not to fetch a known item. The cache run develops in the field, under pressure, after Engineering diagnoses Halcyon Drift's damage. The captain's decisions emerge from discovery, not from a pre-briefed plan.

**Weapons must have a real live-fire role.** The pirate-under-salvage-cover element of Act III is not pure negotiation. The pirates-under-cover design gives Comms a deception-detection beat and then gives Weapons a real combat beat if the situation goes hot. This is intentional balancing — earlier design iterations over-served Comms and left Weapons under-exercised.

### Session Targets

- Total session length: variable by Act I fork
- Full Shakedown Cruise: approximately 115-125 minutes total
- Compressed Shakedown Cruise: approximately 100-110 minutes total
- Direct Scenario: approximately 85-95 minutes total
- Act II — Investigation: ~15 minutes
- Act III — Halcyon Drift and Khovan Reach: ~50 minutes
- Debrief: ~10 minutes
- Crew complement: six players (Captain, Helm, Weapons, Engineering, Science, Comms) plus GM

---

## 2. CAPTAIN'S BRIEFING MATERIALS

### Ship State at Mission Start

**TSN Cruiser Artemis** — just out of Kestrel Yards refit cycle.

- Hull: full integrity
- Energy: visible ship energy = 0 at fresh load
- Generator status: temporary generator-output governor active; yard crews are still working the generator problem
- Practical effect: Artemis is not mission-ready until the Kestrel/Tarsis flow is completed; Tarsis restores full energy and armament and clears the governor during normal docking/resupply
- Torpedoes: 0 loaded at fresh load; Kestrel holds 2 homing torpedoes as emergency reserve and loads them only after Comms requests the reserve
- No nukes, no EMPs, no mines until Tarsis resupply
- Coolant: full
- DAMCON teams: standard complement (six teams, three personnel each)
- Crew: full bridge complement, all new to this ship together

The crew should discover the generator limitation through play. Do not front-load it in the opening briefing. Let the ship feel slow after departure; Kestrel Yard Control explains it ten seconds after launch-envelope exit.

### Mission Orders (as briefed by Dillon at scenario start)

Routine qualification cruise. Standard pattern: depart Kestrel Yards, dock-and-resupply at Tarsis Station, conduct a shakedown profile selected by the captain, return for debrief. The captain may choose Full Shakedown, Compressed Shakedown, or Direct Scenario after launch. Dillon is embedded as instructor.

Standard rules of engagement: defensive posture, hailing before any escalation, deference to TSN protocol. No live combat is anticipated.

### Anderson Diversion Orders (transmitted during Act II)

After the selected Act I profile completes, Anderson transmits new orders.

A fragmentary distress signal has been detected in the Khovan Reach region by long-range monitoring. The signal is on a TSN-compatible frequency band but is too degraded for definitive identification. Pattern suggests either civilian emergency beacon or possibly a TSN vessel in trouble. No other TSN assets are within response range. Artemis is the closest cruiser-class ship with operational capability.

Orders: investigate the signal source, render aid as appropriate, report findings. Estimated transit: approximately 90 minutes from Tarsis at standard cruise. Anderson notes that the qualification framework remains in effect — this transitions from drill scenario to live operation, but Dillon retains observation authority.

**Guardrail for Anderson's orders.** Anderson must NOT mention quantum field stabilizers, the Khovan Reach cache as a fetch target, or any specific component that Halcyon Drift will need. The cache is referenced only as regional context (TSN maintains forward-deployed scientific caches in this region, as it does in several lightly patrolled regions). Mentioning the stabilizer or framing the mission as a fetch reintroduces the original design contrivance that this revision was built to eliminate. If you find yourself writing Anderson dialogue that names the part, stop and rewrite.

### Captain's Information State

The captain has the following before encountering Halcyon Drift:

- The distress signal is fragmentary and TSN-frequency-compatible
- Source identification is not possible from current sensor data
- Region is normally quiet — civilian shipping lanes nearby, occasional independent operators, no recent hostile activity reports
- TSN has standing forward-deployed scientific caches in the broader region (Khovan Reach itself is one such cache location)
- Standard ROE applies; aid is mandatory if a TSN-flagged vessel is in distress

The captain does *not* know:
- That Halcyon Drift is Vesperan civilian
- That the damage is a reactor regulator failure
- That a quantum field stabilizer from the Khovan Reach cache is the only component that can repair Halcyon Drift
- That pirates are inbound under salvage cover

These facts develop during the mission through investigation and Engineering's away-mission diagnosis.

---

## 3. SCENE-BY-SCENE PLAY GUIDE


### ACT I — QUALIFICATION CRUISE / SHAKEDOWN FORK (~10-45 min)

#### Act I delivery rule

Until final UI exists, all training/instruction/advisory text displays in two places:

1. **Upper-left lifeform overlay** — temporary visible prompt channel for the whole bridge.
2. **Comms Officer's console archive** — durable message log so Comms can review prior instructions and advisories.

The lifeform overlay is temporary build scaffolding. In-fiction, these messages are Kestrel Yard Control, Tarsis Control, or Dillon. Do not treat them as a new NPC.

**Revision note (operator-ratified 2026-08-08) — "Training Control" is retired as a speaker.** Earlier text used "Training Control" as a faceless instructional voice alongside Dillon, and one message was even attributed to "Dillon / Training Control". That split the instructor role across two names for no design gain, and it wasted the character the crew is meant to recognise again in the next mission.

All instructional and drill traffic is now **Dillon**, the instructor embedded aboard Artemis. Kestrel Yard Control and Tarsis Control remain distinct — they are external stations performing real operational functions (yard-lock, generator acceptance, docking clearance, resupply), not instruction.

Delivery convention that follows from this:

- **Comms messages** render a sender name. Dillon speaks in the first person; the body must not repeat "Dillon:" as a prefix, because the title already carries it.
- **Current Objective panel** broadcasts body text only — no sender is rendered. Objective text is therefore terse in-world instruction with no speaker prefix.

Implemented on `slice06-dillon-voice-and-prompt-polish`. Player-facing copy was also corrected for spelling and for design-language leakage ("no failure state", "fallback confirmation", "damage observer") that was reaching player consoles.

---

#### Scene 1: Kestrel Departure, Generator Advisory, and Shakedown Fork (~5-7 min)

**Setting:** Artemis on the launch ramp at Kestrel Yards. Bridge crew at stations. Dillon present, standing behind the Captain's chair.

**Play:** Play Dillon Clip 1. The clip still frames the qualification cruise and hands the ship to the captain.

**Initial runtime state:**

```text
starting_energy = 0
generator_governor_active = true
starting_homing_torpedoes = 0
homing_reserve_count = 2
energy_restored = false
launch_envelope_cleared = false
kestrel_generator_packet_sent = false
shakedown_mode = unset
```

**Gate:** Artemis remains at Kestrel until Comms requests departure clearance from Kestrel Yard Control and clearance is granted. Helm cannot be released into the launch envelope before that request.

**Expected sequence:**

1. Captain conducts readiness check.
2. Comms requests departure clearance.
3. Kestrel grants departure.
4. Helm clears the launch envelope.
5. The ship feels sluggish once underway.
6. Ten seconds after launch-envelope exit, Kestrel transmits the generator advisory.
7. Dillon / Training Control gives the captain the shakedown choice.

**Kestrel delayed advisory — overlay and Comms archive:**

> "Artemis, Kestrel Yard Control. Advisory packet follows. Your generator assembly is still under observation. We are working a regulator-output problem on our end and have placed a temporary governor on your generator output. You may see sluggish acceleration and reduced sustained-speed response until Tarsis accepts the generator handoff and clears the governor."
>
> "Kestrel holds two homing torpedoes as emergency reserve and will load them only after Comms requests the reserve. Tarsis has been notified to prioritize homing torpedo production, generator acceptance, and energy restoration."

**Dillon / Training Control speed-power reminder — overlay and Comms archive:**

> "Training Control note: speed and energy consumption are not linear. The faster you go, the more sharply energy expenditure rises. High speed may solve a timing problem and create an energy problem. Captain and Engineering should keep that tradeoff visible."

**Fork point — captain selects profile:**

```text
FULL_SHAKEDOWN: run the expanded onboarding sequence.
COMPRESSED_SHAKEDOWN: run only essential gates.
DIRECT_SCENARIO: complete expedited Tarsis resupply, then proceed directly to the operational scenario.
```

Skipped drill observations are recorded as N/A / not observed by captain election. They are not scored as failures.

---

#### Branch A: Full Shakedown Cruise

##### Scene 2A: Tarsis Production Priority, Generator Acceptance, Docking, and Resupply (~8-10 min)

**Objective:** Teach Comms station protocol, docking clearance, armament production priority, and resupply handoff.

**Gate:** Tarsis docking does not unlock until Comms has completed all three required requests:

1. request homing torpedo production priority
2. request generator acceptance/support
3. request docking clearance

**Expected sequence:**

1. Comms hails Tarsis.
2. Comms asks Tarsis to focus production on homing torpedoes.
3. Comms requests generator acceptance/support for the Kestrel governor issue.
4. Comms requests docking clearance.
5. Helm docks only after clearance.
6. Engineering supports docking state.
7. Tarsis clears generator-output governor and restores normal output.
8. Resupply loads full operational complement.

**Tarsis response after homing priority request:**

> "Tarsis Control acknowledges. Homing torpedo production priority set for Artemis. Other ordnance will load as available after homing complement is restored."

**Tarsis response after generator support request:**

> "Generator acceptance packet received. We can clear the Kestrel governor after docking and yard-lock synchronization. Do not assume full acceleration response until transfer complete."

**Completion:** Play Dillon Clip 3 when resupply is confirmed and the generator governor is cleared.

---

##### Scene 3A: Engineering Systems Shakedown (~8-10 min)

**Objective:** Teach Engineering impulse/warp power, apparent motion validation, DAMCON routing, controlled overload, repair supervision, and navigation priority presets.

**Step 3A.1 — impulse zero / warp 200**

Training Control instructs Engineering:

> "Engineering: set impulse engines to zero percent and warp engines to two hundred percent. Captain: once Engineering reports set, order undock and full impulse. Helm should validate no movement."

**Gate:** Runtime should automatically detect no forward motion after full-impulse order if available. Otherwise, captain/Helm confirmation is acceptable.

**Step 3A.2 — DAMCON rest-cycle standby**

> "Engineering: assign DAMCON teams to crew quarters and place them on rest-cycle standby. Captain: require confirmation through Comms."

**Preferred fallback:** DAMCON team location may not be mechanically visible. Use Comms message: "DAMCON Control confirms rest-cycle standby in crew quarters." GM mark only if Comms routing is unavailable.

**Step 3A.3 — DAMCON meal-cycle standby**

> "Engineering: assign DAMCON teams to the mess and place them on meal-cycle standby. Captain: require confirmation through Comms."

**Preferred fallback:** Comms message: "DAMCON Control confirms meal-cycle standby in mess." GM mark only if needed.

**Step 3A.4 — controlled overload**

> "Engineering: set impulse and warp engine output to three hundred percent. Allow the overload to occur. Do not prevent it. This is a controlled damage-and-repair exercise."

**Gate:** Runtime should detect engine damage or overload state if possible.

**Step 3A.5 — repair supervision**

> "Engineering: assign repair crews and supervise repair until engine output is restored. Captain: hold movement orders until Engineering reports repair complete."

**Gate:** Runtime should detect repair completion if possible. Otherwise Engineering report + Comms/captain confirmation.

**Step 3A.6 — navigation priority preset**

> "Engineering: set a navigation priority preset suitable for sustained transit. Captain and Helm: acknowledge when Helm has usable response."

**Completion:** Proceed to stationary drone drill.

---

##### Scene 4A: Stationary Drone Controlled Disable (~12-15 min)

**Objective:** Teach identification, hailing, shield-frequency relay, beam lock, range discipline, manual subsystem targeting, authorization, and ceasefire.

**Target:** Drone 01. Normal enemy ship object, non-attacking AI. It should not fire on Artemis.

**Required sequence:**

1. Drone 01 appears at range.
2. Captain orders intercept.
3. Science scans the drone.
4. Comms hails the vessel.
5. Science relays weak shield frequencies to Weapons.
6. Weapons locks beams.
7. Captain orders Helm to position Artemis between 1 and 2 km from Drone 01.
8. Artemis remains stationary in the band for 15 seconds.
9. Weapons is locked on.
10. Runtime clears Weapons to disable the Weapons array only.
11. Weapons switches to manual targeting and targets Drone 01 Weapons array.
12. Weapons disables the Weapons array in three confirmed manual subsystem hits.
13. Captain calls ceasefire.

**Weapons reminder — overlay and Comms archive:**

> "Training Control note for Weapons: beam rate and beam intensity are directly correlated. A direct hit to a subsystem can be effective even with a weak beam. Precision matters more than brute force in a disable order."

**Early-fire reset:**

If Weapons hits Drone 01 before authorization, Drone 01 despawns and respawns five kilometers farther from the Tarsis Training Beacon. Reset lock/range/stationary timer and send:

> "Training Control: unauthorized hit detected. Target reset. Reacquire, reestablish range, and wait for clearance."

**Drone-destruction reset:**

If the captain allows Drone 01 to be destroyed, Drone 01 respawns five kilometers farther from the Tarsis Training Beacon. Send:

> "Training Control: target destroyed. Drill objective was controlled subsystem disable. Target reset for repeat."

**Completion:** Remove Drone 01 when Weapons array is disabled and ceasefire is confirmed.

---

##### Scene 5A: Live-Fire Target Destruction (~6-8 min)

**Objective:** Transfer the controlled sequence into a simpler combat-resolution task.

**Target:** Drone 02 / live-fire target spawns ten kilometers away. It may maneuver but should not create a lethal training scenario.

**Instruction:**

> "Training Control: live-fire target deployed at ten kilometers. Captain: engage and destroy the target. Science, Helm, Weapons, Engineering, Comms: coordinate as standard."

**Gate:** Target destruction is automatic where object-destroyed events are available.

**Completion:** On target destruction, play completion training message and proceed.

---

##### Scene 6A: Cultural Comms Packet and Act II Transition (~2-3 min)

**Comms cultural packet — overlay and Comms archive:**

> "Training Control note for Comms: hostile contact handling is not only tone control. Different species, fleets, and political groups value different things. Cultural knowledge can help you diffuse a situation, pressure a contact, or detect a false identity. When a contact's claimed culture and actual conduct do not match, report it."

**Transition:** Anderson Clip 1 may now interrupt the return-to-debrief plan and move the cruise into Act II.

---

#### Branch B: Compressed Shakedown Cruise

Compressed mode preserves the essential learning gates while removing extended practice.

**Required compressed gates:**

1. Kestrel departure clearance.
2. Delayed generator advisory.
3. Tarsis homing priority + generator support + docking clearance.
4. Tarsis docking and resupply clears governor.
5. One compact controlled-disable target: scan, hail, frequency relay, lock, 1-2 km band, 15-second stationary hold, authorized Weapons-array disable.
6. Optional quick live-fire destroy target if time permits.
7. Cultural Comms packet.
8. Act II transition.

Skipped Engineering practice steps are N/A / development-only, not failures.

---

#### Branch C: Direct Scenario

Direct mode lets an experienced crew skip the shakedown drills.

**Required direct-mode gates:**

1. Kestrel departure clearance.
2. Delayed generator advisory.
3. Tarsis homing priority + generator support + docking clearance.
4. Tarsis docking and resupply clears governor.
5. Captain confirms shakedown bypass.
6. Act II begins.

**Overlay confirmation:**

> "Training Control: shakedown bypass accepted. Act I drill observations will be recorded as not observed by captain election. Live-operation observations remain active. Proceeding to operational scenario."

---

### ACT II — INVESTIGATION (~15 min)

#### Scene 5: New Orders (~3 min)

**Trigger:** Begins after Full Shakedown, Compressed Shakedown, or Direct Scenario resupply path completes.

**Setting:** Artemis returning from the training area, en route back toward Tarsis for the planned cruise debrief.

**Play:** GM plays Anderson Clip 1 (New Orders). The clip transmits on TSN command frequency, marked priority.

Anderson briefs:
- A fragmentary distress signal has been detected in the Khovan Reach region
- TSN-compatible frequency, too degraded for source identification
- Pattern consistent with civilian emergency or possible TSN vessel in trouble
- Artemis is closest TSN cruiser-class asset
- Orders: investigate, render aid, report findings
- Expected transit: ~90 minutes from current position
- Qualification framework remains in effect under Dillon's observation

Captain acknowledges. GM plays Dillon Clip 8 (Pivot Acknowledgment) — brief, notes the transition from drill scenario to live operation, qualifications continue.

**Station beats:**
- Captain: acknowledges orders, transitions ship posture from drill to operational
- Comms: confirms Anderson transmission, repeats orders for record
- Other stations: standby for course change

#### Scene 6: Long-Range Transit (~5 min)

**Setting:** Artemis transiting toward Khovan Reach at sustained warp.

**Play:** Helm engages warp and holds course. Engineering manages power for sustained high-speed transit. Energy depletion is visible to Engineering.

This is a quiet stretch. The crew settles into operational rhythm. GM may provide brief atmospheric notes (Khovan Reach is at the edge of routinely-patrolled space, occasional civilian shipping lanes pass nearby, sensors mostly empty).

If Dillon comments during the transit (GM-voiced, not a clip), the comments are observational, not corrective. Treat as a quiet moment that surfaces character.

**Station beats:**
- Helm: sustained warp course management
- Engineering: energy management during transit, reserves tracking
- Science: long-range passive sensor sweeps
- Comms: maintains Command reporting cadence
- Captain: situational awareness, brief check-ins with stations
- Weapons: passive standby

#### Scene 7: Distress Signal Detected (~4 min)

**Setting:** Approximately 60 minutes into transit. Sensor range now covers Khovan Reach's outer envelope.

**Play:** Science detects the partial distress signal at the edge of sensor range. The signal is degraded but trackable. Science triangulates and identifies:
- Source: a single vessel approximately 15 minutes off the direct route to Khovan Reach
- Vessel class: civilian cargo hauler, possibly mid-size
- Registry: not yet readable from signal degradation
- Signal pattern: authentic emergency beacon, not a hostile lure

GM provides this information to Science as a sensor read. Science reports to Captain via Comms.

Captain's decision: deviate to render aid, or continue on the briefed Khovan Reach investigation route.

The "correct" decision is to deviate — the distress signal is the investigation Anderson ordered. Captain who deviates is responding to orders correctly. Captain who hesitates or asks Dillon receives no guidance (Dillon does not intervene at decision points; this is the captain's call). Captain who refuses to deviate triggers the offramp scenario (see "Offramp" below).

For the main scenario, the captain deviates. Helm sets course to the distress signal source. Estimated arrival: 15 minutes.

**Station beats:**
- Science: detection, classification, source identification
- Captain: investigation deviation decision, decisiveness
- Helm: course change execution
- Comms: brief Command update on the deviation

**Offramp note:** If the captain refuses to deviate, GM plays an abbreviated Anderson follow-up that emphasizes "render aid as appropriate" and reissues the order more directly. If the captain still refuses, mission continues to Khovan Reach where the cache is found unused and Halcyon Drift is later reported lost. Debrief notes this as a serious failure of judgment. This path is not the design target; document for completeness but do not optimize for it.

#### Scene 8: Approach to Halcyon Drift (~3 min)

**Setting:** Artemis approaches the distress source on Helm's heading.

**Play:** As Artemis closes to scanner range:

- **Science** scans the vessel, now clearly visible. Identifies:
  - Vessel: Halcyon Drift, Vesperan-registered cargo hauler
  - Damage state: significant. Primary reactor offline. Hull integrity compromised in two sections. Emergency power active.
  - Crew status: signs of life. Estimated 6-8 individuals aboard. No combat signatures.
- **Comms** opens hailing channel. After initial signal handshake, Hessler responds. His voice is exhausted but stable. He confirms:
  - He is the captain
  - The reactor experienced a cascading regulator failure
  - Crew of 7, three injured
  - They have power for life support for several more hours but need professional engineering assistance to attempt repair
  - He explicitly requests an engineering team to assist

Captain authorizes Engineering deployment. The Engineering player stands up from their console, moves to the GPT-4o conversation position at the table (still observed by the rest of the crew), and prepares for the away conversation.

GM triggers MAST script: DAMCON team Reyes (lead), Park, and Achebe are deployed with Engineering. Three DAMCON resources are now removed from Artemis's pool until away mission completion.

**Station beats:**
- Science: damage assessment, crew status, threat assessment (none currently)
- Comms: opens hail to Halcyon Drift, establishes Hessler contact
- Captain: deploys Engineering with DAMCON team
- Engineering: transitions to away mission posture

End of Act II.

---

### ACT III — HALCYON DRIFT AND KHOVAN REACH (~50 min)

#### Scene 9: Away Mission to Halcyon Drift (~10 min)

**Setting:** Engineering and the DAMCON team aboard Halcyon Drift. Hessler meets them at the boarding airlock and escorts them to the damaged engineering section.

**Play:** GPT-4o conversation between the Engineering player and Hessler, observed by the whole table. The conversation runs naturally; what follows are the beats it should hit.

**Beat 1 — Introduction and damage walk-through.** Hessler greets Engineering, briefly thanks Artemis for responding. He walks them to the affected section. Describes the failure sequence: the primary reactor regulator showed warning signs, the crew began shutdown procedures, the regulator cascaded faster than the shutdown could complete, atmosphere was lost briefly in the secondary chamber but is now sealed and stable.

**Beat 2 — Diagnostic discussion.** Engineering asks diagnostic questions. Hessler answers from his ship's status — what systems were lost, what's still functioning, what the failure pattern looked like at the regulator interface. Engineering may identify the regulator failure pattern (a known issue with this class of regulator that TSN bulletins have flagged but Vesperan civilian operators have been slow to address). This is a Science/Engineering crossover knowledge beat — Engineering recognizes the symptoms.

**Beat 3 — The convergence reveal.** Engineering identifies that the required replacement is a quantum field stabilizer unit. Hessler confirms this. Engineering realizes: Khovan Reach hosts a TSN scientific cache, and that cache routinely stocks quantum field stabilizers for forward-deployed missions. The component Artemis is investigating Khovan Reach for *exists* at the cache, and it's exactly what Halcyon Drift needs.

This is the convergence beat. Engineering should relay this discovery to the bridge via Comms.

**Beat 4 — Repair preparation.** Engineering and the DAMCON team begin repair preparation work. Hessler describes the install location and the procedure his crew would normally follow. DAMCON team begins clearing access to the regulator assembly.

**Beat 5 — The cascade.** During the preparation work, a secondary structural element gives way. Atmosphere begins venting in the engineering section. Blast doors seal automatically. The DAMCON team — Reyes, Park, Achebe — is on the wrong side of the seal. They are now isolated in a section with active atmospheric loss and limited suit O2 reserves.

GM triggers MAST: cascade event. Suit O2 timer begins. Initial DAMCON status report comes through Comms: "Reyes here. Atmospheric pressure dropping in section 4. Suit O2 reads 30 minutes. We're attempting to seal the secondary bulkhead manually."

Hessler reacts in real time — apologetic, concerned, identifies the structural element that failed, notes that without active mitigation the section will lose atmosphere faster than the team's suits will hold.

Engineering reports back to the bridge with the full situation: convergence requires the cache component, cascade has trapped the DAMCON team, mitigation requires Engineering on-site, decision needed from the captain.

**Voice-mode notes:** Hessler is cooperative, civilian, exhausted but professional. He has no secrets to gate. He may not know all technical details Engineering asks about (he's a cargo captain, not an engineer) — appropriate to defer to Engineering's expertise on specifics. If Engineering asks something Hessler wouldn't know, Hessler should say so honestly. The cascade is a surprise to him as much as to Engineering; he is not responsible for it.

**Station beats during Scene 9 (for stations on Artemis):**
- Comms: relays Engineering reports, maintains bridge-to-away-team channel
- Captain: receives the convergence report, receives the cascade report, prepares for decision
- Science: scans Halcyon Drift continuously, may detect cascade structural signatures
- Helm: holds station alongside Halcyon Drift
- Weapons: passive standby

#### Scene 10: The Captain's Decision (~8 min)

**Setting:** Artemis bridge, with Engineering reporting from Halcyon Drift via Comms.

**Play:** The captain now has the full picture:
- DAMCON team trapped, suit O2 timer running
- Convergence: Khovan Reach cache holds the only available repair component
- Engineering on Halcyon Drift can slow atmospheric loss through hands-on mitigation
- Without Engineering on-site, atmospheric loss accelerates and DAMCON timer compresses
- Without the cache component, Halcyon Drift cannot be repaired (brick wall — confirm via Engineering report if captain attempts to repair without the part)

The captain must commit to one of three paths:

**Path A/B (Engineer stays on Halcyon Drift):** Engineering remains aboard. Atmospheric loss is mitigated. DAMCON timer runs at full 30-minute window. Artemis runs to Khovan Reach for the cache component, returns. Engineering is exposed to whatever happens at Halcyon Drift during Artemis's absence.

**Path C/D (Engineer returns to Artemis):** Engineering is withdrawn. Atmospheric loss accelerates without mitigation. DAMCON timer compresses to 15-minute window. Artemis runs to Khovan Reach with full crew complement, returns. Race condition: can Artemis fetch the part and return before T+15?

**Brick wall:** Captain refuses to depart, attempts repair without the cache component. Engineering reports after 2-3 minutes of attempted work that the repair requires the stabilizer unit, no substitute available aboard Halcyon Drift or Artemis. If captain still refuses to depart, timer runs out at T+30 (Engineer aboard) or T+15 (Engineer aboard Artemis but ship not departed); DAMCON team is lost. Halcyon Drift is also unrecoverable without the part. Total mission failure on this path.

The captain's secondary decision: torpedo conversion for speed. Captain may call for Weapons to convert torpedoes to energy to accelerate the cache run. Each torpedo converted yields fuel for higher sustained warp speeds, at the cost of weapons reserves for the return trip. This produces Paths B and D (speed variants) versus Paths A and C (efficient variants).

GM tracks captain's decisions in qualification observations. Both decisions should be clear and verbalized — captain who hedges or fails to commit gets noted at debrief.

**Station beats:**
- Captain: commits to engineer placement, commits to torpedo conversion or not, manages chain of command
- Engineering: if leaving Halcyon Drift, returns to console; if staying, continues mitigation work and reports periodically via Comms
- Weapons: executes torpedo-to-energy conversion if ordered (multiple conversions may be ordered)
- Helm: prepares departure course to Khovan Reach
- Comms: relays captain's decisions to Engineering and to Halcyon Drift; continues DAMCON status reports
- Science: scans cache approach vector, predicts arrival time

#### Scene 11: The Sprint or Run to Khovan Reach (~8-10 min)

**Setting:** Artemis transiting to Khovan Reach. Halcyon Drift behind, in degraded comms range.

**Play:** Helm engages warp at the captain's authorized speed. Engineering manages power. If torpedoes were converted, energy reserves are higher and sustained speed is faster; coolant consumption is higher and heat dissipation matters.

During the transit, DAMCON status reports come through Comms at scheduled intervals. The format gives players the timer naturally:

- T+3 minutes: "Reyes here. Pressure at 60%. Suit O2 at 27 minutes. Sealing bulkhead progressing slowly."
- T+6 minutes: "Park here. Pressure at 45%. Suit O2 at 24 minutes. Seal partial; secondary leak."
- (And so on at 3-minute intervals in the extended scenario; 90-second intervals in the compressed scenario.)

The reports surface the timer in fiction — no UI clock, just the team reporting their oxygen budget. Players hear urgency through Comms.

**The pirate-under-salvage-cover arrival approaches.** Runtime schedules the pirate arrival timer from the cascade event. Approximately 20 minutes after the cascade, two unknown vessels are detected by Science approaching Halcyon Drift. They are at significant range from Artemis's current position (Artemis is at Khovan Reach or near it). Science reports the contacts to Captain via Comms.

GM runs the salvage-cover arrival sequence — see Scene 12 below — at this trigger. Player-facing traffic may still call the contacts salvagers until exposure.

**Station beats during transit:**
- Helm: sustained warp management
- Engineering: power and heat management during sprint; if aboard Halcyon Drift, this is mitigation work and limited bridge contribution
- Weapons: monitors threats, manages torpedo reserves if not depleted
- Science: detects the scheduled pirate-under-salvage-cover arrival; classifies them as standby contacts
- Comms: relays DAMCON status reports, transmits to the claimed salvagers when prompted
- Captain: situational awareness across Artemis and Halcyon Drift

#### Scene 12: The "Salvager" Arrival and the Comms Deception Detection (~10 min)

This is the scene with the most novel design and the most variability. Read carefully.

**Setting:** Two unknown vessels arrive at Halcyon Drift. They identify as independent salvage operators. They are pirates.

**Pirate captain design requirements (governs all dialogue authoring in Pass 2):**

- They present first as salvage operators investigating the distress signal
- They claim some right to secure the scene; their legal posture is wrong because Halcyon Drift is crewed and requesting aid
- They evade credential requests or provide incomplete/incorrect credentials
- Their behavior mismatches at least one claimed cultural norm
- They request docking; if denied and not otherwise exposed, they escalate to unauthorized approach or attack
- Once exposed, they become a combat threat capable of damaging Halcyon Drift and harming Engineering if aboard
- Motive is clean opportunism — no syndicate, no campaign tie, no larger conspiracy

**The vessels (placeholders — finalize species from Cosmos canonical roster in Pass 2):**

- Vessel One: *Cordial Reach*, claiming Skaraani registry. Skaraani cultural style: mercantile, direct, transactional, procedurally precise about credentials when legitimate.
- Vessel Two: *Bright Reckoning*, claiming Torgoth registry. Torgoth cultural style: formal honor protocols, deferential to recognized authority, dislike being rushed.

**Pirate scene state variables (drives MAST scripting in Pass 3 and dialogue branching in Pass 2):**

Track these flags as the scene unfolds. Pass 2 dialogue will branch on them; Pass 3 MAST will instantiate them.

- `pirate_cover_status`: `intact` / `suspected` / `exposed`
- `credentials_requested`: yes/no
- `credentials_provided`: none / partial / evasive / refused
- `legal_posture_challenged`: yes/no
- `cultural_mismatch_observed`: yes/no
- `science_scan_completed`: yes/no
- `science_scan_result`: clean / suspicious (weapons signatures, boarding gear, transponder inconsistency)
- `docking_requested`: yes/no
- `docking_denied`: yes/no
- `unauthorized_docking_attempt`: yes/no
- `combat_active`: yes/no
- `pirate_outcome`: pending / fled / surrendered / destroyed / boarded / escaped_with_cargo

The `pirate_cover_status` flag is the primary state. `intact` is the opening state; the pirates are presenting as salvagers. Any qualifying deception cue (Comms probing that surfaces a tell, Science scan returning suspicious results, captain explicitly questioning the cover) advances to `suspected`. Either a second cue, or any escalation event (denied docking, unauthorized approach, weapons activation), advances to `exposed`. Combat may begin at `suspected` if captain authorizes preemptively, or at `exposed` once the pirates commit.

**Two paths to the reveal — Comms determines which one happens.**

**Path 1: Comms detects the deception through good hailing work.**

When Comms hails the claimed salvagers, the Comms player has the opportunity to ask probing questions that the deception cannot fully cover. Three specific things Comms can probe:

1. **Registry verification.** Comms can ask the salvager captains to transmit their salvage operator credentials and current operating zone permits. Legitimate salvagers have these; pirates don't. If Comms asks, the salvager response is evasive: "We'll transmit credentials at the appropriate time, after we've secured the wreck." (Wreck. Not vessel in distress. This is a tell.)

2. **Legal posture verification.** Comms can directly cite rescue law — "Halcyon Drift is a crewed vessel in distress. Salvage rights do not apply. You are required to render aid and stand down on any claim." Legitimate salvagers would acknowledge this and either depart or offer to assist. Pirates equivocate or assert "operational discretion." If they push back on the legal point, that's a tell.

3. **Cultural protocol mismatch.** A skilled Comms officer reads the cultural cues. Skaraani salvagers would be aggressive about their cut but procedurally precise about credentials. Torgoth salvagers would be deferential to TSN authority. If the Skaraani are evasive on credentials, that's wrong. If the Torgoth are dismissive of TSN authority, that's wrong. The cultural inconsistencies are the deepest tell.

Any single strong tell advances `pirate_cover_status` to `suspected`. A second tell, or Science scan corroboration, advances to `exposed`. Comms reports to Captain. Captain has time to authorize Weapons readiness and engagement posture before the pirates strike.

**Path 2: The pirates reveal themselves through escalation.**

If Comms doesn't probe effectively, the pirates close on Halcyon Drift and request docking authorization. The captain (or Engineering if aboard Halcyon Drift) denies docking authorization. The pirates initially comply — they hold position outside Halcyon Drift's approach envelope. After 2-3 minutes of denial, they attempt to bypass authorization and dock anyway. At this point, Hessler reports unauthorized docking attempt over Comms, `unauthorized_docking_attempt` advances to yes, and `pirate_cover_status` advances directly to `exposed`. The pirates' true nature is now obvious.

This path costs the crew time and gives the pirates an initial positional advantage. If Engineering is aboard Halcyon Drift, Engineering is now in direct danger.

**The combat scenario (either path):**

Once the deception is revealed, the pirates engage. Two vessels, light-to-moderate armament — designed to overwhelm an isolated civilian ship, not a TSN cruiser. Against Artemis they're a real threat but not a campaign-ending one.

If Artemis is still en route from Khovan Reach when the engagement begins, the captain must decide:
- Continue sprint to Khovan Reach (DAMCON timer continues; pirates have free engagement at Halcyon Drift; Engineering at risk if aboard)
- Reverse course to engage pirates (DAMCON timer continues; cache run delayed)

If Artemis has already retrieved the cache component and is returning, the engagement happens at Halcyon Drift on arrival.

Combat is standard SBS engagement. The qualification beats:
- Science classifies the pirates and surfaces weapons profiles
- Weapons engages with subsystem targeting; torpedo reserves are real if conversions happened
- Helm maneuvers for firing arcs while protecting Halcyon Drift
- Engineering balances combat power, manages heat
- Comms broadcasts surrender demand to pirates (combat can end via surrender if they're sufficiently damaged)
- Captain commands engagement, including potential surrender acceptance

**Station beats:**
- Comms: deception detection through registry, legal, and cultural probing; combat communications if engagement begins
- Science: scans the claimed salvagers; suspicious signatures reveal weapons inconsistent with civilian salvage; combat targeting data
- Weapons: combat engagement; subsystem targeting; reserves management
- Helm: combat maneuvering, protecting Halcyon Drift
- Engineering: combat power balance; if aboard Halcyon Drift, position holding under threat
- Captain: force authorization timing, engagement command, surrender acceptance judgment

#### Scene 13: Cache Retrieval at Khovan Reach (~5 min)

**Setting:** Artemis at the Khovan Reach scientific cache. The cache is a TSN-administered storage facility, automated, no personnel on station.

**Play:** Comms hails the cache's automated dock control, transmits Artemis ID and request codes. Cache opens external access. Artemis docks.

The cache inventory includes multiple components. Science consults the inventory and must identify the correct one — the quantum field stabilizer rated for civilian power systems matching Halcyon Drift's reactor class.

Inventory options (GM prepares a list, displayed to Science):
- Quantum field stabilizer, military-grade (incorrect — too high rating, may damage civilian reactor)
- Quantum field stabilizer, civilian-grade (correct — matches Halcyon Drift specifications)
- Quantum field regulator, civilian-grade (incorrect — different component class, similar name)
- Several other unrelated components (sensor arrays, hull patches, etc.)

Science's check: identify the correct stabilizer (civilian-grade, correct class) from the inventory. If Engineering relayed enough detail in the convergence reveal (Scene 9, Beat 3), Science has the specifications needed. If Engineering's relay was vague or incomplete, Science is working from partial information and the risk of selecting wrong is real.

**First attempt:** Science selects a component. If correct, retrieval proceeds; Artemis departs. If incorrect, the error is not detected at the cache — it only surfaces when Engineering attempts installation at Halcyon Drift. Helm must return to the cache for a second attempt. Significant time cost (additional 15-20 minutes round trip) which compresses the DAMCON timer further.

**Recoverable failure note:** If Science picks wrong, the qualification card captures this. The mission continues. The recovery is the consequence — but the recovery is built into the design. No campaign-ending failure here.

**Station beats:**
- Science: component identification, qualification check
- Comms: cache access protocols, retrieval coordination
- Engineering (if aboard Artemis): can review Science's selection and may catch errors before retrieval — this is a Science/Engineering cross-check, optional but valuable
- Helm: docking and departure from the cache
- Captain: authorizes retrieval, manages timing pressure

#### Scene 14: Return and Rescue Resolution (~10 min)

**Setting:** Artemis returns to Halcyon Drift with the cache component (correct or incorrect).

**Play:** Several variables resolve in this scene:

**DAMCON team status:**
Based on the suit O2 timer state, the DAMCON team's outcome is determined:
- Extended timer, returned before T+10: full survival, no medical complications
- Extended timer, T+10 to before T+30: hypoxic but alive, full survival with medical recovery
- Extended timer, T+30 or later: total team loss
- Compressed timer, returned before T+5: full survival, no medical complications
- Compressed timer, T+5 to before T+15: hypoxic but alive, full survival with medical recovery
- Compressed timer, T+15 or later: total team loss

GM reports the outcome through Comms as Artemis arrives. If the team is alive, Hessler reports they've maintained suit integrity. If the team is hypoxic, medical attention is needed immediately. If the team is lost, Hessler reports the loss with appropriate gravity.

**Pirate status:**
If pirates were engaged and defeated, they have either fled, surrendered, or been destroyed. If they were defeated by surrender, the captain has captured vessels and personnel; this becomes a Command report at debrief. If destroyed, the wreckage is in space and Command will recover what they can.

If pirates were not yet engaged (Artemis returned before they could attack), they may attempt to flee on Artemis's arrival. Captain decides whether to pursue or let them go (pursuit costs more time, but capturing the pirates is a meaningful outcome).

**Halcyon Drift repair:**
If the correct component was retrieved, Engineering completes the repair — either still aboard if they stayed, or re-deploys with the component if they returned to Artemis. Halcyon Drift's reactor comes back online. Hessler thanks the crew profusely.

If the incorrect component was retrieved on first attempt and the recovery run was made, the repair completes (with the recovered correct component). If the correct component was never retrieved due to refusal, Halcyon Drift cannot be repaired — Hessler and his surviving crew can be evacuated to Artemis for return to TSN territory. This is the worst-case outcome short of total mission failure.

**Station beats:**
- Engineering: repair completion (or evacuation coordination if repair fails)
- Helm: station-keeping during transfer; return course preparation
- Comms: status reports to Command, coordination with Hessler
- Science: post-engagement scan of pirates (if relevant) and Halcyon Drift
- Weapons: standby; reserves report
- Captain: closes the operation, transitions to return transit

#### Scene 15: Return Transit and Debrief (~5 min)

**Setting:** Artemis on return course toward Tarsis (or directly to Kestrel Yards depending on damage state).

**Play:** Helm sets return course. Energy management for the return trip — if torpedoes were heavily converted, reserves may be lean. Engineering manages.

GM plays Dillon Clip 10 (Debrief Opening). Dillon initiates the qualification framework review.

Each station receives their qualification dimensions and result. Order: Captain, Helm, Weapons, Engineering, Science, Comms. Each player hears what was being measured and how they did.

If DAMCON casualties occurred, GM plays Dillon Clip 11 (DAMCON Replenishment) — Reyes, Park, and Achebe are named, the loss is acknowledged, replenishment will occur at next docking.

Overall mission result and Command-level observations follow. GM plays Anderson Clip 2 (Status Acknowledgment) if appropriate — brief, professional, notes the outcome without editorializing.

Open floor for crew questions. GM plays Dillon Clip 12 (Debrief Closing). Crew dismissed.

End of session.

**Station beats:**
- All: receive qualification feedback
- Captain: optional Command report observations

---

## 4. CRITICAL TIMING NOTES

These are the trigger relationships GM must track:

**Cascade timer (Scene 9, Beat 5):** Starts at the cascade event during Engineering's away mission. Two configurations based on Captain's decision in Scene 10:
- Engineer aboard Halcyon Drift: 30-minute window
- Engineer aboard Artemis: 15-minute window

**Pirate-under-salvage-cover arrival timer:** Starts at the cascade event. Fixed at approximately 20 minutes. The claimed salvagers arrive at Halcyon Drift regardless of Artemis's location or speed.

**Cache transit time:** Helm-dependent. At standard cruise, approximately 25 minutes round trip from Halcyon Drift. With torpedo conversions, can be reduced to approximately 15 minutes. This is the binding variable on the cascade timer outcome.

**The interaction:** Captain choosing Engineer-stays plus efficient cruise puts Artemis returning at approximately T+25, with the DAMCON team in the extended timer's deep critical hypoxic band but not automatically dead. Captain choosing Engineer-stays plus torpedo conversion puts return at T+15, inside the extended hypoxic-survival band. Captain choosing Engineer-returns plus efficient cruise puts return at approximately T+25 — beyond the compressed timer and therefore too late for the DAMCON team. Captain choosing Engineer-returns plus torpedo conversion puts return near T+15 — exactly at the compressed loss edge, a race condition that should be treated strictly by elapsed runtime.

GM should track these timers loosely — exact-minute tracking is too tight for tabletop play. Round to nearest 3-minute interval and announce DAMCON status accordingly.

---

## 5. OFFRAMP HANDLING

Several decision points produce non-standard paths. Brief notes for the GM:

**Captain refuses to deviate to distress signal:** Anderson reissues orders more firmly. If still refused, mission continues to Khovan Reach (cache untouched), Halcyon Drift lost. Debrief notes serious judgment failure.

**Captain refuses to depart for cache (brick wall):** Engineering confirms repair impossible without the component after 2-3 minutes. If captain still refuses, DAMCON team dies; Halcyon Drift cannot be repaired; mission fails operationally. Debrief notes failure to act on available information.

**Crew destroys their own ship through combat error or carelessness:** MAST state-save reload. Crew returns to the last drill checkpoint with prior qualifications preserved. Mission resumes from that point. No campaign penalty.

**Pirates never revealed (Comms misses everything, captain refuses to authorize engagement):** Pirates attack Halcyon Drift, kill remaining crew, depart with cargo before Artemis can intervene. Massive operational failure. Debrief notes the cascading judgment failures.

These paths exist for completeness. Most crews will not hit them. Document them in case.

---

## PASS 1 DESIGN DECISIONS

Decisions made during Pass 1 that weren't fully locked in the outline. Review and push back if any don't match design intent.

**1. Initial ship state at scenario start (v2.3 Slice 04 implementation finding).** Artemis starts with visible ship energy = 0, a temporary generator-output governor, and no loaded ordnance. Kestrel holds two homing torpedoes as emergency reserve and loads them only after Comms requests the reserve. The crew completes Kestrel departure, receives the Kestrel advisory ten seconds after launch-envelope exit, and resolves the issue through Tarsis generator acceptance, energy restoration, governor clear, and resupply.

**2. Anderson's order phrasing.** I framed it as "investigate the fragmentary distress signal" with the Khovan Reach scientific cache mentioned only as regional context, not as a fetch target. The cache becomes operationally relevant when Engineering surfaces the convergence in Scene 9.

**3. Hessler's request specifies an engineering team.** This steers the captain toward the default decision (deploy Engineering) rather than requiring explicit captain reasoning. New captains follow the obvious path; the qualification observation captures whether they did so cleanly.

**4. Two routes to pirate deception detection.** Comms-probing in early hailing (the "skillful play" path) versus escalation through denied docking (the "default play" path). Both work; one rewards proficiency, the other is the backstop.

**5. Skaraani and Torgoth as placeholder species.** Cultural cues specified: Skaraani direct/mercantile, Torgoth formal/honor-coded. These are placeholder names from the Cosmos canonical roster; if you want different species, swap in Pass 2.

**6. Cache inventory presented as a list with foils.** Science must distinguish quantum field stabilizer (civilian-grade) from similar-named foils. This makes the Science qualification check substantive rather than trivial.

**7. Cache transit time of approximately 25 minutes round trip at standard cruise, ~15 with torpedo conversion.** These numbers can be tuned in MAST scripting; they're calibration targets for the timer math to work out.

**8. Brick wall mechanics.** If captain refuses to depart for the cache, Engineering reports infeasibility after 2-3 minutes of attempted work. This gives the captain a fair chance to course-correct before timer expiration.

**9. Pirate combat is light-to-moderate.** Two vessels, designed to threaten Halcyon Drift, not designed to overwhelm Artemis. New crews can handle it; experienced crews handle it easily.

**10. Mission can fail in the brick wall path or the offramp paths.** State-save reload covers ship destruction. It does not cover refusal-to-act paths. Those are recorded as command failures in debrief.

---

## END OF PASS 1 v2.2

This document is now an active scenario-core source, not a draft awaiting Pass 2/Pass 3 generation. Use the companion v2.2 implementation, GM, qualification, debrief, DAMCON, and testing documents as the active handoff set.
