try:
    from datetime import datetime, timezone
    from pathlib import Path

    import sbslibs
    from sbs_utils.handlerhooks import *
    from sbs_utils.gui import Gui
    from sbs_utils.mast.maststorypage import StoryPage
    from sbs_utils.mast.mast import Mast


    SLICE01_SMOKE_MARKER_TEXT = (
        "Khovan Reach Slice 01 bootstrap loaded. Scene 1 initialized."
    )
    SLICE01_SMOKE_MARKER_PATH = (
        Path(__file__).resolve().parent / "tests" / "live_smoke_last_bootstrap.txt"
    )


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
                    "entry_chain=story.json -> script.py -> story.mast -> scripts/main.mast -> khovan_reach_slice01_entry",
                    "",
                ]
            ),
            encoding="utf-8",
        )


    class KhovanReachStoryPage(StoryPage):
        story_file = "story.mast"
        main_server = "khovan_reach_slice01_entry"
        main_client = "khovan_reach_slice01_client_entry"

        def start_story(self, client_id):
            super().start_story(client_id)
            write_slice01_live_smoke_marker(client_id)


    Mast.include_code = True

    Gui.server_start_page_class(KhovanReachStoryPage)
    Gui.client_start_page_class(KhovanReachStoryPage)
except Exception as e:
    message = e

    def cosmos_event_handler(sim, event):
        import sbs

        sbs.send_gui_clear(event.client_id, "")
        sbs.send_gui_text(
            event.client_id,
            "",
            "text",
            f"$text:sbs_utils runtime error^{message};",
            0,
            0,
            80,
            95,
        )
        sbs.send_gui_complete(event.client_id, "")
