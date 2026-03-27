from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static
from src.ui.sidebar import Sidebar
from src.ui.track_list import TrackList
from src.ui.player_bar import PlayerBar
from src.ui.status_bar import StatusBar


class MainScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref

    def compose(self):
        yield Container(
            Horizontal(
                Vertical(
                    Sidebar(id="sidebar"),
                    id="sidebar-container",
                ),
                Vertical(
                    TrackList(id="track-list"),
                    id="main-content",
                ),
                id="main-area",
            ),
            PlayerBar(id="player-bar"),
            StatusBar(id="status-bar"),
            id="main-container",
        )

    def on_mount(self) -> None:
        self.app = self.app_ref
