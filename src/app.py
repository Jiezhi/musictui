import os
from textual.app import App
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from src.config import get_config, save_config
from src.player import Player
from src.library import Library
from src.ui.widgets.player_bar import PlayerBar
from src.ui.widgets.track_table import TrackTable
from src.ui.widgets.sidebar import Sidebar
from src.ui.widgets.context_menu import TrackContextMenu
from src.ui.settings import Settings
from src.ui.search import Search
from src.ui.status_bar import StatusBar
from src.ui.queue import Queue
from src.ui.command_input import CommandInput
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
    #sidebar-container {
        width: 20;
    }
    #sidebar {
        width: 100%;
        dock: left;
        border: solid $primary;
    }
    #track-table {
        width: 1fr;
        height: 100%;
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
    #queue, #search, #settings {
        width: 1fr;
        height: 100%;
    }
    #command-input {
        dock: bottom;
        height: 1;
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
        Binding("1", "show_library", "Library", show=False),
        Binding("2", "show_queue", "Queue", show=False),
        Binding("3", "show_search", "Search", show=False),
        Binding("4", "show_favorites", "Favorites", show=False),
        Binding("5", "show_settings", "Settings", show=False),
        Binding("l", "sidebar_up", "Sidebar Up", show=False),
        Binding("h", "sidebar_down", "Sidebar Down", show=False),
        Binding("+", "volume_up", "Vol+", show=False),
        Binding("=", "volume_up", "Vol+", show=False),
        Binding("-", "volume_down", "Vol-", show=False),
        Binding("_", "volume_down", "Vol-", show=False),
        Binding("backspace", "search_backspace", "Backspace", show=False),
        Binding("escape", "clear_search", "Clear", show=False),
        Binding("f", "add_favorite", "Favorite", show=False),
        Binding("u", "add_url", "Add URL", show=False),
        Binding("b", "add_to_blacklist", "Block", show=False),
        Binding(":", "start_command", "Command", show=False),
        Binding("pageup", "page_up", "Page Up", show=False),
        Binding("pagedown", "page_down", "Page Down", show=False),
        Binding("ctrl+b", "page_up", "Page Up", show=False),
        Binding("ctrl+f", "page_down", "Page Down", show=False),
    ]

    SEARCH_KEYS = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "-",
        "_",
        " ",
        ".",
        "@",
    ]

    COMMAND_KEYS = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "-",
        "_",
        ".",
        "/",
        ":",
    ]

    def compose(self):
        with Container(id="main-container"):
            with Horizontal():
                with Vertical(id="sidebar-container"):
                    yield Sidebar(id="sidebar")
                with Vertical(id="main-content"):
                    yield TrackTable(id="track-table")
            yield Settings(id="settings")
            yield Search(id="search")
            yield Queue(id="queue")
            yield CommandInput(id="command-input")
            yield PlayerBar(id="player-bar")
            yield StatusBar(id="status-bar")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_view = "library"

    def on_mount(self) -> None:
        self.config = get_config()
        self.player = Player()
        self.library = Library(os.path.expanduser("~/.musictui/music.db"))

        self._init_views()
        self._init_player()
        self._load_library()

    def on_track_table_track_selected(self, event) -> None:
        if event.track:
            self.push_screen(TrackContextMenu(event.track), self._handle_menu_action)

    def on_sidebar_item_clicked(self, event) -> None:
        """侧边栏项目点击"""
        if event.item == "Library":
            self.action_show_library()
        elif event.item == "Queue":
            self.action_show_queue()
        elif event.item == "Search":
            self.action_show_search()
        elif event.item == "Favorites":
            self.action_show_favorites()
        elif event.item == "Settings":
            self.action_show_settings()

    def _handle_menu_action(self, result) -> None:
        if result.action == "play":
            self.player.play(result.track)
        elif result.action == "queue":
            self.player.add_to_queue(result.track)
        elif result.action == "next":
            self.player.add_to_queue_front(result.track)
        elif result.action == "favorite":
            self.library.add_favorite(result.track.id)
        elif result.action == "blacklist":
            self.library.add_to_blacklist(result.track.id)

    def _init_views(self) -> None:
        settings = self.query_one("#settings", Settings)
        settings.values["Volume"] = self.config.player.volume
        settings.values["Play Mode"] = self.config.player.play_mode
        settings.values["Theme"] = self.config.ui.theme
        settings._update_content()
        settings.styles.display = "none"

        search = self.query_one("#search", Search)
        search.styles.display = "none"
        search.set_library(self.library)

        queue = self.query_one("#queue", Queue)
        queue.styles.display = "none"

        command_input = self.query_one("#command-input", CommandInput)
        command_input.styles.display = "none"

        self.command_mode = False
        self._add_search_key_bindings()
        self._add_command_key_bindings()

    def _init_player(self) -> None:
        self.player.set_volume(self.config.player.volume)
        if self.config.player.play_mode == "shuffle":
            self.player.set_play_mode(PlayMode.SHUFFLE)
        self.player.set_on_track_change(self._on_track_change)
        self.player.set_on_state_change(self._on_state_change)

    def _load_library(self) -> None:
        self.total_tracks = self.library.get_total_count()
        if self.total_tracks == 0:
            for path in self.config.library_paths:
                if os.path.exists(path):
                    self.library.scan_local(path)
            self.total_tracks = self.library.get_total_count()

        self.tracks = self.library.get_all_tracks(limit=50)
        self._update_track_table()

    def _update_track_table(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track_table.set_tracks(self.tracks)
            self.call_later(lambda: track_table.focus())
        except Exception as e:
            print(f"Error: {e}")
            self.set_timer(0.1, self._update_track_table)

    def _on_track_change(self, track) -> None:
        self.call_later(self._update_player_bar)
        if not hasattr(self, "_position_timer"):
            self._position_timer = self.set_interval(
                0.5, self._update_playback_position
            )

    def _on_state_change(self, state) -> None:
        self.call_later(self._update_player_bar)
        if state == PlayerState.STOPPED:
            if hasattr(self, "_position_timer"):
                self._position_timer.stop()

    def _update_playback_position(self) -> None:
        if self.player.state == PlayerState.PLAYING and self.player._current_sound:
            try:
                current_pos = self.player._current_sound.get_pos() / 1000.0
                self._update_player_bar(current_pos)
            except Exception:
                pass

    def _update_player_bar(self, current_time: float = 0.0) -> None:
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

    def action_play_pause(self) -> None:
        if self.player.state == PlayerState.PLAYING:
            self.player.pause()
        elif self.player.state == PlayerState.PAUSED:
            self.player.resume()
        else:
            track_table = self.query_one("#track-table", TrackTable)
            track = track_table.get_selected_track()
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
                track_table = self.query_one("#track-table", TrackTable)
                track_table.move_down()
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
                track_table = self.query_one("#track-table", TrackTable)
                track_table.move_up()
        except Exception:
            pass

    def action_play_selected(self) -> None:
        if self.command_mode:
            self._execute_command()
            return
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
                track_table = self.query_one("#track-table", TrackTable)
                track = track_table.get_selected_track()
                if track:
                    self.player.play(track)
        except Exception:
            pass

    def _apply_settings_change(self, settings) -> None:
        selected = settings.get_selected()
        if selected == "Volume":
            volume = settings.get_value("Volume")
            self.player.set_volume(volume)
            self.config.player.volume = volume
            save_config(self.config)
        elif selected == "Play Mode":
            settings.toggle_play_mode()
            mode = settings.get_value("Play Mode")
            if mode == "shuffle":
                self.player.set_play_mode(PlayMode.SHUFFLE)
            elif mode == "repeat_one":
                self.player.set_play_mode(PlayMode.SINGLE)
            else:
                self.player.set_play_mode(PlayMode.LOOP)
            self.config.player.play_mode = mode
            save_config(self.config)
        elif selected == "Theme":
            settings.cycle_theme()
            theme = settings.get_value("Theme")
            if theme == "nord":
                self.theme("nord")
            elif theme == "dracula":
                self.theme("dracula")
            else:
                self.theme("monokai")
            self.config.ui.theme = theme
            save_config(self.config)

    def action_volume_up(self) -> None:
        try:
            if self.current_view == "settings":
                settings = self.query_one("#settings", Settings)
                settings.adjust_volume(0.1)
            volume = self.player.volume + 0.1
            self.player.set_volume(min(1.0, volume))
            self.config.player.volume = self.player.volume
            save_config(self.config)
        except Exception:
            pass

    def action_volume_down(self) -> None:
        try:
            if self.current_view == "settings":
                settings = self.query_one("#settings", Settings)
                settings.adjust_volume(-0.1)
            volume = self.player.volume - 0.1
            self.player.set_volume(max(0.0, volume))
            self.config.player.volume = self.player.volume
            save_config(self.config)
        except Exception:
            pass

    def _add_search_key_bindings(self) -> None:
        for key in self.SEARCH_KEYS:
            self.BINDINGS.append(Binding(key, f"search_input_{key}", "", show=False))

    def _add_command_key_bindings(self) -> None:
        for key in self.COMMAND_KEYS:
            self.BINDINGS.append(Binding(key, f"command_input_{key}", "", show=False))

    def __getattr__(self, name: str):
        if name.startswith("action_search_input_"):
            key = name.replace("action_search_input_", "")
            return lambda: self._handle_search_input(key)
        if name.startswith("action_command_input_"):
            key = name.replace("action_command_input_", "")
            return lambda: self._handle_command_input(key)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def _handle_search_input(self, char: str) -> None:
        if self.current_view == "search":
            try:
                search = self.query_one("#search", Search)
                search.append_char(char)
            except Exception:
                pass

    def _handle_command_input(self, char: str) -> None:
        if self.command_mode:
            try:
                command_input = self.query_one("#command-input", CommandInput)
                command_input.append_char(char)
            except Exception:
                pass

    def action_search_backspace(self) -> None:
        if self.current_view == "search":
            try:
                search = self.query_one("#search", Search)
                search.backspace()
            except Exception:
                pass
        if self.command_mode:
            try:
                command_input = self.query_one("#command-input", CommandInput)
                command_input.backspace()
            except Exception:
                pass

    def action_clear_search(self) -> None:
        if self.command_mode:
            self._exit_command_mode()
            return
        if self.current_view == "search":
            try:
                search = self.query_one("#search", Search)
                search.clear()
            except Exception:
                pass

    def _exit_command_mode(self) -> None:
        self.command_mode = False
        try:
            command_input = self.query_one("#command-input", CommandInput)
            command_input.clear()
            command_input.styles.display = "none"
        except Exception:
            pass
        self._show_status_message("")

    def _execute_command(self) -> None:
        try:
            command_input = self.query_one("#command-input", CommandInput)
            command = command_input.get_command().strip()
        except Exception:
            return

        if not command:
            self._exit_command_mode()
            return

        parts = command.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "url":
            self._handle_url_command(arg)
        elif cmd == "scan":
            self._handle_scan_command(arg)
        else:
            self._show_status_message(f"Unknown command: {cmd}")

        self._exit_command_mode()

    def _handle_url_command(self, url: str) -> None:
        if not url:
            self._show_status_message("Usage: url <URL>")
            return

        self._show_status_message(f"Fetching songs from {url}...")
        try:
            tracks = self.library.fetch_remote_list(url)
            count = self.library.save_remote_tracks(tracks)
            self.total_tracks = self.library.get_total_count()
            self.tracks = self.library.get_all_tracks(limit=50)
            self._update_track_table()
            self._show_status_message(f"Added {count} songs from {url}")
        except ValueError as e:
            self._show_status_message(f"Error: {str(e)}")
        except Exception as e:
            self._show_status_message(f"Error: {str(e)}")

    def _handle_scan_command(self, path: str) -> None:
        if not path:
            self._show_status_message("Usage: scan <path>")
            return

        if not os.path.exists(path):
            self._show_status_message(f"Path not found: {path}")
            return

        self._show_status_message(f"Scanning {path}...")
        tracks = self.library.scan_local(path)
        self.total_tracks = self.library.get_total_count()
        self.tracks = self.library.get_all_tracks(limit=50)
        self._update_track_table()
        self._show_status_message(f"Scanned {len(tracks)} songs from {path}")

    def action_show_library(self) -> None:
        self.current_view = "library"
        try:
            self.total_tracks = self.library.get_total_count()
            self.tracks = self.library.get_all_tracks(limit=50)
            self._update_track_table()
            self._hide_other_views("#track-table")
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.set_selected(0)
        except Exception:
            pass

    def action_show_queue(self) -> None:
        self.current_view = "queue"
        try:
            self._hide_other_views("#queue")
            queue = self.query_one("#queue", Queue)
            queue.set_tracks(self.player.queue)
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.set_selected(1)
        except Exception:
            pass

    def action_show_search(self) -> None:
        self.current_view = "search"
        try:
            self._hide_other_views("#search")
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.set_selected(2)
        except Exception:
            pass

    def action_show_settings(self) -> None:
        self.current_view = "settings"
        try:
            self._hide_other_views("#settings")
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.set_selected(4)
        except Exception:
            pass

    def _hide_other_views(self, show_id: str) -> None:
        views = ["#track-table", "#settings", "#search", "#queue"]
        for vid in views:
            try:
                view = self.query_one(vid)
                view.styles.display = "block" if vid == show_id else "none"
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
            elif selected == "Favorites":
                self.action_show_favorites()
            elif selected == "Settings":
                self.action_show_settings()
        except Exception:
            pass

    def _show_status_message(self, message: str) -> None:
        try:
            status_bar = self.query_one("#status-bar", StatusBar)
            status_bar.update(message)
        except Exception:
            pass

    def action_add_favorite(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track = track_table.get_selected_track()
            if track and track.id:
                if self.library.add_favorite(track.id):
                    self._show_status_message(
                        f"Added to favorites: {track.display_name}"
                    )
                else:
                    self._show_status_message(
                        f"Already in favorites: {track.display_name}"
                    )
        except Exception:
            pass

    def action_add_url(self) -> None:
        self._show_status_message("Enter URL: (e.g., https://example.com/songs.js)")
        self._start_command_mode("url ")

    def _start_command_mode(self, initial_text: str = "") -> None:
        self.command_mode = True
        try:
            command_input = self.query_one("#command-input", CommandInput)
            command_input.set_command(initial_text)
            command_input.styles.display = "block"
        except Exception:
            pass

    def action_start_command(self) -> None:
        self._start_command_mode()

    def action_remove_favorite(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track = track_table.get_selected_track()
            if track and track.id:
                if self.library.remove_favorite(track.id):
                    self._show_status_message(
                        f"Removed from favorites: {track.display_name}"
                    )
                else:
                    self._show_status_message(f"Not in favorites: {track.display_name}")
        except Exception:
            pass

    def action_add_to_blacklist(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track = track_table.get_selected_track()
            if track and track.id:
                if self.library.add_to_blacklist(track.id):
                    self._show_status_message(
                        f"Added to blacklist: {track.display_name}"
                    )
                    if (
                        self.player.get_current_track()
                        and self.player.get_current_track().id == track.id
                    ):
                        self.player.next()
                else:
                    self._show_status_message(
                        f"Already in blacklist: {track.display_name}"
                    )
        except Exception:
            pass

    def action_page_up(self) -> None:
        try:
            if self.current_view == "settings":
                settings = self.query_one("#settings", Settings)
                for _ in range(5):
                    settings.move_up()
            elif self.current_view == "search":
                search = self.query_one("#search", Search)
                search.page_up()
            elif self.current_view == "queue":
                queue = self.query_one("#queue", Queue)
                queue.page_up()
            else:
                track_table = self.query_one("#track-table", TrackTable)
                track_table.move_up()
        except Exception:
            pass

    def action_page_down(self) -> None:
        try:
            if self.current_view == "settings":
                settings = self.query_one("#settings", Settings)
                for _ in range(5):
                    settings.move_down()
            elif self.current_view == "search":
                search = self.query_one("#search", Search)
                search.page_down()
            elif self.current_view == "queue":
                queue = self.query_one("#queue", Queue)
                queue.page_down()
            else:
                track_table = self.query_one("#track-table", TrackTable)
                track_table.move_down()
        except Exception:
            pass

    def action_show_favorites(self) -> None:
        self.current_view = "favorites"
        try:
            self._hide_other_views("#track-table")
            favorites = self.library.get_favorites()
            track_table = self.query_one("#track-table", TrackTable)
            track_table.set_tracks(favorites)
            sidebar = self.query_one("#sidebar", Sidebar)
            sidebar.set_selected(3)
        except Exception:
            pass
