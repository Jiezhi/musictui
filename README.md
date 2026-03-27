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
