import pygame
import sys
from game.App import App
from game.scenes.Scene import Scene
from game.scenes.ui.Button import Button
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from utils.utils import get_assets_path, get_font

class WinScreen(Scene):
    def __init__(self, app: App, menu_scene: Scene = None) -> None:
        super().__init__()
        self.bg_color = (0, 0, 0, 0.8)
        self.app = app
        self.menu_scene = menu_scene
        self.menu_tittle = get_font(100).render("You win!", True, "#ffffff")
        self.menu_rect = self.menu_tittle.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.menu_button = Button(image=pygame.image.load(get_assets_path("assets/sprites/quit_rect.png")), pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200),
                            text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")




    def go_menu(self):
        self.app.change_scene(self.menu_scene)


    def pre_loads(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(get_assets_path("assets/music/win.wav"))
        pygame.mixer.music.play(1)

    def update(self, pressed_keys: list) -> None:
        super().update(pressed_keys)
        screen = pygame.display.get_surface()
        screen.fill(self.bg_color)

        mouse_pos = pygame.mouse.get_pos()

        screen.blit(self.menu_tittle, self.menu_rect)


        for button in [self.menu_button]:
            button.changeColor(mouse_pos)
            button.update(screen)
        

    def on_event(self, event: pygame.event) -> None:
        super().on_event(event)
        if event.type == pygame.QUIT:
            self.app.is_running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.is_running = False
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.menu_button.checkForInput(mouse_pos):
                self.go_menu()
