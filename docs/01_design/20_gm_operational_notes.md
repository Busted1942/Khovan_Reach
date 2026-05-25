# KHOVAN REACH — GM OPERATIONAL NOTES v2.2 MERGED
*Updated GM guide after runtime architecture, Scenario Control Panel, and testing/regression improvements.*

Status: Canonical GM operations guide  
Supersedes: `docs/01_design/20_gm_operational_notes.md` and `docs/01_design/20_gm_operational_notes.md` for active use  
Pair with: `docs/01_design/00_scenario_play_guide.md`, Pass 2 content files, `docs/01_design/30_qualification_cards.md`, `docs/02_content/50_debrief_script.md`, `docs/02_content/20_damcon_reports.md`, and `docs/01_design/10_mast_requirements.md`

---

# 1. GM operating stance

**Repo-consolidation note:** Use this guide with `docs/00_project/00_source_index.md`. Older Pass 3 GM notes and previous handoff references are archived.


Khovan Reach is runtime-driven and GM-supervised.

Your job is not to manually run the mission engine.

Your job is to:
- watch player decisions
- perform key NPC/dialogue moments
- adjust pacing when needed
- interpret ambiguous actions
- preserve scenario flow
- deliver the debrief

The runtime should handle:
- scene sequencing
- clip triggers
- timers
- checkpointing
- state logging
- story-jump presets
- evidence display

Use the Scenario Control Panel as a support instrument, not as a manual steering wheel for every beat.

---

# 2. Before-session prep

## 2.1 Materials checklist

- [ ] Cosmos/MAST mission loads cleanly.
- [ ] Scenario Control Panel visible to GM only.
- [ ] Player-facing debug/admin controls hidden.
- [ ] Dillon clips recorded and accessible.
- [ ] Anderson clips recorded and accessible.
- [ ] Pirate dialogue document available.
- [ ] DAMCON reports available.
- [ ] Hessler voice-mode file ready.
- [ ] Qualification cards available for debrief.
- [ ] Debrief script available.
- [ ] Pre-session acceptance checklist run.
- [ ] Backup physical timer available.
- [ ] Notes/log sheet available.

## 2.2 Pre-session acceptance checklist

Run this before a player session:

```text
PRE-001: fresh mission load reaches Scene 1
PRE-002: player-facing debug hidden
PRE-003: GM Scenario Control Panel visible
PRE-004: jump to Drill Two; verify prompt/clip/drone
PRE-005: jump to Anderson Orders; verify clip trigger
PRE-006: jump to cascade_decision; verify DAMCON timer start
PRE-007: jump to pirate_arrival_cover_intact; verify pirate state and GM branch display
PRE-008: jump to repair_resolution_clean; verify debrief opens
PRE-009: reload last checkpoint once
PRE-010: replay last clip once
PRE-011: verify audio assets available
PRE-012: verify Hessler voice-mode file ready
```

Do not skip this for live sessions once implementation is underway.

---

# 3. Player briefing

Before starting Cosmos, tell players:

- This is a 95-105 minute mission with debrief.
- Qualification happens through normal play.
- They will not see qualification cards during the mission.
- Dillon observes and surfaces results at the end.
- A real operation can produce real losses.
- The mission will not fail in a campaign-ending way; catastrophic ship destruction reloads from checkpoint.
- One brief Engineering away mission uses Hessler voice-mode.
- The bridge should play the mission, not chase the rubric.

Keep this to 2-3 minutes.

---

# 4. Scenario Control Panel modes

## 4.1 Test / Authoring Mode

Use for:
- development
- playtest setup
- jump testing
- focused feature tests
- synthetic debrief states

Not for normal live play.

## 4.2 Live GM Recovery Mode

Use during actual sessions.

Permitted live uses:
- reload last checkpoint
- hold/release transition
- replay critical clip
- delay/trigger DAMCON report
- reset current drill after safety failure
- expose pirates if state machine deadlocks
- force next scene only if blocked
- add qualification note

Avoid arbitrary story jumps in live play unless the session is broken.

---


# 5. Pacing targets

Act I duration now depends on the selected profile:

```text
Full Shakedown Cruise:       ~38-45 minutes
Compressed Shakedown Cruise: ~18-25 minutes
Direct Scenario:             ~10-15 minutes
Act II:                      ~15 minutes
Act III:                     ~50 minutes
Debrief:                     ~10 minutes
```

The GM should not rush Full Shakedown when the crew consists of new players. The extra time is intentional training value.

Do compress only when:

- players already understand normal station controls
- live-session time is constrained
- the captain explicitly chooses compressed or direct mode
- the training objective is qualification confirmation rather than onboarding

