# OPERATOR CHECKLIST — Dillon voice and prompt polish

Branch: `slice06-dillon-voice-and-prompt-polish`
Prepared: 2026-08-08
Status: **static evidence only — no live Cosmos run has rendered any of this copy**

This is the list of things only you can check. Everything on it needs a running
Cosmos session, a human reading a console, or a design judgment. Nothing here
can be closed from static tests.

---

# 0. What changed, in one paragraph

"Training Control" is retired as a speaker. All instructional and drill traffic
is now **Dillon**. Kestrel Yard Control and Tarsis Control remain distinct
stations. Redundant `"Training Control:"` prefixes were removed from message
bodies (the Comms title already names the sender) and from Current Objective
text (which renders no sender at all). Sixteen distinct spelling errors that
were reaching player consoles were corrected, and design language that had
leaked into player-facing copy was rewritten.

Files changed: 3 act files, 3 system files, 4 test files, 1 design doc.
No gate logic, no state names, no runtime flow changed. **Copy and speaker
attribution only.**

---

# 1. Before you launch

- [ ] `git checkout slice06-dillon-voice-and-prompt-polish`
- [ ] `python run_tests.py quick` — expect **PASS, 159 checks, 0 failures, 0 warnings**
- [ ] Confirm the summary does **not** print `EVIDENCE GAP` (that would mean the
      compile preflight skipped and this build is weaker than it looks)
- [ ] Clear or mark `tests/live_startup_trace.txt` so this session's trace is separable

---

# 2. The one thing that could actually be broken

Everything else here is cosmetic. This is not.

`khovan_engineering_send_message` passes `engineering_message_title` through to
`khovan_reach_send_safe_startup_message` as `startup_sender`, which becomes both
the `comms_override(from_name=...)` and the `comms_receive(title=...)`. That
default changed from `"Training Control"` to `"Dillon"`.

- [ ] **ENG messages still render at all.** Reach the Engineering shakedown and
      confirm at least one Dillon message appears on a player console.
      - Expected: message renders with sender/title **Dillon**
      - Failure: message does not render, or renders with title `(unknown)`
      - **If it shows `(unknown)`, stop and report it.** That is the same
        signature as the GM `comms_receive()` rendering failure recorded in
        `SLICE06_VERIFICATION.md`, and it would mean the sender identity is not
        binding — a real bug, not a copy problem.
      - Trace to check: `[KHOVAN ACT1 ENG MSG] guarded message sent`

---

# 3. Copy review — read these on a real console

The point is whether they read naturally to a crew who has never seen the
mission. Mark each **OK** or write what felt wrong.

## Kestrel departure

- [ ] Objective: "Comms, request departure clearance from Kestrel Yard Control."
- [ ] Kestrel yard-lock message
- [ ] Kestrel generator advisory (10s after launch envelope)
- [ ] Dillon speed-power reminder — reads as Dillon, not a station
- [ ] Homing reserve prompt and the transfer confirmation

## Tarsis

- [ ] Objective: "Come about for Tarsis. Comms, request generator support and docking clearance before we approach."
- [ ] Tarsis generator acceptance and docking clearance
- [ ] Resupply: "Tarsis Control: resupply authorized and the generator governor is cleared."
- [ ] Objective after resupply: "Resupply complete. Stand by for Dillon to begin the Engineering shakedown."

## Engineering shakedown

- [ ] Start block — three station-addressed lines, renders across the newline
      breaks (`\n`) as separate lines and not as one run-on paragraph
- [ ] DAMCON rally-point instruction
- [ ] The crew-welfare speech ("Take care of your crew when the pressure is low...")
- [ ] Controlled overload instruction — including the bonus line:
      "Quarters, mess, and gym each earn a separate bonus."
      **Design question for you:** this now states the mechanic plainly. Is that
      the right level of hand-holding, or should it stay vaguer?
- [ ] Damage-logged message
- [ ] Preset instruction — the "Press S ... then press 2" console keys are
      **unverified by me**. Confirm those are the actual keys in your build.
- [ ] Completion: "...we will put a training drone in the water for you."

## Drone drill

- [ ] "Training drone standing by. Science, scan the contact; ..."
- [ ] "Drone away. Science, scan the contact. ..."
- [ ] Hail response: "Training drone acknowledges. Transponder reads TSN training contact, no weapons free."
- [ ] Fire authorization: "You are cleared to fire. Weapons, go to manual targeting..."
- [ ] Unauthorized-fire reset copy
- [ ] Premature-destruction reset copy
- [ ] Ceasefire: "...Comms, confirm it with Dillon."
- [ ] Cultural packet: "Comms, one more thing before we hand you back..."
- [ ] Direct Scenario bypass: "Captain has elected to skip the gunnery drills. Nothing is held against the crew for it."

---

# 4. Known-imperfect, deliberately left alone

- **GM spike objective text** still reads "GM target spike active. Science scan,
  Comms hail, Weapons select, then test subsystem damage/destruction evidence."
  It is dev-facing and it *does* broadcast to players — but only in GM Test Mode,
  so a real session never sees it. Left as-is because the GM needs to know what
  state they are in. Say the word if you want it neutralised.

- **Test-instrumentation text in the Comms hail and two Science scan blocks** is
  still present. This is the pre-existing deferred item in
  `SLICE06_VERIFICATION.md` Acceptance Not Covered — it must land before this
  spike's text is reused as a Drone 01/02 template. Not touched here.

- **Two test assertions intentionally still check the OLD copy.**
  `SLICE04_VERIFICATION.md` quotes the copy that was live during its smoke, and
  the live-smoke log is append-only. Those assertions carry a comment saying they
  track the historical record. Do not "fix" them to match current copy.

---

# 5. Slice 06 Phase B is still open

This branch did **not** close Phase B. The exit criteria are in
`tests/SLICE06_VERIFICATION.md`. Phase B still needs the crewed run of
`tests/SLICE06_PHASE_B_PLAYTEST_WORKSHEET.md`, and the worksheet's copy
expectations now differ from the runtime — for example ACT1-019 quotes the old
reset text.

- [ ] **Decide:** update the worksheet's quoted strings to the new copy before
      the Phase B run, or accept that those checks are matched on meaning rather
      than exact wording. Recommend updating it, so a check is a real comparison.

---

# 6. Reporting back

For anything that fails, the useful shape is:

```text
what you did:
what you expected:
what you saw:
trace lines:
```

If a message does not render, the trace tells you whether the handler ran. A
handler that ran with no visible output is the `(unknown)` sender problem from
section 2, not a copy problem, and it is worth stopping for.
