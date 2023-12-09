import arcade

from constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from views.game import GameView


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                         resizable=False)

        self.views = {}
        self.views['game'] = GameView()


def main() -> None:
    window = GameWindow()
    window.show_view(window.views['game'])
    arcade.run()


if __name__ == "__main__":
    main()
