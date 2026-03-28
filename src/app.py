import os
from textual.app import App
from textual import work
from src.config import get_config
from src.player import Player
from src.library import Library
from src.ui.main_screen import MainScreen
from src.ui.player_bar import PlayerBar
from src.ui.track_list import TrackList
from src.models import PlayerState, PlayMode


class MusicTUI(App):
    CSS = """
    Screen {
        background: $surface;
    }
    #main-container {
        height: 100%;
    }
    #main-area {
        height: 100%;
    }
    #sidebar-container {
        width: 20;
        border: solid $primary;
    }
    #main-content {
        width: 80;
    }
    #player-bar {
        height: 3;
        border-top: solid $primary;
        background: $surface-darken-1;
    }
    #status-bar {
        height: 1;
        background: $accent;
        color: $text;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = get_config()
        self.player = Player()
        self.library = Library(os.path.expanduser("~/.musictui/music.db"))
        self.player.set_volume(self.config.player.volume)
        if self.config.player.play_mode == "shuffle":
            self.player.set_play_mode(PlayMode.SHUFFLE)

        self.player.set_on_track_change(self._on_track_change)
        self.player.set_on_state_change(self._on_state_change)

    def _on_track_change(self, track):
        self.call_later(self._update_player_bar)

    def _on_state_change(self, state):
        self.call_later(self._update_player_bar)

    def _update_player_bar(self):
        player_bar = self.query_one("#player-bar", PlayerBar)
        current = self.player.get_current_track()
        if current:
            player_bar.update_track(
                current.title, current.artist, 0.0, current.duration
            )
        else:
            player_bar.update_track("No track", "", 0.0, 0.0)

    def on_mount(self) -> None:
        self.install_screen(MainScreen(self), "main")
        self.push_screen("main")
        self.call_later(self._load_library)

    def _load_library(self):
        tracks = self.library.get_all_tracks()
        track_list = self.query_one("#track-list", TrackList)
        track_list.set_tracks(tracks)

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

    def action_scan(self, path: str) -> None:
        tracks = self.library.scan_local(path)
        track_list = self.query_one("#track-list", TrackList)
        track_list.set_tracks(self.library.get_all_tracks())

    def on_key(self, event) -> None:
        if event.key == "space":
            self.action_play_pause()
            event.prevent_default()
        elif event.key == "n":
            self.action_next()
        elif event.key == "p":
            self.action_previous()
        elif event.key == "q":
            self.action_quit()
        elif event.key == "j":
            track_list = self.query_one("#track-list", TrackList)
            track_list.move_down()
        elif event.key == "k":
            track_list = self.query_one("#track-list", TrackList)
            track_list.move_up()
        elif event.key == "enter":
            track_list = self.query_one("#track-list", TrackList)
            track = track_list.get_selected_track()
            if track:
                self.player.play(track)
        super().on_key(event)
