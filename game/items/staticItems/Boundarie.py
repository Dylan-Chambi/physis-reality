from math import radians
import pygame
# import pymunk.pygame_util
import pymunk

from game.items.Item import Item
from game.items.ItemRect import ItemRect

from utils.utils import get_assets_path

class Boundarie(ItemRect):
    def __init__(self, x: int, y: int, width: int, heigth: int, bg_color: tuple = (100, 100, 100, 255), img: pygame.Surface = None) -> None:
        img_load = pygame.image.load(get_assets_path("assets/sprites/wood.jpg"))
        scale_factor = min(width, heigth)
        img_load = pygame.transform.scale(img_load, (scale_factor, scale_factor))
        self.img_rotated = pygame.transform.rotate(img_load, 90)
        super().__init__(x, y, width, heigth, pymunk.Body.STATIC, bg_color=bg_color, img=img_load)


    def draw_in_screen(self) -> None:
        screen = pygame.display.get_surface()
        image_size = min(self.width, self.heigth)
        images_count = max(self.width, self.heigth) // image_size
        image_rest = max(self.width, self.heigth) % image_size
        for i in range(images_count):
            if self.width > self.heigth:
                screen.blit(self.img_rotated, (i * image_size, self.y - self.heigth/2))
            else:
                screen.blit(self.img, (self.x - self.width/2, i * image_size))
        if image_rest > 0:
            if self.width > self.heigth:
                new_img = pygame.transform.scale(self.img_rotated, (image_rest, image_size))
                screen.blit(new_img, (images_count * image_size, self.y - self.heigth/2))
            else:
                new_img = pygame.transform.scale(self.img, (image_size, image_rest))
                screen.blit(new_img, (self.x - self.width/2, images_count * image_size))