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
from src.ui.settings import Settings
from src.ui.search import Search
from src.ui.status_bar import StatusBar
from src.ui.queue import Queue
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
    #queue {
        width: 1fr;
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
        Binding("1", "show_library", "Library", show=False),
        Binding("2", "show_queue", "Queue", show=False),
        Binding("3", "show_search", "Search", show=False),
        Binding("4", "show_settings", "Settings", show=False),
        Binding("l", "sidebar_up", "Sidebar Up", show=False),
        Binding("h", "sidebar_down", "Sidebar Down", show=False),
        Binding("+", "volume_up", "Vol+", show=False),
        Binding("-", "volume_down", "Vol-", show=False),
    ]

    def compose(self):
        with Container(id="main-container"):
            yield Sidebar(id="sidebar")
            yield TrackList(id="track-list")
            yield Settings(id="settings")
            yield Search(id="search")
            yield Queue(id="queue")
            yield PlayerBar(id="player-bar")
            yield StatusBar(id="status-bar")

    def _on_track_change(self, track):
        self.call_later(self._update_player_bar)
        if not hasattr(self, "_position_timer"):
            self._position_timer = self.set_interval(
                0.5, self._update_playback_position
            )

    def _on_state_change(self, state):
        self.call_later(self._update_player_bar)
        if state == PlayerState.STOPPED:
            if hasattr(self, "_position_timer"):
                self._position_timer.stop()

    def _update_playback_position(self):
        if self.player.state == PlayerState.PLAYING and self.player._current_sound:
            try:
                current_pos = self.player._current_sound.get_pos() / 1000.0
                self._update_player_bar(current_pos)
            except Exception:
                pass

    def _update_player_bar(self, current_time: float = 0.0):
        try:
            player_bar = self.query_one("#player-bar", PlayerBar)
            current = self.player.get_current_track()
            if current:
                player_bar.update_track(
                    current.title, current.artist, current_time, current.duration
                )
            else:
                player_bar.update_track("No track", "", 0.0, 0.0)
        except Exception:
            pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_view = "library"

    def on_mount(self) -> None:
        self.config = get_config()
        self.player = Player()
        self.library = Library(os.path.expanduser("~/.musictui/music.db"))

        settings = self.query_one("#settings", Settings)
        settings.styles.display = "none"

        search = self.query_one("#search", Search)
        search.styles.display = "none"

        queue = self.query_one("#queue", Queue)
        queue.styles.display = "none"

        self.total_tracks = self.library.get_total_count()
        if self.total_tracks == 0:
            for path in self.config.library_paths:
                if os.path.exists(path):
                    self.library.scan_local(path)
            self.total_tracks = self.library.get_total_count()

        self.tracks = self.library.get_all_tracks(limit=50)

        self.player.set_volume(self.config.player.volume)
        if self.config.player.play_mode == "shuffle":
            self.player.set_play_mode(PlayMode.SHUFFLE)

        self.player.set_on_track_change(self._on_track_change)
        self.player.set_on_state_change(self._on_state_change)

        self._load_library()

    def _load_library(self):
        try:
            track_list = self.query_one("#track-list", TrackList)
            track_list.set_tracks(self.tracks, self.total_tracks)
            track_list.set_load_more_callback(self._load_more_tracks)
        except Exception as e:
            print(f"Error: {e}")
            self.set_timer(0.1, self._load_library)

    def _load_more_tracks(self):
        new_tracks = self.library.get_all_tracks(offset=len(self.tracks), limit=50)
        if new_tracks:
            self.tracks.extend(new_tracks)
            try:
                track_list = self.query_one("#track-list", TrackList)
                track_list.append_tracks(new_tracks)
            except Exception:
                pass

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
            if self.current_view == "settings":
                settings = self.query_one("#settings", Settings)
                settings.move_down()
            elif self.current_view == "search":
                search = self.query_one("#search", Search)
                search.move_down()
            elif self.current_view == "queue":
                queue = self.query_one("#queue", Queue)
                queue.move_down()
            else:
                track_list = self.query_one("#track-list", TrackList)
                track_list.move_down()
        except Exception:
            pass

    def action_move_up(self) -> None:
        try:
            if self.current_view == "settings":
                settings = self.query_one("#settings", Settings)
                settings.move_up()
            elif self.current_view == "search":
                search = self.query_one("#search", Search)
                search.move_up()
            elif self.current_view == "queue":
                queue = self.query_one("#queue", Queue)
                queue.move_up()
            else:
                track_list = self.query_one("#track-list", TrackList)
                track_list.move_up()
        except Exception:
            pass

    def _apply_volume_change(self, settings) -> None:
        volume = settings.get_value("Volume")
        self.player.set_volume(volume)

    def action_play_selected(self) -> None:
        try:
            if self.current_view == "settings":
                settings = self.query_one("#settings", Settings)
                self._apply_settings_change(settings)
            elif self.current_view == "search":
                search = self.query_one("#search", Search)
                track = search.get_selected_track()
                if track:
                    self.player.play(track)
            else:
                track_list = self.query_one("#track-list", TrackList)
                track = track_list.get_selected_track()
                if track:
                    self.player.play(track)
        except Exception:
            pass

    def _apply_settings_change(self, settings) -> None:
        selected = settings.get_selected()
        if selected == "Volume":
            pass
        elif selected == "Play Mode":
            mode = settings.get_value("Play Mode")
            if mode == "shuffle":
                self.player.set_play_mode(PlayMode.SHUFFLE)
            elif mode == "repeat_one":
                self.player.set_play_mode(PlayMode.SINGLE)
            else:
                self.player.set_play_mode(PlayMode.LOOP)
        elif selected == "Theme":
            theme = settings.get_value("Theme")
            if theme == "nord":
                self.theme = "nord"
            elif theme == "dracula":
                self.theme = "dracula"
            else:
                self.theme = "monokai"

    def action_volume_up(self) -> None:
        try:
            settings = self.query_one("#settings", Settings)
            settings.adjust_volume(0.1)
            volume = settings.get_value("Volume")
            self.player.set_volume(volume)
        except Exception:
            pass

    def action_volume_down(self) -> None:
        try:
            settings = self.query_one("#settings", Settings)
            settings.adjust_volume(-0.1)
            volume = settings.get_value("Volume")
            self.player.set_volume(volume)
        except Exception:
            pass

    def action_scan(self, path: str) -> None:
        tracks = self.library.scan_local(path)
        self.total_tracks = self.library.get_total_count()
        self.tracks = self.library.get_all_tracks(limit=50)
        track_list = self.query_one("#track-list", TrackList)
        track_list.set_tracks(self.tracks, self.total_tracks)

    def action_show_library(self) -> None:
        self.current_view = "library"
        try:
            track_list = self.query_one("#track-list", TrackList)
            track_list.styles.display = "block"
            settings = self.query_one("#settings", Settings)
            settings.styles.display = "none"
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.selected = 0
            sidebar._update_content()
        except Exception:
            pass

    def action_show_queue(self) -> None:
        self.current_view = "queue"
        try:
            track_list = self.query_one("#track-list", TrackList)
            track_list.styles.display = "none"
            settings = self.query_one("#settings", Settings)
            settings.styles.display = "none"
            search = self.query_one("#search", Search)
            search.styles.display = "none"
            queue = self.query_one("#queue", Queue)
            queue.set_tracks(self.player.queue)
            queue.styles.display = "block"
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.selected = 1
            sidebar._update_content()
        except Exception:
            pass

    def action_show_search(self) -> None:
        self.current_view = "search"
        try:
            track_list = self.query_one("#track-list", TrackList)
            track_list.styles.display = "none"
            settings = self.query_one("#settings", Settings)
            settings.styles.display = "none"
            search = self.query_one("#search", Search)
            search.styles.display = "block"
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.selected = 2
            sidebar._update_content()
        except Exception:
            pass

    def action_show_settings(self) -> None:
        self.current_view = "settings"
        try:
            track_list = self.query_one("#track-list", TrackList)
            track_list.styles.display = "none"
            settings = self.query_one("#settings", Settings)
            settings.styles.display = "block"
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.selected = 3
            sidebar._update_content()
        except Exception:
            pass

    def action_sidebar_up(self) -> None:
        try:
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.move_up()
            self._on_sidebar_change()
        except Exception:
            pass

    def action_sidebar_down(self) -> None:
        try:
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.move_down()
            self._on_sidebar_change()
        except Exception:
            pass

    def _on_sidebar_change(self) -> None:
        try:
            sidebar = self.query_one("#sidebar", Sidebar)
            selected = sidebar.get_selected()
            if selected == "Library":
                self.action_show_library()
            elif selected == "Queue":
                self.action_show_queue()
            elif selected == "Search":
                self.action_show_search()
            elif selected == "Settings":
                self.action_show_settings()
        except Exception:
            pass
