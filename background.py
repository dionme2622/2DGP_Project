from pico2d import load_image
WIDTH, HEIGHT = 1280, 1024


class Background:

    def __init__(self):
        self.image = load_image('GROUND.png')

    def draw(self):
        self.image.clip_draw(0, 0, 1684, 846, WIDTH // 2, HEIGHT // 2 + 10, WIDTH, HEIGHT)

    def update(self):
        pass