from pico2d import *

WIDTH, HEIGHT = 1920, 1080
alpha = 0.0


class Title:
    def __init__(self):
        self.image = load_image('./object/title.png')
        self.bgm = load_music('./bgm/mus_story.ogg')
        self.bgm.set_volume(32)
        self.bgm.play()

    def draw(self):
        self.image.clip_draw(0, 0, WIDTH, HEIGHT, WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    def update(self):
        global alpha
        alpha += 0.1
        pass
