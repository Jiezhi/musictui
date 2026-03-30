from src.theme.base import ThemeColors


class MonokaiTheme(ThemeColors):
    def __init__(self):
        super().__init__(
            name="monokai",
            background="#272822",
            surface="#3e3d32",
            foreground="#f8f8f2",
            primary="#f92672",
            secondary="#ae81ff",
            accent="#66d9ef",
            success="#a6e22e",
            warning="#e6db74",
            error="#f92672",
            playing="#a6e22e",
            paused="#e6db74",
            stopped="#75715e",
            progress_bar="#f92672",
            progress_background="#49483e",
            border="#49483e",
            border_focus="#f92672",
        )
