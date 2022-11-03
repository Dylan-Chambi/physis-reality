import mediapipe as mp
import cv2
import pygame
import math
import asyncio
import threading
import random
import pymunk
import pymunk.pygame_util

from utils.utils import get_assets_path, get_font

from game.items.dynamicItems.BuildItem import BuildItem
from game.items.dynamicItems.BuildItems.GemItem import GemItem
from game.items.dynamicItems.BuildItems.SemiTriangle import SemiTriangle

from game.scenes.Scene import Scene
from game.items.staticItems.Boundarie import Boundarie
from game.items.staticItems.Container import Container

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
        super().__init__(bg_color=(3, 224, 224), background_img=pygame.image.load(get_assets_path("assets/sprites/background.jpg")))
        self.app = app
        self.lose_scene = lose_scene
        self.win_scene = win_scene
        self.menu_scene = menu_scene
        self.show_camera = self.app.show_camera
        if USE_CAMERA:
            self.hands = mp_hands.Hands(
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)
            self.cap = cv2.VideoCapture(0)
        self.screen = self.app.screen
        self.width = self.app.width
        self.height = self.app.height
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        self.frame_count = 0
        self.right_fingers = []
        self.right_thumb_finger = None
        self.left_wrist = None
        self.left_middle_finger = None
        self.thread = None
        self.container = None

        if DRAW_PYMUNK:
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)


    def process_frame(self, frame):
        pass
        # improve performance
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = self.hands.process(frame)
        
        if not results.multi_hand_landmarks:
            self.right_fingers = []
            self.right_thumb_finger = None
            self.left_wrist = None
            self.left_middle_finger = None
            return

        index_finger1= results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_finger1 = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP]
        middle_finger1 = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_finger1 = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_finger1 = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.PINKY_TIP]
        wrist1 = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.WRIST]

        
        if len(results.multi_hand_landmarks) > 1:
            index_finger2 = results.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_finger2 = results.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_finger2 = results.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger2 = results.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_finger2 = results.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.PINKY_TIP]
            wrist2 = results.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.WRIST]

        
        if results.multi_handedness[0].classification[0].label == "Left":
            self.right_fingers = [index_finger1, middle_finger1, ring_finger1, pinky_finger1]
            self.right_thumb_finger = thumb_finger1
            self.left_wrist = None
            self.left_middle_finger = None

        if results.multi_handedness[0].classification[0].label == "Right":
            self.left_wrist = wrist1
            self.left_middle_finger = middle_finger1
            self.right_fingers = []
            self.right_thumb_finger = None

        if len(results.multi_hand_landmarks) > 1:
            if results.multi_handedness[1].classification[0].label == "Left":
                self.right_fingers = [index_finger2, middle_finger2, ring_finger2, pinky_finger2]
                self.right_thumb_finger = thumb_finger2

        if len(results.multi_hand_landmarks) > 1:
            if results.multi_handedness[1].classification[0].label == "Right":
                self.left_wrist = wrist2
                self.left_middle_finger = middle_finger2
        

    def draw_frame(self):
        if self.right_thumb_finger is not None and len(self.right_fingers) > 0:
            pygame.draw.circle(self.screen, (255, 255, 0), (-self.right_thumb_finger.x * self.width + self.width, self.right_thumb_finger.y * self.height), 10)
            center_point_x = self.right_fingers[0].x
            center_point_y = self.right_fingers[0].y
            for i in range(1, len(self.right_fingers)):
                center_point_x += self.right_fingers[i].x
                center_point_y += self.right_fingers[i].y
            center_point_x /= len(self.right_fingers)
            center_point_y /= len(self.right_fingers)
            pygame.draw.circle(self.screen, (255, 0, 0), (-center_point_x * self.width + self.width, center_point_y * self.height), 10)
    

        if self.left_wrist is not None and self.left_middle_finger is not None:
            # calculate angle
            angle = math.atan2(self.left_middle_finger.y - self.left_wrist.y, self.left_middle_finger.x - self.left_wrist.x)
            angle = math.degrees(angle)
            # angle_threshold = 20
            if angle > 0:
                angle = angle - 180
            elif angle < 0:
                angle = angle + 180
            self.container.angle = angle

            # pygame.draw.line(self.screen, (255, 255, 0), (-self.left_wrist.x * self.width + self.width, self.left_wrist.y * self.height), (-self.left_middle_finger.x * self.width + self.width, self.left_middle_finger.y * self.height), 5)
            # distance = math.sqrt((index_finger.x - thumb_finger.x) ** 2 + (index_finger.y - thumb_finger.y) ** 2 + (index_finger.z - thumb_finger.z) ** 2)
            # distance2 = math.sqrt((middle_finger.x - thumb_finger.x) ** 2 + (middle_finger.y - thumb_finger.y) ** 2 + (middle_finger.z - thumb_finger.z) ** 2)

    def pre_loads(self) -> None:
        # Boundaries
        self.add_static_item(Boundarie(SCREEN_WIDTH/2, 25, SCREEN_WIDTH, 50))
        # self.add_static_item(Boundarie(SCREEN_WIDTH/2, SCREEN_HEIGHT, SCREEN_WIDTH, 50))
        self.add_static_item(Boundarie(25, SCREEN_HEIGHT/2, 50, SCREEN_HEIGHT))
        self.add_static_item(Boundarie(SCREEN_WIDTH - 25, SCREEN_HEIGHT/2, 50, SCREEN_HEIGHT))


        self.container = Container(SCREEN_WIDTH/2, SCREEN_HEIGHT - 200, SCREEN_WIDTH/2, 100, pymunk.Body.KINEMATIC)
        self.add_interactive_item(self.container)

        if USE_CAMERA:
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

    def get_random_item(self, x, y):
        switch = random.randint(0, 1)
        min_size = 30
        max_size = 50
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        random_width = random.randint(min_size, max_size)
        random_height = random.randint(min_size, max_size)
        if switch == 0:
            return GemItem(x, y, random_width, random_height, random_color)
        elif switch == 1:
            return SemiTriangle(x, y, random_width, random_height, random_color)

    def draw_interface(self):

        self.screen.blit(get_font(30).render("Score: " , True, (255, 255, 255)), (10, 10))
        self.screen.blit(get_font(30).render("Lives: " , True, (255, 255, 255)), (10, 50))
        self.screen.blit(get_font(30).render("Level: " , True, (255, 255, 255)), (10, 90))
        self.screen.blit(get_font(30).render("Time: " , True, (255, 255, 255)), (10, 130))
    
    def update(self, pressed_keys: list) -> None:
        super().update(pressed_keys)

        # draw pick item box
        pygame.draw.rect(self.screen, (13, 129, 133), (SCREEN_WIDTH/2 - 200, 0, 400, 200))
        pygame.draw.rect(self.screen, (255, 255, 255), (SCREEN_WIDTH/2 - 200, 0, 400, 200), 5)
        
        for item in self.item_list:
            item.draw_in_screen()
            item.update(pressed_keys, self, self.app.dt)
    
        if DRAW_PYMUNK:
            self.space.debug_draw(self.draw_options)
        if USE_CAMERA:
            self.draw_frame()

        self.draw_interface()
        fps = self.app.clock.get_fps()
        if fps > 0:
            self.space.step(1 / fps)
            self.app.dt = 1 / fps


    async def capture(self):
        while self.app.is_running:
            ret, self.frame = self.cap.read()
            if self.frame is not None:
                self.process_frame(self.frame)

    def on_event(self, event: pygame.event) -> None:
        super().on_event(event)
        # check mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                self.add_dynamic_item(self.get_random_item(pos[0], pos[1]))
        if event.type == pygame.QUIT:
            self.thread.join()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.thread.join()