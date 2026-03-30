# MusicTUI 重构实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 Textual 8.x 重构 MusicTUI，实现功能优先的现代化终端音乐播放器，支持鼠标交互和主题扩展

**Architecture:** 
- 使用 theme 模块实现主题协议和管理器
- 使用 DataTable 替代自定义渲染实现曲目列表
- 使用 ListView 实现侧边栏
- 使用 PopupMenu 实现右键菜单
- 使用 ContentSwitcher 管理视图切换

**Tech Stack:** Python 3.9+, Textual 8.x, Pydantic

---

## 文件结构

```
src/
├── theme/
│   ├── __init__.py
│   ├── base.py            # 主题基类与协议
│   ├── manager.py         # 主题管理器
│   └── themes/            # 内置主题
│       ├── __init__.py
│       ├── monokai.py
│       ├── nord.py
│       └── dracula.py
└── ui/
    ├── widgets/
    │   ├── track_table.py     # 曲目列表（DataTable）
    │   ├── sidebar.py          # 侧边栏（ListView）
    │   ├── player_bar.py      # 播放进度条
    │   └── context_menu.py    # 右键菜单
    └── views/
        └── main_view.py       # 主视图容器
```

---

## Task 1: 创建主题模块基础结构

**Files:**
- Create: `src/theme/__init__.py`
- Create: `src/theme/base.py`
- Create: `src/theme/manager.py`
- Create: `src/theme/themes/__init__.py`
- Create: `src/theme/themes/monokai.py`
- Create: `src/theme/themes/nord.py`
- Create: `src/theme/themes/dracula.py`

- [ ] **Step 1: 创建 src/theme/__init__.py**

```python
from src.theme.base import ThemeProtocol, ThemeColors
from src.theme.manager import ThemeManager

__all__ = ["ThemeProtocol", "ThemeColors", "ThemeManager"]
```

- [ ] **Step 2: 创建 src/theme/base.py**

```python
from typing import Protocol, runtime_checkable
from dataclasses import dataclass


@runtime_checkable
class ThemeProtocol(Protocol):
    """主题协议定义"""

    @property
    def name(self) -> str:
        """主题名称"""
        ...

    @property
    def background(self) -> str:
        """背景色"""
        ...

    @property
    def surface(self) -> str:
        """表面色（卡片、侧边栏）"""
        ...

    @property
    def foreground(self) -> str:
        """前景色（文字）"""
        ...

    @property
    def primary(self) -> str:
        """主色（选中、强调）"""
        ...

    @property
    def secondary(self) -> str:
        """次色"""
        ...

    @property
    def accent(self) -> str:
        """点缀色"""
        ...

    @property
    def success(self) -> str:
        """成功色"""
        ...

    @property
    def warning(self) -> str:
        """警告色"""
        ...

    @property
    def error(self) -> str:
        """错误色"""
        ...

    @property
    def playing(self) -> str:
        """播放中颜色"""
        ...

    @property
    def paused(self) -> str:
        """暂停颜色"""
        ...

    @property
    def stopped(self) -> str:
        """停止颜色"""
        ...

    @property
    def progress_bar(self) -> str:
        """进度条颜色"""
        ...

    @property
    def progress_background(self) -> str:
        """进度条背景"""
        ...

    @property
    def border(self) -> str:
        """边框色"""
        ...

    @property
    def border_focus(self) -> str:
        """聚焦边框色"""
        ...


@dataclass
class ThemeColors:
    """主题颜色集合"""
    name: str
    background: str = "#272822"
    surface: str = "#3e3d32"
    foreground: str = "#f8f8f2"
    primary: str = "#f92672"
    secondary: str = "#ae81ff"
    accent: str = "#66d9ef"
    success: str = "#a6e22e"
    warning: str = "#e6db74"
    error: str = "#f92672"
    playing: str = "#a6e22e"
    paused: str = "#e6db74"
    stopped: str = "#75715e"
    progress_bar: str = "#f92672"
    progress_background: str = "#49483e"
    border: str = "#49483e"
    border_focus: str = "#f92672"
```

