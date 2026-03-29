import pytest
from unittest.mock import Mock, patch
from src.ui.search import Search
from src.models import Track


class TestSearch:
    def test_initial_state(self):
        search = Search()
        assert search.query == ""
        assert search.results == []
        assert search.selected_index == 0

    def test_set_results(self):
        search = Search()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        search.set_results(tracks)
        assert len(search.results) == 2
        assert search.selected_index == 0

    def test_append_char(self):
        search = Search()
        search.append_char("t")
        search.append_char("e")
        assert search.query == "te"

    def test_backspace(self):
        search = Search()
        search.append_char("t")
        search.append_char("e")
        search.backspace()
        assert search.query == "t"

    def test_clear(self):
        search = Search()
        search.append_char("test")
        search.clear()
        assert search.query == ""
        assert search.results == []

    def test_move_up(self):
        search = Search()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        search.set_results(tracks)
        search.selected_index = 1
        search.move_up()
        assert search.selected_index == 0

    def test_move_down(self):
        search = Search()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        search.set_results(tracks)
        search.move_down()
        assert search.selected_index == 1

    def test_page_up(self):
        search = Search()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        search.set_results(tracks)
        search.selected_index = 15
        search.page_up()
        assert search.selected_index == 0

    def test_page_up_at_top(self):
        search = Search()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        search.set_results(tracks)
        search.selected_index = 5
        search.page_up()
        assert search.selected_index == 0

    def test_page_down(self):
        search = Search()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        search.set_results(tracks)
        search.selected_index = 5
        search.page_down()
        assert search.selected_index == 25

    def test_page_down_at_bottom(self):
        search = Search()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        search.set_results(tracks)
        search.selected_index = 25
        search.page_down()
        assert search.selected_index == 29

    def test_get_selected_track(self):
        search = Search()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        search.set_results(tracks)
        selected = search.get_selected_track()
        assert selected is not None
        assert selected.title == "Song 1"

    def test_get_selected_track_empty(self):
        search = Search()
        assert search.get_selected_track() is None

    def test_move_down_triggers_refresh(self):
        search = Search()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        search.set_results(tracks)
        with patch.object(search, "refresh") as mock_refresh:
            search.move_down()
            mock_refresh.assert_called()

    def test_move_up_triggers_refresh(self):
        search = Search()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        search.set_results(tracks)
        search.selected_index = 1
        with patch.object(search, "refresh") as mock_refresh:
            search.move_up()
            mock_refresh.assert_called()

    def test_page_up_triggers_refresh(self):
        search = Search()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        search.set_results(tracks)
        search.selected_index = 15
        with patch.object(search, "refresh") as mock_refresh:
            search.page_up()
            mock_refresh.assert_called()

    def test_page_down_triggers_refresh(self):
        search = Search()
        tracks = [
            Track(id=i, title=f"Song {i}", file_path=f"/{i}.mp3") for i in range(30)
        ]
        search.set_results(tracks)
        with patch.object(search, "refresh") as mock_refresh:
            search.page_down()
            mock_refresh.assert_called()
