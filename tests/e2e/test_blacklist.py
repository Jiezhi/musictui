"""End-to-end tests for blacklist functionality"""

import pytest
import os
import tempfile
from src.models import Track


@pytest.mark.asyncio
async def test_add_to_blacklist():
    """Test adding track to blacklist"""
    from src.app import MusicTUI
    from src.library import Library

    # Create temp database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_db = tmp.name

    try:
        app = MusicTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            temp_library = Library(tmp_db)
            app.library = temp_library

            track = Track(id=1, file_path="/test.mp3", title="Test Song")
            temp_library._save_track(track)

            # Add to blacklist
            result = temp_library.add_to_blacklist(1)
            assert result is True

            # Verify blacklisted
            assert temp_library.is_blacklisted(1) is True
    finally:
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


@pytest.mark.asyncio
async def test_remove_from_blacklist():
    """Test removing track from blacklist"""
    from src.app import MusicTUI
    from src.library import Library

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_db = tmp.name

    try:
        temp_library = Library(tmp_db)
        app = MusicTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            app.library = temp_library

            track = Track(id=1, file_path="/test.mp3", title="Test Song")
            temp_library._save_track(track)
            temp_library.add_to_blacklist(1)

            # Remove from blacklist
            result = temp_library.remove_from_blacklist(1)
            assert result is True

            # Verify not blacklisted
            assert temp_library.is_blacklisted(1) is False
    finally:
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


@pytest.mark.asyncio
async def test_blacklist_keybinding():
    """Test pressing 'b' adds track to blacklist"""
    from src.app import MusicTUI
    from src.library import Library

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_db = tmp.name

    try:
        app = MusicTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            temp_library = Library(tmp_db)
            app.library = temp_library

            track = Track(id=1, file_path="/test.mp3", title="Test Song")
            temp_library._save_track(track)

            track_table = app.query_one("#track-table")
            track_table.set_tracks([track])

            # Press 'b' to add to blacklist
            await pilot.press("b")
            await pilot.pause()

            # Verify blacklisted
            assert temp_library.is_blacklisted(1) is True
    finally:
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


@pytest.mark.asyncio
async def test_get_tracks_excluding_blacklist():
    """Test getting tracks excluding blacklisted ones"""
    from src.app import MusicTUI
    from src.library import Library

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_db = tmp.name

    try:
        temp_library = Library(tmp_db)
        app = MusicTUI()
        async with app.run_test() as pilot:
            await pilot.pause()

            app.library = temp_library

            # Add multiple tracks
            for i in range(3):
                track = Track(id=i+1, file_path=f"/test{i+1}.mp3", title=f"Song {i+1}")
                temp_library._save_track(track)

            # Blacklist one
            temp_library.add_to_blacklist(2)

            # Get tracks excluding blacklist
            tracks = temp_library.get_tracks_excluding_blacklist()
            
            assert len(tracks) == 2
            assert all(t.id != 2 for t in tracks)
    finally:
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)