# 6. Act I shakedown fork

Act I now has three captain-selectable profiles:

```text
Full Shakedown Cruise
Compressed Shakedown Cruise
Direct Scenario
```

The GM should present this as an operational choice, not a meta-game difficulty menu.

Suggested framing:

> "Training Control has three profiles available. Full shakedown if the crew wants the complete systems pass. Compressed shakedown if you want the essential checks only. Direct scenario if you want to skip drills after expedited Tarsis resupply. Your call, Captain."

## 6.1 GM operating rule for Act I

Do not manually drive the drills if the runtime can gate them.

Use this priority:

1. Let MAST detect the event.
2. Let Comms/captain confirmation carry unobservable in-fiction actions.
3. Use GM marks only when neither is available.

The GM should watch player behavior and pacing, not operate as a hidden mission CPU.

## 6.2 Generator-governor start

Do not tell the crew before departure that the generator is governed. Let them request departure clearance, depart, and notice the sluggish response.

Ten seconds after launch-envelope exit, Kestrel Yard Control sends the generator advisory through the overlay and Comms archive. The message explains:

- Kestrel is working a generator-output problem.
- A temporary governor is limiting output.
- Artemis has two homing torpedoes as emergency conversion reserve.
- Tarsis has been notified to prioritize homing torpedoes and generator acceptance.

This is a better fiction than starting with visibly low energy: the crew experiences a ship problem and learns to route the solution through Comms and Tarsis.

## 6.3 Tarsis gate

Do not allow docking at Tarsis until Comms has requested:

1. homing torpedo production priority
2. generator acceptance/support
3. docking clearance

If the runtime cannot block docking mechanically, the GM should treat premature docking as Tarsis refusing yard-lock until the missing request is made.

## 6.4 Full Shakedown

Full mode is for new players or crews who want onboarding.

GM focus:

- keep instructions short
- let the overlay/Comms archive carry the procedure
- do not over-explain station controls if the player is succeeding
- treat mistakes as training resets, not punishment

Important gates:

- Engineering power/no-motion validation
- DAMCON rest-cycle and meal-cycle confirmations
- controlled overload and repairs
- navigation priority preset
- Drone 01 controlled disable
- Drone 02 live-fire destroy
- cultural Comms packet

## 6.5 Compressed Shakedown

Compressed mode should feel operationally valid, not like a skipped tutorial.

Run only:

- Kestrel departure and generator advisory
- Tarsis priority/docking/resupply
- controlled Drone 01 disable
- optional quick live-fire target if time permits
- cultural Comms packet

Skipped Engineering practice items are N/A/development-only.

## 6.6 Direct Scenario

Direct mode is allowed. Do not punish the crew for choosing it.

Run:

- Kestrel departure and generator advisory
- Tarsis priority/docking/resupply
- shakedown bypass confirmation
- Act II transition

Act I drill observations are recorded as "not observed by captain election," not NEEDS RETEST. Later live-operation performance carries more weight.

## 6.7 Drone 01 safety resets

If Weapons fires before authorization, reset the drone five kilometers farther from the Tarsis Training Beacon.

If the captain allows the controlled-disable drone to be destroyed, reset the drone five kilometers farther from the Tarsis Training Beacon.

Read this as training discipline, not as failure narration.

Suggested line:

> "Training Control: target reset. The drill objective was controlled disable, not destruction. Reacquire and wait for clearance."

## 6.8 DAMCON location fallback

DAMCON location may not be visible to the engine. Prefer in-fiction confirmation through Comms:

> "DAMCON Control confirms rest-cycle standby in crew quarters."

or

> "DAMCON Control confirms meal-cycle standby in mess."

Only use GM marks if the Comms confirmation pathway is unavailable.

# 7. Hessler / away mission

The Hessler scene is GM/voice-mode-heavy but should remain bounded.

Runtime wrapper should show beats:

1. Greeting/damaged section
2. Diagnostic discussion
3. Stabilizer convergence
4. Repair preparation
5. Cascade trigger
6. Bridge report

GM job:
- Keep Hessler cooperative and honest.
- Avoid withholding information.
- Keep scene to roughly 8-10 minutes.
- Trigger cascade after the required beats are complete.
- Do not let the voice-mode scene become a second full game.

If Hessler hallucinated or overstates technical certainty, correct in GM narration or redirect to Engineering expertise.

---

# 8. DAMCON timer

## 8.1 Runtime primary, physical backup

MAST is the primary timer once implemented.

Use a phone/kitchen timer only as backup.

The runtime should:
- start timer at cascade
- schedule reports
- show next report to GM
- calculate outcome
- preserve timer state across checkpoint

