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
    cover: str = ""  # Remote cover URL

    @property
    def display_name(self) -> str:
        if self.title:
            return f"{self.artist} - {self.title}" if self.artist else self.title
        return Path(self.file_path).stem


@dataclass
class Playlist:
    id: Optional[int] = None
    name: str = ""
    track_ids: Optional[list[int]] = None

    def __post_init__(self):
        if self.track_ids is None:
            self.track_ids = []