- [ ] **Step 3: 创建 src/theme/manager.py**

```python
from typing import Dict, Optional
from src.theme.base import ThemeProtocol, ThemeColors


class ThemeManager:
    """主题管理器"""

    def __init__(self):
        self._themes: Dict[str, ThemeColors] = {}
        self._current_theme: Optional[ThemeColors] = None

    def register_theme(self, theme: ThemeColors) -> None:
        """注册主题"""
        self._themes[theme.name] = theme

    def load_theme(self, name: str) -> Optional[ThemeColors]:
        """加载主题"""
        return self._themes.get(name)

    def get_current_theme(self) -> Optional[ThemeColors]:
        """获取当前主题"""
        return self._current_theme

    def set_theme(self, name: str) -> bool:
        """设置当前主题"""
        theme = self.load_theme(name)
        if theme:
            self._current_theme = theme
            return True
        return False

    def get_theme_names(self) -> list[str]:
        """获取所有主题名称"""
        return list(self._themes.keys())


# 全局主题管理器实例
_theme_manager = ThemeManager()


def get_theme_manager() -> ThemeManager:
    """获取全局主题管理器"""
    return _theme_manager


def init_themes() -> None:
    """初始化内置主题"""
    from src.theme.themes.monokai import MonokaiTheme
    from src.theme.themes.nord import NordTheme
    from src.theme.themes.dracula import DraculaTheme

    manager = get_theme_manager()
    manager.register_theme(MonokaiTheme())
    manager.register_theme(NordTheme())
    manager.register_theme(DraculaTheme())
    manager.set_theme("monokai")
```

- [ ] **Step 4: 创建 src/theme/themes/__init__.py**

```python
from src.theme.themes.monokai import MonokaiTheme
from src.theme.themes.nord import NordTheme
from src.theme.themes.dracula import DraculaTheme

__all__ = ["MonokaiTheme", "NordTheme", "DraculaTheme"]
```

- [ ] **Step 5: 创建 src/theme/themes/monokai.py**

```python
from src.theme.base import ThemeColors


class MonokaiTheme(ThemeColors):
    """Monokai 主题"""

    def __init__(self):
        super().__init__(
            name="monokai",
            background="#272822",
            surface="#3e3d32",
            foreground="#f8f8f2",
            primary="#f92672",
            secondary="#ae81ff",
            accent="#66d9ef",
            success="#a6e22e",
            warning="#e6db74",
            error="#f92672",
            playing="#a6e22e",
            paused="#e6db74",
            stopped="#75715e",
            progress_bar="#f92672",
            progress_background="#49483e",
            border="#49483e",
            border_focus="#f92672",
        )
```

- [ ] **Step 6: 创建 src/theme/themes/nord.py**

```python
from src.theme.base import ThemeColors


class NordTheme(ThemeColors):
    """Nord 主题"""

    def __init__(self):
        super().__init__(
            name="nord",
            background="#2e3440",
            surface="#3b4252",
            foreground="#eceff4",
            primary="#88c0d0",
            secondary="#81a1c1",
            accent="#5e81ac",
            success="#a3be8c",
            warning="#ebcb8b",
            error="#bf616a",
            playing="#a3be8c",
            paused="#ebcb8b",
            stopped="#4c566a",
            progress_bar="#88c0d0",
            progress_background="#434c5e",
            border="#4c566a",
            border_focus="#88c0d0",
        )
```

- [ ] **Step 7: 创建 src/theme/themes/dracula.py**

```python
from src.theme.base import ThemeColors


class DraculaTheme(ThemeColors):
    """Dracula 主题"""

    def __init__(self):
        super().__init__(
            name="dracula",
            background="#282a36",
            surface="#44475a",
            foreground="#f8f8f2",
            primary="#ff79c6",
            secondary="#bd93f9",
            accent="#8be9fd",
            success="#50fa7b",
            warning="#f1fa8c",
            error="#ff5555",
            playing="#50fa7b",
            paused="#f1fa8c",
            stopped="#6272a4",
            progress_bar="#ff79c6",
            progress_background="#44475a",
            border="#44475a",
            border_focus="#ff79c6",
        )
```

