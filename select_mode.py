from pico2d import load_image, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework, game_world, play_mode

from tkinter import *

import help_mode

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

def init():
    global image
    image = load_image('./object/Select.png')
    pass


def finish():
    pass


def handle_events():
    global player1
    global player2
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if event.x >= 320 and event.x <= 560 and event.y >= 980 and event.y <= 1060:
                game_framework.change_mode(play_mode)
            elif event.x >= 660 and event.x <= 900 and event.y >= 980 and event.y <= 1060:
                game_framework.change_mode(help_mode)
            elif event.x >= 1020 and event.x <= 1260 and event.y >= 980 and event.y <= 1060:
                # 옵션 모드로 이동
                pass
            elif event.x >= 1370 and event.x <= 1610 and event.y >= 980 and event.y <= 1060:
                game_framework.quit()
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
        #     # 플레이어1 핑크빈 선택
        #     pass
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
        #     player1 = Player1(Sands())
        #     game_world.add_object(player1, 1)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
        #     player1 = Player1(Gray())
        #     game_world.add_object(player1, 1)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
        #     # 플레이어2 핑크빈 선택
        #     pass
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
        #     player2 = Player2(Sands())
        #     game_world.add_object(player2, 1)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_6:
        #     player2 = Player2(Gray())
        #     game_world.add_object(player2, 1)



def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 2702, 1542, WIDTH//2, HEIGHT//2, WIDTH, HEIGHT)
    update_canvas()
    pass

def pause():
    pass


def resume():
    pass