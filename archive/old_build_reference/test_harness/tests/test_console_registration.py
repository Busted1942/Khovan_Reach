import sys
import types
import importlib
import os
import re
import pytest


def make_fake_gui():
    calls = {"server": False, "client": False}

    class FakeGui:
        @staticmethod
        def server_start_page_class(cls):
            calls["server"] = True

        @staticmethod
        def client_start_page_class(cls):
            calls["client"] = True

    return FakeGui, calls


def test_server_registration(monkeypatch):
    FakeGui, calls = make_fake_gui()
    # Install fake modules explicitly so import order does not interfere.
    sys.modules['sbs_utils'] = types.ModuleType('sbs_utils')
    sys.modules['sbs_utils.handlerhooks'] = types.ModuleType('sbs_utils.handlerhooks')
    sys.modules['sbs_utils.gui'] = types.ModuleType('sbs_utils.gui')
    sys.modules['sbs_utils.gui'].Gui = FakeGui
    sys.modules['sbs_utils.mast.maststorypage'] = types.ModuleType('sbs_utils.mast.maststorypage')
    sys.modules['sbs_utils.mast.maststorypage'].StoryPage = object
    sys.modules['sbs_utils.mast.mast'] = types.ModuleType('sbs_utils.mast.mast')
    sys.modules['sbs_utils.mast.mast'].Mast = types.SimpleNamespace(include_code=False)

    import script
    importlib.reload(script)

    assert calls['server'], "Server start page was not registered"


@pytest.mark.parametrize('console', ['gamemaster', 'science', 'weapons', 'engineering', 'comms', 'helm'])
def test_console_registration_heuristic(console):
    root = os.path.dirname(os.path.dirname(__file__))
    # Heuristic 1: gamemaster -> settings.yaml contains GAMEMASTER
    if console == 'gamemaster':
        settings = os.path.join(root, 'settings.yaml')
        assert os.path.isfile(settings), 'settings.yaml missing'
        with open(settings, 'r', encoding='utf-8') as f:
            txt = f.read()
        assert re.search(r'^GAMEMASTER\s*:', txt, re.M), 'GAMEMASTER section missing in settings.yaml'
        return

    # Heuristic 2: other consoles -> presence of console-related tokens in scripts/main.mast
    mast = os.path.join(root, 'scripts', 'main.mast')
    assert os.path.isfile(mast), 'scripts/main.mast missing'
    with open(mast, 'r', encoding='utf-8') as f:
        txt = f.read()
    assert console in txt, f"Console token '{console}' not found in scripts/main.mast"