- [ ] **Step 8: 提交**

```bash
git add src/theme/
git commit -m "feat: 添加主题模块基础结构"
```

---

## Task 2: 创建 UI 组件 - TrackTable

**Files:**
- Create: `src/ui/widgets/track_table.py`
- Test: `tests/test_track_table.py`

- [ ] **Step 1: 创建 src/ui/widgets/track_table.py**

```python
from typing import Optional, Callable
from textual.data_table import DataTable
from textual.events import RowSelected
from textual.message import Message
from textual.widgets import Button
from src.models import Track


class TrackTable(DataTable):
    """曲目列表组件，基于 DataTable"""

    class TrackSelected(Message):
        """曲目选中消息"""

        def __init__(self, track: Optional[Track], index: int) -> None:
            super().__init__()
            self.track = track
            self.index = index

    class TrackDoubleClicked(Message):
        """曲目双击消息"""

        def __init__(self, track: Optional[Track], index: int) -> None:
            super().__init__()
            self.track = track
            self.index = index

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracks: list[Track] = []
        self.cursor_type = "none"

    def on_mount(self) -> None:
        self.add_columns("#", "Title", "Artist", "Album", "Duration")

    def set_tracks(self, tracks: list[Track], total_count: int = 0) -> None:
        """设置曲目列表"""
        self.tracks = tracks
        self.clear()
        for i, track in enumerate(tracks):
            duration = self._format_duration(track.duration)
            self.add_row(
                str(i + 1),
                track.title or "Unknown",
                track.artist or "Unknown",
                track.album or "Unknown",
                duration,
                key=str(track.id),
            )
        if tracks:
            self.cursor_row = 0

    def _format_duration(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    def get_selected_track(self) -> Optional[Track]:
        """获取选中的曲目"""
        if 0 <= self.cursor_row < len(self.tracks):
            return self.tracks[self.cursor_row]
        return None

    def get_selected_index(self) -> int:
        """获取选中索引"""
        return self.cursor_row

    def move_up(self) -> None:
        """上移选择"""
        if self.cursor_row > 0:
            self.cursor_row -= 1

    def move_down(self) -> None:
        """下移选择"""
        if self.cursor_row < len(self.tracks) - 1:
            self.cursor_row += 1

    def on_data_table_row_selected(self, event: RowSelected) -> None:
        """行选中事件"""
        track = self.get_selected_track()
        self.post_message(self.TrackSelected(track, self.cursor_row))

    def on_data_table_row_double_clicked(self, event: RowSelected) -> None:
        """行双击事件"""
        track = self.get_selected_track()
        self.post_message(self.TrackDoubleClicked(track, self.cursor_row))
```

- [ ] **Step 2: 创建测试 tests/test_track_table.py**

```python
import pytest
from src.ui.widgets.track_table import TrackTable
from src.models import Track


class TestTrackTable:
    def test_initial_state(self):
        table = TrackTable()
        assert table.tracks == []

    def test_set_tracks(self):
        table = TrackTable()
        tracks = [
            Track(id=1, title="Song 1", artist="Artist 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", artist="Artist 2", file_path="/b.mp3"),
        ]
        table.set_tracks(tracks, 2)
        assert len(table.tracks) == 2
        assert table.cursor_row == 0

    def test_get_selected_track(self):
        table = TrackTable()
        tracks = [Track(id=1, title="Song 1", file_path="/a.mp3")]
        table.set_tracks(tracks, 1)
        track = table.get_selected_track()
        assert track is not None
        assert track.title == "Song 1"

    def test_move_up(self):
        table = TrackTable()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        table.set_tracks(tracks, 2)
        table.cursor_row = 1
        table.move_up()
        assert table.cursor_row == 0

    def test_move_down(self):
        table = TrackTable()
        tracks = [
            Track(id=1, title="Song 1", file_path="/a.mp3"),
            Track(id=2, title="Song 2", file_path="/b.mp3"),
        ]
        table.set_tracks(tracks, 2)
        table.move_down()
        assert table.cursor_row == 1
```

