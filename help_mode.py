from pico2d import load_image, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT
import game_framework, game_world

WIDTH, HEIGHT = 1920, 1080


def init():
    global image
    image = load_image('./object/help.png')
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
            if event.x >= 1700 and event.x <= 1920 and event.y >= 945 and event.y <= 1045:
                game_framework.pop_mode()


def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 1375, 640, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass
