from project_pilot.artist_profile import load_profile
from project_pilot.filters import anti_theme_check, canon_check


def test_anti_theme_check_flags_drift(data_dir):
    profile = load_profile(data_dir, "top")
    warnings = anti_theme_check(
        "this song is about money and partying all night", profile.anti_themes
    )
    assert warnings
    assert any("money" in w for w in warnings)


def test_anti_theme_check_is_quiet_on_theme(data_dir):
    profile = load_profile(data_dir, "top")
    warnings = anti_theme_check("this song is about identity and doubt", profile.anti_themes)
    assert warnings == []


def test_canon_check_is_currently_a_stub():
    # documents current behavior; see the TODO in filters.py for what this needs to become
    assert canon_check("anything", "some mythology notes") == []
