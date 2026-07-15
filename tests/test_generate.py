import pytest

from project_pilot.generate import GenerationParseError, _extract_json


def test_extract_json_plain():
    text = '{"title": "Untitled", "sections": []}'
    assert _extract_json(text) == {"title": "Untitled", "sections": []}


def test_extract_json_fenced():
    text = '```json\n{"title": "Untitled", "sections": []}\n```'
    assert _extract_json(text) == {"title": "Untitled", "sections": []}


def test_extract_json_with_stray_prose():
    text = 'Sure, here is the song:\n{"title": "Untitled", "sections": []}\nHope that helps!'
    assert _extract_json(text) == {"title": "Untitled", "sections": []}


def test_extract_json_raises_on_garbage():
    with pytest.raises(GenerationParseError):
        _extract_json("this is not json at all")
