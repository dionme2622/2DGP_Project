from math import tan

from pico2d import load_image

from tkinter import *

from mode import select_mode, game_framework

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('./object/ball41x41.png')
        self.x, self.y, self.velocity = x, y, velocity

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_bb())

    def update(self):

        angle1 = select_mode.player1.angle * 2 * 3.14 / 180
        angle2 = select_mode.player2.angle * 2 * 3.14 / 180

        if select_mode.player1.getball == True and select_mode.player2.getball == False:
            if select_mode.player1.shoot == True:
                self.x += self.velocity * 100 * game_framework.frame_time
                self.y += self.velocity * 100 * game_framework.frame_time * tan(angle1)
            elif select_mode.player1.shoot == False:
                self.velocity = select_mode.player1.attack_speed
                self.x = select_mode.player1.x + 80
                self.y = select_mode.player1.y

        elif select_mode.player1.getball == False and select_mode.player2.getball == True:
            if select_mode.player2.shoot == True:
                self.x += self.velocity * 100 * game_framework.frame_time
                self.y += self.velocity * 100 * game_framework.frame_time * -tan(angle2)
            elif select_mode.player2.shoot == False:
                self.velocity = -select_mode.player2.attack_speed
                self.x = select_mode.player2.x - 80
                self.y = select_mode.player2.y


        if self.x > WIDTH + 50:
            select_mode.player1.shoot = False
            select_mode.player1.getball = False
            select_mode.player2.getball = True

        if self.x < 0 - 50:
            select_mode.player2.shoot = False
            select_mode.player1.getball = True
            select_mode.player2.getball = False
    def handle_collision(self, group, other):
        if group == 'player1:ball':
            select_mode.player1.getball = True
            select_mode.player2.getball = False
            select_mode.player2.shoot = False
        elif group == 'player2:ball':
            select_mode.player1.getball = False
            select_mode.player2.getball = True
            select_mode.player1.shoot = False

        pass
