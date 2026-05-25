# KHOVAN REACH

*Standalone TSN training scenario for Cosmos Starship Bridge Simulator. Working document — Pass 1 of three. Revision 1.2.*

---

## PASS 1 NOTE

This document is the operational core: mission overview, captain's briefing, and full scene-by-scene play guide. After your review, Pass 2 produces NPC files (Hessler voice-mode, pirate scripted dialogue, DAMCON team reports, Anderson and Dillon clip scripts). Pass 3 produces qualification cards, GM operational notes, MAST scripting documentation, and the debrief script.

A short list of design decisions made during Pass 1 — places where I committed to specifics that weren't fully locked in the outline — appears at the end of this document under "Pass 1 Design Decisions." Review those alongside the main content.

---

## REVISION HISTORY

**Rev 1.2 (current)** — Act I drill block baked in. Changes:
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

The Artemis is dispatched to investigate a fragmentary distress signal in a quiet region near Khovan Reach. They find a damaged civilian cargo hauler, a crew in genuine distress, and — eventually — opportunistic pirates exploiting the situation under the pretense of being salvagers.

The mission tests six bridge stations through coordinated play rather than discrete drill checks. Helm dockings and transits; Weapons subsystem targeting and torpedo management; Engineering power balance, away mission diagnosis, and the personal-stakes decision; Science long-range sensors, threat classification, and component identification; Comms station hailing, multi-relay coordination, cultural-fluency negotiation, and deception detection; Captain investigation authorization, resource allocation, force authorization, and command judgment under pressure.

The tone is lighter than Sigma Protocol — no moral triangle, no hidden conspiracy, no doctrine confession — but the dramatic weight is real. Engineering may be in personal danger. The DAMCON team may die. The pirates are a genuine combat threat. Failures cost lives. The captain's choices have measurable consequences.

### Design Philosophy

**Console play is the default.** Six players, six stations, mission run through the SBS consoles. The only departure from console play is the brief Engineering away mission to Halcyon Drift, where the Engineering player physically leaves their console but stays at the table for an observed GPT-4o conversation with Hessler.

**Voice-mode AI is limited.** One GPT-4o NPC — Hessler. Lightweight, cooperative, no tier gating. Used to expose the team to voice-mode roleplay before they encounter the harder version in Sigma Protocol. All other NPC dialogue (Anderson, Dillon, salvagers, DAMCON team) is delivered through recorded clips or GM voice over Comms console exchanges.

**Qualification is observation, not testing.** Players see no qualification cards during play. Dillon surfaces them at debrief. The mission is played as a real operation; competence is measured by what players actually do, not by checking items off a visible rubric.

**No-fail with real costs.** Catastrophic failures (ship destruction) trigger a MAST state-save reload to the last drill checkpoint with prior qualifications preserved. Non-catastrophic failures (DAMCON casualties, Halcyon Drift loss, weapons depletion) are absorbed into qualification cards and acknowledged at debrief. The team always finishes the mission.

**Reactive, not procedural.** Anderson's orders dispatch Artemis to investigate, not to fetch a known item. The cache run develops in the field, under pressure, after Engineering diagnoses Halcyon Drift's damage. The captain's decisions emerge from discovery, not from a pre-briefed plan.

**Weapons must have a real live-fire role.** The salvager element of Act III is not pure negotiation. The pirates-under-cover design gives Comms a deception-detection beat and then gives Weapons a real combat beat if the situation goes hot. This is intentional balancing — earlier design iterations over-served Comms and left Weapons under-exercised.

### Session Targets

- Total session length: 95-105 minutes
- Act I — Qualification Cruise: ~28-30 minutes
- Act II — Investigation: ~15 minutes
- Act III — Halcyon Drift and Khovan Reach: ~50 minutes
- Debrief: ~10 minutes
- Crew complement: six players (Captain, Helm, Weapons, Engineering, Science, Comms) plus GM

---

## 2. CAPTAIN'S BRIEFING MATERIALS

### Ship State at Mission Start