- [ ] **Step 3: 运行测试**

```bash
pytest tests/test_track_table.py -v
```

- [ ] **Step 4: 提交**

```bash
git add src/ui/widgets/track_table.py tests/test_track_table.py
git commit -feat: 添加 TrackTable 组件"
```

---

## Task 3: 创建 UI 组件 - Sidebar

**Files:**
- Create: `src/ui/widgets/sidebar.py`
- Test: `tests/test_sidebar.py`

- [ ] **Step 1: 创建 src/ui/widgets/sidebar.py**

```python
from typing import Optional
from textual.widgets import ListView, ListItem, Static
from textual.events import ItemSelected
from textual.message import Message


class Sidebar(ListView):
    """侧边栏组件，基于 ListView"""

    class ItemClicked(Message):
        """项目被点击消息"""

        def __init__(self, item: str, index: int) -> None:
            super().__init__()
            self.item = item
            self.index = index

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = ["Library", "Queue", "Search", "Favorites", "Settings"]

    def on_mount(self) -> None:
        for item in self.items:
            self.append(ListItem(Static(item)))

    def on_list_view_selected(self, event: ItemSelected) -> None:
        """列表项选中事件"""
        self.post_message(self.ItemClicked(self.items[event.list_view.index], event.list_view.index))

    def get_selected(self) -> str:
        """获取选中的项目"""
        if 0 <= self.index < len(self.items):
            return self.items[self.index]
        return self.items[0]

    def get_selected_index(self) -> int:
        """获取选中索引"""
        return self.index

    def set_selected(self, index: int) -> None:
        """设置选中项"""
        if 0 <= index < len(self.items):
            self.index = index
            self.cursor_position = index
```

- [ ] **Step 2: 创建测试 tests/test_sidebar.py**

```python
import pytest
from src.ui.widgets.sidebar import Sidebar


class TestSidebar:
    def test_initial_items(self):
        sidebar = Sidebar()
        assert sidebar.items == ["Library", "Queue", "Search", "Favorites", "Settings"]

    def test_get_selected(self):
        sidebar = Sidebar()
        assert sidebar.get_selected() == "Library"

    def test_set_selected(self):
        sidebar = Sidebar()
        sidebar.set_selected(2)
        assert sidebar.get_selected() == "Search"
```

- [ ] **Step 3: 运行测试**

```bash
pytest tests/test_sidebar.py -v
```

- [ ] **Step 4: 提交**

```bash
git add src/ui/widgets/sidebar.py tests/test_sidebar.py
git commit - "feat: 添加 Sidebar 组件"
```

---

## Task 4: 创建 UI 组件 - PlayerBar（支持鼠标）

**Files:**
- Create: `src/ui/widgets/player_bar.py`
- Test: `tests/test_player_bar.py`

- [ ] **Step 1: 创建 src/ui/widgets/player_bar.py**

```python
from textual.widgets import Static
from textual.message import Message


class PlayerBar(Static):
    """播放条组件，支持鼠标点击"""

    class PlayPauseClicked(Message):
        """播放/暂停按钮点击"""
        pass

    class ProgressClicked(Message):
        """进度条点击"""
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_track_title = "No track"
        self.current_track_artist = ""
        self.current_time = 0.0
        self.duration = 0.0

    def update_track(
        self,
        title: str,
        artist: str,
        current_time: float = 0.0,
        duration: float = 0.0,
    ) -> None:
        """更新曲目信息"""
        self.current_track_title = title
        self.current_track_artist = artist
        self.current_time = current_time
        self.duration = duration
        self._render_content()

    def _render_content(self) -> None:
        """渲染内容"""
        progress = ""
        if self.duration > 0:
            progress_width = 30
            filled = int((self.current_time / self.duration) * progress_width)
            progress = "[" + "=" * filled + "-" * (progress_width - filled) + "]"

        track_info = f"{self.current_track_title}"
        if self.current_track_artist:
            track_info += f" - {self.current_track_artist}"

        time_info = f"{self._format_time(self.current_time)} / {self._format_time(self.duration)}"

        self.update(f"{track_info} {progress} {time_info}")

    def _format_time(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    def on_click(self, event) -> None:
        """点击事件"""
        # 简单实现：点击任意位置切换播放/暂停
        self.post_message(self.PlayPauseClicked())
```

