from math import radians
import pygame
# import pymunk.pygame_util
import pymunk

from game.items.Item import Item
from game.items.ItemRect import ItemRect

class LItem(Item):
    def __init__(self, x: int, y: int, width: int, heigth: int, bg_color: tuple = (108, 0, 170, 255), img: pygame.Surface = None) -> None:
        # star vertices
        heigth = -heigth
        # l shape vertices
        vertices_array = [
            (-width, heigth),
            (-width, -heigth),
            (width/2, -heigth),
            (width/2, -heigth/2),
            (-width/2, -heigth/2),
            (-width/2, heigth)
        ]
        super().__init__(vertices_array, pymunk.Body.DYNAMIC, x, y, 0, 0, bg_color=bg_color, img=img, img_width=width, img_height=-heigth)
