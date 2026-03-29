import pytest
from unittest.mock import Mock, patch
from src.ui.queue import Queue
from src.models import Track


class TestQueue:
    def test_initial_state(self):
        queue = Queue()
        assert queue.tracks == []
        assert queue.selected_index == 0

    def test_set_tracks(self):
        queue = Queue()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        queue.set_tracks(tracks)
        assert len(queue.tracks) == 2
        assert queue.selected_index == 0

    def test_move_up(self):
        queue = Queue()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        queue.set_tracks(tracks)
        queue.selected_index = 1
        queue.move_up()
        assert queue.selected_index == 0

    def test_move_down(self):
        queue = Queue()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        queue.set_tracks(tracks)
        queue.move_down()
        assert queue.selected_index == 1

    def test_page_up(self):
        queue = Queue()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        queue.set_tracks(tracks)
        queue.selected_index = 15
        queue.page_up()
        assert queue.selected_index == 0

    def test_page_up_at_top(self):
        queue = Queue()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        queue.set_tracks(tracks)
        queue.selected_index = 5
        queue.page_up()
        assert queue.selected_index == 0

    def test_page_down(self):
        queue = Queue()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        queue.set_tracks(tracks)
        queue.selected_index = 5
        queue.page_down()
        assert queue.selected_index == 25

    def test_page_down_at_bottom(self):
        queue = Queue()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        queue.set_tracks(tracks)
        queue.selected_index = 25
        queue.page_down()
        assert queue.selected_index == 29

    def test_get_selected_track(self):
        queue = Queue()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        queue.set_tracks(tracks)
        selected = queue.get_selected_track()
        assert selected is not None
        assert selected.title == "Song 1"

    def test_get_selected_track_empty(self):
        queue = Queue()
        assert queue.get_selected_track() is None

    def test_move_down_triggers_refresh(self):
        queue = Queue()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        queue.set_tracks(tracks)
        with patch.object(queue, "refresh") as mock_refresh:
            queue.move_down()
            mock_refresh.assert_called()

    def test_move_up_triggers_refresh(self):
        queue = Queue()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        queue.set_tracks(tracks)
        queue.selected_index = 1
        with patch.object(queue, "refresh") as mock_refresh:
            queue.move_up()
            mock_refresh.assert_called()

    def test_page_up_triggers_refresh(self):
        queue = Queue()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        queue.set_tracks(tracks)
        queue.selected_index = 15
        with patch.object(queue, "refresh") as mock_refresh:
            queue.page_up()
            mock_refresh.assert_called()

    def test_page_down_triggers_refresh(self):
        queue = Queue()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        queue.set_tracks(tracks)
        with patch.object(queue, "refresh") as mock_refresh:
            queue.page_down()
            mock_refresh.assert_called()
