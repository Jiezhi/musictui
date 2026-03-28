from textual.widgets import Static


class PlayerBar(Static):
    def __init__(self, **kwargs):
        super().__init__("No track playing", **kwargs)
        self.track_title = ""
        self.track_artist = ""
        self.current_time = 0.0
        self.total_time = 0.0

    def _format_time(self, seconds: float) -> str:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def update_track(
        self, title: str, artist: str, current: float, total: float
    ) -> None:
        self.track_title = title
        self.track_artist = artist
        self.current_time = current
        self.total_time = total
        status = "▶"
        progress = "━" * 20
        content = f"{status} {self.track_title} - {self.track_artist}  {self._format_time(self.current_time)}/{self._format_time(self.total_time)}\n[{progress}]"
        self.update(content)
