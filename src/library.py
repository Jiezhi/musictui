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
