"""End-to-end tests for Settings view"""

import pytest
from src.models import Track


@pytest.mark.asyncio
async def test_settings_view_exists():
    """Test that settings view exists in the app"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        settings = app.query_one("#settings")
        assert settings is not None


@pytest.mark.asyncio
async def test_settings_view_hidden_by_default():
    """Test that settings view is hidden by default"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        settings = app.query_one("#settings")
        assert settings.styles.display == "none"


@pytest.mark.asyncio
async def test_show_settings_keybinding():
    """Test pressing '5' shows settings view"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Press '5' to show settings
        await pilot.press("5")
        await pilot.pause()
        
        settings = app.query_one("#settings")
        assert settings.styles.display == "block"
        assert app.current_view == "settings"


@pytest.mark.asyncio
async def test_settings_navigation():
    """Test navigating settings with j/k keys"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Show settings
        await pilot.press("5")
        await pilot.pause()
        
        settings = app.query_one("#settings")
        initial_selected = settings.selected
        
        # Press j to move down
        await pilot.press("j")
        await pilot.pause()
        
        assert settings.selected == (initial_selected + 1) % len(settings.items)
        
        # Press k to move up
        await pilot.press("k")
        await pilot.pause()
        
        assert settings.selected == initial_selected


@pytest.mark.asyncio
async def test_settings_displays_values():
    """Test that settings displays configuration values"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Show settings
        await pilot.press("5")
        await pilot.pause()
        
        settings = app.query_one("#settings")
        # Check that values dict has expected keys
        assert "Volume" in settings.values
        assert "Play Mode" in settings.values
        assert "Theme" in settings.values


@pytest.mark.asyncio
async def test_return_to_library_from_settings():
    """Test returning to library view from settings"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Show settings
        await pilot.press("5")
        await pilot.pause()
        assert app.current_view == "settings"
        
        # Return to library
        await pilot.press("1")
        await pilot.pause()
        
        assert app.current_view == "library"
        settings = app.query_one("#settings")
        track_table = app.query_one("#track-table")
        assert settings.styles.display == "none"
        assert track_table.styles.display == "block"
