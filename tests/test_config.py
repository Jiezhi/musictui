import pytest
from src.config import Config, get_config


def test_config_default_values():
    config = Config()
    assert config.library_paths == []
    assert config.player.volume == 0.7
    assert config.player.play_mode == "loop"


def test_config_loads_from_file():
    config = get_config()
    assert config is not None
    assert hasattr(config, 'library_paths')
