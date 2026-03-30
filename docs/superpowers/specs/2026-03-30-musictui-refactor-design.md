# MusicTUI 重构设计方案

## 概述

基于 Textual 8.x 重构 MusicTUI，实现功能优先的现代化终端音乐播放器，支持鼠标交互和主题扩展。

## 架构设计

### 1. 项目结构

```
src/
├── app.py                 # 主应用（精简）
├── config.py              # 配置管理
├── models.py              # 数据模型
├── player.py              # 音频播放
├── library.py             # 音乐库管理
├── theme/
│   ├── __init__.py
│   ├── base.py            # 主题基类与协议
│   ├── manager.py         # 主题管理器
│   └── themes/            # 内置主题
│       ├── monokai.py
│       ├── nord.py
│       └── dracula.py
└── ui/
    ├── __init__.py
    ├── widgets/
    │   ├── track_table.py     # 曲目列表（DataTable）
    │   ├── sidebar.py          # 侧边栏（ListView）
    │   ├── player_bar.py      # 播放进度条
    │   ├── search_bar.py       # 搜索栏
    │   └── context_menu.py    # 右键菜单
    ├── views/
    │   ├── library_view.py   # 音乐库视图
    │   ├── queue_view.py     # 播放队列视图
    │   ├── search_view.py    # 搜索视图
    │   ├── favorites_view.py # 收藏视图
    │   └── settings_view.py  # 设置视图
    └── screens/
        └── main_screen.py    # 主屏幕
```

### 2. 主题系统

**主题协议（Theme Protocol）:**

```python
class ThemeProtocol:
    # 基础颜色
    background: str      # 背景色
    surface: str        # 表面色（卡片、侧边栏）
    foreground: str     # 前景色（文字）
    primary: str        # 主色（选中、强调）
    secondary: str      # 次色
    accent: str         # 点缀色

    # 功能颜色
    success: str        # 成功（播放中）
    warning: str         # 警告
    error: str          # 错误

    # 播放状态颜色
    playing: str        # 正在播放
    paused: str         # 暂停
    stopped: str        # 停止

    # 进度条
    progress_bar: str   # 进度条颜色
    progress_background: str

    # 边框与装饰
    border: str
    border_focus: str
```

**主题管理器:**

```python
class ThemeManager:
    def __init__(self)
    def load_theme(self, name: str) -> ThemeProtocol
    def get_current_theme(self) -> ThemeProtocol
    def register_theme(self, name: str, theme: ThemeProtocol)
    def apply_theme(self, app: App, theme: ThemeProtocol)
```

### 3. 视图管理系统

使用 Textual 的 `ContentSwitcher` 或自定义 ViewStack：

```python
class ViewStack(Container):
    def show(self, view_id: str)
    def hide(self, view_id: str)
    def get_current(self) -> str
```

## UI 组件设计

### 1. TrackTable（曲目列表）

基于 `DataTable` 实现：

```python
class TrackTable(DataTable):
    # 列：#、标题、艺术家、专辑、时长
    # 支持排序点击
    # 鼠标点击选中
    # 双击播放

    def on_data_table_row_selected(self, event)
    def on_data_table_row_double_clicked(self, event)
```

### 2. Sidebar（侧边栏）

基于 `ListView` 实现：

```python
class Sidebar(ListView):
    # 项目：Library, Queue, Search, Favorites, Settings
    # 单击切换视图

    def on_list_view_selected(self, event)
```

### 3. PlayerBar（播放条）

```python
class PlayerBar(Static):
    # 显示：封面占位、曲目信息、进度条、控制按钮
    # 鼠标点击进度条跳转位置
    # 播放/暂停按钮点击

    def on_click(self, event)
    def update_progress(self, position: float)
```

### 4. ContextMenu（右键菜单）

使用 Textual 8.x `PopupMenu`：

```python
# 曲目右键菜单
- 播放
- 添加到队列
- 下一首播放
- 收藏
- 移除收藏
- 加入黑名单
- 查看详情
```

## 交互设计

### 1. 鼠标事件

| 组件 | 单击 | 双击 | 右键 |
|------|------|------|------|
| TrackTable 行 | 选中 | 播放 | 弹出菜单 |
| Sidebar 项 | 切换视图 | - | - |
| PlayerBar 进度条 | 跳转位置 | - | - |
| PlayerBar 播放按钮 | 播放/暂停 | - | - |
| Settings 项 | 切换/选中 | - | - |

### 2. 键盘保持

原有快捷键全部保留：
- `j/k` 上下移动
- `Enter` 播放
- `Space` 播放/暂停
- `n/p` 下一首/上一首
- `1-5` 切换视图
- `f` 收藏
- `b` 黑名单

## 实现计划

### Phase 1: 基础设施
1. 创建 theme 模块
2. 实现主题协议和内置主题
3. 实现主题管理器

### Phase 2: UI 组件
1. 重构 TrackTable 基于 DataTable
2. 重构 Sidebar 基于 ListView
3. 重构 PlayerBar 添加鼠标支持
4. 实现 ContextMenu

### Phase 3: 视图层
1. 创建视图管理类
2. 实现各视图
3. 集成到主应用

### Phase 4: 交互增强
1. 添加所有鼠标事件处理
2. 测试与调试

## 兼容性

- Python 3.9+
- Textual 8.x
- 保持与现有配置格式兼容
