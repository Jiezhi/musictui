from typing import Optional
from textual.widgets import Static
from src.models import Track


class Queue(Static):
    def __init__(self, **kwargs):
        super().__init__("Queue is empty.", **kwargs)
        self.tracks: list[Track] = []
        self.selected_index = 0
        self._last_rendered_content = ""

    def set_tracks(self, tracks: list[Track]) -> None:
        self.tracks = tracks
        self.selected_index = 0
        self._render_content()

    def _render_content(self) -> None:
        if not self.tracks:
            new_content = "Queue is empty. Add tracks to queue to see them here."
        else:
            lines = []
            for i, track in enumerate(self.tracks):
                prefix = "> " if i == self.selected_index else "  "
                duration = self._format_duration(track.duration)
                lines.append(f"{prefix}{track.display_name} [{duration}]")
            new_content = "\n".join(lines)

        self.update(new_content)
        self._last_rendered_content = new_content

    def _format_duration(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    def move_up(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index - 1) % len(self.tracks)
            self._render_content()

    def move_down(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index + 1) % len(self.tracks)
            self._render_content()

    def page_up(self) -> None:
        if self.tracks:
            self.selected_index = max(0, self.selected_index - 20)
            self._render_content()

    def page_down(self) -> None:
        if self.tracks:
            self.selected_index = min(len(self.tracks) - 1, self.selected_index + 20)
            self._render_content()

    def get_selected_track(self) -> Optional[Track]:
        if 0 <= self.selected_index < len(self.tracks):
            return self.tracks[self.selected_index]
        return None
