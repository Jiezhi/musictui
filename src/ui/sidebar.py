from textual.widgets import Static


class Sidebar(Static):
    def __init__(self, **kwargs):
        items = ["Library", "Queue", "Search", "Favorites", "Settings"]
        super().__init__("\n".join(items), **kwargs)
        self.items = items
        self.selected = 0

    def move_up(self) -> None:
        self.selected = (self.selected - 1) % len(self.items)
        self._update_content()

    def move_down(self) -> None:
        self.selected = (self.selected + 1) % len(self.items)
        self._update_content()

    def _update_content(self):
        lines = [
            f"  {item}" if i != self.selected else f"> {item}"
            for i, item in enumerate(self.items)
        ]
        self.update("\n".join(lines))

    def get_selected(self) -> str:
        return self.items[self.selected]
