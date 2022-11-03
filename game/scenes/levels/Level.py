import mediapipe as mp
import cv2
import pygame
import math
import asyncio
import threading
import random
import pymunk
import time
import pymunk.pygame_util


from game.items.dynamicItems.BuildItems.GemItem import GemItem
from game.items.dynamicItems.BuildItems.SemiTriangle import SemiTriangle


from game.items.staticItems.Boundarie import Boundarie
from game.items.staticItems.Container import Container
from game.items.staticItems.Goal import Goal

from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SPAWN_ITEM, GRAB, DROP, COUNT_ONE_SECOND, ITEM_FALLED, GOAL_Y, ITEM_IN_GOAL, ITEM_IN_GOAL_TIME_COUNT
from game.scenes.Scene import Scene
from utils.utils import get_assets_path, get_font

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles



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

        if self.app.use_camera:
            self.cap = self.app.cap
            self.hands = mp_hands.Hands(
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)

        self.screen = self.app.screen
        self.width = self.app.width
        self.height = self.app.height
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        self.spawn_position = (SCREEN_WIDTH/2 - 200, 50)
        self.right_fingers = []
        self.right_thumb_finger = None
        self.rigth_wrist = None
        self.left_wrist = None
        self.left_middle_finger = None
        self.thread = None
        self.container = None
        self.spawn_item = None
        self.grab_item = None
        self.goal = None
        self.hand_img = pygame.image.load(get_assets_path("assets/sprites/hand_grab.png"))
        self.hand_img = pygame.transform.scale(self.hand_img, (50, 50))
        self.hand_img.set_colorkey((255, 255, 255, 0))
        self.hand_grabbing_img = pygame.image.load(get_assets_path("assets/sprites/hand_grabbing.png"))
        self.hand_grabbing_img = pygame.transform.scale(self.hand_grabbing_img, (50, 50))
        self.hand_grabbing_img.set_colorkey((255, 255, 255, 0))
        self.hand_position = None
        self.hand_angle = 0
        self.is_grabbing = False
        self.time = 200
        self.lives = 10
        self.camera_fps = 0
        self.counting = False
        self.is_running_current_scene = False

        if DRAW_PYMUNK:
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)


    def process_frame(self, frame):
        # improve performance
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = self.hands.process(frame)
        
        if not results.multi_hand_landmarks:
            self.right_fingers = []
            self.right_thumb_finger = None
            self.rigth_wrist = None
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
            self.rigth_wrist = wrist1
            self.left_wrist = None
            self.left_middle_finger = None

        if results.multi_handedness[0].classification[0].label == "Right":
            self.left_wrist = wrist1
            self.left_middle_finger = middle_finger1
            self.right_fingers = []
            self.right_thumb_finger = None
            self.rigth_wrist = None

        if len(results.multi_hand_landmarks) > 1:
            if results.multi_handedness[1].classification[0].label == "Left":
                self.right_fingers = [index_finger2, middle_finger2, ring_finger2, pinky_finger2]
                self.right_thumb_finger = thumb_finger2
                self.rigth_wrist = wrist2

        if len(results.multi_hand_landmarks) > 1:
            if results.multi_handedness[1].classification[0].label == "Right":
                self.left_wrist = wrist2
                self.left_middle_finger = middle_finger2
        

    def draw_frame(self):
        if self.right_thumb_finger is not None and self.rigth_wrist is not None and len(self.right_fingers) > 0:
            center_point_x = self.right_fingers[0].x
            center_point_y = self.right_fingers[0].y
            center_point_z = self.right_fingers[0].z
            for i in range(1, len(self.right_fingers)):
                center_point_x += self.right_fingers[i].x
                center_point_y += self.right_fingers[i].y
                center_point_z += self.right_fingers[i].z
            center_point_x /= len(self.right_fingers)
            center_point_y /= len(self.right_fingers)
            center_point_z /= len(self.right_fingers)

            center_center_point_x = (center_point_x + self.right_thumb_finger.x) / 2
            center_center_point_y = (center_point_y + self.right_thumb_finger.y) / 2
            center_center_point_z = (center_point_z + self.right_thumb_finger.z) / 2


            self.hand_position = (center_center_point_x, center_center_point_y)

            distance = math.sqrt((center_point_x - self.right_thumb_finger.x) ** 2 + (center_point_y - self.right_thumb_finger.y) ** 2)
            
            # calculate distance relative to z axis
            self.is_grabbing = distance + center_center_point_z + self.right_thumb_finger.z < 0.01
            # self.is_grabbing = distance < 0.1

            self.hand_angle = math.atan2(self.rigth_wrist.y - center_point_y, self.rigth_wrist.x - center_point_x)
            self.hand_angle += math.radians(-90)
        else:
            self.hand_position = None
            self.hand_angle = None
            self.is_grabbing = False

    

        if self.left_wrist is not None and self.left_middle_finger is not None:
            angle = math.atan2(self.left_middle_finger.y - self.left_wrist.y, self.left_middle_finger.x - self.left_wrist.x)
            angle = math.degrees(angle)
            if angle > 0:
                angle = angle - 180
            elif angle < 0:
                angle = angle + 180
            self.container.angle = angle
        else:
            self.container.angle = 0


    def pre_loads(self) -> None:
        self.is_running_current_scene = True
        # Boundaries
        self.add_static_item(Boundarie(SCREEN_WIDTH/2, 25, SCREEN_WIDTH, 50))
        # self.add_static_item(Boundarie(SCREEN_WIDTH/2, SCREEN_HEIGHT, SCREEN_WIDTH, 50))
        self.add_static_item(Boundarie(25, SCREEN_HEIGHT/2, 50, SCREEN_HEIGHT))
        self.add_static_item(Boundarie(SCREEN_WIDTH - 25, SCREEN_HEIGHT/2, 50, SCREEN_HEIGHT))

        #Goal
        self.goal = Goal(GOAL_Y, 10)
        self.add_static_item(self.goal)


        self.container = Container(SCREEN_WIDTH/2, SCREEN_HEIGHT - 200, SCREEN_WIDTH/2, 100, pymunk.Body.KINEMATIC)
        self.add_interactive_item(self.container)

        pygame.event.post(pygame.event.Event(SPAWN_ITEM))

        if self.app.use_camera:
            self.thread = threading.Thread(target=self.worker)
            self.thread.start()

        pygame.time.set_timer(COUNT_ONE_SECOND, 1000)


    def worker(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(self.capture())

    async def capture(self):
        while self.is_running_current_scene:
            start_time = time.time()
            _, self.frame = self.cap.read()
            if self.frame is not None:
                self.process_frame(self.frame)
            end_time = time.time()
            self.camera_fps = 1 / (end_time - start_time)

            

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
        min_size = 50
        max_size = 80
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        random_width = random.randint(min_size, max_size)
        random_height = random.randint(min_size, max_size)
        if switch == 0:
            return GemItem(x, y, random_width, random_height, random_color)
        elif switch == 1:
            return SemiTriangle(x, y, random_width, random_height, random_color)

    def draw_interface(self):
        self.screen.blit(get_font(30).render("Lives: " + str(self.lives), True, (255, 255, 255)), (10, 10))
        self.screen.blit(get_font(30).render("Time: " + str(int(self.time)), True, (255, 255, 255)), (10, 50))
        # self.screen.blit(get_font(30).render("Time to win" + str(int(self.goal.time_to_win)), True, (255, 255, 255)), (10, 90))
        self.screen.blit(get_font(30).render("Camera FPS: " + str(int(self.camera_fps)), True, (255, 255, 255)), (SCREEN_WIDTH - 440, 10))
        self.screen.blit(get_font(30).render("FPS: " + str(int(self.app.clock.get_fps())), True, (255, 255, 255)), (SCREEN_WIDTH - 270, 50))

        # Draw in center of screen
        if self.counting:
            self.screen.blit(get_font(50).render("Hold on!!! " + str(self.goal.time_to_win) + "...", True, (122, 84, 13)), (SCREEN_WIDTH/2-310, SCREEN_HEIGHT/2-100))

    def draw_hand(self):
        if self.hand_position is not None and self.hand_angle is not None:
            img_rotated = None
            if self.is_grabbing:
                img_rotated = pygame.transform.rotate(self.hand_grabbing_img, math.degrees(self.hand_angle))
                pygame.event.post(pygame.event.Event(GRAB))
            else:
                img_rotated = pygame.transform.rotate(self.hand_img, math.degrees(self.hand_angle))
                pygame.event.post(pygame.event.Event(DROP))
            self.screen.blit(img_rotated, (-self.hand_position[0] * SCREEN_WIDTH + SCREEN_WIDTH - img_rotated.get_width()/2, self.hand_position[1] * SCREEN_HEIGHT - img_rotated.get_height()/2))
        else:
            pygame.event.post(pygame.event.Event(DROP))
    
    def update(self, pressed_keys: list) -> None:
        super().update(pressed_keys)

        # draw pick item box
        pygame.draw.rect(self.screen, (13, 129, 133), (self.spawn_position[0], self.spawn_position[1], 400, 200))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.spawn_position[0], self.spawn_position[1], 400, 200), 10)
        
        for item in self.item_list:
            item.draw_in_screen()
            item.update(pressed_keys, self, self.app.dt)
    
        if DRAW_PYMUNK:
            self.space.debug_draw(self.draw_options)
        if self.app.use_camera:
            self.draw_frame()
            self.draw_hand()

        self.control_object()
        self.draw_interface()
        fps = self.app.clock.get_fps()
        if fps > 0:
            self.space.step(1 / fps)
            self.app.dt = 1 / fps

    def control_object(self):
        if self.grab_item is not None and self.hand_position is not None:
            self.grab_item.body.position = (-self.hand_position[0] * SCREEN_WIDTH + SCREEN_WIDTH, self.hand_position[1] * SCREEN_HEIGHT)
            self.grab_item.body.angle = -self.hand_angle
            self.grab_item.shape.filter = pymunk.ShapeFilter(categories=1, mask=1)
            self.grab_item.body.velocity_func = lambda body, gravity, damping, dt: pymunk.Body.update_velocity(body, (0, 0), damping, dt)


    def on_event(self, event: pygame.event) -> None:
        super().on_event(event)
        # check mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                self.add_dynamic_item(self.get_random_item(pos[0], pos[1]))
        if event.type == pygame.QUIT:
            self.is_running_current_scene = False
            if self.app.use_camera:
                self.cap.release()
                cv2.destroyAllWindows()
                self.thread.join()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_unload()
                self.app.change_scene(self.menu_scene)
                if self.app.use_camera:
                    self.thread.join()
        if event.type == SPAWN_ITEM:
            self.spawn_item = self.get_random_item(self.spawn_position[0] + 200, self.spawn_position[1] + 100)
            self.spawn_item.shape.filter = pymunk.ShapeFilter(categories=100, mask=100)
            self.spawn_item.body.velocity_func = lambda body, gravity, damping, dt: (0, 0)
            self.add_dynamic_item(self.spawn_item)
        if event.type == GRAB:
            if self.is_grabbing and self.grab_item is None:
                for item in self.item_list:
                    if not isinstance(item, Container):
                        dist = item.shape.point_query((-self.hand_position[0] * SCREEN_WIDTH + SCREEN_WIDTH, self.hand_position[1] * SCREEN_HEIGHT))
                        if dist.distance < 0.1:
                            self.grab_item = item
                            if item == self.spawn_item:
                                pygame.time.set_timer(SPAWN_ITEM, 2000, 1)
        if event.type == DROP:
            if self.grab_item is not None:
                self.grab_item.body.velocity_func = lambda body, gravity, damping, dt: pymunk.Body.update_velocity(body, gravity, damping, dt)
                self.grab_item = None
        if event.type == COUNT_ONE_SECOND:
            self.time -= 1
            if self.time <= 0:
                self.on_unload()
                self.app.change_scene(self.lose_scene)
            if self.counting:
                pygame.event.post(pygame.event.Event(ITEM_IN_GOAL_TIME_COUNT))
        if event.type == ITEM_FALLED:
            self.lives -= 1
            self.item_list.remove(event.item)
            if self.lives <= 0:
                self.on_unload()
                self.app.change_scene(self.lose_scene)
        if event.type == ITEM_IN_GOAL:
            if not (event.item == self.spawn_item or event.item == self.grab_item):
                # print velocity
                if event.item.body.velocity.length < 3:
                    self.goal.bg_color = (0, 255, 0)
                    if not self.counting:
                        self.counting = True
                else:
                    self.goal.bg_color = (255, 0, 0)
                    self.counting = False
                    self.goal.time_to_win = 3
        if event.type == ITEM_IN_GOAL_TIME_COUNT:
            self.goal.time_to_win -= 1
            if self.goal.time_to_win <= -1:
                self.on_unload()
                self.app.change_scene(self.win_scene)

    def on_unload(self) -> None:
        super().on_unload()
        self.is_running_current_scene = False
        self.thread.join()
        for item in self.space.shapes:
            self.space.remove(item)
        self.spawn_item = None
        self.grab_item = None
        self.hand_position = None
        self.hand_angle = None
        self.is_grabbing = False
        self.counting = False
        self.time = 200
        self.lives = 10