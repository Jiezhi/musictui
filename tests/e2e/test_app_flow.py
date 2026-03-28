import pytest


@pytest.mark.asyncio
async def test_app_startup():
    """Test that app starts and all components are rendered"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        # Verify all main components exist
        assert app.query_one("#sidebar") is not None
        assert app.query_one("#track-list") is not None
        assert app.query_one("#player-bar") is not None
        assert app.query_one("#status-bar") is not None
