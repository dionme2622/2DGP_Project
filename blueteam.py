# from pico2d import load_image, draw_rectangle, get_time, load_font, clip_draw
import random

from pico2d import *
import game_framework
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_r, SDLK_d, SDLK_f, SDLK_g, SDLK_q, SDLK_w, SDLK_a, SDLK_s
from tkinter import *

import game_world
import play_mode
from ball import Ball
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

root = Tk()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 45.0  # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


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


def atk_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q


def def_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def lets_idle(e):
    return e[0] == 'LETS_IDLE'


def lets_defense(e):
    return e[0] == 'LETS_DEFENSE'


class Idle:
    @staticmethod
    def enter(ch, e):
        ch.frame = 0
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
        if ch.action == 2:
            ch.angle += 45
        elif ch.action == 3:
            ch.angle += 0
        elif ch.action == 4:
            ch.angle += 90
        elif ch.action == 5:
            ch.angle += 135

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if ch.action == 2:
            ch.angle -= 45
        elif ch.action == 3:
            ch.angle -= 0
        elif ch.action == 4:
            ch.angle -= 90
        elif ch.action == 5:
            ch.angle -= 135
        pass

    @staticmethod
    def do(ch):
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRight:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(300, ch.x, WIDTH // 2 - 20)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > WIDTH - 190 and ch.x < WIDTH - 130 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y >= 770:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y <= 125:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(0, ch.y, 800)

        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(300, ch.x, WIDTH // 2 - 20)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > WIDTH - 190 and ch.x < WIDTH - 130 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y >= 770:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y <= 125:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 3
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(300, ch.x, WIDTH // 2 - 20)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > WIDTH - 190 and ch.x < WIDTH - 130 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y >= 770:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y <= 125:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeft:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        ch.angle += 90
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(300, ch.x, WIDTH // 2 - 20)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > WIDTH - 190 and ch.x < WIDTH - 130 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y >= 770:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y <= 125:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        ch.angle += 90
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(300, ch.x, WIDTH // 2 - 20)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > WIDTH - 190 and ch.x < WIDTH - 130 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y >= 770:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y <= 125:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(0, ch.y, 800)
    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 4
        ch.angle += 90
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(300, ch.x, WIDTH // 2 - 20)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > WIDTH - 190 and ch.x < WIDTH - 130 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y >= 770:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y <= 125:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(0, ch.y, 800)
    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunUp:
    @staticmethod
    def enter(ch, e):
        ch.action = 2
        ch.angle += 45
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
            print("증가")
        if s_down(e):
            ch.angle -= 5
        print(ch.angle)

    @staticmethod
    def exit(ch, e):
        ch.angle -= 45
        if atk_down(e):
            ch.shoot_ball()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y += RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(300, ch.x, WIDTH // 2 - 20)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > WIDTH - 190 and ch.x < WIDTH - 130 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y >= 770:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y <= 125:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunDown:
    @staticmethod
    def enter(ch, e):
        ch.action = 5
        ch.angle += 135
        print("각도 270 증가")
        if def_down(e):
            if get_time() - ch.wait_time > 2.0:  # get_time() - ch.time() > 5
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if a_down(e):
            ch.angle += 5
        if s_down(e):
            ch.angle -= 5
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 135
        if atk_down(e):
            ch.shoot_ball()

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y -= RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(300, ch.x, WIDTH // 2 - 20)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > WIDTH - 190 and ch.x < WIDTH - 130 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y >= 770:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x < WIDTH - 130 and ch.y <= 125:
                ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 170)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(WIDTH - 170, ch.x, WIDTH - 150)
                ch.y = clamp(0, ch.y, 800)


    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class Attack:

    @staticmethod
    def enter(ch, e):
        ch.action = 1
        ch.frame = 0

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        if ch.frame < 1:
            ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)
        elif ch.frame >= 1:
            ch.image.clip_draw(int(ch.frame) * 32, ch.action * 52, 32, 52 - 14, ch.x, ch.y, 100, 100)


class Defense:
    @staticmethod
    def enter(ch, e):
        ch.action = 1
        ch.frame = 0

    @staticmethod
    def exit(ch, e):
        ch.wait_time = get_time()

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        if ch.frame < 1:
            ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)
        elif ch.frame >= 1:
            ch.image.clip_draw(int(ch.frame) * 32, ch.action * 52, 32, 52 - 14, ch.x, ch.y, 100, 100)


class Damage:

    @staticmethod
    def enter(ch, e):
        ch.action = 0
        ch.frame = 0

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            ch.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class StateMachine:
    def __init__(self, ch):
        self.ch = ch
        self.cur_state = Idle
        self.transitions = {
            Idle: {g_down: RunRight, d_down: RunLeft, d_up: RunRight, g_up: RunLeft, r_down: RunUp,
                   f_down: RunDown, r_up: RunDown, f_up: RunUp, atk_down: Attack, def_down: Idle, a_down: Idle,
                   s_down: Idle, lets_defense: Defense},
            RunRight: {g_up: Idle, d_down: Idle, r_down: RunRightUp, r_up: RunRightDown,
                       f_down: RunRightDown, f_up: RunRightUp, atk_down: Attack, def_down: RunRight, a_down: RunRight,
                       s_down: RunRight, lets_defense: Defense},
            RunRightUp: {r_up: RunRight, g_up: RunUp, d_down: RunUp, f_down: RunRight, atk_down: Attack,
                         def_down: RunRightUp, a_down: RunRightUp, s_down: RunRightUp, lets_defense: Defense},
            RunUp: {r_up: Idle, d_down: RunLeftUp, f_down: Idle, g_down: RunRightUp,
                    d_up: RunRightUp, g_up: RunLeftUp, atk_down: Attack, def_down: RunUp, a_down: RunUp, s_down: RunUp,
                    lets_defense: Defense},
            RunLeftUp: {g_down: RunUp, f_down: RunLeft, d_up: RunUp, r_up: RunLeft,
                        atk_down: Attack, def_down: RunLeftUp, a_down: RunLeftUp, s_down: RunLeftUp,
                        lets_defense: Defense},
            RunLeft: {d_up: Idle, r_down: RunLeftUp, g_down: Idle, f_down: RunLeftDown,
                      r_up: RunLeftDown, f_up: RunLeftUp, atk_down: Attack, def_down: RunLeft, a_down: RunLeft,
                      s_down: RunLeft, lets_defense: Defense},
            RunLeftDown: {d_up: RunDown, f_up: RunLeft, r_down: RunLeft, g_down: RunDown,
                          atk_down: Attack, def_down: RunLeftDown, a_down: RunLeftDown, s_down: RunLeftDown,
                          lets_defense: Defense},
            RunDown: {f_up: Idle, d_down: RunLeftDown, r_down: Idle, g_down: RunRightDown,
                      d_up: RunRightDown, g_up: RunLeftDown,
                      atk_down: Attack, def_down: RunDown, a_down: RunDown, s_down: RunDown, lets_defense: Defense},
            RunRightDown: {g_up: RunDown, f_up: RunRight, d_down: RunDown, r_down: RunRight,
                           atk_down: Attack, def_down: RunRightDown, a_down: RunRightDown, s_down: RunRightDown,
                           lets_defense: Defense},
            Attack: {lets_idle: Idle},
            Defense: {lets_idle: Idle},
            Damage: {lets_idle: Idle},
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


class Blueteam:
    image = None

    def __init__(self, x, y, num):
        if Blueteam.image == None:
            Blueteam.image = load_image("./character/sands_blue.png")
        self.x, self.y, self.num = x, y, num
        self.state = 'alive'
        self.frame, self.action = 0, 0
        self.angle = 0
        self.getball = False
        self.shoot = False
        self.wait_time = -2.0
        self.font = load_font('./object/ENCR10B.TTF', 30)
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def shoot_ball(self):
        if self.getball == True:
            self.getball = False
            play_mode.ball.shoot = True

    def get_bb(self):
        return self.x - 40, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.state_machine.update()
        if play_mode.select[0] != self.num:     # 선택되지 않았다면 AI가 조작한다
            self.bt.run()
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x, self.y + 70, f'{self.num}', (255, 255, 255))
        draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'Blueteam:ball':
            if play_mode.ball.state == 'floor':  # 공이 바닥에 놓여져있다면
                print("블루팀 공 주움")
                self.getball = True
                play_mode.ball.state = 'Blueteam_get'
            elif play_mode.ball.state == 'Redteam_get' and play_mode.ball.shoot == True:  # 공을 적 팀이 들고있었다면
                if self.state == 'alive':
                    play_mode.ball.shoot = False
                    if self.state_machine.cur_state != Defense:
                        play_mode.ball.x, play_mode.ball.y = self.x, self.y  # 맞은 플레이어 앞에 떨어진다
                        self.state_machine.cur_state = Damage
                        self.x, self.y, self.state = WIDTH - 180, 400, 'dead'
                        play_mode.ball.state = 'floor'
                    else:
                        self.getball = True
            elif play_mode.ball.state == 'Blueteam_get' and play_mode.ball.shoot == True:  # 공을 같은 팀이 들고있었다면
                self.getball = True
                play_mode.ball.shoot = False
        pass
    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2


    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        #self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx, self.ty = random.randint(300, WIDTH // 2 - 20), random.randint(180, 700)
        return BehaviorTree.SUCCESS


    def is_alive(self):
        if self.state == 'alive':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_ball_nearby(self, distance):
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.boy.x, play_mode.boy.y)
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING



    def flee(self):
        self.state = 'Walk'
        # 소년으로부터 멀어지는 방향
        self.dir = math.atan2(self.y - play_mode.boy.y, self.x - play_mode.boy.x)

        # 살짝 이동
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

        return BehaviorTree.RUNNING
        pass
    def build_behavior_tree(self):
        a1 = Action("랜덤위치지정", self.set_random_location)
        a2 = Action("이동", self.move_to)
        root = SEQ_wander = Sequence("Wander", a1, a2)
        c1 = Condition("살아있는가?", self.is_alive)
        root = SEQ_wander = Sequence("살아있으면 배회", c1, SEQ_wander)




        self.bt = BehaviorTree(root)

def remove_shoot(beg, end):
    for i in range(beg, end):
        play_mode.player[i].shoot = False
