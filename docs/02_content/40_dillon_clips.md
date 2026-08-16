# DILLON CLIP SCRIPTS v2.2

*Full text for the 12 Dillon instructor clips plus v2.2 Act I trigger notes and non-audio Training Control/Kestrel/Tarsis text packets.*

---


# V2.2 ACT I TRIGGER AND TEXT-MESSAGE UPDATE

This file keeps the 12 Dillon recorded clips as the canonical audio set. It adds v2.2 trigger notes and non-audio Training Control / Kestrel / Tarsis text packets for the Act I shakedown fork.

**Revision note (operator-ratified 2026-08-16) — Dillon transmits from Kestrel Yards; he is never aboard Artemis.** Every staging direction below that has him standing on the bridge (Clip 1's "Dillon stands behind the captain's chair," the "physically present on the bridge" characterization, Clip 8's pivot address) is corrected by this note: he is present in voice only, for the whole cruise including the Act II pivot and debrief. See `docs/01_design/00_scenario_play_guide.md` for the full design-canon correction.

## Trigger changes

**v2.2 cleanup note:** Text packets remain script-driven overlay/Comms-archive messages. No re-recording is required for this cleanup pass unless the production team chooses to refresh Dillon audio later.

- **Clip 1** still plays at mission start.
- **Kestrel generator advisory** is not a recorded Dillon clip. It is a text packet displayed in the upper-left lifeform overlay and echoed to the Comms archive ten seconds after Artemis clears the launch envelope.
- **Dillon / Training Control speed-power reminder** is also a text packet, not recorded audio for now.
- **Clip 2** plays only for shakedown profiles that run the Tarsis drill framing. Direct Scenario may skip Clip 2 after expedited resupply if pacing demands.
- **Clip 3** plays after Tarsis resupply and generator-governor clearance.
- **Clips 4-7** fire only if the selected shakedown profile includes Drone 01 / Drone 02 drills.
- **Clip 8** fires after Act II orders as before.

## New Act I text packets

### Kestrel generator advisory

Trigger: ten seconds after launch-envelope exit.

Slice 04 live-clarity wording:

> "Kestrel Yard Control: advisory packet follows. Artemis is operating under a temporary generator governor. Expect constrained startup resources and deliberate speed/power handling until Tarsis completes generator acceptance. Tarsis has the acceptance package and will clear the handoff after docking/resupply."

Emergency reserve response:

> "Kestrel Yard Control: emergency homing reserve approved. Loading two homing torpedoes now. These are reserve margin under the generator governor, not a full combat load. No nukes, EMPs, or mines are released before Tarsis resupply."

### Dillon / Training Control speed-power reminder

Trigger: immediately after Kestrel generator advisory.

> "Training Control note: speed and energy consumption are not linear. The faster you go, the more sharply energy expenditure rises. High speed may solve a timing problem and create an energy problem. Captain and Engineering should keep that tradeoff visible."

Slice 04 live-clarity wording:

> "Training Control: keep speed and power changes deliberate. Treat the governor as active until Tarsis completes the handoff. Comms should coordinate homing priority, generator support, and docking clearance with Tarsis."

### Shakedown fork prompt

Trigger: after speed-power reminder.

> "Training Control has three profiles available. Full shakedown if the crew wants the complete systems pass. Compressed shakedown if you want the essential checks only. Direct scenario if you want to skip drills after expedited Tarsis resupply. Your call, Captain."

### Tarsis homing-priority acknowledgment

> "Tarsis Control: homing production priority set for Artemis. Replacement torpedoes will be prioritized during resupply."

### Tarsis generator-support acknowledgment

> "Tarsis Generator Acceptance: Kestrel package received. We can clear the governor after docking and yard-lock synchronization."

### Tarsis hail / docking-clearance / handoff packets

> "Tarsis Station: Artemis, we read you. Production Control and Generator Acceptance are standing by. Request homing priority, generator support, and docking clearance before approach."

> "Tarsis Docking Control: docking clearance granted. Helm, approach within tolerance and initiate docking."

> "Tarsis Docking Control: docking clearance not granted. Complete Tarsis Comms traffic before approach."

> "Tarsis Control: normal docking resupply and generator handoff confirmed. Full energy and armament restored; governor clear is recorded. Await the next shakedown instruction."

### Direct Scenario bypass confirmation

> "Training Control: shakedown bypass accepted. Act I drill observations will be recorded as not observed by captain election. Live-operation observations remain active. Proceeding to operational scenario."

---


## ABOUT THESE CLIPS

Master Sergeant Dillon's voice (from Sigma Protocol design): calm, procedural, faintly bureaucratic. No emotion. No urgency. He is a specialist following procedure. Brief — short paragraphs, not long monologues.

Khovan Reach uses him differently than Sigma Protocol did. In Sigma, Dillon was the background command-net voice requesting authorization. In Khovan Reach, he is the qualification instructor, stationed at Kestrel Yards and transmitting to Artemis for the entire cruise — present in voice, never in person. He observes more than he speaks. When he speaks, it's deliberate.

Three categories of clips:

1. **Mission framing clips** — opening briefing, pivot acknowledgment
2. **Drill clips** — three pairs (intro + complete) for the three Act I drills
3. **Debrief clips** — opening, conditional DAMCON acknowledgment, closing

Plus one optional observation clip after the distress-signal decision.

Total: 12 clips. About 5-6 minutes of total audio.

---

## CLIP 1: OPENING BRIEFING

**Trigger:** Mission start, as Artemis prepares to leave Kestrel Yards.

**Setup:** Bridge crew at stations. Dillon transmits from Kestrel Yards Control, addressing the bridge over comms.

**Script:**

Slice 04 text stand-in:

> "Dillon: Crew of Artemis, this is a qualification cruise. First task: get the ship out of Kestrel cleanly. Comms, request departure clearance. Helm, hold position until Kestrel releases the yard-lock. Captain, coordinate the sequence."

Recorded-audio source text:

> "Captain. Crew of Artemis.
>
> This is a qualification cruise. Your first cruise together as a crew on this ship. Standard pattern: depart Kestrel, dock and resupply at Tarsis, conduct two skill drills in the adjacent operating area, return for debrief. Expected duration four standard hours.
>
> I'll be observing. Standard observational framework — each station will be evaluated across operational tasks. The framework is internal; you don't need to track it. Run the cruise. Do your jobs. I'll handle the rest.
>
> Rules of engagement: defensive posture, hail before any escalation, standard TSN protocol. No live combat is anticipated.
>
> Captain, the ship is yours."

**Notes on delivery:**

- Pace: measured. Dillon is not in a hurry. He's read this briefing dozens of times.
- The "you don't need to track it" is the key line — it tells the players they don't have to think about qualification cards during play.
- "Captain, the ship is yours" is the hand-off. Read it cleanly, not warmly.

**Length:** ~30 seconds.

---

## CLIP 2: DRILL ONE INTRO (Dock and Resupply)

**Trigger:** Helm approaches Tarsis Station on initial approach vector.

**Script:**

> "Drill one. Dock and resupply at Tarsis Station.
>
> Helm: approach within standard tolerance, align to the docking port heading, hold station within the docking envelope. Comms: handle station hailing and resupply protocol. Engineering: manage power state for docking — shields, impulse, reserves. Captain: coordinate.
>
> If anything looks wrong, I may pause for retry. Otherwise, run it clean.
>
> Proceed when ready."

**Notes on delivery:**

- Brisk. Dillon is enumerating responsibilities, not explaining them.
- "Run it clean" is procedural language — the closest Dillon gets to encouragement.

**Length:** ~25 seconds.

---

## CLIP 3: DRILL ONE COMPLETE

**Trigger:** Resupply confirmed complete. Artemis prepared to undock.

**Variant A (clean execution):**

> "Drill one complete. Docking within tolerance. Resupply confirmed: energy at one hundred percent, torpedo complement standard. Bridge coordination acceptable.
>
> Helm, undock and set course for the training area. Captain, your ship."

**Variant B (with procedural error caught and corrected):**

> "Drill one complete after retry. Initial approach was outside tolerance — corrected on second attempt. Resupply confirmed: energy at one hundred percent, torpedo complement standard. Coordination acceptable.
>
> Helm, undock and set course for the training area. Captain, your ship."

**Notes on delivery:**

- Even more procedural than Clip 2. No commendation. No encouragement. Acknowledgment only.
- Variant B is for when Dillon paused the drill mid-execution. If no retry occurred, use Variant A.

**Length:** ~20 seconds each.

**Production note:** If you want to reduce production load, record Variant A only. Skip Variant B and have the GM voice it from memory if needed.

---

## CLIP 4: DRILL TWO INTRO — GUIDED CONTACT HANDLING

**Trigger:** Artemis departs Tarsis and enters the training operating area. Drill Drone 01 is ready to spawn at long range.

**Script:**

> "Drill two. Guided contact handling and controlled disable.
>
> This drill will proceed step by step. I will call each station action, then hold the drill until the check is complete.
>
> Objective: identify the contact, hail it, establish firing geometry, bring weapons power to threshold, select and tune the target, then disable the contact's weapons subsystem under captain authorization. The contact will not attack.
>
> Weapons hold until authorized. Exit criterion is weapons subsystem disabled and ceasefire confirmed.
>
> Proceed when ready."

**Length target:** ~35 seconds.

**Delivery notes:**

- Emphasize "step by step" and "hold the drill until the check is complete."
- Keep tone instructional, not remedial.
- This clip replaces the old no-fire threat-identification framing.

---

## OPTIONAL DRILL TWO STEP PROMPTS

These can be GM-voiced in Dillon's tone or sent as Training Control text. Use them as checks, not speeches.

### Step 1 — Science

> "Step one. Science, scan and classify the contact. Report when you have full classification."

Completion line:

> "Science check complete. Contact classified as TSN drill drone."

### Step 2 — Comms

> "Step two. Comms, hail on standard bands. Report the response."

Completion line:

> "Comms check complete. Drill-mode response logged."

### Step 3 — Captain posture

> "Step three. Captain, authorize intercept posture. This is not fire authorization."

Completion line:

> "Command check complete. Intercept posture authorized. Weapons remain on hold."

### Step 4 — Helm geometry

> "Step four. Helm, establish safe firing geometry. Weapons needs arc, not proximity."

Completion line:

> "Helm check complete. Firing geometry acceptable."

### Step 5 — Engineering boost

> "Step five. Engineering, bring weapons power to training threshold. Report heat and coolant stable."

Completion line:

> "Engineering check complete. Weapons power at threshold, heat within tolerance."

### Step 6 — Weapons ready

> "Step six. Weapons, select target, tune beams, and set manual subsystem target to Weapons. Hold fire."

Completion line:

> "Weapons readiness check complete. Target selected, beams tuned, Weapons subsystem selected."

### Step 7 — Fire authorization

> "Step seven. Captain, authorize controlled fire when ready. Objective is Weapons subsystem disable only."

Completion line:

> "Fire authorization logged. Weapons may engage the Weapons subsystem."

### Step 8 — Disable objective

> "Step eight. Weapons, fire to disable the Weapons subsystem. Cease fire when the objective is met."

Completion line:

> "Subsystem check complete. Weapons subsystem disabled."

### Step 9 — Ceasefire

> "Step nine. Captain, call ceasefire. Weapons, confirm weapons safe."

Completion line:

> "Ceasefire confirmed."

### Step 10 — Verification

> "Step ten. Science and Comms, verify target status."

Completion line:

> "Verification complete. Drone status stable."

---

## CLIP 5: DRILL TWO COMPLETE

**Trigger:** Drill Drone 01 Weapons subsystem disabled, ceasefire confirmed, and guided verification complete.

**Script:**

> "Drill two complete. Guided contact sequence logged: scan, hail, posture, geometry, power, target, authorization, subsystem disable, ceasefire, verification.
>
> The drone did not fight back. That was intentional. You have now seen the sequence.
>
> Resetting for drill three. Stand by."

**Length target:** ~24 seconds.

**Optional GM-voiced retry variant:**

> "Drill two paused. We are resetting to the current checkpoint. The objective is controlled subsystem disable, not target destruction or unauthorized fire. Repeat the step when ready."

---

## CLIP 6: DRILL THREE INTRO — NOW YOU DO IT

**Trigger:** Drill Drone 02 is deployed after Drill Two completion.

**Script:**

> "Drill three. Evasive live-fire repeat.
>
> Same contact-handling sequence. This time there are no step calls. Apply the procedure you just used.
>
> A second training drone will maneuver under simple evasion. Engagement is live fire after captain authorization. Objective: disable Engines. Do not destroy the drone unless the situation changes.
>
> Exit criterion is Engine subsystem disabled and ceasefire confirmed.
>
> Proceed when ready."

**Length target:** ~30 seconds.

**Delivery notes:**

- The key line is "This time there are no step calls."
- Do not enumerate every station task again. That would undercut the "now you do it" design.

---

## CLIP 7: DRILL THREE COMPLETE

**Trigger:** Drill Drone 02 Engine subsystem disabled and ceasefire confirmed.

**Script:**

> "Drill three complete. Evasive target disabled. Engine subsystem objective met under live fire. Ceasefire confirmed.
>
> Artemis is resupplied and demonstrably operational. Standard qualification cruise track is complete.
>
> Captain, return course to Tarsis when ready."

**Length target:** ~22 seconds.

**Optional GM-voiced overfire variant:**

> "Drill three paused. Objective was Engine subsystem disable, not target destruction. Resetting the drone for one repeat."

---

## CLIP 8: PIVOT ACKNOWLEDGMENT

**Trigger:** Immediately after Anderson's new orders are received and the captain acknowledges. Dillon transmits to the bridge briefly.

**Script:**

> "Captain. Crew.
>
> The qualification framework remains in effect. This is now a live operation. The same observational discipline applies, but the consequences are real.
>
> Operate accordingly. I'll continue to observe."

**Notes on delivery:**

- Slightly weightier than the drill clips. Dillon is signaling the change in stakes without dramatizing.
- "Consequences are real" is the key line. Read it cleanly.

**Length:** ~20 seconds.

---

## CLIP 9: DISTRESS SIGNAL OBSERVATION (optional)

**Trigger:** Optional. Plays only if the GM wants to mark the moment the captain decides to deviate to the distress signal. Many sessions will skip this clip entirely.

**Script:**

> "Captain. Noted. Investigation decision is logged."

**Notes on delivery:**

- Briefest of all clips. Almost a procedural acknowledgment.

**Length:** ~8 seconds.

**Production note:** This is the lowest-priority clip. Skip it if you want to reduce production load to 11 clips.

---

## CLIP 10: DEBRIEF OPENING

**Trigger:** Mission resolution complete. Artemis on return transit. Dillon begins the qualification debrief.

**Script:**

> "Captain. Crew.
>
> Khovan Reach is operationally complete. We're returning to standard. I'll walk the qualification framework station by station.
>
> Before I begin, the operational outcome: [GM fills this in based on session result — e.g., 'Halcyon Drift stabilized, crew preserved, pirates engaged and surrendered, no own-ship casualties' or 'Halcyon Drift stabilized, crew preserved, DAMCON casualties Reyes, Park, and Achebe' or whatever applies].
>
> Standard debrief order: Captain, Helm, Weapons, Engineering, Science, Comms. Begin with the Captain."

**Notes on delivery:**

- Two parts: a fixed opening, then a GM-filled operational summary. Record only the fixed parts; GM voices the summary live based on session outcome.
- Two recorded segments:
  - Opening: "Captain. Crew. Khovan Reach is operationally complete. We're returning to standard. I'll walk the qualification framework station by station. Before I begin, the operational outcome:"
  - Closing: "Standard debrief order: Captain, Helm, Weapons, Engineering, Science, Comms. Begin with the Captain."
- GM speaks the outcome summary in their own voice in between, or in voice mode imitating Dillon's tone.

**Length:** ~30 seconds for the recorded segments combined.

---

## CLIP 11: DAMCON REPLENISHMENT (conditional)

**Trigger:** Plays only if DAMCON casualties occurred. Inserted during the debrief at an appropriate moment (typically after Engineering's qualification review).

**Script:**

> "DAMCON personnel status.
>
> Reyes, Park, and Achebe. Logged as deceased in the line of duty. Recorded with honors. Replenishment scheduled at next station rotation.
>
> This loss is part of the operational record. The crew should know who they were."

**Notes on delivery:**

- This is the one clip with even slight tonal weight. Dillon doesn't dramatize, but he doesn't move past it either. The "the crew should know who they were" line is the dignity-preserving moment.
- Read the three names cleanly and distinctly. Pause briefly between each.

**Length:** ~25 seconds.

**Production note:** If you want to reduce production load, this clip can be GM-voiced live. The recorded version adds weight; the GM version is functional.

---

## CLIP 12: DEBRIEF CLOSING

**Trigger:** End of qualification debrief. All stations have received feedback.

**Script:**

> "Qualification cruise concluded. All stations have received feedback. Anderson's closing transmission may follow.
>
> You're a crew now. Some of the work in front of you will be harder than what we just ran. Most of it won't be. Either way: you handled this one.
>
> Dismissed."

**Notes on delivery:**

- The "you're a crew now" line is the most personal Dillon gets. Not warm — acknowledging. Read it as a procedural statement of fact, not as a moment.
- "Dismissed" is the operational close. Final word.

**Length:** ~20 seconds.

---

## PRODUCTION SUMMARY

If you record everything: 12 clips. About 4-5 minutes of total audio.

If you record minimum viable: 9 clips. Skip Clip 9 (distress signal observation), Clip 11 (DAMCON replenishment — GM voices live), and Variant B of Clip 3 (drill one complete with retry). About 4 minutes of audio.

**Recommended production order:**

1. Clip 1 (opening briefing) — most important, sets the tone
2. Clip 12 (debrief closing) — pair with opening, both calibrate Dillon's voice
3. Clips 2-7 (drill clips) — short, repetitive structure
4. Clip 8 (pivot acknowledgment)
5. Clip 10 (debrief opening — both segments)
6. Clip 11 (DAMCON conditional)
7. Clip 9 (distress observation — optional)

Estimated total recording time: 1-2 focused sessions (~90 minutes each) including takes and review. Dillon's procedural tone is forgiving — you don't need perfect emotional delivery, you need clean professional delivery.

---

## TONAL NOTES — KEEPING DILLON CONSISTENT

Across all clips, Dillon should sound:

- **Calm.** Not bored — calm. He is alert, he is paying attention, he just doesn't dramatize.
- **Procedural.** He uses procedural language reflexively. "Within tolerance." "Coordination acceptable." "Operate accordingly." This is his voice.
- **Faintly bureaucratic.** He could be reading a status report. The information is delivered cleanly without performance.
- **Brief.** He doesn't pad. He doesn't editorialize. He says what needs to be said and stops.

What he is NOT:

- He is not warm. No "great job, crew." Not even at the end.
- He is not stern. He's not a drill instructor. He's an observer.
- He is not theatrical. The Sigma Protocol Dillon voice carries over — Inquiry Control, procedural, distant.

If a take feels too warm or too dramatic, redo it cooler. Dillon's character is in the restraint.

---

## END OF DILLON CLIP SCRIPTS
