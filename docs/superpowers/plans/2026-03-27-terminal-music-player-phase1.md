# Terminal Music Player - Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a working MVP with basic TUI framework, player core, and local music scanning capability.

**Architecture:** Use Textual as the TUI framework with pygame.mixer for audio playback. Separate concerns: UI layer (Textual), business logic (Player, Library), data layer (SQLite).

**Tech Stack:** Python 3.9+, Textual, pygame.mixer, SQLite, mutagen

---

## File Structure

```
musictui/
├── src/
│   ├── __init__.py
│   ├── app.py              # Main application entry
│   ├── player.py           # Audio player core
│   ├── library.py          # Music library management
│   ├── config.py           # Configuration management
│   ├── models.py           # Data models (Track, Playlist, etc.)
│   └── ui/
│       ├── __init__.py
│       ├── main_screen.py  # Main screen layout
│       ├── sidebar.py      # Sidebar navigation
│       ├── track_list.py   # Track list widget
│       ├── player_bar.py   # Player control bar
│       └── status_bar.py   # Status bar
├── data/
│   └── music.db            # SQLite database (auto-created)
├── config/
│   └── settings.json       # Configuration file (auto-created)
├── tests/
│   ├── __init__.py
│   ├── test_player.py
│   └── test_library.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Task 1: Project Setup

**Files:**
- Create: `requirements.txt`
- Create: `pyproject.toml`
- Create: `src/__init__.py`
- Create: `src/models.py`

- [ ] **Step 1: Create requirements.txt**

```txt
textual>=0.40.0
pygame>=2.5.0
mutagen>=1.47.0
pydantic>=2.0.0
pytest>=7.0.0
```

- [ ] **Step 2: Create pyproject.toml**

```toml
[project]
name = "musictui"
version = "0.1.0"
description = "A terminal-based music player with Vim-style interface"
requires-python = ">=3.9"
dependencies = [
    "textual>=0.40.0",
    "pygame>=2.5.0",
    "mutagen>=1.47.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

- [ ] **Step 3: Create src/models.py**

```python
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


class PlayerState(Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class PlayMode(Enum):
    LOOP = "loop"
    SHUFFLE = "shuffle"
    SINGLE = "single"


@dataclass
class Track:
    id: Optional[int] = None
    file_path: str = ""
    title: str = ""
    artist: str = ""
    album: str = ""
    duration: float = 0.0
    genre: str = ""
    year: Optional[int] = None
    track_number: Optional[int] = None

    @property
    def display_name(self) -> str:
        if self.title:
            return f"{self.artist} - {self.title}" if self.artist else self.title
        return Path(self.file_path).stem


@dataclass
class Playlist:
    id: Optional[int] = None
    name: str = ""
    track_ids: list[int] = None

    def __post_init__(self):
        if self.track_ids is None:
            self.track_ids = []
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt pyproject.toml src/__init__.py src/models.py
git commit -m "chore: project setup with dependencies and models"
```

---

## Task 2: Configuration Management

**Files:**
- Create: `src/config.py`
- Create: `config/settings.json`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_config.py
import pytest
from src.config import Config, get_config


def test_config_default_values():
    config = Config()
    assert config.library_paths == []
    assert config.player.volume == 0.7
    assert config.player.play_mode == "loop"


def test_config_loads_from_file():
    config = get_config()
    assert config is not None
    assert hasattr(config, 'library_paths')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src'"

- [ ] **Step 3: Create tests/__init__.py and tests/test_config.py**

```python
# tests/__init__.py
```

```python
# tests/test_config.py
import pytest
from src.config import Config, get_config


def test_config_default_values():
    config = Config()
    assert config.library_paths == []
    assert config.player.volume == 0.7
    assert config.player.play_mode == "loop"


def test_config_loads_from_file():
    config = get_config()
    assert config is not None
    assert hasattr(config, 'library_paths')
```

- [ ] **Step 4: Run test to verify it fails**

Run: `pytest tests/test_config.py -v`
Expected: FAIL with "Config" not defined

- [ ] **Step 5: Create src/config.py**

```python
import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class PlayerConfig(BaseModel):
    volume: float = 0.7
    play_mode: str = "loop"


class WebDAVConfig(BaseModel):
    enabled: bool = False
    url: str = ""
    username: str = ""
    password: str = ""


class UIConfig(BaseModel):
    theme: str = "monokai"


class Config(BaseModel):
    library_paths: list[str] = Field(default_factory=list)
    webdav: WebDAVConfig = Field(default_factory=WebDAVConfig)
    player: PlayerConfig = Field(default_factory=PlayerConfig)
    ui: UIConfig = Field(default_factory=UIConfig)


_config: Optional[Config] = None


def get_config(config_path: Optional[Path] = None) -> Config:
    global _config
    if _config is not None:
        return _config

    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "settings.json"

    if config_path.exists():
        with open(config_path) as f:
            data = json.load(f)
            _config = Config(**data)
    else:
        _config = Config()
        save_config(_config, config_path)

    return _config


def save_config(config: Config, config_path: Optional[Path] = None) -> None:
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "settings.json"

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config.model_dump(), f, indent=2)
```

- [ ] **Step 6: Create config/settings.json**

```json
{
  "library_paths": [],
  "webdav": {
    "enabled": false,
    "url": "",
    "username": "",
    "password": ""
  },
  "player": {
    "volume": 0.7,
    "play_mode": "loop"
  },
  "ui": {
    "theme": "monokai"
  }
}
```

- [ ] **Step 7: Run test to verify it passes**

Run: `pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add src/config.py config/settings.json tests/test_config.py tests/__init__.py
git commit -m "feat: add configuration management"
```

---

## Task 3: Player Core

**Files:**
- Create: `src/player.py`
- Test: `tests/test_player.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_player.py
import pytest
from src.player import Player
from src.models import Track, PlayerState, PlayMode


def test_player_initial_state():
    player = Player()
    assert player.state == PlayerState.STOPPED
    assert player.volume == 0.7
    assert player.play_mode == PlayMode.LOOP
    assert player.queue == []


def test_player_add_to_queue():
    player = Player()
    track = Track(file_path="/test.mp3", title="Test Song")
    player.add_to_queue(track)
    assert len(player.queue) == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_player.py -v`
Expected: FAIL with "No module named 'src.player'"

- [ ] **Step 3: Create src/player.py**

```python
import pygame
from typing import Optional, Callable
from src.models import Track, PlayerState, PlayMode


class Player:
    def __init__(self):
        self.queue: list[Track] = []
        self.current_index: int = -1
        self.state: PlayerState = PlayerState.STOPPED
        self.volume: float = 0.7
        self.play_mode: PlayMode = PlayMode.LOOP
        self.position: float = 0.0
        self._current_sound: Optional[pygame.mixer.Sound] = None
        self._on_track_change: Optional[Callable[[Track], None]] = None
        self._on_state_change: Optional[Callable[[PlayerState], None]] = None
        pygame.mixer.init()

    def set_on_track_change(self, callback: Callable[[Track], None]) -> None:
        self._on_track_change = callback

    def set_on_state_change(self, callback: Callable[[PlayerState], None]) -> None:
        self._on_state_change = callback

    def add_to_queue(self, track: Track) -> None:
        self.queue.append(track)

    def add_to_queue_front(self, track: Track) -> None:
        self.queue.insert(0, track)

    def clear_queue(self) -> None:
        self.queue.clear()
        self.current_index = -1

    def play(self, track: Optional[Track] = None) -> None:
        if track:
            self.add_to_queue(track)
            self.current_index = len(self.queue) - 1

        if self.current_index < 0 or self.current_index >= len(self.queue):
            return

        self._load_and_play(self.queue[self.current_index])

    def _load_and_play(self, track: Track) -> None:
        try:
            if self._current_sound:
                self._current_sound.stop()
            self._current_sound = pygame.mixer.Sound(track.file_path)
            self._current_sound.set_volume(self.volume)
            self._current_sound.play()
            self.state = PlayerState.PLAYING
            if self._on_track_change:
                self._on_track_change(track)
            if self._on_state_change:
                self._on_state_change(self.state)
        except Exception as e:
            print(f"Error playing track: {e}")
            self.next()

    def pause(self) -> None:
        if self.state == PlayerState.PLAYING:
            pygame.mixer.pause()
            self.state = PlayerState.PAUSED
            if self._on_state_change:
                self._on_state_change(self.state)

    def resume(self) -> None:
        if self.state == PlayerState.PAUSED:
            pygame.mixer.unpause()
            self.state = PlayerState.PLAYING
            if self._on_state_change:
                self._on_state_change(self.state)

    def stop(self) -> None:
        pygame.mixer.stop()
        self.state = PlayerState.STOPPED
        if self._on_state_change:
            self._on_state_change(self.state)

    def next(self) -> None:
        if not self.queue:
            return

        if self.play_mode == PlayMode.SHUFFLE:
            import random
            self.current_index = random.randint(0, len(self.queue) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.queue)

        if self.state == PlayerState.PLAYING:
            self._load_and_play(self.queue[self.current_index])

    def previous(self) -> None:
        if not self.queue:
            return

        self.current_index = (self.current_index - 1) % len(self.queue)

        if self.state == PlayerState.PLAYING:
            self._load_and_play(self.queue[self.current_index])

    def seek(self, position: float) -> None:
        self.position = position

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))
        if self._current_sound:
            self._current_sound.set_volume(self.volume)

    def set_play_mode(self, mode: PlayMode) -> None:
        self.play_mode = mode

    def get_current_track(self) -> Optional[Track]:
        if 0 <= self.current_index < len(self.queue):
            return self.queue[self.current_index]
        return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_player.py -v`
Expected: PASS (or SKIP pygame init in test environment)

- [ ] **Step 5: Commit**

```bash
git add src/player.py tests/test_player.py
git commit -m "feat: add player core with queue management"
```

---

## Task 4: Library Management

**Files:**
- Create: `src/library.py`
- Create: `tests/test_library.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_library.py
import pytest
from src.library import Library
from src.models import Track


def test_library_initialization(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))
    tracks = library.get_all_tracks()
    assert tracks == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_library.py -v`
Expected: FAIL with "No module named 'src.library'"

- [ ] **Step 3: Create src/library.py**

```python
import sqlite3
from pathlib import Path
from typing import Optional
from mutagen import File as MutagenFile
from src.models import Track


class Library:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                title TEXT,
                artist TEXT,
                album TEXT,
                duration REAL DEFAULT 0.0,
                genre TEXT,
                year INTEGER,
                track_number INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        return conn

    def scan_local(self, path: str) -> list[Track]:
        music_extensions = {'.mp3', '.flac', '.wav', '.ogg', '.m4a', '.wma'}
        tracks = []

        for file_path in Path(path).rglob('*'):
            if file_path.suffix.lower() in music_extensions:
                track = self._extract_metadata(file_path)
                self._save_track(track)
                tracks.append(track)

        return tracks

    def _extract_metadata(self, file_path: Path) -> Track:
        try:
            audio = MutagenFile(file_path)
            if audio is None:
                return Track(file_path=str(file_path), title=file_path.stem)

            tags = audio.tags or {}
            return Track(
                file_path=str(file_path),
                title=tags.get('title', [file_path.stem])[0] if tags else file_path.stem,
                artist=tags.get('artist', [''])[0] if tags else '',
                album=tags.get('album', [''])[0] if tags else '',
                duration=float(audio.info.length) if audio.info else 0.0,
                genre=tags.get('genre', [''])[0] if tags else '',
                year=int(tags.get('date', ['0'])[0][:4]) if tags and tags.get('date') else None,
                track_number=int(tags.get('tracknumber', [0])[0]) if tags else None,
            )
        except Exception:
            return Track(file_path=str(file_path), title=file_path.stem)

    def _save_track(self, track: Track) -> None:
        conn = self._get_connection()
        cursor = conn.execute(
            """INSERT OR REPLACE INTO tracks 
               (file_path, title, artist, album, duration, genre, year, track_number)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (track.file_path, track.title, track.artist, track.album,
             track.duration, track.genre, track.year, track.track_number)
        )
        track.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def get_all_tracks(self) -> list[Track]:
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT id, file_path, title, artist, album, duration, genre, year, track_number FROM tracks"
        )
        tracks = []
        for row in cursor.fetchall():
            tracks.append(Track(
                id=row[0], file_path=row[1], title=row[2], artist=row[3],
                album=row[4], duration=row[5], genre=row[6], year=row[7], track_number=row[8]
            ))
        conn.close()
        return tracks

    def search(self, query: str) -> list[Track]:
        conn = self._get_connection()
        pattern = f"%{query}%"
        cursor = conn.execute(
            """SELECT id, file_path, title, artist, album, duration, genre, year, track_number 
               FROM tracks 
               WHERE title LIKE ? OR artist LIKE ? OR album LIKE ?""",
            (pattern, pattern, pattern)
        )
        tracks = []
        for row in cursor.fetchall():
            tracks.append(Track(
                id=row[0], file_path=row[1], title=row[2], artist=row[3],
                album=row[4], duration=row[5], genre=row[6], year=row[7], track_number=row[8]
            ))
        conn.close()
        return tracks

    def get_track_by_id(self, track_id: int) -> Optional[Track]:
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT id, file_path, title, artist, album, duration, genre, year, track_number FROM tracks WHERE id = ?",
            (track_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return Track(
                id=row[0], file_path=row[1], title=row[2], artist=row[3],
                album=row[4], duration=row[5], genre=row[6], year=row[7], track_number=row[8]
            )
        return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_library.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/library.py tests/test_library.py
git commit -m "feat: add library management with local scanning"
```

---

## Task 5: UI Framework

**Files:**
- Create: `src/ui/__init__.py`
- Create: `src/ui/main_screen.py`
- Create: `src/ui/sidebar.py`
- Create: `src/ui/track_list.py`
- Create: `src/ui/player_bar.py`
- Create: `src/ui/status_bar.py`

- [ ] **Step 1: Create src/ui/__init__.py**

```python
from .main_screen import MainScreen
from .sidebar import Sidebar
from .track_list import TrackList
from .player_bar import PlayerBar
from .status_bar import StatusBar

__all__ = ["MainScreen", "Sidebar", "TrackList", "PlayerBar", "StatusBar"]
```

- [ ] **Step 2: Create src/ui/player_bar.py**

```python
from textual.widget import Widget
from textual.widgets import Static


class PlayerBar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.track_title = ""
        self.track_artist = ""
        self.current_time = 0.0
        self.total_time = 0.0

    def render(self) -> str:
        status = "▶"
        progress = "━" * 20
        return f"{status} {self.track_title} - {self.track_artist}  {self._format_time(self.current_time)}/{self._format_time(self.total_time)}\n[{progress}]"

    def _format_time(self, seconds: float) -> str:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def update_track(self, title: str, artist: str, current: float, total: float) -> None:
        self.track_title = title
        self.track_artist = artist
        self.current_time = current
        self.total_time = total
        self.refresh()
```

- [ ] **Step 3: Create src/ui/status_bar.py**

```python
from textual.widget import Widget


class StatusBar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self) -> str:
        return "NORMAL │ q:quit  space:play/pause  n:next  p:prev  /:search"
```

- [ ] **Step 4: Create src/ui/sidebar.py**

```python
from textual.widget import Widget
from textual.widgets import Static


class Sidebar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["Library", "Queue", "Search", "Settings"]
        self.selected = 0

    def render(self) -> str:
        lines = [f"  {item}" if i != self.selected else f"> {item}" for i, item in enumerate(self.items)]
        return "\n".join(lines)

    def move_up(self) -> None:
        self.selected = (self.selected - 1) % len(self.items)
        self.refresh()

    def move_down(self) -> None:
        self.selected = (self.selected + 1) % len(self.items)
        self.refresh()

    def get_selected(self) -> str:
        return self.items[self.selected]
```

- [ ] **Step 5: Create src/ui/track_list.py**

```python
from textual.widget import Widget
from src.models import Track


class TrackList(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracks: list[Track] = []
        self.selected_index = 0

    def render(self) -> str:
        if not self.tracks:
            return "No tracks in library. Use :scan <path> to add music."

        lines = []
        for i, track in enumerate(self.tracks):
            prefix = "> " if i == self.selected_index else "  "
            lines.append(f"{prefix}{track.display_name}")
        return "\n".join(lines)

    def set_tracks(self, tracks: list[Track]) -> None:
        self.tracks = tracks
        self.selected_index = 0
        self.refresh()

    def move_up(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index - 1) % len(self.tracks)
            self.refresh()

    def move_down(self) -> None:
        if self.tracks:
            self.selected_index = (self.selected_index + 1) % len(self.tracks)
            self.refresh()

    def get_selected_track(self) -> Track:
        if 0 <= self.selected_index < len(self.tracks):
            return self.tracks[self.selected_index]
        return None
```

- [ ] **Step 6: Create src/ui/main_screen.py**

```python
from textual.app import Compose
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

    def compose(self) -> Compose:
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
```

- [ ] **Step 7: Commit**

```bash
git add src/ui/__init__.py src/ui/main_screen.py src/ui/sidebar.py src/ui/track_list.py src/ui/player_bar.py src/ui/status_bar.py
git commit -m "feat: add UI framework with Textual"
```

---

## Task 6: Main Application

**Files:**
- Create: `src/app.py`

- [ ] **Step 1: Create src/app.py**

```python
import os
from textual.app import App
from textual import work
from src.config import get_config
from src.player import Player
from src.library import Library
from src.ui.main_screen import MainScreen
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
            player_bar.update_track(current.title, current.artist, 0.0, current.duration)
        else:
            player_bar.update_track("No track", "", 0.0, 0.0)

    def on_mount(self) -> None:
        self.install_screen(MainScreen(self), "main")
        self.push_screen("main")
        self._load_library()

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
```

- [ ] **Step 2: Create src/__init__.py (if not exists)**

```python
```

- [ ] **Step 3: Commit**

```bash
git add src/app.py
git commit -m "feat: add main application entry point"
```

---

## Task 7: Entry Point and Testing

**Files:**
- Create: `src/__main__.py`
- Create: `README.md`

- [ ] **Step 1: Create src/__main__.py**

```python
from src.app import MusicTUI


def main():
    app = MusicTUI()
    app.run()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create README.md**

```markdown
# MusicTUI

A terminal-based music player with Vim-style interface.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src
```

## Features

- Scan local music library
- Play, pause, next, previous controls
- Search tracks
- Vim-style keyboard navigation

## Keybindings

- `j/k` - Navigate up/down
- `Enter` - Play selected track
- `Space` - Play/Pause
- `n` - Next track
- `p` - Previous track
- `q` - Quit
- `:scan <path>` - Scan music directory

## Configuration

Configuration file is located at `config/settings.json`.
```

- [ ] **Step 3: Commit**

```bash
git add src/__main__.py README.md
git commit -m "chore: add entry point and documentation"
```

---

## Summary

This Phase 1 implementation plan covers:
- Project setup with dependencies
- Configuration management
- Player core with queue management
- Library scanning and search
- Basic Textual UI framework
- Main application with keybindings
- Entry point

After completing this phase, the application should be able to:
1. Scan local music directories
2. Display track list in terminal
3. Play/pause/skip tracks
4. Basic keyboard navigation (Vim-style)
