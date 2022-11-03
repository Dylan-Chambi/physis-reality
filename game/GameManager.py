
from game.App import App

from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SHOW_CAMERA
from game.scenes.levels.Level import Level
from game.scenes.menus.MainMenu import MainMenu
from game.scenes.menus.LoseScreen import LoseScreen
from game.scenes.menus.WinScreen import WinScreen
from game.scenes.menus.Splash1 import Splash1
from game.scenes.menus.Splash2 import Splash2
from game.scenes.menus.Credits import Credits

class GameManager():
    def start_game(self):
        app = App(SCREEN_WIDTH, SCREEN_HEIGHT, SHOW_CAMERA, FPS)

        splash_scene1 = Splash1(app)
        splash_scene2 = Splash2(app)

        main_menu = MainMenu(app)

        level = Level(app)

        lose_screen = LoseScreen(app, level, main_menu)
        win_screen = WinScreen(app, main_menu)

        credits = Credits(app, main_menu)



        splash_scene1.next_scene = splash_scene2
        splash_scene2.next_scene = main_menu
        main_menu.play_scene = level
        main_menu.credits_scene = credits
        level.lose_scene = lose_screen
        level.win_scene = win_screen
        level.menu_scene = main_menu

        app.change_scene(splash_scene1)
        app.run()
