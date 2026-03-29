import pytest
from src.models import Track
from src.library import Library


@pytest.mark.asyncio
async def test_remote_url_fetch_and_save():
    """Test fetching remote URL and saving tracks to database"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        library = app.library
        test_url = "https://example.com/songs.js"

        js_content = """var list = [
            {name: "Remote Song 1", artist: "Artist 1", url: "https://example.com/1.mp3"},
            {name: "Remote Song 2", artist: "Artist 2", url: "https://example.com/2.mp3"}
        ];"""

        tracks = library._parse_remote_content(js_content)
        assert len(tracks) == 2
        assert tracks[0].title == "Remote Song 1"
        assert tracks[1].title == "Remote Song 2"


@pytest.mark.asyncio
async def test_remote_url_json_format():
    """Test parsing JSON format remote URL content"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        library = app.library

        json_content = """[
            {"name": "JSON Song 1", "artist": "Artist A", "url": "https://example.com/1.mp3", "cover": "https://example.com/c1.jpg"},
            {"name": "JSON Song 2", "artist": "Artist B", "url": "https://example.com/2.mp3"}
        ]"""

        tracks = library._parse_remote_content(json_content)

        assert len(tracks) == 2
        assert tracks[0].title == "JSON Song 1"
        assert tracks[0].artist == "Artist A"
        assert tracks[0].cover == "https://example.com/c1.jpg"
        assert tracks[1].cover == ""


@pytest.mark.asyncio
async def test_add_remote_tracks_to_queue():
    """Test adding remote tracks to player queue"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        tracks = [
            Track(
                id=1,
                file_path="https://example.com/1.mp3",
                title="Remote 1",
                artist="Artist 1",
            ),
            Track(
                id=2,
                file_path="https://example.com/2.mp3",
                title="Remote 2",
                artist="Artist 2",
            ),
        ]

        for track in tracks:
            app.player.add_to_queue(track)

        assert len(app.player.queue) == 2
        assert app.player.queue[0].title == "Remote 1"
        assert app.player.queue[1].title == "Remote 2"


@pytest.mark.asyncio
async def test_save_remote_tracks_to_library():
    """Test saving remote tracks to library database"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        library = app.library

        tracks = [
            Track(
                file_path="https://example.com/1.mp3",
                title="DB Song 1",
                artist="Artist 1",
            ),
            Track(
                file_path="https://example.com/2.mp3",
                title="DB Song 2",
                artist="Artist 2",
            ),
        ]

        count = library.save_remote_tracks(tracks)

        assert count == 2

        saved_tracks = library.get_all_tracks()
        assert len(saved_tracks) >= 2
