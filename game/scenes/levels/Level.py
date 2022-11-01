import mediapipe as mp
import cv2
import pygame
import math
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


USE_CAMERA = False

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
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)
            self.cap = cv2.VideoCapture(0)
        self.screen = self.app.screen
        self.width = self.app.width
        self.height = self.app.height
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)


        # self.line_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        # self.line_shape = pymunk.Segment(self.line_body, (0, 0), (500, 500), 5)
        # self.line_shape.elasticity = 0.95
        # self.line_shape.friction = 0.9
        # self.space.add(self.line_body, self.line_shape)


    def process_frame(self, frame):
        # improve performance
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = self.hands.process(frame)
        if not results.multi_hand_landmarks:
            if self.show_camera:
                self.screen.blit(convert_opencv_to_pygame(frame), (0, 0))
            return
        # out = frame.copy()


        # for hand_landmarks in results.multi_hand_landmarks:
        #     mp_drawing.draw_landmarks(
        #         out,
        #         hand_landmarks,
        #         mp_hands.HAND_CONNECTIONS,
        #         mp_drawing_styles.get_default_hand_landmarks_style(),
        #         mp_drawing_styles.get_default_hand_connections_style()
        #     )

        middle_finger = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        index_finger = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_finger = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP]

        # if self.show_camera:
        #     self.screen.blit(convert_opencv_to_pygame(out), (0, 0))

        pygame.draw.circle(self.screen, (255, 255, 0), (-middle_finger.x * self.width + self.width, middle_finger.y * self.height), 10)
        pygame.draw.circle(self.screen, (255, 0, 0), (-index_finger.x * self.width + self.width, index_finger.y * self.height), 10)
        pygame.draw.circle(self.screen, (0, 255, 0), (-thumb_finger.x * self.width + self.width, thumb_finger.y * self.height), 10)

        # distance = math.sqrt((index_finger.x - thumb_finger.x) ** 2 + (index_finger.y - thumb_finger.y) ** 2 + (index_finger.z - thumb_finger.z) ** 2)
        # distance2 = math.sqrt((middle_finger.x - thumb_finger.x) ** 2 + (middle_finger.y - thumb_finger.y) ** 2 + (middle_finger.z - thumb_finger.z) ** 2)

    def pre_loads(self) -> None:
        semicircle = SemicirlcleLine(500, 500, 50, 5, pymunk.Body.STATIC)
        self.space.add(semicircle.body, semicircle.shape)
        pass
        

    def add_static_item(self, item):
        super().add_static_item(item)
        self.space.add(item.body, item.shape)

    def add_dynamic_item(self, item):
        super().add_dynamic_item(item)
        self.space.add(item.body, item.shape)

    def update(self, pressed_keys: list) -> None:
        super().update(pressed_keys)
        self.space.debug_draw(self.draw_options)
        if USE_CAMERA:
            ret, frame = self.cap.read()
            self.process_frame(frame)

        #move line
        # self.line_body.position = (self.line_body.position[0] + 1, self.line_body.position[1])
        # if self.line_body.position[0] > self.width:
        #     self.line_body.position = (0, 0)
        
            



        fps = self.app.clock.get_fps()
        if fps > 0:
            self.space.step(1 / fps)
        

    def on_event(self, event: pygame.event) -> None:
        super().on_event(event)
        # check mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                self.add_dynamic_item(BuildItem(pos[0], pos[1], 50, 50))