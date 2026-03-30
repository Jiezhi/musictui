from src.theme.base import ThemeColors


class DraculaTheme(ThemeColors):
    def __init__(self):
        super().__init__(
            name="dracula",
            background="#282a36",
            surface="#44475a",
            foreground="#f8f8f2",
            primary="#ff79c6",
            secondary="#bd93f9",
            accent="#8be9fd",
            success="#50fa7b",
            warning="#f1fa8c",
            error="#ff5555",
            playing="#50fa7b",
            paused="#f1fa8c",
            stopped="#6272a4",
            progress_bar="#ff79c6",
            progress_background="#44475a",
            border="#44475a",
            border_focus="#ff79c6",
        )
