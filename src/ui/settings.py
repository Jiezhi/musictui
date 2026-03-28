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
        self._update_content()

    def move_up(self) -> None:
        self.selected = (self.selected - 1) % len(self.items)
        self._update_content()

    def move_down(self) -> None:
        self.selected = (self.selected + 1) % len(self.items)
        self._update_content()

    def _format_value(self, key: str) -> str:
        value = self.values.get(key, "")
        if key == "Volume":
            return f"{int(value * 100)}%"
        elif key == "Play Mode":
            return value
        elif key == "Theme":
            return value
        elif key == "Library Paths":
            return value if value else "(not set)"
        return str(value)

    def _update_content(self):
        lines = []
        for i, item in enumerate(self.items):
            prefix = "> " if i == self.selected else "  "
            value = self._format_value(item)
            if value:
                lines.append(f"{prefix}{item}: {value}")
            else:
                lines.append(f"{prefix}{item}")
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
        self._update_content()

    def cycle_theme(self) -> None:
        themes = ["monokai", "nord", "dracula"]
        current = self.values.get("Theme", "monokai")
        idx = themes.index(current) if current in themes else 0
        self.values["Theme"] = themes[(idx + 1) % len(themes)]
        self._update_content()

    def adjust_volume(self, delta: float) -> None:
        new_volume = max(0.0, min(1.0, self.values["Volume"] + delta))
        self.values["Volume"] = new_volume
        self._update_content()

    def toggle_value(self) -> None:
        selected = self.get_selected()
        if selected == "Volume":
            pass
        elif selected == "Play Mode":
            self.toggle_play_mode()
        elif selected == "Theme":
            self.cycle_theme()
        elif selected == "Library Paths":
            pass

    def set_library_paths(self, paths: list[str]) -> None:
        self.values["Library Paths"] = ", ".join(paths)
        self._update_content()

    def get_display_text(self) -> str:
        lines = []
        for i, item in enumerate(self.items):
            prefix = "> " if i == self.selected else "  "
            value = self._format_value(item)
            if value:
                lines.append(f"{prefix}{item}: {value}")
            else:
                lines.append(f"{prefix}{item}")
        return "\n".join(lines)
