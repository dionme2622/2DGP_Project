from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time
from pico2d import *
import game_framework
import title_mode
from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

def init():
    global image
    global logo_start_time
    image = load_image('./object/tuk_credit.png')
    logo_start_time = get_time()
    pass


def finish():
    pass


def handle_events():
    events = get_events()
    pass


def update():
    global running

    if get_time() - logo_start_time >= 5.0:
        game_framework.change_mode(title_mode)
    pass


def draw():
    clear_canvas()

    image.clip_draw(0, 0, 800, 600, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    update_canvas()
    pass


def pause():
    pass


def resume():
    pass