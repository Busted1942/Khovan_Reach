# KHOVAN REACH — PASS 3 COVER

*Final pass. Qualification cards, GM notes, MAST scripting requirements, debrief script. Completes the Khovan Reach scenario document set.*

---

## CONTENTS

Pass 3 ships four working files:

1. **`01_qualification_cards.md`** — Final per-station qualification cards. GM-only, surfaced at debrief. Six stations with 4-6 observation items each. Pass/Partial/Needs Retest rubric.

2. **`02_gm_operational_notes.md`** — Practical guidance for the GM running the mission. Prep checklist, pacing guidance, judgment calls, common problems and how to handle them.

3. **`03_mast_requirements.md`** — Implementation specification for the MAST code. Designed to be handed to ChatGPT alongside Pass 1 and Pass 2 documents as the spec for code generation.

4. **`04_debrief_script.md`** — Template for the post-mission debrief. Sequential flow with embedded clip cues and station-by-station prompts.

Approximate combined length: ~10,500 words. Slightly larger than my Pass 3 estimate (~4,400) for the same reason Pass 2 ran over — the MAST requirements document expanded to cover the state machine implementation in detail, and the debrief template needed concrete example language to be useful.

---

## PASS 3 DESIGN DECISIONS

**Revision note for the baked Drill Two/Three update:** The Pass 3 files in this bundle incorporate the Act I teach-then-transfer update: guided Drill Two with Weapons subsystem disable, unguided Drill Three with Engine subsystem disable, MAST gates/observations for both, and updated qualification/debrief guidance.

Decisions made during Pass 3 that weren't fully locked in the outline or earlier passes.

**1. Qualification card structure: 4-6 items per station, with Pass/Partial/Needs Retest rubric.** This provides observable granularity without becoming a bureaucratic checklist. Each item is tied to a specific scene moment so the GM knows what to watch for.

**2. Overall qualification result has three tiers, not pass/fail.** "Full qualification," "qualified with development items," and "qualified with retests required." This matches real military training frameworks — most personnel qualify on first attempt with notes, not on a binary pass/fail.

**3. Dillon's instructor override is rare.** Once or twice per session maximum. The Pass 3 GM notes emphasize this — Dillon's role is observation, not active correction. The override exists for catastrophic moments only.

**4. GM operational notes include explicit "judgment calls" section.** Some decisions during play are interpretive — when to advance pirate state, when to invoke override, when to deliver off-schedule reports. The notes name these explicitly so the GM knows where their authority lies.

**5. MAST scripting estimates total 1,200-1,800 lines of code across all files.** This is comparable to LegendaryMissions in scope. I'm being honest that this is a real coding project, not a trivial script.

**6. State machine for pirates uses GM-voiced dialogue triggered by MAST state transitions.** Rather than fully scripted branching dialogue with TTS, MAST tracks state and triggers dialogue *type*; GM reads the corresponding text from Pass 2. This is a deliberate simplification that keeps implementation lightweight while preserving the design logic.

**7. State save/reload boundaries documented explicitly.** The reload cannot undo DAMCON deaths, Halcyon Drift damage, or expended torpedoes. It exists for catastrophic failure recovery (ship destruction), not for "I wish I'd decided differently."

**8. Debrief template includes specific example language for developmental notes.** Rather than just "Dillon makes a developmental observation here," the template provides illustrative examples ("Your cache component identification saved approximately 15 minutes — three personnel are alive because of that precision"). The GM adapts; the examples calibrate the tone.

**9. The debrief allows for player questions at the end.** This is a deliberate transition out of Dillon's voice into the GM's voice. Players can ask "why did I get a partial on that?" and the answer comes from the GM as themselves, not from Dillon as a character.

**10. DAMCON casualty handling is dignified without being maudlin.** The Pass 3 framing — Dillon reads the names cleanly, the GM holds a brief silence, no apologies — is intentional. The dignity is in the procedural restraint, not in performed grief.

---

## THE COMPLETE SCENARIO DOCUMENT SET

After Pass 3, the full Khovan Reach scenario document set is:

