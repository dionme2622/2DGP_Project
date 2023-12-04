from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework, game_world

from tkinter import *

import select_mode

WIDTH, HEIGHT = 1920, 1080


class Image:
    image = None
    def __init__(self):
        if Image.image == None:
            Image.image = load_image('./object/option.png')

    def update(self):
        pass

    def draw(self):
        Image.image.clip_draw(0, 0, 1980, 1080, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
        pass

def init():
    global sound, image
    image = Image()
    sound = 40

    game_world.add_object(image, 0)
    pass


def finish():
    game_world.clear()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if event.x >= 590 and event.x <= 845 and event.y >= 670 and event.y <= 750:
                select_mode.volume = 40
                game_framework.pop_mode()
            elif event.x >= 1110 and event.x <= 1350 and event.y >= 670 and event.y <= 750:
                select_mode.volume = 0
                game_framework.pop_mode()


def update():
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass
