# KHOVAN REACH — QUALIFICATION CARDS v2.2

*Final per-station qualification cards. GM-only — players never see these during play. Surfaced at debrief by Dillon. v2.2 keeps the Act I shakedown fork scoring rule and applies cleanup/source-hygiene updates.*

---

## ABOUT THESE CARDS

The cards capture what's being observed at each station during the mission. Each card has 4-6 observation items, each tied to a specific scene or decision point. Results are recorded as:

- **PASS** — demonstrated cleanly
- **PARTIAL** — demonstrated with errors or under prompting
- **NEEDS RETEST** — not demonstrated, or demonstrated incorrectly without correction

The cards are not a checklist players work down. They're the GM's observational framework, surfaced at debrief in Dillon's tone. Players hear what was being measured *after* the mission, not before.

A "NEEDS RETEST" result on any single item is not a mission failure. It's a development note. The qualification framework is no-fail — even a station with multiple NEEDS RETEST items completes the qualification cruise. The retests are scheduled separately.



### Act I shakedown fork scoring note

Act I may run in three profiles:

```text
Full Shakedown Cruise
Compressed Shakedown Cruise
Direct Scenario
```

Scoring rule:

- **Full Shakedown:** all Act I training observations are available.
- **Compressed Shakedown:** score the core gates actually run; skipped Engineering/DAMCON practice items are N/A or development-only.
- **Direct Scenario:** Act I drill observations are N/A / not observed by captain election. They are not NEEDS RETEST. Later live-operation performance carries more weight.

Do not punish the crew for choosing Direct Scenario. The captain's choice is an operational profile choice, not a refusal to train.

The expanded Full Shakedown adds these observable training behaviors:

- Comms requests Kestrel departure clearance.
- Comms requests Tarsis homing torpedo production priority.
- Comms requests Tarsis generator acceptance/support.
- Comms requests Tarsis docking clearance.
- Engineering demonstrates power/no-motion validation.
- Engineering routes DAMCON teams through rest-cycle and meal-cycle confirmations where available.
- Engineering performs controlled overload and repair supervision.
- Engineering sets a navigation priority preset.
- Science scans Drone 01 and relays weak shield frequencies.
- Weapons locks beams, uses manual targeting, and disables the Weapons array under authorization.
- Helm holds 1-2 km range and stationary geometry for the firing window.
- Captain gates authorization and calls ceasefire.


### Act I guided/unguided scoring note

Drill Two is an instructional sequence. Because Dillon or Training Control walks the crew through each step, minor hesitation during Drill Two should usually be scored as development context, not a hard failure. A station earns concern in Drill Two only if it cannot complete the prompted action, violates a safety/fire-control boundary, or repeats an error after correction.

Drill Three is the independent repeat. Give it more qualification weight. If a station performed correctly in Drill Two only because it was prompted, but fails to initiate or coordinate the same function in Drill Three, mark the Drill Three item PARTIAL or NEEDS RETEST as appropriate.

---

## CAPTAIN

### Observation items

**1. Act I fire-control sequence: guided then independent (Scenes 3-4)**

Did the Captain learn the guided fire-control sequence in Drill Two, then independently run the same pattern in Drill Three?

- PASS: In Drill Two, Captain separated intercept posture from fire authorization, declared Weapons subsystem objective, and called ceasefire. In Drill Three, Captain independently declared Engine objective, authorized live fire at the right time, and called ceasefire after Engine disable.
- PARTIAL: Captain executed the guided Drill Two sequence but required reminder/nudge in Drill Three, delayed objective declaration, or called ceasefire late without destroying the drone.
- NEEDS RETEST: Captain failed to control fire authorization, allowed weapons fire before authorization, did not declare subsystem objective, or could not independently run Drill Three without significant instructor correction.

**2. Investigation deviation decision (Scene 7)**

Did the captain decisively authorize deviation to the distress signal when Science reported it? Looking for: clear command, no extended hedging, no waiting for Dillon's input.

- PASS: Captain ordered course change within ~30 seconds of Science's report
- PARTIAL: Captain hesitated noticeably or asked Dillon for guidance before committing
- NEEDS RETEST: Captain refused to deviate, or required Anderson to reissue orders

**3. Convergence recognition (Scene 10)**

When Engineering reported that the Khovan Reach cache held the component needed to repair Halcyon Drift, did the captain recognize the implications immediately and begin formulating the decision?

