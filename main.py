from pico2d import *

import game_control

open_canvas(1280, 1024)
game_control.init()
# game loop
while game_control.running:
    game_control.handle_events()
    game_control.update()
    game_control.draw()
    delay(0.1)
game_control.finish()
# finalization code
close_canvas()