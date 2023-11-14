from math import tan

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import play_mode
from tkinter import *

import select_mode

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


class Arrow:
    image = None

    def __init__(self):
        if Arrow.image == None:
            Arrow.image = load_image('./object/Arrow.png')
            self.x, self.y = 0, 0

    def get_bb(self):
        pass

    def draw(self):
        if select_mode.player1.getball == True and select_mode.player1.shoot == False:
            self.image.clip_composite_draw(0, 0, 300, 160, angle1, ' ', self.x, self.y, 300, 120)
        elif select_mode.player2.getball == True and select_mode.player2.shoot == False:
            self.image.clip_composite_draw(0, 0, 300, 160, -angle2, 'h', self.x, self.y, 300, 120)
    def update(self):
        global angle1, angle2
        angle1 = select_mode.player1.angle * 2 * 3.14 / 180
        angle2 = select_mode.player2.angle * 2 * 3.14 / 180

        if select_mode.player1.getball == True and select_mode.player2.getball == False:
            if select_mode.player1.shoot == False:
                self.x = select_mode.player1.x + 100
                self.y = select_mode.player1.y

        elif select_mode.player1.getball == False and select_mode.player2.getball == True:
            if select_mode.player2.shoot == False:
                self.velocity = -select_mode.player2.attack_speed
                self.x = select_mode.player2.x - 100
                self.y = select_mode.player2.y



    def handle_collision(self, group, other):
        pass
