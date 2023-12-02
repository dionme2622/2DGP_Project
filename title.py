from pico2d import *
from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


class Title:

    def __init__(self):
        self.image = load_image('./object/title.png')
        self.word = load_image('./object/press.png')
        self.word.opacify(0)
    def draw(self):
        self.image.clip_draw(0, 0, WIDTH, HEIGHT, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
        self.word.clip_draw(0, 0, 402, 38, 702 + 220, 260)
    def update(self):
        pass