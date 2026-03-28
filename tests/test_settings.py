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


def test_settings_displays_values():
    settings = Settings()
    settings._update_content()
    content = settings.get_display_text()
    assert "Volume" in content
    assert "70%" in content
    assert "Play Mode" in content
    assert "loop" in content


def test_settings_increase_volume():
    settings = Settings()
    settings.selected = 0
    initial_volume = settings.values["Volume"]
    settings.adjust_volume(0.1)
    assert settings.values["Volume"] == initial_volume + 0.1


def test_settings_decrease_volume():
    settings = Settings()
    settings.selected = 0
    settings.values["Volume"] = 0.5
    settings.adjust_volume(-0.1)
    assert settings.values["Volume"] == 0.4


def test_settings_volume_clamped():
    settings = Settings()
    settings.values["Volume"] = 0.9
    settings.adjust_volume(0.2)
    assert settings.values["Volume"] == 1.0


def test_settings_volume_min_clamped():
    settings = Settings()
    settings.values["Volume"] = 0.1
    settings.adjust_volume(-0.2)
    assert settings.values["Volume"] == 0.0


def test_settings_toggle_value():
    settings = Settings()
    settings.selected = 1
    initial_mode = settings.values["Play Mode"]
    settings.toggle_value()
    new_mode = settings.values["Play Mode"]
    assert new_mode != initial_mode


def test_settings_library_paths():
    settings = Settings()
    settings.set_library_paths(["/music", "/downloads"])
    assert settings.values["Library Paths"] == "/music, /downloads"


def test_settings_get_display_text():
    settings = Settings()
    settings.selected = 0
    text = settings.get_display_text()
    assert "Volume" in text
    assert ">" in text
