from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import play_mode
from tkinter import *

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
        draw_rectangle(*self.get_bb())

    def update(self):


        if play_mode.player1.getball == True and play_mode.player2.getball == False:
            self.velocity = play_mode.player1.attack_speed
            self.x = play_mode.player1.x + 80
            self.y = play_mode.player1.y
        elif play_mode.player1.getball == False and play_mode.player2.getball == False:
            self.x += self.velocity * 100 * game_framework.frame_time

        elif play_mode.player1.getball == False and play_mode.player2.getball == True:
            self.velocity = -play_mode.player2.attack_speed

            self.x = play_mode.player2.x - 80
            self.y = play_mode.player2.y
        elif play_mode.player1.getball == False and play_mode.player2.getball == False:
            self.x += self.velocity * 100 * game_framework.frame_time

        if self.x > WIDTH + 50:
            play_mode.player2.getball = True

        if self.x < 0 - 50 :
            play_mode.player1.getball = True

    def handle_collision(self, group, other):
        pass

