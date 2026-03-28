from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from src.ui.sidebar import Sidebar
from src.ui.track_list import TrackList
from src.ui.player_bar import PlayerBar
from src.ui.status_bar import StatusBar


class MainScreen(Screen):
    def compose(self):
        yield Container(
            Sidebar(id="sidebar"),
            TrackList(id="track-list"),
            PlayerBar(id="player-bar"),
            StatusBar(id="status-bar"),
        )