- PASS: Captain understood the convergence on first relay and began allocating resources
- PARTIAL: Captain required clarification or asked Engineering to repeat the assessment
- NEEDS RETEST: Captain did not understand the convergence; bridge had to walk them through it

**4. Engineer placement decision (Scene 11)**

Did the captain make a clear, committed decision on whether to leave Engineering aboard Halcyon Drift or recall them for the fetch run?

- PASS: Clear decision, verbalized, executed without revisiting under pressure
- PARTIAL: Decision made but the captain visibly oscillated or revisited under stress
- NEEDS RETEST: No clear decision; bridge crew had to operate on inferred intent

**5. Torpedo conversion decision (Scene 11)**

Did the captain make a clear call on whether to convert torpedoes to energy for the sprint to Khovan Reach? Both yes and no are correct answers — the qualification is about the decisiveness, not the choice.

- PASS: Clear decision, verbalized to Weapons and Engineering, executed cleanly
- PARTIAL: Decision made but coordination with Weapons or Engineering was unclear
- NEEDS RETEST: No decision made; defaulted to standard cruise without acknowledging the option

**6. Salvager handling (Scene 12)**

Did the captain effectively coordinate the pirate/salvage-cover situation — delegating to Comms appropriately, authorizing Weapons readiness at the right time, making the force-authorization call when the pirates exposed themselves?

- PASS: Coordinated cleanly; force authorized at appropriate moment (after exposure or strong suspicion)
- PARTIAL: Force authorization too early (fired on apparent civilians) or too late (Halcyon Drift damaged or DAMCON team at greater risk)
- NEEDS RETEST: No effective coordination; pirate/salvage-cover situation resolved by other stations or by GM intervention

### Debrief framing for Captain

When delivering this debrief, Dillon's tone is procedural. Read the items and results cleanly. Do not editorialize about which decision the captain made (engineer-stays vs engineer-returns) — the qualification is about decisiveness, not strategy.

If the captain's path resulted in DAMCON casualties, note this *after* the qualification items, framed as operational context: "Your decisions on engineer placement and torpedo conversion produced a compressed timer scenario. The DAMCON team was lost. This outcome reflects the choices you made under available information. Future training will revisit the resource-allocation tradeoffs."

---

## HELM

### Observation items

**1. Departure and approach (Scene 1, Scene 2)**

Did Helm execute the Kestrel Yards departure cleanly, and dock at Tarsis Station within tolerance on first attempt?

- PASS: Both executed cleanly without retry
- PARTIAL: Tarsis docking required a retry (Drill One was paused and resumed)
- NEEDS RETEST: Multiple retries required, or Dillon had to intervene with corrections

**2. Contact geometry: guided passive target, then independent evasive target (Scenes 3-4)**

Did Helm establish safe firing geometry when prompted in Drill Two, then maintain arc and range independently against Drill Three's evasion?

- PASS: Established safe range/arc in Drill Two; in Drill Three, preserved a usable firing solution against evasion without prompting.
- PARTIAL: Completed the guided Drill Two geometry check but required prompting or lost arc/range briefly during Drill Three.
- NEEDS RETEST: Could not establish Drill Two geometry even with prompt, repeatedly lost Drill Three geometry, crowded the target, or required GM/Dillon intervention.

**3. Long-range transit (Scenes 6, 7, 11)**

Did Helm manage warp engagement and sustained transit speed appropriately for the Khovan Reach run, balancing speed against energy consumption?

- PASS: Sustained appropriate warp without exhausting reserves; speed adjusted appropriately when ordered
- PARTIAL: Required Engineering input on speed/energy tradeoffs
- NEEDS RETEST: Burned through reserves inappropriately or moved at inefficient speeds

**4. Station-keeping during away mission (Scenes 9-12)**

Did Helm hold station alongside Halcyon Drift during the away mission and through the rescue, including during pirate/salvage-cover arrival?

- PASS: Maintained station-keeping throughout; adjusted as needed for transfer and salvager threat
- PARTIAL: Drift occurred; required prompting to correct
- NEEDS RETEST: Did not maintain station; required active GM intervention

**5. Return transit (Scene 15)**

Did Helm execute return transit with appropriate energy budget given mission's torpedo expenditure and remaining reserves?

- PASS: Return executed cleanly
- PARTIAL: Required Engineering input on route or speed
- NEEDS RETEST: Did not coordinate energy budget; trip required adjustment

### Debrief framing for Helm

