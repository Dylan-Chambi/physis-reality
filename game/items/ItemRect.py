from math import degrees, radians
import pygame
# import pymunk.pygame_util
import pymunk

from game.items.Item import Item

class ItemRect(Item):
    def __init__(self, x: int, y: int, width: int, heigth: int, body: pymunk.body, scale: int = 1, theta = radians(0), bg_color: tuple = (0, 100, 255, 255), img: pygame.Surface = None) -> None:
        vertices_array = [
            (-width/2, -heigth/2),
            (width/2, -heigth/2),
            (width/2, heigth/2),
            (-width/2, heigth/2)
            # (x + width / 2, y + heigth / 2),
            # (x + width / 2, y - heigth / 2),
            # (x - width / 2, y - heigth / 2),
            # (x - width / 2, y + heigth / 2)
        ]
        super().__init__(vertices_array, body, x, y, 0, 0, scale, theta, bg_color=bg_color, img=img, img_width=width, img_height=heigth)

    def update(self, event_keys: list, scene, dt):
        super().update(event_keys, scene, dt)
        pass
        
        
    

    def draw_in_screen(self) -> None:
        screen = pygame.display.get_surface()
        # screen.blit(self.surf, self.rect)