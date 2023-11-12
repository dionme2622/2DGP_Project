from pico2d import load_image

import game_framework
import game_world
import play_mode


class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball41x41.png')
        self.x, self.y, self.velocity = x, y, velocity

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):

        if play_mode.player1.getball == True:
            self.velocity = play_mode.player1.attack_speed
            self.x = play_mode.player1.x + 60
            self.y = play_mode.player1.y
        else:
            self.x += self.velocity * 100 * game_framework.frame_time

        if play_mode.player2.getball == True:
            self.velocity = -play_mode.player2.attack_speed

            self.x = play_mode.player2.x - 50
            self.y = play_mode.player2.y
        else:
            self.x += self.velocity * 100 * game_framework.frame_time

        if self.x > 1400:
            play_mode.player2.getball = True

        if self.x < -120 :
            play_mode.player1.getball = True

    def handle_collision(self, group, other):
        pass

