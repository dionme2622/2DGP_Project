from pico2d import load_image

from tkinter import *
import select_mode
import play_mode

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
PI = 3.141592


class Skill:
    image = None

    def __init__(self, x, y):
        if Skill.image == None:
            Skill.image = load_image('./object/skill.png')
        self.x, self.y = x, y
        self.angle = 0.0

    def get_bb(self):
        pass

    def draw(self):
        self.image.clip_composite_draw(0, 0, 48, 59, self.angle, ' ', self.x, self.y, 48, 59)


    def update(self):
        for i in range(0, 10):
            if play_mode.player[i].getball == True:
                self.angle = (play_mode.player[i].angle + 45) * 2 * 3.14 / 180
        pass


    def handle_collision(self, group, other):
        pass
