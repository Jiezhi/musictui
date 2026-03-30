from src.theme.base import ThemeColors


class NordTheme(ThemeColors):
    def __init__(self):
        super().__init__(
            name="nord",
            background="#2e3440",
            surface="#3b4252",
            foreground="#eceff4",
            primary="#88c0d0",
            secondary="#81a1c1",
            accent="#5e81ac",
            success="#a3be8c",
            warning="#ebcb8b",
            error="#bf616a",
            playing="#a3be8c",
            paused="#ebcb8b",
            stopped="#4c566a",
            progress_bar="#88c0d0",
            progress_background="#434c5e",
            border="#4c566a",
            border_focus="#88c0d0",
        )