If the crew burned torpedoes for the sprint, Helm's transit performance is the variable that determined whether the sprint produced the intended timing benefit. Note this connection in debrief — the captain's call to convert torpedoes only pays off if Helm exploits the additional energy effectively.

---

## WEAPONS

### Observation items

**1. Weapons hold during docking (Scene 2)**

Did Weapons maintain weapons-hold discipline during the Tarsis docking — no targeting, no beam charging, no torpedo arming?

- PASS: Discipline maintained throughout
- PARTIAL: Targeting or charging activity occurred but was caught and stopped
- NEEDS RETEST: Weapons activity occurred in violation of docking protocol

**2. Guided Drill Two Weapons-subsystem disable (Scene 3)**

Did Weapons complete the guided sequence: target selection, beam tuning, manual Weapons subsystem selection, fire only after authorization, Weapons subsystem disabled, ceasefire?

- PASS: Completed each prompted step cleanly; no fire before authorization; disabled Weapons subsystem; ceased fire when ordered or when objective was met.
- PARTIAL: Required prompting on tuning, manual subsystem target, or ceasefire but achieved the objective without destroying the drone.
- NEEDS RETEST: Fired before authorization, failed to select the Weapons subsystem after correction, destroyed the drone before subsystem-disable confirmation, or did not cease fire.

**3. Unguided Drill Three Engine-subsystem disable (Scene 4)**

Did Weapons independently repeat the process under simple evasion and live fire, with Engine disable as the objective?

- PASS: Acquired target, tuned beams, selected Engines, engaged under authorization, disabled Engines, and ceased fire without needing step prompts.
- PARTIAL: Achieved Engine disable but required a nudge, had tuning/subtargeting delays, or ceased fire late without destroying the drone before objective completion.
- NEEDS RETEST: Did not use manual subsystem targeting, targeted the wrong subsystem after correction, fired before authorization in a serious way, destroyed the drone before Engine-disable confirmation, or failed to engage when authorized.

**4. Torpedo conversion (Scene 11)**

When the captain ordered torpedo conversion for energy, did Weapons execute cleanly and coordinate with Engineering on energy budget?

- PASS: Conversion executed without error; coordination clear
- PARTIAL: Conversion executed but coordination with Engineering was unclear
- NEEDS RETEST: Conversion not executed correctly, or executed without captain's authorization
- N/A: Captain did not order conversion this run

**5. Salvager-phase weapons readiness (Scene 12)**

Did Weapons maintain appropriate threat readiness during the pirate/salvage-cover presence — weapons hot when authorized, fire discipline until exposure was confirmed, decisive engagement once authorized?

- PASS: Readiness appropriate to scene state throughout; clean engagement when authorized
- PARTIAL: Readiness lagged the scene state at some point, or engagement was uncoordinated
- NEEDS RETEST: Fired before pirate exposure was confirmed, or failed to engage when authorized

**6. Combat engagement (Scene 12, if combat occurred)**

Did Weapons engage the pirates effectively using subsystem targeting and beam frequency tuning, working with Science on shield data?

- PASS: Effective engagement using full SBS coordination
- PARTIAL: Engaged but did not coordinate effectively with Science
- NEEDS RETEST: Engagement was uncoordinated or did not use available tactical advantages
- N/A: Combat did not occur this run

### Debrief framing for Weapons

If torpedo conversion occurred, note the reserves state at mission end and any operational implications. If combat occurred, note the engagement quality. If neither happened, the Weapons qualification is primarily from the drills and the readiness posture during the salvager scene.

---

## ENGINEERING

### Observation items

**1. Power management during docking (Scene 2)**

Did Engineering manage power state appropriately during Tarsis docking — shields dropped, impulse reduced, reserves protected?

- PASS: Power state managed cleanly
- PARTIAL: Required prompting or correction
- NEEDS RETEST: Power state was not managed; required Dillon intervention

**2. Weapons-power support: guided boost, then independent support (Scenes 3-4)**

Did Engineering perform the guided weapons boost/heat check in Drill Two, then independently support Drill Three live fire with appropriate power and heat/coolant management?

- PASS: Boosted weapons power or overpowered as required in Drill Two; reported heat/coolant stable; in Drill Three, anticipated or responded to the live-fire power need without step-by-step prompting; returned systems to nominal after ceasefire.
- PARTIAL: Completed Drill Two under prompt but was late, unclear, or prompted again during Drill Three; power/heat remained within safe bounds.
- NEEDS RETEST: Did not support the weapons-power requirement, allowed heat/coolant to become unsafe, or left systems overcommitted after ceasefire.

