# PIRATE SCRIPTED DIALOGUE

*Scripted comms exchanges for the two pirate captains in Scene 12. Designed to drive the state machine defined in Pass 1 Rev 1.1.*

---

## ABOUT THIS DOCUMENT

The two pirates are not voice-mode AI characters. They are scripted comms exchanges that the GM voices based on player Comms input. This document provides the dialogue branches keyed to the state variables.

The GM reads pirate lines aloud over the Comms console. The Comms player responds. The GM judges which state variable advanced based on the Comms player's wording. New dialogue is selected based on current state.

The two pirate captains have distinct voices but share the same underlying deception logic. They alternate or back each other up as the scene develops.

---

## 1. THE TWO PIRATE CAPTAINS

### Captain Vrenn-Ka (Vessel One: *Cordial Reach*, claiming Skaraani registry)

**Cover identity:** Senior salvage operator. Skaraani by claimed lineage. Hard-nosed, transactional, "first-on-scene-takes-the-prize" mentality.

**Voice texture:** Direct, mercantile rhythm. Uses commercial language reflexively — "the wreck," "the claim," "operational discretion." Speaks as if every conversation is a transaction. When pushed on legal points, retreats into procedural-sounding language that doesn't quite match real salvage law.

**Cultural mismatch tell:** Real Skaraani salvagers are aggressive about their cut but *procedurally precise* about credentials. Vrenn-Ka is aggressive about claiming the wreck but evasive about producing operating permits. That's the inconsistency a sharp Comms officer should catch.

**Sample voice (GM read aloud):**
> "Cordial Reach to TSN cruiser. We picked up the beacon. We're here for the claim. Stand down from the wreck and we'll do this clean."

### Captain Therrek-Bal (Vessel Two: *Bright Reckoning*, claiming Torgoth registry)

**Cover identity:** Junior salvage operator partnered with Vrenn-Ka. Torgoth by claimed lineage. Defers to Vrenn-Ka but speaks for himself when addressed directly.

**Voice texture:** More formal than Vrenn-Ka. Tries to invoke procedural language — "appropriate channels," "in accordance with operational practice." But his formality doesn't match real Torgoth honor protocols, which would require explicit deference to TSN authority on TSN-recognized distress, not lateral procedural argumentation.

**Cultural mismatch tell:** Real Torgoth salvagers would, when confronted by TSN authority on a crewed-vessel distress, formally acknowledge that authority and withdraw. Therrek-Bal does not withdraw and does not formally defer. That's wrong for the species he claims.

**Sample voice (GM read aloud):**
> "TSN cruiser, this is Bright Reckoning. We have legitimate operational interest in the casualty vessel. We request the appropriate channels for coordinating with your team."

---

## 2. STATE MACHINE QUICK REFERENCE

From Pass 1 Rev 1.1. GM tracks current values:

- `pirate_cover_status`: `intact` / `suspected` / `exposed`
- `credentials_requested`: yes/no
- `credentials_provided`: none / partial / evasive / refused
- `legal_posture_challenged`: yes/no
- `cultural_mismatch_observed`: yes/no
- `science_scan_completed`: yes/no
- `science_scan_result`: clean / suspicious
- `docking_requested`: yes/no
- `docking_denied`: yes/no
- `unauthorized_docking_attempt`: yes/no
- `combat_active`: yes/no
- `pirate_outcome`: pending / fled / surrendered / destroyed / boarded / escaped_with_cargo

State transitions:
- `intact` → `suspected`: any one strong tell (Comms probe surfaces evasion, Science scan returns suspicious, captain explicitly questions cover)
- `suspected` → `exposed`: second strong tell, OR escalation event (unauthorized docking, weapons activation, refusal to acknowledge TSN authority after explicit invocation)
- `intact` → `exposed`: unauthorized docking attempt directly (skips suspected if no probe occurred)

---

## 3. INITIAL HAIL (state: intact)

