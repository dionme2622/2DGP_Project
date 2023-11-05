from pico2d import *

import play_mode as start_mode
import game_framework

# game loop
open_canvas(1280, 1024)
game_framework.run(start_mode)
close_canvas()

# finalization code
