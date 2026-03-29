# AGENTS.md - MusicTUI Developer Guide

This file provides guidelines and commands for AI agents working on the MusicTUI project.

## Project Overview

MusicTUI is a terminal-based music player with Vim-style interface built with Textual. It uses:
- **Textual** - TUI framework
- **pygame** - Audio playback
- **SQLite** - Local music library database
- **mutagen** - Audio metadata extraction
- **Pydantic** - Configuration management

## Build, Lint, and Test Commands

### Running the Application

```bash
python -m src
```

### Running Tests

```bash
pytest tests/                      # All tests
pytest tests/test_settings.py -v   # Single file
pytest tests/test_settings.py::test_settings_initialization -v  # Single test
pytest tests/e2e/ -v              # E2E tests only
pytest tests/ --ignore=tests/e2e/ -v  # Unit tests only
```

## Architecture

### Data Flow

```
User Input → App (app.py) → Action Methods → Player/Library → UI Update
```

1. **Input**: User presses key → Textual dispatches to action method
2. **Processing**: Action method calls Player or Library
3. **Output**: Update UI components via query_one()

### Key Components

| Component | File | Responsibility |
|-----------|------|----------------|
| MusicTUI | app.py | Main app, keybindings, view management |
| Player | player.py | Audio playback, queue management |
| Library | library.py | SQLite database, track CRUD, search |
| TrackList | ui/track_list.py | Track display, selection |
| Sidebar | ui/sidebar.py | Navigation menu |
| PlayerBar | ui/player_bar.py | Playback progress display |
| StatusBar | ui/status_bar.py | Status messages |

### Database Schema

**tracks table:**
```sql
CREATE TABLE tracks (
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
```

**favorites table:**
```sql
CREATE TABLE favorites (
    track_id INTEGER PRIMARY KEY,
    FOREIGN KEY (track_id) REFERENCES tracks(id)
)
```

**blacklist table:**
```sql
CREATE TABLE blacklist (
    track_id INTEGER PRIMARY KEY,
    FOREIGN KEY (track_id) REFERENCES tracks(id)
)
```

## Code Style Guidelines

### General Principles

- Write clean, readable code with minimal complexity
- Prefer explicit over implicit
- Keep functions focused and small (single responsibility)
- Add tests for all new functionality (TDD recommended)

### Imports

```python
# Standard library first
import os
from pathlib import Path
from typing import Optional, Callable

# Third-party libraries
import pygame
from textual.widgets import Static

# Local modules
from src.models import Track, PlayerState
```

- Use absolute imports from `src` package
- Group imports: stdlib → third-party → local
- Sort imports alphabetically within groups

### Types

- Use Python 3.9+ type hints (list[int], not List[int])
- Use Optional for nullable types
- Include return types on all functions:

```python
def get_track_by_id(track_id: int) -> Optional[Track]:
    ...
```

### Naming Conventions

