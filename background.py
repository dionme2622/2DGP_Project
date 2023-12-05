from pico2d import load_image, load_music, load_font, get_time

import game_framework
import play_mode
import select_mode
from blueteam import Blueteam
from redteam import Redteam

WIDTH, HEIGHT = 1920, 1080


class Background:

    def __init__(self):
        self.image = load_image('./object/GROUND.png')
        self.bgm = load_music('./bgm/mus_zz_megalovania.mp3')
        self.bgm.repeat_play()

    def draw(self):
        self.image.clip_draw(0, 0, WIDTH, HEIGHT, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    def update(self):
        self.bgm.set_volume(select_mode.volume)

        pass


class Heart:
    def __init__(self):
        self.image = load_image('./character/heart.png')

    def draw(self):
        self.image.clip_draw(0, 16, 16, 16, 750, 930, 32, 32)
        self.image.clip_draw(16, 16, 16, 16, 1250, 930, 32, 32)

    def update(self):
        pass


class Icon:
    def __init__(self):
        self.image = load_image('./object/skill_icon.png')
        self.font = load_font('./object/DeterminationSansK2.ttf', 50)
        self.time = 0
    def draw(self):
        self.image.clip_draw(0, 0, 45, 45, 400, 930, 90, 90)
        self.image.clip_draw(0, 0, 45, 45, 1580, 930, 90, 90)
        if float(Blueteam.skill_wait_time) + 30 - self.time < 0:
            self.font.draw(500, 930, f'ON', (255, 255, 255))
        else:
            self.font.draw(500, 930, f'{float(Blueteam.skill_wait_time) + 30 - self.time:.1f}',
                           (255, 255, 255))
        if float(Redteam.skill_wait_time) + 30 - self.time < 0:
            self.font.draw(1450, 930, f'ON', (255, 255, 255))
        else:
            self.font.draw(1380, 930, f'{float(Redteam.skill_wait_time) + 30 - self.time:.1f}',
                           (255, 255, 255))

    def update(self):
        self.time = (self.time + game_framework.frame_time)
        pass
