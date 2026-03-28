# Terminal Music Player Design

## 1. Overview

**Project Name**: musictui
**Purpose**: A terminal-based music player that supports scanning, managing, and playing audio files from local storage and WebDAV servers.
**Target Users**: Developers and power users who prefer terminal-based workflows.

## 2. Requirements

### 2.1 Core Features
- **Music Library Management**: Scan and index local music files with metadata extraction
- **WebDAV Support**: Connect to WebDAV servers to access remote music collections
- **Playlist Management**: Create, edit, save, and load playlists
- **Search Functionality**: Search by song title, artist, album, or genre
- **Playback Controls**: Play, pause, stop, next, previous, seek, volume control
- **Playback Modes**: Loop, shuffle, single repeat
- **Metadata Scraping**: Fetch and fix audio file metadata from MusicBrainz
- **Visualization**: Display album art and spectrum visualization (optional)

### 2.2 User Interface
- **Style**: Minimalist Vim-style interface
- **Navigation**: Keyboard-driven with Vim-style shortcuts
- **Layout**: Sidebar + main content area + player controls + status bar

## 3. Technical Architecture

### 3.1 Technology Stack
| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| TUI Framework | Textual |
| Audio Playback | pygame.mixer |
| Database | SQLite |
| WebDAV Client | webdavclient3 |
| Metadata | mutagen, musicbrainzngs |
| Configuration | pydantic |

### 3.2 Project Structure
```
musictui/
├── src/
│   ├── __init__.py
│   ├── app.py              # Main application entry
│   ├── player.py           # Audio player core
│   ├── library.py          # Music library management
│   ├── playlist.py         # Playlist management
│   ├── webdav.py           # WebDAV client
│   ├── metadata.py         # Metadata processing/scraper
│   ├── search.py           # Search functionality
│   └── ui/                 # UI components
│       ├── __init__.py
│       ├── player_view.py  # Player interface
│       ├── library_view.py # Library interface
│       ├── playlist_view.py# Playlist interface
│       └── widgets.py      # Custom widgets
├── data/
│   └── music.db            # SQLite database
├── config/
│   └── settings.json       # Configuration file
├── tests/                  # Test directory
├── requirements.txt
└── pyproject.toml
```

### 3.3 Core Components

#### 3.3.1 Player Class
```python
class Player:
    """Audio player core, manages playback state and audio output"""
    
    def __init__(self):
        self.queue: list[Track]        # Play queue
        self.current_index: int        # Current playing index
        self.state: PlayerState        # Playing state (playing/paused/stopped)
        self.volume: float             # Volume (0.0-1.0)
        self.play_mode: PlayMode       # Play mode (loop/shuffle/single)
        self.position: float           # Current playback position (seconds)
    
    def play(self, track: Track) -> None
    def pause(self) -> None
    def resume(self) -> None
    def stop(self) -> None
    def next(self) -> None
    def previous(self) -> None
    def seek(self, position: float) -> None
    def set_volume(self, volume: float) -> None
    def set_play_mode(self, mode: PlayMode) -> None
```

#### 3.3.2 Library Class
```python
class Library:
    """Music library, manages local and WebDAV music files"""
    
    def __init__(self, db_path: str):
        self.db: sqlite3.Connection     # Database connection
        self.webdav_client: WebDAVClient # WebDAV client
    
    def scan_local(self, path: str) -> list[Track]
    def scan_webdav(self, config: WebDAVConfig) -> list[Track]
    def get_all_tracks(self) -> list[Track]
    def search(self, query: str) -> list[Track]
    def update_metadata(self, track: Track) -> None
```

#### 3.3.3 PlaylistManager Class
```python
class PlaylistManager:
    """Playlist manager"""
    
    def __init__(self, db_path: str):
        self.db: sqlite3.Connection
    
    def create(self, name: str) -> Playlist
    def delete(self, playlist_id: str) -> None
    def add_track(self, playlist_id: str, track: Track) -> None
    def remove_track(self, playlist_id: str, track_id: str) -> None
    def get_tracks(self, playlist_id: str) -> list[Track]
    def get_all_playlists(self) -> list[Playlist]
```

#### 3.3.4 MetadataScraper Class
```python
class MetadataScraper:
    """Audio metadata scraper and fixer"""
    
    def scrape(self, track: Track) -> TrackMetadata
    def apply(self, track: Track, metadata: TrackMetadata) -> None
    def batch_scrape(self, tracks: list[Track]) -> None
```

## 4. User Interface Design

