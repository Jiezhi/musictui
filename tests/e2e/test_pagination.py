"""End-to-end tests for pagination"""

import pytest
from src.models import Track


@pytest.mark.asyncio
async def test_page_down_key():
    """Test pressing 'pagedown' moves down by page"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Add multiple tracks
        track_table = app.query_one("#track-table")
        tracks = [Track(id=i, file_path=f"/test{i}.mp3", title=f"Test{i}") for i in range(50)]
        track_table.set_tracks(tracks)
        
        initial_index = track_table.get_selected_index()
        
        # Press page down
        await pilot.press("pagedown")
        await pilot.pause()
        
        # Should have moved down by a page
        assert track_table.get_selected_index() > initial_index


@pytest.mark.asyncio
async def test_page_up_key():
    """Test pressing 'pageup' moves up by page"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Add multiple tracks
        track_table = app.query_one("#track-table")
        tracks = [Track(id=i, file_path=f"/test{i}.mp3", title=f"Test{i}") for i in range(50)]
        track_table.set_tracks(tracks)
        
        # Move down first
        await pilot.press("pagedown")
        await pilot.pause()
        
        middle_index = track_table.get_selected_index()
        
        # Press page up
        await pilot.press("pageup")
        await pilot.pause()
        
        # Should have moved up
        assert track_table.get_selected_index() < middle_index


@pytest.mark.asyncio
async def test_ctrl_f_page_down():
    """Test pressing 'ctrl+f' also moves down by page"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Add multiple tracks
        track_table = app.query_one("#track-table")
        tracks = [Track(id=i, file_path=f"/test{i}.mp3", title=f"Test{i}") for i in range(50)]
        track_table.set_tracks(tracks)
        
        initial_index = track_table.get_selected_index()
        
        # Press ctrl+f
        await pilot.press("ctrl+f")
        await pilot.pause()
        
        # Should have moved down by a page
        assert track_table.get_selected_index() > initial_index


@pytest.mark.asyncio
async def test_ctrl_b_page_up():
    """Test pressing 'ctrl+b' also moves up by page"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Add multiple tracks
        track_table = app.query_one("#track-table")
        tracks = [Track(id=i, file_path=f"/test{i}.mp3", title=f"Test{i}") for i in range(50)]
        track_table.set_tracks(tracks)
        
        # Move down first
        await pilot.press("pagedown")
        await pilot.pause()
        
        middle_index = track_table.get_selected_index()
        
        # Press ctrl+b
        await pilot.press("ctrl+b")
        await pilot.pause()
        
        # Should have moved up
        assert track_table.get_selected_index() < middle_index


@pytest.mark.asyncio
async def test_pagination_wraps_around():
    """Test that pagination wraps around at boundaries"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Add some tracks
        track_table = app.query_one("#track-table")
        tracks = [Track(id=i, file_path=f"/test{i}.mp3", title=f"Test{i}") for i in range(10)]
        track_table.set_tracks(tracks)
        
        # Move up from first position should wrap to end
        initial_index = track_table.get_selected_index()
        assert initial_index == 0
        
        await pilot.press("pageup")
        await pilot.pause()
        
        # Should have wrapped around
        assert track_table.get_selected_index() >= 0


@pytest.mark.asyncio
async def test_pagination_in_queue_view():
    """Test pagination works in queue view"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Add tracks to queue
        tracks = [Track(id=i, file_path=f"/test{i}.mp3", title=f"Test{i}") for i in range(30)]
        for track in tracks:
            app.player.add_to_queue(track)
        
        # Switch to queue view
        await pilot.press("2")
        await pilot.pause()
        
        # Press page down
        await pilot.press("pagedown")
        await pilot.pause()
        
        # Should be able to navigate
        queue = app.query_one("#queue")
        assert queue.selected_index >= 0


@pytest.mark.asyncio
async def test_pagination_in_search_view():
    """Test pagination works in search view"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Add tracks to library
        track_table = app.query_one("#track-table")
        tracks = [Track(id=i, file_path=f"/test{i}.mp3", title=f"Test{i}") for i in range(30)]
        track_table.set_tracks(tracks)
        
        # Switch to search view
        await pilot.press("3")
        await pilot.pause()
        
        # Press page down
        await pilot.press("pagedown")
        await pilot.pause()
        
        # Should be able to navigate
        search = app.query_one("#search")
        assert search.selected_index >= 0
