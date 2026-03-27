import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class PlayerConfig(BaseModel):
    volume: float = 0.7
    play_mode: str = "loop"


class WebDAVConfig(BaseModel):
    enabled: bool = False
    url: str = ""
    username: str = ""
    password: str = ""


class UIConfig(BaseModel):
    theme: str = "monokai"


class Config(BaseModel):
    library_paths: list[str] = Field(default_factory=list)
    webdav: WebDAVConfig = Field(default_factory=WebDAVConfig)
    player: PlayerConfig = Field(default_factory=PlayerConfig)
    ui: UIConfig = Field(default_factory=UIConfig)


_config: Optional[Config] = None


def get_config(config_path: Optional[Path] = None) -> Config:
    global _config
    if _config is not None:
        return _config

    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "settings.json"

    if config_path.exists():
        with open(config_path) as f:
            data = json.load(f)
            _config = Config(**data)
    else:
        _config = Config()
        save_config(_config, config_path)

    return _config


def save_config(config: Config, config_path: Optional[Path] = None) -> None:
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "settings.json"

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config.model_dump(), f, indent=2)
