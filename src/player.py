import random
import time
import threading
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
        self.duration: float = 0.0
        self._current_sound: Optional[pygame.mixer.Sound] = None
        self._on_track_change: Optional[Callable[[Track], None]] = None
        self._on_state_change: Optional[Callable[[PlayerState], None]] = None
        self._on_position_change: Optional[Callable[[float], None]] = None
        self._position_thread: Optional[threading.Thread] = None
        self._stop_position_tracking = threading.Event()
        pygame.mixer.init()

    def set_on_track_change(self, callback: Callable[[Track], None]) -> None:
        self._on_track_change = callback

    def set_on_state_change(self, callback: Callable[[PlayerState], None]) -> None:
        self._on_state_change = callback

    def set_on_position_change(self, callback: Callable[[float], None]) -> None:
        self._on_position_change = callback

    def add_to_queue(self, track: Track) -> None:
        self.queue.append(track)

    def add_to_queue_front(self, track: Track) -> None:
        self.queue.insert(0, track)

    def clear_queue(self) -> None:
        self.queue.clear()
        self.current_index = -1

    def play(self, track: Optional[Track] = None) -> None:
        if track:
            # Check if track already in queue
            for i, t in enumerate(self.queue):
                if t.id == track.id:
                    self.current_index = i
                    break
            else:
                # Track not in queue, add it
                self.add_to_queue(track)
                self.current_index = len(self.queue) - 1

        if self.current_index < 0 or self.current_index >= len(self.queue):
            if self.queue:
                self.current_index = 0
            else:
                return

        self._load_and_play(self.queue[self.current_index])

    def _load_and_play(self, track: Track) -> None:
        try:
            if self._current_sound:
                self._current_sound.stop()

            # Stop position tracking if it's running
            self._stop_position_tracking.set()
            if self._position_thread and self._position_thread.is_alive():
                self._position_thread.join(timeout=1.0)

            pygame.mixer.music.load(track.file_path)
            pygame.mixer.music.set_volume(self.volume)

            # Get track duration if possible
            try:
                info = pygame.mixer.music.get_audio()
                self.duration = getattr(info, 'length', 0.0) if info else 0.0
            except:
                self.duration = 0.0

            pygame.mixer.music.play()
            self.state = PlayerState.PLAYING
            self.position = 0.0

            if self._on_track_change:
                self._on_track_change(track)
            if self._on_state_change:
                self._on_state_change(self.state)

            # Start position tracking
            self._stop_position_tracking.clear()
            self._position_thread = threading.Thread(target=self._track_position, daemon=True)
            self._position_thread.start()

        except pygame.error as e:
            print(f"Error loading track {track.file_path}: {e}")
            self.state = PlayerState.STOPPED
            if self._on_state_change:
                self._on_state_change(self.state)
        except Exception as e:
            print(f"Unexpected error playing track: {e}")
            self.state = PlayerState.STOPPED
            if self._on_state_change:
                self._on_state_change(self.state)

    def pause(self) -> None:
        if self.state == PlayerState.PLAYING:
            pygame.mixer.pause()
            self.state = PlayerState.PAUSED
            self._stop_position_tracking.set()
            if self._position_thread and self._position_thread.is_alive():
                self._position_thread.join(timeout=1.0)
            if self._on_state_change:
                self._on_state_change(self.state)

    def resume(self) -> None:
        if self.state == PlayerState.PAUSED:
            pygame.mixer.unpause()
            self.state = PlayerState.PLAYING
            # Restart position tracking
            self._stop_position_tracking.clear()
            self._position_thread = threading.Thread(target=self._track_position, daemon=True)
            self._position_thread.start()
            if self._on_state_change:
                self._on_state_change(self.state)

    def stop(self) -> None:
        pygame.mixer.stop()
        self.state = PlayerState.STOPPED
        self.position = 0.0
        self._stop_position_tracking.set()
        if self._position_thread and self._position_thread.is_alive():
            self._position_thread.join(timeout=1.0)
        if self._on_state_change:
            self._on_state_change(self.state)
        if self._on_position_change:
            self._on_position_change(0.0)

    def next(self) -> None:
        if not self.queue:
            return

        if self.play_mode == PlayMode.SHUFFLE:
            self.current_index = random.randint(0, len(self.queue) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.queue)

        if self.state == PlayerState.PLAYING:
            try:
                self._load_and_play(self.queue[self.current_index])
            except Exception as e:
                print(f"Error loading next track: {e}")
                # Try to continue with the queue
                self.state = PlayerState.STOPPED
                if self._on_state_change:
                    self._on_state_change(self.state)

    def previous(self) -> None:
        if not self.queue:
            return

        self.current_index = (self.current_index - 1) % len(self.queue)

        if self.state == PlayerState.PLAYING:
            try:
                self._load_and_play(self.queue[self.current_index])
            except Exception as e:
                print(f"Error loading previous track: {e}")
                # Try to continue with the queue
                self.state = PlayerState.STOPPED
                if self._on_state_change:
                    self._on_state_change(self.state)

    def previous(self) -> None:
        if not self.queue:
            return

        self.current_index = (self.current_index - 1) % len(self.queue)

        if self.state == PlayerState.PLAYING:
            self._load_and_play(self.queue[self.current_index])

    def seek(self, position: float) -> None:
        if position < 0:
            position = 0.0
        if self.duration > 0 and position > self.duration:
            position = self.duration

        try:
            pygame.mixer.music.set_pos(position)
            self.position = position
            if self._on_position_change:
                self._on_position_change(position)
        except pygame.error as e:
            print(f"Error seeking to position {position}: {e}")
        except Exception as e:
            print(f"Unexpected error during seek: {e}")

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def set_play_mode(self, mode: PlayMode) -> None:
        self.play_mode = mode

    def get_current_track(self) -> Optional[Track]:
        if 0 <= self.current_index < len(self.queue):
            return self.queue[self.current_index]
        return None

    def get_position(self) -> float:
        """Get current playback position in seconds"""
        if self.state == PlayerState.PLAYING:
            try:
                return pygame.mixer.music.get_pos() / 1000.0 + self.position
            except:
                return self.position
        return self.position

    def get_progress(self) -> float:
        """Get playback progress as a fraction (0.0 to 1.0)"""
        if self.duration <= 0:
            return 0.0
        return min(1.0, self.position / self.duration)

    def _track_position(self) -> None:
        """Track the current playback position in a separate thread"""
        last_time = time.time()

        while not self._stop_position_tracking.is_set():
            if self.state == PlayerState.PLAYING:
                current_pos = pygame.mixer.music.get_pos() / 1000.0 + self.position
                if current_pos != self.position:
                    self.position = current_pos
                    if self._on_position_change:
                        self._on_position_change(self.position)

            # Sleep for a short interval
            time.sleep(0.1)
            last_time = time.time()

    def remove_from_queue(self, index: int) -> bool:
        """Remove a track from the queue at the specified index"""
        if 0 <= index < len(self.queue):
            removed = self.queue.pop(index)

            # Adjust current index if necessary
            if self.current_index == index:
                # If removing the current track, stop playback
                self.stop()
            elif self.current_index > index:
                self.current_index -= 1

            return True
        return False

    def move_in_queue(self, from_index: int, to_index: int) -> bool:
        """Move a track from one position to another in the queue"""
        if (0 <= from_index < len(self.queue) and
            0 <= to_index < len(self.queue) and
            from_index != to_index):

            # Remove and reinsert at new position
            track = self.queue.pop(from_index)
            self.queue.insert(to_index, track)

            # Adjust current index if it was affected
            if self.current_index == from_index:
                self.current_index = to_index
            elif from_index < self.current_index <= to_index:
                self.current_index -= 1
            elif to_index <= self.current_index < from_index:
                self.current_index += 1

            return True
        return False

    def get_queue_length(self) -> int:
        """Get the number of tracks in the queue"""
        return len(self.queue)

    def is_empty(self) -> bool:
        """Check if the queue is empty"""
        return len(self.queue) == 0

    def toggle_pause(self) -> None:
        """Toggle between play and pause states"""
        if self.state == PlayerState.PLAYING:
            self.pause()
        elif self.state == PlayerState.PAUSED:
            self.resume()
