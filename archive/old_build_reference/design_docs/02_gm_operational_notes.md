# KHOVAN REACH — GM OPERATIONAL NOTES

*Guidance for the GM running Khovan Reach. Practical notes on pacing, failure handling, common questions, and judgment calls that emerge during play.*

---

## ABOUT THIS DOCUMENT

These notes are not the scenario design — that's in Pass 1 Rev 1.1. These are not the dialogue or clips — those are in Pass 2. This is what the GM needs to know in addition to those materials: how to run the mission well, what to watch for, how to handle the unexpected.

Read this once before your first session. Skim it again before each subsequent session. Add your own playtest notes to it as you learn what your group needs.

---

## 1. PREP BEFORE THE SESSION

### Materials checklist

Before the players arrive:

- [ ] All Dillon clips recorded and accessible (12 clips)
- [ ] All Anderson clips recorded and accessible (1 definite, 2-3 variants of optional)
- [ ] Pirate dialogue document open or printed for live reference
- [ ] DAMCON reports document open or printed for live reference
- [ ] Qualification cards document open for post-mission debrief
- [ ] Hessler voice-mode file ready to paste into a fresh ChatGPT voice chat
- [ ] MAST mission loaded in Cosmos and verified to run
- [ ] Notebook or scratch sheet for tracking qualification observations
- [ ] Timer (your phone, a kitchen timer, anything) for the suit O2 countdown
- [ ] Snacks and water — this is a 95-105 minute session

### Players-on-deck briefing

Before starting Cosmos, give your players a 2-3 minute briefing:

- This is a 95-105 minute mission with a debrief at the end
- They'll be qualifying on their stations through real play, not drill checks
- The instructor (Dillon) will observe and surface what was tracked at debrief
- There's a real possibility of crew losses if certain decisions go badly
- The mission cannot fail in a campaign-ending way — if the ship is destroyed, the session resets to the last checkpoint
- One brief away mission, no other voice-mode AI work
- Questions before we start?

This sets expectations. Players who understand the no-fail design and the qualification framework will play more confidently. Players who think they're being tested in a punitive way will play timidly and miss the experience.

---

## 2. PACING GUIDANCE

### Total session budget

95-105 minutes from "Captain on deck" to "Dismissed" at the end of Dillon's debrief.

If you're tracking time:
- Act I (qualification cruise): 28-30 minutes target
- Act II (investigation): 15 minutes
- Act III (Halcyon Drift and Khovan Reach): 50 minutes
- Debrief: 10 minutes

Add 5-10 minutes of slack for transitions, questions, real-life interruptions.

### Where to compress if you're running long

If Act I is running long, do not skip the core Drill Two checks — that drill is the guided teaching pass. Keep each prompt short and each confirmation crisp. Drill Three can end as soon as the Engine subsystem is disabled and ceasefire is confirmed; do not extend it into extra practice unless a single repeat is needed after overfire or major confusion.

If Act II is running long, skip the Cache Retrieval Side-Trip (Scene 8). It's only relevant if the captain prioritized the fetch before the rescue, and that's a rare path.

If Act III is running long, the biggest variable is the cache retrieval. If Science correctly identifies the component first time, the cache scene is a quick 3-4 minutes. If they pick wrong, the recovery run takes additional time. Plan for this — the worst-case timing math should still fit within Act III's 50-minute budget, but barely.

If the debrief is running long, focus on the most important qualification items per station rather than walking through every observation. The debrief is for player feedback, not for completing the checklist.

### Where to expand if you're running short

Some crews move quickly. If you finish Act II in 8-10 minutes and Act III in 35-40, you have extra time. Use it for:

- More descriptive scene narration during transits (atmospheric detail, crew chatter on the bridge)
- Letting the pirates' interaction with Comms run longer if Comms is doing strong probing work
- A longer Hessler conversation during the away mission, especially if the engineer is asking good diagnostic questions

Avoid filling time with new content — stick to what's in the design. If you're done in 70 minutes, end the session at 70 minutes. Don't pad.

---

## 3. ACT I TEACH-THEN-TRANSFER DRILLS

Act I now uses a teach-then-transfer pattern.

- Drill Two: guided, step-by-step, passive drone, Weapons subsystem disabled.
- Drill Three: unguided, simple evasion, live fire, Engine subsystem disabled.

This is the right place to teach the whole ship-contact loop because the later pirate encounter should not be the first time players have to combine scan, hail, geometry, power, subsystem targeting, and ceasefire.

