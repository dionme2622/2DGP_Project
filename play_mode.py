from pico2d import *

import game_framework, game_world

from background import Background
from tkinter import *
from blueteam import Blueteam
from redteam import Redteam

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
select = [1, 1]
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
                player1.handle_event(event)
            elif select[0] == 2:
                player2.handle_event(event)
            elif select[0] == 3:
                player3.handle_event(event)
            elif select[0] == 4:
                player4.handle_event(event)
            elif select[0] == 5:
                player5.handle_event(event)
            if select[1] == 1:
                player6.handle_event(event)
            elif select[1] == 2:
                player7.handle_event(event)
            elif select[1] == 3:
                player8.handle_event(event)
            elif select[1] == 4:
                player9.handle_event(event)
            elif select[1] == 5:
                player10.handle_event(event)
            pass
            # select_mode.player1.handle_event(event)
            # select_mode.player2.handle_event(event)


def init():
    global running
    global background
    global player1, player2, player3, player4, player5, player6, player7, player8, player9, player10
    global ball
    global font

    font = load_font('./object/ENCR10B.TTF', 50)
    background = Background()
    game_world.add_object(background, 0)

    player1 = Blueteam(300, 200)
    game_world.add_object(player1, 1)
    player2 = Blueteam(300, 400)
    game_world.add_object(player2, 1)
    player3 = Blueteam(300, 600)
    game_world.add_object(player3, 1)
    player4 = Blueteam(480, 300)
    game_world.add_object(player4, 1)
    player5 = Blueteam(480, 500)
    game_world.add_object(player5, 1)

    player6 = Redteam(WIDTH - 300, 200)
    game_world.add_object(player6, 1)
    player7 = Redteam(WIDTH - 300, 400)
    game_world.add_object(player7, 1)
    player8 = Redteam(WIDTH - 300, 600)
    game_world.add_object(player8, 1)
    player9 = Redteam(WIDTH - 480, 300)
    game_world.add_object(player9, 1)
    player10 = Redteam(WIDTH - 480, 500)
    game_world.add_object(player10, 1)
    # ball = Ball(select_mode.player1.x + 100, select_mode.player1.y, 5)
    # game_world.add_object(ball, 1)
    # game_world.add_collision_pair('player1:ball', None, ball)
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
