"""End-to-end tests for player controls"""

import pytest
import os
from src.models import Track, PlayerState, PlayMode


@pytest.mark.asyncio
async def test_player_initial_state():
    """Test that player starts with correct initial state"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        assert app.player.state == PlayerState.STOPPED
        assert app.player.volume == 0.7
        assert app.player.play_mode == PlayMode.LOOP
        assert len(app.player.queue) == 0


@pytest.mark.asyncio
async def test_player_add_to_queue():
    """Test adding tracks to queue"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        track = Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Test Song")
        app.player.add_to_queue(track)
        
        assert len(app.player.queue) == 1
        assert app.player.queue[0].title == "Test Song"


@pytest.mark.asyncio
async def test_player_add_to_queue_front():
    """Test adding track to front of queue"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        track1 = Track(id=1, file_path="/test1.mp3", title="Song 1")
        track2 = Track(id=2, file_path="/test2.mp3", title="Song 2")
        
        app.player.add_to_queue(track1)
        app.player.add_to_queue_front(track2)
        
        assert len(app.player.queue) == 2
        assert app.player.queue[0].title == "Song 2"
        assert app.player.queue[1].title == "Song 1"


@pytest.mark.asyncio
async def test_player_clear_queue():
    """Test clearing the queue"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        track = Track(id=1, file_path="/test.mp3", title="Test")
        app.player.add_to_queue(track)
        app.player.clear_queue()
        
        assert len(app.player.queue) == 0
        assert app.player.current_index == -1


@pytest.mark.asyncio
async def test_player_get_current_track():
    """Test getting current track"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # No track playing
        assert app.player.get_current_track() is None
        
        # Add track and play
        track = Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Test")
        app.player.add_to_queue(track)
        app.player.play(track)
        
        current = app.player.get_current_track()
        assert current is not None
        assert current.title == "Test"


@pytest.mark.asyncio
async def test_player_volume_limits():
    """Test volume limits are enforced"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Test upper limit
        app.player.set_volume(1.5)
        assert app.player.volume == 1.0
        
        # Test lower limit
        app.player.set_volume(-0.5)
        assert app.player.volume == 0.0
        
        # Test normal value
        app.player.set_volume(0.5)
        assert app.player.volume == 0.5


@pytest.mark.asyncio
async def test_player_play_mode_cycle():
    """Test cycling through play modes"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Default is LOOP
        assert app.player.play_mode == PlayMode.LOOP
        
        # Change to SHUFFLE
        app.player.set_play_mode(PlayMode.SHUFFLE)
        assert app.player.play_mode == PlayMode.SHUFFLE
        
        # Change to SINGLE
        app.player.set_play_mode(PlayMode.SINGLE)
        assert app.player.play_mode == PlayMode.SINGLE
        
        # Back to LOOP
        app.player.set_play_mode(PlayMode.LOOP)
        assert app.player.play_mode == PlayMode.LOOP


@pytest.mark.asyncio
async def test_player_queue_navigation():
    """Test navigating through queue"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        tracks = [
            Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Song 1"),
            Track(id=2, file_path="tests/e2e/fixtures/test.mp3", title="Song 2"),
            Track(id=3, file_path="tests/e2e/fixtures/test.mp3", title="Song 3"),
        ]
        
        for track in tracks:
            app.player.add_to_queue(track)
        
        # Start playing first track
        app.player.play(tracks[0])
        await pilot.pause()
        
        assert app.player.current_index == 0
        
        # Next track
        app.player.next()
        await pilot.pause()
        assert app.player.current_index == 1
        
        # Previous track
        app.player.previous()
        await pilot.pause()
        assert app.player.current_index == 0


@pytest.mark.asyncio
async def test_player_queue_wrap_around():
    """Test queue navigation wraps around"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        tracks = [
            Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Song 1"),
            Track(id=2, file_path="tests/e2e/fixtures/test.mp3", title="Song 2"),
        ]
        
        for track in tracks:
            app.player.add_to_queue(track)
        
        app.player.play(tracks[0])
        await pilot.pause()
        
        # Go to next (wraps to beginning when in loop mode after playing)
        app.player.next()
        await pilot.pause()
        assert app.player.current_index == 1
        
        # Go previous (should wrap to last)
        app.player.current_index = 0
        app.player.previous()
        await pilot.pause()
        assert app.player.current_index == 1  # wraps to last track
