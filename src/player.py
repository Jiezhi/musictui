import random
from typing import Optional, Callable

import pygame
from src.models import Track, PlayerState, PlayMode


class Player:
    def __init__(self):
        self.queue: list[Track] = []
        self.current_index: int = -1
        self.state: PlayerState = PlayerState.STOPPED
        self.volume: float = 0.7
        self.play_mode: PlayMode = PlayMode.LOOP
        self.position: float = 0.0
        self._current_sound: Optional[pygame.mixer.Sound] = None
        self._on_track_change: Optional[Callable[[Track], None]] = None
        self._on_state_change: Optional[Callable[[PlayerState], None]] = None
        pygame.mixer.init()

    def set_on_track_change(self, callback: Callable[[Track], None]) -> None:
        self._on_track_change = callback

    def set_on_state_change(self, callback: Callable[[PlayerState], None]) -> None:
        self._on_state_change = callback

    def add_to_queue(self, track: Track) -> None:
        self.queue.append(track)

    def add_to_queue_front(self, track: Track) -> None:
        self.queue.insert(0, track)

    def clear_queue(self) -> None:
        self.queue.clear()
        self.current_index = -1

    def play(self, track: Optional[Track] = None) -> None:
        if track:
            self.add_to_queue(track)
            self.current_index = len(self.queue) - 1

        if self.current_index < 0 or self.current_index >= len(self.queue):
            return

        self._load_and_play(self.queue[self.current_index])

    def _load_and_play(self, track: Track) -> None:
        try:
            if self._current_sound:
                self._current_sound.stop()
            pygame.mixer.music.load(track.file_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            self.state = PlayerState.PLAYING
            if self._on_track_change:
                self._on_track_change(track)
            if self._on_state_change:
                self._on_state_change(self.state)
        except Exception as e:
            print(f"Error playing track: {e}")
            self.next()

    def pause(self) -> None:
        if self.state == PlayerState.PLAYING:
            pygame.mixer.pause()
            self.state = PlayerState.PAUSED
            if self._on_state_change:
                self._on_state_change(self.state)

    def resume(self) -> None:
        if self.state == PlayerState.PAUSED:
            pygame.mixer.unpause()
            self.state = PlayerState.PLAYING
            if self._on_state_change:
                self._on_state_change(self.state)

    def stop(self) -> None:
        pygame.mixer.stop()
        self.state = PlayerState.STOPPED
        if self._on_state_change:
            self._on_state_change(self.state)

    def next(self) -> None:
        if not self.queue:
            return

        if self.play_mode == PlayMode.SHUFFLE:
            self.current_index = random.randint(0, len(self.queue) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.queue)

        if self.state == PlayerState.PLAYING:
            self._load_and_play(self.queue[self.current_index])

    def previous(self) -> None:
        if not self.queue:
            return

        self.current_index = (self.current_index - 1) % len(self.queue)

        if self.state == PlayerState.PLAYING:
            self._load_and_play(self.queue[self.current_index])

    def seek(self, position: float) -> None:
        self.position = position

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def set_play_mode(self, mode: PlayMode) -> None:
        self.play_mode = mode

    def get_current_track(self) -> Optional[Track]:
        if 0 <= self.current_index < len(self.queue):
            return self.queue[self.current_index]
        return None
