import pytest
from src.models import Track, Playlist, PlayerState, PlayMode


class TestTrack:
    def test_track_display_name_with_artist_and_title(self):
        track = Track(title="Hello", artist="World", file_path="/test.mp3")
        assert track.display_name == "World - Hello"

    def test_track_display_name_with_title_only(self):
        track = Track(title="Hello", file_path="/test.mp3")
        assert track.display_name == "Hello"

    def test_track_display_name_no_title_uses_filename(self):
        track = Track(file_path="/path/to/song.mp3")
        assert track.display_name == "song"

    def test_track_display_name_empty_title_and_filename(self):
        track = Track()
        assert track.display_name == ""


class TestPlaylist:
    def test_playlist_default_track_ids(self):
        playlist = Playlist(name="Test")
        assert playlist.track_ids == []

    def test_playlist_with_track_ids(self):
        playlist = Playlist(name="Test", track_ids=[1, 2, 3])
        assert playlist.track_ids == [1, 2, 3]