- [ ] **Step 2: 创建测试 tests/test_player_bar.py**

```python
import pytest
from src.ui.widgets.player_bar import PlayerBar


class TestPlayerBar:
    def test_initial_state(self):
        bar = PlayerBar()
        assert bar.current_track_title == "No track"

    def test_update_track(self):
        bar = PlayerBar()
        bar.update_track("Test Song", "Test Artist", 30.0, 180.0)
        assert bar.current_track_title == "Test Song"
        assert bar.current_track_artist == "Test Artist"
        assert bar.duration == 180.0

    def test_format_time(self):
        bar = PlayerBar()
        assert bar._format_time(65.0) == "1:05"
        assert bar._format_time(0.0) == "0:00"
```

- [ ] **Step 3: 运行测试**

```bash
pytest tests/test_player_bar.py -v
```

- [ ] **Step 4: 提交**

```bash
git add src/ui/widgets/player_bar.py tests/test_player_bar.py
git commit - "feat: 添加 PlayerBar 组件"
```

---

## Task 5: 创建右键菜单组件

**Files:**
- Create: `src/ui/widgets/context_menu.py`

- [ ] **Step 1: 创建 src/ui/widgets/context_menu.py**

```python
from typing import Callable
from textual.app import App
from textual.widgets import Button, Static
from textual.containers import Container
from textual.popup import Popup
from textual.message import Message
from src.models import Track


class TrackContextMenu(Popup):
    """曲目右键菜单"""

    class MenuItemSelected(Message):
        """菜单项选中消息"""

        def __init__(self, action: str, track: Track) -> None:
            super().__init__()
            self.action = action
            self.track = track

    def __init__(self, track: Track, **kwargs):
        super().__init__(**kwargs)
        self.track = track

    def compose(self):
        yield Container(
            Button("Play", id="play", variant="primary"),
            Button("Add to Queue", id="queue"),
            Button("Next Track", id="next"),
            Button("Favorite", id="favorite"),
            Button("Blacklist", id="blacklist"),
            classes="menu-buttons",
        )

    def on_button_pressed(self, event) -> None:
        """按钮点击事件"""
        self.post_message(self.MenuItemSelected(event.button.id, self.track))
        self.dismiss()
```

---

## Task 6: 创建主视图容器

**Files:**
- Create: `src/ui/views/main_view.py`

- [ ] **Step 1: 创建 src/ui/views/main_view.py**

```python
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static
from src.ui.widgets.sidebar import Sidebar
from src.ui.widgets.track_table import TrackTable
from src.ui.widgets.player_bar import PlayerBar


class MainView(Container):
    """主视图容器"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self):
        with Horizontal():
            with Vertical(width=20, id="sidebar-container"):
                yield Sidebar(id="sidebar")
            with Vertical(id="content-container"):
                yield TrackTable(id="track-table")
                yield PlayerBar(id="player-bar")
```

---

## Task 7: 重构主应用 app.py

**Files:**
- Modify: `src/app.py`
- Create: `src/ui/__init__.py`
- Create: `src/ui/widgets/__init__.py`
- Create: `src/ui/views/__init__.py`

- [ ] **Step 1: 创建 src/ui/__init__.py**

```python
from src.ui.views.main_view import MainView

__all__ = ["MainView"]
```

- [ ] **Step 2: 创建 src/ui/widgets/__init__.py**

```python
from src.ui.widgets.track_table import TrackTable
from src.ui.widgets.sidebar import Sidebar
from src.ui.widgets.player_bar import PlayerBar

__all__ = ["TrackTable", "Sidebar", "PlayerBar"]
```

- [ ] **Step 3: 创建 src/ui/views/__init__.py**

```python
from src.ui.views.main_view import MainView

__all__ = ["MainView"]
```

- [ ] **Step 4: 重构 src/app.py**

