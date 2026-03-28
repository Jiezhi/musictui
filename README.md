# MusicTUI

A terminal-based music player with Vim-style interface built with Textual.

## Features

- Scan local music library (mp3, flac, wav, ogg, m4a, wma)
- Play, pause, next, previous controls
- Search tracks by title, artist, or album
- Vim-style keyboard navigation
- Sidebar navigation (Library, Queue, Search, Settings)
- Settings panel with volume, play mode, and theme options
- Lazy loading for large libraries (pagination)
- Real-time playback progress display
- Multiple play modes (loop, shuffle, repeat_one)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src
```

## Keybindings

| Key | Action |
|-----|--------|
| `j` / `k` | Navigate down/up (in current view) |
| `l` / `h` | Navigate sidebar up/down |
| `Enter` | Play selected track |
| `Space` | Play/Pause |
| `n` | Next track |
| `p` | Previous track |
| `1` | Show Library view |
| `2` | Show Queue view |
| `3` | Show Search view |
| `4` | Show Settings view |
| `q` | Quit |
| `:scan <path>` | Scan music directory |

## Configuration

Configuration file is located at `config/settings.json`.

```json
{
  "library_paths": ["/path/to/music"],
  "player": {
    "volume": 0.7,
    "play_mode": "loop"
  },
  "ui": {
    "theme": "monokai"
  }
}
```

## Development

Run tests:

```bash
pytest tests/
```

## Tech Stack

- [Textual](https://textual.textualize.io/) - TUI framework
- [pygame](https://www.pygame.org/) - Audio playback
- [mutagen](https://mutagen.readthedocs.io/) - Audio metadata
- [SQLite](https://www.sqlite.org/) - Local database
