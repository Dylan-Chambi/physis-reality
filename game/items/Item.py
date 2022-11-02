import numpy as np
from math import radians
import pygame
import pymunk

from pygame.sprite import Sprite
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Item(Sprite):
    def __init__(self, vertices: list, body: pymunk.Body, x: int, y: int, vx: float, vy: float, scale: int = 1, theta = radians(0), bg_color: tuple = (0, 100, 255, 255)) -> None:
        super().__init__()
        self.vertices: list = vertices
        self.body: pymunk.Body = pymunk.Body(body_type=body)
        self.body.position: tuple =(x, y)
        # self.body.velocity: tuple = (vx, vy)
        # self.body.angular_velocity: float = 0
        self.shape: pymunk.Shape = pymunk.Poly(self.body, self.vertices)
        self.shape.mass: float = 1
        self.shape.color: tuple = bg_color
        self.shape.elasticity = 0.4
        self.shape.friction = 0.5
        # self.shape.collision_type = 2
        self.bg_color: tuple = bg_color

    def update(self, event_keys: list, scene, dt):
        pass

    def draw_in_screen(self, screen: pygame.Surface) -> None:
        # screen = pygame.display.get_surface()
        pass

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