```python
import os
from textual.app import App
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from src.config import get_config, save_config
from src.player import Player
from src.library import Library
from src.theme import get_theme_manager, init_themes
from src.theme.base import ThemeColors
from src.ui.widgets.track_table import TrackTable
from src.ui.widgets.sidebar import Sidebar
from src.ui.widgets.player_bar import PlayerBar
from src.ui.widgets.context_menu import TrackContextMenu
from src.models import PlayerState, PlayMode


class MusicTUI(App):
    CSS = """
    Screen {
        background: $surface;
    }
    #main-container {
        width: 100%;
        height: 100%;
    }
    #sidebar {
        width: 20;
        dock: left;
        border: solid $primary;
    }
    #track-table {
        width: 1fr;
        height: 100%;
    }
    #player-bar {
        height: 3;
        dock: bottom;
        border-top: solid $primary;
    }
    """

    BINDINGS = [
        Binding("space", "play_pause", "Play/Pause", show=False),
        Binding("n", "next", "Next", show=False),
        Binding("p", "previous", "Prev", show=False),
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
        Binding("enter", "play_selected", "Play", show=False),
        Binding("q", "quit", "Quit", show=False),
        Binding("1", "show_library", "Library", show=False),
        Binding("2", "show_queue", "Queue", show=False),
        Binding("3", "show_search", "Search", show=False),
        Binding("4", "show_favorites", "Favorites", show=False),
        Binding("5", "show_settings", "Settings", show=False),
        Binding("+", "volume_up", "Vol+", show=False),
        Binding("=", "volume_up", "Vol+", show=False),
        Binding("-", "volume_down", "Vol-", show=False),
        Binding("_", "volume_down", "Vol-", show=False),
        Binding("f", "add_favorite", "Favorite", show=False),
        Binding("b", "add_to_blacklist", "Block", show=False),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_view = "library"
        init_themes()

    def compose(self):
        with Container(id="main-container"):
            with Horizontal():
                with Vertical(width=20):
                    yield Sidebar(id="sidebar")
                with Vertical():
                    yield TrackTable(id="track-table")
            yield PlayerBar(id="player-bar")

    def _apply_theme(self, theme: ThemeColors) -> None:
        """应用主题颜色"""
        self.theme = theme.name

    def on_mount(self) -> None:
        self.config = get_config()
        self.player = Player()
        self.library = Library(os.path.expanduser("~/.musictui/music.db"))

        # 应用主题
        theme_manager = get_theme_manager()
        theme_manager.set_theme(self.config.ui.theme)
        theme = theme_manager.get_current_theme()
        if theme:
            self._apply_theme(theme)

        # 初始化数据
        self.total_tracks = self.library.get_total_count()
        if self.total_tracks == 0:
            for path in self.config.library_paths:
                if os.path.exists(path):
                    self.library.scan_local(path)
            self.total_tracks = self.library.get_total_count()

        self.tracks = self.library.get_all_tracks(limit=50)

        # 设置播放器
        self.player.set_volume(self.config.player.volume)
        if self.config.player.play_mode == "shuffle":
            self.player.set_play_mode(PlayMode.SHUFFLE)

        self.player.set_on_track_change(self._on_track_change)
        self.player.set_on_state_change(self._on_state_change)

        # 加载曲目
        self._load_tracks()

    def _load_tracks(self):
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track_table.set_tracks(self.tracks, self.total_count)
        except Exception:
            pass

    def _on_track_change(self, track):
        self.call_later(self._update_player_bar)

    def _on_state_change(self, state):
        self.call_later(self._update_player_bar)

    def _update_player_bar(self, current_time: float = 0.0):
        try:
            player_bar = self.query_one("#player-bar", PlayerBar)
            current = self.player.get_current_track()
            if current:
                player_bar.update_track(
                    current.title, current.artist, current_time, current.duration
                )
            else:
                player_bar.update_track("No track", "", 0.0, 0.0)
        except Exception:
            pass

    def action_play_pause(self) -> None:
        if self.player.state == PlayerState.PLAYING:
            self.player.pause()
        elif self.player.state == PlayerState.PAUSED:
            self.player.resume()
        else:
            track_table = self.query_one("#track-table", TrackTable)
            track = track_table.get_selected_track()
            if track:
                self.player.play(track)

    def action_next(self) -> None:
        self.player.next()

    def action_previous(self) -> None:
        self.player.previous()

    def action_quit(self) -> None:
        self.player.stop()
        self.exit()

    def action_move_down(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track_table.move_down()
        except Exception:
            pass

    def action_move_up(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track_table.move_up()
        except Exception:
            pass

    def action_play_selected(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track = track_table.get_selected_track()
            if track:
                self.player.play(track)
        except Exception:
            pass

    def action_volume_up(self) -> None:
        volume = self.player.volume + 0.1
        self.player.set_volume(min(1.0, volume))
        self.config.player.volume = self.player.volume
        save_config(self.config)

    def action_volume_down(self) -> None:
        volume = self.player.volume - 0.1
        self.player.set_volume(max(0.0, volume))
        self.config.player.volume = self.player.volume
        save_config(self.config)

    def action_show_library(self) -> None:
        self.current_view = "library"
        self.tracks = self.library.get_all_tracks(limit=50)
        self._load_tracks()

    def action_show_queue(self) -> None:
        self.current_view = "queue"
        # TODO: 加载队列

    def action_show_search(self) -> None:
        self.current_view = "search"
        # TODO: 显示搜索

    def action_show_favorites(self) -> None:
        self.current_view = "favorites"
        favorites = self.library.get_favorites()
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track_table.set_tracks(favorites, len(favorites))
        except Exception:
            pass

    def action_show_settings(self) -> None:
        self.current_view = "settings"

    def action_add_favorite(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track = track_table.get_selected_track()
            if track and track.id:
                self.library.add_favorite(track.id)
        except Exception:
            pass

    def action_add_to_blacklist(self) -> None:
        try:
            track_table = self.query_one("#track-table", TrackTable)
            track = track_table.get_selected_track()
            if track and track.id:
                self.library.add_to_blacklist(track.id)
        except Exception:
            pass

    # 鼠标事件处理
    def on_sidebar_item_clicked(self, event) -> None:
        """侧边栏项目点击"""
        item = event.item
        if item == "Library":
            self.action_show_library()
        elif item == "Queue":
            self.action_show_queue()
        elif item == "Search":
            self.action_show_search()
        elif item == "Favorites":
            self.action_show_favorites()
        elif item == "Settings":
            self.action_show_settings()

    def on_track_table_track_selected(self, event) -> None:
        """曲目选中（单击）"""
        pass

    def on_track_table_track_double_clicked(self, event) -> None:
        """曲目双击"""
        if event.track:
            self.player.play(event.track)
```

