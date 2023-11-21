from pico2d import *

import game_framework, game_world

from background import Background
from tkinter import *

from ball import Ball
from blueteam import Blueteam
from redteam import Redteam

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
select = [1, 1]
player = [[], [], [], [], [], [], [], [], [], []]
# Game object class here


def handle_events():
    global running
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            select[0] = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            select[0] = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            select[0] = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            select[0] = 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            select[0] = 5
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_1:
            select[1] = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_2:
            select[1] = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_3:
            select[1] = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_4:
            select[1] = 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_5:
            select[1] = 5

        else:
            if select[0] == 1:
                player[0].handle_event(event)
            elif select[0] == 2:
                player[1].handle_event(event)
            elif select[0] == 3:
                player[2].handle_event(event)
            elif select[0] == 4:
                player[3].handle_event(event)
            elif select[0] == 5:
                player[4].handle_event(event)
            if select[1] == 1:
                player[5].handle_event(event)
            elif select[1] == 2:
                player[6].handle_event(event)
            elif select[1] == 3:
                player[7].handle_event(event)
            elif select[1] == 4:
                player[8].handle_event(event)
            elif select[1] == 5:
                player[9].handle_event(event)
            pass
            # select_mode.player1.handle_event(event)
            # select_mode.player2.handle_event(event)


def init():
    global running
    global background
    #global player1, player2, player3, player4, player5, player6, player7, player8, player9, player10
    global player
    global ball
    global font

    font = load_font('./object/ENCR10B.TTF', 50)
    background = Background()
    game_world.add_object(background, 0)

    # Blueteam 객체 추가
    player[0] = Blueteam(300, 200, 1)
    game_world.add_object(player[0], 1)
    player[1] = Blueteam(300, 400, 2)
    game_world.add_object(player[1], 1)
    player[2] = Blueteam(300, 600, 3)
    game_world.add_object(player[2], 1)
    player[3] = Blueteam(480, 300, 4)
    game_world.add_object(player[3], 1)
    player[4] = Blueteam(480, 500, 5)
    game_world.add_object(player[4], 1)
    # Redteam 객체 추가
    player[5] = Redteam(WIDTH - 300, 200, 1)
    game_world.add_object(player[5], 1)
    player[6] = Redteam(WIDTH - 300, 400, 2)
    game_world.add_object(player[6], 1)
    player[7] = Redteam(WIDTH - 300, 600, 3)
    game_world.add_object(player[7], 1)
    player[8] = Redteam(WIDTH - 480, 300, 4)
    game_world.add_object(player[8], 1)
    player[9] = Redteam(WIDTH - 480, 500, 5)
    game_world.add_object(player[9], 1)

    ball = Ball()
    game_world.add_object(ball, 1)
    # Blueteam
    for i in range(0, 5):
        game_world.add_collision_pair('Blueteam:ball', player[i], ball)
    # Redteam
    for i in range(5, 10):
        game_world.add_collision_pair('Redteam:ball', player[i], ball)
    # game_world.add_collision_pair('player2:ball', None, ball)
    #
    # arrow = Arrow()
    # game_world.add_object(arrow, 1)
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
    font.draw(WIDTH // 2 - 50, HEIGHT // 2 + 350, f'{90- get_time():.2f}', (255, 255, 255))

    update_canvas()


def pause():
    pass


def resume():
    pass
# 게임 월드 객체들을 모두 다 업데이트
