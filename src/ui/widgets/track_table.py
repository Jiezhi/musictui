from typing import Optional, Any
from textual.widgets import DataTable
from textual.message import Message
from src.models import Track


class TrackTable(DataTable):
    # Helper to move cursor; Textual DataTable may not expose cursor_move directly
    def cursor_move(self, row: int, column: int = 0) -> None:
        """Set cursor position programmatically.

        Args:
            row: Row index to select.
            column: Column index (default 0).
        """
        # DataTable uses `cursor_coordinate` property for position
        self.cursor_coordinate = (row, column)

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
        self.cursor_type = "row"

    def on_mount(self) -> None:
        self.add_column("#", width=5)
        self.add_column("Title", width=25)
        self.add_column("Artist", width=20)
        self.add_column("Album", width=20)
        self.add_column("Duration", width=10)

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
            self.set_timer(0.001, lambda: self.cursor_move(row=0, column=0))

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
            self.cursor_move(row=self.cursor_row - 1)

    def move_down(self) -> None:
        """下移选择"""
        if self.cursor_row < len(self.tracks) - 1:
            self.cursor_move(row=self.cursor_row + 1)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """行选中事件"""
        track = self.get_selected_track()
        self.post_message(self.TrackSelected(track, self.cursor_row))

    def on_data_table_row_activated(self, event: Any) -> None:
        """行双击事件 (fallback)"""
        track = self.get_selected_track()
        self.post_message(self.TrackDoubleClicked(track, self.cursor_row))

    def on_data_table_row_double_clicked(self, event: Any) -> None:
        """行双击事件（显式）"""
        track = self.get_selected_track()
        self.post_message(self.TrackDoubleClicked(track, self.cursor_row))
