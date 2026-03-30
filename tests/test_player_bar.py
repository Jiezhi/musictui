import pytest
from src.ui.widgets.player_bar import PlayerBar


class TestPlayerBar:
    def test_initial_state(self):
        bar = PlayerBar()
        assert bar.current_track_title == "No track"

    def test_update_track(self):
        bar = PlayerBar()
        bar.update_track("Test Song", "Test Artist", 30.0, 180.0)
        assert bar.current_track_title == "Test Song"
        assert bar.current_track_artist == "Test Artist"
        assert bar.duration == 180.0

    def test_format_time(self):
        bar = PlayerBar()
        assert bar._format_time(65.0) == "1:05"
        assert bar._format_time(0.0) == "0:00"
