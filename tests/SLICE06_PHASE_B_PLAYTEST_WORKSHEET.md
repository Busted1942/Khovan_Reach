# Slice 06 Phase B Playtest Worksheet

Branch/build: `slice06-drone-contact-fire` at `6c59daf`  
Operator: ____________________  Date/time: ____________________  Cosmos build: ____________________

Use one fresh server session for the normal run. Record `PASS`, `FAIL`, or `AMBIGUOUS`—a clean screen with no trace or state evidence is **AMBIGUOUS**, not a pass. Attach screenshots or copy the relevant `tests/live_startup_trace.txt` lines for every completed check.

## Before the run

- [ ] Branch/build confirmed: `slice06-drone-contact-fire` / `6c59daf`
- [ ] `python run_tests.py quick` passes before launch
- [ ] Fresh Cosmos server/session started
- [ ] Crew stations available: Science / Comms / Weapons / Helm / Captain
- [ ] Engineering Shakedown Complete state reached (or approved equivalent entry state)
- [ ] Current objective shows Drone 01 ready
- [ ] Trace file cleared or a session start marker recorded

Evidence notes:  
______________________________________________________________________________

## ACT1-019 — Drone 01 early-fire reset

Test action: Deploy Drone 01. Before Training Control authorizes fire, apply a Weapons hit.

Expected outcome:

- [ ] Drone 01 is removed/reset and does not advance the disable sequence.
- [ ] Replacement Drone 01 appears 5 km farther from the Tarsis Training Beacon than the prior spawn (initial offset is 15 km).
- [ ] Scan, hail, relay, Weapons-lock, range, stationary-hold, and hit-count state are cleared.
- [ ] Objective broadcast says: “Training Control: unauthorized hit detected. Target reset. Reacquire, reestablish range, and wait for clearance.”
- [ ] No Drone 02 spawn and no Act-II-ready state.

Observed result: `PASS / FAIL / AMBIGUOUS`  Notes: ________________________________  
Trace marker / screenshot: _____________________________________________________

Failure or ambiguity to record: wrong offset, stale gate, no objective, duplicate target, or no trace/state evidence.

## ACT1-020 — Drone 01 destruction reset

Test action: Deploy a fresh Drone 01 and destroy it before the Weapons array is disabled.

Expected outcome:

- [ ] Destruction is classified as premature Drone 01 destruction, not success.
- [ ] Drone 01 respawns 5 km farther again; reset offset is now 25 km if ACT1-019 was run first, otherwise 20 km.
- [ ] `drone_01_destroyed_in_error`/reset status is visible in trace or GM state.
- [ ] Objective broadcast says: “Training Control: target destroyed. Drill objective was controlled subsystem disable. Target reset for repeat.”
- [ ] Drone 02 does not spawn.

Observed result: `PASS / FAIL / AMBIGUOUS`  Notes: ________________________________  
Trace marker / screenshot: _____________________________________________________

Failure or ambiguity to record: cleanup counted as a kill, offset did not increment, Drone 02 appeared, or no evidence.

## ACT1-021 — Range band and stationary hold

Test action: Deploy Drone 01 and complete scan, hail, shield relay, and Weapons selection. Try to authorize outside 1–2 km, then enter the band and move during the hold.

Expected outcome:

- [ ] Science's `Initial Scan` or `scan` displays: "Drone 01 is a neutral training contact. Weak shield-frequency relay data is available for Weapons."
- [ ] Fire remains blocked outside 1–2 km.
- [ ] Fire remains blocked until Artemis is stationary in the band for 15 seconds.
- [ ] Movement or leaving the band resets the hold timer; stale delayed work cannot authorize fire.
- [ ] After a continuous 15-second stationary hold in range, the objective broadcast authorizes Weapons fire.
- [ ] If an observer cannot verify a value, its named Comms/GM fallback is available.

Observed result: `PASS / FAIL / AMBIGUOUS`  Notes: ________________________________  
Range observed: __________ m  Hold observed: __________ s  
Trace marker / screenshot: _____________________________________________________

Failure or ambiguity to record: early authorization, timer survives movement/reset, wrong range, or fallback unavailable.

## ACT1-022 — Drone 01 Weapons-array disable

Test action: After authorization, use manual targeting on Drone 01’s Weapons array. Apply three confirmed Weapons subsystem hits, then stop firing.