**TSN Cruiser Artemis** — just out of Kestrel Yards refit cycle.

- Hull: full integrity
- Energy reserves: 70% of standard load
- Torpedoes: 0 homing torpedoes (full slot allocation reserved for resupply at Tarsis)
- No nukes, no EMPs, no mines (reserved for resupply at Tarsis)
- Coolant: full
- DAMCON teams: standard complement (six teams, three personnel each)
- Crew: full bridge complement, all new to this ship together

### Mission Orders (as briefed by Dillon at scenario start)

Routine qualification cruise. Three-leg pattern: depart Kestrel Yards, dock-and-resupply at Tarsis Station, conduct two skill drills in the adjacent operating area, return for debrief. Expected total duration: four standard hours. Dillon embedded as instructor.

Standard rules of engagement: defensive posture, hailing before any escalation, deference to TSN protocol. No live combat is anticipated.

### Anderson Diversion Orders (transmitted during Act II)

Approximately one hour into the qualification cruise, Anderson transmits new orders.

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
- That pirates are inbound under salvager cover

These facts develop during the mission through investigation and Engineering's away-mission diagnosis.

---

## 3. SCENE-BY-SCENE PLAY GUIDE

### ACT I — QUALIFICATION CRUISE (~30 min)

#### Scene 1: Departure and Briefing (~5 min)

**Setting:** Artemis on the launch ramp at Kestrel Yards. Bridge crew at stations. Dillon present, standing slightly behind the Captain's chair.

**Play:** GM plays Dillon Clip 1 (Opening Briefing). The clip welcomes the crew, frames the cruise, references the qualification framework in general terms ("standard operational observation across the cruise") without enumerating specific items.

Captain takes the chair, conducts a verbal readiness check around the bridge. Each station reports console ready. Helm receives departure clearance via Comms hail to Yards Control. Helm engages thrusters and clears the launch envelope.

**GM responsibilities:** Brief atmospheric description of Kestrel Yards departing on Helm's main view. Confirm Dillon Clip 1 plays cleanly. Note initial Captain command rhythm and station readiness verbiage in mental qualification observations.

**Station beats:**
- Captain: opens with verbal readiness check; sets tone
- Helm: executes departure maneuver, sets initial course to Tarsis
- Comms: hails Yards Control for clearance
- Other stations: report ready

#### Scene 2: Drill One — Dock and Resupply (~8 min)

**Setting:** Tarsis Station, standard TSN orbital facility. Artemis approaches on Helm's vector.

**Play:** GM plays Dillon Clip 2 (Drill One Intro) as Artemis enters the station's approach lane. Dillon notes this drill exercises docking discipline, station hailing, and resupply coordination.

The drill itself runs as a coordinated sequence:

1. **Helm** executes docking approach within tolerance. The approach requires reducing speed to maneuvering thrusters, aligning to the docking port heading, holding station within Tarsis's docking envelope.
2. **Comms** hails Tarsis docking control, requests docking clearance, transmits Artemis ID codes.
3. **Engineering** manages power balance during docking. Shields must be dropped; impulse power reduced; reserves held for the resupply transfer.
4. **Captain** coordinates the overall sequence and issues the resupply order.
5. **Weapons** confirms weapons hold during docking proximity (no targeting, no charging beams).
6. **Science** monitors station environment, confirms no anomalies.

If any station makes a significant procedural error — Helm misjudges the approach, Comms uses incorrect hailing protocols, Engineering fails to drop shields, Weapons charges beams in proximity — Dillon may pause the drill and request a retry. This is the only point in the mission where Dillon overtly intervenes in real-time. Treat it as instructor latitude, used sparingly.

Once docked, Comms requests resupply of:
- Energy to 100%
- Full torpedo complement: 8 homing, 2 nukes, 2 EMPs, 2 mines

GM scripts the resupply completion. Energy and torpedo stores update. GM plays Dillon Clip 3 (Drill One Complete) as resupply finishes.

