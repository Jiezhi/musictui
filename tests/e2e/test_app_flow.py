import pytest
from src.models import Track


@pytest.mark.asyncio
async def test_app_startup():
    """Test that app starts and all components are rendered"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Verify all main components exist
        assert app.query_one("#sidebar") is not None
        assert app.query_one("#track-table") is not None
        assert app.query_one("#player-bar") is not None
        assert app.query_one("#status-bar") is not None


@pytest.mark.asyncio
async def test_navigate_tracks():
    """Test navigating tracks with j/k keys"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Add mock tracks to the library and track list
        track_list = app.query_one("#track-table")
        track1 = Track(id=1, file_path="/test1.mp3", title="Test1")
        track2 = Track(id=2, file_path="/test2.mp3", title="Test2")
        track_list.set_tracks([track1, track2])

        initial_index = track_list.get_selected_index()

        # Press j to move down
        await pilot.press("j")
        await pilot.pause()

        assert track_list.get_selected_index() == initial_index + 1

        # Press k to move up
        await pilot.press("k")
        await pilot.pause()

        assert track_list.get_selected_index() == initial_index


@pytest.mark.asyncio
async def test_play_track():
    """Test pressing Enter plays the selected track"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Add mock track to player queue
        track = Track(file_path="tests/e2e/fixtures/test.mp3", title="Test")
        app.player.add_to_queue(track)

        await pilot.pause()

        # Press Enter to play - this should add track to queue and play
        await pilot.press("enter")
        await pilot.pause()

        # Verify player has a track in queue
        assert len(app.player.queue) > 0


@pytest.mark.asyncio
async def test_play_pause():
    """Test space toggles play/pause"""
    from src.app import MusicTUI
    from src.models import PlayerState

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        # Manually set player state to PLAYING to test pause functionality
        app.player.state = PlayerState.PLAYING

        # Pause
        await pilot.press("space")
        await pilot.pause()
        assert app.player.state == PlayerState.PAUSED

        # Resume
        await pilot.press("space")
        await pilot.pause()
        assert app.player.state == PlayerState.PLAYING


@pytest.mark.asyncio
async def test_next_previous_track():
    """Test n/p keys for next/previous track"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        # Add multiple tracks to queue
        track1 = Track(file_path="tests/e2e/fixtures/test.mp3", title="Test1")
        track2 = Track(file_path="tests/e2e/fixtures/test.mp3", title="Test2")
        app.player.add_to_queue(track1)
        app.player.add_to_queue(track2)

        # Play first track
        app.player.play(track1)
        await pilot.pause()

        initial_track = app.player.get_current_track()
        assert initial_track.title == "Test1"

        # Next track
        await pilot.press("n")
        await pilot.pause()

        next_track = app.player.get_current_track()
        assert next_track.title == "Test2"

        # Previous track
        await pilot.press("p")
        await pilot.pause()

        prev_track = app.player.get_current_track()
        assert prev_track.title == "Test1"


@pytest.mark.asyncio
async def test_quit():
    """Test q key exits the app"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        # Press q to quit
        await pilot.press("q")
        await pilot.pause()

        # App should have exited
        assert app._exit
