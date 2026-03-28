import os
from textual.app import App
from textual import work
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from src.config import get_config
from src.player import Player
from src.library import Library
from src.ui.player_bar import PlayerBar
from src.ui.track_list import TrackList
from src.ui.sidebar import Sidebar
from src.ui.status_bar import StatusBar
from src.models import PlayerState, PlayMode


class MusicTUI(App):
    CSS = """
    Screen {
        background: $surface;
    }
    #main-container {
        width: 100%;
        height: 100%;
    }
    #sidebar {
        width: 20;
        dock: left;
        border: solid $primary;
    }
    #track-list {
        width: 1fr;
    }
    #player-bar {
        height: 3;
        dock: bottom;
        border-top: solid $primary;
    }
    #status-bar {
        height: 1;
        dock: bottom;
        background: $accent;
    }
    """

    BINDINGS = [
        Binding("space", "play_pause", "Play/Pause", show=False),
        Binding("n", "next", "Next", show=False),
        Binding("p", "previous", "Prev", show=False),
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
        Binding("enter", "play_selected", "Play", show=False),
        Binding("q", "quit", "Quit", show=False),
    ]

    def compose(self):
        with Container(id="main-container"):
            yield Sidebar(id="sidebar")
            yield TrackList(id="track-list")
            yield PlayerBar(id="player-bar")
            yield StatusBar(id="status-bar")

    def _on_track_change(self, track):
        self.call_later(self._update_player_bar)

    def _on_state_change(self, state):
        self.call_later(self._update_player_bar)

    def _update_player_bar(self):
        try:
            player_bar = self.query_one("#player-bar", PlayerBar)
            current = self.player.get_current_track()
            if current:
                player_bar.update_track(
                    current.title, current.artist, 0.0, current.duration
                )
            else:
                player_bar.update_track("No track", "", 0.0, 0.0)
        except Exception:
            pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_mount(self) -> None:
        self.config = get_config()
        self.player = Player()
        self.library = Library(os.path.expanduser("~/.musictui/music.db"))

        for path in self.config.library_paths:
            if os.path.exists(path):
                self.library.scan_local(path)

        self.tracks = self.library.get_all_tracks()

        self.player.set_volume(self.config.player.volume)
        if self.config.player.play_mode == "shuffle":
            self.player.set_play_mode(PlayMode.SHUFFLE)

        self.player.set_on_track_change(self._on_track_change)
        self.player.set_on_state_change(self._on_state_change)

        self._load_library()

    def _load_library(self):
        try:
            track_list = self.query_one("#track-list", TrackList)
            track_list.set_tracks(self.tracks)
        except Exception as e:
            print(f"Error: {e}")
            self.set_timer(0.1, self._load_library)

    def action_play_pause(self) -> None:
        if self.player.state == PlayerState.PLAYING:
            self.player.pause()
        elif self.player.state == PlayerState.PAUSED:
            self.player.resume()
        else:
            track_list = self.query_one("#track-list", TrackList)
            track = track_list.get_selected_track()
            if track:
                self.player.play(track)

    def action_next(self) -> None:
        self.player.next()

    def action_previous(self) -> None:
        self.player.previous()

    def action_quit(self) -> None:
        self.player.stop()
        self.exit()

    def action_move_down(self) -> None:
        try:
            track_list = self.query_one("#track-list", TrackList)
            track_list.move_down()
        except Exception:
            pass

    def action_move_up(self) -> None:
        try:
            track_list = self.query_one("#track-list", TrackList)
            track_list.move_up()
        except Exception:
            pass

    def action_play_selected(self) -> None:
        try:
            track_list = self.query_one("#track-list", TrackList)
            track = track_list.get_selected_track()
            if track:
                self.player.play(track)
        except Exception:
            pass

    def action_scan(self, path: str) -> None:
        tracks = self.library.scan_local(path)
        track_list = self.query_one("#track-list", TrackList)
        track_list.set_tracks(self.library.get_all_tracks())
