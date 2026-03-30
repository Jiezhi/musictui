from typing import Optional
from src.theme.base import ThemeProtocol, ThemeColors


class ThemeManager:
    def __init__(self):
        self._themes: dict[str, ThemeProtocol] = {}
        self._current_theme: Optional[ThemeProtocol] = None

    def register(self, theme: ThemeProtocol) -> None:
        self._themes[theme.name] = theme

    def load(self, name: str) -> bool:
        return name in self._themes

    def set_theme(self, name: str) -> bool:
        if self.load(name):
            self._current_theme = self._themes[name]
            return True
        return False

    @property
    def current(self) -> Optional[ThemeProtocol]:
        return self._current_theme

    @property
    def theme_names(self) -> list[str]:
        return list(self._themes.keys())


_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager


def init_themes() -> ThemeManager:
    from src.theme.themes.monokai import MonokaiTheme
    from src.theme.themes.nord import NordTheme
    from src.theme.themes.dracula import DraculaTheme

    manager = get_theme_manager()
    manager.register(MonokaiTheme())
    manager.register(NordTheme())
    manager.register(DraculaTheme())
    manager.set_theme("nord")
    return manager