Artemis undocks. Helm sets course out of the station's approach lane.

**Station beats:**
- Helm: docking approach within tolerance is the qualification check
- Comms: station hailing protocol correctness, resupply request format
- Engineering: shield/power state during docking
- Captain: sequence coordination, clear orders
- Weapons: weapons-hold discipline during docking
- Science: passive monitoring

#### Scene 3: Drill Two — Guided Contact Handling and Controlled Weapons Disable (~9-11 min)

**Setting:** Open space approximately 20 minutes from Tarsis, in the designated training operating area.

**Instructional frame:** This is the teaching drill. Dillon or Training Control walks the crew through the ship-contact loop step by step. The drill should not feel like a lecture, but it should be explicit: one station beat, one check, then the next station beat.

The drone does not fight back and does not evade. The task pressure comes from procedure and coordination, not threat.

**Drone configuration:** GM spawns Drill Drone 01 at long range.

Drone requirements:

- Initially unidentified to Science at standard sweep.
- Marked as a TSN drill drone after proper scan/classification.
- Holds position.
- Does not evade.
- Does not fire.
- Exposes targetable subsystem: Weapons.
- Survives a normal controlled subsystem-disable pass if the crew does not overfire.

**Play:** GM plays Dillon Clip 4 (Drill Two Intro — Guided Contact Handling). Dillon introduces the drill, states that it will proceed step by step, and gives the hard objective: disable Drone 01's Weapons subsystem and confirm ceasefire.

Dillon or Training Control then proceeds through the following gated steps.

| Step | Prompted station/action | Required check before advancing |
|---|---|---|
| 1 | Science scans and classifies the unknown contact. | Science reports TSN drill drone or equivalent full classification. |
| 2 | Comms hails on standard bands. | Automated drill-mode response received or GM marks hail complete. |
| 3 | Captain authorizes intercept posture, not fire. | Captain gives clear intercept/readiness order and preserves weapons hold. |
| 4 | Helm moves to safe firing geometry. | Drone is in safe range/arc, or GM marks geometry acceptable. |
| 5 | Engineering boosts weapons power to training threshold and reports heat/coolant stable. | Weapons power/overpower observed mechanically, or GM marks Engineering boost complete. |
| 6 | Weapons selects target, tunes beams from Science data, selects manual subsystem target: Weapons. | Target selected, beam tuning set, Weapons subsystem selected, and no fire yet. |
| 7 | Captain authorizes controlled fire on Weapons subsystem only. | Captain gives explicit fire authorization and objective. |
| 8 | Weapons fires until Drone 01's Weapons subsystem is disabled. | Weapons subsystem disabled mechanically, or GM marks disable after direct observation. |
| 9 | Captain orders ceasefire; Weapons stops firing. | Ceasefire confirmed. |
| 10 | Science and Comms verify training status. | Science verifies subsystem state; Comms reports drone status broadcast, or GM marks final verification. |

Dillon's guidance should be short and procedural. Do not explain every console in abstract. Prompt the next action, let the station execute, confirm the check, then continue.

Example prompt language:

- "Science, scan and classify the contact. Report when you have full classification."
- "Comms, hail on standard bands. Report the response."
- "Captain, authorize intercept posture. This is not fire authorization."
- "Helm, establish safe firing geometry. Weapons will need arc, not proximity."
- "Engineering, bring weapons power to training threshold. Report heat and coolant stable."
- "Weapons, select the target, tune beams, and set manual subsystem target to Weapons. Hold fire."
- "Captain, authorize controlled fire when ready. Objective is Weapons subsystem disable only."
- "Weapons, fire to disable Weapons subsystem. Cease fire when objective is met."
- "Science and Comms, verify disabled state."

**Exit criteria:** Drill Two completes only when all required outcomes are true:

- Science classification complete.
- Comms hail/check complete.
- Captain intercept posture order given.
- Helm firing geometry established.
- Engineering weapons boost/check complete.
- Weapons target/tuning/subsystem-selection check complete.
- Captain controlled-fire authorization given.
- Drone 01 Weapons subsystem disabled.
- Ceasefire confirmed.
- Science/Comms final status verification complete.
- Drone 01 not destroyed before subsystem-disable confirmation.

