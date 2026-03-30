from textual.widgets import Static


class CommandInput(Static):
    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
        self.command = ""

    def set_command(self, cmd: str) -> None:
        self.command = cmd
        self._render_content()

    def get_command(self) -> str:
        return self.command

    def append_char(self, char: str) -> None:
        self.command += char
        self._render_content()

    def backspace(self) -> None:
        if self.command:
            self.command = self.command[:-1]
            self._render_content()

    def clear(self) -> None:
        self.command = ""
        self._render_content()

    def _render_content(self) -> None:
        self.update(f":{self.command}")
