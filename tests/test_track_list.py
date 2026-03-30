import pytest
from unittest.mock import Mock, patch
from src.ui.track_list import TrackList
from src.models import Track
from types import SimpleNamespace


class TestTrackList:
    def test_initial_state(self):
        track_list = TrackList()
        assert track_list.tracks == []
        assert track_list.selected_index == 0
        assert track_list.total_count == 0

    def test_set_tracks_empty(self):
        track_list = TrackList()
        track_list.set_tracks([], 0)
        assert track_list.tracks == []
        assert track_list.selected_index == 0

    def test_set_tracks_with_data(self):
        track_list = TrackList()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        track_list.set_tracks(tracks, 2)
        assert len(track_list.tracks) == 2
        assert track_list.selected_index == 0

    def test_get_selected_track_empty(self):
        track_list = TrackList()
        assert track_list.get_selected_track() is None

    def test_get_selected_track_with_data(self):
        track_list = TrackList()
        tracks = [Track(id=1, title="Song 1", file_path="/a.mp3")]
        track_list.set_tracks(tracks, 1)
        assert track_list.get_selected_track() is not None
        assert track_list.get_selected_track().title == "Song 1"

    def test_move_up(self):
        track_list = TrackList()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        track_list.set_tracks(tracks, 2)
        track_list.selected_index = 1
        track_list.move_up()
        assert track_list.selected_index == 0

    def test_move_down(self):
        track_list = TrackList()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        track_list.set_tracks(tracks, 2)
        track_list.move_down()
        assert track_list.selected_index == 1

    def test_move_down_wraps_around(self):
        track_list = TrackList()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        track_list.set_tracks(tracks, 2)
        track_list.selected_index = 1
        track_list.move_down()
        assert track_list.selected_index == 0

    def test_append_tracks(self):
        track_list = TrackList()
        tracks1 = [Track(id=1, title="Song 1", file_path="/a.mp3")]
        track_list.set_tracks(tracks1, 1)

        tracks2 = [Track(id=2, title="Song 2", file_path="/b.mp3")]
        track_list.append_tracks(tracks2)

        assert len(track_list.tracks) == 2

    def test_set_load_more_callback(self):
        track_list = TrackList()
        called = []

        def callback():
            called.append(1)

        track_list.set_load_more_callback(callback)
        assert track_list._load_more_callback is not None

    def test_load_more_callback_triggered(self):
        track_list = TrackList()
        called = False

        def callback():
            nonlocal called
            called = True

        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(10)
        ]
        track_list.set_tracks(tracks, 20)
        track_list.set_load_more_callback(callback)

        track_list.load_more()
        assert called == True

    def test_load_more_not_triggered_when_all_loaded(self):
        track_list = TrackList()
        called = False

        def callback():
            nonlocal called
            called = True

        tracks = [Track(id=1, title="Song 1", file_path="/a.mp3")]
        track_list.set_tracks(tracks, 1)
        track_list.set_load_more_callback(callback)

        track_list.load_more()
        assert called == False

    def test_page_up(self):
        track_list = TrackList()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        track_list.set_tracks(tracks, 30)
        track_list.selected_index = 15
        track_list.page_up()
        assert track_list.selected_index == 0

    def test_page_up_at_top(self):
        track_list = TrackList()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        track_list.set_tracks(tracks, 30)
        track_list.selected_index = 5
        track_list.page_up()
        assert track_list.selected_index == 0

    def test_page_down(self):
        track_list = TrackList()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        track_list.set_tracks(tracks, 30)
        track_list.selected_index = 5
        track_list.page_down()
        assert track_list.selected_index == 25

    def test_page_down_at_bottom(self):
        track_list = TrackList()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        track_list.set_tracks(tracks, 30)
        track_list.selected_index = 25
        track_list.page_down()
        assert track_list.selected_index == 29

    def test_render_calls_refresh(self):
        track_list = TrackList()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        with patch.object(track_list, "refresh") as mock_refresh:
            track_list.set_tracks(tracks, 2)
            mock_refresh.assert_called()

    def test_move_down_triggers_refresh(self):
        track_list = TrackList()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        track_list.set_tracks(tracks, 2)
        with patch.object(track_list, "refresh") as mock_refresh:
            track_list.move_down()
            mock_refresh.assert_called()

    def test_move_up_triggers_refresh(self):
        track_list = TrackList()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        track_list.set_tracks(tracks, 2)
        track_list.selected_index = 1
        with patch.object(track_list, "refresh") as mock_refresh:
            track_list.move_up()
            mock_refresh.assert_called()

    def test_page_up_triggers_refresh(self):
        track_list = TrackList()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        track_list.set_tracks(tracks, 30)
        track_list.selected_index = 15
        with patch.object(track_list, "refresh") as mock_refresh:
            track_list.page_up()
            mock_refresh.assert_called()

    def test_page_down_triggers_refresh(self):
        track_list = TrackList()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        track_list.set_tracks(tracks, 30)
        with patch.object(track_list, "refresh") as mock_refresh:
            track_list.page_down()
            mock_refresh.assert_called()


def test_append_tracks_scrolls_to_selection_when_out_of_view():
    tl = TrackList()
    # Create 60 initial tracks
    initial_tracks = [
        Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(60)
    ]
    tl.set_tracks(initial_tracks, total_count=60)
    # Move selection well past the initial visible window
    tl.selected_index = 25
    # Simulate scroll position; height will fall back to default in code
    tl.scroll_y = 0

    # Prepare new tracks to append
    new_tracks = [
        Track(id=60 + i, title=f"Song {60 + i}", file_path=f"/{60 + i}.mp3")
        for i in range(5)
    ]

    with (
        patch.object(tl, "call_later") as mock_call_later,
        patch.object(tl, "update") as mock_update,
    ):
        tl.append_tracks(new_tracks)
        mock_update.assert_called()
        # Expect call_later to be invoked to schedule scroll AFTER rendering
        # (called from _render_content and then from append_tracks)
        assert mock_call_later.called
        # Verify scroll_to_selection is one of the callbacks passed to call_later
        call_args_list = [args[0] for args, _ in mock_call_later.call_args_list]
        assert tl.scroll_to_selection in call_args_list
