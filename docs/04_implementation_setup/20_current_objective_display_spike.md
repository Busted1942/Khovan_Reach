# KHOVAN REACH — CURRENT OBJECTIVE DISPLAY SPIKE

Version: 1.0
Status: Implementation spike requirement
Purpose: Capture the unfinished work from the prior build: keeping the current drill goal visible as persistent left/mid-screen static text while preserving overlay and Comms archive behavior.

---

# 1. Decision

Persistent current-goal display should be treated as its own implementation spike.

It should not block the mission skeleton.

It should be built before the full Act I drill sequence, because Drill Two and the shakedown flow rely heavily on step-by-step instruction.

---

# 2. Source Basis from Old MAST Files

The old implementation already had a working text prompt pattern:

- character/instructor messages used gui_info_panel_send_message
- objective messages used khovan_reach_objective_text
- messages appeared as timed GUI info-panel packets
- messages used history=True
- some messages were also sent through comms_receive or comms_broadcast
- dev jump summaries used the same objective message wrapper

That pattern worked for timed prompts.

It did not yet provide a true static current-goal display.

---

# 3. Current v2.2 Requirement

The current architecture requires:

- training text displays through the temporary upper-left lifeform overlay
- training text echoes into the Comms archive
- runtime drives normal flow
- Comms can jump back to previous messages
- player-facing debug/admin controls remain hidden

This spike adds an implementation enhancement:

- current objective remains visible as persistent left/mid-screen or closest supported static display

If Cosmos/MAST cannot support true static left/mid-screen text, the fallback is a managed objective heartbeat using the known GUI info-panel pattern.

---

# 4. Functional Requirement

Create a central current-objective system.

It should support:

- setting the current objective
- replacing the current objective
- clearing the current objective
- echoing each objective update to the Comms archive
- showing the current objective to all player GUIs
- showing richer state in the GM/admin panel
- invalidating stale objectives after story jumps
- surviving normal prompt traffic without being overwritten by ordinary dialogue

---

# 5. Proposed State Variables

Add current-objective state:

- current_objective_id
- current_objective_title
- current_objective_body
- current_objective_step
- current_objective_owner
- current_objective_mode
- current_objective_visible
- current_objective_run_id
- current_objective_updated_at
- current_objective_archive_id

Suggested owner values:

- all
- captain
- helm
- weapons
- engineering
- science
- comms
- gm

Suggested mode values:

- training
- mission
- warning
- recovery
- debug

---

# 6. Preferred Architecture

Do not call GUI message functions directly from every scene.

Create a message/objective router.

Suggested fresh module:

- scripts/systems/message_overlay.mast
- scripts/systems/comms_archive.mast
- scripts/systems/current_objective_display.mast

Suggested labels:

- khovan_message_send_training
- khovan_message_send_character
- khovan_message_send_command
- khovan_current_objective_set
- khovan_current_objective_clear
- khovan_current_objective_refresh
- khovan_current_objective_heartbeat
- khovan_comms_archive_append

---

# 7. Display Modes to Test

## Mode A — True static display

Preferred if Cosmos/MAST exposes a supported persistent text UI.

Requirements:

- visible until replaced or cleared
- appears in left/mid-screen or closest acceptable objective area
- does not spam message history
- can be updated by story jumps and drill steps
- visible to all relevant player GUIs
- hidden from enemy/irrelevant interfaces if applicable

Unknown:
- exact MAST/Cosmos API support needs verification.

## Mode B — Managed info-panel heartbeat

Fallback using old working pattern.

Behavior:

- call gui_info_panel_send_message with the current objective
- use a moderate or long display time
- refresh the same objective periodically
- use current_objective_run_id to prevent stale refreshes
- avoid flooding Comms history by archiving only on objective changes, not every heartbeat

This is not as clean as true static text, but it is more likely to work because the old prompt pattern already used GUI info-panel messages.

## Mode C — Comms archive only plus timed overlay

Minimum fallback.

Behavior:

- show objective as timed overlay
- echo to Comms archive
- rely on Comms to recall prior objective messages

This satisfies current v2.2 baseline but not the desired static-goal enhancement.

---

# 8. Run ID Requirement

Every objective display loop must use run ID guarding.

When a new objective is set:

- increment current_objective_run_id
- write current objective state
- display objective
- append one Comms archive entry
- start or refresh heartbeat if using fallback mode

When a story jump occurs:

- increment current_objective_run_id
- clear old objective
- set jump preset objective
- prevent old heartbeat from redisplaying stale text

---

# 9. Archive Rule

Every objective change should echo once into the Comms archive.

Do not echo every heartbeat refresh.

Required archive metadata:

- timestamp if available
- objective_id
- title
- body
- source
- scene
- step
- mode

Comms should be able to review previous objective messages.

---

# 10. GM Panel Rule

GM should see:

- current objective
- current objective run ID
- last objective update time
- whether heartbeat/static mode is active
- last Comms archive echo
- any stale-objective warnings

Players should not see debug metadata.

---

# 11. Acceptance Tests

OBJ-001:
- Set objective.
- Objective appears to all player GUIs.

OBJ-002:
- Objective echoes once into Comms archive.

OBJ-003:
- Objective remains visible for at least 60 seconds or until explicitly replaced.

OBJ-004:
- Replace objective.
- Old objective disappears or is superseded.
- New objective appears.

OBJ-005:
- Heartbeat mode does not spam Comms archive.

OBJ-006:
- Story jump invalidates old objective.
- Old objective does not reappear.

OBJ-007:
- Ordinary Dillon/Anderson/text prompt does not permanently erase current objective.

OBJ-008:
- GM panel shows objective debug state.
- Player consoles do not show debug state.

OBJ-009:
- Clear objective removes or suppresses current display.

OBJ-010:
- Fallback mode is documented if true static display is not supported.

---

# 12. Act I Use Cases

Scene 1:
- "Comms: request departure clearance from Kestrel."

After launch-envelope exit:
- "Proceed to Tarsis under generator-output governor."

Tarsis gate:
- "Comms: request homing-torpedo priority, generator acceptance support, and docking clearance."

Engineering shakedown:
- "Engineering: set impulse 0 and warp 200."

Stationary drone drill:
- "Helm and Weapons: hold Drone 01 at 1-2 km with Weapons locked."

Authorization hold:
- "Hold range and lock for 15 seconds. Do not fire."

Controlled disable:
- "Weapons: disable Drone 01 Weapons array only. Stop on disable cue."

Live-fire transfer:
- "Destroy Drone 02."

---

# 13. Implementation Warning

Do not over-invest in perfect static placement before verifying API support.

The acceptable fallback is:

- timed upper-left lifeform overlay
- Comms archive echo
- heartbeat objective refresh if needed

The strongest implementation path is:

1. centralize message routing
2. implement Comms archive echo
3. implement current-objective state
4. test true static display
5. fall back to heartbeat if true static is not available
