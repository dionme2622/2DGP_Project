import math
from math import tan
import random

from pico2d import load_image, draw_rectangle

from tkinter import *

import blueteam
import play_mode, game_framework
import redteam

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


class Ball:
    image = None

    def __init__(self, velocity=7):
        if Ball.image == None:
            Ball.image = load_image('./object/ball.png')
        self.spawn = 0 #random.randint(0,1)
        if self.spawn == 0:
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
        self.player_getball()
        self.angle1 = play_mode.arrow.angle1
        self.angle2 = play_mode.arrow.angle2
        self.shoot_ball()
        self.ball_out()

        pass

    def player_getball(self):
        for i in range(0, 10):
            if play_mode.player[i].getball == True:
                if play_mode.player[i].action == 2:
                    self.x = play_mode.player[i].x
                    self.y = play_mode.player[i].y + 80
                elif play_mode.player[i].action == 3:
                    self.x = play_mode.player[i].x + 80
                    self.y = play_mode.player[i].y
                elif play_mode.player[i].action == 4:
                    self.x = play_mode.player[i].x - 80
                    self.y = play_mode.player[i].y
                elif play_mode.player[i].action == 5:
                    self.x = play_mode.player[i].x
                    self.y = play_mode.player[i].y - 80

    def ball_out(self):
        if blueteam.survivor == 5:
            if self.x > WIDTH + 50 or (self.x > WIDTH // 2 and (self.y > HEIGHT + 150 or self.y < -150)):
                self.state = 'floor'
                self.x = WIDTH * 3 // 4
                self.y = 400
                for i in range(0, 5):
                    play_mode.player[i].shoot = False
        else:
            if self.x > WIDTH + 50:
                self.state = 'floor'
                self.x = WIDTH - 180
                self.y = 400
                for i in range(0, 5):
                    play_mode.player[i].shoot = False
            elif self.x > WIDTH // 2 and self.y > HEIGHT + 150:
                self.state = 'floor'
                self.x = WIDTH // 2 + 200
                self.y = 790
                for i in range(0, 5):
                    play_mode.player[i].shoot = False
            elif self.x > WIDTH // 2 and self.y < -150:
                self.state = 'floor'
                self.x = WIDTH // 2 + 200
                self.y = 70
                for i in range(0, 5):
                    play_mode.player[i].shoot = False
        if redteam.survivor == 5:
            if self.x < -50 or (self.x < WIDTH // 2 and (self.y > HEIGHT + 150 or self.y < -150)):
                self.state = 'floor'
                self.x = WIDTH * 1 // 4
                self.y = 400
                for i in range(5, 10):
                    play_mode.player[i].shoot = False
        else:
            if self.x < -50:
                self.state = 'floor'
                self.x = 200
                self.y = 400
                for i in range(5, 10):
                    play_mode.player[i].shoot = False
            elif self.x < WIDTH // 2 and self.y > HEIGHT + 150:
                self.state = 'floor'
                self.x = WIDTH // 2 - 200
                self.y = 790
                for i in range(5, 10):
                    play_mode.player[i].shoot = False
            elif self.x < WIDTH // 2 and self.y < -150:
                self.state = 'floor'
                self.x = WIDTH // 2 - 200
                self.y = 70
                for i in range(5, 10):
                    play_mode.player[i].shoot = False

    def shoot_ball(self):
        if self.shoot == True:
            if self.state == 'Blueteam_get':
                self.x += self.velocity * 100 * game_framework.frame_time * math.cos(self.angle1)
                self.y += self.velocity * 100 * game_framework.frame_time * math.sin(self.angle1)
            elif self.state == 'Redteam_get':
                self.x += self.velocity * 100 * game_framework.frame_time * math.cos(self.angle2)
                self.y += self.velocity * 100 * game_framework.frame_time * math.sin(self.angle2)

    def handle_collision(self, group, other):
        pass