### 4.1 Main Layout
```
┌─────────────────────────────────────────────────────────────┐
│ musictui v0.1.0                           [Library] [Queue] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────────────────────────────┐   │
│  │  Sidebar    │  │  Main Content Area                  │   │
│  │             │  │                                     │   │
│  │  > Library  │  │  Current view content               │   │
│  │    Queue    │  │  (music list/playlist/search result)│   │
│  │    Search   │  │                                     │   │
│  │    Settings │  │                                     │   │
│  │             │  │                                     │   │
│  └─────────────┘  └─────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ ▶ Playing: Song Title - Artist            02:30 / 04:15    │
│ [■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■] 80%  Vol: 70%   │
├─────────────────────────────────────────────────────────────┤
│ NORMAL │ q:quit  space:play/pause  n:next  p:prev  /:search │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Vim-style Keybindings

#### Normal Mode
| Key | Action |
|-----|--------|
| `j/k` | Navigate up/down |
| `Enter` | Play selected track |
| `Space` | Play/Pause toggle |
| `n/p` | Next/Previous track |
| `s` | Toggle shuffle |
| `l` | Toggle loop mode |
| `+/-` | Volume up/down |
| `/` | Enter search mode |
| `:` | Enter command mode |
| `q` | Quit application |

#### Search Mode
| Key | Action |
|-----|--------|
| Type | Enter search query |
| `Enter` | Execute search |
| `Esc` | Cancel search |

#### Command Mode
| Command | Action |
|---------|--------|
| `:scan <path>` | Scan local music directory |
| `:webdav` | Configure WebDAV connection |
| `:playlist create <name>` | Create new playlist |
| `:scrape` | Batch scrape metadata |

#### View Navigation
| Key | Action |
|-----|--------|
| `g+h` | Switch to Library |
| `g+q` | Switch to Queue |
| `g+s` | Switch to Search |
| `g+p` | Switch to Settings |

## 5. Data Flow

### 5.1 Architecture Diagram
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User Input│───>│   UI Layer  │───>│  App Layer  │
│  (Keyboard) │    │  (Textual)  │    │  (App Class)│
└─────────────┘    └─────────────┘    └──────┬──────┘
                                            │
       ┌────────────────────────────────────┼────────────────┐
       │                                    │                │
       ▼                                    ▼                ▼
┌─────────────┐                      ┌─────────────┐  ┌─────────────┐
│   Library   │                      │   Player    │  │  Playlist   │
│   (Music)   │                      │   (Audio)   │  │  (Manager)  │
└──────┬──────┘                      └──────┬──────┘  └──────┬──────┘
       │                                    │                │
       ▼                                    ▼                ▼
┌─────────────┐                      ┌─────────────┐  ┌─────────────┐
│   SQLite    │                      │ pygame.mixer│  │   SQLite    │
│  (Database) │                      │ (Audio Backend)│  │  (Database) │
└─────────────┘                      └─────────────┘  └─────────────┘
```

### 5.2 Error Handling Strategy

**Layer-based Error Handling**:
1. **UI Layer**: Capture user operation errors, display friendly prompts
2. **Application Layer**: Business logic errors, log and recover
3. **Bottom Layer**: Audio/database/network errors, throw exceptions upward

**Specific Scenarios**:
- **File Not Found**: Prompt user, remove from library
- **Unsupported Audio Format**: Skip and log
- **WebDAV Connection Failed**: Display error, suggest config check
- **Database Error**: Attempt recovery, rebuild if necessary
- **Playback Error**: Auto skip to next track

### 5.3 Configuration
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

## 6. Testing Strategy

### 6.1 Unit Testing
- Each core component tested independently
- Mock external dependencies (filesystem, database, pygame)
- Use pytest framework

### 6.2 Test Coverage
- `test_player.py`: Player state management
- `test_library.py`: Library scanning and querying
- `test_playlist.py`: Playlist CRUD operations
- `test_metadata.py`: Metadata scraping
- `test_webdav.py`: WebDAV connection (Mock)

## 7. Development Phases

### Phase 1: Foundation (MVP)
- Project structure setup
- Basic UI framework (Textual)
- Player core (pygame.mixer)
- Local music scanning

### Phase 2: Core Features
- Music library management
- Playlist functionality
- Search functionality
- Vim-style keybindings

### Phase 3: Advanced Features
- WebDAV support
- Metadata scraping
- Visualization effects
- Theme system

## 8. Dependencies

```
textual>=0.40.0
pygame>=2.5.0
mutagen>=1.47.0
webdavclient3>=3.14.6
musicbrainzngs>=0.7.1
pydantic>=2.0.0
pytest>=7.0.0
```

## 9. Success Criteria

1. Successfully scan and play local music files
2. Connect to WebDAV server and stream music
3. Create and manage playlists
4. Search music by title, artist, or album
5. Scrape and fix audio metadata
6. Intuitive Vim-style keyboard navigation
7. Clean, responsive terminal interface

## 10. Future Enhancements

- Lyrics display support
- Last.fm scrobbling
- Podcast support
- Audio equalizer
- Theme customization API
- Plugin system
