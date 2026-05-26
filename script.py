from datetime import datetime, timezone
from pathlib import Path
import os
import sys
import traceback


MISSION_ROOT = Path(__file__).resolve().parent
SLICE01_SMOKE_MARKER_TEXT = (
    "Khovan Reach Slice 01A playable bootstrap loaded. Scene 1 initialized."
)
SLICE01_SMOKE_MARKER_PATH = MISSION_ROOT / "tests" / "live_smoke_last_bootstrap.txt"
KHOVAN_STARTUP_TRACE_PATH = MISSION_ROOT / "tests" / "live_startup_trace.txt"


def write_khovan_startup_trace(message):
    KHOVAN_STARTUP_TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with KHOVAN_STARTUP_TRACE_PATH.open("a", encoding="utf-8") as trace_file:
        trace_file.write(f"{timestamp} {message}\n")
        trace_file.flush()
        os.fsync(trace_file.fileno())


write_khovan_startup_trace("[KHOVAN EARLY 001] script.py entered")
write_khovan_startup_trace("[KHOVAN EARLY 002] before sbs_utils import")

try:
    import sbslibs
    from sbs_utils.handlerhooks import *
    from sbs_utils.gui import Gui
    from sbs_utils.mast.maststorypage import StoryPage
    from sbs_utils.mast.mast import Mast
    from sbs_utils.mast.mast_globals import MastGlobals

    MastGlobals.globals["script"] = sys.modules.get("script")
    write_khovan_startup_trace("[KHOVAN EARLY 003] after sbs_utils import")


    def write_slice01_live_smoke_marker(client_id):
        if client_id != 0:
            return

        SLICE01_SMOKE_MARKER_PATH.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).isoformat()
        SLICE01_SMOKE_MARKER_PATH.write_text(
            "\n".join(
                [
                    f"timestamp_utc={timestamp}",
                    SLICE01_SMOKE_MARKER_TEXT,
                    "mission_phase=act_1",
                    "current_scene=1",
                    "dillon_clip_1_status=stubbed",
                    "artemis_player_ship_status=initialized_by_reference_pattern",
                    "scene_1_runtime_presence=artemis_player_ship_and_dillon_stub",
                    "client_start_page=LegendaryMissions.server_console/client_main",
                    "entry_chain=story.json -> script.py -> story.mast -> LegendaryMissions.server_console -> scripts/main.mast @map/khovan_reach -> khovan_reach_slice01_entry",
                    "",
                ]
            ),
            encoding="utf-8",
        )


    class KhovanReachStoryPage(StoryPage):
        story_file = "story.mast"

        def start_story(self, client_id):
            try:
                write_khovan_startup_trace("[KHOVAN EARLY 006] before story.mast load/handoff")
                super().start_story(client_id)
                write_khovan_startup_trace("[KHOVAN EARLY 007] after story.mast load/handoff")
            except Exception as e:
                write_khovan_startup_trace(
                    f"[KHOVAN EARLY EXCEPTION] {type(e).__name__}: {e}\n{traceback.format_exc()}"
                )
                raise


    Mast.include_code = True

    write_khovan_startup_trace("[KHOVAN EARLY 004] before reference StoryPage registration")
    Gui.server_start_page_class(KhovanReachStoryPage)
    Gui.client_start_page_class(KhovanReachStoryPage)
    write_khovan_startup_trace("[KHOVAN EARLY 005] after reference StoryPage registration")
except Exception as e:
    write_khovan_startup_trace(
        f"[KHOVAN EARLY EXCEPTION] {type(e).__name__}: {e}\n{traceback.format_exc()}"
    )
    raise
