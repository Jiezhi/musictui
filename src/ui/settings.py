from textual.widgets import Static


class Settings(Static):
    def __init__(self, **kwargs):
        items = ["Volume", "Play Mode", "Theme", "Library Paths"]
        super().__init__("\n".join(items), **kwargs)
        self.items = items
        self.selected = 0
        self.values = {
            "Volume": 0.7,
            "Play Mode": "loop",
            "Theme": "monokai",
            "Library Paths": "",
        }

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

    def update_value(self, key: str, value) -> None:
        if key in self.values:
            self.values[key] = value

    def get_value(self, key: str):
        return self.values.get(key, None)

    def toggle_play_mode(self) -> None:
        modes = ["loop", "shuffle", "repeat_one"]
        current = self.values.get("Play Mode", "loop")
        idx = modes.index(current) if current in modes else 0
        self.values["Play Mode"] = modes[(idx + 1) % len(modes)]

    def cycle_theme(self) -> None:
        themes = ["monokai", "nord", "dracula"]
        current = self.values.get("Theme", "monokai")
        idx = themes.index(current) if current in themes else 0
        self.values["Theme"] = themes[(idx + 1) % len(themes)]
