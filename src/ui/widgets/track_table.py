from typing import Optional, Any
from textual.widgets import DataTable
from textual.message import Message
from src.models import Track


class TrackTable(DataTable):
    """曲目列表组件，基于 DataTable"""

    class TrackSelected(Message):
        """曲目选中消息（单击）"""

        def __init__(self, track: Optional[Track], index: int) -> None:
            super().__init__()
            self.track = track
            self.index = index

    class TrackDoubleClicked(Message):
        """曲目双击消息"""

        def __init__(self, track: Optional[Track], index: int) -> None:
            super().__init__()
            self.track = track
            self.index = index

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.tracks: list[Track] = []
        self.cursor_type = "none"

    def on_mount(self) -> None:
        self.add_columns("#", "Title", "Artist", "Album", "Duration")

    def set_tracks(self, tracks: list[Track]) -> None:
        """设置曲目列表"""
        self.tracks = tracks
        self.clear()
        for i, track in enumerate(tracks):
            duration = self._format_duration(track.duration)
            self.add_row(
                str(i + 1),
                track.title or "Unknown",
                track.artist or "Unknown",
                track.album or "Unknown",
                duration,
                key=str(track.id),
            )
        if tracks:
            self.call_later(lambda: setattr(self, "cursor_coordinate", (0, 0)))

    def _format_duration(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    def get_selected_track(self) -> Optional[Track]:
        """获取选中的曲目"""
        if 0 <= self.cursor_row < len(self.tracks):
            return self.tracks[self.cursor_row]
        return None

    def get_selected_index(self) -> int:
        """获取选中索引"""
        return self.cursor_row

    def move_up(self) -> None:
        """上移选择"""
        if self.cursor_row > 0:
            self.cursor_coordinate = (self.cursor_row - 1, self.cursor_column)

    def move_down(self) -> None:
        """下移选择"""
        if self.cursor_row < len(self.tracks) - 1:
            self.cursor_coordinate = (self.cursor_row + 1, self.cursor_column)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """行选中事件"""
        track = self.get_selected_track()
        self.post_message(self.TrackSelected(track, self.cursor_row))

    def on_data_table_row_double_clicked(self, event: DataTable.RowSelected) -> None:
        """行双击事件"""
        track = self.get_selected_track()
        self.post_message(self.TrackDoubleClicked(track, self.cursor_row))