The pirates hail Halcyon Drift, or are hailed by Comms first. Order of lines below assumes Comms hails them; reverse if pirates hail first.

### Pirate opening hail (if they hail first)

**Vrenn-Ka, opening hail to Halcyon Drift:**
> "Halcyon Drift, Cordial Reach. We picked up your beacon. We're here for the claim. Confirm crew status and prepare to evacuate. Standard salvage protocols apply."

**If Halcyon Drift does not respond:** Pirates hail Artemis directly after about 30 seconds:
> "TSN cruiser, Cordial Reach. We have operational interest in the casualty vessel. Coordinating salvage operations. Out."

### TSN-initiated hail (if Comms reaches them first)

**Comms hails the unknown contacts.** Standard TSN identification challenge.

**Vrenn-Ka response (default, state: intact):**
> "Cordial Reach, independent salvage. We picked up the distress beacon and arrived to investigate. We have operational interest in the casualty vessel. Coordinating our approach with the scene."

**Therrek-Bal echo (within 10 seconds):**
> "Bright Reckoning, also responding. Salvage cooperative arrangement with Cordial Reach. We can coordinate through appropriate channels."

---

## 4. COMMS PROBE BRANCHES

The Comms player will (hopefully) probe in one or more of these directions. Each probe produces a response that may advance state.

### PROBE 1: Registry credentials

**Comms asks for credentials, registry verification, operating permits, or authorization documentation.**

Mark: `credentials_requested = yes`

**Vrenn-Ka response (state: intact, first probe):**
> "Cordial Reach is registered out of the Skaraani Free Trade Combine. Operating zone permits will be transmitted once we've secured the wreck. Standard procedure."

> *Tell: real Skaraani protocols transmit credentials on request, not after asset acquisition. "Standard procedure" is wrong. Also calls Halcyon Drift "the wreck" — it's a crewed vessel in distress, not wreckage.*

Mark: `credentials_provided = evasive`

If Comms catches this and pushes: `pirate_cover_status: intact → suspected`

**Vrenn-Ka response if pressed for credentials again:**
> "TSN cruiser, we're operating under independent salvage authority. Credentials will be provided through appropriate channels at the appropriate time. I'm not going to debate procedure on an open band."

> *Tell deepens: real salvagers don't refuse credential transmission. The deflection is increasingly clumsy.*

Mark: `credentials_provided = refused` (advance state if not already suspected)

**Therrek-Bal interjection (if Comms continues to press Vrenn-Ka):**
> "TSN cruiser, Bright Reckoning. We can coordinate through appropriate channels once operational scene authority is resolved. Until then, we maintain operational discretion."

> *Tell: Torgoth would defer to TSN authority on a TSN-recognized scene. "Operational discretion" against TSN authority is wrong for the claimed species.*

If Comms identifies the cultural mismatch: `cultural_mismatch_observed = yes`, advance state.

### PROBE 2: Legal posture

**Comms invokes rescue law. Standard line: "Halcyon Drift is a crewed vessel broadcasting distress. Rescue law applies, not salvage law. You are required to stand down from any claim and offer assistance or depart."**

Mark: `legal_posture_challenged = yes`

**Vrenn-Ka response (state: intact):**
> "Acknowledged, TSN cruiser. We're aware of the vessel's status. Once we've assessed scene conditions, we can coordinate appropriate action. Cordial Reach standing by."

> *Tell: this does not actually concede the legal point. Real salvagers, on being correctly cited, either depart or explicitly acknowledge "we will stand down." Vrenn-Ka deflects without conceding.*

If Comms presses ("Do you acknowledge that *Halcyon Drift* is not salvageable property and that you have no legal claim?"):

**Vrenn-Ka second response:**
> "We are taking the situation under operational review. Cordial Reach will not interfere with rescue operations once they are properly authorized."

> *Tell deepens: "properly authorized" implies the pirates have a role in authorizing TSN rescue. Real salvagers do not.*

