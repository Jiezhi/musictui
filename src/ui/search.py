from typing import Optional, TYPE_CHECKING
from textual.widgets import Static
from src.models import Track

if TYPE_CHECKING:
    from src.library import Library


class Search(Static):
    def __init__(self, **kwargs):
        super().__init__("Search: ", **kwargs)
        self.query = ""
        self.results: list[Track] = []
        self.selected_index = 0
        self._library = None

    def set_library(self, library: "Library") -> None:
        self._library = library

    def set_results(self, tracks: list[Track]) -> None:
        self.results = tracks
        self.selected_index = 0
        self._render()

    def append_char(self, char: str) -> None:
        self.query += char
        self.execute_search()

    def backspace(self) -> None:
        if self.query:
            self.query = self.query[:-1]
            if self._library and self.query.strip():
                self.execute_search()
            else:
                self.results = []
                self._render()

    def execute_search(self) -> None:
        if self._library and self.query.strip():
            self.results = self._library.search(self.query)
            self.selected_index = 0
            self._render()

    def perform_search(self, query: str, library: "Library") -> None:
        self.query = query
        if query.strip():
            self.results = library.search(query)
        else:
            self.results = []
        self.selected_index = 0
        self._render()

    def _render(self) -> None:
        if not self.query:
            self.update("Search: (type to search)\n")
        elif not self.results:
            self.update(f"Search: {self.query}\n\nNo results found.")
        else:
            lines = [f"Search: {self.query}"]
            for i, track in enumerate(self.results):
                prefix = "> " if i == self.selected_index else "  "
                lines.append(f"{prefix}{track.display_name}")
            lines.append(f"\n[{len(self.results)} results]")
            self.update("\n".join(lines))

    def move_up(self) -> None:
        if self.results:
            self.selected_index = (self.selected_index - 1) % len(self.results)
            self._render()

    def move_down(self) -> None:
        if self.results:
            self.selected_index = (self.selected_index + 1) % len(self.results)
            self._render()

    def get_selected_track(self) -> Optional[Track]:
        if 0 <= self.selected_index < len(self.results):
            return self.results[self.selected_index]
        return None

    def clear(self) -> None:
        self.query = ""
        self.results = []
        self.selected_index = 0
        self._render()