### How to run Drill Two

Drill Two is a tutorial in procedure. Be explicit and sequential.

Run the steps in this order:

1. Science scan/classify.
2. Comms hail/report.
3. Captain intercept posture, not fire authorization.
4. Helm safe firing geometry.
5. Engineering weapons boost/heat stable.
6. Weapons select/tune/manual target Weapons, hold fire.
7. Captain controlled-fire authorization.
8. Weapons disable Weapons subsystem.
9. Captain/Weapons ceasefire.
10. Science/Comms verification.

Do not rush the sequence. The point is to make every station feel the loop once.

Do not make the drone threatening. It should not fight back or evade. If players ask why it is passive, answer in Dillon's tone:

> "This is a procedural drill, not a threat drill. The contact is passive by design."

### Check discipline

After each step, confirm the check before moving on.

Use concise confirmation language:

- "Science check complete."
- "Comms check complete."
- "Helm geometry acceptable."
- "Engineering check complete."
- "Weapons readiness check complete."
- "Ceasefire confirmed."

These checks can be GM-observed. Do not let lack of API instrumentation derail the tutorial.

### How hard to grade Drill Two

Grade Drill Two leniently unless the crew violates a safety boundary or cannot complete the prompted action.

Examples:

- Science needs one prompt to rescan: usually fine.
- Comms forgets to hail until prompted: expected in a guided drill.
- Weapons fires before authorization: serious development item.
- Drone destroyed before Weapons subsystem disable: retry or mark partial/needs retest.

Drill Two is where they learn. Drill Three is where you learn whether it stuck.

### How to run Drill Three

Drill Three is the unprompted repeat. Give the objective and then stop teaching.

Dillon intro should communicate:

- Same contact-handling sequence.
- No step calls.
- Drone will evade simply.
- Live fire after Captain authorization.
- Objective is Engine subsystem disabled.
- Ceasefire after objective.

Then observe.

Do not call out the station order again. Do not say "Science, scan now" or "Engineering, boost now" unless the drill has stalled enough to justify the single allowed nudge.

### The single allowed nudge

If the crew stalls completely, use one procedural nudge:

> "Crew, this is a repeat drill. Apply the previous sequence. Objective remains Engine subsystem disable."

Record that a nudge was needed. It should not stop the mission, but it matters for debrief.

### How hard to grade Drill Three

Grade Drill Three as the independent qualification signal.

Examples:

- Crew scans/hails/postures/powers/targets/ceasefires without prompt: strong pass.
- Crew disables Engines but skips Comms entirely: complete the drill, mark Comms partial/needs retest.
- Weapons disables Engines but only after wrong subsystem attempts: partial for Weapons.
- Engineering never boosts but the drone still disables: complete the drill, mark Engineering partial/needs retest unless the station was never cued by Captain.
- Captain never states objective but Weapons guesses correctly: mark Captain partial or needs retest.

Do not silently block completion because a process flag is missing. If Engines are disabled and ceasefire is confirmed, the drill has produced its runtime exit condition. Use the debrief to address skipped process steps.

### Drill failure handling

**Weapons fires before authorization in Drill Two:** pause and reset to the current safe step.

GM-voiced Dillon line:

> "Drill paused. Weapons fire preceded captain authorization. Resetting to fire-control step."

This is a development item for Captain and/or Weapons.

**Weapons fires before authorization in Drill Three:** do not necessarily pause unless safety or drone survival requires it. Record the observation. If the crew still disables Engines and ceases fire, allow completion with qualification consequences.

GM-voiced Dillon after completion if needed:

> "Drill three complete with authorization error recorded. We will address it in debrief."

**Drone destroyed before objective:** this is not a clean pass.

For Drill Two:

> "Drill paused. Objective was Weapons subsystem disable, not target destruction. Resetting the step."

For Drill Three:

> "Drill paused. Objective was Engine subsystem disable, not target destruction. Resetting for one repeat."

Use one retry maximum unless you deliberately want extra practice. After that, proceed and capture retest needs in debrief.

### Engineering boost handling

If Engineering does not boost in Drill Two, prompt directly because Drill Two is guided:

> "Engineering, training control requires weapons power at threshold before fire authorization. Report when stable."

If Engineering does not boost in Drill Three, do not prompt immediately. Observe whether the crew recognizes the need. If the task stalls mechanically, Captain or Weapons may ask for Engineering support. If no one does, use the single allowed nudge after the stall threshold.

