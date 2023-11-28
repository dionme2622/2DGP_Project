from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework, game_world, play_mode

from tkinter import *

import help_mode

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
PI = 3.141592
def init():
    global image, background, word
    global size_W, size_H, sradian, sangle
    global start, wevent, time
    size_W = 1980
    size_H = 1080
    sradian, sangle = 0, 0
    wevent, start = False, False
    time = 0.0
    image = load_image('./object/Select.png')
    background = load_image('./object/background.png')
    word = load_image('./object/word.png')
    pass


def finish():
    game_world.clear()
    pass


def handle_events():
    global player1
    global player2
    global start, wevent, time
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if event.x >= 320 and event.x <= 560 and event.y >= 980 and event.y <= 1060:
                wevent = True

            elif event.x >= 660 and event.x <= 900 and event.y >= 980 and event.y <= 1060:
                game_framework.change_mode(help_mode)
            elif event.x >= 1020 and event.x <= 1260 and event.y >= 980 and event.y <= 1060:
                # 옵션 모드로 이동
                pass
            elif event.x >= 1370 and event.x <= 1610 and event.y >= 980 and event.y <= 1060:
                game_framework.quit()


def update():
    global start, wevent, time
    if wevent == True:
        time = get_time()
    print(time)
    if time > 3.0:
        start = True
        wevent = False
    if start == True:
        screen_event()
    pass


def screen_event():
    global size_W, size_H, sradian, sangle
    size_W -= 1.8 * 8
    size_H -= 1 * 8
    sradian += 3
    sangle = sradian * PI / 180
    if size_W < 0 and size_H < 0:
        game_framework.change_mode(play_mode)
def draw():
    clear_canvas()
    background.draw(WIDTH//2, HEIGHT//2)
    image.clip_composite_draw(0, 0, 2702, 1542, sangle, ' ', WIDTH//2, HEIGHT//2, size_W, size_H)
    if wevent == True:
        word.clip_draw(0, 0, 835, 173, 950, 370, 1245, 200)
        # 3초 후 event = false 그리고 start = true로 만들기

    update_canvas()
    pass

def pause():
    pass


def resume():
    pass