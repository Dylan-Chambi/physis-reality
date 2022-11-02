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
        super().__init__(vertices_array, body, x, y, 0, 0, scale, theta, bg_color=bg_color)
        if img is not None:
            self.surf = img
            self.surf = pygame.transform.scale(self.surf, (width, heigth))
            self.rect = self.surf.get_rect(center=(x, y))
        else:
            self.surf = pygame.Surface((width, heigth), pygame.SRCALPHA).convert_alpha()
            self.surf.fill(self.bg_color)
            self.rect = self.surf.get_rect(center=(x, y))

    def update(self, event_keys: list, scene, dt):
        super().update(event_keys, scene, dt)
        self.rect.x = self.body.position.x
        self.rect.y = self.body.position.y
        self.rect.center = (self.body.position.x, self.body.position.y)
        rotated_surf = pygame.transform.rotate(self.surf, -degrees(self.body.angle))
        rotated_rect = rotated_surf.get_rect(center=self.rect.center)
        screen = pygame.display.get_surface()
        screen.blit(rotated_surf, rotated_rect)
        
        
    

    def draw_in_screen(self) -> None:
        screen = pygame.display.get_surface()
        # screen.blit(self.surf, self.rect)