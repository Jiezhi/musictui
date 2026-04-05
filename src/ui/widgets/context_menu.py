from textual.widgets import Button
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.message import Message
from src.models import Track


class TrackContextMenu(ModalScreen):
    """曲目右键菜单"""

    class MenuItemSelected(Message):
        def __init__(self, action: str, track: Track) -> None:
            super().__init__()
            self.action = action
            self.track = track

    def __init__(self, track: Track, **kwargs):
        super().__init__(**kwargs)
        self.track = track

    def compose(self):
        with Container(classes="context-menu"):
            with Vertical(classes="menu-buttons"):
                yield Button("Play", id="play", variant="primary")
                yield Button("Add to Queue", id="queue")
                yield Button("Next Track", id="next")
                yield Button("Favorite", id="favorite")
                yield Button("Blacklist", id="blacklist")

    def on_button_pressed(self, event) -> None:
        self.post_message(self.MenuItemSelected(event.button.id, self.track))
        self.dismiss()
