from math import radians
import pygame
# import pymunk.pygame_util
import pymunk

from game.items.Item import Item
from game.items.ItemRect import ItemRect
from game.constants import GOAL_Y, ITEM_IN_GOAL

class SemiTriangle(Item):
    def __init__(self, x: int, y: int, width: int, heigth: int, bg_color: tuple = (108, 0, 170, 255), img: pygame.Surface = None) -> None:
        # star vertices
        heigth = -heigth
        # l shape vertices
        vertices_array = [
            (-width, heigth),
            (-width, -heigth),
            (width/2, -heigth),
            (width/2, -heigth/2),
            (-width/2, heigth)
        ]
        super().__init__(vertices_array, pymunk.Body.DYNAMIC, x, y, 0, 0, bg_color=bg_color, img=img, img_width=width, img_height=-heigth)

    def update(self, event_keys: list, scene, dt):
        super().update(event_keys, scene, dt)
        if self.body.position.y < GOAL_Y:
            pygame.event.post(pygame.event.Event(ITEM_IN_GOAL, item=self))
            # velocity = self.body.velocity
            # if velocity.y < 0:
            #     print("velocity.y < 0")
