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
