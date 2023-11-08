from pico2d import load_image

PIXEL_PER_METER = (20.0 / 0.6)  # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 40.0  # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER
# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Gray:

    def __init__(self):
        self.x, self.y = 400, 400
        self.hp, self.mp, self.speed, self.attack_speed = 3, 0, 3, 3
        self.frame = 0
        self.dirX = 0
        self.dirY = 0
        self.action = 1
        self.face_dir = 1  # 오른쪽 방향 얼굴을 향하고 있음
        self.dir_left, self.dir_right, self.dir_up, self.dir_down = 0, 0, 0, 0
        self.image = load_image('GROUND.png')
        self.FRAMES_PER_ACTION = FRAMES_PER_ACTION
        self.ACTION_PER_TIME = ACTION_PER_TIME
        self.RUN_SPEED_PPS = RUN_SPEED_PPS
    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        pass
