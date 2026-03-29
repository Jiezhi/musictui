import pytest
from src.library import Library
from src.models import Track


def test_parse_js_format():
    """Test parsing JS format song list"""
    library = Library(":memory:")
    js_content = """var list = [
      {name: "song1", artist: "artist1", url: "https://example.com/1.mp3", cover: "https://example.com/c1.png"},
      {name: "song2", artist: "artist2", url: "https://example.com/2.mp3"}
    ];"""

    tracks = library._parse_remote_content(js_content)

    assert len(tracks) == 2
    assert tracks[0].title == "song1"
    assert tracks[0].artist == "artist1"
    assert tracks[0].file_path == "https://example.com/1.mp3"
    assert tracks[0].cover == "https://example.com/c1.png"
    assert tracks[1].cover == ""


def test_parse_json_format():
    """Test parsing JSON format song list"""
    library = Library(":memory:")
    json_content = """[
      {"name": "song1", "artist": "artist1", "url": "https://example.com/1.mp3", "cover": "https://example.com/c1.png"},
      {"name": "song2", "artist": "artist2", "url": "https://example.com/2.mp3"}
    ]"""

    tracks = library._parse_remote_content(json_content)

    assert len(tracks) == 2
    assert tracks[0].title == "song1"
    assert tracks[0].artist == "artist1"
    assert tracks[0].file_path == "https://example.com/1.mp3"
    assert tracks[0].cover == "https://example.com/c1.png"
    assert tracks[1].cover == ""