Expected outcome:

- [ ] Only a damage event with `MANUAL_SYSTEM = WEAPONS` increments the hit count.
- [ ] `MANUAL_CRITICAL_HIT` is not required for a valid subsystem hit.
- [ ] Non-Weapons subsystem hits and generic `system_damage` do not increment the Weapons count.
- [ ] Hit 1, hit 2, and hit 3 are separately evidenced; exactly the third valid hit sets Weapons disabled.
- [ ] Objective broadcast requests ceasefire; Drone 01 is not complete until ceasefire is confirmed.

Observed result: `PASS / FAIL / AMBIGUOUS`  Notes: ________________________________  
Hit evidence / `MANUAL_SYSTEM` values: __________________________________________  
Trace marker / screenshot: _____________________________________________________

Failure or ambiguity to record: count advances on generic damage, fewer/more than three valid hits, signal absent without fallback, or disable occurs before the third hit.

## ACT1-023 — Drone 02 genuine destruction and Act-II-ready boundary

Test action: Confirm Drone 01 ceasefire. Verify Drone 02 appears, run one GM cleanup as a negative control, then perform a genuine Weapons destruction.

Expected outcome:

- [ ] Drone 02 appears at 10 km from the Tarsis Training Beacon and remains training-safe.
- [ ] GM cleanup records cleanup—not a genuine kill—and does not set completion.
- [ ] Genuine destruction records `drone_02_destroyed` / genuine destruction source.
- [ ] `drone_contact_act2_ready` becomes true and `drone_contact_act2_handoff_status` identifies Slice 07 readiness.
- [ ] `mission_phase` remains `act_1`; Slice 06 does not invent or invoke an Act-II callback.

Observed result: `PASS / FAIL / AMBIGUOUS`  Notes: ________________________________  
Drone 02 offset: __________ m  Cleanup source: __________________  Kill source: __________________  
Trace marker / screenshot: _____________________________________________________

Failure or ambiguity to record: cleanup counts as completion, wrong spawn range, no ready marker, phase changes early, or no source evidence.

## ACT1-024 — Cultural Comms packet

Test action: After genuine Drone 02 destruction, inspect the player objective surface and Comms archive.

Expected outcome:

- [ ] The canonical cultural packet appears through the objective-broadcast channel.
- [ ] The packet appears in the Comms archive exactly once.
- [ ] No Phase A instrumentation wording (“observe whether”, API-test language, or stock-menu probe text) is player-visible.
- [ ] Objective identifies the Act-II-ready boundary and tells the crew to stand by for orders.

Observed result: `PASS / FAIL / AMBIGUOUS`  Notes: ________________________________  
Archive entry / screenshot: ____________________________________________________

Failure or ambiguity to record: missing/duplicated packet, GM-only output, instrumentation text, or no archive/state evidence.

## Fallback and profile checks

- [ ] Scan fallback is available and marks only scan complete.
- [ ] Hail fallback is available and marks only hail complete.
- [ ] Shield-relay fallback is available and marks only relay complete.
- [ ] Weapons-lock fallback is available and starts/continues the hold observer.
- [ ] Range fallback is available and does not skip unrelated gates.
- [ ] Stationary-hold fallback is available and authorizes only after the preceding gates.
- [ ] Subsystem-hit fallback requires authorization and does not double-count a later automatic hit.
- [ ] Ceasefire fallback completes only after Weapons disable.
- [ ] Full Shakedown runs Drone 02 by default.
- [ ] Compressed Shakedown runs Drone 02 by default.
- [ ] Direct Scenario bypasses both drones without failure flags.

## Session summary

| Test | Result | Evidence captured | Follow-up |
|---|---|---|---|
| ACT1-019 | __________ | __________________ | __________________ |
| ACT1-020 | __________ | __________________ | __________________ |
| ACT1-021 | __________ | __________________ | __________________ |
| ACT1-022 | __________ | __________________ | __________________ |
| ACT1-023 | __________ | __________________ | __________________ |
| ACT1-024 | __________ | __________________ | __________________ |

Overall: `PASS / PARTIAL / FAIL / AMBIGUOUS`  
Trace marker last: _____________________________________________________________  
Operator finding / blocker: ___________________________________________________

Static checks prove file structure only. This worksheet’s checkboxes become live evidence only when backed by the operator observation and trace/state evidence recorded above.
