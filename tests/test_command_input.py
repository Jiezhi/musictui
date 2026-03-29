import pytest
from src.ui.command_input import CommandInput


class TestCommandInput:
    def test_initial_state(self):
        cmd_input = CommandInput()
        assert cmd_input.command == ""

    def test_set_command(self):
        cmd_input = CommandInput()
        cmd_input.set_command("test")
        assert cmd_input.get_command() == "test"

    def test_append_char(self):
        cmd_input = CommandInput()
        cmd_input.append_char("t")
        cmd_input.append_char("e")
        cmd_input.append_char("s")
        cmd_input.append_char("t")
        assert cmd_input.get_command() == "test"

    def test_backspace(self):
        cmd_input = CommandInput()
        cmd_input.set_command("test")
        cmd_input.backspace()
        assert cmd_input.get_command() == "tes"

    def test_backspace_empty(self):
        cmd_input = CommandInput()
        cmd_input.backspace()
        assert cmd_input.get_command() == ""

    def test_clear(self):
        cmd_input = CommandInput()
        cmd_input.set_command("test")
        cmd_input.clear()
        assert cmd_input.get_command() == ""

    def test_get_command_empty(self):
        cmd_input = CommandInput()
        assert cmd_input.get_command() == ""
