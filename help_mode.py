from pico2d import load_image, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
import game_framework, game_world, play_mode

from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

def init():
    global image
    image = load_image('./object/help.png')
    pass


def finish():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()



def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 1375, 640, WIDTH//2, HEIGHT//2, WIDTH, HEIGHT)
    update_canvas()
    pass

def pause():
    pass


def resume():
    pass