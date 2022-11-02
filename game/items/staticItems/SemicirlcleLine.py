from math import radians, cos, sin, degrees
import pygame
# import pymunk.pygame_util
import pymunk

from pygame.sprite import Sprite
from game.items.Item import Item
from game.items.ItemRect import ItemRect

class SemicirlcleLine(Sprite):
    def __init__(self, x: int, y: int, radio_x: int, radio_y: int, n_points: int, body: pymunk.Body, bg_color: tuple = (100, 100, 100, 255), img: pygame.Surface = None) -> None:
        super().__init__()
        self.points = []
        self.body = []
        self.shape = []
        self.x = x
        self.y = y
        self.radio_x = radio_x
        self.radio_y = radio_y
        self.angle = 0
        for num in range(n_points+1):
            angle = radians(num * (180 / n_points))
            x1 = radio_x * cos(angle)
            y1 = radio_y * sin(angle)
            self.points.append((x1, y1))

        for i in range(len(self.points) - 1):
            self.body.append(pymunk.Body(body_type=body))
            self.body[i].position = (x, y)
            self.shape.append(pymunk.Segment(self.body[i], self.points[i], self.points[i + 1], 20))
            self.shape[i].elasticity = 0.95
            self.shape[i].friction = 0.9

        # self.surf = pygame.Surface((radio_x * 2, radio_y * 2), pygame.SRCALPHA)
        # self.surf.fill(bg_color)
        # self.rect = self.surf.get_rect()
        # self.rect.center = (x, y)

        
        

    
    def update(self, event_keys: list, scene, dt):
        if event_keys[pygame.K_RIGHT]:
            if self.angle < 45:
                self.angle += 50 * dt
                for i in range(len(self.points) - 1):
                    self.body[i].angle = radians(self.angle)
            
                for i in range(len(self.points)):
                    self.points[i] = (self.radio_x * cos(radians(self.angle)) * cos(radians(i * (180 / (len(self.points) - 1)))) - self.radio_y * sin(radians(self.angle)) * sin(radians(i * (180 / (len(self.points) - 1)))), self.radio_x * sin(radians(self.angle)) * cos(radians(i * (180 / (len(self.points) - 1)))) + self.radio_y * cos(radians(self.angle)) * sin(radians(i * (180 / (len(self.points) - 1)))))



        if event_keys[pygame.K_LEFT]:
            if self.angle > -45:
                self.angle -= 50 * dt
                for i in range(len(self.points) - 1):
                    self.body[i].angle = radians(self.angle)
            
                for i in range(len(self.points)):
                    self.points[i] = (self.radio_x * cos(radians(self.angle)) * cos(radians(i * (180 / (len(self.points) - 1)))) - self.radio_y * sin(radians(self.angle)) * sin(radians(i * (180 / (len(self.points) - 1)))), self.radio_x * sin(radians(self.angle)) * cos(radians(i * (180 / (len(self.points) - 1)))) + self.radio_y * cos(radians(self.angle)) * sin(radians(i * (180 / (len(self.points) - 1)))))


    def draw_in_screen(self) -> None:
        screen = pygame.display.get_surface()
        for i in range(len(self.points) - 1):
            pygame.draw.line(screen, (255, 255, 255), (self.points[i][0] + self.x, self.points[i][1] + self.y), (self.points[i + 1][0] + self.x, self.points[i + 1][1] + self.y), 40)
            pygame.draw.circle(screen, (255, 255, 255), (self.points[i][0] + self.x, self.points[i][1] + self.y), 20)
        pygame.draw.circle(screen, (255, 255, 255), (self.points[-1][0] + self.x, self.points[-1][1] + self.y), 20)
    def on_event(self, event):
        pass
        # print("I am a SemicirlcleLine and I received an event", event)
