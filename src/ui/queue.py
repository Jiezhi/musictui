from typing import Optional
from textual.widgets import Static
from src.models import Track


class Queue(Static):
    def __init__(self, **kwargs):
        super().__init__("Queue is empty.", **kwargs)
        self.tracks: list[Track] = []
        self.selected_index = 0

    def set_tracks(self, tracks: list[Track]) -> None:
        self.tracks = tracks
        self.selected_index = 0
        self._render()

    def _render(self) -> None:
        if not self.tracks:
            self.update("Queue is empty. Add tracks to queue to see them here.")
        else:
            lines = []
            for i, track in enumerate(self.tracks):
                prefix = "> " if i == self.selected_index else "  "
                duration = self._format_duration(track.duration)
                lines.append(f"{prefix}{track.display_name} [{duration}]")
            self.update("\n".join(lines))

    def _format_duration(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    def move_up(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index - 1) % len(self.tracks)
            self._render()

    def move_down(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index + 1) % len(self.tracks)
            self._render()

    def get_selected_track(self) -> Optional[Track]:
        if 0 <= self.selected_index < len(self.tracks):
            return self.tracks[self.selected_index]
        return None