## 8.2 Delivery timing

Reports should be delivered on schedule unless they would interrupt an important decision or combat beat.

Allowed GM drift:
- normal: up to 60 seconds
- combat: up to 90 seconds

Do not delay repeatedly to spare the players pressure. The timer is meant to matter.

## 8.3 Canonical outcomes

Extended timer:

```text
T+0 to <T+10: clean survival
T+10 to <T+30: hypoxic survival
T+30+: total loss
```

Compressed timer:

```text
T+0 to <T+5: clean survival
T+5 to <T+15: hypoxic survival
T+15+: total loss
```

T+25 extended and T+10 compressed should be treated as deep critical bands, not automatic death.

If total loss occurs, do not retroactively rescue Reyes, Park, and Achebe.

---

# 9. Pirate scene

Scene 12 remains the hardest scene.

Runtime should now support you by showing:
- current pirate cover status
- suggested dialogue branch
- primary pirate variables
- available transitions
- backstop timer state
- combat transition control

You still voice the pirates.

Track four primary variables mentally:

```text
pirate_cover_status
combat_active
unauthorized_docking_attempt
pirate_outcome
```

Let the runtime track the rest.

## 9.1 Comms interpretation

Ask:

```text
Did the Comms player probe a deception cue, or just talk?
```

Probe cues:
- credentials
- registry
- rescue law
- cultural protocol
- docking distance
- operational authority
- the premature “wreck/casualty” tell

If they probe well, advance suspicion or exposure.

When in doubt, favor detection over stonewalling. The design rewards sharp Comms play.

## 9.2 Backstop path

If Comms does not meaningfully probe after 3-4 minutes, runtime should surface docking backstop.

You may:
- trigger docking request
- wait another interval
- hold backstop for pacing

If denied, pirates attempt unauthorized docking after the designed delay.

## 9.3 Combat transition

Once combat starts:
- stop extended pirate dialogue
- use one or two combat flavor lines only
- let bridge mechanics take over
- focus on outcome tracking

---

# 10. Cache and repair

Science selection is a real qualification moment.

If wrong component is selected:
- do not detect the error at the cache unless Engineering cross-checks cleanly
- reveal the error on installation attempt
- require return/retry path
- apply timer consequence
- log Science development item

Wrong selection is recoverable but costly.

---

# 11. Checkpoint and reload

Reload is for catastrophic recovery, not tactical undo.

Canonical checkpoint IDs:

```text
post_drill_1
post_drill_2
post_drill_3
post_anderson_orders
post_halcyon_arrival
post_cascade
pre_pirate_combat
mission_resolution
```

Before reload, verify whether irreversible consequences have occurred.

Reload does not undo:
- DAMCON deaths
- Halcyon Drift loss/damage already visible in fiction
- expended or converted torpedoes
- qualification observations
- pirate exposure already revealed

---

# 12. Qualification and debrief

Runtime evidence display is support only.

You decide final ratings.

During play:
- jot brief notes
- mark evidence when convenient
- do not fill out the entire card live
- avoid GM bandwidth collapse

During debrief:
- use runtime display and notes
- speak in Dillon's procedural tone
- focus on meaningful observations
- keep developmental feedback specific
- allow player questions after Dillon's close

The debrief is educational, not punitive.

---

# 13. Common recovery actions

## Clip failed

Use Scenario Control Panel:

```text
Replay last clip / replay selected clip
```

Give a one-sentence GM bridge if necessary.

## Drone stuck

Use:

```text
reset current drill
respawn drone
mark subsystem disabled only if actually observed or test mode
```

## DAMCON report missed

Use:

```text
trigger next DAMCON report
```

Do not rewind the timer unless it was a technical fault.

## Pirate state deadlocked

Use:

```text
mark suspected
mark exposed
trigger docking request
trigger combat
```

Choose the least invasive recovery that preserves fiction.

## Player refuses investigation/cache run

Use the documented offramp or brick wall. Do not have Dillon solve the decision for them.

---

# 14. After-session workflow

After each session:

1. Save regression/playtest log.
2. Record actual act timings.
3. Record where GM had to intervene.
4. Record confusing beats.
5. Record runtime bugs.
6. Record qualification/debrief clarity issues.
7. Update known issues.
8. If design change is needed, route back to architecture project.

Do not silently mutate architecture from implementation convenience.

---

# 15. GM success criteria

A good GM run feels like:

```text
The runtime handles structure.
The players make decisions.
The GM conducts the experience.
```

You should not feel like you are manually moving every scene forward.

You should feel like you are supervising a mission that mostly runs, intervening when human judgment is valuable.