**3. Long-range transit power (Scenes 6, 11)**

Did Engineering manage power for sustained transit, including the sprint to Khovan Reach (if torpedo conversion occurred)?

- PASS: Sustained transit power managed without reserve exhaustion
- PARTIAL: Required Captain or Helm input on tradeoffs
- NEEDS RETEST: Reserves managed poorly; transit was constrained or risked failure

**4. Away mission diagnosis (Scene 9)**

During the away mission to Halcyon Drift, did Engineering effectively diagnose the regulator failure and identify the convergence — that the Khovan Reach cache component is what's needed for the repair?

- PASS: Diagnosis clean; convergence identified and communicated clearly to the bridge
- PARTIAL: Diagnosis correct but convergence required Hessler's explicit prompting
- NEEDS RETEST: Diagnosis was incorrect or convergence was not identified

**5. Atmospheric mitigation (Scenes 9-14, if Engineer stayed aboard)**

If the captain left Engineering aboard Halcyon Drift, did the Engineer maintain effective atmospheric mitigation work?

- PASS: Mitigation work sustained throughout the away period; DAMCON timer extended as designed
- PARTIAL: Mitigation occurred but was interrupted or imperfect
- NEEDS RETEST: Mitigation was not performed effectively
- N/A: Captain returned Engineer to Artemis; this item not applicable

**6. Repair installation (Scene 14)**

Did Engineering install the cache component cleanly when delivered, completing the Halcyon Drift repair?

- PASS: Installation cleanly executed
- PARTIAL: Installation required additional consultation with Hessler or retries
- NEEDS RETEST: Installation failed or was significantly delayed
- N/A: Halcyon Drift was not repaired (Science cache failure not recovered, or brick wall path)

### Debrief framing for Engineering

Engineering's qualification covers the broadest scope of the cruise — power management, away mission, diagnosis, atmospheric mitigation, installation. A station with several PARTIAL items but PASS on the away mission and installation has demonstrated the core competencies; the partials are development items.

If the Engineer stayed aboard Halcyon Drift during pirate/salvage-cover arrival, note this as additional context — they were in real personal danger and held their position effectively. This is not a separate qualification item but worth acknowledging in debrief.

---

## SCIENCE

**Revision note (operator-ratified 2026-08-16) — band rotation added to items 1 and 2.** The stock Science panel's subsystem-integrity readout is a per-band scan snapshot, not a live feed (measured 2026-08-16; see `docs/04_implementation_setup/60_mast_api_cookbook.md` section 7.3). Item 1 (guided Drill Two) now treats a prompted rotation as a PASS and grades on whether Science corrects a stale report once told. Item 2 (unguided Drill Three) treats unprompted rotation as the pass criterion, since Drill Three carries no step calls. A debrief-framing note was also added below covering both outcomes.

### Observation items

**1. Guided contact classification and subsystem data (Scene 3)**

Did Science complete the guided Drill Two scan/classification check and provide the data needed for Weapons subsystem targeting?

- PASS: Identified the contact as a TSN drill drone, reported relevant frequency/subsystem data, and verified the Weapons subsystem disabled state on a fresh sensor band after the Step 10 prompt.
- PARTIAL: Completed the guided check but required prompting or delayed data delivery, or reported a stale subsystem figure and corrected it once reminded that the band was baffled.
- NEEDS RETEST: Could not identify the contact, did not provide actionable subsystem/frequency data even when prompted, or reported the pre-damage subsystem reading as current and did not correct it when prompted.

> **Note on the sensor-band criterion (added 2026-08-16).** Subsystem integrity is a
> per-band snapshot, not a live feed: re-reading a band that has already been scanned
> returns the earlier figures unchanged, while an unused band re-resolves them. Shield
> levels on the same panel *are* live. Drill Two is guided, so Dillon prompts the
> rotation at Step 10 and being prompted is still a PASS. What separates PASS from
> NEEDS RETEST here is whether Science corrects a stale report once told — not whether
> they knew the technique in advance.

**2. Unguided moving-target data and Engine verification (Scene 4)**

Did Science independently reacquire the evasive Drill Three drone, provide usable data, and verify Engine disable?

- PASS: Reacquired moving target, surfaced frequency/subsystem data without waiting for step prompt, and verified Engine disable at completion — rotating to an unused sensor band unprompted, since Drill Three carries no step calls.
- PARTIAL: Reacquired or reported data late, or required a nudge — including a reminder that the subsystem reading was stale — but ultimately supported the objective.
- NEEDS RETEST: Did not reacquire effectively, did not surface useful Engine targeting data, or reported stale subsystem figures as current through to the end of the drill.

