from textual.widgets import Static
from textual.message import Message


class PlayerBar(Static):
    """播放条组件，支持鼠标点击"""

    class PlayPauseClicked(Message):
        """播放/暂停按钮点击"""

        pass

    class ProgressClicked(Message):
        """进度条点击"""

        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_track_title = "No track"
        self.current_track_artist = ""
        self.current_time = 0.0
        self.duration = 0.0

    def update_track(
        self,
        title: str,
        artist: str,
        current_time: float = 0.0,
        duration: float = 0.0,
    ) -> None:
        """更新曲目信息"""
        self.current_track_title = title
        self.current_track_artist = artist
        self.current_time = current_time
        self.duration = duration
        self._render_content()

    def _render_content(self) -> None:
        """渲染内容"""
        progress = ""
        if self.duration > 0:
            progress_width = 30
            filled = int((self.current_time / self.duration) * progress_width)
            progress = "[" + "=" * filled + "-" * (progress_width - filled) + "]"

        track_info = f"{self.current_track_title}"
        if self.current_track_artist:
            track_info += f" - {self.current_track_artist}"

        time_info = f"{self._format_time(self.current_time)} / {self._format_time(self.duration)}"

        self.update(f"{track_info} {progress} {time_info}")

    def _format_time(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    def on_click(self, event) -> None:
        """点击事件"""
        self.post_message(self.PlayPauseClicked())
