from math import tan
import random

from pico2d import load_image, draw_rectangle

from tkinter import *

import play_mode, game_framework

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


class Ball:
    image = None

    def __init__(self, velocity = 5):
        if Ball.image == None:
            Ball.image = load_image('./object/ball.png')
        spawn = random.randint(0,1)
        if spawn == 0:
            self.x = WIDTH // 2 - 100
        else:
            self.x = WIDTH // 2 + 100
        self.y, self.velocity = HEIGHT // 2 - 100, velocity
        self.state = 'floor'
        self.angle1, self.angle2 = 0, 0
    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        for i in range(0, 5):
            if play_mode.player[i].getball == True:
                self.x = play_mode.player[i].x + 80
                self.y = play_mode.player[i].y
        for i in range(5, 10):
            if play_mode.player[i].getball == True:
                self.x = play_mode.player[i].x - 80
                self.y = play_mode.player[i].y

        self.angle1 = play_mode.arrow.angle1
        self.angle2 = play_mode.arrow.angle2

        for i in range(0, 5):
            if play_mode.player[i].shoot == True:
                self.x += self.velocity * 100 * game_framework.frame_time
                self.y += self.velocity * 100 * game_framework.frame_time * tan(self.angle1)
        for i in range(5, 10):
            if play_mode.player[i].shoot == True:
                self.x += self.velocity * 100 * game_framework.frame_time
                self.y += self.velocity * 100 * game_framework.frame_time * -tan(self.angle2)
                #         self.y += self.velocity * 100 * game_framework.frame_time * -tan(self.angle2)
        # if play_mode.player1.getball == True and play_mode.player2.getball == False:
        #     if play_mode.player1.shoot == True:
        #         self.x += self.velocity * 100 * game_framework.frame_time
        #         self.y += self.velocity * 100 * game_framework.frame_time * tan(self.angle1)
        #     elif play_mode.player1.shoot == False:
        #         self.velocity = play_mode.player1.attack_speed
        #         self.x = play_mode.player1.x + 80
        #         self.y = play_mode.player1.y

        # elif play_mode.player1.getball == False and play_mode.player2.getball == True:
        #     if play_mode.player2.shoot == True:
        #         self.x += self.velocity * 100 * game_framework.frame_time
        #         self.y += self.velocity * 100 * game_framework.frame_time * -tan(self.angle2)
        #     elif play_mode.player2.shoot == False:
        #         self.velocity = -play_mode.player2.attack_speed
        #         self.x = play_mode.player2.x - 80
        #         self.y = play_mode.player2.y
    #
    #
    #     if self.x > WIDTH + 50:
    #         play_mode.player1.shoot = False
    #         play_mode.player1.getball = False
    #         play_mode.player2.getball = True
    #
    #     if self.x < 0 - 50:
    #         play_mode.player2.shoot = False
    #         play_mode.player1.getball = True
    #         play_mode.player2.getball = False
        pass
    def handle_collision(self, group, other):
    #     if group == 'player1:ball':
    #         play_mode.player1.getball = True
    #         play_mode.player2.getball = False
    #         play_mode.player2.shoot = False
    #     elif group == 'player2:ball':
    #         play_mode.player1.getball = False
    #         play_mode.player2.getball = True
    #         play_mode.player1.shoot = False

        pass
