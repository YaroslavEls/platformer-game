from arcade import View as ArcadeView


class View(ArcadeView):
    def __init__(self):
        super().__init__()

        self.started = False

    def setup(self):
        self.started = True

    def on_show(self):
        if not self.started:
            self.setup()
