import pygame
import sys
import os

def calculate_center(vertices: list, x: int, y: int) -> tuple:
    x_sum = 0
    y_sum = 0
    for vertex in vertices:
        x_sum += vertex[0]
        y_sum += vertex[1]
    return (x_sum / len(vertices) + x, y_sum / len(vertices) + y)

def collition_query(static_items: list, point: tuple) -> bool:
    for item in static_items:
        if item.rect.collidepoint(point):
            return True
    return False

def get_font(size):
    return pygame.font.Font(get_assets_path("assets/fonts/font.ttf"), size)

def get_assets_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)