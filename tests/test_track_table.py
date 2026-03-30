import pytest
from textual.widgets import DataTable
from src.ui.widgets.track_table import TrackTable
from src.models import Track
from textual.app import App


class DummyApp(App):
    pass


class TestTrackTable:
    def test_initial_state(self):
        table = TrackTable()
        assert table.tracks == []

    @pytest.mark.asyncio
    async def test_set_tracks(self):
        app = DummyApp()
        async with app.run_test() as pilot:
            table = TrackTable()
            app.mount(table)
            await pilot.pause()
            tracks = [
                Track(id=1, title="Song 1", artist="Artist 1", file_path="/a.mp3"),
                Track(id=2, title="Song 2", artist="Artist 2", file_path="/b.mp3"),
            ]
            table.set_tracks(tracks)
            assert len(table.tracks) == 2
            assert table.cursor_row == 0

    @pytest.mark.asyncio
    async def test_get_selected_track(self):
        app = DummyApp()
        async with app.run_test() as pilot:
            table = TrackTable()
            app.mount(table)
            await pilot.pause()
            tracks = [Track(id=1, title="Song 1", file_path="/a.mp3")]
            table.set_tracks(tracks)
            track = table.get_selected_track()
            assert track is not None
            assert track.title == "Song 1"

    @pytest.mark.asyncio
    async def test_move_up(self):
        app = DummyApp()
        async with app.run_test() as pilot:
            table = TrackTable()
            app.mount(table)
            await pilot.pause()
            tracks = [
                Track(id=1, title="Song 1", file_path="/a.mp3"),
                Track(id=2, title="Song 2", file_path="/b.mp3"),
            ]
            table.set_tracks(tracks)
            table.cursor_coordinate = (1, 0)
            table.move_up()
            assert table.cursor_row == 0

    @pytest.mark.asyncio
    async def test_move_down(self):
        app = DummyApp()
        async with app.run_test() as pilot:
            table = TrackTable()
            app.mount(table)
            await pilot.pause()
            tracks = [
                Track(id=1, title="Song 1", file_path="/a.mp3"),
                Track(id=2, title="Song 2", file_path="/b.mp3"),
            ]
            table.set_tracks(tracks)
            table.move_down()
            assert table.cursor_row == 1

    @pytest.mark.asyncio
    async def test_track_selected_message(self):
        selected_messages: list[TrackTable.TrackSelected] = []

        class TestApp(DummyApp):
            def on_track_table_track_selected(self, event: TrackTable.TrackSelected):
                selected_messages.append(event)

        app = TestApp()
        async with app.run_test() as pilot:
            table = TrackTable()
            app.mount(table)
            await pilot.pause()
            tracks = [
                Track(id=1, title="Song 1", file_path="/a.mp3"),
                Track(id=2, title="Song 2", file_path="/b.mp3"),
            ]
            table.set_tracks(tracks)
            table.cursor_coordinate = (1, 0)
            event = DataTable.RowSelected(table, "1", False)
            table.on_data_table_row_selected(event)
            await pilot.pause()
            assert len(selected_messages) == 1
            assert selected_messages[0].track is not None
            assert selected_messages[0].track.title == "Song 2"
            assert selected_messages[0].index == 1

    @pytest.mark.asyncio
    async def test_track_double_clicked_message(self):
        double_clicked_messages: list[TrackTable.TrackDoubleClicked] = []

        class TestApp(DummyApp):
            def on_track_table_track_double_clicked(
                self, event: TrackTable.TrackDoubleClicked
            ):
                double_clicked_messages.append(event)

        app = TestApp()
        async with app.run_test() as pilot:
            table = TrackTable()
            app.mount(table)
            await pilot.pause()
            tracks = [
                Track(id=1, title="Song 1", file_path="/a.mp3"),
                Track(id=2, title="Song 2", file_path="/b.mp3"),
            ]
            table.set_tracks(tracks)
            table.cursor_coordinate = (0, 0)
            event = DataTable.RowSelected(table, "1", False)
            table.on_data_table_row_double_clicked(event)
            await pilot.pause()
            assert len(double_clicked_messages) == 1
            assert double_clicked_messages[0].track is not None
            assert double_clicked_messages[0].track.title == "Song 1"
            assert double_clicked_messages[0].index == 0
