import pytest
from src.models import Track


@pytest.mark.asyncio
async def test_search_view_exists():
    """Test that Search view component exists in the app"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        search = app.query_one("#search")
        assert search is not None


@pytest.mark.asyncio
async def test_search_view_hidden_by_default():
    """Test that Search view is hidden initially"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        search = app.query_one("#search")
        assert search.styles.display == "none"


@pytest.mark.asyncio
async def test_show_search_keybinding():
    """Test that pressing 3 key shows search view"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.press("3")
        await pilot.pause()

        search = app.query_one("#search")
        assert search.styles.display == "block"

        track_list = app.query_one("#track-list")
        assert track_list.styles.display == "none"


@pytest.mark.asyncio
async def test_search_navigation():
    """Test navigation in search view with j/k keys"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        search = app.query_one("#search")
        search.set_results(
            [
                Track(
                    id=1, file_path="/test1.mp3", title="Song One", artist="Artist A"
                ),
                Track(
                    id=2, file_path="/test2.mp3", title="Song Two", artist="Artist B"
                ),
            ]
        )

        await pilot.press("3")
        await pilot.pause()

        initial_index = search.selected_index

        await pilot.press("j")
        await pilot.pause()

        assert search.selected_index == initial_index + 1

        await pilot.press("k")
        await pilot.pause()

        assert search.selected_index == initial_index


@pytest.mark.asyncio
async def test_search_play_selected():
    """Test pressing Enter plays the selected search result"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        search = app.query_one("#search")
        track = Track(
            id=1,
            file_path="tests/e2e/fixtures/test.mp3",
            title="Test Song",
            artist="Test Artist",
        )
        search.set_results([track])

        await pilot.press("3")
        await pilot.pause()

        await pilot.press("enter")
        await pilot.pause()

        assert len(app.player.queue) > 0


@pytest.mark.asyncio
async def test_search_perform_search():
    """Test that search performs actual search"""
    from src.app import MusicTUI
    from unittest.mock import MagicMock

    app = MusicTUI()
    async with app.run_test() as pilot:
        search = app.query_one("#search")

        mock_library = MagicMock()
        mock_library.search.return_value = [
            Track(
                id=1, file_path="/test.mp3", title="Found Song", artist="Found Artist"
            )
        ]

        search.perform_search("test", mock_library)

        mock_library.search.assert_called_once_with("test")
        assert len(search.results) == 1
        assert search.results[0].title == "Found Song"
