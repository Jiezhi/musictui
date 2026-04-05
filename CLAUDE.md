# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

- Install runtime dependencies: `pip install -e .`
- Install dev dependencies: `pip install -e .[dev]`
- Run the app: `python -m src`
- Run all tests: `pytest tests/`
- Run unit tests only: `pytest tests/ --ignore=tests/e2e/`
- Run e2e tests only: `pytest tests/e2e/ -v`
- Run a single test file: `pytest tests/test_player.py`
- Run a single test: `pytest tests/test_player.py -k test_player_add_to_queue`

## Project architecture

This is a Textual-based terminal music player. The top-level app is `MusicTUI` in `src/app.py`, which composes the UI, owns the `Player` and `Library` instances, and wires keyboard actions to view updates, playback, and persistence.

### Core runtime flow

- Entrypoint is `python -m src`, which calls `src.__main__.main()` and runs `MusicTUI`.
- On mount, `MusicTUI` loads config from `config/settings.json`, creates a `Player`, creates a `Library` backed by `~/.musictui/music.db`, initializes views, then loads the first page of tracks.
- The app uses a single active-view model controlled by `self.current_view`; switching views mostly means hiding/showing `#track-table`, `#queue`, `#search`, and `#settings`.
- Keyboard handling is centralized in `src/app.py`. Search input and command input are implemented by dynamically creating action bindings from `SEARCH_KEYS` and `COMMAND_KEYS`, then routing them through `__getattr__`.

### Main state holders

- `src/player.py`: in-memory playback state and queue management around `pygame.mixer`. The player owns queue order, current index, volume, play mode, and state transitions. UI updates depend on its `set_on_track_change` and `set_on_state_change` callbacks.
- `src/library.py`: SQLite-backed library and metadata layer. It initializes tables (`tracks`, `favorites`, `blacklist`), scans local files with Mutagen metadata extraction, persists remote tracks, and serves search/favorites/blacklist queries.
- `src/config.py`: Pydantic-backed config loader/saver with a module-level cache. Default config path is `config/settings.json` relative to the repo.
- `src/models.py`: shared dataclasses/enums (`Track`, `Playlist`, `PlayerState`, `PlayMode`). `Track.display_name` is the common UI display string.

### UI structure

The current UI implementation is centered on `src/app.py` and the widgets under `src/ui/` and `src/ui/widgets/`:

- `src/ui/widgets/sidebar.py`: navigation list for Library / Queue / Search / Favorites / Settings.
- `src/ui/widgets/track_table.py`: main library/favorites table using `DataTable`; emits `TrackSelected` and `TrackDoubleClicked` messages.
- `src/ui/queue.py`: text-based queue view over the player's in-memory queue.
- `src/ui/search.py`: text-based search results panel backed by `Library.search()`.
- `src/ui/settings.py`: simple settings panel for volume, play mode, theme, and library paths.
- `src/ui/command_input.py`: `:` command line used for `scan <path>` and `url <url>`.
- `src/ui/widgets/player_bar.py` and `src/ui/status_bar.py`: playback/status display.
- `src/ui/widgets/context_menu.py`: modal screen opened from track-table selection for play/queue/favorite/blacklist actions.

There are newer-looking files such as `src/ui/views/main_view.py`, `src/ui/main_screen.py`, `src/ui/widgets/player_bar.py`, and theme modules under `src/theme/`, but the active app wiring currently comes from `src/app.py` and directly imports the widget modules listed above. Check imports before editing alternate UI files.

### Library/search behavior

- Local library scanning is recursive via `Library.scan_local()` and stores supported audio files into SQLite.
- `Library.search()` first performs SQL `LIKE` matching on title/artist/album, then falls back to pinyin/full-spelling/initials matching by scanning all tracks in Python.
- Remote song lists are fetched with `requests` and parsed from either raw JSON arrays or `var list = [...]` JavaScript blobs.
- Favorites and blacklist are separate tables keyed by track id; favorites view reuses the main track table, while blacklist is mainly enforced through library queries and explicit app actions.

### Playback behavior

- `Player.play(track)` ensures the selected track is in the queue and updates `current_index` before loading it through `pygame.mixer.music`.
- `next()` and `previous()` change the queue index; actual playback reload only happens if the current state is `PLAYING`.
- The app updates the player bar via callbacks and a periodic timer that polls `pygame.mixer.music.get_pos()` while a track is playing.

## Testing notes

- Tests are split between direct unit-style tests in `tests/` and Textual integration/e2e tests in `tests/e2e/`.
- Test fixtures set `SDL_AUDIODRIVER=dummy` so pygame can initialize without real audio hardware.
- E2E tests commonly use `MusicTUI().run_test()` and interact through Textual's `pilot`.
- When changing keyboard behavior or view switching, check the e2e tests first; when changing a widget's local behavior, there is often a focused unit test alongside it.
