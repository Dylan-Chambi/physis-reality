from math import radians, cos, sin
import pygame
# import pymunk.pygame_util
import pymunk

from game.items.Item import Item
from game.items.ItemRect import ItemRect

class SemicirlcleLine:
    def __init__(self, x: int, y: int, radio: int, density: int, body: pymunk.Body, bg_color: tuple = (100, 100, 100, 255), img: pygame.Surface = None) -> None:
        self.body = pymunk.Body(body_type=body)
        self.body.position = (x, y)
        self.points = []
        self.points.append((x, y))
        self.points.append((x + radio, y))
        self.points.append((x + radio, y + radio))
        self.points.append((x, y + radio))
        # self.points.append((x, y))
        # for num in range(density):
        #     self.points.append((x + radio * cos(radians(num * 360 / density)), y + radio * sin(radians(num * 360 / density))))
        # self.points.append((x + radio * cos(radians(0)), y + radio * sin(radians(0))))
        # self.points.append((x + radio * cos(radians(360 / density)), y + radio * sin(radians(360 / density))))

        self.shape = pymunk.Poly(self.body, self.points)
        self.mass = 1
        self.shape.elasticity = 0.95
        self.shape.friction = 0.9
        self.surf = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA).convert_alpha()
        self.surf.fill(bg_color)
        self.rect = self.surf.get_rect(center=(x, y))
        

    
    def update(self, event_keys: list, scene):
        pass

    # def draw_in_screen(self) -> None:
    #     screen = pygame.display.get_surface()
    #     pygame.draw.lines(screen, self.bg_color, False, self.points, self.width)