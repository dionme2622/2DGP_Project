from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework, game_world, play_mode

from tkinter import *

import select_mode

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
import tkinter as tk
from tkinter import ttk

def init():
    global sound, image
    image = load_image('./object/option.png')
    sound = 40
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
    image.clip_draw(0, 0, 1980, 1080, WIDTH//2, HEIGHT//2, WIDTH, HEIGHT)
    update_canvas()
    pass

def pause():
    pass


def resume():
    pass