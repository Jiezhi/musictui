import pytest
from src.player import Player
from src.models import Track, PlayerState, PlayMode


def test_player_initial_state():
    player = Player()
    assert player.state == PlayerState.STOPPED
    assert player.volume == 0.7
    assert player.play_mode == PlayMode.LOOP
    assert player.queue == []


def test_player_add_to_queue():
    player = Player()
    track = Track(file_path="/test.mp3", title="Test Song")
    player.add_to_queue(track)
    assert len(player.queue) == 1


def test_player_add_to_queue_front():
    player = Player()
    track1 = Track(file_path="/test1.mp3", title="First")
    track2 = Track(file_path="/test2.mp3", title="Second")
    player.add_to_queue(track1)
    player.add_to_queue_front(track2)
    assert player.queue[0].title == "Second"


def test_player_clear_queue():
    player = Player()
    track = Track(file_path="/test.mp3", title="Test")
    player.add_to_queue(track)
    player.clear_queue()
    assert len(player.queue) == 0
    assert player.current_index == -1


def test_player_get_current_track_empty_queue():
    player = Player()
    assert player.get_current_track() is None


def test_player_get_current_track_with_tracks():
    player = Player()
    track = Track(id=1, file_path="/test.mp3", title="Test")
    player.add_to_queue(track)
    player.current_index = 0
    assert player.get_current_track() is not None
    assert player.get_current_track().title == "Test"


def test_player_set_volume():
    player = Player()
    player.set_volume(0.5)
    assert player.volume == 0.5


def test_player_set_volume_clamped():
    player = Player()
    player.set_volume(1.5)
    assert player.volume == 1.0
    player.set_volume(-0.5)
    assert player.volume == 0.0


def test_player_set_play_mode():
    player = Player()
    player.set_play_mode(PlayMode.SHUFFLE)
    assert player.play_mode == PlayMode.SHUFFLE


def test_player_seek():
    player = Player()
    player.seek(30.0)
    assert player.position == 30.0
