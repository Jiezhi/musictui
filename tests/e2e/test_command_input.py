"""End-to-end tests for command input mode"""

from unittest.mock import patch

import pytest
from src.models import Track


@pytest.mark.asyncio
async def test_command_input_exists():
    """Test that command input widget exists"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        command_input = app.query_one("#command-input")
        assert command_input is not None


@pytest.mark.asyncio
async def test_command_input_hidden_by_default():
    """Test that command input is hidden by default"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        command_input = app.query_one("#command-input")
        assert command_input.styles.display == "none"


@pytest.mark.asyncio
async def test_start_command_mode():
    """Test pressing ':' enters command mode"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Press ':' to start command
        await pilot.press(":")
        await pilot.pause()
        
        command_input = app.query_one("#command-input")
        assert command_input.styles.display == "block"
        assert app.command_mode is True


@pytest.mark.asyncio
async def test_type_command():
    """Test typing characters in command mode"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        await pilot.press(":")
        await pilot.pause()
        await pilot.pause()

        for char in "scan /tmp":
            await pilot.press(char)
            await pilot.pause()

        command_input = app.query_one("#command-input")
        assert command_input.get_command() == "scan /tmp"


@pytest.mark.asyncio
async def test_command_backspace():
    """Test backspace in command mode"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Enter command mode and type
        await pilot.press(":")
        await pilot.pause()
        await pilot.pause()
        await pilot.press("s")
        await pilot.pause()
        await pilot.press("c")
        await pilot.pause()
        
        # Press backspace
        await pilot.press("backspace")
        await pilot.pause()
        
        command_input = app.query_one("#command-input")
        # Backspace should have removed at least one character
        assert len(command_input.get_command()) < 2


@pytest.mark.asyncio
async def test_command_mode_executes_on_enter():
    """Test pressing Enter executes command"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Enter command mode
        await pilot.press(":")
        await pilot.pause()
        await pilot.pause()
        
        # Type a command (help command for testing)
        await pilot.press("h")
        await pilot.pause()
        await pilot.press("e")
        await pilot.pause()
        await pilot.press("l")
        await pilot.pause()
        await pilot.press("p")
        await pilot.pause()
        
        # Press Enter to execute
        await pilot.press("enter")
        await pilot.pause()
        
        # Command input should be hidden or cleared after execution
        command_input = app.query_one("#command-input")
        # After execution, command mode exits and command is cleared or hidden
        assert command_input.styles.display == "none" or command_input.get_command() == ""


@pytest.mark.asyncio
async def test_escape_exits_command_mode():
    """Test pressing Escape exits command mode"""
    from src.app import MusicTUI

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Enter command mode
        await pilot.press(":")
        await pilot.pause()
        
        # Press Escape
        await pilot.press("escape")
        await pilot.pause()
        
        command_input = app.query_one("#command-input")
        assert command_input.styles.display == "none"
        assert app.command_mode is False


@pytest.mark.asyncio
async def test_command_mode_with_scan():
    """Test scan command in command mode"""
    from src.app import MusicTUI
    import tempfile

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()

        with tempfile.TemporaryDirectory() as tmpdir:
            await pilot.press(":")
            await pilot.pause()
            await pilot.pause()

            for char in f"scan {tmpdir}":
                await pilot.press(char)
                await pilot.pause()

            command_input = app.query_one("#command-input")
            assert command_input.get_command() == f"scan {tmpdir}"

            with patch.object(app.library, "scan_local", return_value=[]) as mock_scan:
                await pilot.press("enter")
                await pilot.pause()

            mock_scan.assert_called_once_with(tmpdir)

            command_input = app.query_one("#command-input")
            assert command_input.styles.display == "none"
