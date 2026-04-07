import os
import pytest
import sqlite3
from unittest.mock import MagicMock, patch
from src.app import MusicTUI
from src.library import Library

# Ensure pygame doesn't try to open real audio devices during tests
os.environ["SDL_AUDIODRIVER"] = "dummy"


@pytest.fixture
def test_audio_file():
    """Return path to test audio file (placeholder, not actually used)."""
    return "tests/e2e/fixtures/test.mp3"


@pytest.fixture
def mock_pygame_mixer():
    """Mock pygame.mixer so no real audio device is accessed during tests."""
    with patch("pygame.mixer") as mixer:
        mixer.init = MagicMock()
        mixer.Sound = MagicMock(return_value=MagicMock())
        mixer.music = MagicMock()
        mixer.music.load = MagicMock()
        mixer.music.play = MagicMock()
        mixer.music.pause = MagicMock()
        mixer.music.unpause = MagicMock()
        mixer.music.stop = MagicMock()
        yield mixer


@pytest.fixture
def empty_db(tmp_path):
    """Create a temporary SQLite DB pre‑populated with a couple of tracks."""
    db_path = tmp_path / "test.db"
    lib = Library(str(db_path))
    # Use direct connection to insert test data
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        INSERT INTO tracks (file_path, title, artist, duration)
        VALUES
            ('/music/track1.mp3', 'First', 'ArtistA', 180),
            ('/music/track2.mp3', 'Second', 'ArtistB', 210);
        """
    )
    conn.commit()
    conn.close()
    return lib


@pytest.fixture
async def app_runner(empty_db, mock_pygame_mixer):
    """Run the MusicTUI app in test mode with a deterministic DB.

    The MusicTUI constructor is expected to accept a ``db_path`` argument for
    testing; if it does not, the fixture can be adjusted accordingly.
    """

    async def _run():
        app = MusicTUI(db_path=str(empty_db.db_path))  # type: ignore[arg-type]
        async with app.run_test() as pilot:
            yield pilot, app

    return _run
