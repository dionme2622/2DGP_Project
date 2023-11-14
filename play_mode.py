from pico2d import *

import game_framework
from ball import Ball
from gray import Gray

from player1 import Player1
from player2 import Player2
from sands import Sands
import game_world
from background import Background
from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player1.handle_event(event)
            player2.handle_event(event)
            # select_mode.player1.handle_event(event)
            # select_mode.player2.handle_event(event)


def init():
    global running
    global background
    global player1, player2
    global ball
    global font
    font = load_font('./object/ENCR10B.TTF', 50)
    background = Background()
    game_world.add_object(background, 0)

    player1 = Player1(Gray())
    game_world.add_object(player1, 1)
    game_world.add_collision_pair('player1:ball', player1, None)
    player2 = Player2(Sands())
    game_world.add_object(player2, 1)
    game_world.add_collision_pair('player2:ball', player2, None)

    ball = Ball(player1.x + 100, player1.y, 5)
    game_world.add_object(ball, 1)
    game_world.add_collision_pair('player1:ball', None, ball)
    game_world.add_collision_pair('player2:ball', None, ball)

    running = True


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    font.draw(WIDTH // 2 - 50, HEIGHT // 2 + 350, f'{90- get_time():.2f}', (0, 0, 0))

    update_canvas()


def pause():
    pass


def resume():
    pass
# 게임 월드 객체들을 모두 다 업데이트
