from pico2d import load_image, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_z, SDLK_RETURN

import game_framework
import game_world
from title import Title
import select_mode

WIDTH, HEIGHT = 1920, 1080
alpha = 0.0
alpha_increase = 0.01


def init():
    global title, word
    title = Title()
    word = load_image('./object/press.png')

    game_world.add_object(title, 0)
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.change_mode(select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            game_framework.change_mode(select_mode)
    pass


def update():
    global alpha, alpha_increase
    if alpha > 1.0:
        alpha_increase *= -1
    elif alpha < 0.0:
        alpha_increase *= -1
    alpha += alpha_increase
    word.opacify(alpha)
    pass


def draw():
    clear_canvas()
    game_world.render()
    word.clip_draw(0, 0, 402, 38, 702 + 220, 260)
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass
