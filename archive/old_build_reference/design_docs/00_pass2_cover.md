# KHOVAN REACH — PASS 2 COVER

*NPC files, scripted dialogue, and clip scripts for the Khovan Reach scenario. Pass 2 of three. Companion to Pass 1 Rev 1.2.*

---

## CONTENTS

Pass 2 ships five working files:

1. **`01_hessler_voice_mode.md`** — GPT-4o operating file for Captain Hessler aboard Halcyon Drift. The sole voice-mode NPC in this scenario. Used during Scene 9 (Engineering away mission).

2. **`02_pirate_dialogue.md`** — Scripted comms exchanges for the two pirate captains (Vrenn-Ka, Therrek-Bal). Drives the state machine defined in Pass 1 Rev 1.1. Used during Scene 12.

3. **`03_damcon_reports.md`** — Scheduled comms messages from the trapped DAMCON team (Reyes, Park, Achebe). Surfaces the suit O2 timer through fiction. Used during Scenes 11-14.

4. **`04_anderson_clips.md`** — Full text for the recorded Anderson clips. Three primary clips (one definite, two optional). Hybrid presentation pattern from Sigma Protocol.

5. **`05_dillon_clips.md`** — Full text for all 12 Dillon instructor clips. Includes opening briefing, three drill pairs, pivot acknowledgment, debrief opening, conditional DAMCON acknowledgment, and debrief closing.

Approximate combined length: ~6,500 words across the five files. Slightly larger than Pass 2 scope estimate (5,500-6,000) — the pirate dialogue file expanded to handle the full state machine cleanly.

---

## PASS 2 DESIGN DECISIONS

**Revision note for the baked Drill Two/Three update:** Dillon Clips 4-7 in this bundle reflect the later Act I teach-then-transfer update: Drill Two is guided contact handling ending in Weapons subsystem disable; Drill Three is the unguided evasive repeat ending in Engine subsystem disable. The clip count remains 12.

Decisions made during Pass 2 that weren't fully locked in the outline or Pass 1. Review and push back if any don't match design intent.

**1. Pirate captain names locked.** Vrenn-Ka (Cordial Reach) and Therrek-Bal (Bright Reckoning). Both pronounceable, distinct from each other, neither too on-the-nose. These can be changed; the dialogue tables would need find-and-replace.

**2. Hessler's first name: Aurel.** Pronounceable, ambiguous as to species or origin (could be human, could be Vesperan colonial), fits a civilian cargo captain. Surname Hessler held from Pass 1.

**3. DAMCON team specific personalities.** Reyes (calm, military, female, Cuban-coded), Park (younger, animated, female, Korean-coded), Achebe (quiet, technical, male, Igbo-coded). Personalities are minimal — they exist to make the loss matter if it occurs. If you'd prefer different personalities, the rewrite is small.

**4. The "wreck" tell.** Throughout the pirate dialogue, the pirates refer to Halcyon Drift as "the wreck" or "the casualty" before TSN has confirmed crew status. Real salvagers wouldn't do this on an active distress signal. This is one of the deeper deception cues a sharp Comms player might catch.

**5. Anderson casualty acknowledgment includes the DAMCON names.** "Reyes, Park, Achebe — recorded with honors." This was a deliberate choice to give the moment weight. If you want Anderson to remain colder, the line can be cut to "DAMCON casualties recorded with honors" without naming.

**6. Three variants of Anderson's Status Acknowledgment clip.** Clean success, with DAMCON casualties, with Halcyon Drift loss. If production load is a concern, recommend recording the first two and improvising the third — the Halcyon Drift loss outcome is rare in expected play.

**7. Dillon clip count.** 12 total. The "minimum viable" set drops to 9 by skipping the distress signal observation (Clip 9), the drill-one retry variant (Clip 3 Variant B), and the DAMCON replenishment (Clip 11, GM-voiced live instead).

**8. Two-segment debrief opening (Clip 10).** The recorded clip has two parts (opening framing + transition to station-by-station) with GM-voiced operational summary in between. This is the only Dillon clip that combines recording with live GM voice work.

**9. Hessler can be quiet for a beat during the cascade.** Voice-mode files generally discourage stage directions and silences, but this is the one moment the file explicitly allows it. The exhausted captain absorbing that his ship is killing TSN personnel is a legitimate beat for a brief silence.

**10. Pirates do not have a planned final confrontation moment with the captain.** If they surrender, they're processed. If they're destroyed, they're destroyed. If they flee, they flee. There is no "before we go" pirate-captain monologue. This preserves the clean opportunism motive — they're not characters, they're a threat.

---

## CROSS-FILE NOTES

A few things to flag about how the files interact during play.

### Hessler and the pirates

Hessler does not voice-roleplay with the pirates directly. The pirate dialogue is GM-spoken over the Comms console. Hessler, in voice mode, may report unauthorized docking attempts ("Artemis, they're trying to dock without authorization") but the actual pirate dialogue happens through the Comms console, not through the Hessler voice-mode chat.

If during the away mission the engineer asks Hessler about the salvagers, Hessler honestly doesn't know — he's not familiar with them and has no reason to think they're pirates until they reveal themselves. This is consistent with Hessler's no-secrets design.

### DAMCON reports and the suit O2 timer

The DAMCON reports are the primary mechanism for surfacing the timer. The MAST script (Pass 3) will schedule these reports at the specified intervals. The reports are pre-written; the GM reads them aloud over the Comms console when triggered.

If the captain disrupts the natural rhythm (e.g., calls a long bridge conference and a report would interrupt awkwardly), the GM can delay a report by 30-60 seconds. The schedule is approximate, not strict.

### Dillon's debrief and the qualification cards

Dillon's debrief clips (10, 11, 12) are framing only. The actual station-by-station qualification review is GM-voiced in Dillon's tone, working from the qualification cards (Pass 3 deliverable). The cards drive the content; the clips provide the structural framing.

### Anderson's hybrid presentation

Anderson's video appearance is limited to Clip 1 (new orders). All subsequent Anderson clips are low-bandwidth packet format — still image plus audio, justified in-fiction by routing through containment zones or normal command-net packetization. This matches the Sigma Protocol design pattern.

---

## WHAT'S NOT IN PASS 2

Things deliberately not included that come in Pass 3:

- Per-station qualification cards (final text)
- GM operational notes (failure handling, pacing guidance, common questions)
- MAST scripting requirements documentation (detailed enough to feed to ChatGPT for code generation)
- Debrief script template (the structure Dillon's debrief follows, with station-by-station prompts)

---

## PASS 3 SCOPE

Estimated:

- Qualification cards (6 stations): ~1,200 words total
- GM operational notes: ~1,500 words
- MAST scripting documentation: ~1,200 words
- Debrief script template: ~500 words

Total: ~4,400 words. Smaller than Pass 1 or Pass 2.

After Pass 3, the full Khovan Reach scenario document is complete and ready for MAST implementation with ChatGPT support.

---

## END OF PASS 2 COVER
