from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_a, SDLK_1, SDLK_2

import game_framework
import game_world
import play_mode
from sands import Sands


def init():
    global image
    image = load_image('GROUND.png')
    pass


def finish():
    pass


def handle_events():
    global player1
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            player1 = Sands("player1")
            game_world.add_object(player1, 1)
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass

def pause():
    pass


def resume():
    pass