from textual.widgets import Static


class StatusBar(Static):
    def __init__(self, **kwargs):
        super().__init__(
            "NORMAL │ q:quit  space:play/pause  n:next  p:prev  /:search  :scan <path>", **kwargs
        )
