import arcade

from constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from views.menu import MenuView
from views.select import SelectView
from views.game import GameView
from views.pause import PauseView
from views.ending import EndingView


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                         resizable=False)

        self.views = {
            'menu': MenuView(),
            'select': SelectView(),
            'game': GameView(),
            'pause': PauseView(),
            'ending': EndingView()
        }


def main() -> None:
    window = GameWindow()
    window.show_view(window.views['menu'])
    arcade.run()


if __name__ == "__main__":
    main()
