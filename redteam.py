import math
import random

from pico2d import load_image, get_time, load_font, clamp, draw_rectangle, load_wav
import game_framework
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_PERIOD, SDLK_COMMA, SDLK_SLASH, \
    SDLK_SEMICOLON, SDLK_QUOTE

import game_world
import play_mode
import select_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from function import *
from skill import Skill
import lazer

WIDTH, HEIGHT = 1920, 1080

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 당 30cm   100 pixel에 3m
RUN_SPEED_KMPH = 20.0  # 시속
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

def_cool_time = 5.0
skill_cool_time = 30.0


def Semi_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SEMICOLON


def Quote_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_QUOTE


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def atk_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_COMMA


def def_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_PERIOD


def skill_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SLASH


PI = 3.141592
radian = 10


class Idle:

    @staticmethod
    def enter(ch, e):
        ch.frame = 0
        ch.run_state = Idle

        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        if ch.run == 2:
            ch.angle += 45
        elif ch.run == 3:
            ch.angle += 0
        elif ch.run == 4:
            ch.angle += 90
        elif ch.run == 5:
            ch.angle += 135

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        if ch.run == 2:
            ch.angle -= 45
        elif ch.run == 3:
            ch.angle -= 0
        elif ch.run == 4:
            ch.angle -= 90
        elif ch.run == 5:
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
        ch.action, ch.run = 3, 3
        ch.run_state = RunRight
        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightUp:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 3, 3
        ch.run_state = RunRightUp
        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += ch.RUN_SPEED_PPS * game_framework.frame_time
        ch.y += ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunRightDown:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 3, 3
        ch.run_state = RunRightDown
        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x += ch.RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeft:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 4, 4
        ch.angle += 90
        ch.run_state = RunLeft
        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftUp:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 4, 4
        ch.angle += 90
        ch.run_state = RunLeftUp
        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= ch.RUN_SPEED_PPS * game_framework.frame_time
        ch.y += ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunLeftDown:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 4, 4
        ch.angle += 90
        ch.run_state = RunLeftDown
        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 90
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.x -= ch.RUN_SPEED_PPS * game_framework.frame_time
        ch.y -= ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunUp:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 2, 2
        ch.angle += 45
        ch.run_state = RunUp
        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian

    @staticmethod
    def exit(ch, e):
        ch.angle -= 45
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y += ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 770:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class RunDown:
    @staticmethod
    def enter(ch, e):
        ch.action, ch.run = 5, 5
        ch.angle += 135
        ch.run_state = RunDown
        if def_down(e):
            if get_time() - ch.wait_time > def_cool_time:  # get_time() - ch.time() > 5
                ch.auto_guard = False
                ch.state_machine.handle_event(('LETS_DEFENSE', 0))
        if Semi_down(e):
            ch.angle -= radian
        if Quote_down(e):
            ch.angle += radian
        pass

    @staticmethod
    def exit(ch, e):
        ch.angle -= 135
        if atk_down(e):
            ch.shoot_ball()
        if skill_down(e):
            if ch.time - Redteam.skill_wait_time > skill_cool_time:
                ch.use_skill()
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ch.y -= ch.RUN_SPEED_PPS * game_framework.frame_time
        if ch.state == 'alive':
            ch.x = clamp(WIDTH // 2 + 70, ch.x, WIDTH - 270)
            ch.y = clamp(180, ch.y, 700)
        elif ch.state == 'dead':
            if ch.x > 180 and ch.x < 240 and ch.y >= 100 and ch.y <= 780:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(50, ch.y, 800)
            elif ch.x > 180 and ch.y >= 770:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(780, ch.y, 800)
            elif ch.x > 180 and ch.y <= 125:
                ch.x = clamp(200, ch.x, WIDTH // 2 - 20)
                ch.y = clamp(50, ch.y, 100)
            else:
                ch.x = clamp(200, ch.x, 220)
                ch.y = clamp(0, ch.y, 800)

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class Attack:

    @staticmethod
    def enter(ch, e):
        ch.action = 1
        ch.frame = 0
        Redteam.atk_sound.play()

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            ch.state_machine.handle_event(('LETS_STOP', 0))

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
        Redteam.def_sound.play()

    @staticmethod
    def exit(ch, e):
        if not ch.auto_guard:
            ch.wait_time = ch.time
        else:
            ch.auto_wait_time = ch.time
    @staticmethod
    def do(ch):
        ch.frame = (ch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if ch.frame >= 2:
            ch.state_machine.handle_event(('LETS_STOP', 0))

    @staticmethod
    def draw(ch):
        if ch.frame < 1:
            ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)
        elif ch.frame >= 1:
            ch.image.clip_draw(int(ch.frame) * 32, ch.action * 52, 32, 52 - 14, ch.x, ch.y, 100, 100)



class Stop:

    @staticmethod
    def enter(ch, e):
        ch.frame = 0

    @staticmethod
    def exit(ch, e):
        pass

    @staticmethod
    def do(ch):
        pass

    @staticmethod
    def draw(ch):
        ch.image.clip_draw(int(ch.frame) * 29, ch.action * 52, 29, 52 - 14, ch.x, ch.y, 100, 100)


class StateMachine:
    def __init__(self, ch):
        self.ch = ch
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft, up_down: RunUp,
                   down_down: RunDown, up_up: RunDown, down_up: RunUp, atk_down: Attack, def_down: Idle,
                   Semi_down: Idle, Quote_down: Idle, lets_defense: Defense, skill_down: Idle, lets_stop: Stop},
            RunRight: {right_up: Idle, left_down: Idle, up_down: RunRightUp, up_up: RunRightDown,
                       down_down: RunRightDown, down_up: RunRightUp, atk_down: Attack, def_down: RunRight,
                       Semi_down: RunRight,
                       Quote_down: RunRight, lets_defense: Defense, skill_down: RunRight, lets_stop: Stop},
            RunRightUp: {up_up: RunRight, right_up: RunUp, left_down: RunUp, down_down: RunRight, atk_down: Attack,
                         def_down: RunRightUp, Semi_down: RunRightUp, Quote_down: RunRightUp,
                         lets_defense: Defense, skill_down: RunRightUp, lets_stop: Stop},
            RunUp: {up_up: Idle, left_down: RunLeftUp, down_down: Idle, right_down: RunRightUp,
                    left_up: RunRightUp, right_up: RunLeftUp, atk_down: Attack, def_down: RunUp, Semi_down: RunUp,
                    Quote_down: RunUp, lets_defense: Defense, skill_down: RunUp, lets_stop: Stop},
            RunLeftUp: {right_down: RunUp, down_down: RunLeft, left_up: RunUp, up_up: RunLeft,
                        atk_down: Attack, def_down: RunLeftUp, Semi_down: RunLeftUp, Quote_down: RunLeftUp,
                        lets_defense: Defense, skill_down: RunLeftUp, lets_stop: Stop},
            RunLeft: {left_up: Idle, up_down: RunLeftUp, right_down: Idle, down_down: RunLeftDown,
                      up_up: RunLeftDown, down_up: RunLeftUp, atk_down: Attack, def_down: RunLeft, Semi_down: RunLeft,
                      Quote_down: RunLeft, lets_defense: Defense, skill_down: RunLeft, lets_stop: Stop},
            RunLeftDown: {left_up: RunDown, down_up: RunLeft, up_down: RunLeft, right_down: RunDown,
                          atk_down: Attack, def_down: RunLeftDown, Semi_down: RunLeftDown, Quote_down: RunLeftDown,
                          lets_defense: Defense, skill_down: RunLeftDown, lets_stop: Stop},
            RunDown: {down_up: Idle, left_down: RunLeftDown, up_down: Idle, right_down: RunRightDown,
                      left_up: RunRightDown, right_up: RunLeftDown,
                      atk_down: Attack, def_down: RunDown, Semi_down: RunDown, Quote_down: RunDown,
                      lets_defense: Defense, skill_down: RunDown, lets_stop: Stop},
            RunRightDown: {right_up: RunDown, down_up: RunRight, left_down: RunDown, up_down: RunRight,
                           atk_down: Attack, def_down: RunRightDown, Semi_down: RunRightDown, Quote_down: RunRightDown,
                           lets_defense: Defense, skill_down: RunRightDown, lets_stop: Stop},
            Attack: {lets_stop: Stop},
            Defense: {lets_stop: Stop},
            Stop: { right_down: RunRight, left_down: RunLeft, up_down: RunUp,
                   down_down: RunDown, lets_defense: Defense }
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


class Redteam:
    image = None
    skill_wait_time = 0.0
    atk_sound = None
    def_sound = None
    skill_sound = None
    dead_sound = None
    out_sound = None

    def __init__(self, x, y, num):
        if Redteam.image == None:
            Redteam.image = load_image("./character/sands_red.png")
        self.x, self.y, self.num = x, y, num
        self.run = 0
        self.frame, self.action = 0, 0
        self.state = 'alive'
        self.run_state = Idle
        self.angle = 0
        self.getball = False
        self.shoot = False
        self.wait_time, self.auto_wait_time = -5.0, -15.0
        self.font = load_font('./object/DeterminationSansK2.ttf', 24)
        self.tx, self.ty = 0, 0
        self.dir = 0.0
        self.auto_guard = False
        self.time = 0.0
        self.build_behavior_tree()
        self.RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        if not Redteam.atk_sound:
            Redteam.atk_sound = load_wav('./bgm/attack.wav')
            Redteam.atk_sound.set_volume(40)
        if not Redteam.def_sound:
            Redteam.def_sound = load_wav('./bgm/defense.wav')
            Redteam.def_sound.set_volume(40)
        if not Redteam.skill_sound:
            Redteam.skill_sound = load_wav('./bgm/blaster.wav')
            Redteam.skill_sound.set_volume(40)
        if not Redteam.dead_sound:
            Redteam.dead_sound = load_wav('./bgm/dead.wav')
            Redteam.dead_sound.set_volume(20)
        if not Redteam.out_sound:
            Redteam.out_sound = load_wav('./bgm/out.wav')
            Redteam.out_sound.set_volume(20)

    def shoot_ball(self):
        if self.getball == True:
            self.getball = False
            play_mode.ball.shoot = True

    def use_skill(self):
        if self.getball == True:
            Redteam.skill_sound.play()
            Redteam.skill_wait_time = self.time
            skill = Skill(self.x, self.y, self.action, "Redteam")
            lazer.state = "Redteam"
            game_world.add_object(skill, 1)

    def get_bb(self):
        return self.x - 40, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.time += game_framework.frame_time
        if play_mode.select[1] != self.num and self.getball != True:  # 선택되지 않았다면 AI가 조작한다
            self.bt.run()
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x, self.y + 60, f'{self.num}', (255, 255, 255))
        if float(self.auto_wait_time) + 15 - self.time > 0:
            self.font.draw(self.x - 10, self.y + 80, f'{float(self.auto_wait_time) + 15 - self.time:.1f}', (255, 255, 0))
        # draw_rectangle(*self.get_bb())

    def handle_collision(self, group, other):
        if group == 'Redteam:ball':
            # 공이 바닥에 놓여있다면
            if play_mode.ball.state == 'floor':
                ball_is_floor(self)
            # 공을 블루팀이 들고있었다면
            elif play_mode.ball.state == 'Blueteam_get' and play_mode.ball.shoot == True:
                ball_is_enemy(self)
            # 공을 같은 팀이 들고있었다면
            elif play_mode.ball.state == 'Redteam_get' and play_mode.ball.shoot == True:
                ball_is_team(self)
        if group == 'player:lazer':
            if self.state == 'alive':
                # 만약 아군이 쐈으면 안전함
                if lazer.state == "Redteam":
                    pass
                elif lazer.state == "Blueteam":
                    self.hitted_from_lazor()
                # 적이 쐈으면 아웃
            pass

    def hitted_from_lazor(self):
        global survivor
        Redteam.out_sound.play()
        self.RUN_SPEED_PPS *= 2
        self.x, self.y, self.state = 200, random.randint(100, 700), 'dead'
        play_mode.redteam_survivor -= 1

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = self.RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        if math.cos(self.dir) < 0:
            self.action = 4
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            self.action = 3
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self, type):
        if type == 'Wide':
            self.tx, self.ty = random.randint(WIDTH // 2 + 200, WIDTH - 270), random.randint(180, 700)
        else:
            self.tx, self.ty = random.randint(WIDTH // 2 + 350, WIDTH - 270), random.randint(180, 700)
        return BehaviorTree.SUCCESS

    def is_alive(self):
        if self.state == 'alive':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_ball_nearby(self, distance):
        if self.distance_less_than(play_mode.ball.x, play_mode.ball.y, self.x, self.y, distance) and play_mode.ball.shoot == True:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_ball_team(self):
        if play_mode.ball.state == 'Redteam_get':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_ball_enemy(self):
        if play_mode.ball.state == 'Blueteam_get':
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


    def defense(self):
        if self.time - self.auto_wait_time > def_cool_time + 10:
            self.auto_guard = True
            self.state_machine.handle_event(('LETS_DEFENSE', 0))
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        c1 = Condition("살아있는가?", self.is_alive)
        c2 = Condition("적이 공을 갖고있는가?", self.is_ball_enemy)
        c3 = Condition("공이 몸 근처까지 날아왔는가?", self.is_ball_nearby, 3)
        c4 = Condition("아군이 공을 갖고 있는가?", self.is_ball_team)
        a1 = Action("랜덤위치지정", self.set_random_location, 'Wide')
        a2 = Action("이동", self.move_to)
        a3 = Action("공 잡기", self.defense)
        a4 = Action("랜덤위치좁게지정", self.set_random_location, 'Narrow')
        root = SEQ_defense = Sequence("공이 범위내로 들어오며 잡는다", c3, a3)

        root = SEQ_alive_and_defense = Sequence("살아있고 범위 내에 공이 날아오면 공 잡기", c1, SEQ_defense)
        root = SEQ_enemy_ball_alive_and_defense = Sequence("적이 공 갖고있고 살아있고 범위 내에 공이 날아오면 공 잡기", c2,
                                                           SEQ_alive_and_defense)

        root = SEQ_wide_wander = Sequence("넓게배회", a1, a2)
        root = SEQ_narrow_wander = Sequence("좁게배회", a4, a2)
        root = SEQ_team_ball_and_narrow_wander = Sequence("팀이 공을 갖고 있다면 좁게 배회", c4, SEQ_narrow_wander)
        root = SEL_wander_type = Selector("좁게 또는 넓게 배회", SEQ_team_ball_and_narrow_wander, SEQ_wide_wander)
        root = SEQ_wander = Sequence("살아있으면 넓게배회", c1, SEL_wander_type)

        root = SEL_defense_or_wander = Selector("배회 또는 도망", SEQ_enemy_ball_alive_and_defense, SEQ_wander)
        self.bt = BehaviorTree(root)


def ball_is_team(ch):
    play_mode.ball.shoot = False
    ch.getball = True
    for i in range(5, 10):
        play_mode.player[i].state_machine.handle_event(('LETS_STOP', 0))
    play_mode.select[1] = ch.num
    play_mode.ball.state = 'Redteam_get'
    pass


def ball_is_enemy(ch):
    global survivor
    if ch.state == 'alive':
        play_mode.ball.shoot = False
        if ch.state_machine.cur_state != Defense:  # 방어에 실패했다면
            Redteam.out_sound.play()
            ch.RUN_SPEED_PPS *= 2
            play_mode.ball.x, play_mode.ball.y = ch.x - 80, ch.y  # 맞은 플레이어 앞에 떨어진다
            ch.x, ch.y, ch.state = 200, random.randint(100, 700), 'dead'
            play_mode.redteam_survivor -= 1
            play_mode.ball.state = 'floor'
        else:  # 방어에 성공했다면
            play_mode.ball.x, play_mode.ball.y = ch.x - 80, ch.y
            play_mode.ball.state = 'floor'
    pass


def ball_is_floor(ch):
    ch.getball = True
    for i in range(5, 10):
        play_mode.player[i].state_machine.handle_event(('LETS_STOP', 0))
    play_mode.select[1] = ch.num
    play_mode.ball.state = 'Redteam_get'
    pass
