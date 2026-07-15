import pytest

from project_pilot.artist_profile import load_profile


def test_load_profile(data_dir):
    profile = load_profile(data_dir, "top")
    assert profile.name == "Twenty One Pilots"
    assert profile.sole_writer is True
    assert "faith and doubt" in profile.themes
    assert any(era.name == "lore" for era in profile.eras)


def test_load_profile_missing_artist(data_dir):
    with pytest.raises(FileNotFoundError):
        load_profile(data_dir, "not-a-real-artist")


def test_as_context_block_includes_key_fields(data_dir):
    profile = load_profile(data_dir, "top")
    block = profile.as_context_block()
    assert "Twenty One Pilots" in block
    assert "AVOID" in block  # anti-themes should be flagged as such
    assert "Dema" in block  # mythology notes should come through
