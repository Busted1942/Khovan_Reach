import sys
import types


def test_import_script_with_minimal_mocks(monkeypatch):
    # Provide minimal sbs_utils modules to avoid heavy runtime imports
    fake_pkg = types.SimpleNamespace()
    fake_handlerhooks = types.SimpleNamespace()
    class FakeGui:
        @staticmethod
        def server_start_page_class(cls):
            return None

        @staticmethod
        def client_start_page_class(cls):
            return None

    fake_maststorypage = types.SimpleNamespace(StoryPage=object)
    fake_mast = types.SimpleNamespace(Mast=types.SimpleNamespace())

    sys.modules.setdefault('sbs_utils', fake_pkg)
    sys.modules.setdefault('sbs_utils.handlerhooks', fake_handlerhooks)
    sys.modules.setdefault('sbs_utils.gui', types.SimpleNamespace(Gui=FakeGui))
    sys.modules.setdefault('sbs_utils.mast.maststorypage', fake_maststorypage)
    sys.modules.setdefault('sbs_utils.mast.mast', fake_mast)

    # Importing should not raise
    import importlib
    import script
    importlib.reload(script)
    assert hasattr(script, 'Mast') or hasattr(script, 'cosmos_event_handler')
