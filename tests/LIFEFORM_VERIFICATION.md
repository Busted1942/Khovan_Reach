# Lifeform Verification — Dillon and Anderson as engine lifeforms

Goal: the mission's named characters exist as addressable engine lifeforms and speak as themselves, instead of borrowing a station's object id as message sender.

Not a slice record. The lifeform conversion (`c8a97c2`) cuts across Slices 01–07B, so it has no slice packet of its own; this record exists so cookbook section 16 has something to cite, per the cookbook's own promotion rule (section 15: promote a tag only when a verification doc records the live observation).

## Status

**partially-live-proven.** Creation is confirmed live. Everything downstream of creation — badges, path routes, and the send path — is still unproven. Status is reviewer-set per handoff protocol 4.3.

This split matters and must not be collapsed: "the lifeform objects exist" and "the lifeform feature works" are different claims, and only the first has evidence.

## Live observation — 2026-08-16

Unplanned observation. The operator started a Cosmos session at 12:52 UTC; the mission loaded and reached `BOOT 010`. Trace preserved in `tests/live_startup_trace.txt`.

```text
2026-08-16T12:56:41.127242+00:00 [KHOVAN LIB LIFEFORM] Master Sergeant Dillon created id=36028797018964039 roles=khovan_dillon path=//comms/khovan_dillon
2026-08-16T12:56:41.128745+00:00 [KHOVAN LIB LIFEFORM] Admiral Anderson created id=36028797018964041 roles=khovan_anderson path=//comms/khovan_anderson
2026-08-16T12:56:41.129777+00:00 [KHOVAN LIB LIFEFORM] characters ready dillon=36028797018964039 anderson=36028797018964041 status=lifeform_created
```

### What this proves

`prefab_spawn(prefab_lifeform_generic, {...})` followed by `to_object_list(role(lifeform_roles))` returns a real, addressable object in Khovan. Both ids are non-zero, distinct, and were read back from a role query — not assumed from the spawn call, which returns a task rather than an object (cookbook 16.3.1).

This is stronger evidence than a bare breadcrumb: the trace line carries a *value recovered from the engine*, not merely a marker proving a line was reached. Per `AGENTS.md` section 5, that distinction is the whole point.

It also means the station-borrow fallback in `khovan_lifeform_send` is **not** currently carrying the mission — the lifeform branch is the live path for every converted send.

### What this does NOT prove

- **Badge rendering.** Whether Dillon and Anderson appear by name in a player's internal Comms panel. Untested. Cookbook 16.3 says the badge query is `role("comms_badge") & linked_to(COMMS_SELECTED_ID, "onboard")`, so the badges should only appear when **Artemis herself is the selected contact** — a detail that made an early screenshot look like a failure when the console had Tarsis selected.
- **Path routes.** Whether `//comms/khovan_dillon` and `//comms/khovan_anderson` open when a badge is clicked.
- **The send path.** `khovan_lifeform_send`'s lifeform branch has **never executed** — there is not one `[KHOVAN LIB LIFEFORM SEND]` line anywhere in the trace history. Every Dillon message observed live so far predates the conversion or comes from `audio_runtime.mast`, which was never converted.
- **`comms_override` with a lifeform id as sender.** The converted sends pass `send_lifeform_id` where every proven call site passes a station/ship id. Untested shape.

## Files

- `scripts/lib/lifeform_helpers.mast` — creation, the shared send helper, both badge routes.
- Call sites: `act1_engineering_shakedown.mast`, `act1_drone_contact_fire.mast`, `act1_generator_tarsis_gate.mast`, `act2_pivot.mast`, `act2_halcyon_arrival.mast`.
- Not converted: `scripts/systems/audio_runtime.mast` (Dillon Clip 1 opening briefing) still calls `khovan_reach_send_safe_startup_message` directly.

## Acceptance Not Covered

- Everything under "What this does NOT prove" above.
- **Whether the prove-first order in cookbook 16.5 was followed. It was not.** That section requires proving badge render and path routes on a single throwaway lifeform *before* converting Dillon. Dillon and Anderson were both converted in `c8a97c2` without those steps. The conversion is defended by the fallback in `khovan_lifeform_send` rather than by prior proof, which is a weaker position than 16.5 asks for.
- **Whether a borrowed sender must be in range.** Open risk, cookbook 16.4.1. All nine Dillon fallbacks moved to `kestrel_yards_id` on 2026-08-16 to match corrected canon; if range gates delivery, that is worse in Act II, where Artemis ends up ~95 km from Kestrel. Latent while the lifeform ids stay non-zero.

## Next Action

Cheapest decisive check first:

1. **Select Artemis** (not a station) on a player Comms console. Do "Master Sergeant Dillon" and "Admiral Anderson" appear as badges, by name? This settles cookbook 16.5 steps 1–2 and costs about ten seconds.
2. Click Dillon's badge → "Request Current Instruction". Does the route open and print the live objective with header `Dillon: Instructor`?
3. Watch for the first-ever `[KHOVAN LIB LIFEFORM SEND] ... spoke as lifeform id=` line during Act I. Either that or `fell back to station-borrow path` is a pass for Act I continuity, but only the first proves the lifeform send path.
4. In Act II, at maximum distance from Kestrel, confirm whether a fallback-path Dillon message still renders — the 16.4.1 range question.

---

# Live smoke log (append-only)

**2026-08-16** — Creation confirmed live, ids non-zero (see above). Badges, routes, and the send path remain unobserved. No `[KHOVAN LIB LIFEFORM SEND]` line has ever been written.
