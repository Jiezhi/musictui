from textual.containers import Container, Horizontal, Vertical
from src.ui.widgets.sidebar import Sidebar
from src.ui.widgets.track_table import TrackTable


class MainView(Container):
    def compose(self):
        with Horizontal():
            with Vertical(width=20):
                yield Sidebar(id="sidebar")
            with Vertical():
                yield TrackTable(id="track-table")
