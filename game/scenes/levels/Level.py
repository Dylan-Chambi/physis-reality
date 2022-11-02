import mediapipe as mp
import cv2
import pygame
import math
import asyncio
import threading
import pymunk
import pymunk.pygame_util
from game.items.dynamicItems.BuildItem import BuildItem

from game.scenes.Scene import Scene
from game.items.staticItems.Boundarie import Boundarie
from game.items.staticItems.SemicirlcleLine import SemicirlcleLine

from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


USE_CAMERA = True
DRAW_PYMUNK = False

def convert_opencv_to_pygame(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    new_shape = img.shape[1::-1]
    new_img = pygame.image.frombuffer(img.tobytes(), new_shape, "RGB")
    new_img = pygame.transform.flip(new_img, True, False)
    new_img = pygame.transform.scale(new_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return new_img

class Level(Scene):
    def __init__(self, app, lose_scene: Scene = None, win_scene: Scene = None, menu_scene: Scene = None):
        super().__init__(bg_color=(3, 224, 224))
        self.app = app
        self.lose_scene = lose_scene
        self.win_scene = win_scene
        self.menu_scene = menu_scene
        self.show_camera = self.app.show_camera
        if USE_CAMERA:
            self.hands = mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)
            self.cap = cv2.VideoCapture(0)
        self.screen = self.app.screen
        self.width = self.app.width
        self.height = self.app.height
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        self.frame_count = 0
        self.index_finger = None
        self.thumb_finger = None
        self.thread = None

        if DRAW_PYMUNK:
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)


    def process_frame(self, frame):
        pass
        # improve performance
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        # resize frame to improve performance
        frame = cv2.resize(frame, (640, 480))
        results = self.hands.process(frame)
        
        if not results.multi_hand_landmarks:
            self.index_finger = None
            self.thumb_finger = None
            return

        self.index_finger = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        self.thumb_finger = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP]





    def draw_frame(self):
        if self.index_finger is not None and self.thumb_finger is not None:
            #pygame.draw.circle(self.screen, (255, 255, 0), (-middle_finger.x * self.width + self.width, middle_finger.y * self.height), 10)
            pygame.draw.circle(self.screen, (255, 255, 0), (-self.index_finger.x * self.width + self.width, self.index_finger.y * self.height), 10)
            pygame.draw.circle(self.screen, (255, 255, 0), (-self.thumb_finger.x * self.width + self.width, self.thumb_finger.y * self.height), 10)

            # distance = math.sqrt((index_finger.x - thumb_finger.x) ** 2 + (index_finger.y - thumb_finger.y) ** 2 + (index_finger.z - thumb_finger.z) ** 2)
            # distance2 = math.sqrt((middle_finger.x - thumb_finger.x) ** 2 + (middle_finger.y - thumb_finger.y) ** 2 + (middle_finger.z - thumb_finger.z) ** 2)

    def pre_loads(self) -> None:
        semicircle = SemicirlcleLine(SCREEN_WIDTH/2, 400, 300, 200, 10, pymunk.Body.KINEMATIC)
        self.add_interactive_item(semicircle)
        self.thread = threading.Thread(target=self.worker)
        self.thread.start()


    def worker(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(self.capture())


        

    def add_static_item(self, item):
        super().add_static_item(item)
        self.space.add(item.body, item.shape)

    def add_dynamic_item(self, item):
        super().add_dynamic_item(item)
        self.space.add(item.body, item.shape)

    def add_interactive_item(self, item) -> None:
        super().add_interactive_item(item)
        self.space.add(*item.body, *item.shape)
    
    def update(self, pressed_keys: list) -> None:
        super().update(pressed_keys)
        if DRAW_PYMUNK:
            self.space.debug_draw(self.draw_options)
        if USE_CAMERA:
            self.draw_frame()
        #     # Capture a frame each 2 frames

        #     if self.frame_count % 3 == 0:
        #         ret, self.frame = self.cap.read()

        #     if self.frame is not None:
        #         self.process_frame(self.frame)
        #     self.frame_count += 1

        #move line
        # self.line_body.position = (self.line_body.position[0] + 1, self.line_body.position[1])
        # if self.line_body.position[0] > self.width:
        #     self.line_body.position = (0, 0)
        
            



        fps = self.app.clock.get_fps()
        if fps > 0:
            self.space.step(1 / fps)
            self.app.dt = 1 / fps


    async def capture(self):
        while self.app.is_running:
            if USE_CAMERA:
                # Capture a frame each 2 frames
                ret, self.frame = self.cap.read()
                if self.frame is not None:
                    self.process_frame(self.frame)

    def on_event(self, event: pygame.event) -> None:
        super().on_event(event)
        # check mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                self.add_dynamic_item(BuildItem(pos[0], pos[1], 50, 50))
        if event.type == pygame.QUIT:
            self.thread.join()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.thread.join()