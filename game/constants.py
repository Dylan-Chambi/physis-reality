import pygame


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 144
DT = 1/FPS
SHOW_CAMERA = False

SPAWN_ITEM = pygame.USEREVENT + 1
GRAB = pygame.USEREVENT + 2
DROP = pygame.USEREVENT + 3