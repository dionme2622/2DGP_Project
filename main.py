from pico2d import *
import play_mode
import game_framework
import select_mode
import help_mode
import logo_mode as start_mode
import title_mode
import gameover_mode

WIDTH, HEIGHT = 1920, 1080
# game loop

open_canvas(WIDTH, HEIGHT)
game_framework.run(start_mode)
close_canvas()

# 0finalization code
