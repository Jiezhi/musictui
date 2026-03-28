# AGENTS.md - MusicTUI Developer Guide

This file provides guidelines and commands for AI agents working on the MusicTUI project.

## Project Overview

MusicTUI is a terminal-based music player with Vim-style interface built with Textual.

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
│       ├── status_bar.py  # Status display
│       └── settings.py     # Settings panel
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
5. Write unit tests in `tests/test_<component>.py`

### Adding a New Feature

1. Write failing tests first (TDD)
2. Implement minimal code to pass
3. Refactor if needed
4. Ensure all tests pass

### Running Specific Test Suites

```bash
# Config tests
pytest tests/test_config.py -v

# Library tests
pytest tests/test_library.py -v

# Player tests
pytest tests/test_player.py -v

# Track list tests
pytest tests/test_track_list.py -v
```
