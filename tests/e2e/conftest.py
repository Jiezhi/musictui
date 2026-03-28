import os
import pytest
from src.app import MusicTUI

os.environ["SDL_AUDIODRIVER"] = "dummy"


@pytest.fixture
def test_audio_file():
    """Return path to test audio file"""
    return "tests/e2e/fixtures/test.mp3"


@pytest.fixture
async def app_with_pilot():
    """Create app instance with pilot for testing"""
    app = MusicTUI()
    async with app.run_test() as pilot:
        yield app, pilot
