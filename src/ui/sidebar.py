from textual.widget import Widget
from textual.widgets import Static


class Sidebar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["Library", "Queue", "Search", "Settings"]
        self.selected = 0

    def render(self) -> str:
        lines = [f"  {item}" if i != self.selected else f"> {item}" for i, item in enumerate(self.items)]
        return "\n".join(lines)

    def move_up(self) -> None:
        self.selected = (self.selected - 1) % len(self.items)
        self.refresh()

    def move_down(self) -> None:
        self.selected = (self.selected + 1) % len(self.items)
        self.refresh()

    def get_selected(self) -> str:
        return self.items[self.selected]
