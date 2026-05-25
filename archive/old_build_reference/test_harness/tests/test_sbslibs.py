import os
import json


def test_story_json_exists():
    assert os.path.isfile("story.json")


def test_sbslib_entries_exist():
    with open("story.json", "r") as f:
        data = json.load(f)
    assert "sbslib" in data
    for lib in data.get("sbslib", []):
        path = os.path.join("__lib__", lib)
        assert os.path.isfile(path), f"Missing library listed in story.json: {path}"
