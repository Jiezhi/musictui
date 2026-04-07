"""End-to-end tests for enhanced player functionality"""

import pytest
import os
import pygame
from unittest.mock import patch, MagicMock
from src.models import Track, PlayerState, PlayMode


@pytest.mark.asyncio
async def test_player_seek_functionality():
    """Test seek functionality in E2E context"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Mock mixer for position tracking
        with patch("pygame.mixer") as mock_mixer:
            mock_mixer.music.get_pos.return_value = 5000  # 5 seconds
            mock_mixer.music.set_pos = MagicMock()
            mock_mixer.music.get_audio.return_value = MagicMock(length=180)

            # Add a track to queue
            track = Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Test Song")
            app.player.add_to_queue(track)
            app.player.play(track)

            await pilot.pause()

            # Test seeking
            app.player.seek(30.0)
            assert app.player.position == 30.0
            mock_mixer.music.set_pos.assert_called_with(30.0)


@pytest.mark.asyncio
async def test_player_position_tracking():
    """Test position tracking callback"""
    from src.app import MusicTUI

    callback_called = False
    last_position = 0.0

    def position_callback(position):
        nonlocal callback_called, last_position
        callback_called = True
        last_position = position

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Set up callback
        app.player.set_on_position_change(position_callback)

        # Mock mixer
        with patch("pygame.mixer") as mock_mixer:
            mock_mixer.music.get_pos.return_value = 3000  # 3 seconds
            mock_mixer.music.get_audio.return_value = MagicMock(length=180)

            # Play a track
            track = Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Test Song")
            app.player.add_to_queue(track)
            app.player.play(track)

            await pilot.pause()

            # Test that callback is set up correctly
            assert app.player._on_position_change is not None


@pytest.mark.asyncio
async def test_player_queue_management():
    """Test queue management operations"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Add multiple tracks
        tracks = [
            Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Song 1"),
            Track(id=2, file_path="tests/e2e/fixtures/test.mp3", title="Song 2"),
            Track(id=3, file_path="tests/e2e/fixtures/test.mp3", title="Song 3"),
        ]

        for track in tracks:
            app.player.add_to_queue(track)

        # Test removing from queue
        assert app.player.remove_from_queue(1)  # Remove Song 2
        assert len(app.player.queue) == 2
        assert app.player.queue[0].title == "Song 1"
        assert app.player.queue[1].title == "Song 3"

        # Test moving track in queue
        app.player.move_in_queue(0, 1)  # Move Song 1 to position 1
        assert app.player.queue[0].title == "Song 3"
        assert app.player.queue[1].title == "Song 1"


@pytest.mark.asyncio
async def test_player_toggle_pause():
    """Test toggle pause functionality"""
    from src.app import MusicTUI
    app = MusicTUI()
    async with app.run_test() as pilot:
        app = pilot.app

        # Play a track
        track = Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Test Song")
        app.player.add_to_queue(track)
        app.player.play(track)

        await pilot.pause()
        assert app.player.state == PlayerState.PLAYING

        # Toggle to pause
        app.player.toggle_pause()
        await pilot.pause()
        assert app.player.state == PlayerState.PAUSED

        # Toggle back to play
        app.player.toggle_pause()
        await pilot.pause()
        assert app.player.state == PlayerState.PLAYING


@pytest.mark.asyncio
async def test_player_error_handling():
    """Test error handling for invalid files"""
    from src.app import MusicTUI
    app = MusicTUI()
    async with app.run_test() as pilot:
        app = pilot.app

        # Mock mixer to raise error
        mock_pygame_mixer.music.load.side_effect = pygame.error("File not found")

        # Try to play non-existent file
        track = Track(id=1, file_path="/nonexistent.mp3", title="Nonexistent")
        app.player.add_to_queue(track)
        app.player.play(track)

        await pilot.pause()
        assert app.player.state == PlayerState.STOPPED


@pytest.mark.asyncio
async def test_player_shuffle_mode():
    """Test shuffle play mode"""
    from src.app import MusicTUI
    app = MusicTUI()
    async with app.run_test() as pilot:
        app = pilot.app

        # Add tracks
        tracks = [
            Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Song 1"),
            Track(id=2, file_path="tests/e2e/fixtures/test.mp3", title="Song 2"),
            Track(id=3, file_path="tests/e2e/fixtures/test.mp3", title="Song 3"),
        ]

        for track in tracks:
            app.player.add_to_queue(track)

        # Set shuffle mode
        app.player.set_play_mode(PlayMode.SHUFFLE)

        # Start playing
        app.player.play(tracks[0])
        await pilot.pause()
        original_index = app.player.current_index

        # Go to next track (should be different)
        app.player.next()
        await pilot.pause()

        assert app.player.current_index != original_index
        assert 0 <= app.player.current_index < len(app.player.queue)