### Pacing

Target timing:

- Drill Two: 9-11 minutes.
- Drill Three: 6-8 minutes.
- Act I total after update: approximately 28-30 minutes.

Drill Two may run long the first time because it is a guided tutorial. Keep each prompt short and each check crisp.

Drill Three should be short. If they can do it, they will do it quickly. If they cannot, one repeat is enough to expose the development item.

### Debug buttons and GM controls

GM-only controls are acceptable and likely necessary for guided checks.

Player-facing Debug buttons should be hidden for production if Cosmos allows it, especially on Science and Comms. Do not remove debug access globally if it supports smoke tests, checkpoint recovery, or GM manual marks.

Use the smallest set of GM controls needed:

- Mark each Drill Two check complete.
- Mark Drone 01 Weapons disabled if subsystem API is unavailable.
- Mark Drone 02 Engines disabled if subsystem API is unavailable.
- Mark Drill Three observation flags for debrief.
- Reset Drill Two/Three if overfire or test failure occurs.

### What not to add

Do not add the following to the revised drills:

- Torpedo conversion.
- EMP, mine, or nuke training.
- Pirate deception.
- Salvage-law dialogue.
- DAMCON timers.
- Cache retrieval.
- Boarding actions.

Those mechanics belong later. Act I should teach the ship-contact fundamentals and then move on.

---

## 4. THE PIRATE SCENE IS THE HARDEST TO RUN

Scene 12 is the most complex scene in the mission. It requires the GM to:

- Voice two distinct pirate captains
- Track the state machine (12 variables)
- Read Comms player input and decide which state transitions to trigger
- Manage the salvager arrival timer alongside the DAMCON suit O2 timer
- Coordinate with Hessler's voice-mode chat if engineer is aboard Halcyon Drift
- Be ready to flip from negotiation to combat with no prep time

Practical advice:

**Voice differentiation:** If you can't reliably distinguish Vrenn-Ka and Therrek-Bal vocally, just name them before each line. "Vrenn-Ka responds: 'We picked up your beacon...'" works fine. Players will track by the named attribution.

**State machine tracking:** Don't try to track all 12 variables. Track the four primary ones: `pirate_cover_status`, `combat_active`, `unauthorized_docking_attempt`, and `pirate_outcome`. The others are downstream and resolve themselves based on play.

**Comms input interpretation:** When the Comms player says something, ask yourself "did they probe a deception cue or did they just talk?" If they probed (asked for credentials, cited rescue law, invoked cultural protocols), advance state. If they just chatted, hold state. When in doubt, advance — the design favors detection over stonewalling.

**The "wreck" tell:** Watch for the Comms player picking up on Vrenn-Ka calling Halcyon Drift "the wreck" or "the casualty." This is a deep tell that a sharp player might catch. If they do, advance state on that observation alone.

**Falling to Path 2:** If the Comms player isn't probing effectively after 3-4 minutes, fall to the escalation backstop. The pirates request docking. Captain (or Hessler) denies. Pirates attempt unauthorized docking after 2-3 minutes. State advances to `exposed`. Combat begins.

**Combat transition:** When combat starts, the scene shifts mechanical. You stop voicing pirates and the bridge takes over with standard SBS combat. The pirate combat dialogue lines (in Pass 2) are for atmosphere only — drop one or two for texture, no more.

---

## 5. THE SUIT O2 TIMER

### Tracking the timer

Use a real-world timer. Your phone with a stopwatch works. Start it at the cascade event in Scene 9.

The extended scenario uses a 30-minute fictional timer with reports every 3 minutes. Real-world play will take roughly that long if pacing is good. The fictional time and real-world time are intentionally close.

The compressed scenario uses a 15-minute fictional timer with reports every 90 seconds. Real-world play will be slightly faster — say 12-15 minutes of actual play. Don't try to compress real-world play to match fictional time exactly.

### Delivering reports

Read the DAMCON reports at the scheduled intervals. The suit O2 numbers (30, 27, 24...) are the timer surface. Players will track time through the numbers without needing a visible clock.

If you need to delay a report because the bridge is mid-decision and the report would interrupt awkwardly, delay by 30-60 seconds. The schedule is approximate, not strict. Don't delay more than 60 seconds — that breaks the pacing.

If you need to advance a report because the bridge is in a quiet moment and pressure would help, deliver early. Same constraint — don't advance more than 60 seconds.

