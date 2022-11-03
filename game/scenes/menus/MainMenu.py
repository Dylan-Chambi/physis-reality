import pygame
import sys
from game.App import App
from game.scenes.Scene import Scene
from game.scenes.ui.Button import Button
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from utils.utils import get_font, get_assets_path

class MainMenu(Scene):
    def __init__(self, app: App, play_scene: Scene = None, credits_scene: Scene = None) -> None:
        super().__init__()
        self.bg_color = (39, 185, 245, 0.8)
        self.app = app
        self.play_scene = play_scene
        self.credits_scene = credits_scene
        self.menu_tittle = get_font(100).render("Physis Reality", True, "#D3D3D3")
        self.menu_rect = self.menu_tittle.get_rect(center=(SCREEN_WIDTH / 2, 130))
        self.background = pygame.transform.scale(pygame.image.load(get_assets_path("assets/sprites/back_blue.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))

        play_background = pygame.image.load(get_assets_path("assets/sprites/play_rect.png"))
        play_background = pygame.transform.scale(play_background, (play_background.get_width() + 100, play_background.get_height() + 60))

        self.play_button = Button(image=play_background, pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80),
                            text_input="PLAY", font=get_font(100), base_color="#d7fcd4", hovering_color="White")
        self.credits_button = Button(image=pygame.image.load(get_assets_path("assets/sprites/credits_rect.png")), pos=(SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2 + 150),
                            text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.quit_button = Button(image=pygame.image.load(get_assets_path("assets/sprites/credits_rect.png")), pos=(SCREEN_WIDTH / 3 * 2, SCREEN_HEIGHT / 2 + 150),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    def play(self):
        self.app.change_scene(self.play_scene)

    def credits(self):
        self.app.change_scene(self.credits_scene)

    def pre_loads(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(get_assets_path("assets/music/menu_song.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

    def update(self, pressed_keys: list) -> None:
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()


        screen.blit(self.menu_tittle, self.menu_rect)

        for button in [self.play_button, self.credits_button, self.quit_button]:
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
            if self.play_button.checkForInput(mouse_pos):
                self.play()
            if self.credits_button.checkForInput(mouse_pos):
                self.credits()
            if self.quit_button.checkForInput(mouse_pos):
                self.app.is_running = False
                pygame.quit()
                sys.exit()
