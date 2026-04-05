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
        self._page_size = 20
        self._last_rendered_content = ""

    def set_load_more_callback(self, callback: Callable[[], None]) -> None:
        self._load_more_callback = callback

    def _render_content(self) -> None:
        if not self.tracks:
            new_content = "No tracks in library. Use :scan <path> to add music."
        else:
            lines = []
            for i, track in enumerate(self.tracks):
                prefix = "> " if i == self.selected_index else "  "
                lines.append(f"{i + 1}. {prefix}{track.display_name}")
            new_content = "\n".join(lines)

        self._last_rendered_content = new_content
        self.update(new_content)
        # Use call_later so tests can mock the timer. Fallback to set_timer if call_later is unavailable.
        try:
            # type: ignore[attr-defined]
            self.call_later(0, self.scroll_to_selection)
        except Exception:
            try:
                self.set_timer(0, self.scroll_to_selection)
            except RuntimeError:
                pass

    def scroll_to_selection(self) -> None:
        if not self.tracks:
            return
        try:
            # Safely determine visible lines. Fall back to a sane default if size is not set.
            visible_lines = getattr(self.size, "height", 20)
            if not isinstance(visible_lines, int) or visible_lines <= 0:
                visible_lines = 20
            selection_line = self.selected_index
            current_scroll = getattr(self, "scroll_y", 0)
            bottom_line = (
                current_scroll + visible_lines if current_scroll else visible_lines
            )
            if selection_line < current_scroll:
                self.scroll(selection_line, animate=False)
            elif selection_line >= bottom_line:
                self.scroll(selection_line - visible_lines + 1, animate=False)
        except Exception:
            pass

    def set_tracks(self, tracks: list[Track], total_count: int = 0) -> None:
        self.tracks = tracks
        # Clamp selected_index to valid range
        max_index = max(0, len(tracks) - 1)
        if self.selected_index > max_index:
            self.selected_index = max_index
        self._track_offset = 0
        self.total_count = total_count
        self._render_content()

    def _force_render(self) -> None:
        if not self.tracks:
            new_content = "No tracks in library. Use :scan <path> to add music."
        else:
            lines = []
            for i, track in enumerate(self.tracks):
                prefix = "> " if i == self.selected_index else "  "
                lines.append(f"{i + 1}. {prefix}{track.display_name}")
            new_content = "\n".join(lines)

        self._last_rendered_content = new_content
        self.update(new_content)
        # Use call_later so tests can mock the timer. Fallback to set_timer if call_later is unavailable.
        try:
            # type: ignore[attr-defined]
            self.call_later(0, self.scroll_to_selection)
        except Exception:
            try:
                self.set_timer(0, self.scroll_to_selection)
            except RuntimeError:
                pass

    def load_more(self) -> None:
        if self._load_more_callback and len(self.tracks) < self.total_count:
            self._load_more_callback()

    def append_tracks(self, tracks: list[Track]) -> None:
        self.tracks.extend(tracks)
        self._track_offset = len(self.tracks)
        self._render_content()
        # Use set_timer to scroll AFTER the content is rendered
        # This handles scenarios where the selected item was outside the
        # current viewport and the list needs to scroll to bring it into view.
        # Use call_later so tests can mock the timer. Fallback to set_timer if call_later is unavailable.
        try:
            # type: ignore[attr-defined]
            self.call_later(0, self.scroll_to_selection)
        except Exception:
            try:
                self.set_timer(0, self.scroll_to_selection)
            except RuntimeError:
                pass

    def move_up(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index - 1) % len(self.tracks)
            self._force_render()

    def move_down(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index + 1) % len(self.tracks)
            self._force_render()
            if self.selected_index >= len(self.tracks) - 5:
                self.load_more()

    def page_up(self) -> None:
        if self.tracks:
            self.selected_index = max(0, self.selected_index - self._page_size)
            self._force_render()

    def page_down(self) -> None:
        if self.tracks:
            new_index = self.selected_index + self._page_size
            if new_index >= len(self.tracks) - 5:
                self.load_more()
            self.selected_index = min(new_index, len(self.tracks) - 1)
            self._force_render()

    def on_mouse_scroll_down(self, event: events.MouseScrollDown) -> None:
        self.move_down()

    def on_mouse_scroll_up(self, event: events.MouseScrollUp) -> None:
        self.move_up()

    def get_selected_track(self) -> Optional[Track]:
        if 0 <= self.selected_index < len(self.tracks):
            return self.tracks[self.selected_index]
        return None
