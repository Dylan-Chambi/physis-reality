
from game.App import App

from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SHOW_CAMERA
from game.scenes.levels.Level import Level

class GameManager():
    def start_game(self):
        app = App(SCREEN_WIDTH, SCREEN_HEIGHT, SHOW_CAMERA, FPS)
        level = Level(app)
        app.change_scene(level)
        app.run()
