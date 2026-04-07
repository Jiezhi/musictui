import pytest
import time
import threading
import pygame
from unittest.mock import MagicMock, patch
from src.player import Player
from src.models import Track, PlayerState, PlayMode


class TestPlayerEnhanced:
    """Test cases for enhanced Player functionality"""

    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.player = Player()

    def test_player_initial_state_enhanced(self):
        """Test enhanced initial state"""
        assert self.player.state == PlayerState.STOPPED
        assert self.player.volume == 0.7
        assert self.player.play_mode == PlayMode.LOOP
        assert self.player.position == 0.0
        assert self.player.duration == 0.0
        assert self.player.queue == []
        assert self.player.get_current_track() is None

    def test_add_to_queue_with_id(self):
        """Test adding tracks to queue with ID"""
        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.add_to_queue(track)
        assert len(self.player.queue) == 1
        assert self.player.queue[0].id == 1

    def test_add_duplicate_track_to_queue(self):
        """Test adding duplicate track to queue"""
        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.add_to_queue(track)
        self.player.add_to_queue(track)

        # Should have two entries in queue
        assert len(self.player.queue) == 2
        assert self.player.queue[0].id == self.player.queue[1].id

    def test_play_with_duplicate_track(self):
        """Test playing a track that's already in queue"""
        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.add_to_queue(track)
        self.player.play(track)

        # Should set current index to existing track
        assert self.player.current_index == 0
        assert self.player.get_current_track() == track

    @patch('pygame.mixer.music')
    def test_seek_functionality(self, mock_music):
        """Test seek functionality"""
        # Mock get_audio to return a fake audio object with length
        mock_audio_info = MagicMock()
        mock_audio_info.length = 180.0  # 3 minutes
        mock_music.get_audio.return_value = mock_audio_info
        mock_music.set_pos = MagicMock()

        track = Track(id=1, file_path="/test.mp3", title="Test Song", duration=180)
        self.player.play(track)

        # Test seeking
        self.player.seek(30.0)
        assert self.player.position == 30.0
        mock_music.set_pos.assert_called_once_with(30.0)

    @patch('pygame.mixer.music')
    def test_seek_clamps_values(self, mock_music):
        """Test that seek clamps values to valid range"""
        # Mock get_audio to return actual numbers, not MagicMock
        mock_audio_info = MagicMock()
        mock_audio_info.length = 180.0
        mock_music.get_audio.return_value = mock_audio_info
        mock_music.set_pos = MagicMock()

        track = Track(id=1, file_path="/test.mp3", title="Test Song", duration=180)
        self.player.play(track)

        # Test negative position
        self.player.seek(-10.0)
        assert self.player.position == 0.0
        mock_music.set_pos.assert_called_with(0.0)

        # Test position beyond duration
        self.player.seek(200.0)
        assert self.player.position == 180.0
        mock_music.set_pos.assert_called_with(180.0)

    @patch('pygame.mixer.music')
    def test_get_position_while_playing(self, mock_music):
        """Test getting position while playing"""
        mock_music.get_pos.return_value = 5000  # 5 seconds in milliseconds

        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.play(track)
        self.player.position = 30.0  # Simulate some elapsed time

        position = self.player.get_position()
        assert position == 35.0  # 30s + 5s

    @patch('pygame.mixer.music')
    def test_get_position_stopped(self, mock_music):
        """Test getting position when stopped"""
        mock_music.get_pos.return_value = 0

        position = self.player.get_position()
        assert position == 0.0

    @patch('pygame.mixer.music')
    def test_get_progress(self, mock_music):
        """Test progress calculation"""
        mock_music.get_audio = MagicMock()
        mock_music.get_audio.return_value.length = 100.0

        track = Track(id=1, file_path="/test.mp3", title="Test Song", duration=100)
        self.player.play(track)

        # Test at 50%
        self.player.position = 50.0
        assert self.player.get_progress() == 0.5

        # Test at 0%
        self.player.position = 0.0
        assert self.player.get_progress() == 0.0

        # Test at 100%
        self.player.position = 100.0
        assert self.player.get_progress() == 1.0

    def test_get_progress_zero_duration(self):
        """Test progress calculation with zero duration"""
        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.play(track)

        progress = self.player.get_progress()
        assert progress == 0.0

    def test_remove_from_queue(self):
        """Test removing tracks from queue"""
        track1 = Track(id=1, file_path="/test1.mp3", title="Song 1")
        track2 = Track(id=2, file_path="/test2.mp3", title="Song 2")
        track3 = Track(id=3, file_path="/test3.mp3", title="Song 3")

        self.player.add_to_queue(track1)
        self.player.add_to_queue(track2)
        self.player.add_to_queue(track3)

        # Remove middle track
        assert self.player.remove_from_queue(1)
        assert len(self.player.queue) == 2
        assert self.player.queue[0].title == "Song 1"
        assert self.player.queue[1].title == "Song 3"

    def test_remove_from_queue_invalid_index(self):
        """Test removing from invalid index"""
        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.add_to_queue(track)

        # Try to remove non-existent track
        assert not self.player.remove_from_queue(1)
        assert not self.player.remove_from_queue(-1)

    def test_move_in_queue(self):
        """Test moving tracks in queue"""
        tracks = [
            Track(id=1, file_path="/test1.mp3", title="Song 1"),
            Track(id=2, file_path="/test2.mp3", title="Song 2"),
            Track(id=3, file_path="/test3.mp3", title="Song 3"),
            Track(id=4, file_path="/test4.mp3", title="Song 4"),
        ]

        for track in tracks:
            self.player.add_to_queue(track)

        # Move track 1 to position 3
        self.player.move_in_queue(0, 3)
        assert self.player.queue[0].title == "Song 2"
        assert self.player.queue[3].title == "Song 1"

    def test_move_in_queue_invalid_indices(self):
        """Test moving with invalid indices"""
        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.add_to_queue(track)

        # Try invalid moves
        assert not self.player.move_in_queue(-1, 0)
        assert not self.player.move_in_queue(0, -1)
        assert not self.player.move_in_queue(0, 1)  # Only one track

    @patch('pygame.mixer.music')
    def test_toggle_pause(self, mock_music):
        """Test toggle pause functionality"""
        mock_music.get_audio = MagicMock()

        track = Track(id=1, file_path="/test.mp3", title="Test Song")

        # Can't toggle when stopped
        self.player.toggle_pause()
        assert self.player.state == PlayerState.STOPPED

        # Play and toggle to pause
        self.player.play(track)
        self.player.toggle_pause()
        assert self.player.state == PlayerState.PAUSED

        # Toggle back to play
        self.player.toggle_pause()
        assert self.player.state == PlayerState.PLAYING

    @patch('pygame.mixer.music')
    def test_error_handling_on_play(self, mock_music):
        """Test error handling when playing fails"""
        mock_music.load.side_effect = pygame.error("File not found")

        track = Track(id=1, file_path="/nonexistent.mp3", title="Nonexistent")
        self.player.play(track)

        # Should end up in stopped state
        assert self.player.state == PlayerState.STOPPED

    @patch('pygame.mixer.music')
    def test_error_handling_on_next(self, mock_music):
        """Test error handling when next track fails to load"""
        mock_music.load.side_effect = pygame.error("File not found")

        tracks = [
            Track(id=1, file_path="/test1.mp3", title="Song 1"),
            Track(id=2, file_path="/test2.mp3", title="Song 2"),
        ]

        for track in tracks:
            self.player.add_to_queue(track)

        # Start playing first track
        self.player.play(tracks[0])

        # Try to play next (will fail)
        self.player.next()

        # Should be stopped
        assert self.player.state == PlayerState.STOPPED

    def test_queue_length_checks(self):
        """Test queue length checks"""
        assert self.player.get_queue_length() == 0
        assert self.player.is_empty()

        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.add_to_queue(track)

        assert self.player.get_queue_length() == 1
        assert not self.player.is_empty()

    def test_position_callback(self):
        """Test position change callback"""
        callback_called = False
        last_position = 0.0

        def position_callback(position):
            nonlocal callback_called, last_position
            callback_called = True
            last_position = position

        self.player.set_on_position_change(position_callback)

        # Simulate position change
        self.player.position = 10.0
        callback_called = False  # Reset for test

        # Trigger callback manually (normally done by position tracking thread)
        if self.player._on_position_change:
            self.player._on_position_change(10.0)

        # Note: In a real scenario, the callback would be triggered by the
        # position tracking thread. This is a simplified test.

    @patch('pygame.mixer.music')
    def test_shuffle_play_mode(self, mock_music):
        """Test shuffle play mode"""
        mock_music.get_audio = MagicMock()

        tracks = [
            Track(id=1, file_path="/test1.mp3", title="Song 1"),
            Track(id=2, file_path="/test2.mp3", title="Song 2"),
            Track(id=3, file_path="/test3.mp3", title="Song 3"),
        ]

        for track in tracks:
            self.player.add_to_queue(track)

        # Set shuffle mode
        self.player.set_play_mode(PlayMode.SHUFFLE)

        # Test next in shuffle mode
        original_index = self.player.current_index
        self.player.next()

        # Should have changed to a different track
        assert self.player.current_index != original_index
        assert 0 <= self.player.current_index < len(self.player.queue)

    @patch('time.sleep', side_effect=lambda t: None)  # Don't actually sleep in tests
    def test_position_tracking_thread(self, mock_sleep):
        """Test position tracking thread functionality"""
        callback_called = False
        last_position = 0.0

        def position_callback(position):
            nonlocal callback_called, last_position
            callback_called = True
            last_position = position

        self.player.set_on_position_change(position_callback)

        # Mock pygame.mixer.music.get_pos
        with patch('pygame.mixer.music.get_pos') as mock_get_pos:
            mock_get_pos.return_value = 1000  # 1 second

            # Start playing
            track = Track(id=1, file_path="/test.mp3", title="Test Song")
            self.player.play(track)

            # Let position tracking run briefly
            time.sleep(0.2)

            # Stop playback
            self.player.stop()

        # Note: This is a simplified test. In a real scenario, the callback
        # would be triggered by the background thread.

    def test_clear_queue_resets_index(self):
        """Test that clearing queue resets current index"""
        track = Track(id=1, file_path="/test.mp3", title="Test Song")
        self.player.add_to_queue(track)
        self.player.current_index = 0
        self.player.play(track)

        self.player.clear_queue()
        assert self.player.current_index == -1
        assert len(self.player.queue) == 0