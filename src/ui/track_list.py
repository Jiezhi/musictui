from typing import Optional, Callable
from textual.widgets import Static
from textual import events
from src.models import Track


class TrackList(Static):
    def __init__(self, **kwargs):
        super().__init__("No tracks in library.", **kwargs)
        self.tracks: list[Track] = []
        self.selected_index = 0
        self._track_offset = 0
        self._limit = 50
        self.total_count = 0
        self._load_more_callback: Optional[Callable[[], None]] = None

    def set_load_more_callback(self, callback: Callable[[], None]) -> None:
        self._load_more_callback = callback

    def _render(self) -> None:
        if not self.tracks:
            self.update("No tracks in library. Use :scan <path> to add music.")
        else:
            lines = []
            for i, track in enumerate(self.tracks):
                prefix = "> " if i == self.selected_index else "  "
                lines.append(f"{prefix}{track.display_name}")
            self.update("\n".join(lines))

    def set_tracks(self, tracks: list[Track], total_count: int = 0) -> None:
        self.tracks = tracks
        self.selected_index = 0
        self._track_offset = 0
        self.total_count = total_count
        self._render()

    def load_more(self) -> None:
        if self._load_more_callback and len(self.tracks) < self.total_count:
            self._load_more_callback()

    def append_tracks(self, tracks: list[Track]) -> None:
        self.tracks.extend(tracks)
        self._track_offset = len(self.tracks)
        self._render()

    def move_up(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index - 1) % len(self.tracks)
            self._render()

    def move_down(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index + 1) % len(self.tracks)
            self._render()
            if self.selected_index >= len(self.tracks) - 5:
                self.load_more()

    def on_mouse_scroll_down(self, event: events.MouseScrollDown) -> None:
        self.move_down()

    def on_mouse_scroll_up(self, event: events.MouseScrollUp) -> None:
        self.move_up()

    def get_selected_track(self) -> Optional[Track]:
        if 0 <= self.selected_index < len(self.tracks):
            return self.tracks[self.selected_index]
        return None
