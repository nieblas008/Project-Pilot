"""Shared fixtures for the project_pilot test suite.

The real embedder (sentence-transformers) pulls in torch and downloads a
model, which is overkill for testing plumbing. `fake_embedder` replaces
project_pilot.retrieval._embed with a tiny deterministic bag-of-words
vectorizer that's good enough to prove retrieval ranks by relevance.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from project_pilot import retrieval

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

_VOCAB = ["identity", "doubt", "faith", "hope", "chorus", "verse", "bridge", "placeholder"]


def _fake_embed(texts: list[str]) -> np.ndarray:
    vectors = []
    for text in texts:
        lowered = text.lower()
        vec = np.array([lowered.count(word) for word in _VOCAB], dtype=np.float32)
        norm = np.linalg.norm(vec)
        vectors.append(vec / norm if norm > 0 else vec)
    return np.asarray(vectors, dtype=np.float32)


@pytest.fixture
def fake_embedder(monkeypatch):
    """Stub out the real (heavy) embedder with a deterministic fake one."""
    monkeypatch.setattr(retrieval, "_embed", _fake_embed)
    return _fake_embed


@pytest.fixture
def data_dir() -> Path:
    return DATA_DIR
