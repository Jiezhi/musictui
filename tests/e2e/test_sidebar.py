"""End-to-end tests for sidebar navigation"""

import pytest
from src.models import Track


@pytest.mark.asyncio
async def test_sidebar_exists():
    """Test that sidebar exists in the app"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        sidebar = app.query_one("#sidebar")
        assert sidebar is not None


@pytest.mark.asyncio
async def test_sidebar_displays_items():
    """Test that sidebar displays all navigation items"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        sidebar = app.query_one("#sidebar")
        assert "Library" in sidebar.items
        assert "Queue" in sidebar.items
        assert "Search" in sidebar.items
        assert "Favorites" in sidebar.items
        assert "Settings" in sidebar.items


@pytest.mark.asyncio
async def test_sidebar_initial_selection():
    """Test that sidebar initially selects Library"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        sidebar = app.query_one("#sidebar")
        assert sidebar.selected == 0
        assert sidebar.get_selected() == "Library"


@pytest.mark.asyncio
async def test_sidebar_move_down():
    """Test pressing 'l' moves sidebar selection down"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        sidebar = app.query_one("#sidebar")
        initial_selection = sidebar.selected
        
        # Press 'l' to move down
        await pilot.press("l")
        await pilot.pause()
        
        assert sidebar.selected == (initial_selection + 1) % len(sidebar.items)


@pytest.mark.asyncio
async def test_sidebar_move_up():
    """Test pressing 'h' moves sidebar selection up"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Move down first
        await pilot.press("l")
        await pilot.pause()
        
        sidebar = app.query_one("#sidebar")
        middle_selection = sidebar.selected
        
        # Press 'h' to move up
        await pilot.press("h")
        await pilot.pause()
        
        assert sidebar.selected == (middle_selection - 1) % len(sidebar.items)


@pytest.mark.asyncio
async def test_sidebar_wraps_around():
    """Test that sidebar selection wraps around"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        sidebar = app.query_one("#sidebar")
        # Move to last item
        for _ in range(len(sidebar.items) - 1):
            await pilot.press("l")
            await pilot.pause()
        
        assert sidebar.selected == len(sidebar.items) - 1
        
        # Move down should wrap to first
        await pilot.press("l")
        await pilot.pause()
        
        assert sidebar.selected == 0


@pytest.mark.asyncio
async def test_sidebar_click_navigates_to_view():
    """Test that clicking sidebar item navigates to that view"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Move to Queue in sidebar
        await pilot.press("l")
        await pilot.pause()
        
        # Press enter to select
        await pilot.press("enter")
        await pilot.pause()
        
        # Should navigate to Queue view
        assert app.current_view == "queue"


@pytest.mark.asyncio
async def test_sidebar_library_selection():
    """Test sidebar Library selection navigates to library"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Move to Settings first
        await pilot.press("5")
        await pilot.pause()
        assert app.current_view == "settings"
        
        # Move sidebar to Library (need to move up 4 times or down once)
        for _ in range(4):
            await pilot.press("h")
            await pilot.pause()
        
        # Press enter to select
        await pilot.press("enter")
        await pilot.pause()
        
        assert app.current_view == "library"


@pytest.mark.asyncio
async def test_sidebar_search_selection():
    """Test sidebar Search selection navigates to search"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Move to Search in sidebar (down 2 times)
        await pilot.press("l")
        await pilot.pause()
        await pilot.press("l")
        await pilot.pause()
        
        # Press enter to select
        await pilot.press("enter")
        await pilot.pause()
        
        assert app.current_view == "search"


@pytest.mark.asyncio
async def test_sidebar_favorites_selection():
    """Test sidebar Favorites selection navigates to favorites"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Move to Favorites in sidebar (down 3 times)
        for _ in range(3):
            await pilot.press("l")
            await pilot.pause()
        
        # Press enter to select
        await pilot.press("enter")
        await pilot.pause()
        
        assert app.current_view == "favorites"


@pytest.mark.asyncio
async def test_sidebar_settings_selection():
    """Test sidebar Settings selection navigates to settings"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Move to Settings in sidebar (down 4 times)
        for _ in range(4):
            await pilot.press("l")
            await pilot.pause()
        
        # Press enter to select
        await pilot.press("enter")
        await pilot.pause()
        
        assert app.current_view == "settings"