- [ ] **Step 5: 运行测试**

```bash
pytest tests/ -v
```

- [ ] **Step 6: 提交**

```bash
git add src/app.py src/ui/
git commit - "refactor: 重构主应用使用新组件"
```

---

## Task 8: 添加右键菜单支持

**Files:**
- Modify: `src/app.py`

- [ ] **Step 1: 添加右键菜单**

在 TrackTable 的右键菜单功能需要添加。这需要使用 Textual 的 ContextMenu。

```python
# 在 MusicTUI 类中添加
def on_track_table_track_selected(self, event) -> None:
    """右键菜单"""
    if event.track:
        self.push_screen(
            TrackContextMenu(event.track),
            self._handle_menu_action,
        )

def _handle_menu_action(self, result) -> None:
    """处理菜单选择结果"""
    if result.action == "play":
        self.player.play(result.track)
    elif result.action == "queue":
        self.player.add_to_queue(result.track)
    elif result.action == "favorite":
        self.library.add_favorite(result.track.id)
    elif result.action == "blacklist":
        self.library.add_to_blacklist(result.track.id)
```

---

## 执行检查

运行完整测试套件确保一切正常：

```bash
pytest tests/ -v
```

---

**计划完成。执行方式选择？**

1. **Subagent-Driven (推荐)** - 每个任务分配给子代理，快速迭代
2. **Inline Execution** - 在当前会话中执行任务
