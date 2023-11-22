from pico2d import *
import play_mode as start_mode, game_framework
from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
# game loop
open_canvas(WIDTH, HEIGHT)
game_framework.run(start_mode)
close_canvas()

# 0finalization code
