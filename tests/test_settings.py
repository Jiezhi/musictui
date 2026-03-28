import pytest
from textual.widgets import Static
from src.ui.settings import Settings


def test_settings_initialization():
    settings = Settings()
    assert settings is not None
    assert hasattr(settings, "items")


def test_settings_default_items():
    settings = Settings()
    expected_items = ["Volume", "Play Mode", "Theme", "Library Paths"]
    assert settings.items == expected_items


def test_settings_move_up():
    settings = Settings()
    settings.selected = 2
    settings.move_up()
    assert settings.selected == 1


def test_settings_move_up_wraps():
    settings = Settings()
    settings.selected = 0
    settings.move_up()
    assert settings.selected == len(settings.items) - 1


def test_settings_move_down():
    settings = Settings()
    settings.selected = 1
    settings.move_down()
    assert settings.selected == 2


def test_settings_move_down_wraps():
    settings = Settings()
    settings.selected = len(settings.items) - 1
    settings.move_down()
    assert settings.selected == 0


def test_settings_get_selected():
    settings = Settings()
    settings.selected = 1
    assert settings.get_selected() == "Play Mode"


def test_settings_update_value():
    settings = Settings()
    settings.selected = 0
    settings.update_value("Volume", 0.5)
    assert settings.values["Volume"] == 0.5


def test_settings_get_value():
    settings = Settings()
    assert settings.get_value("Volume") == 0.7


def test_settings_toggle_play_mode():
    settings = Settings()
    initial_mode = settings.values["Play Mode"]
    settings.toggle_play_mode()
    new_mode = settings.values["Play Mode"]
    assert new_mode in ["loop", "shuffle", "repeat_one"]


def test_settings_cycle_theme():
    settings = Settings()
    initial_theme = settings.values["Theme"]
    settings.cycle_theme()
    new_theme = settings.values["Theme"]
    assert new_theme in ["monokai", "nord", "dracula"]
