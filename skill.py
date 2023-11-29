from pico2d import load_image

from tkinter import *

import game_framework
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
FRAMES_PER_ACTION = 4

class Skill:
    image = None

    def __init__(self, x, y):
        if Skill.image == None:
            Skill.image = load_image('./object/skill.png')
        self.x, self.y = x, y
        self.angle = 0.0
        self.frame = 0.0
    def get_bb(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(int(self.frame) * 48, 0, 48, 59, self.angle, ' ', self.x, self.y, 48, 59)


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        for i in range(0, 10):
            if play_mode.player[i].getball == True:
                self.angle = (play_mode.player[i].angle + 45) * 2 * 3.14 / 180
        pass


    def handle_collision(self, group, other):
        pass
