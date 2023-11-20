from pico2d import load_image
from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()


class Background:

    def __init__(self):
        self.image = load_image('./object/GROUND.png')

    def draw(self):
        self.image.clip_draw(0, 0, WIDTH, HEIGHT, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    def update(self):
        pass