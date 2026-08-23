# KHOVAN REACH — NEXT-SESSION EXECUTION PLAN

Status: build-side plan, not design authority
Written: 2026-08-10
Purpose: let a cheaper model execute the next stretch without re-deriving context.

**Read first:** `AGENTS.md`, then `60_mast_api_cookbook.md` sections 4.1, 5.1,
5.2, 6.2, 8.1, 9.1, and **17** (working practices). Section 17 is the one that
prevents repeating this project's expensive mistakes.

---

# 1. Where the build actually stands

| Slice | State | What it needs |
|---|---|---|
| 01–05 | live-proven | — |
| 06 | Phase A accepted; Phase B **built, never live-smoked** | one crewed session |
| 07A | built, never run | live smoke |
| 07B | built, never run | live smoke |
| 08–16 | packets written, nothing built | 08 is next to build |

Three slices of runtime now sit unproven on top of each other. **That is the
main risk in this repo, and it is not solved by building a fourth.**

---

# 2. Do these first, in order

## 2.1 Operator live smoke — blocks everything else

Nothing below is worth doing until these run. Each has a stop condition.

1. **Slice 06 Phase B** — `tests/SLICE06_PHASE_B_PLAYTEST_WORKSHEET.md`, exit
   criteria in `tests/SLICE06_VERIFICATION.md`.
2. **JUMP-012 twice, count Halcyon contacts.** Two or more = **stop**; the
   cleanup helper is wrong and Slices 10/11/12 all reuse it. *(Retired
   2026-08-23: this gate originally named JUMP-013, a second preset for the
   same Halcyon-arrival beat. It was deleted as redundant with JUMP-012, which
   already spawns Halcyon and stages the same approach — see cookbook 17.12.
   013 is expected to be reissued to a future preset; do not read this line as
   still pointing at a live jump.)*
3. **Act II pivot** — does `[KHOVAN ACT2 002] mission_phase=act_2` fire without
   GM action?
4. **Lifeforms** — do Dillon and Anderson appear as Comms badges by name? Trace
   line `[KHOVAN LIB LIFEFORM] characters ready dillon=<id> anderson=<id>`.
   `dillon=0` means the fallback is carrying the mission and lifeforms are
   disconfirmed on this build.
5. **Proximity sweep** — fly toward Khovan Reach; does
   `[KHOVAN ACT2 SWEEP] signal resolved` fire?

## 2.2 Then, and only then

Merge Slice 06 to `master`, prune its children (ledger convention), and open
Slice 08 from `master` per its packet.

---

# 3. Slice 08 — the build task, when unblocked

Packet: `80_slice_packets_07_16.md`. Read it in full; the notes below only cover
what this session learned that the packet predates.

**Hessler should be a lifeform.** He is a person aboard Halcyon Drift, and
`scripts/lib/lifeform_helpers.mast` already does the work — call
`khovan_lifeform_create` with `lifeform_host_id: halcyon_object_id`. Do this
*after* live smoke confirms Dillon and Anderson render. If they did not, use the
fallback path and record the disconfirmation in cookbook 16.

**Reyes is the second candidate**, for DAMCON status reports during the cascade.
Same helper. Slice 09 owns the timer; Slice 08 only needs him to exist and speak.

**The cascade is a delayed task**, so it needs the cookbook 5.1 run-ID guard, and
`khovan_act2_invalidate_act1_timers` in `act2_pivot.mast` will need the new
counter added — `tests/test_act2_pivot_static.py` fails the build if you forget.

---

# 4. Standing rules that will bite otherwise

Each of these already cost a session here.

1. **`\n` only survives in a `shared` declaration.** Inline in `comms_receive()`
   or a `task_schedule()` dict it fails the parser. Cookbook 4.1.
2. **`data_set.get(name, index)`** — second argument is an index, never a
   default. The review gate lints this now.
3. **Stage explicit paths.** `git add <path>`, never `-A`. Verify `HEAD` before
   every commit. Cookbook 17.2.
4. **Prefer Edit over scripted regex.** Four files were damaged by regex edits in
   one day. Cookbook 17.1.
5. **Run both gates before committing:**
   ```bash
   python run_tests.py quick
   python tools/review_gate.py --base master
   ```
6. **Negative-control every new guard.** Break it once, confirm it fails, restore.
7. **Do not pin player copy in tests.** `tests/test_mission_text_contract.py`
   owns conventions; assert wiring instead.

---

# 5. Open design questions — operator only

Do not decide these in code.

1. **Halcyon's hull.** `tsn_warpster` is a TSN warship standing in for a Vesperan
   civilian hauler, chosen because it is the only hull proven to spawn here.
2. **Halcyon destroyed in Act II** has no recovery path; currently an error state.
3. **DAMCON idle buffs** — branch ledger Finding 3 was read from the *legacy*
   AI and needs re-answering against `grid_brains` before anyone acts on it.
4. **Act I fork advantage** — whether a Full Shakedown crew should reach Act III
   with faster DAMCON teams than a Direct Scenario crew.

---

# 6. What NOT to do

- **Do not build Slice 09+ before the live smoke in section 2.1.** Four unproven
  layers is worse than three, and Slice 09's DAMCON timer depends on
  `engineering_placement`, which 07B sets and nothing has verified.
- **Do not refactor `act1_generator_tarsis_gate.mast`.** `AGENTS.md` section 2:
  accepted debt with the deepest live-smoke history in the repo.
- **Do not edit `docs/01_design/` or `docs/02_content/`.** Route findings instead.
- **Do not promote an `[UNPROVEN]` tag without a live-smoke record.**
