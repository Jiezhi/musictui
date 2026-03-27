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