- **Classes**: PascalCase (`MusicTUI`, `PlayerBar`)
- **Functions/methods**: snake_case (`get_selected_track`, `move_up`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_VOLUME = 0.7`)
- **Private methods**: prefix with underscore (`_update_content`)

### Class Structure

- Use dataclasses for simple data models (`src/models.py`)
- Use Enum for fixed sets of values
- Keep `__init__` simple; initialize attributes with type hints

### Error Handling

- Use try/except for operations that may fail (file I/O, audio playback)
- Log errors with descriptive messages
- Handle specific exceptions when possible

### UI Components (Textual)

- Inherit from `Static` for simple widgets
- Use `id` parameter for DOM queries
- Implement move_up/move_down methods with _update_content()

### Database (SQLite)

- Use connection per operation in `Library` class
- Close connections explicitly
- Use parameterized queries to prevent SQL injection

### Configuration

- Use Pydantic models for configuration (`src/config.py`)
- Store config in `config/settings.json`
- Use `get_config()` singleton pattern

## Project Structure

```
musictui/
├── src/
│   ├── app.py              # Main application
│   ├── player.py           # Audio playback
│   ├── library.py          # Music library database
│   ├── config.py           # Configuration management
│   ├── models.py           # Data models (Track, Playlist, etc.)
│   └── ui/
│       ├── sidebar.py      # Navigation sidebar
│       ├── track_list.py   # Track listing
│       ├── player_bar.py   # Playback controls
│       ├── status_bar.py   # Status display
│       ├── settings.py     # Settings panel
│       ├── search.py       # Search functionality
│       └── queue.py        # Playback queue
├── tests/
│   ├── test_*.py           # Unit tests
│   └── e2e/                # End-to-end tests
├── config/                 # Configuration files
└── README.md
```

## Common Tasks

### Adding a New UI Component

1. Create component in `src/ui/<component>.py`
2. Add to `app.py` compose() method
3. Add keybindings in `BINDINGS` list
4. Add action methods in `MusicTUI` class
5. Add view switching logic in action methods
6. Write unit tests in `tests/test_<component>.py`

Example - adding bindings:
```python
BINDINGS = [
    Binding("key", "action_method_name", "Description", show=False),
]
```

Example - view switching pattern:
```python
def action_show_viewname(self) -> None:
    self.current_view = "viewname"
    try:
        track_list = self.query_one("#track-list", TrackList)
        track_list.styles.display = "none"
        new_view = self.query_one("#new-view", NewView)
        new_view.styles.display = "block"
    except Exception:
        pass
```

### Adding a New Feature

1. Write failing tests first (TDD)
2. Implement minimal code to pass
3. Refactor if needed
4. Ensure all tests pass

### Adding Database Features

1. Add table schema in `_init_db()` method
2. Add CRUD methods to `Library` class
3. Follow connection-per-operation pattern
4. Write tests for new methods

### Adding Keyboard Shortcuts

1. Add Binding to BINDINGS list in app.py
2. Implement action_method_name() in MusicTUI class
3. Update status_bar.py to document the new shortcut

### Modifying Player Behavior

The Player class manages:
- Current track playback
- Queue (playback order)
- Volume
- Play mode (loop/shuffle/single)

Key methods:
- `play(track)` - Play a track
- `pause()` / `resume()` - Pause control
- `next()` / `previous()` - Navigation
- `set_volume(level)` - Volume control (0.0-1.0)

## Important Implementation Details

### View Management

- Track visibility with `styles.display = "block"` / `"none"`
- Only one view visible at a time (except player_bar, status_bar, sidebar)
- `current_view` string tracks active view

### State Management

- Player state: `PlayerState` enum (STOPPED, PLAYING, PAUSED)
- TrackList: `selected_index` for current selection
- Sidebar: `selected` for current menu item

### Callbacks

- Player uses callbacks for state/track changes: `set_on_track_change()`
- TrackList uses callback for pagination: `set_load_more_callback()`

### Testing Patterns

```python
# Testing a UI component
def test_component_initialization():
    component = Component()
    assert component.initial_state == expected

# Testing library methods
def test_library_crud():
    library = Library(":memory:")
    track = Track(title="Test")
    library._save_track(track)
    result = library.get_track_by_id(track.id)
    assert result.title == "Test"
```

## Running Specific Test Suites

```bash
# Config tests
pytest tests/test_config.py -v

# Library tests
pytest tests/test_library.py -v

# Player tests
pytest tests/test_player.py -v

# Track list tests
pytest tests/test_track_list.py -v

# Models tests
pytest tests/test_models.py -v
```

## Git Workflow

1. Create branch for feature/fix
2. Write tests first (TDD)
3. Implement feature
4. Ensure all tests pass
5. Commit with descriptive message

### Commit Message Format

```
<type>: <short description>

<detailed description if needed>

- Changed X
- Added Y
- Fixed Z
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`

## Common Pitfalls

1. **Forgetting to close DB connections** - Always use try/finally or context managers
2. **Not handling None returns** - Check for None before using returned objects
3. **View state persistence** - Remember to hide/show views correctly
4. **Queue pagination** - TrackList needs load_more_callback for large libraries
5. **Player callbacks** - Set up callbacks in on_mount(), not __init__()

## Quick Reference

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `space` | Play/Pause |
| `n` | Next track |
| `p` | Previous track |
| `j` | Move down |
| `k` | Move up |
| `enter` | Play selected |
| `q` | Quit |
| `1` | Show Library |
| `2` | Show Queue |
| `3` | Show Search |
| `4` | Show Favorites |
| `5` | Show Settings |
| `l` | Sidebar move up |
| `h` | Sidebar move down |
| `+` / `=` | Volume up |
| `-` / `_` | Volume down |
| `/` | Start search |
| `escape` | Clear search |
| `f` | Add to favorites |
| `u` | Remove from favorites |
| `b` | Add to blacklist |

### Task Reference

| Task | File to Modify |
|------|----------------|
| Add new shortcut | app.py BINDINGS + action method |
| Add database field | library.py models.py |
| Add UI component | ui/*.py + app.py compose() |
| Add configuration | config.py + settings.py |
| Fix playback issue | player.py |
| Fix search issue | library.py search() method |
