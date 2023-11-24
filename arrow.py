from pico2d import load_image

from tkinter import *
import select_mode
import play_mode

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
PI = 3.141592


class Arrow:
    image = None

    def __init__(self):
        if Arrow.image == None:
            Arrow.image = load_image('./object/arrow.png')
            self.x, self.y = 0, 0
            self.angle1, self.angle2 = 0, 0

    def get_bb(self):
        pass

    def draw(self):
        for i in range(0, 5):
            if play_mode.player[i].getball == True:
                self.image.clip_composite_draw(0, 0, 100, 100, self.angle1, ' ', self.x, self.y, 100, 100)
        for i in range(5, 10):
            if play_mode.player[i].getball == True:
                self.image.clip_composite_draw(0, 0, 100, 100, self.angle2, ' ', self.x, self.y, 100, 100)

    def update(self):
        global angle1, angle2
        for i in range(0, 5):
            if play_mode.player[i].getball == True:
                self.angle1 = play_mode.player[i].angle * 2 * 3.14 / 180
                if play_mode.player[i].action == 2:
                    self.x = play_mode.player[i].x
                    self.y = play_mode.player[i].y + 100
                elif play_mode.player[i].action == 3:
                    self.x = play_mode.player[i].x + 100
                    self.y = play_mode.player[i].y
                elif play_mode.player[i].action == 4:
                    self.x = play_mode.player[i].x - 100
                    self.y = play_mode.player[i].y
                elif play_mode.player[i].action == 5:
                    self.x = play_mode.player[i].x
                    self.y = play_mode.player[i].y - 100
        for i in range(5, 10):
            if play_mode.player[i].getball == True:
                self.angle2 = play_mode.player[i].angle * 2 * 3.14 / 180
                if play_mode.player[i].action == 2:
                    self.x = play_mode.player[i].x
                    self.y = play_mode.player[i].y + 100
                elif play_mode.player[i].action == 3:
                    self.x = play_mode.player[i].x + 100
                    self.y = play_mode.player[i].y
                elif play_mode.player[i].action == 4:
                    self.x = play_mode.player[i].x - 100
                    self.y = play_mode.player[i].y
                elif play_mode.player[i].action == 5:
                    self.x = play_mode.player[i].x
                    self.y = play_mode.player[i].y - 100

    def handle_collision(self, group, other):
        pass
