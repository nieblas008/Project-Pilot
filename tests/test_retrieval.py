from project_pilot.corpus import load_corpus
from project_pilot.retrieval import CorpusIndex


def test_build_index_shape(data_dir, fake_embedder):
    songs = load_corpus(data_dir / "artists" / "top" / "corpus")
    index = CorpusIndex.build(songs)
    assert index.vectors.shape[0] == len(songs)


def test_save_and_load_round_trip(data_dir, fake_embedder, tmp_path):
    songs = load_corpus(data_dir / "artists" / "top" / "corpus")
    index = CorpusIndex.build(songs)

    index.save(tmp_path / "index")
    reloaded = CorpusIndex.load(tmp_path / "index")

    assert len(reloaded.songs) == len(songs)
    assert reloaded.vectors.shape == index.vectors.shape


def test_retrieve_ranks_by_relevance(data_dir, fake_embedder):
    songs = load_corpus(data_dir / "artists" / "top" / "corpus")
    index = CorpusIndex.build(songs)

    results = index.retrieve("faith and hope", top_k=2)
    assert results[0].id == "_sample-002"  # the faith/doubt/hope-themed sample


def test_retrieve_era_filter_excludes_non_matching(data_dir, fake_embedder):
    songs = load_corpus(data_dir / "artists" / "top" / "corpus")
    index = CorpusIndex.build(songs)

    assert index.retrieve("faith", top_k=5, era="nonexistent-era") == []
    assert index.retrieve("faith", top_k=5, era="sample") != []


def test_retrieve_respects_top_k(data_dir, fake_embedder):
    songs = load_corpus(data_dir / "artists" / "top" / "corpus")
    index = CorpusIndex.build(songs)

    assert len(index.retrieve("faith", top_k=1)) == 1
