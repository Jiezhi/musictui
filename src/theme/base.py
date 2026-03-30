from typing import Protocol
from dataclasses import dataclass


class ThemeProtocol(Protocol):
    name: str
    background: str
    surface: str
    foreground: str
    primary: str
    secondary: str
    accent: str
    success: str
    warning: str
    error: str
    playing: str
    paused: str
    stopped: str
    progress_bar: str
    progress_background: str
    border: str
    border_focus: str


@dataclass
class ThemeColors:
    name: str
    background: str
    surface: str
    foreground: str
    primary: str
    secondary: str
    accent: str
    success: str
    warning: str
    error: str
    playing: str
    paused: str
    stopped: str
    progress_bar: str
    progress_background: str
    border: str
    border_focus: str
