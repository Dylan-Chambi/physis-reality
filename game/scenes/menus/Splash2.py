import pygame
import sys
from game.App import App
from game.scenes.Scene import Scene
from game.scenes.ui.Button import Button
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, GO_NEXT_EVENT
from utils.utils import get_assets_path, get_font


class Splash2(Scene):
    def __init__(self, app: App, next_scene: Scene = None) -> None:
        super().__init__()
        self.bg_color = (0, 0, 0, 0.8)
        self.app = app
        self.next_scene = next_scene
        self.menu_tittle = get_font(75).render("Presents...", True, "#ffffff")
        self.menu_rect = self.menu_tittle.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))




    def go_next(self):
        self.app.change_scene(self.next_scene)


    def pre_loads(self) -> None:
        pygame.mixer.music.stop()
        pygame.time.set_timer(GO_NEXT_EVENT, 4000)

    def update(self, pressed_keys: list) -> None:
        super().update(pressed_keys)
        screen = pygame.display.get_surface()
        screen.fill(self.bg_color)

        self.menu_tittle.set_alpha(self.menu_tittle.get_alpha() - 1)

        screen.blit(self.menu_tittle, self.menu_rect)

        

    def on_event(self, event: pygame.event) -> None:
        super().on_event(event)
        if event.type == GO_NEXT_EVENT:
            self.go_next()