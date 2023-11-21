from pico2d import load_image

from tkinter import *
import select_mode
import play_mode
root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


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
                self.image.clip_composite_draw(0, 0, 100, 100, -self.angle2, 'h', self.x, self.y, 100, 100)
        # if player_mode.player1.getball == True and select_mode.player1.shoot == False:
        #
        # elif select_mode.player2.getball == True and select_mode.player2.shoot == False:
        #     self.image.clip_composite_draw(0, 0, 100, 100, -angle2, 'h', self.x, self.y, 100, 100)
    def update(self):
        global angle1, angle2
        for i in range(0, 5):
            if play_mode.player[i].getball == True:
                self.x = play_mode.player[i].x + 100
                self.y = play_mode.player[i].y
                self.angle1 = play_mode.player[i].angle * 2 * 3.14 / 180
        for i in range(5, 10):
            if play_mode.player[i].getball == True:
                self.x = play_mode.player[i].x - 100
                self.y = play_mode.player[i].y
                self.angle2 = play_mode.player[i].angle * 2 * 3.14 / 180
        # angle1 = select_mode.player1.angle * 2 * 3.14 / 180
        # angle2 = select_mode.player2.angle * 2 * 3.14 / 180
        #
        # if select_mode.player1.getball == True and select_mode.player2.getball == False:
        #     if select_mode.player1.shoot == False:
        #         self.x = select_mode.player1.x + 100
        #         self.y = select_mode.player1.y
        #
        # elif select_mode.player1.getball == False and select_mode.player2.getball == True:
        #     if select_mode.player2.shoot == False:
        #         self.velocity = -select_mode.player2.attack_speed
        #         self.x = select_mode.player2.x - 100
        #         self.y = select_mode.player2.y



    def handle_collision(self, group, other):
        pass
