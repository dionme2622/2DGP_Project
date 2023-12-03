from pico2d import load_image, load_music
from tkinter import *

import select_mode

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


class Background:

    def __init__(self):
        self.image = load_image('./object/GROUND.png')
        self.bgm = load_music('./bgm/mus_zz_megalovania.mp3')
        self.bgm.repeat_play()

    def draw(self):
        self.image.clip_draw(0, 0, WIDTH, HEIGHT, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    def update(self):
        self.bgm.set_volume(select_mode.volume)

        pass

class Heart:
    def __init__(self):
        self.image = load_image('./character/heart.png')

    def draw(self):
        self.image.clip_draw(0, 16, 16, 16, 750, 930, 32, 32)
        self.image.clip_draw(16, 16, 16, 16, 1250, 930, 32, 32)

    def update(self):
        pass

class Icon:
    def __init__(self):
        self.image = load_image('./object/skill_icon.png')

    def draw(self):
        self.image.clip_draw(0, 0, 45, 45, 400, 930, 90, 90)
        self.image.clip_draw(0, 0, 45, 45, 1580, 930, 90, 90)

    def update(self):
        pass