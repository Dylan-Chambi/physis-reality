import mediapipe as mp
import cv2
import pygame
import traceback


from game.scenes.Scene import Scene

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

USE_CAMERA = True

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
        self.use_camera = USE_CAMERA
        if self.use_camera:
            self.hands = mp_hands.Hands(
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)
            self.cap = cv2.VideoCapture(0)
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
        try:
            while self.is_running:
                for event in pygame.event.get():
                    self.scene.on_event(event)

                keys = pygame.key.get_pressed()

                self.update(keys)
                # fps text
                pygame.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
        except Exception:
            traceback.print_exc()
        finally:
            self.is_running = False
        pygame.quit()