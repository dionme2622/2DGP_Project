from pico2d import load_image

PIXEL_PER_METER = (20.0 / 0.6)  # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 15.0  # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Sands:

    def __init__(self):
        self.hp, self.mp, self.speed, self.attack_speed = 3, 0, 3, 30
        self.frame = 0
        self.dirX = 0
        self.dirY = 0
        self.action = 1
        self.dir_left, self.dir_right, self.dir_up, self.dir_down = 0, 0, 0, 0
        self.image = load_image('./character/sands.png')
        self.FRAMES_PER_ACTION = FRAMES_PER_ACTION
        self.RUN_SPEED_PPS = RUN_SPEED_PPS * self.speed
        self.ACTION_PER_TIME = ACTION_PER_TIME
        self.job = "sands"
    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        pass
