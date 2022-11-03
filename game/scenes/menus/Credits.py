import pygame
import sys
from game.App import App
from game.scenes.Scene import Scene
from game.scenes.ui.Button import Button
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from utils.utils import get_font, get_assets_path

class Credits(Scene):
    def __init__(self, app: App, back_scene: Scene = None) -> None:
        super().__init__()
        self.bg_color = (0, 0, 0, 0.8)
        self.app = app
        self.back_scene = back_scene
        self.menu_tittle = get_font(100).render("Credits", True, "#ffffff")
        self.menu_rect = self.menu_tittle.get_rect(center=(SCREEN_WIDTH / 2, 130))
        self.back_button = Button(image=pygame.image.load(get_assets_path("assets/sprites/quit_rect.png")), pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200),
                            text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Column 1
        self.programmers_text_tittle = get_font(50).render("Programmers", True, "#ffffff")
        self.programmers_text_tittle_rect = self.programmers_text_tittle.get_rect(center=(SCREEN_WIDTH / 4, 300))
        self.programmers_text = get_font(30).render("Dylan Chambi", True, "#ffffff")
        self.programmers_text_rect = self.programmers_text.get_rect(center=(SCREEN_WIDTH / 4, 350))

        self.artists_text_tittle = get_font(50).render("Artists", True, "#ffffff")
        self.artists_text_tittle_rect = self.artists_text_tittle.get_rect(center=(SCREEN_WIDTH / 4, 450))
        self.artists_text = get_font(30).render("Dylan Chambi", True, "#ffffff")
        self.artists_text_rect = self.artists_text.get_rect(center=(SCREEN_WIDTH / 4, 500))

        self.music_text_tittle = get_font(50).render("Music selectors", True, "#ffffff")
        self.music_text_tittle_rect = self.music_text_tittle.get_rect(center=(SCREEN_WIDTH / 4, 600))
        self.music_text = get_font(30).render("Dylan Chambi", True, "#ffffff")
        self.music_text_rect = self.music_text.get_rect(center=(SCREEN_WIDTH / 4, 650))


        # Column 2

        self.special_thanks_text_tittle = get_font(50).render("Special Thanks", True, "#ffffff")
        self.special_thanks_text_tittle_rect = self.special_thanks_text_tittle.get_rect(center=(SCREEN_WIDTH / 4 * 3, 300))
        self.special_thanks_text = get_font(30).render("Ing. Jose Laruta", True, "#ffffff")
        self.special_thanks_text_rect = self.special_thanks_text.get_rect(center=(SCREEN_WIDTH / 4 * 3, 350))

        self.subject_text_tittle = get_font(50).render("Subject", True, "#ffffff")
        self.subject_text_tittle_rect = self.subject_text_tittle.get_rect(center=(SCREEN_WIDTH / 4 * 3, 450))
        self.subject_text = get_font(30).render("Infographic", True, "#ffffff")
        self.subject_text_rect = self.subject_text.get_rect(center=(SCREEN_WIDTH / 4 * 3, 500))

        self.students_text_tittle = get_font(50).render("Student", True, "#ffffff")
        self.students_text_tittle_rect = self.students_text_tittle.get_rect(center=(SCREEN_WIDTH / 4 * 3, 600))
        self.students_text = get_font(30).render("Dylan Chambi", True, "#ffffff")
        self.students_text_rect = self.students_text.get_rect(center=(SCREEN_WIDTH / 4 * 3, 650))



    def go_back(self):
        self.app.change_scene(self.back_scene)


    def pre_loads(self) -> None:
        pass

    def update(self, pressed_keys: list) -> None:
        screen = pygame.display.get_surface()
        screen.fill(self.bg_color)

        mouse_pos = pygame.mouse.get_pos()


        screen.blit(self.menu_tittle, self.menu_rect)
        screen.blit(self.programmers_text_tittle, self.programmers_text_tittle_rect)
        screen.blit(self.programmers_text, self.programmers_text_rect)
        screen.blit(self.artists_text_tittle, self.artists_text_tittle_rect)
        screen.blit(self.artists_text, self.artists_text_rect)
        screen.blit(self.music_text_tittle, self.music_text_tittle_rect)
        screen.blit(self.music_text, self.music_text_rect)
        screen.blit(self.students_text_tittle, self.students_text_tittle_rect)
        screen.blit(self.students_text, self.students_text_rect)
        screen.blit(self.special_thanks_text_tittle, self.special_thanks_text_tittle_rect)
        screen.blit(self.special_thanks_text, self.special_thanks_text_rect)
        screen.blit(self.subject_text_tittle, self.subject_text_tittle_rect)
        screen.blit(self.subject_text, self.subject_text_rect)


        for button in [self.back_button]:
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
            if self.back_button.checkForInput(mouse_pos):
                self.go_back()