> **Why band rotation is the criterion here and not in item 1.** Drill Three removes the
> step calls by design, so this is where a technique demonstrated under prompting has to
> come back unprompted. A Science officer who rotated bands in Drill Two only because
> Dillon said to, and then reads a frozen figure through all of Drill Three, has not
> learned the skill — and the failure is silent, because a stale panel looks exactly like
> a working one.

**3. Distress signal detection (Scene 7)**

Did Science detect the partial distress signal at long range and classify it appropriately (signal type, source vector, vessel class to the extent identifiable)?

- PASS: Detection clean; classification provided with appropriate confidence levels
- PARTIAL: Detection occurred but classification was incomplete
- NEEDS RETEST: Did not detect the signal until close range, or misclassified it

**4. Halcyon Drift damage assessment (Scene 8)**

Did Science scan Halcyon Drift on approach and report damage state, crew status, and threat assessment to the captain?

- PASS: Clean assessment delivered before docking decision
- PARTIAL: Assessment incomplete or required prompting
- NEEDS RETEST: Did not assess; bridge made decisions without scan data

**5. Cache component identification (Scene 13)**

Did Science identify the correct component at the Khovan Reach cache — civilian-grade quantum field stabilizer matching Halcyon Drift specifications?

- PASS: Correct component identified on first attempt
- PARTIAL: First attempt was incorrect; correct component identified on retry
- NEEDS RETEST: Did not correctly identify even on retry, or could not identify at all

**6. Salvager scan (Scene 12)**

When the claimed claimed salvagers arrived, did Science scan them and surface the suspicious indicators (weapons signatures, boarding gear, transponder mismatches)?

- PASS: Scan completed and findings surfaced clearly
- PARTIAL: Scan completed but findings were not communicated effectively
- NEEDS RETEST: No scan completed before pirates exposed themselves

### Debrief framing for Science

The Science qualification has the highest variance because the cache component identification (item 5) is binary — correct or incorrect on first attempt determines the timer compression. A Science officer who identified correctly first time saved meaningful time for the rescue. One who picked wrong put pressure on the DAMCON timer.

Note this dynamic at debrief. The Science qualification is about precision under partial information — the cache inventory contained foils (military-grade stabilizer, civilian regulator, etc.) and the correct selection required attention to the diagnostic detail Engineering relayed.

Sensor-band discipline (items 1 and 2) is worth calling out separately at debrief, because it is the one Science habit that transfers to every engagement rather than to one puzzle. The underlying lesson is that a subsystem reading carries a timestamp: shields are observed continuously from outside a hull, but what is broken *inside* one is intelligence, and you only hold it as of the last time you went and got it. A Science officer who internalizes that stops treating the panel as a feed and starts treating a scan as something spent deliberately — which is the correct model, and the one the engine actually implements.

Be fair about the failure mode when it appears. Reporting a frozen figure is not carelessness; a stale panel is indistinguishable from a working one, and the officer has no cue that anything is wrong. The question at debrief is whether they re-checked before reporting, not whether they were fooled once.

---

## COMMS

### Observation items

**1. Station and Act I training hailing/status relay (Scenes 2-4)**

Did Comms handle Tarsis Station hailing and resupply protocols, complete the guided Drill Two hail/status check, and independently monitor/report Drill Three training status?

- PASS: Tarsis protocols followed cleanly. In Drill Two, hailed Drone 01 and reported drill-mode response when prompted. In Drill Three, monitored or hailed as appropriate and relayed status/disable information without waiting for step calls.
- PARTIAL: Tarsis hailing or resupply needed correction, or Drill Two completed under prompt but Drill Three monitoring/status relay was late, incomplete, or required a nudge.
- NEEDS RETEST: Station protocols were incorrect enough to require Dillon intervention, did not hail/report in Drill Two even when prompted, or failed to provide any useful status relay in Drill Three.

**2. Command reporting cadence (Scenes 5, 7, throughout)**

Did Comms maintain appropriate Command reporting cadence throughout the mission — Anderson updates, status reports, formal acknowledgments?

- PASS: Cadence maintained without prompting
- PARTIAL: Required prompting on occasion
- NEEDS RETEST: Cadence was not maintained; significant gaps in Command communication

**3. Away mission relay (Scenes 9-14)**

