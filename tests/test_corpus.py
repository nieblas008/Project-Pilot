from project_pilot.corpus import load_corpus


def test_load_corpus(data_dir):
    songs = load_corpus(data_dir / "artists" / "top" / "corpus")
    assert len(songs) == 2
    ids = {song.id for song in songs}
    assert ids == {"_sample-001", "_sample-002"}


def test_song_full_text_includes_sections_and_themes(data_dir):
    songs = load_corpus(data_dir / "artists" / "top" / "corpus")
    song = next(s for s in songs if s.id == "_sample-001")
    text = song.full_text()
    assert song.title in text
    assert "identity" in text  # from the themes list
    assert "[verse]" in text
    assert "[chorus]" in text
