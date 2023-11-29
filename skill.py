import math

from pico2d import load_image

from tkinter import *

import game_framework
import game_world
import select_mode
import play_mode
from lazer import Lazer

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
FRAMES_PER_ACTION = 2

class Skill:
    image = None

    def __init__(self, x, y, action):
        if Skill.image == None:
            Skill.image = load_image('./object/skill.png')
        self.x, self.y = x, y
        self.action = action
        if self.action == 2:
            self.angle = math.radians(180)
        elif self.action == 3:
            self.angle = math.radians(90)
        elif self.action == 4:
            self.angle = math.radians(270)
        elif self.action == 5:
            self.angle = math.radians(0)
        self.frame = 0.0
        self.radian = 0.0
    def get_bb(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(int(self.frame) * 48, 0, 48, 59, self.angle + math.radians(self.radian), ' ', self.x, self.y, 100, 100)


    def update(self):
        global lazer
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.frame > 3:
            lazer = Lazer(self.x, self.y, self.angle - PI / 2, self.frame, self.action)
            game_world.add_object(lazer, 1)
            game_world.add_collision_pair("player:lazer", None, lazer)
        if self.frame > 5:
            game_world.remove_object(self)
        if self.radian < 360:
            self.radian += 20

        pass


    def handle_collision(self, group, other):
        pass
