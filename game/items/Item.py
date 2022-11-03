import numpy as np
from math import radians, degrees, sin, cos
import pygame
import pymunk

from pygame.sprite import Sprite
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, ITEM_FALLED

class Item(Sprite):
    def __init__(self, vertices: list, body: pymunk.Body, x: int, y: int, vx: float, vy: float, scale: int = 1, theta = radians(0), bg_color: tuple = (0, 100, 255, 255), img: pygame.Surface = None, img_width: int = 0, img_height: int = 0) -> None:
        super().__init__()
        self.vertices: list = vertices
        self.body: pymunk.Body = pymunk.Body(body_type=body)
        self.body.position: tuple =(x, y)
        self.x = x
        self.y = y
        self.shape: pymunk.Shape = pymunk.Poly(self.body, self.vertices)
        self.shape.mass: float = 1
        self.shape.color: tuple = (100, 100, 100, 255)
        self.shape.elasticity = 0.4
        self.shape.friction = 0.5
        # self.shape.collision_type = 2
        self.bg_color: tuple = bg_color
        self.img = img
        self.shape.filter = pymunk.ShapeFilter(categories=1, mask=1)
        if img is not None:
            self.surf = img
            self.surf = pygame.transform.scale(self.surf, (img_width, img_height))
            self.rect = self.surf.get_rect(center=(x, y))
        else:
            self.surf = pygame.Surface((img_width, img_height), pygame.SRCALPHA).convert_alpha()
            self.surf.fill(self.bg_color)
            self.rect = self.surf.get_rect(center=(x, y))
        

    def update(self, event_keys: list, scene, dt):
        self.rect.x = self.body.position.x
        self.rect.y = self.body.position.y
        self.rect.center = (self.body.position.x, self.body.position.y)
        if self.body.position.y > SCREEN_HEIGHT or self.body.position.x > SCREEN_WIDTH or self.body.position.x < 0 or self.body.position.y < 0:
            self.kill()
            pygame.event.post(pygame.event.Event(ITEM_FALLED, item=self))

    def draw_in_screen(self) -> None:
        new_points_rotated = [self.body.local_to_world(self.vertices[i]) for i in range(len(self.vertices))]

        if self.img is None:
            screen = pygame.display.get_surface()
            pygame.draw.polygon(screen, self.bg_color, new_points_rotated)
        else:
            rotated_surf = pygame.transform.rotate(self.surf, -degrees(self.body.angle))
            rotated_rect = rotated_surf.get_rect(center=self.rect.center)
            screen = pygame.display.get_surface()
            screen.blit(rotated_surf, rotated_rect)

    def transform(self, t_matrix):
        vert_list = [[v[0], v[1], 1] for v in self.vertices] 
        vert_matrix = np.transpose(np.array(vert_list))
        new_matrix = np.transpose(np.dot(t_matrix, vert_matrix))
        new_vertices = [(v[0], v[1]) for v in new_matrix]
        self.vertices = new_vertices
    
    def rotate(self, theta, xr=None, yr=None):
        if xr is None and yr is None:
            xr = self.vertices[0][0]
            yr = self.vertices[0][1]
        translate_to_matrix = np.array([[1, 0, -xr], [0, 1, -yr], [0, 0, 1]])
        translate_back_matrix = np.array([[1, 0, xr], [0, 1, yr], [0, 0, 1]])
        
        self.transform(translate_to_matrix)


        rotate_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                    [np.sin(theta), np.cos(theta), 0],
                                    [0, 0, 1]])
        self.transform(rotate_matrix)

        self.transform(translate_back_matrix)