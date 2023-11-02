from pico2d import *

import sands
import game_world
from background import Background
from player1 import Sands, Pinkbean, Gray
from player2 import Sands, Pinkbean, Gray
# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False




def init():
    global running
    global background

    background = Background()
    game_world.add_object(background, 0)

    player1 = Sands()
    game_world.add_object(player1, 1)
    player2 = Sands()
    game_world.add_object(player2, 1)

    running = True
def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
# 게임 월드 객체들을 모두 다 업데이트

