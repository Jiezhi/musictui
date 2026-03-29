# MusicTUI

A terminal-based music player with Vim-style interface built with Textual.

## Features

- **Local Music Library**: Scan and manage local music files (mp3, flac, wav, ogg, m4a, wma)
- **Remote URL Support**: Load music from remote URL song lists (JS/JSON format)
- **Playback Controls**: Play, pause, next, previous, seek, volume control
- **Search**: Search tracks by title, artist, album with pinyin support
- **Vim-style Navigation**: Navigate using j/k/h/l keys
- **Multiple Views**: Library, Queue, Search, Favorites, Settings
- **Play Modes**: Loop, shuffle, repeat one
- **Lazy Loading**: Efficient pagination for large music libraries
- **Favorites & Blacklist**: Mark favorite tracks or blacklist unwanted ones

## Installation

```bash
# Clone the repository
git clone https://github.com/Jiezhi/musictui.git
cd musictui

# Install dependencies
pip install -e .
```

## Usage

```bash
# Run the application
python -m src
```

## Keybindings

### Navigation

| Key | Action |
|-----|--------|
| `j` / `k` | Navigate down/up (in current view) |
| `l` / `h` | Navigate sidebar down/up |
| `1` | Show Library view |
| `2` | Show Queue view |
| `3` | Show Search view |
| `4` | Show Favorites view |
| `5` | Show Settings view |

### Playback

| Key | Action |
|-----|--------|
| `Space` | Play/Pause toggle |
| `Enter` | Play selected track |
| `n` | Next track |
| `p` | Previous track |

### Volume

| Key | Action |
|-----|--------|
| `+` / `=` | Volume up |
| `-` / `_` | Volume down |

### Library Management

| Key | Action |
|-----|--------|
| `:` + `scan <path>` | Scan music directory |
| `/` | Start search |
| `Escape` | Clear search |
| `f` | Add to favorites |
| `u` | Remove from favorites |
| `b` | Add to blacklist |

### Other

| Key | Action |
|-----|--------|
| `q` | Quit |

## Configuration

Configuration is stored in `config/settings.json` (auto-created on first run):

```json
{
  "library_paths": ["/path/to/music"],
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

### Remote URL Song List

You can load songs from a remote URL by providing a JS or JSON format:

```javascript
// JS format (var list = [...])
var list = [
  {name: "Song 1", artist: "Artist 1", url: "https://example.com/1.mp3", cover: "https://example.com/c1.jpg"},
  {name: "Song 2", artist: "Artist 2", url: "https://example.com/2.mp3"}
];
```

```json
// JSON format
[
  {"name": "Song 1", "artist": "Artist 1", "url": "https://example.com/1.mp3", "cover": "https://example.com/c1.jpg"},
  {"name": "Song 2", "artist": "Artist 2", "url": "https://example.com/2.mp3"}
]
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/ --ignore=tests/e2e/

# Run e2e tests
pytest tests/e2e/ -v
```

### Project Structure

```
musictui/
├── src/
│   ├── app.py              # Main application
│   ├── player.py           # Audio playback
│   ├── library.py          # Music library database
│   ├── config.py           # Configuration management
│   ├── models.py           # Data models
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
├── pyproject.toml          # Project configuration
└── README.md
```

## Tech Stack

- [Textual](https://textual.textualize.io/) - TUI framework
- [pygame](https://www.pygame.org/) - Audio playback
- [mutagen](https://mutagen.readthedocs.io/) - Audio metadata extraction
- [SQLite](https://www.sqlite.org/) - Local music library database
- [Pydantic](https://pydantic.dev/) - Configuration management
- [requests](https://docs.python-requests.org/) - HTTP requests for remote URLs

## License

MIT License
