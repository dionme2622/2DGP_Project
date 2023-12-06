from pico2d import *

import blueteam
import game_framework, game_world
import gameover_mode
import redteam
import select_mode
from arrow import Arrow

from background import Background, Heart, Icon

from ball import Ball
from blueteam import Blueteam
from redteam import Redteam

WIDTH, HEIGHT = 1920, 1080
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
            for i in range(0, 5):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[0] = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            for i in range(0, 5):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[0] = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            for i in range(0, 5):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[0] = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            for i in range(0, 5):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[0] = 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            for i in range(0, 5):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[0] = 5
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_1:
            for i in range(5, 10):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[1] = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_2:
            for i in range(5, 10):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[1] = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_3:
            for i in range(5, 10):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[1] = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_4:
            for i in range(5, 10):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[1] = 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_5:
            for i in range(5, 10):
                player[i].state_machine.handle_event(('LETS_STOP', 0))
            select[1] = 5
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if event.x >= 1680 and event.x <= 1920 and event.y >= 25 and event.y <= 115:
                select = 1, 1
                game_framework.change_mode(select_mode)
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


def init():
    global background, heart
    global player
    global ball
    global arrow
    global select
    global time
    global blueteam_survivor, redteam_survivor
    select = [1, 1]
    blueteam_survivor, redteam_survivor = 5, 5
    time = get_time()
    background = Background()
    game_world.add_object(background, 0)
    heart = Heart()
    game_world.add_object(heart, 0)
    icon = Icon()
    game_world.add_object(icon, 0)
    # Player 객체 추가
    add_player(player)

    ball = Ball()
    game_world.add_object(ball, 1)
    # Blueteam
    for i in range(0, 5):
        game_world.add_collision_pair('Blueteam:ball', player[i], ball)
        game_world.add_collision_pair("player:lazer", player[i], None)
    # Redteam
    for i in range(5, 10):
        game_world.add_collision_pair('Redteam:ball', player[i], ball)
        game_world.add_collision_pair("player:lazer", player[i], None)

    arrow = Arrow()
    game_world.add_object(arrow, 1)


def add_player(player):
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


def finish():
    game_world.clear()
    pass


def update():
    global getball_player, blueteam_survivor, redteam_survivor
    game_world.update()
    game_world.handle_collisions()
    if blueteam_survivor == 0:
        game_framework.change_mode(gameover_mode)
    elif redteam_survivor == 0:
        game_framework.change_mode(gameover_mode)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
# 게임 월드 객체들을 모두 다 업데이트
