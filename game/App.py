import numpy as np
import pygame


from game.scenes.Scene import Scene



class App:
    def __init__(self, screen_width: int, screen_height: int, show_camera: bool = False, fps: int = 60, init_scene: Scene = None, bg_color: tuple = (39, 185, 245, 0.8)):
        self.width = screen_width
        self.height = screen_height
        self.bg_color = bg_color
        self.fps = fps
        self.dt = 1 / fps
        self.show_camera = show_camera
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.is_running = False
        self.sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.scene = init_scene
        pygame.font.init()
        if self.scene is not None:
            self.scene.pre_loads()


    def change_scene(self, scene: Scene) -> None:
        self.scene = scene
        if self.scene is not None:
            self.scene.pre_loads()


    def update(self, keys):
        if self.scene is not None:
            self.scene.update(keys)

        pygame.display.flip()
        self.clock.tick(self.fps)


    def run(self):
        self.is_running = True
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                self.scene.on_event(event)

            keys = pygame.key.get_pressed()

            self.update(keys)
            # fps text
            pygame.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")

        pygame.quit()