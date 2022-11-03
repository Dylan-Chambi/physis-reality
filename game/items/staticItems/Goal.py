import pygame
import pymunk


from pygame.sprite import Sprite
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Goal(Sprite):
    def __init__(self, y: int, heigth: int, bg_color: tuple = (255, 0, 0, 255), img: pygame.Surface = None) -> None:
        super().__init__()
        if img is None:
            self.image = pygame.Surface((SCREEN_WIDTH, heigth))
            self.image.fill(bg_color)
        else:
            self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (0, y)
        self.shape = pymunk.Segment(self.body, (0, 0), (SCREEN_WIDTH, 0), 0)
        self.shape.elasticity = 0.95
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(categories=1000, mask=1000)
        self.x = 0
        self.y = y
        self.bg_color = bg_color
        self.time_to_win = 3


    def update(self, event_keys: list, scene, dt):
        pass

    def draw_in_screen(self) -> None:
        screen = pygame.display.get_surface()
        pygame.draw.line(screen, self.bg_color, (0, self.y), (SCREEN_WIDTH, self.y), 5)
