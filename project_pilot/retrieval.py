"""Embedding-based retrieval over an artist's lyric corpus.

Implements the "Retrieval" stage of the Phase 1 pipeline described in
docs/research/ai-lyric-generation.md ("Pipeline sketch for Phase 1").

Storage is deliberately simple for a Phase 1 starting point: embeddings are
cached as a .npy matrix next to a metadata .json file, and retrieval is a
brute-force cosine similarity scan. See docs/architecture/system-design-notes.md
(Q4) for the longer-term plan to move this into a real vector DB
(Qdrant/LanceDB) once an artist's corpus outgrows a flat file — a few
hundred songs is well within what this brute-force approach can handle.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .corpus import Song, load_corpus

_MODEL_NAME = "all-MiniLM-L6-v2"  # small, fast, CPU-friendly sentence-transformers model
_model = None  # lazy-loaded singleton, so importing this module doesn't require torch


def _get_embedder():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def _embed(texts: list[str]) -> np.ndarray:
    embedder = _get_embedder()
    vectors = embedder.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return np.asarray(vectors, dtype=np.float32)


@dataclass
class CorpusIndex:
    songs: list[Song]
    vectors: np.ndarray  # shape (n_songs, dim), L2-normalized

    @classmethod
    def build(cls, songs: list[Song]) -> "CorpusIndex":
        texts = [song.full_text() for song in songs]
        vectors = _embed(texts)
        return cls(songs=songs, vectors=vectors)

    def save(self, index_dir: Path) -> None:
        index_dir.mkdir(parents=True, exist_ok=True)
        np.save(index_dir / "vectors.npy", self.vectors)
        (index_dir / "songs.json").write_text(
            json.dumps([song.model_dump() for song in self.songs], indent=2)
        )

    @classmethod
    def load(cls, index_dir: Path) -> "CorpusIndex":
        vectors = np.load(index_dir / "vectors.npy")
        raw_songs = json.loads((index_dir / "songs.json").read_text())
        songs = [Song(**raw) for raw in raw_songs]
        return cls(songs=songs, vectors=vectors)

    def retrieve(self, query: str, top_k: int = 5, era: str | None = None) -> list[Song]:
        pool_indices = [
            i for i, song in enumerate(self.songs) if era is None or song.era == era
        ]
        if not pool_indices:
            return []
        query_vec = _embed([query])[0]
        pool_vectors = self.vectors[pool_indices]
        scores = pool_vectors @ query_vec  # cosine similarity (vectors are pre-normalized)
        ranked = sorted(zip(pool_indices, scores), key=lambda pair: pair[1], reverse=True)
        return [self.songs[i] for i, _ in ranked[:top_k]]


def build_index_for_artist(data_dir: Path, artist_slug: str) -> CorpusIndex:
    corpus_dir = data_dir / "artists" / artist_slug / "corpus"
    songs = load_corpus(corpus_dir)
    if not songs:
        raise ValueError(
            f"No songs found in {corpus_dir}. Add song JSON files there before "
            f"indexing (see {corpus_dir / 'README.md'})."
        )
    index = CorpusIndex.build(songs)
    index.save(data_dir / "artists" / artist_slug / "index")
    return index


def load_index_for_artist(data_dir: Path, artist_slug: str) -> CorpusIndex:
    index_dir = data_dir / "artists" / artist_slug / "index"
    if not index_dir.exists():
        raise FileNotFoundError(
            f"No index found at {index_dir}. Run "
            f"`python -m project_pilot.cli index --artist {artist_slug}` first."
        )
    return CorpusIndex.load(index_dir)