| File | Pass | Purpose |
|---|---|---|
| `khovan_reach_outline.md` | Outline | High-level design specification |
| `khovan_reach_pass1_v2.md` | Pass 1 Rev 1.2 | Scene-by-scene play guide, captain's briefing, design philosophy |
| `00_pass2_cover.md` | Pass 2 | Pass 2 contents summary and design decisions |
| `01_hessler_voice_mode.md` | Pass 2 | GPT-4o operating file for Hessler |
| `02_pirate_dialogue.md` | Pass 2 | Scripted pirate dialogue with state machine routing |
| `03_damcon_reports.md` | Pass 2 | Scheduled DAMCON team comms reports |
| `04_anderson_clips.md` | Pass 2 | Recorded Anderson clip scripts |
| `05_dillon_clips.md` | Pass 2 | Recorded Dillon clip scripts |
| `00_pass3_cover.md` | Pass 3 | This document |
| `01_qualification_cards.md` | Pass 3 | Per-station qualification cards |
| `02_gm_operational_notes.md` | Pass 3 | GM guidance for running the mission |
| `03_mast_requirements.md` | Pass 3 | Implementation specification for MAST code |
| `04_debrief_script.md` | Pass 3 | Template for the debrief sequence |

**13 files total.** Approximately 28,000-30,000 words of documentation.

---

## WHAT COMES NEXT

The scenario document set is complete. What remains is implementation.

### Phase 1: Audio production (1-2 evenings)

Record the Dillon clips (12) and Anderson clips (3-5 variants). Pass 2 scripts have the full text. Plan ~1-2 hours per recording session including takes and review.

### Phase 2: Development environment setup (weekend)

Follow the setup checklist from the weekend setup materials. Get Cosmos, VS Code, sbs_cli, and the ChatGPT project working together. Verify with the trivial MAST test.

### Phase 3: MAST implementation (20-40 hours across multiple sessions)

Work through the MAST requirements document with ChatGPT in VS Code. Use Claude here for design validation when uncertain. Follow the recommended session sequence in Pass 3 file 3, Section 10.

### Phase 4: Playtest (multiple sessions)

Run the scenario with a willing crew. Take playtest notes. Iterate on dialogue, pacing, MAST bugs, qualification card text. Expect 2-3 playtest sessions before the scenario feels solid.

### Phase 5: Final delivery

After playtest revisions, the scenario is ready for normal use. Run it with new crews as needed for qualification training.

---

## REFLECTIONS ON THE DESIGN PROCESS

A few honest observations now that the document set is complete.

**The design grew significantly through conversation.** What started as "a training mission for new players" became a full-weight tabletop scenario with moral stakes, command decisions, and real consequences. This happened because each refinement was good on its own merits and you correctly recognized when something I'd written was contrived (the fetch convergence, the salvager legal framing). The cumulative effect is a scenario richer than what the original brief described.

**The two iterations on the outline were the right move.** The initial outline missed several things — the salvager legal issue, the convenient fetch framing, the under-served Weapons station. The revision pass surfaced all of these. Pass 1 Rev 1.1 incorporated them. Pass 2 and Pass 3 built on that solid foundation. If you'd accepted the first outline as final, the scenario would be weaker.

**The pirate state machine is the load-bearing innovation.** Most training scenarios test stations through scripted drills. Khovan Reach tests Comms through dynamic deception detection with multiple paths to resolution. The state machine that drives this is more complex than most tabletop scenario mechanics, but it's what gives Comms a meaningful role in Act III.

**Voice-mode NPC use is deliberately minimal.** Hessler is the only GPT-4o character because the design surfaced that voice-mode AI is harder to control than console play, and exposing the team to it once (in a low-stakes, cooperative scenario) is more valuable than scattering AI NPCs throughout. This calibration matches what's known about voice-mode reliability.

**The qualification framework being GM-only was the right choice.** Earlier in the design conversation, you considered visible qualification cards during play. We landed on GM-only with debrief surface. This produces better play (players engage with the fiction, not the rubric) and a more honest training experience.

---

## A PERSONAL NOTE

This was a substantial design conversation. Over the course of building Khovan Reach, we worked through:

- Reframing from training-with-fiction to fiction-with-training-scaffolding
- Resolving the contrived fetch motivation
- Correcting the salvager-vs-pirate legal framing
- Designing the pirate state machine
- Choosing the right tonal register for Hessler
- Locking the DAMCON team mechanics
- Defining the no-fail design boundaries
- Establishing Dillon's bookend role
- Specifying the MAST implementation in enough detail to hand off

Each of those was a real design conversation. The scenario reflects that work.

What you have now is a complete tabletop scenario specification. It's not done — it has to be recorded, scripted, playtested, and revised. But the design is solid. The document set tells you what to build.

When you run it, take playtest notes. Some things will surprise you. Some will need adjustment. That's expected. The design accommodates revision.

---

## END OF PASS 3 COVER
