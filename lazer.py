from pico2d import load_image, draw_rectangle

from tkinter import *

import game_framework
import game_world
import math
import select_mode
import play_mode

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
PI = 3.141592

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 25.0  # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

state = None


class Lazer:
    image = None

    def __init__(self, x, y, angle, frame, action, state):
        if Lazer.image == None:
            Lazer.image = load_image('./object/lazer.png')
        self.x, self.y = x, y
        self.angle = angle
        self.frame = frame
        self.action = action
        self.state = state

    def get_bb(self):
        if self.action == 2:
            return (self.x - 20, self.y, self.x + 20, self.y + 1000)
        elif self.action == 3:
            return (self.x, self.y - 20, self.x + 1000, self.y + 20)
        elif self.action == 4:
            return (self.x - 1000, self.y - 20, self.x, self.y + 20)
        elif self.action == 5:
            return (self.x - 20, self.y - 1000, self.x + 20, self.y)

    def draw(self):
        # draw_rectangle(*self.get_bb())
        self.image.clip_composite_draw(0, 0, 100, 100, self.angle, ' ', self.x, self.y, 2000, 400)

    def update(self):
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.frame > 5:
            game_world.remove_object(self)
        pass

    def handle_collision(self, group, other):
        pass
