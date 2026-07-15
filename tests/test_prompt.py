from project_pilot.artist_profile import load_profile
from project_pilot.corpus import load_corpus
from project_pilot.prompt import build_system_prompt, build_user_prompt


def test_system_prompt_includes_artist_context(data_dir):
    profile = load_profile(data_dir, "top")
    system_prompt = build_system_prompt(profile)
    assert "Twenty One Pilots" in system_prompt
    assert "AVOID" in system_prompt


def test_user_prompt_includes_request_params_and_examples(data_dir):
    profile = load_profile(data_dir, "top")
    songs = load_corpus(data_dir / "artists" / "top" / "corpus")

    user_prompt = build_user_prompt(
        retrieved=songs,
        theme="identity",
        mood="anxious",
        structure=["verse", "chorus", "bridge"],
        era=None,
    )

    assert "Theme: identity" in user_prompt
    assert "Mood: anxious" in user_prompt
    assert "verse -> chorus -> bridge" in user_prompt
    assert songs[0].title in user_prompt
    del profile  # only needed to keep the fixture symmetry with the other test


def test_user_prompt_handles_no_retrieved_songs():
    user_prompt = build_user_prompt(
        retrieved=[], theme="hope", mood="quiet", structure=["verse"], era="lore"
    )
    assert "No reference examples were retrieved" in user_prompt
    assert "Target era: lore" in user_prompt
