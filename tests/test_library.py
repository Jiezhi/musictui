import pytest
import os
import tempfile
from pathlib import Path
from src.library import Library
from src.models import Track


def test_library_initialization(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))
    tracks = library.get_all_tracks()
    assert tracks == []


def test_library_get_total_count(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))
    assert library.get_total_count() == 0


def test_library_save_and_get_track(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))

    track = Track(
        file_path="/test/song.mp3",
        title="Test Song",
        artist="Test Artist",
        album="Test Album",
        duration=180.0,
    )

    library._save_track(track)

    tracks = library.get_all_tracks()
    assert len(tracks) == 1
    assert tracks[0].title == "Test Song"
    assert tracks[0].artist == "Test Artist"


def test_library_get_track_by_id(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))

    track = Track(file_path="/test/song.mp3", title="Test Song")
    library._save_track(track)

    found = library.get_track_by_id(track.id)
    assert found is not None
    assert found.title == "Test Song"


def test_library_get_track_by_id_not_found(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))

    found = library.get_track_by_id(999)
    assert found is None


def test_library_search(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))

    track1 = Track(file_path="/test/song1.mp3", title="Hello World", artist="Artist A")
    track2 = Track(file_path="/test/song2.mp3", title="Goodbye", artist="Artist B")
    library._save_track(track1)
    library._save_track(track2)

    results = library.search("Hello")
    assert len(results) == 1
    assert results[0].title == "Hello World"


def test_library_search_by_artist(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))

    track = Track(file_path="/test/song.mp3", title="Song", artist="UniqueArtist")
    library._save_track(track)

    results = library.search("UniqueArtist")
    assert len(results) == 1
    assert results[0].artist == "UniqueArtist"


def test_library_search_no_results(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))

    track = Track(file_path="/test/song.mp3", title="Song", artist="Artist")
    library._save_track(track)

    results = library.search("nonexistent")
    assert len(results) == 0


def test_library_get_all_tracks_with_pagination(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))

    for i in range(100):
        track = Track(file_path=f"/test/song{i}.mp3", title=f"Song {i}")
        library._save_track(track)

    page1 = library.get_all_tracks(offset=0, limit=10)
    assert len(page1) == 10

    page2 = library.get_all_tracks(offset=50, limit=10)
    assert len(page2) == 10

    all_tracks = library.get_all_tracks()
    assert len(all_tracks) == 100
