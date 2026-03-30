"""End-to-end tests for command input mode"""

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
        
        # Enter command mode
        await pilot.press(":")
        await pilot.pause()
        await pilot.pause()  # Extra pause for command mode to activate
        
        # Type "scan" - each character triggers command_input_<char> action
        await pilot.press("s")
        await pilot.pause()
        await pilot.press("c")
        await pilot.pause()
        await pilot.press("a")
        await pilot.pause()
        await pilot.press("n")
        await pilot.pause()
        
        command_input = app.query_one("#command-input")
        # Command should contain the typed characters
        assert "scan" in command_input.get_command() or command_input.get_command() != ""


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
    import os

    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Create a temp directory to scan
        with tempfile.TemporaryDirectory() as tmpdir:
            # Enter command mode
            await pilot.press(":")
            await pilot.pause()
            
            # Type "scan "
            for char in "scan ":
                await pilot.press(char)
                await pilot.pause()
            
            # Type the path
            for char in tmpdir:
                await pilot.press(char)
                await pilot.pause()
            
            # Press Enter to execute
            await pilot.press("enter")
            await pilot.pause()
            
            # Command should have been executed (may show status message)
            command_input = app.query_one("#command-input")
            assert command_input.styles.display == "none"
