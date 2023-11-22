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
        self.shoot = False
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


        if self.shoot == True:
            if self.state == 'Blueteam_get':
                self.x += self.velocity * 100 * game_framework.frame_time
                self.y += self.velocity * 100 * game_framework.frame_time * tan(self.angle1)
            elif self.state == 'Redteam_get':
                self.x -= self.velocity * 100 * game_framework.frame_time
                self.y -= self.velocity * 100 * game_framework.frame_time * -tan(self.angle2)

        # for i in range(0, 5):
        #     if play_mode.player[i].shoot == True:
        #         self.x += self.velocity * 100 * game_framework.frame_time
        #         self.y += self.velocity * 100 * game_framework.frame_time * tan(self.angle1)
        # for i in range(5, 10):
        #     if play_mode.player[i].shoot == True:
        #         self.x -= self.velocity * 100 * game_framework.frame_time
        #         self.y -= self.velocity * 100 * game_framework.frame_time * -tan(self.angle2)

        if self.x > WIDTH + 50:
            self.state = 'floor'
            self.x = WIDTH * 3 // 4
            self.y = 400
            for i in range(0, 10):
                play_mode.player[i].shoot = False
        if self.x < 0 - 50:
            self.state = 'floor'
            self.x = WIDTH // 1 // 4
            self.y = 400
            for i in range(0, 10):
                play_mode.player[i].shoot = False
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
