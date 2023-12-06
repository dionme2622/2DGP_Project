from pico2d import load_image, get_events, clear_canvas, update_canvas, load_font, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

import blueteam
import game_framework
import game_world
import play_mode
import select_mode

WIDTH, HEIGHT = 1920, 1080
FRAMES_PER_ACTION = 1
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class BackGround:
    image = None
    sound = None
    dead_sound = None
    def __init__(self):
        if BackGround.image == None:
            BackGround.image = load_image('./object/select_box.png')
        if BackGround.sound == None:
            BackGround.sound = load_music('./bgm/mus_gameover.ogg')
        if BackGround.dead_sound == None:
            BackGround.dead_sound = load_music('./bgm/dead.mp3')
        BackGround.sound.set_volume(40)
        BackGround.dead_sound.set_volume(40)
        BackGround.sound.repeat_play()
    def draw(self):
        self.image.clip_draw(0, 0, WIDTH, HEIGHT, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    def update(self):
        pass

    pass


class Heart:
    image = None

    def __init__(self):
        if Heart.image == None:
            Heart.image = load_image('./character/heart.png')
        self.heart_break = False
        self.alpha = 1.0
        self.font = load_font('./object/DeterminationSansK2.ttf', 50)
        self.time = 0.0

    def draw(self):
        if not self.heart_break:
            if play_mode.blueteam_survivor == 0:
                self.image.clip_draw(0, 16, 16, 16, 990, 500, 32, 32)
            else:
                self.image.clip_draw(16, 16, 16, 16, 990, 500, 32, 32)
        else:
            if play_mode.blueteam_survivor == 0:
                self.image.clip_draw(0, 0, 20, 16, 990, 500, 32, 32)
                if self.time > 3.0:
                    self.alpha = 1.0
                    self.image.clip_draw(16, 16, 16, 16, 990, 500, 64, 64)
                    self.font.draw(950, 600, f'승리', (255, 255, 255))
            else:
                self.image.clip_draw(20, 0, 20, 16, 990, 500, 32, 32)
                if self.time > 3.0:
                    self.alpha = 1.0
                    self.image.clip_draw(0, 16, 16, 16, 990, 500, 64, 64)
                    self.font.draw(950, 600, f'승리', (255, 255, 255))

    def update(self):
        self.time = (self.time + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.time > 2.0:
            self.heart_break = True
            Heart.image.opacify(self.alpha)
            if self.alpha > 0:
                self.alpha -= 0.01
        if self.time > 3.0:
            pass

    pass


def init():
    global background, heart, font

    background = BackGround()
    game_world.add_object(background, 0)
    heart = Heart()
    game_world.add_object(heart, 1)
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
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if event.x >= 1680 and event.x <= 1920 and event.y >= 25 and event.y <= 115:
                game_framework.change_mode(select_mode)
    pass


def update():
    game_world.update()
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