### Outcome thresholds

| Timer state at rescue completion | Outcome |
|---|---|
| T+0 to T+10 (extended) or T+0 to T+5 (compressed) | Clean survival, no medical needs |
| T+10 to T+25 (extended) or T+5 to T+10 (compressed) | Hypoxic but survive with medical |
| T+25+ (extended) or T+10+ (compressed) | Total team loss |

Rescue completion means the cache component is installed and atmosphere is restored to the affected section. Mark this moment when it happens and look up the outcome.

If the timer reaches the loss threshold and the rescue is not yet complete, the DAMCON team dies. Do not retroactively rescue them — the no-fail design covers ship destruction, not poor decisions about resource allocation. Reyes, Park, and Achebe are gone.

---

## 6. HANDLING COMMON PROBLEMS

### "The captain won't make a decision"

Some captains hedge. They ask Dillon for input. They wait for the bridge to advise. They put the decision back to the players to vote on.

Dillon does not give advice. Dillon observes. If asked, Dillon says: "That's your call, Captain."

The bridge can advise but the captain must commit. If the captain still won't, let the situation play out — the DAMCON team's timer doesn't pause for indecision. After 2-3 minutes of pure hedging, the captain has effectively chosen "no decision" which produces the worst of both worlds (engineer is aboard Halcyon Drift but Artemis hasn't departed for the fetch). Atmosphere keeps draining, suit O2 keeps decreasing, the mission keeps moving.

The qualification card captures the hedging. The debrief acknowledges it without lecturing.

### "Science picked the wrong cache component"

Recoverable failure is the design. Engineering will report on installation attempt that the component doesn't fit. Helm has to return to the cache for a second attempt. Time cost is real — significant timer compression.

The qualification card captures the failure. The mission continues.

If Science picks wrong on the second attempt too — which would require the player to ignore the same information twice — Engineering can salvage the situation through improvised use of available aboard-ship materials. This is a brick-wall recovery, narrated by the GM: "Engineering improvises with the wrong-spec stabilizer; the repair is slower and less stable but it works enough to bring atmosphere back online." This takes additional time and increases the chance of total DAMCON loss.

### "The Comms player is just chatting with the pirates"

If Comms is engaging with the pirates as if they're legitimate salvagers — agreeing with them, offering compromises, being diplomatically friendly — the pirates exploit this. Their cover holds longer because Comms isn't probing.

This is fine play; it's just a different qualification path. Fall to the escalation backstop. The pirates request docking, captain denies, pirates attempt unauthorized docking. State advances. Combat begins.

The Comms qualification card captures the missed probing. The debrief frames this as a development item — Comms learned that diplomatic cooperation isn't always the right tool.

### "The captain won't authorize force"

Some captains, having committed to the rules-of-engagement framing ("defensive posture, hailing before any escalation"), refuse to authorize Weapons against the pirates even after exposure. They keep negotiating. They request the pirates surrender. They issue ultimatums but don't fire.

This is genuine command judgment. Let it play out. The pirates will press the advantage — attempt docking, attack Halcyon Drift, threaten Engineering. If the captain holds the no-fire posture under direct attack, Halcyon Drift takes damage and Engineering (if aboard) is in real danger.

If the situation deteriorates badly, Dillon may break observation discipline once (briefly): "Captain. They've fired on a TSN-protected vessel. Standard ROE permits return fire." This is the only point in the mission where Dillon intervenes in real-time, and only if the captain is allowing real harm through indecision.

If the captain still refuses, let the pirates damage Halcyon Drift further or kill its crew. The qualification card captures the catastrophic judgment failure. The debrief addresses it gravely.

### "The crew destroyed the ship during the drills"

State-save reload. Roll back to the last drill checkpoint. Qualifications already demonstrated are preserved. The drill that caused the destruction is re-attempted.

This is rare in the qualification cruise drills. Drill Two uses a passive drone; Drill Three uses simple evasion and live fire but should remain low-risk. It is more common in the pirate engagement.

If the crew destroyed the ship while engaging pirates and the cascade timer hadn't yet expired, the state-save reload restores them to the start of Scene 12 with the pirate state at `intact` again. This gives them a second chance.

If the crew destroyed the ship after the cascade timer expired, the rescue is over either way. The reload restores to a point where they can complete the return to base but the rescue is recorded as catastrophic failure.

