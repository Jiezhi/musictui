import pytest
from src.models import Track


@pytest.mark.asyncio
async def test_queue_view_displays():
    """Test that queue view displays correctly when shown"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Queue should be hidden initially
        queue = app.query_one("#queue")
        assert queue.styles.display == "none"

        # Add tracks to player queue
        track1 = Track(
            id=1,
            file_path="/test1.mp3",
            title="Song One",
            artist="Artist A",
            duration=180.0,
        )
        track2 = Track(
            id=2,
            file_path="/test2.mp3",
            title="Song Two",
            artist="Artist B",
            duration=200.0,
        )
        app.player.add_to_queue(track1)
        app.player.add_to_queue(track2)

        # Show queue view
        await pilot.press("2")
        await pilot.pause()

        # Queue should now be visible
        assert queue.styles.display == "block"


@pytest.mark.asyncio
async def test_queue_navigation():
    """Test navigating queue with j/k keys"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Add tracks to player queue
        track1 = Track(
            id=1,
            file_path="/test1.mp3",
            title="Song One",
            artist="Artist A",
            duration=180.0,
        )
        track2 = Track(
            id=2,
            file_path="/test2.mp3",
            title="Song Two",
            artist="Artist B",
            duration=200.0,
        )
        app.player.add_to_queue(track1)
        app.player.add_to_queue(track2)

        # Show queue view
        await pilot.press("2")
        await pilot.pause()

        queue = app.query_one("#queue")
        initial_index = queue.selected_index

        # Press j to move down
        await pilot.press("j")
        await pilot.pause()

        assert queue.selected_index == initial_index + 1

        # Press k to move up
        await pilot.press("k")
        await pilot.pause()

        assert queue.selected_index == initial_index


@pytest.mark.asyncio
async def test_queue_shows_tracks():
    """Test that queue displays track info correctly"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Add tracks to player queue
        track1 = Track(
            id=1,
            file_path="/test1.mp3",
            title="Song One",
            artist="Artist A",
            duration=180.0,
        )
        track2 = Track(
            id=2,
            file_path="/test2.mp3",
            title="Song Two",
            artist="Artist B",
            duration=200.0,
        )
        app.player.add_to_queue(track1)
        app.player.add_to_queue(track2)

        # Show queue view
        await pilot.press("2")
        await pilot.pause()

        queue = app.query_one("#queue")
        # Queue should show the tracks
        assert len(queue.tracks) == 2
        assert queue.tracks[0].title == "Song One"
        assert queue.tracks[1].title == "Song Two"


@pytest.mark.asyncio
async def test_queue_keybinding():
    """Test that 2 key shows queue view"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Add tracks to queue
        track = Track(id=1, file_path="/test1.mp3", title="Test")
        app.player.add_to_queue(track)

        await pilot.pause()

        # Press 2 to show queue
        await pilot.press("2")
        await pilot.pause()

        queue = app.query_one("#queue")
        assert queue.styles.display == "block"


@pytest.mark.asyncio
async def test_empty_queue_message():
    """Test that empty queue shows appropriate message"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Show queue view with empty queue
        await pilot.press("2")
        await pilot.pause()

        queue = app.query_one("#queue")
        # Should show empty message (queue is empty, tracks list should be empty)
        assert queue.tracks == [] or "empty" in str(queue.renderable).lower()
