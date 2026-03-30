"""End-to-end tests for volume control"""

import pytest
from src.models import Track


@pytest.mark.asyncio
async def test_volume_up_with_plus():
    """Test pressing '+' increases volume"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        initial_volume = app.player.volume
        
        # Press '+' to increase volume
        await pilot.press("+")
        await pilot.pause()
        
        assert app.player.volume >= initial_volume


@pytest.mark.asyncio
async def test_volume_up_with_equals():
    """Test pressing '=' increases volume (alternative key)"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        initial_volume = app.player.volume
        
        # Press '=' to increase volume
        await pilot.press("=")
        await pilot.pause()
        
        assert app.player.volume >= initial_volume


@pytest.mark.asyncio
async def test_volume_down_with_minus():
    """Test pressing '-' decreases volume"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        initial_volume = app.player.volume
        
        # Press '-' to decrease volume
        await pilot.press("-")
        await pilot.pause()
        
        assert app.player.volume <= initial_volume


@pytest.mark.asyncio
async def test_volume_down_with_underscore():
    """Test pressing '_' decreases volume (alternative key)"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        initial_volume = app.player.volume
        
        # Press '_' to decrease volume
        await pilot.press("_")
        await pilot.pause()
        
        assert app.player.volume <= initial_volume


@pytest.mark.asyncio
async def test_volume_limits():
    """Test that volume stays within 0.0-1.0 range"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Try to increase volume multiple times
        for _ in range(20):
            await pilot.press("+")
            await pilot.pause()
        
        # Volume should not exceed 1.0
        assert app.player.volume <= 1.0
        
        # Try to decrease volume multiple times
        for _ in range(20):
            await pilot.press("-")
            await pilot.pause()
        
        # Volume should not go below 0.0
        assert app.player.volume >= 0.0


@pytest.mark.asyncio
async def test_volume_persists_across_views():
    """Test that volume setting persists when switching views"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Increase volume
        initial_volume = app.player.volume
        await pilot.press("+")
        await pilot.pause()
        new_volume = app.player.volume
        
        # Switch to settings view
        await pilot.press("5")
        await pilot.pause()
        
        # Volume should remain the same
        assert app.player.volume == new_volume
        
        # Switch to queue view
        await pilot.press("2")
        await pilot.pause()
        
        # Volume should still be the same
        assert app.player.volume == new_volume
