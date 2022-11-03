from math import radians, cos, sin, degrees
import pygame
# import pymunk.pygame_util
import pymunk

from pygame.sprite import Sprite
from game.items.Item import Item
from game.items.ItemRect import ItemRect

class Container(Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, body: pymunk.Body, bg_color: tuple = (94, 62, 4, 255), img: pygame.Surface = None) -> None:
        super().__init__()
        self.points = []
        self.body = []
        self.shape = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = 0
        self.angle_threshold = 15
        self.bg_color = bg_color

        self.points.append((-self.width/2, -self.height))
        self.points.append((-self.width/2, 0))
        self.points.append((self.width/2, 0))
        self.points.append((self.width/2, -self.height))



        for i in range(len(self.points) - 1):
            self.body.append(pymunk.Body(body_type=body))
            self.body[i].position = (x, y)
            self.shape.append(pymunk.Segment(self.body[i], self.points[i], self.points[i + 1], 20))
            self.shape[i].friction = 0.5
            self.shape[i].elasticity = 0.5

        # self.surf = pygame.Surface((radio_x * 2, radio_y * 2), pygame.SRCALPHA)
        # self.surf.fill(bg_color)
        # self.rect = self.surf.get_rect()
        # self.rect.center = (x, y)

        
        

    
    def update(self, event_keys: list, scene, dt):
        for i in range(len(self.points) - 1):
            if self.angle > 0:
                if self.body[i].angle > radians(-self.angle_threshold):
                    self.body[i].angle += radians(max(-self.angle, -30)) * dt
            elif self.angle < 0:
                if self.body[i].angle < radians(self.angle_threshold):
                    self.body[i].angle += radians(min(-self.angle, 30)) * dt
        if event_keys[pygame.K_RIGHT]:
            if self.angle < 45:
                self.angle += 50 * dt
                for i in range(len(self.points) - 1):
                    self.body[i].angle = radians(self.angle)
            
                for i in range(len(self.points)):
                    self.points[i] = (self.width * cos(radians(self.angle)) * cos(radians(i * (180 / (len(self.points) - 1)))) - self.height * sin(radians(self.angle)) * sin(radians(i * (180 / (len(self.points) - 1)))), self.width * sin(radians(self.angle)) * cos(radians(i * (180 / (len(self.points) - 1)))) + self.height * cos(radians(self.angle)) * sin(radians(i * (180 / (len(self.points) - 1)))))

        if event_keys[pygame.K_LEFT]:
            if self.angle > -45:
                self.angle -= 50 * dt
                for i in range(len(self.points) - 1):
                    self.body[i].angle = radians(self.angle)
            
                for i in range(len(self.points)):
                    self.points[i] = (self.width * cos(radians(self.angle)) * cos(radians(i * (180 / (len(self.points) - 1)))) - self.height * sin(radians(self.angle)) * sin(radians(i * (180 / (len(self.points) - 1)))), self.width * sin(radians(self.angle)) * cos(radians(i * (180 / (len(self.points) - 1)))) + self.height * cos(radians(self.angle)) * sin(radians(i * (180 / (len(self.points) - 1)))))


    def draw_in_screen(self) -> None:
        screen = pygame.display.get_surface()
        for i in range(len(self.points) - 1):
            new_point_rotated = (self.points[i][0] * cos(self.body[i].angle) - self.points[i][1] * sin(self.body[i].angle), self.points[i][0] * sin(self.body[i].angle) + self.points[i][1] * cos(self.body[i].angle))
            new_point2_rotated = (self.points[i + 1][0] * cos(self.body[i].angle) - self.points[i + 1][1] * sin(self.body[i].angle), self.points[i + 1][0] * sin(self.body[i].angle) + self.points[i + 1][1] * cos(self.body[i].angle))
            pygame.draw.line(screen, self.bg_color, (new_point_rotated[0] + self.x, new_point_rotated[1] + self.y), (new_point2_rotated[0] + self.x, new_point2_rotated[1] + self.y), 40)
            pygame.draw.circle(screen, self.bg_color, (new_point_rotated[0] + self.x, new_point_rotated[1] + self.y), 20)
        pygame.draw.circle(screen, self.bg_color, (new_point2_rotated[0] + self.x, new_point2_rotated[1] + self.y), 20)
        pygame.draw.circle(screen, (112, 112, 119), (self.x, self.y), 10)
        # rgb(112, 112, 119)


    def on_event(self, event):
        pass
        # print("I am a SemicirlcleLine and I received an event", event)
