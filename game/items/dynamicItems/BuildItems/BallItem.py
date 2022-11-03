from math import radians
import pygame
# import pymunk.pygame_util
import pymunk

from game.items.Item import Item
from game.items.ItemRect import ItemRect
from game.constants import GOAL_Y, ITEM_IN_GOAL, SCREEN_HEIGHT, SCREEN_WIDTH, ITEM_FALLED
from pygame.sprite import Sprite

class BallItem(Sprite):
    def __init__(self, x: int, y: int, radio: int, bg_color: tuple = (108, 0, 170, 255), img: pygame.Surface = None) -> None:
        super().__init__()
        self.radio = radio
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position: tuple =(x, y)
        self.shape = pymunk.Circle(self.body, radio)
        self.shape.mass = 1
        self.shape.elasticity = 0.95
        self.shape.friction = 0.9
        self.bg_color: tuple = bg_color
        self.shape.filter = pymunk.ShapeFilter(categories=1, mask=1)

    def update(self, event_keys: list, scene, dt):
        if self.body.position.y < GOAL_Y:
            pygame.event.post(pygame.event.Event(ITEM_IN_GOAL, item=self))
        if self.body.position.y > SCREEN_HEIGHT or self.body.position.x > SCREEN_WIDTH or self.body.position.x < 0 or self.body.position.y < 0:
            self.kill()
            pygame.event.post(pygame.event.Event(ITEM_FALLED, item=self))

    def draw_in_screen(self):
        screen = pygame.display.get_surface()
        pygame.draw.circle(screen, self.bg_color, (self.body.position.x, self.body.position.y), self.radio)