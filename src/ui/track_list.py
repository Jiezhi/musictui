from typing import Optional
from textual.widgets import Static
from src.models import Track


class TrackList(Static):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracks: list[Track] = []
        self.selected_index = 0

    def render(self) -> str:
        if not self.tracks:
            return "No tracks in library. Use :scan <path> to add music."

        lines = []
        for i, track in enumerate(self.tracks):
            prefix = "> " if i == self.selected_index else "  "
            lines.append(f"{prefix}{track.display_name}")
        return "\n".join(lines)

    def set_tracks(self, tracks: list[Track]) -> None:
        self.tracks = tracks
        self.selected_index = 0
        self.update(self.render())

    def move_up(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index - 1) % len(self.tracks)
            self.update(self.render())

    def move_down(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index + 1) % len(self.tracks)
            self.update(self.render())

    def get_selected_track(self) -> Optional[Track]:
        if 0 <= self.selected_index < len(self.tracks):
            return self.tracks[self.selected_index]
        return None