@pytest.mark.asyncio
async def test_player_get_progress():
    """Test progress calculation"""
    from src.app import MusicTUI
    app = MusicTUI()
    async with app.run_test() as pilot:
        app = pilot.app

        # Add track with duration
        track = Track(
            id=1,
            file_path="tests/e2e/fixtures/test.mp3",
            title="Test Song",
            duration=180  # 3 minutes
        )
        app.player.add_to_queue(track)
        app.player.play(track)

        await pilot.pause()

        # Test progress at different positions
        app.player.position = 90.0  # Halfway through
        assert app.player.get_progress() == 0.5

        app.player.position = 0.0
        assert app.player.get_progress() == 0.0

        app.player.position = 180.0
        assert app.player.get_progress() == 1.0


@pytest.mark.asyncio
async def test_player_queue_length_checks():
    """Test queue length utility methods"""
    from src.app import MusicTUI
    app = MusicTUI()
    async with app.run_test() as pilot:
        app = pilot.app

        # Initially empty
        assert app.player.get_queue_length() == 0
        assert app.player.is_empty()

        # Add tracks
        track1 = Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Song 1")
        track2 = Track(id=2, file_path="tests/e2e/fixtures/test.mp3", title="Song 2")

        app.player.add_to_queue(track1)
        assert app.player.get_queue_length() == 1
        assert not app.player.is_empty()

        app.player.add_to_queue(track2)
        assert app.player.get_queue_length() == 2
        assert not app.player.is_empty()


@pytest.mark.asyncio
async def test_player_previous_with_error():
    """Test previous track error handling"""
    from src.app import MusicTUI
    app = MusicTUI()
    async with app.run_test() as pilot:
        app = pilot.app

        # Mock mixer to raise error
        mock_pygame_mixer.music.load.side_effect = pygame.error("File not found")

        # Add tracks
        tracks = [
            Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Song 1"),
            Track(id=2, file_path="tests/e2e/fixtures/test.mp3", title="Song 2"),
        ]

        for track in tracks:
            app.player.add_to_queue(track)

        # Start playing second track
        app.player.play(tracks[1])
        await pilot.pause()

        # Try to go to previous (will fail)
        app.player.previous()
        await pilot.pause()

        # Should be stopped
        assert app.player.state == PlayerState.STOPPED


@pytest.mark.asyncio
async def test_player_seek_with_duration():
    """Test seek behavior with track duration"""
    from src.app import MusicTUI
    app = MusicTUI()
    async with app.run_test() as pilot:
        app = pilot.app

        # Mock audio info
        mock_audio_info = MagicMock()
        mock_audio_info.length = 120.0  # 2 minutes
        mock_pygame_mixer.music.get_audio.return_value = mock_audio_info
        mock_pygame_mixer.music.set_pos = MagicMock()

        # Add track with duration
        track = Track(
            id=1,
            file_path="tests/e2e/fixtures/test.mp3",
            title="Test Song",
            duration=120
        )
        app.player.add_to_queue(track)
        app.player.play(track)

        await pilot.pause()

        # Test seek beyond duration
        app.player.seek(200.0)  # More than 120 seconds
        assert app.player.position == 120.0
        mock_pygame_mixer.music.set_pos.assert_called_with(120.0)


@pytest.mark.asyncio
async def test_player_pause_resumes_position_tracking():
    """Test that position tracking resumes after pause"""
    from src.app import MusicTUI
    app = MusicTUI()
    async with app.run_test() as pilot:
        app = pilot.app

        # Track position changes
        position_history = []

        def position_callback(position):
            position_history.append(position)

        app.player.set_on_position_change(position_callback)

        # Mock mixer
        mock_pygame_mixer.music.get_pos.return_value = 0

        # Play a track
        track = Track(id=1, file_path="tests/e2e/fixtures/test.mp3", title="Test Song")
        app.player.add_to_queue(track)
        app.player.play(track)

        await pilot.pause()

        # Pause
        app.player.pause()
        await pilot.pause()
        assert app.player.state == PlayerState.PAUSED

        # Resume
        app.player.resume()
        await pilot.pause()
        assert app.player.state == PlayerState.PLAYING

        # Note: In a real implementation, the position tracking thread
        # would be restarted on resume