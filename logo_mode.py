from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time
from pico2d import *
import game_framework
import title_mode
from tkinter import *

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
alpha = 0.0
alpha_increase = 0.005
def init():
    global image, background
    global logo_start_time
    global alpha
    background = load_image('./object/logo_mode_background.png')
    image = load_image('./object/tuk_credit.png')
    logo_start_time = get_time()


    pass


def finish():
    pass


def handle_events():
    pass


def update():
    global alpha, alpha_increase
    if alpha < 1.0:
        alpha += alpha_increase
    image.opacify(alpha)
    if get_time() - logo_start_time >= 5.0:
        game_framework.change_mode(title_mode)
    pass


def draw():
    clear_canvas()
    background.draw(WIDTH // 2, HEIGHT // 2)
    image.clip_draw(0, 0, 800, 600, WIDTH // 2, HEIGHT // 2, 2000, 1500)
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass