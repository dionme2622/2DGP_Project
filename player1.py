from pico2d import load_image

import game_framework
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_r, SDLK_d, SDLK_f, SDLK_g


def r_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r


def r_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_r


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f


def f_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_f


def g_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_g


def g_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_g


def lets_idle(e):
    return e[0] == 'LETS_IDLE'





class Idle:

    @staticmethod
    def enter(ch, e):
        ch.dir_x = 0
        ch.frame = 0
        ch.action = 1
        pass

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_composite_draw(int(ch.frame) * 250, ch.action * 420, 250, 330, 0, 'h',
                                            ch.x, ch.y, 100, 150)


class Run:

    @staticmethod
    def enter(ch, e):
        if g_down(e):
            ch.dir_right = 1
            ch.dirX, ch.action = 1, 1
        elif d_down(e):
            ch.dir_left = 1
            ch.dirX, ch.action = -1, 1
        elif r_down(e):
            ch.dir_up = 1
            ch.dirY, ch.action = 1, 1
        elif f_down(e):
            ch.dir_down = 1
            ch.dirY, ch.action = -1, 1

        elif g_up(e):
            ch.dir_right = 0
            ch.dirX = 0

            if ch.dir_left == 1:
                ch.dirX, ch.action = -1, 1
            elif ch.dir_up == 1:
                ch.dirX, ch.dirY, ch.action = 0, 1, 1
            elif ch.dir_down == 1:
                ch.dirX, ch.dirY, ch.action = 0, -1, 1
        elif d_up(e):
            ch.dir_left = 0
            ch.dirX = 0
            if ch.dir_right == 1:
                ch.dirX, ch.action = 1, 1
            elif ch.dir_up == 1:
                ch.dirX, ch.dirY, ch.action = 0, 1, 1
            elif ch.dir_down == 1:
                ch.dirX, ch.dirY, ch.action = 0, -1, 1
        elif r_up(e):
            ch.dir_up = 0
            ch.dirY = 0
            if ch.dir_down == 1:
                ch.dirY, ch.action = -1, 1
            elif ch.dir_right == 1:
                ch.dirX, ch.dirY, ch.action = 1, 0, 1
            elif ch.dir_left == 1:
                ch.dirX, ch.dirY, ch.action = -1, 0, 1

        elif f_up(e):
            ch.dir_down = 0
            ch.dirY = 0
            if ch.dir_up == 1:
                ch.dirY, ch.action = 1, 1
            elif ch.dir_right == 1:
                ch.dirX, ch.dirY, ch.action = 1, 0, 1
            elif ch.dir_left == 1:
                ch.dirX, ch.dirY, ch.action = -1, 0, 1

        if ch.dir_left == 0 and ch.dir_right == 0 and ch.dir_up == 0 and ch.dir_down == 0:
            ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + ch.FRAMES_PER_ACTION * ch.ACTION_PER_TIME * game_framework.frame_time) % 4
        if ch.x >= 620:
            ch.x = 620
        elif ch.x <= 50:
            ch.x = 50
        ch.x += ch.dirX * ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.y >= 800:
            ch.y = 800
        elif ch.y <= 80:
            ch.y = 80
        ch.y += ch.dirY * ch.RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(ch):
        ch.image.clip_composite_draw(int(ch.frame) * 250, ch.action * 420, 250, 330, 0, 'h',
                                            ch.x, ch.y, 100, 150)


class StateMachine:
    def __init__(self, ch):
        self.ch = ch
        self.cur_state = Idle
        self.transitions = {
            Idle: {g_down: Run, d_down: Run, g_up: Run, d_up: Run, r_down: Run, r_up: Run,
                   f_down: Run, f_up: Run},
            Run: {g_down: Run, d_down: Run, g_up: Run, d_up: Run, r_down: Run,
                  r_up: Run, f_down: Run, f_up: Run, lets_idle: Idle}
        }

    def start(self):
        self.cur_state.enter(self.ch, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.ch)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ch, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ch, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.ch)

class Player1:
    def __init__(self, ch):
        self.x, self.y = 50, 500
        self.hp, self.mp, self.speed, self.attack_speed = ch.hp, ch.mp, ch.speed, ch.attack_speed
        self.frame = ch.frame
        self.action = ch.action  # 오른쪽 IDLE
        self.dirX = ch.dirX
        self.dirY = ch.dirY
        self.face_dir = -1  # 왼쪽 방향 얼굴을 향하고 있음
        self.image = ch.image
        self.dir_left, self.dir_right, self.dir_up, self.dir_down = ch.dir_left, ch.dir_right, ch.dir_up, ch.dir_down
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.FRAMES_PER_ACTION = ch.FRAMES_PER_ACTION
        self.ACTION_PER_TIME = ch.ACTION_PER_TIME
        self.RUN_SPEED_PPS = ch.RUN_SPEED_PPS
    def update(self):
        self.state_machine.update()
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