If Comms continues to press for explicit acknowledgment: `pirate_cover_status: intact → suspected` (or `suspected → exposed` if already suspected).

### PROBE 3: Cultural protocol

**Comms invokes species-specific protocol expectations. Example: "Cordial Reach, Skaraani Free Trade Combine protocols require credential transmission on TSN authority request. Transmit credentials now or stand down."**

Or to Therrek-Bal: "Bright Reckoning, Torgoth honor protocols on TSN-recognized distress require formal withdrawal or explicit assistance offer. State your intent."

Mark: `cultural_mismatch_observed = yes` if the cultural cite is correct and the pirate response evades.

**Vrenn-Ka response to Skaraani protocol challenge:**
> "TSN cruiser, we observe the protocols appropriate to our operational situation. We'll transmit through appropriate channels."

> *Tell: this evades the specific protocol citation. Real Skaraani would either comply or formally dispute the protocol citation. They wouldn't deflect to "appropriate channels."*

**Therrek-Bal response to Torgoth protocol challenge:**
> "TSN cruiser, Bright Reckoning observes appropriate operational practice. We do not require correction on our own cultural procedures."

> *Tell: real Torgoth would not push back on a TSN authority citing Torgoth protocol — that would itself be a protocol violation. The defensiveness is wrong for the claimed species.*

Either response, if Comms recognizes the wrongness: `pirate_cover_status` advances.

### PROBE 4: Operational conduct

**Comms challenges the pirates' approach trajectory. Example: "Cordial Reach, you are closing to docking distance with an active TSN rescue scene. Standard practice for legitimate salvage observation is station-keeping at minimum 10 km. Why are you closing?"**

**Vrenn-Ka response:**
> "TSN cruiser, we're positioning for operational efficiency. We can coordinate distance once scene authority is established. Cordial Reach holding course."

> *Tell: "holding course" while at the same time saying they can coordinate distance is contradictory. Real salvagers, on a distance challenge, would either justify the approach with specific operational reasoning or back off.*

If Comms recognizes this: `pirate_cover_status` advances.

### PROBE 5: Science scan

**Science scans the vessels for weapons signatures, boarding equipment, transponder consistency, hull profile.**

Mark: `science_scan_completed = yes`

GM consults Science scan result.