Did Comms effectively relay communications between Engineering on Halcyon Drift and the bridge, including DAMCON status reports?

- PASS: Relay clean and accurate; reports delivered to the right stations in good time
- PARTIAL: Relay occurred but with delays or misdirected information
- NEEDS RETEST: Relay was ineffective; bridge missed critical reports

**4. Hessler contact (Scenes 8-14)**

Did Comms establish and maintain effective contact with Hessler aboard Halcyon Drift, supporting the Engineering player and the bridge?

- PASS: Contact maintained cleanly; relevant information passed in both directions
- PARTIAL: Contact established but with gaps in support
- NEEDS RETEST: Contact ineffective; Hessler was effectively isolated from the bridge

**5. Salvager negotiation (Scene 12)**

Did Comms probe the pirates effectively, surfacing one or more deception cues (registry, legal posture, cultural protocol, operational conduct) before the pirates exposed themselves through escalation?

- PASS: One or more deception cues surfaced before escalation; pirates exposed by Comms work
- PARTIAL: Some probing occurred but did not advance pirate cover status; pirates exposed by escalation
- NEEDS RETEST: No effective probing; pirates were ambiguous until they attempted unauthorized docking

**6. Cultural fluency under pressure (Scene 12)**

Did Comms read the cultural cues correctly — recognizing the Skaraani protocol mismatch (Vrenn-Ka evasive on credentials when real Skaraani would be procedurally precise) or the Torgoth deference mismatch (Therrek-Bal pushing back on TSN authority when real Torgoth would defer)?

- PASS: At least one cultural mismatch correctly identified and surfaced
- PARTIAL: Cultural protocols invoked but mismatches not specifically identified
- NEEDS RETEST: Cultural protocols not invoked; deception detected only through other channels

### Debrief framing for Comms

Comms has the most asymmetric qualification — strong play unlocks the deception detection path; weak play falls to the escalation backstop. Note this dynamic clearly. The Comms officer who surfaced even one cultural mismatch did real qualification work.

If the player attempted soft diplomacy with the pirates (cooperating, offering compromises), note this without judgment. It's a Comms style choice that produced a worse outcome in this specific scenario. The lesson is reading the situation — knowing when probing is required versus when cooperation is appropriate.

---

## OVERALL ACT I QUALIFICATION NOTE

The v2.2 Act I drill block observes a forked training profile:

- Full Shakedown: generator-governor response, Tarsis protocol, Engineering systems shakedown, controlled Drone 01 disable, live-fire Drone 02 destroy.
- Compressed Shakedown: essential resupply and controlled-disable gates only.
- Direct Scenario: expedited resupply and bypass of drill observations.

Do not score guided and independent work as equivalent. Prompted/tutorial actions are training exposure. Independent execution later in Act I or during the live mission carries more qualification weight.

## OVERALL MISSION RESULT

After station-by-station debrief, Dillon delivers an overall qualification summary. Three categories:

**Full qualification (most stations PASS, no NEEDS RETEST items):**
> "Khovan Reach is logged as a clean qualification cruise. All six stations qualified for standard operational duty. Retests are not required. Anderson's next assignment will treat you as a qualified crew."

**Qualified with development items (most stations PASS, some PARTIAL items, no critical NEEDS RETEST):**
> "Khovan Reach is logged as a qualified cruise with development items. All six stations are cleared for standard operational duty. Specific PARTIAL items are recorded as developmental and will be revisited in follow-on training."

**Qualified with retests required (one or more NEEDS RETEST items on critical observations):**
> "Khovan Reach is logged as a qualified cruise. The following stations require retest on specific items before standard operational duty: [Dillon names them]. The retest will be scheduled within thirty days. Until completion, the affected stations operate under instructor oversight."

A station with all NEEDS RETEST items has effectively failed the qualification — but this is rare in practice. The no-fail design assumes most stations achieve at least PARTIAL on most items.

---

## A NOTE ON USING THESE CARDS

These cards are dense by design. The GM does not need to track every item explicitly during play — most items are observable in passing, and the GM can fill in the cards from memory or notes after the mission. Real-time tracking would interrupt GM bandwidth.

A reasonable practice: after each scene, jot a single-line note about which stations did notable work. After the mission, work through the cards in 5-10 minutes based on the notes. Then deliver the debrief.

For the first run, this will feel awkward. For the third run, it'll feel natural. The cards are a framework, not a script.

---

## END OF QUALIFICATION CARDS