**Failure and retry:** If Weapons fires before Captain authorization, pause the drill, reset to Step 6 or Step 7, and record a development note.

If Drone 01 is destroyed before Weapons subsystem disable is confirmed, reset Drill Two or mark the relevant station items PARTIAL/NEEDS RETEST at GM discretion.

If a station cannot complete a check because the current Cosmos build lacks an observable signal, GM may manually mark the step complete after direct observation. Do not block play on missing instrumentation.

GM plays Dillon Clip 5 (Drill Two Complete) only after the Weapons subsystem is disabled, ceasefire is confirmed, and final verification is complete.

**Station beats:**
- Captain: separates readiness from authorization, declares subsystem objective, calls ceasefire
- Helm: establishes geometry on a passive target
- Weapons: target selection, tuning, manual Weapons subsystem target, controlled fire
- Engineering: weapons boost/overpower and heat/coolant management
- Science: classification, frequency/subsystem data, disable verification
- Comms: hail, automated response, status broadcast relay

#### Scene 4: Drill Three — Unguided Evasive Live-Fire Repeat / Engine Disable (~6-8 min)

**Setting:** Same training area. A second drill drone is deployed for a live-fire repeat under simple evasion.

**Instructional frame:** This is the transfer drill. Dillon gives the objective and constraints, then stops walking the crew through the sequence.

The intended player experience is: "You just learned the loop. Now run it yourselves."

**Drone configuration:** GM spawns Drill Drone 02.

Drone requirements:

- Identifiable as a TSN drill drone after scan.
- Uses simple evasion: slow turn, lateral drift, heading changes, or throttle pulses.
- Engagement is live fire against the drone.
- Optional safe/low-risk return fire only if the build supports it and playtest confirms it is safe.
- Exposes targetable subsystem: Engines.
- Survives a normal controlled engine-disable pass if the crew does not overfire.

**Play:** GM plays Dillon Clip 6 (Drill Three Intro — Now You Do It). Dillon states the objective but does not enumerate the step-by-step sequence again.

Dillon should communicate:

- This is the same contact-handling sequence.
- No step calls this time.
- Drone will evade simply.
- Live fire is authorized after Captain command.
- Exit criterion is Engine subsystem disabled and ceasefire confirmed.

Then the crew proceeds without prompts.

Expected unprompted crew sequence:

1. Science reacquires and classifies Drone 02, including frequency/subsystem data.
2. Comms monitors or hails training broadcast as appropriate.
3. Captain declares the objective: disable Engines.
4. Helm maintains range and arc against simple evasion.
5. Engineering boosts weapons power and manages heat/coolant.
6. Weapons tunes beams, selects Engines, fires under authorization, and disables Engines.
7. Captain/Weapons cease fire.
8. Science/Comms verify Engine disable.

**Exit criteria:** Drill Three completes when:

- Drone 02 Engine subsystem is disabled.
- Ceasefire is confirmed.
- Drone 02 is not destroyed before Engine-disable confirmation.

Process quality is observed for qualification, but Drill Three should not silently fail because the crew skipped a nonessential process flag. If they disable Engines without scanning, hailing, or Engineering boost, the drill can complete while the relevant station items receive PARTIAL or NEEDS RETEST.

**Failure and retry:** If Drone 02 is destroyed before Engine disable is confirmed, Dillon may require one repeat or mark the drill as PARTIAL/NEEDS RETEST depending on severity.

If the crew stalls completely, wait long enough for the lack of initiative to be meaningful. Then Dillon may give one safety-level nudge, not a full walkthrough:

> "Crew, this is a repeat drill. Apply the previous sequence. Objective remains Engine subsystem disable."

Using this nudge should be recorded as a development note for the relevant stations, especially Captain.