Result: **suspicious.** Science detects:
- Weapons signatures consistent with boarding-grade armaments (not civilian salvage tools)
- Boarding clamps deployed (not salvage tow rigs)
- Transponder signature inconsistent with claimed registry (the IDs don't match registered Skaraani Free Trade or Torgoth Honor Bond vessels)
- Hull modifications consistent with combat operations

Mark: `science_scan_result = suspicious`

Science can report any combination of the above. Each specific finding is a piece of corroborating evidence. Science reporting two or more is strong corroboration.

If `pirate_cover_status = intact` and Science returns suspicious: advance to `suspected`.

If `pirate_cover_status = suspected` and Science returns suspicious: advance to `exposed`.

---

## 5. DOCKING REQUEST AND ESCALATION (Path 2 backstop)

If Comms does not advance `pirate_cover_status` beyond `intact` within approximately 3-4 minutes of pirate arrival, the pirates initiate docking sequence.

### Pirate docking request

**Vrenn-Ka, broadcast to both Halcyon Drift and Artemis:**
> "Halcyon Drift, Cordial Reach. We're approaching to docking distance to secure the casualty. Confirm boarding lock status. Cordial Reach inbound."

Mark: `docking_requested = yes`

### Denial response

If the captain (or Hessler via comms, or Engineering if aboard Halcyon Drift) explicitly denies docking authorization:

Mark: `docking_denied = yes`

**Vrenn-Ka, initial response to denial:**
> "TSN cruiser, we have operational interest in the casualty. Denying our approach is outside standard protocol. We're going to need a justification."

> *Pirates hold position briefly (2-3 minutes of fiction time) but do not retreat.*

### Unauthorized docking attempt

If the captain holds the denial, after 2-3 minutes:

**Vrenn-Ka, no further announcement; vessels begin closing toward docking range.**

Hessler reports from Halcyon Drift via Comms:
> "Artemis, Halcyon Drift. They're closing without authorization. Boarding clamps deploying. I'm locking my hatches. This isn't salvage — these aren't salvagers!"

Mark: `unauthorized_docking_attempt = yes`. Advance `pirate_cover_status` directly to `exposed`.

**Vrenn-Ka, once `exposed`:**
> "TSN cruiser, your civilian's lying. Stand down or we'll consider this hostile interference."

> *The pretense is dropped. The bluff has failed. Combat is imminent.*

---

## 6. EXPOSED STATE — IMMEDIATE PRE-COMBAT

Once `pirate_cover_status = exposed`, the scene transitions toward combat. The pirates have several response patterns based on whether they were exposed by probe or by escalation.

### If exposed by Comms probe (before docking attempt)

The pirates know they've been caught. They have two choices: fight or flee. They choose based on Artemis's position and threat posture.

**If Artemis is at Halcyon Drift with weapons hot:** Pirates attempt to flee. Mark `pirate_outcome = fleeing_pending`. Captain decides whether to pursue.

**Vrenn-Ka, fleeing:**
> "Cordial Reach withdrawing. We're not here to fight a cruiser. Bright Reckoning, break off."

**If Artemis is en route from Khovan Reach (not at the scene):** Pirates accelerate the boarding attempt while Artemis is still distant. Combat with Halcyon Drift becomes active.

**Vrenn-Ka, committing:**
> "Cordial Reach attacking. Bright Reckoning, take their comms. We need to be gone before that cruiser closes."

### If exposed by unauthorized docking attempt

The pirates are already at boarding distance. Combat begins immediately.

**Vrenn-Ka, on boarding attempt:**
> "Bright Reckoning, breach and clear. We're not leaving without the cargo."

Mark: `combat_active = yes`

---

## 7. COMBAT ENGAGEMENT DIALOGUE

Once combat is active, the pirates speak less. The GM can drop brief lines for atmosphere but the scene shifts to mechanical Weapons engagement.

Sample combat lines (GM uses sparingly, for texture):

**Vrenn-Ka under fire:**
> "Cordial Reach taking damage. Bright Reckoning, cover."

**Therrek-Bal under fire:**
> "Bright Reckoning, hull breach in section two. Pulling back!"

**Vrenn-Ka in serious damage:**
> "TSN cruiser, Cordial Reach standing down! We surrender! Hold fire!"

If captain accepts surrender: `pirate_outcome = surrendered`. The vessel powers down; boarding actions stop. Bright Reckoning may continue fighting or also surrender depending on damage state — GM's call based on combat flow.

**Therrek-Bal in serious damage (if Vrenn-Ka is destroyed or surrendered):**
> "Bright Reckoning surrendering! We surrender! Cease fire!"

If captain refuses surrender or doesn't get the chance to accept: combat continues until destruction. `pirate_outcome = destroyed`.

**Either captain, fleeing successfully (Artemis declines pursuit):**
> "Bright Reckoning clear! Cordial Reach, vector to grid 47-Carnia. Out!"

Mark: `pirate_outcome = fled`

---

## 8. POST-COMBAT — BOARDING AND PRISONER HANDLING

If the captain accepts surrender, the pirates' fate becomes a brief operational beat:

**Comms can broadcast to surrendered pirates:**
> "Surrendered vessels, stand down all weapons. Prepare to be boarded. Any resistance results in lethal force."

**Vrenn-Ka, surrendered:**
> "Cordial Reach acknowledges. We're powering down. Crew complement of seven on this hull."

**Therrek-Bal, surrendered:**
> "Bright Reckoning acknowledges. Five aboard."

The actual boarding is GM-narrated. Standard TSN procedure: Marines deploy, secure vessels, take prisoners, escort back to Artemis for transport to TSN authority. This is a brief beat — maybe 1-2 minutes of GM narration. The pirates do not have further dialogue once secured.

---

## 9. SPECIAL CASES

### If Comms attempts cultural fluency in the pirates' favor

Some Comms players will try to be diplomatic — invoking common ground, offering compromises. The pirates will exploit this if `pirate_cover_status = intact`.

**Vrenn-Ka, exploiting diplomatic approach:**
> "Now you're talking sense, TSN. We're all just doing our jobs. We can coordinate this clean — let us approach the casualty and we'll work with your team."

> *This advances toward docking. The Comms player is being played. If they don't catch the manipulation, the pirates close to docking range under cover of "coordination."*

**GM call:** If Comms doesn't make any probes and instead just tries to cooperate with the pirates, the scene advances faster toward escalation. The captain should be warned via Hessler ("Artemis, they're getting close. Are they cleared to dock?") — but the consequence of soft diplomacy is faster pirate approach.

### If captain orders weapons hot before exposure

If the captain authorizes Weapons readiness while `pirate_cover_status = intact` or `suspected`, this is a real qualification question — but not fatal. Weapons readiness does not equal firing. Captain can have Weapons hot and not fire until the pirates expose themselves.

If the captain orders weapons to *fire* on the pirates while `pirate_cover_status = intact` (no tells surfaced, no Science suspicion), this is a problem — the captain has fired on apparent civilians. The scene continues but the debrief will note the premature force authorization. The pirates will then attack in earnest, having been attacked first.

### If Hessler is asked to verify pirate identity

The captain may ask Hessler whether he recognizes the salvagers. Honest answer: he doesn't recognize them by name and is not aware of any legitimate salvage claim on his ship. He doesn't know they're pirates until they reveal themselves.

This corroborates Comms suspicion if Comms is probing well, but it's not by itself a deception cue — Hessler not recognizing them could just mean they're new to the region.

---

## 10. GM NOTES

### Pacing

This scene is approximately 10 minutes of session time. The state machine should advance steadily through it. If state hasn't advanced past `intact` within 4-5 minutes of pirate arrival, fall to the Path 2 backstop and trigger docking request.

If Comms is doing strong probing work, the state can advance to `exposed` quickly — within 2-3 minutes. That's correct play. The scene then transitions to combat or pursuit decision earlier.

### Reading the Comms player

The Comms player's wording is the input that drives state transitions. Listen for:

- Any explicit request for credentials, permits, registry, authorization → advance the credentials track
- Any invocation of rescue law, distress protocols, salvage law → advance the legal track
- Any species-specific protocol citation → advance the cultural track
- Any challenge to approach distance, trajectory, or behavior → advance the operational track

You don't need to track every word. If the Comms player is clearly probing in good faith, advance state. If they're just chatting with the pirates without challenging, hold state at `intact` and prepare to fall to Path 2.

### Voice work

Vrenn-Ka and Therrek-Bal should sound different. Vrenn-Ka is mercantile and direct — almost gruff. Therrek-Bal is more formal and slightly higher-pitched in delivery. The distinction helps the table track which vessel is responding.

If you can't do two clearly distinct voices, name them explicitly when speaking — "Vrenn-Ka responds..." or "Therrek-Bal cuts in..." before delivering the line.

### The "salvage rights don't apply" beat

Real maritime/space law clearly distinguishes salvage (recovery of derelict/abandoned property) from rescue (assistance to crewed vessels in distress). A crewed ship broadcasting distress is unambiguously a rescue scenario, not salvage. The pirates' attempt to claim salvage rights is therefore *legally impossible* if Halcyon Drift's crew is alive. Real salvagers know this. Pirates posing as salvagers are betting that the TSN crew won't push the legal point precisely.

When Comms makes the rescue-law citation explicitly, the pirates have no good response. Their evasions are clumsy because the law is on TSN's side. This is what makes the Comms probe work as a deception detector.

---

## END OF PIRATE SCRIPTED DIALOGUE
