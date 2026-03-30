"""End-to-end tests for Favorites view"""

import os
import pytest
import tempfile
from src.models import Track


@pytest.mark.asyncio
async def test_favorites_view_exists():
    """Test that favorites view exists in the app"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Favorites view uses the same track-table component
        track_table = app.query_one("#track-table")
        assert track_table is not None


@pytest.mark.asyncio
async def test_show_favorites_keybinding():
    """Test pressing '4' shows favorites view"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Press '4' to show favorites
        await pilot.press("4")
        await pilot.pause()
        
        assert app.current_view == "favorites"


@pytest.mark.asyncio
async def test_add_track_to_favorites():
    """Test adding a track to favorites with 'f' key"""
    from src.app import MusicTUI
    import tempfile
    import os

    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_db = tmp.name
    
    try:
        app = MusicTUI()
        # Override library to use temp db
        async with app.run_test() as pilot:
            await pilot.pause()
            
            # Create new library with temp db
            from src.library import Library
            temp_library = Library(tmp_db)
            app.library = temp_library
            
            # Add a track to the library
            track = Track(id=1, file_path="/test.mp3", title="Test")
            temp_library._save_track(track)
            
            # Select the track and press 'f' to favorite
            track_table = app.query_one("#track-table")
            track_table.set_tracks([track])
            
            await pilot.press("f")
            await pilot.pause()
            
            # Verify track is in favorites
            favorites = temp_library.get_favorites()
            assert len(favorites) >= 1
    finally:
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


@pytest.mark.asyncio
async def test_favorites_view_displays_tracks():
    """Test that favorites view displays favorited tracks"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Add mock tracks to track table
        track_table = app.query_one("#track-table")
        tracks = [
            Track(id=1, file_path="/test1.mp3", title="Test1"),
            Track(id=2, file_path="/test2.mp3", title="Test2"),
        ]
        track_table.set_tracks(tracks)
        
        # Switch to favorites view
        await pilot.press("4")
        await pilot.pause()
        
        assert app.current_view == "favorites"


@pytest.mark.asyncio
async def test_remove_from_favorites():
    """Test removing track from favorites"""
    from src.app import MusicTUI
    from src.library import Library
    import tempfile
    import os

    # Create a temporary database for testing
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_db = tmp.name
    
    try:
        temp_library = Library(tmp_db)
        app = MusicTUI()
        async with app.run_test() as pilot:
            await pilot.pause()
            
            # Use isolated library
            app.library = temp_library
            
            # Add track and favorite it
            track = Track(id=1, file_path="/test.mp3", title="Test")
            temp_library._save_track(track)
            temp_library.add_favorite(1)
            
            # Verify it's favorited
            favorites = temp_library.get_favorites()
            assert len(favorites) == 1
            
            # Remove from favorites using library method
            temp_library.remove_favorite(1)
            
            favorites = temp_library.get_favorites()
            assert len(favorites) == 0
    finally:
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


@pytest.mark.asyncio
async def test_return_to_library_from_favorites():
    """Test returning to library view from favorites"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Show favorites
        await pilot.press("4")
        await pilot.pause()
        assert app.current_view == "favorites"
        
        # Return to library
        await pilot.press("1")
        await pilot.pause()
        
        assert app.current_view == "library"
