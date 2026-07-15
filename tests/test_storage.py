import json

from project_pilot.storage import save_generation


def test_save_generation_writes_labeled_file(tmp_path):
    result = {
        "artist": "Twenty One Pilots",
        "request": {"theme": "Identity!", "mood": "Anxious", "structure": ["verse"], "era": None},
        "generated": {"title": "Untitled", "sections": []},
        "filter_warnings": [],
        "model": "claude-sonnet-5",
    }

    path = save_generation(tmp_path, "top", result)

    assert path.exists()
    assert path.parent == tmp_path / "artists" / "top" / "generations"
    assert "identity-anxious" in path.name

    saved = json.loads(path.read_text())
    assert saved["artist"] == "Twenty One Pilots"
    assert "generated_at" in saved
