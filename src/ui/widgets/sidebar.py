from textual.widgets import ListView, ListItem, Static
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
        self._selected_index = 0

    def on_mount(self) -> None:
        for item in self.items:
            self.append(ListItem(Static(item)))
        self.index = self._selected_index

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """列表项选中事件"""
        self.post_message(
            self.ItemClicked(self.items[event.list_view.index], event.list_view.index)
        )

    def get_selected(self) -> str:
        """获取选中的项目"""
        idx = self._selected_index
        if 0 <= idx < len(self.items):
            return self.items[idx]
        return self.items[0]

    def get_selected_index(self) -> int:
        """获取选中索引"""
        return self._selected_index

    def set_selected(self, index: int) -> None:
        """设置选中项"""
        if 0 <= index < len(self.items):
            self._selected_index = index
            self.index = index