GM plays Dillon Clip 7 (Drill Three Complete) once Drone 02's Engine subsystem is disabled and ceasefire is confirmed.

**Station beats:**
- Captain: independently runs the contact-handling sequence and calls ceasefire
- Helm: preserves firing geometry against simple evasion
- Weapons: targets Engines and executes live-fire subsystem disable
- Engineering: supports live fire with power/heat management without being walked through
- Science: provides moving-target data and verifies Engine disable
- Comms: monitors training broadcast and relays status without waiting for prompt

End of Act I. Artemis is at full energy, full torpedo complement, and has demonstrated coordinated competence on standard tasks: docking/resupply, guided contact handling, and independent evasive live-fire subsystem disable.


---

### ACT II — INVESTIGATION (~15 min)

#### Scene 5: New Orders (~3 min)

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

**The salvager arrival approaches.** GM tracks the salvager arrival timer separately. Approximately 20 minutes after the cascade, two unknown vessels are detected by Science approaching Halcyon Drift. They are at significant range from Artemis's current position (Artemis is at Khovan Reach or near it). Science reports the contacts to Captain via Comms.

GM plays the salvager arrival sequence — see Scene 12 below — at this trigger.

**Station beats during transit:**
- Helm: sustained warp management
- Engineering: power and heat management during sprint; if aboard Halcyon Drift, this is mitigation work and limited bridge contribution
- Weapons: monitors threats, manages torpedo reserves if not depleted
- Science: detects salvager arrival at scheduled trigger; classifies them as standby contacts
- Comms: relays DAMCON status reports, transmits to salvagers when prompted
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

When Comms hails the salvagers, the Comms player has the opportunity to ask probing questions that the deception cannot fully cover. Three specific things Comms can probe:

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
- Science: salvager classification (legitimate signature scan would reveal weapons signatures inconsistent with civilian salvage); combat targeting data
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
- Returned before T+10 (any scenario): full survival, no medical complications
- T+10 to T+25 (extended scenario, Engineer aboard Halcyon Drift): hypoxic but alive, full survival with medical recovery
- T+5 to T+10 (compressed scenario, Engineer aboard Artemis): hypoxic but alive, full survival with medical recovery
- Beyond T+25 (extended) or T+10 (compressed): total team loss

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

**Salvager arrival timer:** Starts at the cascade event. Fixed at approximately 20 minutes. Salvagers arrive at Halcyon Drift regardless of Artemis's location or speed.

**Cache transit time:** Helm-dependent. At standard cruise, approximately 25 minutes round trip from Halcyon Drift. With torpedo conversions, can be reduced to approximately 15 minutes. This is the binding variable on the cascade timer outcome.

**The interaction:** Captain choosing Engineer-stays plus efficient cruise puts Artemis returning at approximately T+25, with the DAMCON team in the extended timer's late hypoxic band. Captain choosing Engineer-stays plus torpedo conversion puts return at T+15, fully in survival floor. Captain choosing Engineer-returns plus efficient cruise puts return at T+25 — but the timer is compressed to 15 minutes, so the team is dead. Captain choosing Engineer-returns plus torpedo conversion puts return at T+15 — exactly at the edge of the compressed timer, race condition.

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

**1. Initial ship state at scenario start.** I specified 70% energy, 8 homing torpedoes, no other ordnance. Dock-and-resupply brings to 100% energy and full torpedo complement. This is the "just out of refit" state that justifies Drill One.

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

## END OF PASS 1

Pass 2 produces NPC files: Hessler voice-mode (lightweight, no tier gating), salvager scripted dialogue (deception detection cues and escalation triggers), DAMCON team reports timeline (scheduled comms messages at timer intervals), Anderson clip scripts (full text for 2-3 clips), Dillon clip scripts (full text for 12 clips).

Pass 3 produces qualification cards (final text per station), GM operational notes (failure handling, pacing guidance, common questions), MAST scripting documentation (state save, timers, scripted comms triggers), and the debrief script template.

Approve Pass 1 or flag changes before Pass 2 begins.