### "A player wants to do something not in the design"

Within reason, support player creativity. The design provides the mainline path; players who go off the path either find new approaches that work (great — improvise) or hit walls that nudge them back (also fine).

Things to support:
- Creative use of station consoles in unexpected ways
- Strong Comms work that probes deception in ways not specifically scripted
- Engineering improvisation during the rescue

Things to redirect:
- Players trying to bypass the design (e.g., teleporting Engineering back to Artemis instantly; this isn't a Cosmos mechanic)
- Players trying to short-circuit the qualification framework (e.g., demanding to know their card)
- Players trying to undermine other players' qualification work (e.g., Comms trying to take Weapons' fire authority)

When in doubt, support the creative attempt and adjust the qualification card accordingly.

---

## 7. JUDGMENT CALLS YOU'LL HAVE TO MAKE

### When to advance pirate state

The state machine is precise but the triggers are interpretive. You'll have to decide:

- Was that Comms probe strong enough to advance state? (If they explicitly cited rescue law and challenged the legal posture, yes. If they vaguely asked "what's your situation?", no.)
- Did Science's scan trigger the suspicious result? (If they specifically scanned for weapons signatures or transponder consistency, yes. If they did a general sweep, partial — surface one suspicious finding but not all.)
- Did the captain's challenge expose the pirates? (If they explicitly named the cover and demanded credentials with force, yes. If they just asked the pirates to back off, no.)

When in doubt, advance state. The design favors detection.

### When to call combat

Combat starts when `pirate_cover_status = exposed` AND the pirates are within engagement range AND either:

- The captain authorizes weapons-free, OR
- The pirates attempt unauthorized docking on Halcyon Drift, OR
- The pirates fire first

If `exposed` happens but Artemis is still en route from Khovan Reach (long way away), the pirates may try to escape rather than commit to combat. If they decide to flee, combat doesn't begin; the captain decides whether to pursue.

### When to invoke Dillon's instructor override

Once. Maybe twice. Dillon's role is observation. The override should only fire when:

- The captain is allowing real harm through paralysis (e.g., refusing to authorize force against pirates actively destroying Halcyon Drift)
- A station player needs immediate technical correction to prevent ship destruction during a drill

If you invoke Dillon's override more than twice in a session, you've over-supported. Players will lean on it. Use it sparingly.

### When to deliver DAMCON reports off-schedule

The schedule is the default. Deviate by 30-60 seconds if pacing requires. Don't deviate more than 60 seconds.

A specific exception: if combat is active and the bridge is fully engaged with the pirates, you can pause DAMCON reports briefly (max 90 seconds) and resume once combat resolves or pauses. The fiction is that combat noise has temporarily masked the team's transmissions.

---

## 8. AFTER THE SESSION

### Take notes immediately

Within an hour of the session ending, jot down:

- What path the captain chose (engineer-stays vs engineer-returns, torpedoes converted or not)
- Which qualification items each station hit cleanly and which were partial or missed
- What the salvager scene felt like (did Comms catch them? did combat happen?)
- The DAMCON outcome
- Anything surprising (player creativity, design issues, pacing problems)

Add these to your project's `docs/playtest_notes.md` file. Future-you will want these notes for revising the design or running additional sessions.

### Don't over-revise after one session

The first session will reveal issues. Some will be design problems (a beat doesn't land, a timing is wrong); some will be group-specific (your specific players struggled with one station). Wait until you've run the scenario at least twice before making structural changes. One session is a data point, not a pattern.

Small tunings are fine after one session — adjusting a clip line, tightening a state-machine trigger, fixing a typo in dialogue. Major structural changes wait for more data.

### Reuse with awareness

If you run Khovan Reach with a second crew, be aware that you (the GM) now have meta-knowledge about how players approach it. Resist the urge to "fix" things that worked fine with the first crew just because the second crew approached differently. Each crew finds their own path. The design accommodates multiple paths intentionally.

### Connect to Sigma Protocol

If your group plays Khovan Reach and then plays Sigma Protocol, Dillon's voice carries over. Players will recognize the procedural-observer character. This is the only intentional connection between the two scenarios — Khovan Reach is otherwise standalone.

Do not retcon Khovan Reach events into Sigma Protocol. If your Khovan Reach DAMCON team died, that doesn't appear in Sigma Protocol. The two scenarios share an instructor and a universe; they don't share a continuity.

---

## END OF GM OPERATIONAL NOTES
